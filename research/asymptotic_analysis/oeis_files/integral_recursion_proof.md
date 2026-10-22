# Integral Construction

The polynomial family is defined for each fixed parameter $s>0$ by

$$
A_0(n;s)=1
$$

and, for $t\geq1$,

$$
\frac{\partial}{\partial n}A_t(n;s)=st\,A_{t-1}(n;s),
$$

with boundary condition

$$
A_t(t;s)=A_{t-1}(t;s).
$$

## From the Derivative to the Indefinite Integral

Starting with

$$
\frac{\partial}{\partial n}A_t(n;s)=st\,A_{t-1}(n;s),
$$

integrate both sides with respect to $n$:

$$
A_t(n;s)
=\int st\,A_{t-1}(n;s)\,dn+C_{t,s},
$$

where $C_{t,s}$ is a constant with respect to $n$.

Using $u$ as the integration variable,

$$
A_t(n;s)
=\int st\,A_{t-1}(u;s)\,du+C_{t,s}.
$$

Thus the derivative recurrence determines $A_t(n;s)$ up to an additive constant.

## Determining the Constant

The boundary condition gives

$$
A_t(t;s)=A_{t-1}(t;s).
$$

Evaluating the antiderivative at $n=t$ gives

$$
A_{t-1}(t;s)
=\left.\int st\,A_{t-1}(u;s)\,du\right|_{u=t}
+C_{t,s}.
$$

Therefore,

$$
C_{t,s}
=A_{t-1}(t;s)
-\left.\int st\,A_{t-1}(u;s)\,du\right|_{u=t}.
$$

Substituting this back gives the equivalent definite-integral form

$$
\boxed{
A_t(n;s)
=A_{t-1}(t;s)
+\int_t^n st\,A_{t-1}(u;s)\,du
}
$$

## Verification

Differentiating the definite-integral form gives

$$
\frac{\partial}{\partial n}
\left[
A_{t-1}(t;s)
+\int_t^n st\,A_{t-1}(u;s)\,du
\right]
=st\,A_{t-1}(n;s),
$$

and evaluating at $n=t$ gives

$$
A_t(t;s)=A_{t-1}(t;s).
$$

Therefore, the definite-integral expression satisfies both the derivative recurrence and the boundary condition.

Starting with

$$
A_0(n;s)=1,
$$

the formula recursively generates the entire polynomial family for each fixed $s>0$.
