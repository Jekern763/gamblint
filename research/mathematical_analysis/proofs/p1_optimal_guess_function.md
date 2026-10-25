# p1: Optimal Guess Function

See `c2`, `c3`

## p1.1 Reflection Property

The payout function is symmetric about the median roll $r=7$.

For any real number $x$, reflection across $7$ is defined by

$$
x' = 14 - x,
$$

so that

$$
x + x' = 14.
$$

Applying this reflection simultaneously to both the player's guess and the actual roll gives

$$
g' = 14-g,\qquad
r' = 14-r.
$$

Then

$$
|g'-r'| = |(14-g)-(14-r)| = |g-r|
$$

and

$$
|g'-7|
=
|(14-g)-7|
=
|g-7|.
$$

$$
\therefore
$$

$$
p(g,r)=p(14-g,\,14-r)
$$

$$
\forall \space g,r\in\mathbb{R}
$$

Consequently, the set of optimal guesses reflects across $r=7$. For $r \ne 7$, where the optimal guess is unique, this gives

$$
G(r)=14-G(14-r).
$$

At $r=7$, the two optimal guesses are $6$ and $8$, which reflect to each other. $\square$

Note that all future parts of p1 will be solved for $r \le 7$

---

## p1.2 $G(r)$ for $r \le g \le 7$

Recall

$$G(r) = \argmax_{g \in \mathbb{R}}(p(g,r))$$

Because $p(g,r) = (2-|g-r|)|g-7|$ is a piecewise function, first solve for,

$$g \ge r, g \le 7 \therefore r \le g \le 7$$

Where

$$
p(g,r) = (2-g+r)(7-g) \\[1em]
= 14 - 2g - 7g + g^2 + 7r - rg \\[1em]
= g^2 - (9+r)g + 14 + 7r
$$

Because the $g^2$ term is positive, this parabola opens upward. Therefore, the maximum on the closed interval $r \le g \le 7$ must occur at one of the boundaries.

Checking boundaries $g=r$ and $g=7$:

At $g=r$:
$$
p(r,r) = (2-r+r)(7-r) = 14-2r
$$

At $g=7$:
$$
p(7,r) = (2-7+r)(7-7) = 0
$$

Checking Bounds:

For $r \le 5$, the boundary $g=r$ yields $14-2r \ge 4$. Since $14-2r > 0$, the maximum payout occurs at $g=r$.

$$
\therefore \\[1.5em]
\forall \space r \in (-\infty, 5]; \space G(r) = r
$$

## p1.3 $G(r)$ for $g \le r \le 7$

For reference: $p(g, r) = (2-|g-r|)|7-g|$

Solving for

$$
g \le r \le 7 \\[2em]
p(g, r) = (2-r+g)(7-g) \\[1em]
= 14 - 2g -7r + rg +7g -g^2 \\[1em]
= -g^2 +g(r+5) -7r +14
$$

Finding the maximum

$$
\frac{\partial p}{\partial g} = -2g + r+5 \\[1em]
0 = -2g + r + 5 \\[1em]
g = \frac{r+5}{2}
$$

Checking Bounds

$$
\frac{r+5}{2} \le r \\[1em]
5 \le r
$$
and
$$
r \le 7
$$

**Global Maximum Check for $r \in [5, 7]$:**
Evaluating the domain $g \ge 7$ for rolls $r \le 7$ yields a second local maximum at $g = \frac{r+9}{2}$. Checking the payouts for $r \in (5, 7]$:

$$
p\left(\frac{r+5}{2}, r\right) = \left(\frac{9-r}{2}\right)^2 \\[1.5em]
p\left(\frac{r+9}{2}, r\right) = \left(\frac{r-5}{2}\right)^2
$$

Because $r \le 7$, $9-r \ge 2$, meaning the first payout is $\ge 1$. Conversely, $r-5 \le 2$, meaning the second payout is $\le 1$. For $5 \le r < 7$, the first payout is strictly larger; at $r=7$, the two payouts are equal, so both $g=6$ and $g=8$ are optimal.

so
$$
\forall \space r \in [5, 7]; G(r) = \frac{r+5}{2}
$$

## p1.4 Applying the reflections

For reference

$$
G(r)=
\begin{cases}
     r & \text{ if } r \le 5 \\
    \frac{r+5}{2}  & \text{if } 5 \le r \le 7
\end{cases}
$$

To reflect the formula for $r \le 5$

$$
G(14-r) = 14-r \\[1em]
G(r) = 14 - G(14-r) \text{ : (p1.1)} \\[1em]
G(r) = 14 - (14-r) \\[1em]
G(r) = r
$$

Similarly for reflecting $5 \le r \le 7$

$$
G(14-r) = \frac{(14-r)+5}{2} \\[1em]
G(r) = 14 - \frac{19-r}{2} \\[1em]
G(r) = \frac{28-19+r}{2} \\[1em]
G(r) = \frac{r+9}{2}
$$

Therefore

$$
\boxed{
G(r)=
\begin{cases}
    r & r \in (-\infty, 5] \cup [9, \infty) \\[1em]
    \frac{r+5}{2}  & r \in [5, 7] \\[1em]
    \frac{r+9}{2}  & r \in [7, 9]
\end{cases}
}
$$

For a graph of this function see `figures/optimum_guess`

## p1.5 Properties

Determing certain properties for this function: funciton validity, continuity, differentiability, injectivity

### p1.5.1 function validity

Does each input produce only on output?

We already know that each of the parts of the piecewise formula are functions themeselves, so we only need to check the hand off points:

$$
r = 5 \\
r= 7 \\
r=9
$$

For $r=5$ and $G(r)$ to be a function
$$
r = \frac{r+5}{2} \\[1em]
5 = \frac{5+5}{2} \\[1em]
5 = 5
$$

For $r=7$

$$
\frac{r+5}{2} = \frac{r+9}{2} \\[1em]
\frac{7+5}{2} = \frac{7+9}{2} \\[1em]
6 \not = 8 \\[1em]
$$

Therefore the argmax is set-valued at $r=7$: the optimal guesses are $G(7)=\{6,8\}$. Thus $G$ is not a single-valued function there unless a tie-breaking rule is chosen.

### p1.5.2 continuity

For $G(r)$ to be continuous, at every break point $b$

$$
\lim _{r \rightarrow b^+}(G(r)) = \lim _{r \rightarrow b^-}(G(r))
$$

As shown in `p1.5.1`, the two branches disagree at $r=7$, so the set-valued optimizer is not an ordinary single-valued function there. If one chooses either branch consistently as a single-valued selection, its continuity must be considered separately; the displayed selection jumps at $r=7$. At $r=5$ and $r=9$, the neighboring formulas agree.

### p1.5.3 differentiability

Because the optimizer is not single-valued at $r=7$, ordinary differentiability is not defined there without a tie-breaking rule. So instead test the branch change at $r=5$ (and use the reflection property)

At $r=5$, the left-hand derivative is $1$, while the right-hand derivative is $1/2$. Since these are unequal, the selected branch is not differentiable at $r=5$. By reflection, the same holds at $r=9$. At $r=7$, the optimizer is set-valued, so differentiability is not defined unless a tie-breaking rule is chosen.

Therefore, for the displayed branches, differentiability fails at the breakpoints as described above:

$$
r=5 \\
r=7 \\
r=9
$$

### p1.5.4 injectivity

For $G(r)$ to be one-to-one, no two distinct inputs may produce the same output. The reflection property alone does not imply that $G(r)=G(14-r)$; instead, it gives $G(r)=14-G(14-r)$ for reflected optimal guesses.

At $r=7$, the optimizer is set-valued, with optimal guesses $6$ and $8$. If a single-valued function is desired, choosing either $6$ or $8$ as the tie-break at $r=7$ gives an injective selection of the displayed branches. Therefore the original claim that $G$ is not injective does not follow and is incorrect.
