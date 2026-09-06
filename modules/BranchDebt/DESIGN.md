# BranchDebt research design

Status: material qualification active under `MSIO-BD-E300`; no performance or
paper Go. Date: 2026-09-06.

## Question

Can a single-node model router use a prospectively visible application branch
to choose which immutable model state to prepare under a real HBM capacity
conflict, while charging wrong-branch bytes and eviction/reload debt?

## Prior evidence and non-inheritance

- CallAhead E001 observed about 0.402 seconds of readiness benefit but no
  material foreground-p95 harm. This motivates state selection and kills the
  old pacing premise; it is not BranchDebt confirmation.
- CallAhead E200/E201 found no public trace that already joins a prospective
  program frontier to physical model-state capacity. BranchDebt therefore
  collects a new execution trace from an open workflow; it may not relabel a
  historical arrival log.
- Existing router/LRU and model-loading systems remain strong baselines.
  Program awareness, prefetch, an LLM policy, or a capacity limit is not novel
  alone.

## Candidate mechanism

An executable workflow emits a decision receipt when its current node makes a
set of next model calls program-visible. BranchDebt may use only that receipt,
immutable model identities, current residency, frozen capacity, and costs
learned from earlier development events. It chooses `abstain`, `retain`,
`evict`, or `prepare-one`. Actual future arrival, branch outcome and
post-decision measurements are forbidden inputs.

The core accounting is:

`readiness saved - preparation work - wrong-branch bytes - eviction reload debt`

Foreground-harm pacing is not part of the first candidate.

## CCF-B contribution threshold

A paper-level candidate requires all of the following:

1. a real executed, open and reproducible multi-model workflow trace with at
   least three immutable states and prospective branch notices;
2. a measured physical capacity conflict, not only a software `models-max`
   setting;
3. a router-integrated implementation with action/readback receipts and total
   transition accounting;
4. held-out improvement of at least 15% in p95 readiness/TTFT or at least 30%
   fewer SLO violations over the strongest deployable equal-information
   baseline, with a frozen interval excluding zero;
5. perfect admitted-request correctness, p99 harm within 5%, useful throughput
   at least 95% of the best safe baseline, and an independent context retaining
   at least half the main effect and at least 10% improvement.

## Stop boundary

Stop if the workflow notice is reconstructed from the future, state identity
is assigned after execution, physical capacity competition is absent, the
strongest deterministic baseline closes the effect, or the mechanism needs a
global cache/CUDA/service mutation. Synthetic fixtures may validate code but
cannot satisfy the research gate.
