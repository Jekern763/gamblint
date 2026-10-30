# A Specialized Lagrange Inversion Identity for $X_s(w)=we^{sX_s(w)}$

This note proves the coefficient-transfer identity used in `explicit_formula_proof.md`, applying the standard Lagrange–Bürmann formula to $X_s(w)=we^{sX_s(w)}$.

## Conventions

All series are formal power series over $\mathbb R$. For a series $F(z)$, $[z^m]F(z)$ denotes the coefficient of $z^m$. Composition $F(X_s(w))$ is valid because $X_s(0)=0$ for all $s$. The tag (LI) denotes the standard Lagrange–Bürmann formula; the tag (L) denotes the coefficient-transfer identity derived below and cited in the main proof.

## 1. The series $X_s(w)$ and the Lambert $W$ function

Let $s\in\mathbb{R}$ be a fixed parameter. All formal power series are taken over $\mathbb{R}$, with $s$ treated as constant with respect to the indeterminates $w$ and $x$.

Let $X_s(w)$ be the unique formal power series when $s$ is constant satisfying

$$
X_s(0)=0,\qquad X_s(w)=we^{sX_s(w)}
$$

To see why it is unique, write $X_s(w)=\sum_{t\geq1}\xi_tw^t$. For $t\geq1$,

$$
[w^t]\bigl(we^{sX_s(w)}\bigr)=[w^{t-1}]e^{sX_s(w)}.
$$

Because $X$ has no constant term, the coefficient of $w^{t-1}$ in $e^{sX_s(w)}$ depends only on $\xi_1,\ldots,\xi_{t-1}$. Thus the equation determines each $\xi_t$ from the coefficients already determined. For example,the first couple of terms with $s=2$ are

$$
X_2(w)=w+2w^2+6w^3+\cdots.
$$

The defining equation also identifies $X$ with the Lambert $W$ function. Rearranging gives

$$
X_s(w)e^{-sX_s(w)}=w,
$$

so

$$
(-sX_s(w))e^{-sX(w)}=-sw.
$$

The Lambert $W$ function is defined by $W(z)e^{W(z)}=z$. Choosing the branch with $W_s(0)=0$ therefore gives

$$
\boxed{X_s(w)=-\frac1sW(-sw).}
$$

This identity may be used whenever a formula involving $X_s(w)$ is to be written in terms of $W$.

## 2. Lagrange–Bürmann inversion

The standard Lagrange–Bürmann formula states that if $X_s(w)=w\varphi(X_s(w))$, with $\varphi(0)=1$, then for any formal power series $F(x)$ and integer $t\geq1$,

$$
\boxed{[w^t]F(X_s(w))=\frac1t[x^{t-1}]F'(x)\varphi(x)^t.}\tag{LI}
$$

See Wilf, *generatingfunctionology*, 3rd ed., Section 5.1, for this formula. Here $\varphi(x)=e^{s \cdot x}$, so

$$
[w^t]\Psi(X_s(w))=\frac1t[x^{t-1}]\Psi'(x)e^{stx},\qquad t\geq1.
$$

## 3. The coefficient-transfer lemma

**Lemma (L).** For every formal power series $\Psi(x)$ and every integer $t\geq0$,

$$
\boxed{[w^t]\Psi(X_s(w))=[x^t](1-sx)\Psi(x)e^{stx}.}\tag{L}
$$

**Proof.** If $t=0$, both sides equal $\Psi(0)$, since $X(0)=0$. Now let $t\geq1$ and put $Q(x)=\Psi(x)e^{stx}$. Then

$$
Q'(x)=\Psi'(x)e^{stx}+st\Psi(x)e^{stx},
$$

so $\Psi'(x)e^{stx}=Q'(x)-stQ(x)$. By (LI),

$$
\begin{aligned}
[w^t]\Psi(X_s(w))
&=\frac1t[x^{t-1}]\Psi'(x)e^{stx}\\
&= \frac1t[x^{t-1}](Q'(x)-stQ(x))\\
&=\frac1t[x^{t-1}]Q'(x)-s[x^{t-1}]Q(x)\\
&=[x^t]Q(x)-s[x^{t-1}]Q(x)\\
&=[x^t](1-sx)Q(x)\\
&=[x^t](1-sx)\Psi(x)e^{stx}.
\end{aligned}
$$

In the third line we used $[x^{t-1}]Q'(x)=t[x^t]Q(x)$, which follows by differentiating a formal power series term by term. This proves (L). $\square$

## 4. Remarks (not used in the proof)

The equation $X=we^{sX}$ also has a combinatorial interpretation. A rooted labeled tree is a root together with a set of rooted subtrees, and assigning weight $s$ to every edge gives the exponential generating function $X_s(w)$. By Cayley's formula,

$$
[w^t]X_s(w)=\frac{(st)^{t-1}}{t!}.
$$

More generally, the specialized Lagrange formula yields

$$
t![w^t]\frac{X_s(w)^k}{k!}
=\binom{t}{k}k\,t^{t-k-1}s^{t-k},
$$
which is the count of rooted forests on $t$ labeled vertices with $k$ rooted components, with each edge weighted $s$.

The main proof uses Lemma (L), not this combinatorial interpretation. The only outside theorem required for Lemma (L) is the Lagrange–Bürmann formula (LI).

**Reference.** Herbert S. Wilf, *generatingfunctionology*, 3rd ed. (A K Peters/CRC Press, 2005), Section 5.1, “The Lagrange Inversion Formula.” [Online text](https://www.ccs.neu.edu/home/vip/teach/DiscreteMathACC/html/Honors/Herbert_Wilf_generating_functionology.pdf).
