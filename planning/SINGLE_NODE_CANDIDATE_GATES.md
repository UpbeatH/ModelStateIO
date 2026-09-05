# Single-node candidate gates

Status: 2026-09-05. This file records feasibility gates, not paper claims.

## CallAhead - causal mechanism No-Go

CallAhead asked whether non-oracular program-frontier notice could drive a
router-integrated model-state preparation action while explicitly charging
transition bytes, eviction/reload debt and foreground harm. It does not reopen
ColdPath or pool its observations into new confirmation evidence.

The first research death gate is deliberately smaller than a controller: on a
resident foreground service and a distinct low-residency background model,
compare `none`, `eager75` and `paced75` in six counterbalanced blocks. Proceed
only if eager preparation causes at least 10% reproducible foreground p95 harm,
pacing removes at least half that harm, and pacing retains at least half the
readiness benefit. Before that run, E000 must establish direct-prior-art
separation, three provenance-complete states, router action readback, safe
user-scoped state control and a bounded workload. See
`../modules/CallAhead/DESIGN.md` and `../modules/CallAhead/EXPERIMENT_PLAN.md`.

E000 passed literature/material/runtime qualification. E001 then completed
all 18 frozen trials but measured only 0.12% median eager foreground p95 harm
with 95% interval [-3.01%, 5.90%], so the affected-set and materiality clauses
failed. The roughly 0.40 s readiness benefit does not justify a harm-aware
pacing controller. Stop the current ladder before E002. A different
branch-uncertainty/eviction-debt admission question may be screened only after
direct prior-art clearance and a real three-model capacity-conflict trace.

## KVGuard — active feasibility candidate

**Observation:** the audited g130 llama.cpp source contains context state
save/load APIs, partial sequence restore, KV-cache offload controls and the
server prompt-cache/idle-slot path. This is sufficient to test a new,
state-specific lifecycle mechanism without inheriting the stopped StateTier
claim.

**E001R1 result:** after a user-local server-target build with prebuilt UI
download disabled, one slot saved and restored 9 tokens / 111,356 bytes with
exact continuation equivalence and clean teardown. E002R2 was invalid for
timing because of unseparated warm-up; E003 stopped on an incompatible
suffix-only invocation; E003R1 then passed a bounded short/long action-
reversal necessity signal. E004 completed the capacity/cancellation gate.
Its controller was worse than the strongest fixed admitted arm for short
return, approximately tied with always-save for long return, and only dropped
a deterministically announced cancellation. **KVGuard is paper-level No-Go on
the available runtime/artifacts.**

## LayerReadyIO — implementation feasibility only

**Observation:** current `llama_model_load()` does not return until
`load_tensors()` completes. The loader allocates/maps all tensors before
inference; non-mmap loading sorts staged tensors by size rather than layer
deadline. Current unmodified runtime therefore cannot demonstrate layer-ready
serving.

**Decision:** No-Go on the unmodified binary. A source-level staged-loader
fork is a distinct future candidate, contingent on a frozen implementation and
tensor-use instrumentation gate; no fixed-prefix ColdPath result is reused.

## StatePatch — static-action research No-Go

E003--E011 now provide a license/provenance-complete exact base-plus-two-
adapter pair, conversion receipts, and a static new-process attach/clean-
restart text contract. These remove the old artifact blocker but do not yield
an online attach/detach protocol, lifecycle trace, capacity conflict, tenant
isolation, task-quality oracle, or equal-budget system evidence. Do not
develop the static startup-time action into a paper; reopen only with a new
online state mechanism meeting those missing conditions.

## ModelSLO — mechanism No-Go

LoadShield E000 closed the direct-I/O-background versus cold-launch mechanism.
No current user-scoped pressure/tenant workload exposes a different affected
set. Do not introduce a scheduler until a new causal externality gate passes.

## WeightResidency — corpus No-Go

The current two-model set is insufficient for an equal-budget reuse-distance
policy and has no request trace. Reopen only with at least three provenance
complete models and a frozen request sequence.
