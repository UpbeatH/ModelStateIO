# MSIO-CP-E023 held-out 7B completed-preparation confirmation

Status: frozen; no result yet. Date: 2026-09-04.

## Question

Does the completed 75%-prefix preparation mechanism that passed on the 0.5B
model retain a material request-visible benefit for a hash-distinct 7B GGUF on
the same g130 runtime and storage device?

## Frozen protocol

- Held-out model: isolated 7B Q4_K_M GGUF, SHA-256
  `2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730`.
- A non-inference preflight measured 2.512 s for 75% prefix preparation from
  file-scoped cold state. The lead budget is frozen to 3.500 s; preparation
  must complete and `mincore` must show at least 70% residency before launch.
- Arms: no preparation and completed 75%-prefix preparation. Six AB/BA
  counterbalanced paired blocks (12 trials). Every trial begins with owned-file
  `POSIX_FADV_DONTNEED`, two-second settling, and no more than 20% residency.
- The foreground command, exact-OK correctness, timeout, GPU placement and
  cleanup identities are hash-pinned to E021. No global cache action,
  installation, retry or post-hoc sample expansion is allowed.

## Decision

`lead3500` qualifies only if all trials are correct and clean, at least five
of six paired request-latency contrasts are negative, the paired median
reduction is at least 10%, and a fixed-seed 10,000-resample block-bootstrap
95% interval for `lead3500 - none` excludes zero. Otherwise this cross-model
confirmation is No-Go. Either outcome is not a controller, total-work or
cross-device result.
