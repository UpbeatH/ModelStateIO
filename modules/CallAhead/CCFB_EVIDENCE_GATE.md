# CallAhead CCF B evidence gate

Status: **target standard, not achieved**. Date: 2026-09-05.

This checklist defines the minimum evidence package for calling CallAhead a
CCF-B-ready systems contribution. Passing one pilot or achieving a large best
case is insufficient.

## 1. Novelty and problem necessity

- [ ] Primary-paper comparison against the closest loading, program-aware,
      KV/advisory, adapter and partial-restoration systems is complete.
- [ ] At least one important workload regime is demonstrated in which native
      LRU, no preparation, eager preparation and a deadline/slack rule make
      systematically worse decisions under equal information.
- [ ] The gap depends on the interaction of program notice, transition debt and
      foreground harm; changing only the state type or hardware is not the gap.
- [ ] A deterministic policy leaves measurable held-out regret before any
      learned controller is introduced.

## 2. System contribution

- [ ] The mechanism executes in a real router/loading path with action readback;
      it is not an external file-read wrapper.
- [ ] State identity/version/digest, capacity, residency and transition bytes
      are explicit and auditable.
- [ ] Abstention, timeout, cancellation accounting, rollback and native-router
      fallback are implemented.
- [ ] Foreground harm and evicted-state reload debt influence a real action;
      they are not dashboard-only metrics.

## 3. Experimental strength

- [ ] At least three provenance-complete model states and three workload
      structures are evaluated.
- [ ] At least two model-size groups, two capacity/pressure groups and one
      independent hardware/storage or runtime context are included.
- [ ] A real or source-auditable program/workflow trace supplies non-oracle
      notices; synthetic replay is supplemental only.
- [ ] Strong baselines share information, action and runtime/controller budgets.
- [ ] Order, seeds, block unit, repetitions, exclusions and primary endpoint are
      frozen before confirmation.
- [ ] p50/p95/p99, goodput/SLO attainment, transition time/bytes, wasted work,
      CPU/DRAM/HBM/device cost, eviction debt and bystander harm are reported.
- [ ] Correctness and state-version isolation pass for every admitted trial.
- [ ] Negative regimes, abstentions, failures and sensitivity results are
      included rather than filtered.

## 4. Quantitative paper-level thresholds

On a prospectively declared primary held-out workload, CallAhead must satisfy
all of the following:

1. at least 15% improvement in p95 readiness/TTFT over the strongest deployable
   non-oracle baseline, or at least 30% fewer SLO violations;
2. a prospectively defined uncertainty interval for the primary paired effect
   excludes zero;
3. foreground p99 degradation is no greater than 5%;
4. aggregate useful throughput is at least 95% of the best safe baseline;
5. the independent context retains at least half of the primary effect and at
   least a 10% improvement over its own strongest safe baseline;
6. controller CPU/wall-clock overhead is no greater than 2% unless a larger
   overhead is fully repaid in the declared end-to-end primary metric;
7. zero silent action, identity, correctness or cleanup failure.

These thresholds are targets to freeze before the relevant data are opened.
They may be tightened prospectively. They may not be weakened after observing
results.

## 5. Claim ladder

| Highest passed gate | Permitted statement |
| --- | --- |
| E000 | implementation and material are feasible |
| E001 | a bounded single-host interference/control opportunity exists |
| E002--E003 | a non-oracle workload and router-integrated mechanism exist |
| E004 | held-out single-context research signal exists |
| E005 | the mechanism transfers to one independent context |
| E006 | paper-level evidence package is complete |

No earlier level may be described as a CCF-B result.

## 6. Immediate stop conditions

- E001 finds no reproducible affected set or a simple fixed cap matches pacing;
- E002 cannot obtain non-oracle multi-state notice material;
- the best action can be selected from model size alone;
- native LRU, eager preparation or a simple slack rule matches CallAhead;
- benefit disappears after charging preparation, eviction and interference;
- improvement requires confirmation-set retuning;
- correctness, version isolation or cleanup is not fail-closed;
- only one model, workload, host or favorable subgroup supports the claim.

## 7. Artifact and submission readiness

- [ ] Exact code revision, environment, model provenance, licenses and hashes
      are recorded.
- [ ] Raw evidence remains outside Git with immutable manifests and checksums;
      compact derived evidence and analysis are versioned.
- [ ] One-command validators reproduce tables and figures from compact data.
- [ ] Limitations explicitly exclude cluster-scale autoscaling, untested state
      classes and production generalization.
- [ ] CCF venue classification is checked against the designated March 2026
      local CCF directory only when the evidence package determines the venue.

## Decision rule

CallAhead becomes **paper-level GO** only after every required item in Sections
1--4 passes and the artifact in Section 7 is reviewable. Otherwise it remains a
feasibility candidate or becomes No-Go with the exact failed gate preserved.
