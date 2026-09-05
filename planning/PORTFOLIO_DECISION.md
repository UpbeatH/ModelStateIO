# ModelStateIO single-node candidate portfolio decision

Status: 2026-09-05. This is a feasibility and evidence decision, not a publication claim.

| candidate | conclusion | authoritative evidence | CCF B disposition |
| --- | --- | --- | --- |
| CallAhead | causal mechanism No-Go | E000 qualification PASS; E001 18/18 trials, median eager p95 harm 0.12%, 95% interval [-3.01%, 5.90%], despite about 0.40 s readiness benefit | stop harm-aware pacing; no E002--E006 execution |
| LayerReadyIO | No-Go on current unmodified runtime | source audit: model/context construction loads tensors before HTTP-ready; no layer-ready serving contract | do not implement a thin scheduling wrapper |
| StatePatch | paper-level No-Go | E003--E011 establish exact artifact conversion and a narrow static attach/clean-restart contract; E200 additionally qualifies one idle-only online attach/detach lifecycle, but no real lifecycle trace, capacity conflict, isolation, task oracle or equal-budget evidence | stop the current route; re-enter only with a provenance-complete real lifecycle trace and a new state-management mechanism |
| KVGuard | paper-level No-Go | E001R1 capability, E003R1 necessity, E004 fixed-baseline failure | stop; the tested switch is not a defensible controller |
| ModelSLO | mechanism No-Go | LoadShield E000 direct-I/O/cold-launch failure; no scoped externality workload | do not add a scheduler |
| WeightResidency | corpus No-Go remains | MSIO-WR-E002 validates a public reuse trace but it lacks model/adapter identities and residency fields | blocked pending at least three traceable models plus a request sequence |

## Portfolio inference

No active ModelStateIO candidate currently meets the minimum mechanism and real-system evidence bar for an independent CCF B paper. CallAhead retained a measurable full-model readiness opportunity, but its preregistered E001 death gate did not establish a material foreground externality, so a harm-aware pacing controller is not warranted. StatePatch's exact artifact and static lifecycle gates are technically feasible, but they do not create an online state-management contribution. KVGuard's observable short/long cost switch is adequately explained by fixed actions and an announced drop. Continuing to tune these routes would be post-hoc threshold chasing.

## Permissible future re-entry

The portfolio may be re-opened only with new evidence that directly addresses the respective recorded failure: for a CallAhead successor, prior-art clearance plus a real provenance-complete three-model program trace with branch uncertainty and capacity conflict; a staged-loader implementation contract (LayerReadyIO); a provenance-complete real adapter lifecycle trace with finite capacity and a task-quality oracle (StatePatch); a real application lifecycle trace with multi-state capacity conflict (KVGuard); a scoped externality workload (ModelSLO); or a provenance-complete multi-model request corpus (WeightResidency). The current platform does not yet supply the required program trace.
