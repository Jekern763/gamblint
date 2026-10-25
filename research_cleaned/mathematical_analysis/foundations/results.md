# Results

## Optimum Guess Function

Let $G(r)$ denote an optimal guess for roll $r$. At $r=7$, there are two optimal guesses, $6$ and $8$, so the argmax is set-valued there.

$$
G(r)=
\begin{cases}
    r & r \in (-\infty, 5] \cup [9, \infty) \\[1em]
    \frac{r+5}{2}  & r \in [5, 7] \\[1em]
    \frac{r+9}{2}  & r \in [7, 9]
\end{cases}
$$

See `proofs/p1_optimal_guess_function`

## Maximum Payout Function

Let $M(r)$ be the maximum payout for any $r$

$$
M(r) =
\begin{cases}
14-2r & r \le 5 \\[1em]
\frac{(9-r)^2}{4} & 5 \le r \le 7 \\[1em]
\frac{(r-5)^2}{4} & 7 \le r \le 9 \\[1em]
2r-14 & r \ge 9
\end{cases}
$$

See `proofs/p2_maximum_payout_function.md`

## Invariant Sum Formula

For any game state at turn $t$:
$$\Sigma_{P_t} + \Sigma_{F_t} = n(n+1)$$

For the standard game ($n=6$):
$$\Sigma_{P_t} + \Sigma_{F_t} = 42$$

See `proofs/p3_invariant_sum.md`

## Game State Transition

$$
\mathcal{T}(S_t) = \left\{
S_{t+1}:
    \begin{array}{l}
        A_{t+1}^{(1)} = A_t^{(1)} \backslash \set{r^{(1)}} \\[1em]
        A_{t+1}^{(2)} = A_t^{(2)} \backslash \set{r^{(2)}} \\[1em]
        r^{(1)} \in A_t^{(1)}, r^{(2)} \in A_t^{(2)}
    \end{array}
\right\}
$$

$$
P(S_{t+1} \mid S_t) =
\begin{cases}
\frac{1}{(6-t)^2}, & S_{t+1}\in \mathcal{T}(S_t) \\[1em]
0, & S_{t+1} \not \in \mathcal{T}(S_t)
\end{cases}
$$

See `proofs/p4_game_state_transition.md`

## Next Peek Given Game State

$$
N(p, S) = \left|
    \left\{
        \begin{array}{l}
            (x, y) \in A^{(1)} \times A^{(2)} : x+y=S
        \end{array}
    \right\}
\right|  
$$

$$
P(p_{t+1} \mid S_t) = \frac{N(p_{t+1}, S_t)}{(6-t)^2}
$$

For the standard game, $t=4$, so the denominator is $4$.

See `proofs/p5_peek_likelihood_given_state`

## Probability of Game State

$$
P(S_t)=\frac{1}{\binom{6}{t}^2}
$$

See `proofs/p6_state_likelihood`

## Next Peek Given Peek History

$$
P(p_{t+1} \mid P_t) =
\sum_{S_t} \frac{N(p_{t+1},S_t)}{(6-t)^2} \cdot \frac{
    \alpha_t(S_t)
}{
    \sum_{S_t}\alpha_t(S_t)
}
$$

## Expected Value

$$
EV(g|P_t)=|g-7| \cdot (2-\sum_{r=2}^{12}|g-r| \cdot P(r|P_t)) \\[1em]

E[\max EV]=\sum_{P_4}\max_{g\in\{2,3,\ldots,12\}}EV(g|P_4) \cdot \sum_{S_4}\alpha_4(S_4)
$$

**State convention:** The probability formula above is for ordered states, where the two dice are distinguished. If an implementation merges states by sorting the two remaining-face sets, probabilities of merged states must be obtained by adding the probabilities of the corresponding ordered states.
