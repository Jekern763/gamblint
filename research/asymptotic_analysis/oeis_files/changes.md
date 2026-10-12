# Changes to Proofs

Here are ideas to make proofs more elegant, more correct, or more fool proof

## `explicit_formula_proof.md`

1. Change renaming conventions at the beginning
   * Currently $G(0,x) := C(x)$ then $\frac{C(x)}{1-2x} := \Psi(x)$
   * Maybe just keep it as $G(0,x)$ and only introduce $\Psi$ when it becomes necessary
   * Then the $1-2x$ is also no longer mysterious as to why we chose it
   * Don't forget to change it in `lagrange_inversion_lemma` as well
