# A Closed-Form Solution to a Difference–Integral Recursion and Its Diagonal Generating Function

## Definition

Let $A_t(n)$, for $t\in\mathbb N_0$ and $n\in\mathbb R$, be defined recursively by

$$
A'_t(n)=2tA_{t-1}(n)\tag{D}
$$

$$
A_0(n)=1,\qquad A_t(t)=A_{t-1}(t).\tag{B}
$$

As proved in `integral_recursion_proof.md`, it follows that
$$
A_t(n)=A_{t-1}(t)+\int_t^n 2tA_{t-1}(u)\,du,\qquad t\geq1.
$$

In particular each $A_t$ is a polynomial in $n$, by induction on $t$.

## Conventions

Throughout, generating functions are formal power series, and $[x^t]F(x)$ denotes the coefficient of $x^t$ in $F$. Let $H_t(y)$ be the physicists' Hermite polynomial of degree $t$, with $H_{-1}(y)=0$. We use the following standard facts about formal power series without further comment.

- A series with nonzero constant term is invertible. In particular $\frac1{1-2x}=1+2x+4x^2+\cdots$, and $1-2X(w)$ is invertible whenever $X(0)=0$.
- If $X(0)=0$, then $F(X(w))$ is defined, and the product rule and the chain rule $\bigl(F(X)\bigr)'=F'(X)X'$ hold. If $F(0)=0$, then $e^{F}$ is defined and $(e^F)'=F'e^F$.
- A series whose derivative is $0$ is constant. If $x\cdot S=0$ then $S=0$, since $[x^{k+1}](xS)=[x^k]S$.
- A series in $x$ whose coefficients are polynomials in $n$ can be differentiated in $n$ coefficient by coefficient.

The one outside theorem we use, Lagrange inversion, is isolated in `lagrange_inversion_lemma.md`. From that file we use the series $X(w)$ (the unique series with $X(0)=0$ and $X=we^{2X}$, so $X=w+2w^2+6w^3+\cdots$) and Lemma (L).

## Main Theorem

The exponential generating function of the polynomial sequence is

$$
\boxed{
G(n,x)=\sum_{t\geq0}A_t(n)\frac{x^t}{t!}
=(1-2x)e^{(2n+1)x-x^2}.
}
$$

Consequently,

$$
\boxed{
A_t(n)=H_t\!\left(n+\tfrac12\right)-2tH_{t-1}\!\left(n+\tfrac12\right).
}
$$

Furthermore, let $d_t=A_t(t)$ be the diagonal. Its exponential generating function is

$$
\boxed{
D(w)=\sum_{t\geq0}d_t\frac{w^t}{t!}
=\exp\!\left(-\tfrac12W(-2w)-\tfrac14W(-2w)^2\right),
}
$$

where $W$ is the branch of the Lambert $W$ function with $W(0)=0$, interpreted analytically near the origin or as its formal power series.

## 1. The Generating Function

Differentiating $G$ coefficient by coefficient and applying (D) (the $t=0$ term contributes nothing, since $A_0=1$ is constant),

$$
\begin{aligned}
\frac{\partial G}{\partial n}
&=\sum_{t\geq1}2tA_{t-1}(n)\frac{x^t}{t!}
=2x\sum_{t\geq1}A_{t-1}(n)\frac{x^{t-1}}{(t-1)!}
=2xG.
\end{aligned}
$$

Hence, by the product rule, $\partial_n\bigl(G\,e^{-2nx}\bigr)=e^{-2nx}\bigl(\partial_nG-2xG\bigr)=0$. Every coefficient of a power of $x$ in $Ge^{-2nx}$ is therefore a polynomial in $n$ with derivative $0$, hence constant. So $Ge^{-2nx}$ equals its value at $n=0$:

$$
G(n,x)=C(x)\,e^{2nx},\qquad C(x):=G(0,x)=\sum_{t\geq0}A_t(0)\frac{x^t}{t!},\qquad C(0)=A_0=1.
$$

The numbers $A_t(0)$ are the constants of integration left over by (D). Condition (B) has not been used yet, and it is what will determine them.

Since $1-2x$ is invertible, define $\Psi(x):=C(x)/(1-2x)$, a series with $\Psi(0)=1$. Then

$$
\boxed{G(n,x)=(1-2x)\,\Psi(x)\,e^{2nx},\qquad \Psi(0)=1.}
\tag{1}
$$

The factor $1-2x$ is split off only because it is the factor that appears in Lemma (L). It remains to determine $\Psi$ from (B).

## 2. The Diagonal and the Next-to-Diagonal

Let $X(w)$ be the series from `lagrange_inversion_lemma.md`. Reading off the coefficient of $x^t$ in (1),

$$
A_t(n)=t!\,[x^t]\,(1-2x)\Psi(x)e^{2nx}.
\tag{$*$}
$$

**Diagonal.** Put $n=t$ in $(*)$ and apply Lemma (L):

$$
d_t=A_t(t)=t!\,[x^t]\,(1-2x)\Psi(x)e^{2tx}=t!\,[w^t]\,\Psi(X(w)).
$$

Since $d_t/t!$ is the coefficient of $w^t$ in $D(w)=\sum_t d_t\frac{w^t}{t!}$, this says

$$
\boxed{D(w)=\Psi(X(w)).}
\tag{2}
$$

**Next-to-diagonal.** Let $t\geq1$. Put $t-1$ in place of $t$ and $n=t$ in $(*)$, then use $[x^{t-1}]F=[x^t](xF)$:

$$
A_{t-1}(t)=(t-1)!\,[x^{t-1}]\,(1-2x)\Psi(x)e^{2tx}=(t-1)!\,[x^t]\,(1-2x)\bigl(x\Psi(x)\bigr)e^{2tx}.
$$

Lemma (L), applied to the series $x\Psi(x)$ in place of $\Psi$, turns this into $(t-1)!\,[w^t]\,X(w)\Psi(X(w))$. By (2), this is

$$
A_{t-1}(t)=(t-1)!\,[w^t]\,X(w)D(w).
$$

## 3. The Boundary Condition

Write $\delta_t=[w^t]D=d_t/t!$. For $t\geq1$, condition (B) says $A_t(t)=A_{t-1}(t)$, that is, $t!\,\delta_t=(t-1)!\,[w^t](XD)$. Dividing by $(t-1)!$,

$$
t\,\delta_t=[w^t]\,(XD)\qquad(t\geq1).
$$

For $t=0$ both sides are $0$, because $X(0)=0$. Since $wD'(w)=\sum_t t\,\delta_t\,w^t$, these equations for all $t\geq0$ say exactly

$$
\boxed{wD'(w)=X(w)D(w).}
\tag{3}
$$

## 4. Determining $\Psi$

**An identity for $X$.** Differentiate $X=we^{2X}$ using the product and chain rules: $X'=e^{2X}+2wX'e^{2X}$. Multiply by $w$ and use $we^{2X}=X$:

$$
wX'=X+2X\cdot wX',\qquad\text{that is,}\qquad (1-2X)\,wX'=X.
\tag{4}
$$

**The equation in terms of $\Psi$.** By (2) and the chain rule, $D'=X'\Psi'(X)$. Multiply (3) by $1-2X$, and use (4) on the left and (2) on the right:

$$
X\,\Psi'(X)=(1-2X)\,X\,\Psi(X).
$$

Define the series $R(x):=x\bigl(\Psi'(x)-(1-2x)\Psi(x)\bigr)$. The equation above says $R(X(w))=0$.

**Why $R=0$.** Suppose $R\neq0$, and let $r_mx^m$ with $r_m\neq0$ be its lowest-degree term. Since $X(w)=w+(\text{higher terms})$, we get $R(X(w))=r_mw^m+(\text{higher terms})\neq0$, a contradiction. Hence $R=0$, and cancelling the factor $x$ gives

$$
\Psi'(x)=(1-2x)\Psi(x),\qquad\Psi(0)=1.
\tag{5}
$$

**Solving (5).** Write $\Psi=\sum\psi_kx^k$. Comparing coefficients of $x^k$ in (5) gives $(k+1)\psi_{k+1}=\psi_k-2\psi_{k-1}$, with $\psi_{-1}=0$ and $\psi_0=1$. This determines every $\psi_k$, so (5) has at most one solution. The series $e^{x-x^2}$ has constant term $1$, and by the chain rule its derivative is $(1-2x)e^{x-x^2}$, so it is a solution. Therefore

$$
\boxed{\Psi(x)=e^{x-x^2}.}
$$

Substituting into (1), and using $x-x^2+2nx=(2n+1)x-x^2$, proves the first part of the theorem:

$$
\boxed{G(n,x)=(1-2x)e^{(2n+1)x-x^2}.}
$$

## 5. Hermite-Polynomial Formulas

The physicists' Hermite polynomials are defined by their exponential generating function

$$
\sum_{t\geq0}H_t(y)\frac{x^t}{t!}
=e^{2yx-x^2}.
$$

Set $y=n+\tfrac12$. Then

$$
G(n,x)=(1-2x)e^{2yx-x^2}.
$$

Multiplying the Hermite generating function by $(1-2x)$ gives

$$
\begin{aligned}
G(n,x)
&=\sum_{t\geq0}H_t(y)\frac{x^t}{t!}\\
&\quad-2\sum_{t\geq1}tH_{t-1}(y)\frac{x^t}{t!}.
\end{aligned}
$$

Comparing coefficients yields

$$
\boxed{
A_t(n)=H_t\!\left(n+\frac12\right)
-2tH_{t-1}\!\left(n+\frac12\right).
}
$$

An alternative expansion follows by writing

$$
G(n,x)=\bigl[(1-2x)e^x\bigr]e^{2nx-x^2}.
$$

Since

$$
(1-2x)e^x
=\sum_{m\geq0}(1-2m)\frac{x^m}{m!},
$$

the Hermite generating function at argument $n$ gives

$$
\boxed{
A_t(n)=
\sum_{k=0}^{t}
\binom{t}{k}
\bigl(1-2(t-k)\bigr)H_k(n).
}
$$

Both formulas are consequences of the same generating-function identity.

## 6. The Diagonal and the Lambert $W$ Function

Recall from §2 that the diagonal sequence $d_t=A_t(t)$ has exponential generating function

$$
D(w)=\sum_{t\geq0}d_t\frac{w^t}{t!}=\Psi(X(w)).
$$

Since $\Psi(x)=e^{x-x^2}$,

$$
\boxed{D(w)=e^{X(w)-X(w)^2}.}
\tag{6}
$$

It remains to express $X(w)$ using the Lambert $W$ function.

Recall that

$$
X(w)=we^{2X(w)}.
$$

Rearranging gives

$$
X(w)e^{-2X(w)}=w.
$$

Multiplying by $-2$,

$$
(-2X(w))e^{-2X(w)}=-2w.
$$

The Lambert $W$ function is defined by the inverse relation

$$
W(z)e^{W(z)}=z.
$$

A series $V$ with $V(0)=0$ and $Ve^{V}=-2w$ is unique, since the coefficient of $w^t$ in $Ve^V$ is $[w^t]V$ plus an expression in the lower coefficients of $V$. So $-2X(w)$ is the series $W(-2w)$.

The solution with $X(0)=0$ consequently satisfies

$$
\boxed{X(w)=-\frac12W(-2w).}
$$

Substituting into (6),

$$
\begin{aligned}
D(w)
&=\exp\left(
-\frac12W(-2w)
-\frac14W(-2w)^2
\right).
\end{aligned}
$$

Hence the diagonal's exponential generating function is

$$
\boxed{
D(w)=
\exp\left(
-\frac12W(-2w)-\frac14W(-2w)^2
\right).
}
$$

This derives the Lambert-$W$ expression directly from the recursive polynomial system, rather than assuming the diagonal's generating function in advance.

## Conclusion

The integral recursion uniquely determines a polynomial sequence whose exponential generating function is

$$
G(n,x)=(1-2x)e^{(2n+1)x-x^2}.
$$

Its diagonal has the Lambert-$W$ exponential generating function

$$
D(w)=
\exp\left(
-\frac12W(-2w)-\frac14W(-2w)^2
\right).
$$

The main mechanism is the transformation of the diagonal boundary condition into coefficient identities, followed by Lagrange–Bürmann inversion. The inversion converts those identities into a differential equation for $C(x)/(1-2x)$, which uniquely determines the generating function and yields the diagonal formula.

## Remarks (not used in the proof)

**Worked values.** The first polynomials are $A_0=1$, $A_1=2n-1$, $A_2=4n^2-4n-5$, $A_3=8n^3-12n^2-30n+1$, so $C(x)=1-x-\tfrac52x^2+\tfrac16x^3+\cdots=(1-2x)e^{x-x^2}$. The diagonal begins $d_0,d_1,d_2,d_3,d_4=1,1,3,19,201$. Equation (3) at low order: $X=w+2w^2+\cdots$ and $D=1+w+\tfrac32w^2+\cdots$ give $wD'=w+3w^2+\cdots=XD$.

**Combinatorial meaning of the diagonal.** As described in `lagrange_inversion_lemma.md`, $X(w)$ is the exponential generating function of rooted labeled trees with each edge weighted $2$. In any tree, $\#\text{vertices}-\#\text{edges}=1$. So (tree with a marked vertex) minus (tree with a marked edge) counts each tree once. A marked vertex is counted by $X$. A marked edge splits the tree into an unordered pair of rooted trees ($X^2/2$) and carries weight $2$, so it is counted by $X^2$. Unrooted trees are therefore counted by $X-X^2$, a forest is a set of trees, and

$$
D(w)=e^{X-X^2}\quad\Longrightarrow\quad d_t=\sum_{F\text{ a forest on }[t]}2^{\,\#\text{edges}(F)}.
$$

For example $d_3=1+3\cdot2+3\cdot4=19$ and $d_4=1+6\cdot2+15\cdot4+16\cdot8=201$. By the standard description of the permutohedron $P_t$ as a zonotope (Stanley), its Ehrhart polynomial is $\sum_F s^{\#\text{edges}(F)}$ over forests $F$ on $[t]$. At $s=2$ this is the number of lattice points of $2P_t$, so $d_t$ is that count. In the proof above, the exponent $x-x^2$ of $\Psi$ is "vertices minus edges", and it was obtained from (D) and (B) alone.