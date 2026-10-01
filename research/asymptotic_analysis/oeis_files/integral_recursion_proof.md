# Integral construction

The polynomial family is defined by

$$
T(n,0)=1
$$

and, for $t \ge 1$,

$$
\frac{\partial}{\partial n}T(n,t)=2t\,T(n,t-1),
$$

with boundary condition

$$
T(t,t)=T(t,t-1).
$$

## From the derivative to the indefinite integral

Starting with

$$
\frac{\partial}{\partial n}T(n,t)=2t\,T(n,t-1),
$$

integrate both sides with respect to $n$:

$$
T(n,t)
=
\int 2t\,T(n,t-1)\,dn+C_t,
$$

where $C_t$ is a constant with respect to $n$.

Using $u$ as the integration variable,

$$
T(n,t)
=
\int 2t\,T(u,t-1)\,du+C_t.
$$

Thus the derivative recurrence determines $T(n,t)$ up to an additive constant.

## Determining the constant

The boundary condition gives

$$
T(t,t)=T(t,t-1).
$$

Substituting $n=t$ into the indefinite integral gives

$$
T(t,t)
=
\int 2t\,T(u,t-1)\,du+C_t.
$$

Therefore,

$$
C_t
=
T(t,t-1)
-
\int 2t\,T(u,t-1)\,du,
$$

where the indefinite integral is evaluated at $u=t$.

Substituting this back gives the equivalent definite-integral form

$$
\boxed{
T(n,t)
=
T(t,t-1)
+
\int_t^n 2t\,T(u,t-1)\,du
}
$$

## Verification

Differentiating the definite-integral form gives

$$
\frac{\partial}{\partial n}
\left[
T(t,t-1)
+
\int_t^n 2t\,T(u,t-1)\,du
\right]
=
2t\,T(n,t-1),
$$

and evaluating at $n=t$ gives

$$
T(t,t)=T(t,t-1).
$$

Therefore the definite-integral expression satisfies both the derivative recurrence and the boundary condition.

Starting with

$$
T(n,0)=1,
$$

the formula recursively generates the entire tr
