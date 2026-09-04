# MSIO-CP-E008 runner-observability correction

Frozen: 2026-09-04. Execution authorized by the user.

## Question

Can the admission and post-trial process guard distinguish an idle state, a short-lived cleanup transient, and a persistent owned process while emitting a structured, self-identifying receipt? This is a runner qualification gate; it does not start the model and does not revisit E007.

## Frozen cases and rules

- `no-process`: an empty process snapshot must yield `PASS`.
- `transient-fixture`: a fixture PID present at t=0 and absent within a five-second settle window must yield `SETTLED`.
- `persistent-fixture`: a fixture PID present through the five-second window must yield `NO_GO`.
- Every receipt contains case, monotonic sample times, PID and full command snapshots, GPU snapshot, decision, reason, settle-window bound, and timestamp. The fixture process is always cleaned up and its final absence is recorded.
- The test is local/isolated and uses no model, GPU, cache, system setting, PFS, Lustre, g129, or remote experiment.

## Decision

PASS requires all three cases to produce the specified decision and structured fields, plus fixture cleanup. Any missing field or wrong branch is a No-Go. A PASS permits a new E009 measurement ID; it does not authorize resuming E007.

