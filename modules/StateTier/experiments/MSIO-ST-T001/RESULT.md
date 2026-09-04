# MSIO-ST-T001 result

Date: 2026-09-04 (Asia/Shanghai). Target: `g127-chenhao`.

## Preflight observations

- GPU: Tesla V100S-PCIE-32GB, 1% utilization, 0 MiB reported use.
- Memory: 503 GiB total, 452 GiB available, no swap.
- Load: 0.42/1.30/1.53 at collection time.
- Observation tools present: `/usr/bin/strace`, `/usr/bin/perf`, `/usr/bin/iostat`.
- Ollama: `/usr/local/bin/ollama` service is running; `qwen2.5:7b` is installed. Its model blob is owned by `ollama:ollama`.
- Proposed data root `/mnt/nvme3n1/chenhao/modelstateio-runtime` does not exist. The parent `/mnt/nvme3n1` is `root:root` with mode `777` and is shared through Kubernetes local-volume mounts.

## Decision

The directory prerequisite was later satisfied by explicit user authorization and ownership verification. Two bounded `ollama run qwen2.5:7b` probes were then attempted. Both timed out after 90 seconds with exit code 124, produced empty stdout, and generated no model-state trace. The process wrapper exited cleanly; iostat and SHA-256 receipts were written under the external run directory.

Decision: `TECHNICAL_FAILURE / NOT_RUN_FOR_SCIENCE`. This is a runtime/observability failure, not evidence for or against the StateTier hypothesis.

## Next gate

Diagnose the Ollama timeout without changing system configuration: first perform a read-only health/API check and verify whether the service can answer a trivial request within a short bound; then test the existing model with a separately frozen packet. Do not repeat the 90-second probes unchanged. A weights-only trace remains `PARTIAL` and cannot test the multi-state hypothesis.
