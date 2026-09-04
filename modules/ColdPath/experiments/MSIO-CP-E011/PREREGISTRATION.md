# MSIO-CP-E011 state-control decision gate

Frozen: 2026-09-04. No model or remote execution.

## Question

Which cache-state labels are scientifically admissible without global cache eviction or system writes? The gate must prevent an unverified “cold” label from entering a later comparison.

## Frozen policy

- `natural_warm` is admissible when the process starts normally and no cache-control action is taken; report it explicitly as warm-only.
- `explicit_cold` is admissible only with a prospective, auditable, non-global method and direct evidence. `drop_caches`, sysctl writes, remounts, raw-device reads, and undocumented tricks are forbidden here.
- `unknown` must abstain from comparative analysis.
- Any forbidden or missing evidence yields `NO_GO`, not a relabeled warm sample. Tests use deterministic fixtures only.

## Decision

PASS means the classifier accepts warm, rejects forbidden cold, and abstains on unknown with structured reasons. This does not authorize a new performance run; it defines the state policy for a future E012/E013 gate.

