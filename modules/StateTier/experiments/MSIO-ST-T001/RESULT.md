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

`NOT_RUN`. The packet requires a user-owned or explicitly isolated external data directory before starting a workload. Creating a directory under the shared root would make ownership and interference ambiguous. No model run, `strace`, file creation, configuration change, installation, or service restart was performed.

## Next gate

Obtain an explicitly isolated, writable experiment directory with an ownership marker and service-interference clearance, or revise the packet to use an approved existing data root. Then repeat the complete preflight immediately before collection. A weights-only trace remains `PARTIAL` and cannot test the multi-state hypothesis.

