# MSIO-CP-E020 equal-byte segment-placement gate

## Question

At a fixed 50% model-byte read budget, does segment placement change request-visible readiness latency enough to justify a GGUF content-aware prefetch mechanism?

## Frozen design

- Arms: no prefetch control; first 50% (`prefix`); last 50% (`suffix`); alternating 8 MiB extents (`striped`).
- The three active arms read exactly the same number of model bytes. Six counterbalanced four-arm blocks yield 24 valid trials.
- Each arm begins with file-scoped `DONTNEED`, two-second settle, and `mincore` cold readback ≤20%. Record requested bytes, resulting residency, preparation time, time-to-first-exact-OK, correctness, and cleanup.
- Retain the exact E019 model, binary, measurement contract, prompt, mmap launch, timeout, and output cap.
- Planned placement contrasts are `suffix-prefix` and `striped-prefix`. To limit multiplicity, content-placement GO requires an absolute paired-median difference ≥5% of prefix latency and a conservative 99% block-bootstrap interval excluding zero for at least one planned contrast.
- All 24 trials must be correct and residue-free. No post-hoc arm selection, sample addition, global cache action, kernel write, or PFS/Lustre action.

## Decision

PASS permits development of a GGUF tensor/access-aware segment selector. Otherwise content placement is NO-GO and ColdPath retains only fraction/timing control. This one-model gate cannot support a paper-level generalization claim.
