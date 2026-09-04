# MSIO-CP-E010 analyzer provenance gate

Frozen: 2026-09-04. No model or GPU execution.

## Question

Can the compact analyzer reject mixed or mislabeled trial receipts and derive the experiment identity from an explicit argument, while preserving complete counts and the fixed robust-CV decision rule?

## Frozen tests

- A valid 18-receipt E009R1 fixture must produce `experiment=MSIO-CP-E009R1`, `valid_trials=18`, and the expected per-mode counts.
- A fixture with one receipt carrying an E007 trial ID must fail with an identity-mismatch error.
- A fixture with one missing receipt must fail with an incomplete-count error.
- No threshold, receipt, or historical E009R1 artifact may be changed. PASS requires all three tests and deterministic output.

