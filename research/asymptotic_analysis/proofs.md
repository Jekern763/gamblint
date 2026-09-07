# Proofs for OEIS A175176

In this file are multiple connected proofs with the end goal of finding non-trivial properties, or a recursive formula, for the OEIS Sequence A175176.

## Abstract

In abstract, OEIS A175176 is the "Number of vector sums of two permutations of 1,2,...,n." (OEIS). For more details see the next section or visit [OEIS A175176](https://oeis.org/A175176).

The specific mechanics included in this game provide an intuitive way to study the sequence. Instead of trying to produce a function statically, as has been done in the past, we can approach the problem through a recursive lens. Specifically, my game is played by incrementing the variable $t$, creating incomplete "histories" that correspond to _partial_ vector sums. Each partial sum can be examined, and hopeful some helpful properties can be discovered.

## Basic Definitions

To describe the series in short:

$$
A(n) =
\left|
\left\{
\pi+\sigma
:
\pi,\sigma\in S_n
\right\}
\right|
$$

Where

$$
S_n = \set{\text{all permutations of } (1, 2, ..., n)} \\[1em]
|S_n| = n!
$$

Notably, the issue of deriving this sequence arises when one considers the collision of sum vector sums. For example

Let $n=3$

$$
S_n = \{(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,2,1), (3,1,2) \} \\
|S_n| = 6
$$

It would seem to a naive count of the ordered pairs of permutations would produce $A(3) = (3!)^2=36$
but consider that not all sums are unique.

For example (using $n=4$ to illustrate more accurately)
$$
(1, 2, 3, 4) + (3, 4, 2, 1) = (2, 3, 4, 1) + (2, 3, 1, 4) \\[1em]
(4, 6, 5, 5) = (4, 6, 5, 5)
$$

So some sums will collapse. This can be seen by observing the naive count $(n!)^2$ next to the discovered terms in the sequnce

|$n$|$(n!)^2$|$A(n)$|% Error|
|---:|---------:|-------:|------:|
|1|1|1|0.00%|
|2|4|3|25.00%|
|3|36|19|47.22%|
|4|576|201|65.10%|
|5|14,400|3,081|78.60%|
|6|518,400|62,663|87.91%|

