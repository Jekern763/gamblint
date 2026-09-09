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

The difficulty in deriving this sequence arises from collisions between vector sums: distinct pairs of permutations can produce the same resulting vector. For example

Let $n=4$

$$
S_n =
\{(1,2,3,4), (1,2,4,3), (1,3,2,4), (1,3,4,2), \ldots\}
$$

where $S_n$ contains all permutations of$\{1,2,3,4\}$. Thus,

$$
|S_n| = 4! = 24.
$$

It would seem that a naive count of the ordered pairs of permutations would produce

$$
A(4) = (4!)^2 = 576,
$$

but this overcounts, since not all sums of pairs of permutations are unique.

For example
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

## New Definitions

To study this sequence in terms of partial sums, I have implemented the following notation

$$
\pi_{[t]} = (\pi_1, \pi_2, ..., \pi_t), \space \sigma_{[t]} = (\sigma_1, \sigma_2, ..., \sigma_t) \\[1em]
\pi_{[t]} + \sigma_{[t]} = (π_1​+σ_1​,…,π_t​+σ_t​)
\\[1em]
\mathcal{A}_t(n) = \left\{
\pi_{[t]}+\sigma_{[t]}
:
\pi,\sigma\in S_n
\right\}

\\[1em]

A_t(n) = |\mathcal{A}_t|\\

1 \le t \le n
$$

For the special case where $t=n$

$$
A_n​(n)=|\set{(π_1​+σ_1​,…,π_n​+σ_n​):π,σ ∈ S_n ​}| =A(n)
$$

When \(t=1\), we consider only the first coordinates of the two permutations:

$$
A_1(n)=
\left|
\left\{
\pi_1+\sigma_1:\pi,\sigma\in S_n
\right\}
\right|.
$$

Since $\pi_1,\sigma_1\in{1,2,\ldots,n}$, their possible sums range from $2$ to $2n$. Every integer in this range can be obtained, so there are $2n-1$ distinct sums. Therefore,

$$
A_1(n)=2n-1
$$

## Sequence Graph

With all values for $n$ and $t$ this graph can be created.

$$
\begin{array}{c|cccccc}
 & n=1&n=2&n=3&n=4&n=5&n=6\\
\hline
t=1&\mathbf{A_1(1)}&A_1(2)&A_1(3)&A_1(4)&A_1(5)&A_1(6)\\
t=2& &\mathbf{A_2(2)}&A_2(3)&A_2(4)&A_2(5)&A_2(6)\\
t=3& & &\mathbf{A_3(3)}&A_3(4)&A_3(5)&A_3(6)\\
t=4& & & &\mathbf{A_4(4)}&A_4(5)&A_4(6)\\
t=5& & & & &\mathbf{A_5(5)}&A_5(6)\\
t=6& & & & & &\mathbf{A_6(6)}
\end{array}
$$

The sequence that we are studying is found by moving from the top left diagonally towards the bottom right (items in bold)

## Initial Generation

In order to better see the structure of this series, I have "brute forced" some of the first terms. Established in OEIS are the first 15 terms, here I have the first 6 and their partial sum counter parts.

$$
\begin{array}{c|cccccc}
 & n=1&n=2&n=3&n=4&n=5&n=6\\
\hline
t=1&1&3&5&7&9&11\\
t=2& &3&19&43&75&115\\
t=3& & &19&201&551&1117\\
t=4& & & &201&3081&9593\\
t=5& & & & &3081&62663\\
t=6& & & & & &62663
\end{array}
$$

## Basic Identities

This section will prove:

$$
A_{t-1}(t) = A_t(t) \text{ equivalently } A_{t}(t+1) = A_{t+1}(t+1) \\[1em]

A_t(n) \le \min{((2n-1)^t, (n!)^2)}
$$

### $A_{t-1}(t) = A_t(t)$

First, this is visualy possible to see in the table above. Any number at the bottom bound is matched by the one vertically above it. Conceptualy this is because, and the point that $t = n-1$, each partial history has only one more option to complete it. Basically, all items from the vector permutations have been used, except for one, leaving only one choice, and therefore not adding any more possible unique sums.

To prove this fist consider the identity

$$
\sum_{i=1}^n \pi_i = \sum_{i=1}^n \sigma_i = \frac{n(n+1)}{2} \\[1em]
\sum_{i=1}^n (\pi_i + \sigma_i) = n(n+1) \\[1em]
\pi_n​+\sigma_n​=n(n+1)− \sum_{i=1}^{n-1} (\pi_i + \sigma_i)
$$

$$
\pi_t+\sigma_t=t(t+1)-\sum_{i=1}^{t-1}(\pi_i+\sigma_i)
$$

Thus, every distinct partial sum in $\mathcal{A}_{t-1}(t)$ corresponds to exactly one complete sum in $\mathcal{A}_t(t)$, since the final coordinate is uniquely determined by the first $t-1$ coordinates.

To show that this correspondence is a bijection, define

$$
f:\mathcal{A}_{t-1}(t)\rightarrow\mathcal{A}_t(t)
$$

by

$$
f(x_1,\ldots,x_{t-1})
=
\left(
x_1,\ldots,x_{t-1},
t(t+1)-\sum_{i=1}^{t-1}x_i
\right).
$$

The function is injective because the first $t-1$ coordinates are unchanged. Therefore, if

$$
f(x)=f(y),
$$

then

$$
x=y.
$$

To show surjectivity, let $y=(y_1,\ldots,y_t)\in\mathcal{A}_t(t)$. By definition, $y$ is witnessed by some $\pi,\sigma\in S_t$, i.e. $y_i=\pi_i+\sigma_i$ for all $i$. Truncating, $(y_1,\ldots,y_{t-1})=(\pi_1+\sigma_1,\ldots,\pi_{t-1}+\sigma_{t-1})$, which lies in $\mathcal{A}_{t-1}(t)$ by definition, since it is exactly the partial sum of this same witnessing pair $\pi,\sigma$.

Applying $f$ to this truncation gives

$$
f(y_1,\ldots,y_{t-1}) = \left(y_1,\ldots,y_{t-1},\ t(t+1)-\sum_{i=1}^{t-1}y_i\right).
$$

Since $\pi,\sigma\in S_t$, the permutation-sum identity gives

$$
\pi_t+\sigma_t = t(t+1)-\sum_{i=1}^{t-1}(\pi_i+\sigma_i) = t(t+1)-\sum_{i=1}^{t-1}y_i = y_t.
$$

So $f(y_1,\ldots,y_{t-1}) = (y_1,\ldots,y_{t-1},y_t) = y$.

Thus, every element of $\mathcal{A}_t(t)$ is the image, under $f$, of an element of $\mathcal{A}_{t-1}(t)$ — namely its own truncation.

Therefore, $f$ is a bijection, and hence

$$
A_{t-1}(t)=A_t(t) \\
\Box
$$

### $A_t(n) \le \min{((2n-1)^t, (n!)^2)}$

**Bound 1: $A_t(n) \le (n!)^2$.** The map $(\pi,\sigma)\mapsto \pi_{[t]}+\sigma_{[t]}$ sends $S_n\times S_n$ onto $\mathcal{A}_t(n)$. A surjection out of a set of size $(n!)^2$ cannot land on more than $(n!)^2$ distinct values, so $A_t(n)\le (n!)^2$.

**Bound 2: $A_t(n) \le (2n-1)^t$.** Each coordinate $\pi_i+\sigma_i$ lies in $\{2,\ldots,2n\}$, a set of $2n-1$ values. Since $\mathcal{A}_t(n)$ consists of $t$-tuples built from these coordinates, there are at most $(2n-1)^t$ distinct tuples.

Combining the two bounds gives

$$
A_t(n) \le \min\{(2n-1)^t,\ (n!)^2\}.
$$

**Monotonicity: $A_t(n) \le A_{t+1}(n)$.** Define the truncation map $\tau:\mathcal{A}_{t+1}(n)\to\mathcal{A}_t(n)$ by $\tau(x_1,\ldots,x_{t+1})=(x_1,\ldots,x_t)$. This map is surjective: any $y\in\mathcal{A}_t(n)$ is witnessed by some $\pi,\sigma\in S_n$ with $y=\pi_{[t]}+\sigma_{[t]}$, and extending these same $\pi,\sigma$ by one more coordinate gives an element of $\mathcal{A}_{t+1}(n)$ whose truncation under $\tau$ is $y$. A surjection between finite sets cannot decrease cardinality, so

$$
A_t(n)\le A_{t+1}(n).
$$
