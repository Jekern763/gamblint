use rayon::prelude::*;
use std::fs::{OpenOptions, create_dir_all};
use std::io::{BufWriter, Write};
use std::time::{Duration, Instant};
use sysinfo::System;

// ---------------------------------------------------------------------------
// Tunables
// ---------------------------------------------------------------------------

/// Never plan to use the last chunk of RAM: OS, Rayon, allocator slack, etc.
const RESERVE_MIN_BYTES: usize = 1536 * 1024 * 1024;
/// ...or this fraction of available RAM, whichever is larger (1/N).
const RESERVE_FRACTION_DIV: usize = 10;
/// One chunk buffer is 1/CHUNKS_PER_PENDING of the pending buffer's capacity.
const CHUNKS_PER_PENDING: usize = 3;
/// If the planned chunk gets smaller than this, we are out of memory budget.
const MIN_CHUNK_ELEMS: usize = 4_000_000;

/// Master buckets: this many per Rayon thread (more buckets = better load
/// balance, since each bucket merge is one serial task).
const BUCKETS_PER_THREAD: usize = 8;
const MAX_BUCKETS: usize = 4096;
/// Don't make buckets smaller than this many elements at the first collapse
/// (small n therefore gets a single bucket).
const MIN_BUCKET_ELEMS: usize = 1 << 16;

/// Minimum seconds between chunk progress lines (first and last chunk always
/// print; collapse/replan lines always print).
const PROGRESS_MIN_INTERVAL_SECS: f64 = 2.0;
/// Width of the ASCII progress bar.
const BAR_WIDTH: usize = 24;

/// OEIS A175176, a(0)..a(14): number of vector sums of two permutations of 1..n.
const KNOWN_A: [u64; 15] = [
    1,
    1,
    3,
    19,
    201,
    3081,
    62663,
    1598185,
    49158651,
    1772832643,
    73394322615,
    3431751900897,
    178904412061235,
    10290301519034057,
    647401635395456919,
];

const GIB: f64 = 1024.0 * 1024.0 * 1024.0;

// ---------------------------------------------------------------------------
// Formatting helpers
// ---------------------------------------------------------------------------

/// 65841128640 -> "65,841,128,640"
fn fmt_int(x: u64) -> String {
    let s = x.to_string();
    let mut out = String::with_capacity(s.len() + s.len() / 3);
    for (i, ch) in s.chars().enumerate() {
        if i > 0 && (s.len() - i) % 3 == 0 {
            out.push(',');
        }
        out.push(ch);
    }
    out
}

/// 1_772_832_643.0 -> "1.77B"
fn fmt_short(x: f64) -> String {
    let (v, suffix) = if x >= 1e12 {
        (x / 1e12, "T")
    } else if x >= 1e9 {
        (x / 1e9, "B")
    } else if x >= 1e6 {
        (x / 1e6, "M")
    } else if x >= 1e3 {
        (x / 1e3, "K")
    } else {
        return format!("{:.0}", x);
    };
    format!("{:.2}{}", v, suffix)
}

fn fmt_gib(bytes: usize) -> String {
    format!("{:.2} GiB", bytes as f64 / GIB)
}

/// Seconds -> "850ms" / "4.2s" / "12m03s" / "1h02m03s"
fn fmt_secs(secs: f64) -> String {
    if secs < 1.0 {
        format!("{:.0}ms", secs * 1000.0)
    } else if secs < 60.0 {
        format!("{:.1}s", secs)
    } else if secs < 3600.0 {
        let total = secs as u64;
        format!("{}m{:02}s", total / 60, total % 60)
    } else {
        let total = secs as u64;
        format!(
            "{}h{:02}m{:02}s",
            total / 3600,
            (total % 3600) / 60,
            total % 60
        )
    }
}

fn progress_bar(frac: f64, width: usize) -> String {
    let filled = (frac.clamp(0.0, 1.0) * width as f64).round() as usize;
    format!("{}{}", "#".repeat(filled), "-".repeat(width - filled))
}

// ---------------------------------------------------------------------------
// Memory planning
// ---------------------------------------------------------------------------

struct Plan {
    /// Max raw pair sums per chunk buffer.
    chunk_elems: usize,
    /// Max values held in `pending` before we must collapse into `master`.
    pending_cap: usize,
    /// Available memory (bytes) at the time the plan was made.
    avail_bytes: usize,
}

/// Re-reads available memory and derives chunk/pending sizes.
///
/// `available_memory()` is measured fresh, so it already EXCLUDES what
/// `master` currently occupies -- nothing needs subtracting.
///
/// Worst-case peaks this plan protects against (in u64 elements):
///   collapse : pending + growth of master by <= pending   = 2 * pending_cap
///   chunking : chunk buffer + pending                     <= 2 * pending_cap
/// so pending_cap = usable / 2.
///
/// (Buckets grow independently, so any realloc-with-copy only ever needs
/// old+new size of ONE bucket per thread, not of the whole master.)
fn plan_memory(sys: &mut System, master_len: usize) -> Result<Plan, String> {
    sys.refresh_memory();
    let avail = sys.available_memory() as usize;
    let reserve = RESERVE_MIN_BYTES.max(avail / RESERVE_FRACTION_DIV);
    let usable_elems = avail.saturating_sub(reserve) / 8;

    let pending_cap = usable_elems / 2;
    let chunk_elems = pending_cap / CHUNKS_PER_PENDING;

    if chunk_elems < MIN_CHUNK_ELEMS {
        return Err(format!(
            "out of memory budget: master already holds {} values ({}) and only \
             {} is available (reserve {}). The fully deduplicated set does \
             not fit in RAM on this machine.",
            fmt_int(master_len as u64),
            fmt_gib(master_len * 8),
            fmt_gib(avail),
            fmt_gib(reserve)
        ));
    }
    Ok(Plan {
        chunk_elems,
        pending_cap,
        avail_bytes: avail,
    })
}

// ---------------------------------------------------------------------------
// Packing / permutations
// ---------------------------------------------------------------------------

/// Bits needed per coordinate so that a sum of `max_k` values <= n never
/// carries into the neighbouring field.
fn bits_per_dim_for(n: u32, max_k: u32) -> u32 {
    let max_val = max_k * n;
    (u32::BITS - max_val.leading_zeros()).max(1)
}

/// Heap's algorithm.
fn heap_permutation(c: &mut [u64], f: &mut impl FnMut(&[u64])) {
    let n = c.len();
    let mut counters = vec![0usize; n];
    f(c);
    let mut i = 0usize;
    while i < n {
        if counters[i] < i {
            if i % 2 == 0 {
                c.swap(0, i);
            } else {
                c.swap(counters[i], i);
            }
            f(c);
            counters[i] += 1;
            i = 0;
        } else {
            counters[i] = 0;
            i += 1;
        }
    }
}

/// Packs each permutation into a u64. Coordinate 0 goes in the HIGHEST field,
/// so dropping trailing coordinates is a right shift that preserves sort order.
/// Packs each permutation into a u64 in parallel.
/// Maps starting prefixes across Rayon's thread pool to utilize all 192 cores.
fn generate_and_pack_permutations(n: usize, bits: u32) -> Vec<u64> {
    let expected_len = (1..=n).product::<usize>();

    // We parallelize by generating the suffixes for each unique starting element
    let final_out: Vec<Vec<u64>> = (0..n)
        .into_par_iter()
        .map(|first_element_idx| {
            let first_val = (first_element_idx + 1) as u64;

            // Build the remaining pool of elements for this thread
            let mut pool = Vec::with_capacity(n - 1);
            for v in 1..=n as u64 {
                if v != first_val {
                    pool.push(v);
                }
            }

            // Local thread storage for this root block
            let block_size = expected_len / n;
            let mut local_block = Vec::with_capacity(block_size);

            // Run standard Heap's algorithm on the remaining elements
            heap_permutation(&mut pool, &mut |suffix| {
                let mut packed = first_val << ((n - 1) as u32 * bits);
                for (idx, &val) in suffix.iter().enumerate() {
                    packed |= val << ((n - 2 - idx) as u32 * bits);
                }
                local_block.push(packed);
            });

            local_block
        })
        .collect();

    // Flatten the parallel blocks into one continuous flat vector
    let mut out = Vec::with_capacity(expected_len);
    for mut block in final_out {
        out.append(&mut block);
    }
    out
}

/// Fills `buf` with the upper-triangle pair sums for rows start_i..end_i.
/// Row i has (b_len - i) entries: base[i] + base[i..].
fn generate_chunk_symmetric(base: &[u64], start_i: usize, end_i: usize, buf: &mut [u64]) {
    let b_len = base.len();
    let mut rows: Vec<(usize, &mut [u64])> = Vec::with_capacity(end_i - start_i);
    let mut rest = buf;
    for i in start_i..end_i {
        let (row, tail) = rest.split_at_mut(b_len - i);
        rows.push((i, row));
        rest = tail;
    }
    rows.into_par_iter().for_each(|(i, row)| {
        let vi = base[i];
        for (slot, &vb) in row.iter_mut().zip(&base[i..]) {
            *slot = vi + vb;
        }
    });
}

// ---------------------------------------------------------------------------
// Bucketed master
// ---------------------------------------------------------------------------

/// The global set of distinct full vectors, split by value range.
///
/// Invariants (before `count_partial_sums`):
///   * `buckets[b]` is sorted and duplicate-free,
///   * every value in `buckets[b]` is in [splitters[b-1], splitters[b])
///     (open-ended at both extremes),
///   * therefore the concatenation of all buckets is globally sorted and
///     duplicate-free.
struct Master {
    /// Non-decreasing; length = buckets.len() - 1.
    splitters: Vec<u64>,
    buckets: Vec<Vec<u64>>,
}

impl Master {
    fn new() -> Self {
        Master {
            splitters: Vec::new(),
            buckets: Vec::new(),
        }
    }

    fn len(&self) -> usize {
        self.buckets.iter().map(|b| b.len()).sum()
    }

    /// Chooses bucket count and splitters from quantiles of a SORTED sample
    /// (the first pending buffer). Correctness never depends on balance; only
    /// parallel speed does.
    fn init_from_sorted_sample(&mut self, sorted: &[u64]) {
        let len = sorted.len();
        let nb = (rayon::current_num_threads() * BUCKETS_PER_THREAD)
            .min(MAX_BUCKETS)
            .min(len / MIN_BUCKET_ELEMS)
            .max(1);
        self.splitters = (1..nb).map(|k| sorted[k * len / nb]).collect();
        self.buckets = (0..nb).map(|_| Vec::new()).collect();
    }

    /// (bucket count, largest bucket / average bucket)
    fn balance(&self) -> (usize, f64) {
        let nb = self.buckets.len().max(1);
        let total = self.len();
        let max = self.buckets.iter().map(|b| b.len()).max().unwrap_or(0);
        let avg = (total as f64 / nb as f64).max(1.0);
        (nb, max as f64 / avg)
    }
}

// ---------------------------------------------------------------------------
// Merge / collapse
// ---------------------------------------------------------------------------

/// Merges a SORTED `run` (duplicates inside `run` are allowed) into a sorted,
/// duplicate-free `bucket`, in place, without a second full-size buffer.
///
/// Works from the back: the bucket grows by run.len(), then the merge writes
/// from the top down. Invariant: w >= i + j, so the write index is always >=
/// the number of unread bucket elements -- an unread element is never
/// overwritten. Duplicates (bucket-vs-run, or inside the run) are written
/// once, which leaves a gap that is closed at the end with one memmove.
fn merge_dedup_into(bucket: &mut Vec<u64>, run: &[u64]) {
    let r = run.len();
    if r == 0 {
        return;
    }
    let m = bucket.len();
    bucket.reserve_exact(r);
    bucket.resize(m + r, 0);

    let (mut i, mut j, mut w) = (m, r, m + r);
    while j > 0 {
        let b = run[j - 1];
        // Duplicate inside the run: skip the higher-index copy.
        if j >= 2 && run[j - 2] == b {
            j -= 1;
            continue;
        }
        if i == 0 {
            w -= 1;
            bucket[w] = b;
            j -= 1;
            continue;
        }
        let a = bucket[i - 1];
        w -= 1;
        if a > b {
            bucket[w] = a;
            i -= 1;
        } else if b > a {
            bucket[w] = b;
            j -= 1;
        } else {
            bucket[w] = a;
            i -= 1;
            j -= 1;
        }
    }

    // Result = bucket[0..i] ++ bucket[w..m+r]; close the gap in between.
    bucket.copy_within(w..m + r, i);
    bucket.truncate(i + (m + r - w));
}

/// Sorts the pending buffer (parallel), then merges it into the master
/// bucket-by-bucket, all buckets in parallel. Prints one summary line and
/// returns the wall time spent.
fn collapse(master: &mut Master, pending: &mut Vec<u64>, collapse_no: usize) -> Duration {
    let t = Instant::now();
    let before_master = master.len();
    let before_pending = pending.len();

    pending.par_sort_unstable();
    let sort_time = t.elapsed();

    if master.buckets.is_empty() {
        master.init_from_sorted_sample(pending);
    }

    // Cut points of the sorted pending buffer, one per bucket boundary.
    // Bucket b receives pending[bounds[b]..bounds[b+1]] (values in
    // [splitters[b-1], splitters[b])).
    let mut bounds: Vec<usize> = Vec::with_capacity(master.buckets.len() + 1);
    bounds.push(0);
    for &s in &master.splitters {
        bounds.push(pending.partition_point(|&x| x < s));
    }
    bounds.push(pending.len());

    let run_all: &[u64] = pending.as_slice();
    let bounds_ref: &Vec<usize> = &bounds;
    master
        .buckets
        .par_iter_mut()
        .enumerate()
        .for_each(|(b, bucket)| {
            merge_dedup_into(bucket, &run_all[bounds_ref[b]..bounds_ref[b + 1]]);
            // The run may have contained duplicates of existing values; give
        });
    pending.clear();

    let total = t.elapsed();
    let merge_time = total.saturating_sub(sort_time);
    let after_master = master.len();
    let added = after_master - before_master;
    let (nb, skew) = master.balance();

    println!(
        "  >> collapse #{}: {} pending -> +{} new distinct ({:.1}% novel) | master {} ({}) | sort {} merge {} | {} buckets, largest {:.2}x avg",
        collapse_no,
        fmt_short(before_pending as f64),
        fmt_short(added as f64),
        100.0 * added as f64 / before_pending as f64,
        fmt_short(after_master as f64),
        fmt_gib(after_master * 8),
        fmt_secs(sort_time.as_secs_f64()),
        fmt_secs(merge_time.as_secs_f64()),
        nb,
        skew
    );

    total
}

// ---------------------------------------------------------------------------
// Partial sums
// ---------------------------------------------------------------------------

/// Number of distinct values in the concatenation of `buckets`.
///
/// Precondition: each bucket is strictly increasing and the concatenation is
/// non-decreasing. Then duplicates can only be a bucket's last value equal to
/// the next non-empty bucket's first value.
fn distinct_count(buckets: &[Vec<u64>]) -> usize {
    let total: usize = buckets.iter().map(|b| b.len()).sum();
    let mut dup_pairs = 0usize;
    let mut prev_last: Option<u64> = None;
    for b in buckets {
        if let (Some(&first), Some(&last)) = (b.first(), b.last()) {
            if prev_last == Some(first) {
                dup_pairs += 1;
            }
            prev_last = Some(last);
        }
    }
    total - dup_pairs
}

/// Computes A_t(n) for t = 1..n from the sorted, deduplicated full vectors.
///
/// Because coordinate 0 is the most significant field, removing the last
/// coordinate is `>> bits`, which keeps everything sorted. Each level is one
/// parallel shift + per-bucket adjacent dedup; equal values that straddle a
/// bucket boundary are accounted for in `distinct_count` (no data movement).
/// Consumes `master` (it is modified in place).
fn count_partial_sums(mut master: Master, n: usize, bits: u32) -> Vec<usize> {
    let mut counts = vec![0usize; n];
    counts[n - 1] = distinct_count(&master.buckets);
    for t in (1..n).rev() {
        master.buckets.par_iter_mut().for_each(|bucket| {
            for v in bucket.iter_mut() {
                *v >>= bits;
            }
            bucket.dedup();
        });
        counts[t - 1] = distinct_count(&master.buckets);
    }
    counts
}

fn save_results_csv(path: &str, n: usize, counts: &[usize]) -> std::io::Result<()> {
    let file_exists = std::path::Path::new(path).exists();
    let file = OpenOptions::new().create(true).append(true).open(path)?;
    let mut w = BufWriter::new(file);
    if !file_exists {
        writeln!(w, "n,t,A_t(n)")?;
    }
    for (idx, &c) in counts.iter().enumerate() {
        writeln!(w, "{},{},{}", n, idx + 1, c)?;
    }
    w.flush()
}

// ---------------------------------------------------------------------------
// Pipeline
// ---------------------------------------------------------------------------

/// Where the wall time went for one n.
#[derive(Default)]
struct Timings {
    generate: Duration,
    chunk_sort: Duration,
    chunk_dedup: Duration,
    collapse: Duration,
    partial: Duration,
}

struct NResult {
    n: u32,
    distinct: usize,
    elapsed: Duration,
}

fn run_pipeline_for_n(n: u32, max_k: u32, results_path: &str) -> Result<NResult, String> {
    let timer = Instant::now();
    let nu = n as usize;

    println!("\n============================================================");
    println!("n = {}", n);
    println!("============================================================");

    let bits = bits_per_dim_for(n, max_k);
    if n * bits > 64 {
        return Err(format!(
            "n={} needs {} bits per packed vector (> 64); would need u128 keys",
            n,
            n * bits
        ));
    }

    // --- permutations ---
    let base = generate_and_pack_permutations(nu, bits);
    let b_len = base.len();
    let expected_len = (1..=n as u64).product::<u64>() as usize;
    assert_eq!(b_len, expected_len);
    let total_pairs = b_len * (b_len + 1) / 2;

    // --- memory plan ---
    let mut sys = System::new();
    let mut master = Master::new();
    let mut plan = plan_memory(&mut sys, master.len())?;
    let mut pending: Vec<u64> = Vec::with_capacity(plan.pending_cap);

    // --- header ---
    println!(
        "  packing              : {} bits/coordinate ({}/64 bits used)",
        bits,
        n * bits
    );
    println!("  permutations         : {}", fmt_int(b_len as u64));
    println!(
        "  pair sums to process : {}  (unordered pairs incl. diagonal)",
        fmt_int(total_pairs as u64)
    );
    match KNOWN_A.get(nu) {
        Some(&exp) => {
            let need = exp as usize * 8;
            println!(
                "  expected A_{n}({n})     : {}  (OEIS A175176; ~{} as u64s)",
                fmt_int(exp),
                fmt_gib(need)
            );
            if need as f64 > plan.avail_bytes as f64 * 0.95 {
                println!(
                    "  NOTE: the final set alone ({}) is close to or above the {} currently \
                     available. This run may stop with an out-of-budget error unless the OS \
                     can reclaim/compress enough memory.",
                    fmt_gib(need),
                    fmt_gib(plan.avail_bytes)
                );
            }
        }
        None => println!("  expected A_{n}({n})     : (no OEIS reference value)"),
    }
    println!("  threads              : {}", rayon::current_num_threads());
    println!(
        "  plan                 : chunk <= {} values ({}), pending cap {} values ({}), available {}",
        fmt_short(plan.chunk_elems as f64),
        fmt_gib(plan.chunk_elems * 8),
        fmt_short(plan.pending_cap as f64),
        fmt_gib(plan.pending_cap * 8),
        fmt_gib(plan.avail_bytes)
    );
    println!();

    // --- chunk loop ---
    let mut timings = Timings::default();
    let mut start_i = 0usize;
    let mut chunk_idx = 0usize;
    let mut collapses = 0usize;
    let mut pairs_done = 0u64;
    let mut last_print: Option<Instant> = None;
    let loop_start = Instant::now();

    while start_i < b_len {
        // Choose whole rows that fit the current chunk size.
        let mut end_i = start_i;
        let mut chunk_elements = 0usize;
        while end_i < b_len && chunk_elements + (b_len - end_i) <= plan.chunk_elems {
            chunk_elements += b_len - end_i;
            end_i += 1;
        }
        if end_i == start_i {
            chunk_elements = b_len - start_i;
            end_i = start_i + 1;
            println!(
                "  WARNING: row {} exceeds the chunk size; processing it anyway.",
                start_i
            );
        }

        // Would this chunk (worst case: no duplicates) overflow pending?
        if pending.len() + chunk_elements > plan.pending_cap {
            if pending.is_empty() {
                return Err(format!(
                    "a single chunk of {} values does not fit the pending budget of {}",
                    fmt_int(chunk_elements as u64),
                    fmt_int(plan.pending_cap as u64)
                ));
            }
            collapses += 1;
            timings.collapse += collapse(&mut master, &mut pending, collapses);
            drop(std::mem::take(&mut pending)); // hand the pages back before re-measuring
            plan = plan_memory(&mut sys, master.len())?;
            pending = Vec::with_capacity(plan.pending_cap);
            println!(
                "  >> replan: chunk <= {} values ({}), pending cap {} values ({}), available {}",
                fmt_short(plan.chunk_elems as f64),
                fmt_gib(plan.chunk_elems * 8),
                fmt_short(plan.pending_cap as f64),
                fmt_gib(plan.pending_cap * 8),
                fmt_gib(plan.avail_bytes)
            );
            continue; // re-choose rows against the new plan
        }

        let t_gen = Instant::now();
        let mut chunk = vec![0u64; chunk_elements];
        generate_chunk_symmetric(&base, start_i, end_i, &mut chunk);
        let gen_time = t_gen.elapsed();

        let t_sort = Instant::now();
        chunk.par_sort_unstable();
        let sort_time = t_sort.elapsed();

        let t_dedup = Instant::now();
        chunk.dedup();
        let dedup_time = t_dedup.elapsed();

        timings.generate += gen_time;
        timings.chunk_sort += sort_time;
        timings.chunk_dedup += dedup_time;

        let chunk_unique = chunk.len();
        pending.extend_from_slice(&chunk); // fits: guaranteed by the check above
        drop(chunk);

        pairs_done += chunk_elements as u64;
        start_i = end_i;
        chunk_idx += 1;

        // --- progress line (throttled; first and last chunk always print) ---
        let is_last = start_i >= b_len;
        let due = last_print
            .map(|t| t.elapsed().as_secs_f64() >= PROGRESS_MIN_INTERVAL_SECS)
            .unwrap_or(true);
        if is_last || due {
            last_print = Some(Instant::now());
            let frac = pairs_done as f64 / total_pairs as f64;
            let elapsed = loop_start.elapsed().as_secs_f64();
            let rate = pairs_done as f64 / elapsed.max(1e-9);
            let eta = (total_pairs as f64 - pairs_done as f64).max(0.0) / rate;
            let master_len = master.len();
            println!(
                "[{:5.1}%] [{}] chunk {} | pairs {}/{} | pend {:>3.0}% | master {} ({}) | uniq/chunk {:.0}% | gen {} sort {} dedup {} | {} elapsed, ETA ~{}",
                frac * 100.0,
                progress_bar(frac, BAR_WIDTH),
                chunk_idx,
                fmt_short(pairs_done as f64),
                fmt_short(total_pairs as f64),
                100.0 * pending.len() as f64 / plan.pending_cap as f64,
                fmt_short(master_len as f64),
                fmt_gib(master_len * 8),
                100.0 * chunk_unique as f64 / chunk_elements as f64,
                fmt_secs(gen_time.as_secs_f64()),
                fmt_secs(sort_time.as_secs_f64()),
                fmt_secs(dedup_time.as_secs_f64()),
                fmt_secs(elapsed),
                fmt_secs(eta)
            );
        }
    }

    // --- final collapse ---
    if !pending.is_empty() {
        collapses += 1;
        timings.collapse += collapse(&mut master, &mut pending, collapses);
    }
    drop(pending);

    let full_count = master.len();
    println!(
        "\n  all chunks done: A_{}({}) = {}",
        n,
        n,
        fmt_int(full_count as u64)
    );

    // --- check A_n(n) against OEIS A175176 ---
    match KNOWN_A.get(nu) {
        Some(&expected) if expected == full_count as u64 => {
            println!(
                "  CHECK PASSED: matches OEIS A175176 ({}).",
                fmt_int(expected)
            );
        }
        Some(&expected) => {
            return Err(format!(
                "CHECK FAILED: computed A_{n}({n}) = {}, OEIS A175176 says {}. Results NOT saved.",
                fmt_int(full_count as u64),
                fmt_int(expected)
            ));
        }
        None => println!("  (no OEIS reference value for n={}; check skipped)", n),
    }

    // --- all A_t(n) ---
    let t_partial = Instant::now();
    let counts = count_partial_sums(master, nu, bits);
    timings.partial = t_partial.elapsed();

    // A_1(n) = 2n - 1 (from your notes): cheap sanity check of the projection step.
    if counts[0] != 2 * nu - 1 {
        return Err(format!(
            "CHECK FAILED: A_1({}) = {}, expected {}. Results NOT saved.",
            n,
            counts[0],
            2 * nu - 1
        ));
    }

    save_results_csv(results_path, nu, &counts).map_err(|e| format!("failed to save CSV: {e}"))?;

    // --- summary ---
    let elapsed = timer.elapsed();
    let total_secs = elapsed.as_secs_f64();
    let pct = |d: Duration| 100.0 * d.as_secs_f64() / total_secs.max(1e-9);
    let named = timings.generate
        + timings.chunk_sort
        + timings.chunk_dedup
        + timings.collapse
        + timings.partial;
    let other = elapsed.saturating_sub(named);

    println!("\n------------------------------------------------------------");
    println!("n = {} complete in {}", n, fmt_secs(total_secs));
    println!(
        "  pair sums processed : {}  ({} chunks, {} collapses)",
        fmt_int(total_pairs as u64),
        chunk_idx,
        collapses
    );
    println!(
        "  distinct vectors    : {}  (1 per {:.1} pair sums; final set {} as u64s)",
        fmt_int(full_count as u64),
        total_pairs as f64 / full_count as f64,
        fmt_gib(full_count * 8)
    );
    println!(
        "  throughput          : {} pairs/s overall",
        fmt_short(total_pairs as f64 / total_secs.max(1e-9))
    );
    println!(
        "  time split          : generate {:.0}% | chunk sort {:.0}% | chunk dedup {:.0}% | collapses {:.0}% | partial sums {:.0}% | other {:.0}%",
        pct(timings.generate),
        pct(timings.chunk_sort),
        pct(timings.chunk_dedup),
        pct(timings.collapse),
        pct(timings.partial),
        pct(other)
    );
    if nu >= 2 {
        println!(
            "  A_(n-1)(n) == A_n(n): {}",
            counts[nu - 2] == counts[nu - 1]
        );
    }
    println!("  A_t({}):", n);
    for (idx, &c) in counts.iter().enumerate() {
        println!("    t = {:>2}  {:>24}", idx + 1, fmt_int(c as u64));
    }
    println!("  saved to {}", results_path);
    println!("------------------------------------------------------------");

    Ok(NResult {
        n,
        distinct: full_count,
        elapsed,
    })
}

fn run_range(start_n: u32, end_n: u32, max_k: u32) {
    create_dir_all("results").expect("Failed to create results directory");
    let results_path = "results/partial_sums.csv";
    println!("Results will be written to {}", results_path);

    let overall = Instant::now();
    let mut done: Vec<NResult> = Vec::new();
    let mut stopped: Option<(u32, String)> = None;

    for n in start_n..=end_n {
        match run_pipeline_for_n(n, max_k, results_path) {
            Ok(r) => done.push(r),
            Err(msg) => {
                eprintln!("\nSTOPPED at n={}: {}", n, msg);
                stopped = Some((n, msg));
                break;
            }
        }
    }

    println!("\n============================================================");
    println!("SUMMARY (n = {} to {})", start_n, end_n);
    println!("============================================================");
    println!("{:>3}  {:>24}  {:>10}", "n", "A_n(n)", "time");
    for r in &done {
        println!(
            "{:>3}  {:>24}  {:>10}",
            r.n,
            fmt_int(r.distinct as u64),
            fmt_secs(r.elapsed.as_secs_f64())
        );
    }
    match stopped {
        Some((n, _)) => println!("Stopped at n={} (see error above).", n),
        None => println!("Completed n={} through n={}.", start_n, end_n),
    }
    println!(
        "Total wall time: {}",
        fmt_secs(overall.elapsed().as_secs_f64())
    );
}

fn main() {
    // Usage: cargo run --release -- [start_n] [end_n]
    // n=9 needs ~14 GB for the final set: it finished on a 16 GB MacBook Air
    // (~1490 s with the serial merge, ~1100 s with the parallel bucketed merge).
    // On machines that are too small it stops with an "out of memory budget"
    // message instead of being killed.
    let args: Vec<u32> = std::env::args()
        .skip(1)
        .filter_map(|a| a.parse().ok())
        .collect();
    let start_n = args.first().copied().unwrap_or(1);
    let end_n = args.get(1).copied().unwrap_or(8);
    run_range(start_n, end_n, 2);
}
