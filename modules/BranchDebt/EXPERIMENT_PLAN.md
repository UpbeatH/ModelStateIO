# BranchDebt experiment plan

## E300 - prospective workload and physical-capacity qualification

### Phase A: source and identity

- Pin an openly licensed executable workflow/task source and preserve its
  upstream license constraints.
- Bind at least three official model artifacts by repository revision, file,
  size and SHA-256 before execution.
- Define the program node, candidate set and notice emission rule in code
  before opening outcomes.

### Phase B: real execution trace

- Execute development tasks rather than replaying historical arrival rows.
- Each event records event/task/node ID, notice time, candidate states,
  dependency edge, branch-resolution time, selected branch, actual
  arrival/completion, correctness, transition bytes and state readback.
- Qualification requires at least 100 nonzero-notice events, a frozen
  time/task-held-out split, at least 10% wrong-branch or abstention opportunity,
  and no forbidden future field at decision time.
- The concrete MBPP workflow uses a 7B primary answer, emits a two-candidate
  14B/32B repair frontier before tests, and routes assertion-only failures to
  14B versus syntax/import/timeout/resource failures to 32B. Passing tasks are
  the natural no-call branch. Candidate code runs only in the frozen Docker
  verifier sandbox; a host-Python fallback is prohibited.

### Phase C: physical capacity

- Record current usable HBM and per-model peak HBM under the exact future run
  configuration.
- The candidate state working set must exceed usable HBM and at least one
  demanded state transition must require measured eviction/reload. A
  `models-max` setting alone does not pass.

### E300 decision

- **PASS:** A--C all pass with trace/schema validators and cleanup.
- **NO-GO:** any immutable identity, prospective notice, real execution,
  branch uncertainty or physical-capacity requirement fails.
- **TECHNICAL STOP:** another user's GPU workload, unavailable lawful artifact,
  or runtime incompatibility prevents safe measurement. Do not substitute a
  synthetic capacity cap.

## E301 - router/action qualification

Only after E300 passes, freeze `native-LRU`, `no-prepare`, `always-prepare`,
`highest-probability`, `deadline/slack`, and deterministic BranchDebt under
equal information, action and wall-clock budgets. Require exact action
readback, charged bytes/time, correctness and cleanup. No learned controller.

## E302 - held-out falsification

Use unopened task/time groups, at least two physical-pressure levels, paired
counterbalanced blocks, frozen seeds/exclusions/bootstrap, and the thresholds
in `DESIGN.md`. Failure against the strongest baseline is research No-Go.

## E303 - independent-context and ablation

Confirm without retuning on a second storage/hardware context and a held-out
model family. Ablate program dependency, wrong-branch debt, eviction debt and
abstention. Only joint E302/E303 success permits a CCF-B paper Go.
