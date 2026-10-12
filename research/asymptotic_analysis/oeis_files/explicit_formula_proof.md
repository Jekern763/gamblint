# A Closed-Form Solution to a Difference–Integral Recursion and Its Diagonal Generating Function

## Definition

Let $A_t(n)$, for $t\in\mathbb N_0$ and $n\in\mathbb R$, be defined recursively by

$$
A'_t(n)=2tA_{t-1}(n)\tag{D}
$$

$$
A_0(n)=1,\qquad A_t(t)=A_{t-1}(t).\tag{B}
$$

As proved in `integral_recursion_proof.md`,

$$
A_t(n)=A_{t-1}(t)+\int_t^n 2tA_{t-1}(u)\,du,\qquad t\geq1.
$$

In particular, each $A_t$ is a polynomial in $n$.

## Conventions

All generating functions are formal power series over $\mathbb R$, and $[x^t]F(x)$ denotes the coefficient of $x^t$ in $F(x)$. Differentiation is coefficientwise; we use the standard product, chain, and exponential rules. Composition $F(X(w))$ is valid when $X(0)=0$. A series with nonzero constant term has a multiplicative inverse; in particular, $1-2x$ is invertible. A series with zero derivative is constant, coefficient by coefficient. Let $H_t(y)$ be the physicists' Hermite polynomial of degree $t$, with $H_{-1}(y)=0$.

The tags (D) and (B) refer to the differential recursion and boundary condition in the Definition. The numbered tags (1)–(8) label equations used later in this proof, and (BC) labels the coefficient identity obtained from the boundary condition. The tag (L) refers to the coefficient-transfer lemma proved in the companion note `lagrange_inversion_lemma.md`. That note derives (L) from the standard Lagrange–Bürmann formula, for which it gives a reference.

## Main Theorem

The exponential generating function of the polynomial sequence is

$$
\boxed{G(n,x)=\sum_{t\geq0}A_t(n)\frac{x^t}{t!}=(1-2x)e^{(2n+1)x-x^2}.}
$$

Consequently,

$$
\boxed{A_t(n)=H_t\!\left(n+\frac12\right)-2tH_{t-1}\!\left(n+\frac12\right).}
$$

Where $H_t$ is the physicists Hermite polynomial

For the diagonal $d_t=A_t(t)$, its exponential generating function is

$$
\boxed{D(w)=\sum_{t\geq0}d_t\frac{w^t}{t!}=\exp\!\left(-\frac12W(-2w)-\frac14W(-2w)^2\right),}
$$

where $W$ is the Lambert $W$ branch satisfying $W(0)=0$.

## 1. The Generating Function

Differentiating $G$ coefficient by coefficient and applying (D),

$$
\begin{aligned}
\frac{\partial G}{\partial n}
&=\sum_{t\geq1}2tA_{t-1}(n)\frac{x^t}{t!}\\
&=2x\sum_{t\geq1}A_{t-1}(n)\frac{x^{t-1}}{(t-1)!}\\
& j:=t-1\\
&= 2x\sum_{j\ge0}A_j(n)\frac{x^j}{j!}\\
&\frac{\partial{G}}{\partial{n}}=2xG.
\end{aligned}
$$

The last equality follows by changing the index from $t$ to $t-1$; the resulting sum is the definition of $G$.

By the product rule,

$$
\frac{\partial}{\partial n}\left(Ge^{-2nx}\right)
=e^{-2nx}\left(\frac{\partial G}{\partial n}-2xG\right)=0.
$$

Thus each coefficient of $Ge^{-2nx}$ is independent of $n$, so $Ge^{-2nx}=G(0,x)$. Since $G(0,0)=A_0(0)=1$, we have

$$
G(n,x)=G(0,x)e^{2nx},\qquad G(0,0)=1.
$$

Since $1-2x$ has constant term $1$, define

$$
\Psi(x):= \frac{G(0,x)}{(1-2x)}
$$

This is a valid formal power series and $\Psi(0)=1$. We have

$$
\boxed{G(n,x)=(1-2x)\Psi(x)e^{2nx},\qquad \Psi(0)=1.}\tag{1}
$$

The factor $1-2x$ is chosen because it is exactly the factor in the coefficient-transfer lemma used next.

## 2. The Diagonal and the Next-to-Diagonal

The coefficient formula from (1) is

$$
\boxed{A_t(n)=t![x^t](1-2x)\Psi(x)e^{2nx}.}\tag{2}
$$

Let $X(w)$ be the unique formal power series satisfying

$$
X(w)=we^{2X(w)},\qquad X(0)=0.
$$

By Lemma (L), proved in `lagrange_inversion_lemma_revised.md`,

$$
\boxed{[w^t]\Psi(X(w))=[x^t](1-2x)\Psi(x)e^{2tx}.}\tag{L}
$$

We will use this single identity for both the diagonal and its neighboring values.

**Diagonal.** Put $n=t$ in (2). By (L),

$$
A_t(t)=t![x^t](1-2x)\Psi(x)e^{2tx}=t![w^t]\Psi(X(w)).
$$

Writing an e.g.f. for the diagonal

$$
D(w) = \sum_{t\geq0}A_t(t) \frac{w^t}{t!} \\
\begin{aligned}
&= \sum_{t\ge0}t![w^t]\Psi(X(w))\frac{w^t}{t!}
\end{aligned}\\

\boxed{D(w)=\Psi(X(w)).}\tag{3}
$$

**Next-to-diagonal.** For $t\geq1$, put $n=t$ and replace the polynomial index $t$ in (2) by $t-1$:

$$
A_{t-1}(t)=(t-1)![x^{t-1}](1-2x)\Psi(x)e^{2tx}.
$$

The coefficient-shift identity $[x^{t-1}]F(x)=[x^t]xF(x)$ gives

$$
A_{t-1}(t)=(t-1)![x^t](1-2x)\bigl(x\Psi(x)\bigr)e^{2tx}.
$$

Apply (L) to the series $x\Psi(x)$, then use (3):

$$
A_{t-1} = (t-1)![w^t]X(w)\Psi(X(w))\\[1em]
\boxed{A_{t-1}(t)=(t-1)![w^t]X(w)D(w).}\tag{4}
$$

## 3. The Boundary Condition

By (B), $A_t(t)=A_{t-1}(t)$. Combining (3) and (4),

$$
t![w^t]D(w)=(t-1)![w^t]X(w)D(w).
$$

Dividing by $(t-1)!$ gives

$$
\boxed{t[w^t]D(w)=[w^t]X(w)D(w),\qquad t\geq1.}\tag{BC}
$$

The same coefficient identity holds for $t=0$, since both sides are zero: the left has a factor $t$, and $X(0)=0$ makes the constant term of $XD$ zero. By termwise differentiation,

$$
\begin{aligned}
D'(w) &= \sum_{t\ge1}\frac{tA_t(t)}{t!}w^{t-1}\\
wD'(w) &= \sum_{t\geq1}t\frac{A_t(t)}{t!}w^t\\
wD'(w)&=\sum_{t\geq1}t[w^t]D(w)\,w^t.
\end{aligned}
$$

By (BC), the coefficient of $w^t$ in this series equals the coefficient of $w^t$ in $XD$ for every $t\geq1$; both constant terms are zero as well. Therefore,

$$
\boxed{wD'(w)=X(w)D(w).}\tag{5}
$$

## 4. Determining $\Psi$

**An identity for $X$.** Differentiate $X=we^{2X}$ using the product and chain rules:

$$
X'=e^{2X}+2we^{2X}X'.
$$

Multiply by $w$ and use $we^{2X}=X$:

$$
wX'=X+2XwX',
$$

so

$$
\boxed{(1-2X)wX'=X.}\tag{6}
$$

**Obtain an equation for $\Psi$.** By (3), $D=\Psi(X)$. The chain rule gives $D'=X'\Psi'(X)$. Substitute this and $D=\Psi(X)$ into (5):

$$
wX'\Psi'(X)=X\Psi(X).
$$

Multiply by $1-2X$ and use (6):

$$
X\Psi'(X)=(1-2X)X\Psi(X).
$$

Hence, with

$$
R(x):=x\bigl(\Psi'(x)-(1-2x)\Psi(x)\bigr),
$$

we have $R(X(w))=0$.

**Why this implies $R(x)=0$.** If $R$ were nonzero, let $r_mx^m$ be its lowest-degree nonzero term, with $r_m\neq0$. Since $X(w)=w+\text{higher-degree terms}$, the lowest-degree term of $R(X(w))$ would be $r_mw^m$, so $R(X(w))$ could not be zero. This contradiction shows that $R=0$. Multiplication by $x$ only shifts a series' coefficients, so we can cancel the factor $x$ to obtain

$$
\boxed{\Psi'(x)=(1-2x)\Psi(x),\qquad \Psi(0)=1.}\tag{7}
$$

**Solve the equation.** Write $\Psi(x)=\sum_{k\geq0}\psi_kx^k$, with $\psi_{-1}=0$. Comparing coefficients in (7) gives

$$
(k+1)\psi_{k+1}=\psi_k-2\psi_{k-1}.
$$

Since $\psi_0=1$, this recurrence determines all coefficients uniquely. The series $e^{x-x^2}$ has constant term $1$ and

$$
\frac{d}{dx}e^{x-x^2}=(1-2x)e^{x-x^2}.
$$

It is therefore the unique solution:

$$
\boxed{\Psi(x)=e^{x-x^2}.}\tag{8}
$$

Substituting (8) into (1) proves the generating-function formula:

$$
\boxed{G(n,x)=(1-2x)e^{(2n+1)x-x^2}.}
$$

## 5. Hermite-Polynomial Formulas

The physicists' Hermite polynomials are defined by

$$
\sum_{t\geq0}H_t(y)\frac{x^t}{t!}=e^{2yx-x^2}.
$$

Set $y=n+\tfrac12$. Then

$$
G(n,x)=(1-2x)e^{2yx-x^2}.
$$

Multiplying the Hermite generating function by $1-2x$ gives

$$
\begin{aligned}
G(n,x)
&=\sum_{t\geq0}H_t(y)\frac{x^t}{t!}
-2\sum_{t\geq1}tH_{t-1}(y)\frac{x^t}{t!}.
\end{aligned}
$$

Comparing coefficients yields

$$
\boxed{A_t(n)=H_t\!\left(n+\frac12\right)-2tH_{t-1}\!\left(n+\frac12\right).}
$$

An alternative expansion follows from

$$
G(n,x)=\bigl[(1-2x)e^x\bigr]e^{2nx-x^2}.
$$

Since

$$
(1-2x)e^x=\sum_{m\geq0}(1-2m)\frac{x^m}{m!},
$$

multiplying by the Hermite generating function at argument $n$ and collecting the coefficient of $x^t$ gives

$$
\boxed{A_t(n)=\sum_{k=0}^{t}\binom{t}{k}\bigl(1-2(t-k)\bigr)H_k(n).}
$$

## 6. The Diagonal and the Lambert $W$ Function

From (3) and (8),

$$
D(w)=\Psi(X(w))=e^{X(w)-X(w)^2}.
$$

Section 2 identified $X(w)=-\tfrac12W(-2w)$. Substituting this into the exponent gives

$$
X(w)-X(w)^2=-\frac12W(-2w)-\frac14W(-2w)^2.
$$

Thus the diagonal's exponential generating function is

$$
\boxed{D(w)=\exp\!\left(-\frac12W(-2w)-\frac14W(-2w)^2\right).}
$$

## 7. Summary of Findings

The recursion and boundary condition uniquely determine the polynomial sequence and its diagonal. The following are equivalent descriptions obtained above.

**Generating function and coefficient formula:**

$$
G(n,x)=\sum_{t\geq0}A_t(n)\frac{x^t}{t!}=(1-2x)e^{(2n+1)x-x^2},
$$

$$
A_t(n)=t![x^t](1-2x)e^{(2n+1)x-x^2}.
$$

**Two Hermite forms:**

$$
A_t(n)=H_t\!\left(n+\frac12\right)-2tH_{t-1}\!\left(n+\frac12\right),
$$

$$
A_t(n)=\sum_{k=0}^{t}\binom{t}{k}\bigl(1-2(t-k)\bigr)H_k(n).
$$

**Diagonal in terms of Hermite polynomials:**

$$
d_t=H_t\!\left(t+\frac12\right)-2tH_{t-1}\!\left(t+\frac12\right).
$$

**Diagonal exponential generating function in terms of Lambert $W$:**

$$
D(w)=\sum_{t\geq0}d_t\frac{w^t}{t!}=\exp\!\left(-\frac12W(-2w)-\frac14W(-2w)^2\right).
$$

Together, these give an identity connecting Hermite polynomials evaluated along the diagonal with Lambert $W$:

$$
\sum_{t\geq0}\left[H_t\!\left(t+\frac12\right)-2tH_{t-1}\!\left(t+\frac12\right)\right]\frac{w^t}{t!}
=\exp\!\left(-\frac12W(-2w)-\frac14W(-2w)^2\right).
$$

The diagonal begins

$$
d_0,d_1,d_2,d_3,d_4=1,1,3,19,201.
$$

There is also a combinatorial interpretation. The series $X$ is the exponential generating function for rooted labeled trees with each edge weighted $2$. The exponential generating function for unrooted trees with this edge weight is $X-X^2$: a tree with $t$ vertices has $t$ choices of a marked vertex and $t-1$ choices of a marked edge, so subtracting the edge-rooted count from the vertex-rooted count leaves one copy of each tree. A forest is a set of trees, giving

$$
D(w)=e^{X(w)-X(w)^2}\quad\Longrightarrow\quad d_t=\sum_{F\text{ a forest on }[t]}2^{|E(F)|}.
$$

For instance, on three vertices there is one empty forest, three one-edge forests, and three two-edge trees, so $d_3=1+3\cdot2+3\cdot4=19$. On four vertices, the corresponding count is $1+6\cdot2+15\cdot4+16\cdot8=201$.

The standard forest expansion of the Ehrhart polynomial of the permutohedron $P_t$ is

$$
\operatorname{Ehr}_{P_t}(s)=\sum_{F\text{ a forest on }[t]}s^{|E(F)|}.
$$

Setting $s=2$ shows that the same sum counts the lattice points of $2P_t$. This final identification uses the known forest expansion for the permutohedron; it is a combinatorial connection to the result proved here, rather than a step needed to derive the generating functions.
