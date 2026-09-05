# ColdPath design

Status: the original loading-path/controller candidate is closed. `RiskPrefetch`
is a distinct, unactivated re-entry candidate; it does not reopen E024.

## Falsifiable claim

Context-conditioned, dependency-aware choice of model-loading path reduces held-out p95 readiness latency beyond the best fixed path under equal information, action availability, and runtime budget, while bounding memory and foreground harm.

## Frozen first information/action space

- Information: model bytes and format, current HBM/DRAM headroom, page-cache state, device read characteristics, requested context size, and foreground load class.
- Actions: framework default, mmap/page-cache, explicit buffered sequential prefetch, and direct/asynchronous path only when supported and read back successfully. Loading order is fixed in the first gate to avoid conflating two mechanisms.
- Excluded initially: kernel/sysctl writes, filesystem remounts, learned online exploration, multi-node loading, and hidden oracle features.

## Correctness and safety

Identical model digest/configuration, deterministic prompt/token check, timeout, process cleanup, disk-capacity guard, temperature/power logging when available, and abstention to framework default on unsupported paths. A partially applied path is a failed action.

## Evidence boundary

The historical workspace records V100S-class hosts and one quantized 14B run, but there has been no current live audit. These facts support feasibility screening only.

## RiskPrefetch re-entry candidate

### Problem and hypothesis

The original ColdPath controller failed because an announced lead alone did not
reproduce a completed-preparation benefit (E024), and it had no evidence about
cache displacement or a co-tenant. The new hypothesis is narrower: an
application or scheduler can supply a traceable *pre-arrival state request*,
and a controller can either abstain or reserve a bounded preparation budget
when requested state, deadline confidence, and current headroom pass a frozen
safety test. It must account for all preparation time and bound foreground harm.

This does not predict arrivals from post-arrival fields or retune E024's lead
threshold. Without a real non-oracle notice source and a user-scoped contention
measurement, it remains a design hypothesis only.

### Frozen prospective interface

- Required pre-decision fields: event ID; notice timestamp; requested
  model/adapter state ID, version and content digest; state-byte estimate;
  declared deadline or launch window; and an application/scheduler provenance
  label.
- Required measurement fields: actual arrival; completion; preparation bytes
  and duration; resident fraction; CPU/DRAM/GPU headroom; foreground latency;
  correctness; cleanup; and a user-scoped contention or displacement measure.
- Allowed first actions: `abstain`, 25%, 50%, or 75% bounded preparation. The
  action budget, state-byte cap and one-action-per-notice rule must be identical
  for learned and fixed baselines.
- Forbidden information: actual arrival, post-decision residency, completion,
  or any field written after the action decision. A missing required field
  causes abstention, not imputation.

### First falsification gate

`MSIO-CP-E029` is a read-only material audit. It requires a provenance-complete
record of at least two state identities and enough pre-arrival notices to form a
time-held-out split. The currently available Qwen trace is tested as a possible
source, not assumed to qualify. Failure leaves both the old controller NO-GO
and this new candidate inactive; no GPU run follows.
