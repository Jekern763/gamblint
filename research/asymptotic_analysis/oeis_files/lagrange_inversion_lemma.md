# Lagrange Inversion for $\varphi(x)=e^{2x}$

This note is the only place where `explicit_formula_proof.md` uses an outside theorem. Section 2 states that theorem, the standard Lagrange inversion formula, without proof. Everything else in this note is proved from it. The proof only needs the series $X(w)$ of Section 1 and the Lemma (L) of Section 3.

**Conventions.** All series are formal power series over $\mathbb R$. For a series $F$, $[x^m]F$ is the coefficient of $x^m$ in $F$, and $[x^m]F=0$ when $m<0$. If $X(0)=0$, then $F(X(w))$ is defined by substituting $X(w)$ for $x$ and collecting powers of $w$.

## 1. The series $X(w)$

**Proposition 1.** There is exactly one series $X(w)$ with $X(0)=0$ and

$$
X(w)=w\,e^{2X(w)}.
$$

Its first terms are $X(w)=w+2w^2+6w^3+\cdots$.

*Proof.* Write $X=\sum_{t\geq1}\xi_tw^t$. For $t\geq1$,
$$[w^t]\bigl(we^{2X}\bigr)=[w^{t-1}]\,e^{2X}.$$
Since $X$ has no constant term, $[w^{s}]e^{2X}$ depends only on $\xi_1,\dots,\xi_s$. So the equation says that $\xi_t$ equals an expression in $\xi_1,\dots,\xi_{t-1}$. In particular $\xi_1=[w^0]e^{2X}=1$. These equations determine $\xi_1,\xi_2,\dots$ one after another, and the series they define satisfies the equation. For example, $\xi_2=[w^1]e^{2X}=2\xi_1=2$ and $\xi_3=[w^2]e^{2X}=2\xi_2+\tfrac12(2\xi_1)^2=6$. $\square$

## 2. The cited theorem

**Theorem 1 (Lagrange inversion).** Let $\varphi(x)$ be a series with $\varphi(0)\neq0$, and let $X(w)$ be a series with $X(0)=0$ and $X(w)=w\,\varphi(X(w))$. Then for all integers $t\geq1$ and $k\geq1$,

$$
[w^t]\,X(w)^k=\frac{k}{t}\,[x^{t-k}]\,\varphi(x)^t .
$$

This is the standard form of the Lagrange inversion formula; see e.g. Stanley, *Enumerative Combinatorics*, Vol. 2, §5.4. Here $X$ is the compositional inverse of $x\mapsto x/\varphi(x)$. We use it only with $\varphi(x)=e^{2x}$, for which Proposition 1 gives $X$.

## 3. The form we use

**Corollary 2.** For every series $H(x)$ and every $t\geq1$,

$$
[w^t]\,H(X(w))=\frac1t\,[x^{t-1}]\,H'(x)\,e^{2tx}.
$$

*Proof.* Both sides are linear in $H$ and depend only on the coefficients $h_0,\dots,h_t$ of $H$. On the left, this is because $X^k$ has no terms below $w^k$. On the right, it is because $H'$ contributes to $[x^{t-1}]$ only through $h_1,\dots,h_t$. So it suffices to take $H=x^k$ with $0\leq k\leq t$. For $k=0$ both sides are $0$. For $k\geq1$, Theorem 1 gives
$$[w^t]X^k=\frac kt[x^{t-k}]e^{2tx}=\frac1t[x^{t-1}]\bigl(kx^{k-1}e^{2tx}\bigr),$$
which is the claim. $\square$

**Lemma (L).** For every series $\Psi(x)$ and every $t\geq0$,

$$
\boxed{\;[w^t]\,\Psi(X(w))=[x^t]\,(1-2x)\,\Psi(x)\,e^{2tx}.\;}
$$

*Proof.* For $t=0$ both sides equal $\Psi(0)$. Let $t\geq1$, and put $g=\Psi e^{2tx}$. Then $g'=\Psi'e^{2tx}+2t\Psi e^{2tx}$, and $[x^{t-1}]g'=t\,[x^t]g$. Therefore
$$[x^{t-1}]\bigl(\Psi'e^{2tx}\bigr)=t\,[x^t]\bigl(\Psi e^{2tx}\bigr)-2t\,[x^{t-1}]\bigl(\Psi e^{2tx}\bigr).$$
Dividing by $t$ and applying Corollary 2 with $H=\Psi$,
$$[w^t]\Psi(X)=[x^t]\bigl(\Psi e^{2tx}\bigr)-2\,[x^{t-1}]\bigl(\Psi e^{2tx}\bigr).$$
Since $[x^{t-1}]F=[x^t](xF)$, the right side equals $[x^t]\,(1-2x)\Psi e^{2tx}$. $\square$

**A hand check.** Take $\Psi=x$ and $t=3$. The left side is $[w^3]X=6$ by Proposition 1. The right side is $[x^2](1-2x)e^{6x}=18-12=6$.

## 4. Remarks (not used in the proof)

**Why $X$ is a change of variable.** From $X=we^{2X}$ we get $w=Xe^{-2X}$, so $X(w)$ is the compositional inverse of $x\mapsto xe^{-2x}$. Lemma (L) translates "the coefficient of $w^t$" into "the coefficient of $x^t$" across this change of coordinates. The factor $e^{2tx}$ is $w^{-t}$ written in $x$, and the factor $(1-2x)$ is the correction for the change of coordinates.

**What Lemma (L) counts.** Read $X=we^{2X}$ combinatorially: a rooted tree is a root together with a set of subtrees, each attached by an edge, and here every edge gets weight $2$. So $X(w)$ is the exponential generating function of rooted labeled trees weighted by $2^{\#\text{edges}}$. By Cayley's formula there are $n^{n-1}$ rooted trees on $n$ labeled vertices, so $[w^n]X=\frac{n^{n-1}2^{n-1}}{n!}=\frac{(2n)^{n-1}}{n!}$, which agrees with Lemma (L) for $\Psi=x$.

More generally, take $\Psi=x^k$ with $k<t$. Lemma (L) gives
$$[w^t]X^k=[x^{t-k}](1-2x)e^{2tx}=\frac{2k\,(2t)^{t-k-1}}{(t-k)!},$$
that is,
$$t!\,[w^t]\frac{X^k}{k!}=\binom tk\,k\,t^{\,t-k-1}\cdot2^{\,t-k}.$$
The left side counts rooted forests on $t$ labeled vertices with $k$ trees and $t-k$ edges, each edge weighted $2$. The classical count of such forests is $\binom tk k\,t^{t-k-1}$. So Lemma (L) packages the generalized Cayley forest counts into one statement for an arbitrary $\Psi$.