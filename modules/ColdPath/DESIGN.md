# ColdPath design

Status: local candidate, not activated on a remote host.

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

