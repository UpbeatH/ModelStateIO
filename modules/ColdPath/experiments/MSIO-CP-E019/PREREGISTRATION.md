# MSIO-CP-E019 fractional-residency dose-response gate

## Question

Does increasing the fraction of a cold GGUF prefetched before launch produce a stable, measurable reduction in request-visible readiness latency, and can a partial action recover most of full-prefetch benefit with fewer bytes?

## Frozen design

- Fractions: 0%, 25%, 50%, 75%, and 100% of model bytes from file offset zero.
- Six counterbalanced five-arm blocks; 30 valid trials total. Each block starts every arm from file-scoped `DONTNEED`, a two-second settle, and `mincore` readback ≤20%.
- The prefetched fraction, preparation duration, resulting resident fraction, time-to-first-exact-OK, correctness, and cleanup state are recorded.
- Exact E018 model, binary, measurement contract, prompt, `mmap` launch mode, GPU placement, timeout, and output cap are retained.
- Raw evidence remains outside Git. No global cache action, installation, kernel write, or PFS/Lustre action is allowed.

## Decision

Mechanism GO requires: at least five of six within-block Spearman correlations between prefetch fraction and request latency are negative; their median is ≤−0.60; and at least one partial arm (25/50/75%) recovers ≥70% of the median full-prefetch latency benefit while reading no more than 75% of model bytes. All 30 trials must be correct and residue-free. Otherwise NO-GO for fractional residency as the controller action space.

This gate tests one model and host only; PASS does not establish cross-model generality or a paper-level controller.
