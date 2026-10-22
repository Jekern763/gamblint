import gc
import itertools
import math
import pickle

import numpy as np
import psutil
from numba import njit, prange

_MIX = np.int64(-7046029254386353131)


def bits_per_dim_for(n, max_k):
    max_val = max_k * n
    return max(1, math.ceil(math.log2(max_val + 1)))


def pack_vectors(arr, bits_per_dim):
    n = arr.shape[1]
    powers = np.int64(1) << (np.arange(n, dtype=np.int64) * bits_per_dim)
    return (arr * powers).sum(axis=1)


@njit(parallel=True, cache=True)
def generate_chunk_symmetric(base_packed, start_i, end_i, chunk_buffer):
    """
    Generates a localized block of pairs natively in parallel.
    No locks, no atomic collisions—each thread writes to a precise index.
    """
    B = base_packed.shape[0]

    # 1. Thread-local mapping pass to find precise slice bounds
    # (Accounts for the upper-triangular matrix shapes)
    offsets = np.empty(end_i - start_i + 1, dtype=np.int64)
    current_offset = np.int64(0)
    for idx in range(start_i, end_i):
        offsets[idx - start_i] = current_offset
        current_offset += B - idx
    offsets[end_i - start_i] = current_offset

    # 2. Main parallel generation block
    for i in prange(start_i, end_i):
        write_pos = offsets[i - start_i]
        val_i = base_packed[i]
        for b in range(i, B):
            chunk_buffer[write_pos] = val_i + base_packed[b]
            write_pos += 1


@njit(parallel=True, cache=True)
def inplace_deduplicate(sorted_arr):
    """
    Scans a sorted array in parallel to compress out duplicates.
    Modifies mask values to flag unique elements.
    """
    N = sorted_arr.shape[0]
    if N <= 1:
        return sorted_arr

    mask = np.ones(N, dtype=np.bool_)
    for i in prange(1, N):
        if sorted_arr[i] == sorted_arr[i - 1]:
            mask[i] = False

    return sorted_arr[mask]


def run_pipeline_for_n(n, max_k=2, checkpoint_interval=5):
    bits_per_dim = bits_per_dim_for(n, max_k)
    perms = np.array(list(itertools.permutations(range(1, n + 1))), dtype=np.int64)
    base_packed = pack_vectors(perms, bits_per_dim)
    B = base_packed.shape[0]

    total_pairs = (B * (B + 1)) // 2
    print(f"\n--- Starting n={n} | Total Pairs to Evaluate: {total_pairs:,} ---")

    # Target safe chunk sizes (~1.5 GiB raw footprint per chunk step)
    TARGET_CHUNK_SIZE = 200_000_000

    # Global Master Array to store the combined unique items
    master_unique = np.empty(0, dtype=np.int64)

    # Track steps to chunk cleanly across rows
    start_i = 0
    chunk_idx = 0

    while start_i < B:
        # Calculate exactly how many rows fit inside our target chunk buffer
        end_i = start_i
        chunk_elements = 0
        while end_i < B and chunk_elements + (B - end_i) <= TARGET_CHUNK_SIZE:
            chunk_elements += B - end_i
            end_i += 1

        if end_i == start_i:  # Fallback safety line for final massive rows
            chunk_elements = B - start_i
            end_i = start_i + 1

        # REAL-TIME RAM SANITY GATE
        vm = psutil.virtual_memory()
        buffer_bytes = chunk_elements * 8
        master_bytes = master_unique.nbytes
        projected_total = master_bytes + (
            buffer_bytes * 2
        )  # Account for sort allocation

        print(
            f"[Chunk {chunk_idx}] Rows {start_i:,} to {end_i:,} | Pairs: {chunk_elements:,} (~{buffer_bytes / 1024**2:,.1f} MB)"
        )
        if projected_total > vm.available * 0.90:
            print(
                f"CRITICAL WARNING: Memory usage approaching limit! Free RAM: {vm.available / 1024**3:.2f} GiB"
            )
            # Trigger emergency garbage collection or data-dump mechanisms here if needed.

        # Allocate, populate, and aggressively sort the local chunk
        chunk_buffer = np.empty(chunk_elements, dtype=np.int64)
        generate_chunk_symmetric(base_packed, start_i, end_i, chunk_buffer)

        chunk_buffer.sort()  # Native multi-threaded parallel NumPy sort
        chunk_unique = inplace_deduplicate(chunk_buffer)

        del chunk_buffer  # Clean up raw elements immediately

        # Merge-Reduce current chunk unique results back into Master Array
        master_unique = np.concatenate((master_unique, chunk_unique))
        master_unique.sort()
        master_unique = inplace_deduplicate(master_unique)

        print(
            f"  -> Merged Master Size: {master_unique.shape[0]:,} unique items. System Free RAM: {psutil.virtual_memory().available / 1024**3:.2f} GiB"
        )

        # DISK STORAGE CHECKPOINT ENGINE
        if chunk_idx % checkpoint_interval == 0 and chunk_idx > 0:
            ckpt_path = f"checkpoint_n{n}_chunk{chunk_idx}.pkl"
            print(f"  [Checkpoint] Persisting master data to disk -> {ckpt_path}")
            with open(ckpt_path, "wb") as f:
                pickle.dump(master_unique, f, protocol=pickle.HIGHEST_PROTOCOL)

        start_i = end_i
        chunk_idx += 1
        gc.collect()

    # Final Export
    final_path = f"final_results_n{n}.pkl"
    with open(final_path, "wb") as f:
        pickle.dump(master_unique, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(
        f"SUCCESS: Completed n={n}. Total unique sums tracked: {master_unique.shape[0]:,}"
    )


if __name__ == "__main__":
    # Test locally with n=6 or n=7 first!
    run_pipeline_for_n(n=7, checkpoint_interval=5)
