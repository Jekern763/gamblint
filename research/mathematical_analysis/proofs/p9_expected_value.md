# p9: Expected Value

First, finding the EV for any guess, given the peeks history

$$
EV(g | P_t) = \sum_{r=2}^{12}p(g, r) \cdot P(r | P_t)
$$

Expanding

$$
EV(g | P_t) = \sum_{r=2}^{12}(2-|g-r|)\cdot(|g-7|)\cdot P(r|P_t) \\[1em]
=|g-7|\sum_{r=2}^{12}(2-|g-r|)\cdot P(r|P_t) \\[1em]
=|g-7|\left(\sum_{r=2}^{12}(2P(r|P_t)) - \sum_{r=2}^{12}|g-r| \cdot P(r|P_t)\right) \\[1em]
\text{because the sum of all } P(r|P_t) = 1 \\[1em]
EV(g|P_t)=|g-7| \cdot (2-\sum_{r=2}^{12}|g-r| \cdot P(r|P_t))
$$

In the actual game, the guess must be an integer from $2$ through $12$. Thus, to find the maximum EV with best play,

$$
\max_{g\in\{2,3,\ldots,12\}}(EV(g | P_t)) = \max_{g\in\{2,3,\ldots,12\}}(
    |g-7| \cdot (2-\sum_{r=2}^{12}|g-r| \cdot P(r|P_t))
)
$$

Then finding the average max EV for any possible game, theoretically

$$
\sum_{P_t}\max_g(EV(g|P_t)) \cdot P(P_t) \\[1em]
E[\max EV]=\sum_{P_4}\max_{g\in\{2,3,\ldots,12\}}(EV(g|P_4)) \cdot P(P_4)\\[1em]
=\sum_{P_4}\max_{g\in\{2,3,\ldots,12\}}(EV(g|P_4)) \cdot \sum_{S_4}\alpha_4(S_4)
$$

Finding the best legal guess given $P_t$ is simply

$$
\argmax_{g\in\{2,3,\ldots,12\}}(EV(g|P_t))
$$
