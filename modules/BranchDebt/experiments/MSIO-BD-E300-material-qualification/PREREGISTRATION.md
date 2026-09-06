# MSIO-BD-E300 material qualification

Status: frozen before source acquisition or GPU execution. Date: 2026-09-06.
Evidence level: material/workload qualification only.

## Frozen source candidate

- Workflow/task source: `pagarsky/agent-trace`, to be pinned to the exact
  acquired Git commit. Candidate task families are MBPP and the repository's
  curated NL2Bash/InterCode fixture.
- The upstream traces are not BranchDebt evidence. Only new executions under
  the frozen program-frontier instrumentation may qualify.
- Before use, record repository commit, code license, upstream task-license
  boundary, file inventory and SHA-256. No install or GPU run occurs during
  source acquisition.

## Frozen workflow contract

The prospective program has three roles: planner, one of two solver branches,
and verifier/repair. The planner output makes the candidate solver set and
dependency edge visible; an actual tool/environment step must occur before the
selected solver request, creating a naturally measured notice interval. The
verifier may open a repair branch only from its observed correctness result.

The branch policy and prompts must be frozen in code before the first measured
task. A delay inserted only to create lead time, a model identity attached
after seeing the answer, or a notice reconstructed from arrival is a protocol
failure.

### Frozen MBPP realization

- Task source is the MBPP prompt embedded in the pinned AgentTrace source
  snapshot. Historical model output and timing fields are ignored.
- `primary = Qwen2.5-7B-Instruct-Q4_K_M`, candidate frontier =
  `{Qwen2.5-14B-Instruct-Q4_K_M, Qwen2.5-32B-Instruct-Q5_K_M}`.
- The frontier notice is emitted immediately after the primary answer is
  durably received and before any test is executed. Both repair candidates
  and the dependency edge are therefore known before the branch outcome.
- The primary answer is then checked by the frozen verifier. `pass` opens no
  repair request; syntax/import/timeout/resource failures select the 32B
  repair branch; assertion-only failures select the 14B repair branch. This
  mapping is immutable after the first task outcome is opened.
- Notice time, verifier start/end, repair arrival and completion are captured
  from one monotonic clock. A nonzero interval must arise from real verifier
  work; no inserted sleep qualifies.
- Generated code is never executed directly on the host. The verifier must use
  an already available Docker runtime with network disabled, read-only root,
  dropped capabilities, no-new-privileges, bounded CPU/memory/PIDs/output and
  a hard wall-clock timeout. Absence of a qualifying isolated image/runtime is
  a technical stop, not permission to weaken isolation.

### Frozen task split

- Normalize tasks by SHA-256 of the exact prompt and deduplicate before split.
- The first 300 unique tasks in source order are development/material tasks;
  the next 100 are held out for E302 and must not be opened during E300/E301.
- E300 may stop after 100 valid development events once all material criteria
  pass. It may not substitute historical AgentTrace results for new events.

## Model and capacity contract

The existing Qwen2.5-0.5B, Qwen2.5-1.5B and SmolLM2-1.7B artifacts qualify for
workflow bring-up only. Their combined file size is insufficient for physical
capacity evidence. The performance gate requires three individually loadable,
officially pinned artifacts whose measured simultaneous working set exceeds
the V100's currently usable HBM under the exact context configuration.

Large-artifact acquisition is permitted only from official Apache-2.0 model
repositories, into the g130 `chenhao` private runtime, with partial-file name,
size/hash/source receipt and atomic final rename. Acquisition is not model
loadability or capacity evidence.

## Safety and stopping

- Only g130 private ModelStateIO paths; no g129, PFS/Lustre, system CUDA,
  driver/service, global cache, installation or other-user directory.
- Do not start a GPU process while an unrelated GPU process is present.
- Stop rather than reduce the physical-capacity criterion, hand-write a trace,
  or change the workflow after observing outcomes.

## Decision

E300 remains incomplete until source identity, new trace qualification, model
identity/loadability and measured physical conflict all pass. Any scientific
requirement that cannot be met is No-Go; transient external occupancy is a
technical stop with a resumable safe checkpoint.
