# Conjectures

## Polynomial structure of $A_t(n)$ for fixed $t$ and variable $n$

Given

$$
A_t(n)
$$
where $t$ is known, the conjecture is that

$$
\deg{A_t(n)} = t
$$

## Polynomial fits for $A_t(n)$

For any set t, I have fit some polynomials to the function, where the fit is complete, but unproven. This becomes the basis for further conjectures and proofs.

## Appell Sequence Structure of $A_t(n)$

If the proposed polynomial functions for $A_t(n)$ are correct then

$$
g_t(n) = \frac{A_t(n)}{2^tt!} \\[1em]
g'_t(n) = g_{t-1}(n)
$$

Which is an appelle sequence, which would suggest

$$
A_t(n) = \sum_{r=0}^t 2^{t-r} \binom{t}{r}A_r(0)n^{t-r}
$$

Where $A_r(0)$ is the only unkwone quantity, and as such is the only degree of freedoms

Because we would have proven the appell property it also holds that

$$
g_{t+1}(n) = \int{g_t(n)}
$$

But because it is an indefinite integral, there is still a degree of freedom on the constant term $C$.

That can be eliminated with one test point, and we can use another, proven identity for that one

$$
A_{t}(t) = A_{t+1}(t) \\
$$

So using a previous case as the lead to our new test point

So when we have something like

$$
A_t(n) = f(n) + C
$$

to find $C$ we would need one test case, but because of the identity above, and that fact taht we must know the lower values before finding this higher one, we can substitue

$$
A_{t-1}(t) = f(n) + C \\
C = A_{t-1}(t) - f(n)
$$

which will solve for every value of $C$ as long as the functions are build recursively

Then just evaluating at $t=n$ gives the full sequence

$$
A_n(n) = A(n)
$$
