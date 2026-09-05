# CallAhead research design

Status: **NO-GO under MSIO-CA-E001**. Date: 2026-09-05. This document records
the tested candidate question and its stopping boundary. It does not reopen
ColdPath or permit post-hoc pressure/model/load changes to rescue the failed
causal premise.

Working title: **CallAhead: Program-Aware, Harm-Bounded Model Warming on
Memory-Constrained LLM Servers**.

## 1. Central research question

Can a single-node LLM server use non-oracular knowledge about an application's
future model calls to prepare model state before arrival, while bounding cache,
memory, I/O and foreground-service harm under limited local resources?

The system problem is not to predict an arbitrary next request. It is to turn
information already exposed by an agent or workflow program into a safe
physical-state transition across NVMe, host page cache/DRAM and GPU memory.

## 2. Evidence-backed motivation

### 2.1 Established local observations

- ColdPath E021 observed a 10.50% median request-latency reduction from a
  completed 75% prefix preparation on the 0.5B model; its fixed-seed bootstrap
  interval for the paired median difference was [-0.372, -0.124] seconds.
- E023 observed a 35.51% median reduction on a hash-distinct 7B model under the
  fixed 75% preparation rule, with all six paired contrasts negative. The 7B
  acquisition provenance limitation remains part of that evidence.
- E022R1, E025 and E026R1 separated completed preparation from preparation
  still active at request arrival. Both mechanisms can reduce request-visible
  latency in the tested single-host conditions.
- E024 did not confirm the announced-lead controller's performance. E027 could
  account for only a bounded notice-to-completion interval, while E028 could
  not test page-cache displacement or a co-tenant. ColdPath therefore remains
  paper-level No-Go.
- E031 established an inspectable llama.cpp multi-model queue/LRU boundary, but
  no admissible workload, complete three-model corpus or harm measure.

These observations establish a preparation opportunity and important failure
modes. They do not establish CallAhead, a controller benefit, general total
cost, or a paper result.

### 2.2 Literature boundary

Direct prior work already covers major adjacent mechanisms:

- ServerlessLLM, BlitzScale and HydraServe optimize distributed model loading,
  placement, stage overlap and live autoscaling.
- dLoRA, S-LoRA and Punica cover multi-tenant adapter serving, dynamic
  orchestration and adapter memory management.
- Mooncake, IMPRESS, Bidaw, SolidAttention and SYMPHONY cover KV-cache reuse,
  tiering, selective loading, prefetch and advisory requests.
- The local Papers summaries for
  [mzCache](../../../Papers/2026-mzCache/notes/SUMMARY.md) and
  [xrd-uCache](../../../Papers/2026-xrd-uCache/notes/SUMMARY.md) show that
  partial restoration/overlap and negative cache regimes are already known.

Therefore none of the following is novelty by itself: partial preparation,
arrival prediction, adding NVMe, choosing a percentage, using an LLM/RL/BO
controller, or combining several state classes.

## 3. Gap and hypothesis

### Gap

Existing systems primarily optimize distributed placement, aggregate loading
speed, or one state class. The candidate gap is a single-node contract that
connects program-visible future-call structure to a measurable local physical
state transition and refuses or paces that transition when the expected
readiness benefit does not repay eviction debt and foreground harm.

This gap is a hypothesis until a source-level prior-art audit and the first
causal experiment both pass. A different state type or smaller platform is not
in itself a contribution.

### Main hypothesis

For multi-model LLM programs with bounded advance knowledge, a controller that
jointly accounts for call uncertainty, cold-readiness benefit, transition
bytes, evicted-state reload debt and foreground harm can improve held-out p95
readiness or SLO attainment beyond the strongest equal-information fixed and
LRU policies, without material foreground degradation.

### Mechanism chain

`program frontier -> non-oracle notice interval -> state/capacity snapshot ->
benefit-debt-harm estimate -> abstain/retain/evict/prepare/pace -> readback and
foreground observation -> bounded update`

## 4. Proposed contributions and claim boundaries

### C1. Program-frontier notice contract

Expose immutable event identity, candidate model-state identities, program
dependency, notice time and an arrival/deadline interval before the physical
action. Actual arrival, post-decision residency and completion are forbidden
inputs. Missing or ambiguous identity causes abstention.

**Claim boundary:** program awareness alone is not novel. The contribution
must show that this contract enables a safe action unavailable to an
arrival-only router under the same information budget.

### C2. Benefit-debt-harm accounting

Estimate net value as readiness latency avoided minus preparation work,
wasted bytes, evicted-state reload debt, memory residency cost and foreground
SLO risk. The system must account from notice/trigger to completion; work
performed before request arrival is not free.

**Claim boundary:** a cost model is not a contribution unless its components
are measured, ablated and necessary on held-out workloads.

### C3. Harm-bounded state transition

Integrate with a real multi-model router and implement bounded preparation with
readback. The eventual action space may include abstention, retention,
eviction, preparation fraction, chunk size, I/O rate and concurrency. The first
gate deliberately exposes only `none`, `eager75` and `paced75` to avoid an
unidentified high-dimensional tuner.

**Claim boundary:** CallAhead may claim only the implemented state class and
tiers. It may not claim unified weight/adapter/KV management without direct
evidence for each class.

## 5. Prospective information and action contract

### Decision-time information

- immutable event, application and program-node identifiers;
- notice timestamp, dependency edge and candidate state ID/version/digest;
- declared arrival/deadline interval and its provenance;
- model-state bytes and current tier/residency readback;
- user-scoped DRAM/page-cache/HBM headroom and device activity;
- foreground queue, latency budget and recent non-future service measurements;
- transition-history estimates learned only from earlier/development events.

### Forbidden information

- actual future arrival or selected branch before it is program-visible;
- post-action completion, residency, latency or correctness;
- a result-derived threshold fitted on confirmatory traces;
- model identity synthesized from an observed outcome;
- private production traces without documented permission and provenance.

### Eventual actions

- `abstain` or leave native routing unchanged;
- retain or evict an eligible model state;
- prepare a bounded fraction of an immutable, verified state file;
- pace chunk size, rate or concurrency within a frozen user-space limit;
- cancel only when cancellation semantics and charged work are explicit.

All actions require allowlists, range checks, effective-setting readback,
timeouts, cleanup and a fallback to the native router.

## 6. Strong baselines

- native router LRU with no proactive preparation;
- no preparation;
- always/eager preparation at the same maximum action budget;
- fixed 75% preparation;
- fixed-rate preparation;
- recency/frequency or static-hotset retention;
- deadline/slack rule using exactly the same notice fields;
- offline clairvoyant oracle as an upper bound, never as a deployable baseline;
- any reproducible ServerlessLLM/HydraServe/SYMPHONY-inspired policy whose
  information and actions can be implemented fairly on the selected runtime.

An LLM, RL, contextual bandit or Bayesian optimizer is eligible only after a
deterministic rule leaves repeatable held-out regret. Model choice is then an
ablation, not the paper's central contribution.

## 7. Safety and scope

- First experiments are single-node and user-scoped. They must not alter
  system CUDA, drivers, services, global cache state, Lustre/PFS or other users.
- Cold control must use experiment-owned immutable files and a separately
  verified user-scoped method. A global `drop_caches` operation is forbidden.
- Correctness requires exact artifact identity, deterministic request checks
  where possible, version binding, clean process termination and no residual
  memory/GPU allocation.
- The current g130 results support only a pilot. Final evidence must include an
  independent model and hardware/storage context before making broader claims.

## 8. Explicit non-goals

- a generic model-state operating system;
- unified weights, experts, adapters and KV caches in the first paper;
- cluster-scale autoscaling or multi-node checkpoint distribution;
- learning a policy before establishing a causal opportunity;
- paper claims from synthetic replay alone;
- retroactively reclassifying ColdPath results as CallAhead confirmation.

## 9. Research decision

CallAhead is the highest-ranked prospective ModelStateIO candidate because it
uses the strongest retained local mechanism while directly addressing the
controller and harm gaps that closed ColdPath. It remains inactive until the
interference-existence gate in `EXPERIMENT_PLAN.md` is frozen, reviewed and
separately authorized for execution.
