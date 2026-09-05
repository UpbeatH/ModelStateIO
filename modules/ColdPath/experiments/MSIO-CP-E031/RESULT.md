# MSIO-CP-E031 QueueAwareWarm material and router audit result

## Established observations

The allowed g130 private `incoming/` directory contains two distinct GGUF
files: Qwen2.5 0.5B Q4_K_M (491,400,032 bytes; prior verified digest
`74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`) and
Qwen2.5 7B Q4_K_M (4,683,073,952 bytes; prior E023 identity digest
`2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730`). The
GPU was idle (0 MiB allocated) at the audit. The 7B file's local acquisition
receipt remains incomplete, as already recorded by E023.

Read-only source inspection establishes a public router configuration boundary:
`--models-dir`, `--models-preset`, and `--models-max`. The router loads local
presets, queues a request when the model limit is reached, and removes the LRU
model before loading another. This is an inspectable model-ID-to-file binding
mechanism, rather than an undocumented loader symbol.

## Decision

**PASS for router capability only; NO-GO for a paper-evidence performance
experiment on current material.** The runtime could support a future bounded
two-model technical experiment. It cannot currently support the intended
QueueAwareWarm scientific claim: there is no provenance-complete admission
trace, no user-scoped contention/displacement measure, and the 7B model lacks
a complete local acquisition record. Replaying a hand-written alternating
sequence would be a synthetic demonstration, not a workload result.

No server/model was launched; no configuration, source, cache, system setting,
or remote file was changed.

## Re-entry requirements

Before any router performance protocol: supply a provenance-complete admission
trace with model IDs and arrivals, complete source/license receipts for every
model state, and a user-scoped foreground/interference measurement.  Then
freeze equal-information/equal-action/equal-runtime baselines against the
router's documented LRU policy.
