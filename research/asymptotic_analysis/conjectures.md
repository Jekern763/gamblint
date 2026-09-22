# Conjectures

Polynomial structure of $A_t(n)$

For fixed $t$, conjecture that

$$
\deg A_t(n)=t
$$
Polynomial formulas

For each $t$, polynomial fits to the computed values appear to give the exact polynomial $A_t(n)$, but this is currently unproven. These formulas motivate the following structural conjectures.

Appell structure

Define

$$
g_t(n)=\frac{A_t(n)}{2^t t!}
$$

If the polynomial formulas are correct, conjecture

$$
g_t'(n)=g_{t-1}(n)
$$

so $\{g_t\}$ forms an Appell sequence.

Therefore

$$
\boxed{ A_t(n)= \sum_{r=0}^t 2^{t-r}\binom tr A_r(0)n^{t-r} }
$$

so the sequence is determined by the values $A_r(0)$.

Equivalently, once $A_t$ is known, $A_{t+1}$ is determined up to one additive constant.

Boundary identity

Use the proven identity

$$
\boxed{A_{t-1}(t)=A_t(t)}
$$

to determine that constant recursively.

If

$$
A_t(n)=f(n)+C,
$$

then

$$
A_t(t)=A_{t-1}(t)
$$

so

$$
\boxed{C=A_{t-1}(t)-f(t)}.
$$

Thus, if the Appell structure and boundary identity hold, each new polynomial can be determined recursively from the preceding one, without needing an independent value for its constant term.

Finally, the original sequence is the diagonal:
$$
A(n)=A_n(n)
$$
