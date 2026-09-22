# Although I have generated many terms in this sequence before, the goal here it to find more, and hopefuly do it effeciently.
# I track partial vector sums, so in other words all values of A_t(n) for values of t up to n and n as high as possible
# will generate only for k (number of vectors) = 2, all numbers past that would need to be proved as they are not feasibly brute force-able
# This will be optimized with numbas, using numpy to type in a numbas accessible way
# I am attempting to do a "top down" generation which will first count all the unique full sums, the chop off components starting from the back. It will need to recount after each one

# Synthesized in collaboration with Claude for complex numbas integration
#
# v2: each n-dimensional vector is bit-packed into a single int64 (n slots of
# bits_per_dim bits each, sized to the final max_k so no slot ever overflows
# into its neighbor during any intermediate addition). That collapses the
# per-vector memory cost from ~n*8 bytes down to a flat ~24 bytes, and turns
# every hash/equality/addition op from an O(n) loop into a single scalar op.
# Feasible up to about n=12 for k=2 (int64 has 64 bits to spend); beyond that
# bits_per_dim * n exceeds 64 and packing isn't possible without splitting
# across two words, which this version does not attempt.

# /// script
# dependencies = ["numpy", "numba", "psutil"]
# ///
import gc
import itertools
import math
import pickle
import time
from collections import Counter, defaultdict
from typing import Annotated

import numpy as np
import psutil
from numba import njit

# 64-bit mixing constant (splitmix64 golden-ratio constant) used to spread
# packed values across the hash table more evenly than a raw modulo would,
# since low bits of a packed vector are not uniformly distributed when
# bits_per_dim is small.

type Data = dict[
    Annotated[int, "k"],
    dict[
        Annotated[int, "t"],
        dict[
            Annotated[int, "n"],
            int,  # The final value is also an integer
        ],
    ],
]
"""
Layout Guide:
Data[k][t][n]
"""

_MIX = np.int64(-7046029254386353131)  # 0x9E3779B97F4A7C15 as signed int64


def bits_per_dim_for(n, max_k):
    max_val = max_k * n
    return max(1, math.ceil(math.log2(max_val + 1)))


def pack_vectors(arr, bits_per_dim):
    n = arr.shape[1]
    powers = np.int64(1) << (np.arange(n, dtype=np.int64) * bits_per_dim)
    return (arr * powers).sum(axis=1)


@njit(cache=True)
def expand_layer_packed(layer_packed, base_packed, max_alloc, symmetric):
    """
    layer_packed: 1D int64 array - unique packed vectors reachable as a sum
    of exactly d permutations (repetition allowed).
    base_packed: 1D int64 array - the n! packed permutation vectors.
    symmetric: True iff layer_packed IS base_packed (same set, same order) -
    i.e. only valid for the depth==2 transition, where we're summing two
    elements of the same set and a+b == b+a, so only the upper-triangular
    half of the pairs needs to be visited.

    Returns (found, total, overflowed).
    """
    found = np.empty(max_alloc, dtype=np.int64)  # only ever read up to `total`
    total = 0

    table_size = max_alloc * 2
    table = np.full(table_size, -1, dtype=np.int64)

    L = layer_packed.shape[0]
    B = base_packed.shape[0]

    for i in range(L):
        base_val = layer_packed[i]
        start_b = i if symmetric else 0
        for b in range(start_b, B):
            new_val = base_val + base_packed[b]

            h = (new_val * _MIX) % table_size
            if h < 0:
                h += table_size

            probe = h
            is_new = True
            while table[probe] != -1:
                idx = table[probe]
                if found[idx] == new_val:
                    is_new = False
                    break
                probe = (probe + 1) % table_size

            if is_new:
                if total >= max_alloc:
                    return found, total, True
                found[total] = new_val
                table[probe] = total
                total += 1

    return found, total, False


def compute_all_truncations_topdown(
    max_n, k_values=(2,), ram_safety_margin=0.75, overhead_factor=3.0
) -> Data:
    """
    Layout Guide:
    Data[k][t][n]
    """
    if isinstance(k_values, int):
        k_values = (k_values,)
    k_values = sorted(set(k_values))
    max_k = max(k_values)

    results = defaultdict(lambda: defaultdict(Counter))

    for n in range(1, max_n + 1):
        bits_per_dim = bits_per_dim_for(n, max_k)
        if n * bits_per_dim > 64:
            print(
                f"[n={n}] SKIPPED - packing needs {n * bits_per_dim} bits "
                f"({bits_per_dim} bits/dim x {n} dims), which doesn't fit in "
                f"an int64. Reduce max_k or n."
            )
            for k in k_values:
                for t in range(1, n + 1):
                    results[k][t][n] = None
            continue

        print(
            f"[n={n}] bits_per_dim={bits_per_dim} "
            f"({n * bits_per_dim}/64 bits used for packing)"
        )

        perms = np.array(list(itertools.permutations(range(1, n + 1))), dtype=np.int64)
        base_packed = pack_vectors(perms, bits_per_dim)
        B = base_packed.shape[0]

        layer_packed = np.zeros(1, dtype=np.int64)  # layer_0 = just the zero vector
        overflowed_from = None

        for depth in range(1, max_k + 1):
            L = layer_packed.shape[0]
            # depth==2 is the only transition where the layer being expanded
            # (layer_1) IS base_packed itself - only there is a+b == b+a a
            # valid shortcut. Every later depth adds a fresh permutation to
            # an already-combined sum, so no such symmetry holds there.
            symmetric = depth == 2

            # Hard ceiling from the actual number of (i, b) pairs that will
            # ever be visited - the true unique-sum count can never exceed
            # this, so there's no reason to size the hash table off available
            # system RAM alone. This is what was making every n (even n=1)
            # pay for a ~100M-row allocation regardless of real output size.
            pair_count = (L * (L + 1)) // 2 if symmetric else L * B

            available = psutil.virtual_memory().available
            bytes_per_row = 8 * overhead_factor  # flat cost - no n factor
            ram_based_max_alloc = max(
                int((available * ram_safety_margin) // bytes_per_row), 1024
            )
            max_alloc = min(ram_based_max_alloc, pair_count)

            print(
                f"[n={n}, depth={depth}] available RAM: {available / 1024**2:,.0f} MB, "
                f"pair_count={pair_count:,} -> max_alloc={max_alloc:,} rows "
                f"(~{max_alloc * bytes_per_row / 1024**2:,.1f} MB)"
                + (" [symmetric]" if symmetric else "")
            )

            if overflowed_from is not None:
                pass  # already incomplete upstream - don't waste time building further
            else:
                start = time.perf_counter()
                layer_packed, total, overflowed = expand_layer_packed(
                    layer_packed, base_packed, max_alloc, symmetric
                )
                layer_packed = layer_packed[:total]
                elapsed = time.perf_counter() - start
                actual_mb = layer_packed.nbytes / 1024**2
                status = (
                    " -- OVERFLOWED (partial lower bound only)" if overflowed else ""
                )
                print(
                    f"[n={n}, depth={depth}] {total:,} unique sums in "
                    f"{elapsed:.3f}s, {actual_mb:,.1f} MB used{status}"
                )
                if overflowed:
                    overflowed_from = depth

            if depth in k_values:
                for t in range(1, n + 1):
                    if overflowed_from is not None:
                        results[depth][t][n] = None
                        print(
                            f"  k={depth}, t={t}, n={n} -> INCOMPLETE (upstream overflow)"
                        )
                    else:
                        mask = (np.int64(1) << (t * bits_per_dim)) - 1
                        truncated = layer_packed & mask
                        count = len(np.unique(truncated))
                        results[depth][t][n] = count
                        print(f"  k={depth}, t={t}, n={n} -> {count}")

        del perms, base_packed, layer_packed
        gc.collect()
    data: Data = {
        k: {t: dict(c) for t, c in tdict.items()} for k, tdict in results.items()
    }
    return data


if __name__ == "__main__":
    MAX_N = 8
    K_VALUES = (2,)
    data = compute_all_truncations_topdown(MAX_N, k_values=K_VALUES)
    with open("generated_sequence.pkl", "wb") as file:
        pickle.dump(data, file)
