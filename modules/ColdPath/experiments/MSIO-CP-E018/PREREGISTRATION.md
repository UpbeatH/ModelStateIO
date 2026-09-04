# MSIO-CP-E018 residency shaping latency gate

## Question

After verified per-file eviction, does a completed sequential prefetch reduce request-visible time-to-first-exact-OK relative to cold launch, and is the gain large enough to justify studying deadline-aware preparation?

## Frozen design

- Six counterbalanced two-arm blocks: cold launch and full prefetch followed immediately by launch; 12 valid trials total.
- Every trial begins with exact model/hash/process checks, file-scoped `DONTNEED`, two-second settle, and `mincore` readback requiring ≤20% residency.
- Prefetch arm records preparation duration and requires ≥80% residency before model launch. Cold arm launches without preparation.
- Identical llama.cpp binary, prompt, generation settings, GPU placement, correctness, timeout, output cap and cleanup guards.
- Primary: request-to-first-exact-OK. Secondary: preparation time, preparation-plus-request latency, correctness, resident fraction, GPU/process residue.
- Equal model/action availability and six observations per arm; block order alternates. No sample addition or exclusion after outcomes.

## Decision

Proceed only if the paired median request-latency reduction is at least 10%, its block-bootstrap 95% lower bound is above zero, all trials are correct, and preparation-plus-request latency is reported rather than hidden. Otherwise NO-GO for full-file predictive prefetch as the next ColdPath mechanism.
