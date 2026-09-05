# MSIO-CP-E030 ArrivalSplit source-capability audit

## Candidate and question

`ArrivalSplit` is a distinct fallback to RiskPrefetch.  At API admission (not
before arrival), it would overlap a bounded, exact-model preparation read with
the runtime's non-I/O initialization, then admit inference only after a
correctness and residency gate.  It makes no arrival prediction claim.

E030 asks whether the isolated, existing llama.cpp source exposes a separable
and instrumentable initialization boundary.  If it does not, an external
parallel read is merely a benchmark trick and this candidate is **NO-GO**
without a source modification plan.

## Scope

Perform one read-only inspection of g130's existing private llama.cpp source,
binary help, and previous ColdPath receipts.  Record only: the order between
model-file loading, context construction, server admission, and first token;
whether a public hook can launch a file-scoped read before/alongside a distinct
non-I/O phase; and available identity/readback controls.  Do not launch a
model, change source, build, install, download, alter cache state, or touch
system paths.

## Decision rule

PASS requires a documented boundary that (1) is reachable from an admitted
request, (2) starts exact-model preparation before a separately measurable
non-I/O initialization phase, (3) preserves an exact-model digest and a
one-token correctness check, and (4) can cleanly abort before inference.  An
unmodified sequential loader, undocumented internal symbol, or no independent
phase is **NO-GO**.  E030 is a capability result, never a latency result.

## Next action

Only PASS permits a new implementation packet with equal-budget sequential,
overlapped, and no-preparation arms.  NO-GO prohibits an external "race"
experiment from being represented as a systems mechanism.
