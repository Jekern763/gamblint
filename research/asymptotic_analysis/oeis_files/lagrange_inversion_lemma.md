# A Specialized Lagrange Inversion Identity for $X(w)=we^{2X(w)}$

This note proves the coefficient-transfer identity used in `explicit_formula_proof_revised.md`, applying the standard Lagrange–Bürmann formula to $X(w)=we^{2X(w)}$.

## Conventions

All series are formal power series over $\mathbb R$. For a series $F(z)$, $[z^m]F(z)$ denotes the coefficient of $z^m$. Composition $F(X(w))$ is valid because $X(0)=0$. The tag (LI) denotes the standard Lagrange–Bürmann formula; the tag (L) denotes the coefficient-transfer identity derived below and cited in the main proof.

## 1. The series $X(w)$ and the Lambert $W$ function

Let $X(w)$ be the unique formal power series satisfying

$$
X(0)=0,\qquad X(w)=we^{2X(w)}.
$$

To see why it is unique, write $X(w)=\sum_{t\geq1}\xi_tw^t$. For $t\geq1$,

$$
[w^t]\bigl(we^{2X(w)}\bigr)=[w^{t-1}]e^{2X(w)}.
$$

Because $X$ has no constant term, the coefficient of $w^{t-1}$ in $e^{2X(w)}$ depends only on $\xi_1,\ldots,\xi_{t-1}$. Thus the equation determines each $\xi_t$ from the coefficients already determined. The first terms are

$$
X(w)=w+2w^2+6w^3+\cdots.
$$

The defining equation also identifies $X$ with the Lambert $W$ function. Rearranging gives

$$
X(w)e^{-2X(w)}=w,
$$

so

$$
(-2X(w))e^{-2X(w)}=-2w.
$$

The Lambert $W$ function is defined by $W(z)e^{W(z)}=z$. Choosing the branch with $W(0)=0$ therefore gives

$$
\boxed{X(w)=-\frac12W(-2w).}
$$

This identity may be used whenever a formula involving $X(w)$ is to be written in terms of $W$.

## 2. Lagrange–Bürmann inversion

The standard Lagrange–Bürmann formula states that if $X(w)=w\varphi(X(w))$, with $\varphi(0)=1$, then for any formal power series $F(x)$ and integer $t\geq1$,

$$
\boxed{[w^t]F(X(w))=\frac1t[x^{t-1}]F'(x)\varphi(x)^t.}\tag{LI}
$$

See Wilf, *generatingfunctionology*, 3rd ed., Section 5.1, for this formula. Here $\varphi(x)=e^{2x}$, so

$$
[w^t]\Psi(X(w))=\frac1t[x^{t-1}]\Psi'(x)e^{2tx},\qquad t\geq1.
$$

## 3. The coefficient-transfer lemma

**Lemma (L).** For every formal power series $\Psi(x)$ and every integer $t\geq0$,

$$
\boxed{[w^t]\Psi(X(w))=[x^t](1-2x)\Psi(x)e^{2tx}.}\tag{L}
$$

**Proof.** If $t=0$, both sides equal $\Psi(0)$, since $X(0)=0$. Now let $t\geq1$ and put $Q(x)=\Psi(x)e^{2tx}$. Then

$$
Q'(x)=\Psi'(x)e^{2tx}+2t\Psi(x)e^{2tx},
$$

so $\Psi'(x)e^{2tx}=Q'(x)-2tF(x)$. By (LI),

$$
\begin{aligned}
[w^t]\Psi(X(w))
&=\frac1t[x^{t-1}]\Psi'(x)e^{2tx}\\
&= \frac1t[x^{t-1}](Q'(x)-2tQ(x))\\
&=\frac1t[x^{t-1}]Q'(x)-2[x^{t-1}]Q(x)\\
&=[x^t]Q(x)-2[x^{t-1}]q(x)\\
&=[x^t](1-2x)Q(x)\\
&=[x^t](1-2x)\Psi(x)e^{2tx}.
\end{aligned}
$$

In the third line we used $[x^{t-1}]Q'(x)=t[x^t]Q(x)$, which follows by differentiating a formal power series term by term. This proves (L). $\square$

## 4. Remarks (not used in the proof)

The equation $X=we^{2X}$ also has a combinatorial interpretation. A rooted labeled tree is a root together with a set of rooted subtrees, and assigning weight $2$ to every edge gives the exponential generating function $X(w)$. By Cayley's formula,

$$
[w^t]X(w)=\frac{(2t)^{t-1}}{t!}.
$$

More generally, the specialized Lagrange formula yields

$$
t![w^t]\frac{X(w)^k}{k!}
=\binom{t}{k}k\,t^{t-k-1}2^{t-k},
$$
which is the count of rooted forests on $t$ labeled vertices with $k$ rooted components, with each edge weighted $2$.

The main proof uses Lemma (L), not this combinatorial interpretation. The only outside theorem required for Lemma (L) is the Lagrange–Bürmann formula (LI).

**Reference.** Herbert S. Wilf, *generatingfunctionology*, 3rd ed. (A K Peters/CRC Press, 2005), Section 5.1, “The Lagrange Inversion Formula.” [Online text](https://www.ccs.neu.edu/home/vip/teach/DiscreteMathACC/html/Honors/Herbert_Wilf_generating_functionology.pdf).
