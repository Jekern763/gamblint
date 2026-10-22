# **A175176 Prefix Sum Hierarchy & Appell Structure**

### **1\. The Core Differential Recurrence**

For two permutations $\\sigma, \\tau \\in S\_n$, let $A\_t(n)$ denote the count of distinct prefix sums of length $t$. Across all verified dimensions, the continuous column polynomials satisfy the differential relation:

$$\\frac{d}{dn} A\_t(n) \= 2t \\cdot A\_{t-1}(n)$$  
Normalized by $Q\_t(n) \= \\frac{A\_t(n)}{2^t}$, this maps directly to a canonical Appell sequence where:

$$Q'\_t(n) \= t \\cdot Q\_{t-1}(n) \\text{\[cite: 3\]}$$  
Successive integration generates each subsequent column up to a single scalar integration constant $C\_t$.

### **2\. Eliminating Empirical Seed Points via the Boundary Identity**

Because the global trace is strictly conserved ($\\sum\_{i=1}^n (\\sigma(i) \+ \\tau(i)) \= n(n+1)$), knowledge of the first $n-1$ coordinates uniquely determines the $n$-th coordinate. This establishes the universal identity:

$$A\_{n-1}(n) \\equiv A\_n(n) \\quad \\forall \\, n \\ge 2 \\text{\[cite: 3, 4\]}$$  
Evaluating this identity along the apex $n \= t$ completely fixes the integration constant without requiring any experimental measurements or external seed values:

$$A\_t(t) \= A\_{t-1}(t) \\text{\[cite: 3, 4\]}$$

#### **Demonstration for $t \= 5$:**

* **Indefinite integral:** $A\_5(n) \= 32n^5 \- 80n^4 \- 400n^3 \+ 40n^2 \+ 410n \+ C\_5$  
* **Base polynomial evaluation at $n \= 5$:** $A\_5(5) \= 3050 \+ C\_5$  
* **Boundary condition:** $A\_5(5) \= A\_4(5) \= 3081$\[cite: 2, 4\]  
* **Immediate resolution:** $3050 \+ C\_5 \= 3081 \\implies \\mathbf{C\_5 \= 31}$ (zero empirical fitting needed)

### **3\. Nature of the Subdiagonal Anomaly at $A\_5(6)$**

At $(t=5, n=6)$, the polynomial predicts $62,683$, whereas the true count is $62,663$ ($\\Delta \= \-20$)\[cite: 2, 3\]. This deviation marks the onset of the higher-dimensional boundary band where $n \\le t \+ 1$:

* **Fallback Guarantee:** Since $(t=5, n=6)$ lies on the subdiagonal $t \= n \- 1$, the true count does not require polynomial extrapolation; it is identically equal to the full vector count $A\_6(6) \= 62,663$\[cite: 2, 3\].  
* **Boundary Duality:** The polynomial at step $t \= 6$ yields $\\text{Poly}\_6(6) \= 62,643$ ($+20$ error). The ground truth is the exact arithmetic mean:  
  $$\\frac{\\text{Poly}\_5(6) \+ \\text{Poly}\_6(6)}{2} \= \\frac{62,683 \+ 62,643}{2} \= 62,663 \\text{\[cite: 2, 3\]}$$

### **4\. Summary Table of Column Polynomials**

| t | Closed-Form Polynomial At​(n) | Constant Source |
| :---- | :---- | :---- |
| **1** | $2n \- 1$ | Base case |
| **2** | $4n^2 \- 4n \- 5$ | $A\_2(2) \= A\_1(2) \= 3$ |
| **3** | $8n^3 \- 12n^2 \- 30n \+ 1$ | $A\_3(3) \= A\_2(3) \= 19$ |
| **4** | $16n^4 \- 32n^3 \- 120n^2 \+ 8n \+ 41$ | $A\_4(4) \= A\_3(4) \= 201$ |
| **5** | $32n^5 \- 80n^4 \- 400n^3 \+ 40n^2 \+ 410n \+ 31$ | $A\_5(5) \= A\_4(5) \= 3081$\[cite: 2, 4\] |

