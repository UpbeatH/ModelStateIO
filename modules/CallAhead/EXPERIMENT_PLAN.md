# CallAhead experiment plan

Status: **stopped at E001 with NO-GO on 2026-09-05**. E000 passed material and
technical qualification. E001 did not establish the required foreground-harm
affected set; E002--E006 are therefore closed without execution.

The plan is a fast-falsification ladder. A failed gate stops the corresponding
claim. Later stages may not repair an earlier failure by adding repetitions,
changing thresholds, selecting favorable models or enlarging the action space
after outcomes are visible.

## E000 - novelty, runtime and material qualification

### Objective

Determine whether the intended mechanism is distinct from current model-load,
adapter, KV-cache and program-aware serving systems, and whether the selected
runtime exposes a real, read-backable multi-model transition boundary.

### Required evidence

1. Source-level matrix against ServerlessLLM, BlitzScale, HydraServe,
   SYMPHONY, Agentix, dLoRA/S-LoRA/Punica, Mooncake, IMPRESS, Bidaw,
   SolidAttention and mzCache.
2. At least three provenance-complete model states with immutable IDs,
   versions, licenses, sizes and SHA-256 values. Two must differ materially in
   footprint; aliases or copies of one state do not count.
3. A documented router/admission path with effective load, queue, residency and
   eviction readback.
4. A user-scoped cold/residency-control method applied only to experiment-owned
   files, plus validation that it realizes the requested state.
5. A bounded foreground service workload and a private interference/preparation
   harness with explicit memory and I/O limits.

### Decision

- **PASS:** all five requirements are met without system-global changes.
- **NO-GO:** fewer than three traceable states, no effective action readback,
  no safe state-control method, or direct prior art already implements the
  complete proposed mechanism.

E000 is read-only/material qualification except for local documentation and
separately authorized user-private artifact preparation. It is not performance
evidence.

## E001 - causal interference and controllability death gate

**Decision:** NO-GO. Median eager relative p95 harm was 0.12%, with paired
block-bootstrap 95% interval [-3.01%, 5.90%], versus the frozen 10% threshold.
The approximately 0.40 s readiness benefit is real for this gate but does not
establish a need for harm-aware pacing. See `experiments/MSIO-CA-E001/`.

### Question

Does eager background model preparation create a repeatable foreground harm
that a bounded pacing action can reduce without eliminating most of the
readiness benefit?

### Frozen minimum design

- One resident foreground model serves a fixed, deterministic request stream.
- A distinct background model begins from a verified low-residency state.
- Arms: `none`, `eager75`, `paced75` only.
- Six counterbalanced blocks. Each arm receives the same foreground offered
  load, notice time, preparation bytes and observation fields; `paced75` may
  differ only in the prospectively frozen rate/chunk schedule.
- Each block contains enough foreground requests to estimate a block-level p95;
  the exact count, random seed and order must be frozen before execution.
- Record trigger-to-ready, request-visible readiness, preparation duration and
  bytes, model residency, process CPU/RSS, page faults, device bytes/activity,
  GPU memory/utilization, foreground p50/p95/p99, throughput and correctness.
- Preparation time before request arrival and unfinished/cancelled bytes are
  charged. All arms finish with process, GPU and owned-file cleanup audits.

### Confirmatory outcomes

- Eager harm: paired block-level foreground p95 difference between `eager75`
  and `none`.
- Preserved benefit: background readiness improvement relative to `none`.
- Pacing recovery: fraction of eager excess harm removed by `paced75`.

### GO

All correctness/cleanup checks pass, and:

1. `eager75` causes at least 10% median foreground p95 harm relative to `none`,
   with a fixed-seed block-bootstrap interval excluding zero;
2. `paced75` removes at least half of that excess harm; and
3. `paced75` retains at least half of `eager75`'s readiness benefit.

### NO-GO

Stop CallAhead's harm-control mechanism if eager preparation has no stable
material harm, if pacing cannot remove at least half the harm, or if pacing
removes most of the preparation benefit. Do not add memory pressure, change the
threshold or increase repetitions after observing the result.

## E002 - program-notice material gate

### Objective

Establish a non-oracular workload in which an application exposes a useful
future model-call frontier before request arrival.

### Minimum material

- At least three real state identities and 100 nonzero-notice events;
- immutable event ID, notice time, actual arrival, program dependency,
  candidate/selected state, deadline or launch window and completion;
- documented source, license/permission and generation procedure;
- time-held-out split frozen before policy development;
- at least one branch or prediction error so the decision is nontrivial.

An open agent/workflow execution trace is preferred. ServeGen or another
generator may supply background arrival/burst structure, but generated events
must be labelled synthetic and cannot replace real program dependencies.

### Decision

- **PASS:** the trace supports a decision before actual arrival and contains
  genuine state competition under finite capacity.
- **NO-GO:** notice is reconstructed from future arrival, model identity is
  hand-assigned after the fact, or the sequence contains no capacity conflict.

## E003 - router-integrated action and accounting qualification

Implement `none`, native LRU, eager fixed preparation, fixed-rate preparation
and a deterministic benefit-debt-harm rule in the real router path. Require
per-event action/readback receipts, immutable state identity, all transition
bytes, eviction/reload debt, foreground latency and cleanup. No learned policy
is allowed in this gate.

**PASS** requires exact action realization, complete accounting and no
correctness/version-isolation failure. This is still technical evidence.

## E004 - held-out policy falsification

### Design

- Development and time-held-out request windows are fixed before tuning.
- At least three model states, three workload structures and two capacity
  pressure levels.
- Compare the deterministic CallAhead rule with native LRU, no preparation,
  eager preparation, fixed75, fixed-rate and deadline/slack baselines under
  equal information, actions and wall-clock/controller budgets.
- Report readiness/TTFT, SLO attainment, foreground p95/p99, goodput,
  transition and wasted bytes, eviction reloads, DRAM/HBM residency, CPU/device
  overhead, starvation and failures.

### Research GO

On unopened windows, CallAhead must beat the strongest deployable non-oracle
baseline by at least 15% in the declared primary p95 readiness/TTFT metric or
reduce SLO violations by at least 30%, with a prospectively selected uncertainty
interval excluding zero. Foreground p99 harm must stay within 5%, aggregate
useful throughput within 95% of the best safe baseline, and correctness must be
perfect for admitted trials.

If only one context passes, the result is exploratory and does not proceed to
a paper-level claim.

## E005 - independent-context confirmation

Repeat the frozen mechanism, not a retuned policy, on at least one independent
hardware/storage context and one held-out model family or materially different
runtime. The second context must retain at least half the primary effect and at
least a 10% improvement over its strongest safe baseline, with no new safety or
correctness failure.

If the mechanism requires retuning using confirmation outcomes, E005 fails and
a new prospectively frozen study is required.

## E006 - ablation, robustness and paper artifact

Required ablations:

- remove program dependency and keep only arrival history;
- remove transition debt;
- remove foreground-harm term;
- disable abstention;
- replace pacing with full-speed fixed preparation;
- exact/offline cost oracle as a non-deployable upper bound.

Robustness must cross notice error, branch error, model size, capacity, request
burst, storage pressure and foreground-load groups. Release protocol, source,
seeds, compact data, manifests and analysis code; keep raw logs/models outside
Git with verified paths and hashes.

Only a jointly passing E004--E006 package can support a paper-level GO.

## Statistical and reporting rules

- Freeze primary endpoint, block unit, exclusions, seeds, repetitions,
  bootstrap method and multiplicity handling before each confirmatory run.
- Analyze paired/counterbalanced blocks; report effect sizes and uncertainty,
  not best cases or isolated p-values.
- Failed, timed-out, partially applied and contaminated trials remain visible.
- Development, exploratory and confirmatory results must be labelled separately.
- No result from ColdPath is pooled into a CallAhead confirmatory interval.

## Resource-governance boundary

CallAhead is not cluster-active. PFSOpt remains the only cluster-active PFS
line. Any remote audit, artifact transfer, dependency installation, runtime
modification or experiment requires a separately frozen executable packet and
the applicable authorization. No stage authorizes g129, Lustre/PFS, system
CUDA/driver/service changes, global cache clearing or access to another user's
files.
