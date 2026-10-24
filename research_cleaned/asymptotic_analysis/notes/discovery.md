# Discovery of the Polynomial Triangle

This array arose from an investigation of vector sums of permutations, originally motivated by A175176.

I began by considering partial vector-sum constructions of two permutations of $1,2,\ldots,n$. For fixed values of the partial construction parameter $t$, I computed the resulting counts and attempted to fit polynomials in $n$ to the data. This produced a triangular collection of polynomial rows.

While examining these polynomials, I noticed a pattern resembling an Appell sequence: differentiating the polynomial in row $t$ gave $2t$ times the polynomial in row $t-1$,

The original combinatorial construction also suggested a boundary identity,

$$\
T(t,t)=T(t,t-1),\
$$

which I proved directly from the vector-sum construction. Together, these observations led to the recursive integral construction described in the accompanying proof.

However, the original vector-sum interpretation did not continue to account for the resulting values. In particular, the first discrepancy appeared at $n=5$. At the same time, I found that the resulting values agreed with A362968, the sequence counting integral points in twice the permutohedron.

This led to a change in perspective: rather than treating the polynomial array as a continuation of the original vector-sum counting problem, I defined the array directly by the polynomial recurrence, initial condition, and boundary condition.

The diagonal of the resulting array,

$$\
T(n,n),\
$$

agrees with A362968 for many computed terms. This is currently an empirical observation rather than a proof of the identity.

The array also contains many non-diagonal rows. These rows arise naturally from the same recursion, but no additional combinatorial interpretation or other significant properties of the internal rows are currently known.
