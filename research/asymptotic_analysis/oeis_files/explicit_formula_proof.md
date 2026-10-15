# A Closed-Form Solution to a Difference–Integral Recursion and Its Diagonal Generating Function

## Definition

Let $A_t(n;s)$, for $t\in\mathbb N_0$ and $n\in\mathbb R$, be defined recursively for each fixed parameter $s>0$ by

$$
A'_t(n;s)=stA_{t-1}(n;s)\tag{D}
$$

$$
A_0(n;s)=1,\qquad A_t(t;s)=A_{t-1}(t;s).\tag{B}
$$

In relaton to the OEIS entry define $T(t,n):=A_t(n;s)$.

As proved in `integral_recursion_proof.md`,

$$
A_t(n;s)=A_{t-1}(t;s)+\int_t^n stA_{t-1}(u;s)\,du,\qquad t\geq1.
$$

In particular, each $A_t(n;s)$ is a polynomial in $n$ for fixed $s$.

## Conventions

All generating functions are formal power series over $\mathbb R$, with $s>0$ treated as a fixed parameter. For a series $F(x)$, $[x^t]F(x)$ denotes the coefficient of $x^t$ in $F(x)$. Differentiation is coefficientwise; we use the standard product, chain, and exponential rules. Composition $F(X_s(w))$ is valid when $X_s(0)=0$. A series with nonzero constant term has a multiplicative inverse; in particular, $1-sx$ is invertible. A series with zero derivative is constant, coefficient by coefficient. Let $H_t(y)$ be the physicists' Hermite polynomial of degree $t$, with $H_{-1}(y)=0$.

The tags (D) and (B) refer to the differential recursion and boundary condition in the Definition. The numbered tags (1)–(8) label equations used later in this proof, and (BC) labels the coefficient identity obtained from the boundary condition. The tag (L) refers to the coefficient-transfer lemma proved in the companion note `lagrange_inversion_lemma.md`. That note derives (L) from the standard Lagrange–Bürmann formula, for which it gives a reference.

## Main Theorem

The exponential generating function of the polynomial sequence is

$$
\boxed{
G(n,x;s)=\sum_{t\geq0}A_t(n;s)\frac{x^t}{t!}
=(1-sx)e^{(sn+1)x-\frac{s}{2}x^2}.
}
$$

Consequently,

$$
\boxed{
A_t(n;s)=
\left(\frac{s}{2}\right)^{t/2}
H_t\!\left(\frac{sn+1}{\sqrt{2s}}\right)
-st\left(\frac{s}{2}\right)^{(t-1)/2}
H_{t-1}\!\left(\frac{sn+1}{\sqrt{2s}}\right).
}
$$

where $H_t$ is the physicists' Hermite polynomial.

For the diagonal $d_t(s)=A_t(t;s)$, its exponential generating function is

$$
\boxed{
D(w;s)=\sum_{t\geq0}d_t(s)\frac{w^t}{t!}
=\exp\!\left(
-\frac1sW(-sw)-\frac{1}{2s}W(-sw)^2
\right),
}
$$

where $W$ is the Lambert $W$ branch satisfying $W(0)=0$.

## 1. The Generating Function

Differentiating $G$ coefficient by coefficient and applying (D),

$$
\begin{aligned}
\frac{\partial G}{\partial n}
&=\sum_{t\geq1}stA_{t-1}(n;s)\frac{x^t}{t!}\\
&=sx\sum_{t\geq1}A_{t-1}(n;s)\frac{x^{t-1}}{(t-1)!}\\
&=sx\sum_{j\geq0}A_j(n;s)\frac{x^j}{j!}\\
&=sxG.
\end{aligned}
$$

The third line follows by changing the index from $t$ to $t-1$; the resulting sum is the definition of $G$.

By the product rule,

$$
\frac{\partial}{\partial n}\left(Ge^{-snx}\right)
=e^{-snx}\left(\frac{\partial G}{\partial n}-sxG\right)=0.
$$

Thus each coefficient of $Ge^{-snx}$ is independent of $n$, so $Ge^{-snx}=G(0,x;s)$. Since $G(0,0;s)=A_0(0;s)=1$, we have

$$
G(n,x;s)=G(0,x;s)e^{snx},\qquad G(0,0;s)=1.
$$

Since $1-sx$ has constant term $1$, define

$$
\Psi_s(x):=\frac{G(0,x;s)}{1-sx}.
$$

This is a valid formal power series and $\Psi_s(0)=1$. We have

$$
\boxed{
G(n,x;s)=(1-sx)\Psi_s(x)e^{snx},\qquad \Psi_s(0)=1.
}\tag{1}
$$

The factor $1-sx$ is chosen because it is exactly the factor in the coefficient-transfer lemma used next.

## 2. The Diagonal and the Next-to-Diagonal

The coefficient formula from (1) is

$$
\boxed{
A_t(n;s)=t![x^t](1-sx)\Psi_s(x)e^{snx}.
}\tag{2}
$$

Let $X_s(w)$ be the unique formal power series satisfying

$$
X_s(w)=we^{sX_s(w)},\qquad X_s(0)=0.
$$

By Lemma (L), proved in `lagrange_inversion_lemma.md`,

$$
\boxed{
[w^t]\Psi_s(X_s(w))
=[x^t](1-sx)\Psi_s(x)e^{stx}.
}\tag{L}
$$

We will use this single identity for both the diagonal and its neighboring values.

**Diagonal.** Put $n=t$ in (2). By (L),

$$
A_t(t;s)=t![x^t](1-sx)\Psi_s(x)e^{stx}
=t![w^t]\Psi_s(X_s(w)).
$$

Writing an e.g.f. for the diagonal,

$$
\begin{aligned}
D(w;s)&=\sum_{t\geq0}A_t(t;s)\frac{w^t}{t!}\\
&=\sum_{t\geq0}t![w^t]\Psi_s(X_s(w))\frac{w^t}{t!}.
\end{aligned}
$$

Therefore,

$$
\boxed{D(w;s)=\Psi_s(X_s(w)).}\tag{3}
$$

**Next-to-diagonal.** For $t\geq1$, put $n=t$ and replace the polynomial index $t$ in (2) by $t-1$:

$$
A_{t-1}(t;s)=(t-1)![x^{t-1}](1-sx)\Psi_s(x)e^{stx}.
$$

The coefficient-shift identity $[x^{t-1}]F(x)=[x^t]xF(x)$ gives

$$
A_{t-1}(t;s)
=(t-1)![x^t](1-sx)\bigl(x\Psi_s(x)\bigr)e^{stx}.
$$

Apply (L) to the series $x\Psi_s(x)$, then use (3):

$$
A_{t-1}(t;s)=(t-1)![w^t]X_s(w)\Psi_s(X_s(w)).
$$

Thus,

$$
\boxed{
A_{t-1}(t;s)=(t-1)![w^t]X_s(w)D(w;s).
}\tag{4}
$$

## 3. The Boundary Condition

By (B), $A_t(t;s)=A_{t-1}(t;s)$. Combining (3) and (4),

$$
t![w^t]D(w;s)=(t-1)![w^t]X_s(w)D(w;s).
$$

Dividing by $(t-1)!$ gives

$$
\boxed{
t[w^t]D(w;s)=[w^t]X_s(w)D(w;s),\qquad t\geq1.
}\tag{BC}
$$

The same coefficient identity holds for $t=0$, since both sides are zero: the left has a factor $t$, and $X_s(0)=0$ makes the constant term of $X_sD$ zero. By termwise differentiation,

$$
\begin{aligned}
D'(w;s)&=\sum_{t\geq1}\frac{tA_t(t;s)}{t!}w^{t-1}\\
wD'(w;s)&=\sum_{t\geq1}t\frac{A_t(t;s)}{t!}w^t\\
wD'(w;s)&=\sum_{t\geq1}t[w^t]D(w;s)\,w^t.
\end{aligned}
$$

By (BC), the coefficient of $w^t$ in this series equals the coefficient of $w^t$ in $X_sD$ for every $t\geq1$; both constant terms are zero as well. Therefore,

$$
\boxed{wD'(w;s)=X_s(w)D(w;s).}\tag{5}
$$

## 4. Determining $\Psi_s$

**An identity for $X_s$.** Differentiate $X_s=we^{sX_s}$ using the product and chain rules:

$$
X_s'=e^{sX_s}+swe^{sX_s}X_s'.
$$

Multiply by $w$ and use $we^{sX_s}=X_s$:

$$
wX_s'=X_s+sX_swX_s',
$$

so

$$
\boxed{(1-sX_s)wX_s'=X_s.}\tag{6}
$$

**Obtain an equation for $\Psi_s$.** By (3), $D=\Psi_s(X_s)$. The chain rule gives $D'=X_s'\Psi_s'(X_s)$. Substitute this and $D=\Psi_s(X_s)$ into (5):

$$
wX_s'\Psi_s'(X_s)=X_s\Psi_s(X_s).
$$

Multiply by $1-sX_s$ and use (6):

$$
X_s\Psi_s'(X_s)=(1-sX_s)X_s\Psi_s(X_s).
$$

Since $X_s(w)=w+O(w^2)$, multiplication by $X_s$ is injective on formal power series. We obtain

$$
\Psi_s'(X_s)=(1-sX_s)\Psi_s(X_s).
$$

Substitution of $X_s(w)$ for $x$ is injective on formal power series because $X_s(w)=w+O(w^2)$. Consequently,

$$
\boxed{
\Psi_s'(x)=(1-sx)\Psi_s(x),\qquad \Psi_s(0)=1.
}\tag{7}
$$

**Solve the equation.** Using the known form $y'=cy$, or equivalently solving this first-order equation coefficientwise, the unique solution is

$$
\boxed{\Psi_s(x)=e^{x-\frac{s}{2}x^2}.}\tag{8}
$$

Substituting (8) into (1) proves the generating-function formula:

$$
\begin{aligned}
G(n,x;s)&=(1-sx)\Psi_s(x)e^{snx}\\
&=(1-sx)e^{x-\frac{s}{2}x^2}e^{snx}.
\end{aligned}
$$

Therefore,

$$
\boxed{
G(n,x;s)=(1-sx)e^{(sn+1)x-\frac{s}{2}x^2}.
}
$$

## 5. Hermite-Polynomial Formulas

The physicists' Hermite polynomials are defined by

$$
\sum_{t\geq0}H_t(y)\frac{z^t}{t!}=e^{2yz-z^2}.
$$

Set

$$
y=\frac{sn+1}{\sqrt{2s}},
\qquad z=\sqrt{\frac{s}{2}}\,x.
$$

Then

$$
G(n,x;s)=(1-sx)e^{2yz-z^2}.
$$

Multiplying the Hermite generating function by $1-sx$ gives

$$
\begin{aligned}
G(n,x;s)
&=\sum_{t\geq0}
\left(\frac{s}{2}\right)^{t/2}
H_t(y)\frac{x^t}{t!}\\
&\quad-s\sum_{t\geq1}
t\left(\frac{s}{2}\right)^{(t-1)/2}
H_{t-1}(y)\frac{x^t}{t!}.
\end{aligned}
$$

Comparing coefficients yields

$$
\boxed{
A_t(n;s)=
\left(\frac{s}{2}\right)^{t/2}
H_t\!\left(\frac{sn+1}{\sqrt{2s}}\right)
-st\left(\frac{s}{2}\right)^{(t-1)/2}
H_{t-1}\!\left(\frac{sn+1}{\sqrt{2s}}\right).
}
$$

An alternative expansion follows from

$$
G(n,x;s)=\bigl[(1-sx)e^x\bigr]e^{snx-\frac{s}{2}x^2}.
$$

Since

$$
(1-sx)e^x
=\sum_{m\geq0}(1-sm)\frac{x^m}{m!},
$$

multiplying by the Hermite generating function with $y=n\sqrt{s/2}$ and $z=\sqrt{s/2}\,x$, then collecting the coefficient of $x^t$, gives

$$
\boxed{
A_t(n;s)=
\sum_{k=0}^{t}\binom{t}{k}
\bigl(1-s(t-k)\bigr)
\left(\frac{s}{2}\right)^{k/2}
H_k\!\left(n\sqrt{\frac{s}{2}}\right).
}
$$

## 6. The Diagonal and the Lambert $W$ Function

From (3) and (8),

$$
D(w;s)=\Psi_s(X_s(w))
=e^{X_s(w)-\frac{s}{2}X_s(w)^2}.
$$

Section 2's definition of $X_s$ gives

$$
X_s(w)=-\frac1sW(-sw).
$$

Substituting this into the exponent gives

$$
X_s(w)-\frac{s}{2}X_s(w)^2
=-\frac1sW(-sw)-\frac{1}{2s}W(-sw)^2.
$$

Thus the diagonal's exponential generating function is

$$
\boxed{
D(w;s)=\exp\!\left(
-\frac1sW(-sw)-\frac{1}{2s}W(-sw)^2
\right).
}
$$

For $s=2$, this reduces to the e.g.f. in [OEIS entry A362968](https://oeis.org/A362968), which counts the integral points in twice the permutohedron of order $n$. The generalized formula above describes the corresponding diagonal for the recursion with arbitrary fixed $s>0$; the stated connection to A362968 is specifically the case $s=2$.

## 7. Summary of Findings

The recursion and boundary condition uniquely determine the polynomial sequence and its diagonal. The following are equivalent descriptions obtained above.

**Generating function and coefficient formula:**

$$
G(n,x;s)=\sum_{t\geq0}A_t(n;s)\frac{x^t}{t!}
=(1-sx)e^{(sn+1)x-\frac{s}{2}x^2},
$$

$$
A_t(n;s)=t![x^t](1-sx)e^{(sn+1)x-\frac{s}{2}x^2}.
$$

**Two Hermite forms:**

$$
\begin{aligned}
A_t(n;s)
&=\left(\frac{s}{2}\right)^{t/2}
H_t\!\left(\frac{sn+1}{\sqrt{2s}}\right)\\
&\quad-st\left(\frac{s}{2}\right)^{(t-1)/2}
H_{t-1}\!\left(\frac{sn+1}{\sqrt{2s}}\right),
\end{aligned}
$$

$$
A_t(n;s)=
\sum_{k=0}^{t}\binom{t}{k}
\bigl(1-s(t-k)\bigr)
\left(\frac{s}{2}\right)^{k/2}
H_k\!\left(n\sqrt{\frac{s}{2}}\right).
$$

**Diagonal in terms of Hermite polynomials:**

$$
\begin{aligned}
A_t(t;s)
&=\left(\frac{s}{2}\right)^{t/2}
H_t\!\left(\frac{st+1}{\sqrt{2s}}\right)\\
&\quad-st\left(\frac{s}{2}\right)^{(t-1)/2}
H_{t-1}\!\left(\frac{st+1}{\sqrt{2s}}\right).
\end{aligned}
$$

**Diagonal exponential generating function in terms of Lambert $W$:**

$$
D(w;s)=\sum_{t\geq0}A_t(t;s)\frac{w^t}{t!}
=\exp\!\left(
-\frac1sW(-sw)-\frac{1}{2s}W(-sw)^2
\right).
$$

Together, these give an identity connecting Hermite polynomials evaluated along the diagonal with Lambert $W$:

$$
\begin{aligned}
&\sum_{t\geq0}
\left[
\left(\frac{s}{2}\right)^{t/2}
H_t\!\left(\frac{st+1}{\sqrt{2s}}\right)\right.\\
&\qquad\left.
-st\left(\frac{s}{2}\right)^{(t-1)/2}
H_{t-1}\!\left(\frac{st+1}{\sqrt{2s}}\right)
\right]\frac{w^t}{t!}\\
&=\exp\!\left(
-\frac1sW(-sw)-\frac{1}{2s}W(-sw)^2
\right).
\end{aligned}
$$