# MSIO-CP-E029 RiskPrefetch notice-material audit

## Status and question

Frozen before execution. E024's announced-lead controller is closed and will
not be rerun. E029 asks a different feasibility question: does any currently
authorized local material provide a provenance-complete, non-oracle notice
stream for a risk-constrained model-state preparation experiment?

## Material and permitted procedure

The only candidate is the public Qwen event trace identified in
`../../../../StateTier/experiments/MSIO-WR-E002/TRACE_MATERIAL_AUDIT.md`.
E029 performs one local, read-only schema and timing audit. It must not launch
a model, contact g130, install software, create synthetic model identities, or
change caches. The audit may read only field names, record counts, event-time
range, and field cardinalities needed for the gate.

## Admissible notice contract

Each event must include, before the controller acts: a stable event ID, a
notice timestamp distinct from actual arrival, model or adapter identity and
version/digest, state-byte estimate, declared deadline/launch window, and
source provenance. The prospective outcome record must additionally expose
actual arrival, preparation completion, state residency, foreground latency,
and a user-scoped contention/displacement measure.

## Decision rule

PASS requires all contract fields, at least two observed state identities, and
at least 100 notices with a nonzero observable pre-arrival interval in a
time-held-out portion. A missing required field, only one state identity, or
inability to distinguish notice from actual arrival is **NO-GO**. No
imputation, post-hoc state assignment, or synthetic scheduling is allowed.

## Consequences

On PASS, freeze a new execution protocol with equal-information/equal-action/
equal-runtime fixed and abstaining baselines. On NO-GO, record the minimum
external material needed; do not start a GPU or performance experiment.
