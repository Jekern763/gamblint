# p7: Peek-History Likelihood Given Game State

Proving

$$
P(P_t | S_t)
$$

## p7.1: $P(S_t, P_t)$

We can rewrite any $P_t$ such that

$$
P_t = (p_1, p_2, ..., p_t)\\
=(P_{t-1}, p_t)
$$

Then

$$
P(P_t|S_t) = P(P_{t-1}, p_t| S_t)
$$

We can also find the probability of $S_t$ using the equation from `p4`

$$
P(S_t | S_{t-1}) = \frac{1}{(7-t)^2}
$$

Since we know that $S_t$ is possible and $n=6$

Let us also define (using `p5`)

$$
P(p_t | S_{t-1}) = \frac{\mathcal{N}_{p_t}(S_{t-1})}{(7-t)^2}
$$

Just to combine everything we have

$$
P(P_t|S_t) = P(P_{t-1}, p_t| S_t) \\[1em]
P(S_t | S_{t-1}) = \frac{1}{(7-t)^2} \\[1em]
P(p_t | S_{t-1}) = \frac{\mathcal{N}_{p_t}(S_{t-1})}{(7-t)^2}
$$

Using these to define $P(S_t, P_t)$

$$
P(P_t, S_t) = P(P_{t-1},p_t, S_t) \\[1em]
= \sum_{S_{t-1}}P(P_{t-1}, p_t, S_t, S_{t-1})
$$

Then using the product rule

$$
P(P_{t-1}, p_t, S_t, S_{t-1}) = P(P_{t-1}​,S_{t−1}​)⋅P(p_t​∣P_{t−1​},S_{t−1}​)⋅P(S_t​∣P_{t−1}​,S_{t−1}​,p_t​)
$$

Using the properties of the game:

- The probability of $p_{t}$ depends only on $S_{t-1}$
- The probability of $S_t$ depends only on $S_{t-1}$ (and, if conditioning on the observed peek, on whether the transition produces $p_t$).

$$
P(P_{t-1}​,S_{t−1}​)⋅P(p_t​∣P_{t−1​},S_{t−1}​)⋅P(S_t​∣P_{t−1}​,S_{t−1}​,p_t​)\\
=P(P_{t-1}​,S_{t−1}​)⋅P(p_t​∣S_{t−1}​)⋅P(S_t​∣​S_{t−1}, p_{t}​​)\\[1em]
$$
Substituting
$$
=
P(P_{t-1}​,S_{t−1}​)
\cdot
\frac{\mathcal{N}_{p_t}(S_{t-1})}{(7-t)^2}
\cdot
\frac{\mathcal{N}_{S_t,p_t}(S_{t-1})}{\mathcal{N}_{p_t}(S_{t-1})}
$$

So going back into the sum

$$
\sum_{S_{t-1}}P(P_{t-1}​,S_{t−1}​)
\cdot
\frac{\mathcal{N}_{p_t}(S_{t-1})}{(7-t)^2}
\cdot
\frac{\mathcal{N}_{S_t,p_t}(S_{t-1})}{\mathcal{N}_{p_t}(S_{t-1})}
$$

This is the recursive step. Define the endpoint conditions:

$$
S_0 = (\set{1,2,3,4,5,6}, \set{1,2,3,4,5,6}) \\
P_0 = () \\
P(S_0, P_0) = 1
$$

For ordered states, define

$$
\alpha_t(S_t) = P(P_t,S_t).
$$

Then the recurrence is

$$
\boxed{
\alpha_t(S_t)=
\sum_{S_{t-1}}\alpha_{t-1}(S_{t-1})
\frac{\mathcal{N}_{S_t,p_t}(S_{t-1})}{(7-t)^2}
}
$$

Here $\mathcal{N}_{S_t,p_t}(S_{t-1})$ counts ordered pairs of removed faces that produce both the observed peek $p_t$ and the ordered successor state $S_t$. For a fixed ordered successor state this count is either $1$ (if the transition is valid and produces $p_t$) or $0$.

## p7.2: $P(S_t | P_t)$

Using Bayes' theorem,

$$
P(S_t | P_t) = \frac{P(S_t,P_t)}{P(P_t)}
=\boxed{
\frac{\alpha_t(S_t)}{\sum_{S_t}\alpha_t(S_t)}
}
$$
