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

The diagnostic HTTP API probe then succeeded. A cold `qwen2.5:7b` request returned `READY` in about 7.98 s, including about 7.86 s model-load time; a warm request returned `W` in about 0.26 s. Both returned valid JSON and one generated token. These are real cold/warm weight-residency observations, not a multi-state trace.

Decision: `PARTIAL`. The API path is usable and the weight cold/warm lifecycle is observable, but no KV/Adapter/Expert state was exposed. The StateTier necessity hypothesis remains untested.

## Next gate

Next: freeze a narrow API-based packet to expose a second state class (KV or adapter) using only supported existing interfaces. If no second class can be observed, stop the unified StateTier route and re-scope to a cold/warm weight-residency study.
