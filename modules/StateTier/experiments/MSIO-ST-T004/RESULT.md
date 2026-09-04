# MSIO-ST-T004 model-footprint expansion gate

Date: 2026-09-04 (Asia/Shanghai). Target: `g127-chenhao`.

## Observation

Read-only inspection of the Ollama registry and blob directory found exactly
one usable model: `qwen2.5:7b` (7.6B, Q4_K_M, approximately 4.68 GB on disk and
8.21 GB reported VRAM residency). No second model or alternate footprint is
present. The NVMe has approximately 1.2 TB free, but model download was not
authorized by the packet and would alter the shared service's artifact state.

## Decision

`BLOCKED_INPUT`. The CCF-B-oriented expansion gate requires at least two model
footprints. Running more repetitions of the same model would not satisfy that
requirement and would create pseudo-replication. No workload was run.

## Next gate

Obtain an explicitly approved second model artifact (or a separately frozen,
defensible same-model footprint protocol) and repeat the full preflight. Until
then, do not claim multi-model robustness or paper readiness.

