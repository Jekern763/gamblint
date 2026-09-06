# Incomplete Histories

## Abstract

In an attempt to uniquely approach the problem of OEIS Sequence A175176 "Number of vector sums of two permutations of 1,2,...,n." the specific game mechanics will be used. Instead of studying the series statically as the counting funciton as shown in this basic formula

Let $S_n$ denote the set of permutations of $\{1,\ldots,n\}$. Then

$$
A(n)
=
\left|
\left\{
(\pi_1+\sigma_1,\ldots,\pi_n+\sigma_n)
:
\pi,\sigma\in S_n
\right\}
\right|
$$

In a shorter form

$$
A(n)
=
\left|
\left\{
\pi+\sigma
:
\pi,\sigma\in S_n
\right\}
\right|
$$

## Abstract Application

The specific mechanics included in this game provide an intuitive way to study this sequence. Instead of trying to produce a function statically, as has been done in the past, we can approach the problem through a recursive lens. Specifically, my game is played by incrementing the variable $t$, creating incomplete "histories" that correspond to partial vector sums from the formula above. From each history, it is possible to determine the consistent dice states and thereby produce the next set of possible incomplete histories. This naturally provides a recursive formula for the total count of complete histories, or vector sums in $\mathbb{Z}^n$.
