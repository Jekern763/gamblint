# Mathematical Analysis

This section develops the mathematical model of the game: the payout and optimal-guess functions, the invariant sum, state transitions, peek probabilities, and expected value.

## Foundations

- [`foundations/definitions.md`](foundations/definitions.md) — notation and game definitions.
- [`foundations/reference.md`](foundations/reference.md) — notation summary.
- [`foundations/results.md`](foundations/results.md) — current collection of formulas and links to their derivations.

## Proofs

The proofs are numbered in their original order. They are preserved as close to the original drafts as possible; edits are limited to clear mathematical, indexing, notation, and cross-reference errors.

1. [`p1_optimal_guess_function.md`](proofs/p1_optimal_guess_function.md) — optimal guess and its properties.
2. [`p2_maximum_payout_function.md`](proofs/p2_maximum_payout_function.md.md) — maximum payout and its properties.
3. [`p3_invariant_sum.md`](proofs/p3_invariant_sum.md.md) — invariant sum.
4. [`p4_game_state_transition.md`](proofs/p4_game_state_transition.md.md) — state transitions.
5. [`p5_peek_likelihood_given_state.md`](proofs/p5_peek_likelihood_given_state.md) — next-peek probability given the state.
6. [`p6_state_likelihood.md`](proofs/p6_state_likelihood.md) — probability of an ordered state.
7. [`p7_history_state_probability.md`](proofs/p7_history_state_probability.md) — joint history/state probability and posterior state probability.
8. [`p8_next_peek_likelihood.md`](proofs/p8_next_peek_likelihood.md) — next-peek probability given the observed history.
9. [`p9_expected_value.md`](proofs/p9_expected_value.md.md) — expected value and optimal legal guess.

## Notes and archive

The original conjecture document is preserved in [`archive/old_conjectures.md`](archive/old_conjectures.md). It is intentionally marked as historical and has not been rewritten, including conjectures that may have been incorrect or superseded. [`archive/early_research_index.md`](archive/early_research_index.md) preserves the earlier research index.

## Figures and code

The existing figures are kept in `figures/`. The figure-generation source code was not searched for or reconstructed during this migration; `code/README.md` records that limitation.

## Important state-model distinction

The proofs below use **ordered states**, in which the first and second dice are distinguished. The game-analysis implementation can canonicalize states by sorting the two remaining-face sets. When comparing proof formulas with that implementation, account for the multiplicity of ordered states and transitions that are merged into a canonical state.
