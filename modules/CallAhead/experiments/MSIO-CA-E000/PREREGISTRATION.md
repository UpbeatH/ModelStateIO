# MSIO-CA-E000 preregistration

Status: frozen before remote inspection. Date: 2026-09-05.

## Question

Does the current CallAhead literature, runtime and material set satisfy every
precondition needed to freeze the first causal interference experiment without
inventing model identities, notices, actions or cold-state controls?

## Evidence inputs

1. Primary papers and official artifact records for the closest model loading,
   advisory/program-aware serving, adapter, KV-cache and partial restoration
   systems listed in `../../DESIGN.md`.
2. Existing compact ColdPath E021--E031 evidence. These results are historical
   inputs only and are not CallAhead confirmation samples.
3. Read-only inspection of g130 user-private ModelStateIO files, runtime source,
   GPU/process state and available user-scoped tools.

## Five pass requirements

1. A source-level prior-art matrix leaves a mechanism gap beyond changing only
   the state type or platform.
2. At least three provenance-complete full-model weight states exist; at least
   two have materially different footprints. Adapters and duplicate copies do
   not count for the first weight-warming claim.
3. A documented router path exposes model identity, queue/admission, load and
   eviction outcomes with effective-setting readback.
4. A user-scoped state-control method can operate only on experiment-owned
   immutable model files and can verify the resulting residency. Global cache
   clearing is forbidden.
5. A bounded foreground request driver and preparation/interference harness can
   enforce memory/I/O limits and record the E001 metrics.

## Decision rule

- `PASS` only if all five requirements are established.
- `MATERIAL_BLOCKED` if the novelty gap remains viable but one or more
  acquisition or implementation prerequisites are missing. This is not a
  scientific No-Go; the missing artifacts must be supplied under a new,
  provenance-complete material subgate before E000 is decided.
- `NO_GO` if direct prior art already implements the complete proposed
  mechanism, the runtime lacks an inspectable action boundary, or safe
  user-scoped state control cannot be implemented.

No GPU/model launch, download, installation, source modification, cache action
or performance comparison is allowed in the E000 inspection.

## Claim ceiling

E000 can establish only literature/material/runtime qualification. It cannot
establish an affected set, performance benefit, controller advantage or CCF B
readiness.
