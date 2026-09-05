# KVGuard

KVGuard studies safe lifecycle control for request-scoped KV state. It does
not claim a generic multi-state controller: weights and adapters are outside
this candidate.

## Hypothesis

If a serving runtime exposes sequence-level state save/load and capacity
pressure, a policy that accounts for restore deadline, state size, recompute
cost and request cancellation can reduce tail deadline violations relative to
always-retain, always-save and always-recompute baselines.

## Necessity gate

First establish one owned exact state round trip and observable state size,
save time, load time and cleanup under the isolated runtime. Stop if the
server/CLI does not expose these signals without system changes. This gate
cannot establish a performance benefit or policy necessity.

## Current evidence boundary and stop decision

E003R1 supplied a bounded necessity signal: with process-per-block isolation,
short state persistence cost more than fresh recomputation while long state
persistence cost less. E004 then created the smallest owned one-slot conflict
and announced-abandonment case. Its controller was worse than the strongest
fixed admitted action for short return, approximately tied with always-save
for long return, and had no nontrivial advantage over always-recompute for an
announced abandonment.

**Decision: paper-level No-Go on the current platform and artifacts.** Do not
tune the switch, add samples, or claim a controller. Reopen only with a
provenance-complete application trace, multiple simultaneously live states, a
measured capacity/eviction externality, and non-oracular lifecycle/deadline
information.

## Novelty boundary

Existing KV-cache compression, prefix caching and prompt reuse are direct
prior art. A future paper requires a validated storage lifecycle contract with
explicit restore deadlines, write/cancellation accounting, safe rollback and
comparisons under equal capacity and information budgets.
