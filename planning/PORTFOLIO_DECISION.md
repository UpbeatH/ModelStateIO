# ModelStateIO single-node candidate portfolio decision

Status: 2026-09-05. This is a feasibility and evidence decision, not a publication claim.

| candidate | conclusion | authoritative evidence | CCF B disposition |
| --- | --- | --- | --- |
| LayerReadyIO | No-Go on current unmodified runtime | source audit: model/context construction loads tensors before HTTP-ready; no layer-ready serving contract | do not implement a thin scheduling wrapper |
| StatePatch | paper-level No-Go | E003--E011 establish exact artifact conversion and a narrow static attach/clean-restart contract, but no online transition, capacity conflict, isolation or equal-budget evidence | stop the static-action route; re-enter only with a new online state mechanism |
| KVGuard | paper-level No-Go | E001R1 capability, E003R1 necessity, E004 fixed-baseline failure | stop; the tested switch is not a defensible controller |
| ModelSLO | mechanism No-Go | LoadShield E000 direct-I/O/cold-launch failure; no scoped externality workload | do not add a scheduler |
| WeightResidency | corpus No-Go remains | MSIO-WR-E002 validates a public reuse trace but it lacks model/adapter identities and residency fields | blocked pending at least three traceable models plus a request sequence |

## Portfolio inference

No active ModelStateIO candidate currently meets the minimum mechanism and real-system evidence bar for an independent CCF B paper. StatePatch's exact artifact and static lifecycle gates are technically feasible, but they do not create an online state-management contribution. KVGuard is the most experimentally developed candidate, but E004 shows that its observable short/long cost switch is adequately explained by fixed actions and an announced drop. Continuing to tune either static route would be post-hoc threshold chasing.

## Permissible future re-entry

The portfolio may be re-opened only with new evidence that directly addresses the respective recorded failure: a staged-loader implementation contract (LayerReadyIO); an online adapter-state mechanism with lifecycle/capacity conflict (StatePatch); a real application lifecycle trace with multi-state capacity conflict (KVGuard); a scoped externality workload (ModelSLO); or a provenance-complete multi-model request corpus (WeightResidency). None of these is supplied by the current platform.
