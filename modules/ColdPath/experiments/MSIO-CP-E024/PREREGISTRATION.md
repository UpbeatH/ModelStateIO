# MSIO-CP-E024 announced-lead error and abstention gate

Status: frozen before execution. Date: 2026-09-05.

## Question

Can a conservative 75%-prefix preparation rule use only an announced request
lead to abstain when that lead is insufficient, while making its decision and
the resulting completed/concurrent state auditable under forecast error?

## Mechanism and boundary

The action is the already-qualified user-scoped sequential read of the first
75% of the 0.5B GGUF, after file-scoped `POSIX_FADV_DONTNEED`.  The policy sees
only a frozen announcement at preparation trigger time; the actual arrival
delay is withheld from it.  `fixed75` always triggers. `guarded75` triggers
only when the announced lead is at least 1.0 s, a conservative threshold above
the earlier approximately 0.8 s 0.5B completion observation. `none` does not
trigger. This is a schedulable-policy qualification, not a learned controller
or a total-work result.

## Frozen schedule and budget

Nine counterbalanced blocks, each containing `none`, `fixed75`, and
`guarded75` once (27 trials), use these three announced/actual lead cases three
times each:

| Case | Announced lead | Actual lead | Expected guarded state |
| --- | ---: | ---: | --- |
| insufficient-known | 0.6 s | 0.6 s | abstain |
| early-arrival error | 1.1 s | 0.6 s | trigger, normally concurrent |
| accurate-sufficient | 1.1 s | 1.1 s | trigger, completed |

Within each block, all arms have the same announced and actual lead; only the
action differs. Arm orders are frozen in the runner. Every trial uses the
same hash-pinned binary, model, foreground correctness command, 75% byte
action, model-file cold-state protocol, timeout, GPU placement and cleanup
checks as E022R1. No global cache clear, installation, model download, sample
extension, retry, or post-hoc threshold change is permitted.

## Measurements

Each raw receipt records announced/actual lead, signed error, policy decision,
action bytes, worker state and resident fraction at arrival, worker duration,
request-visible arrival-to-OK time, full trigger-to-OK time, exact `OK`
correctness, exit code, and final process/GPU cleanup. Preparation time and
bytes are never treated as free.

## Decision

Technical policy qualification passes only if all 27 trials are correct and
clean; all `guarded75` insufficient-known trials abstain; all guarded
accurate-sufficient trials are completed with at least 70% arrival residency;
and all guarded early-arrival-error trials expose their active/completed state
at arrival. The runner also reports paired request-visible contrasts by case,
but only the three accurate-sufficient pairs may be inspected as a directional
replication; no statistical generalization is claimed from this gate. Any
other outcome is a No-Go for the proposed conservative announced-lead policy.
