# MSIO-ST-E000 result

Date: 2026-09-04 (Asia/Shanghai). Target: `g127-chenhao`.

## Scope

The frozen packet authorized read-only preflight and artifact discovery only. No model workload, system/storage parameter write, installation, mount, or deletion was performed.

## Observed preflight

- Host: `g127`.
- GPU: Tesla V100S-PCIE-32GB; 0 MiB reported GPU memory use; no compute application reported.
- Memory: 503 GiB total, 452 GiB available; no swap.
- Load: 3.07/1.99/1.71 at collection time; MinIO, k3s and monitoring services are active.
- Storage: `/mnt/nvme3n1` is ext4, 1.8 TB total, about 1.3 TB free. The device is also exposed through Kubernetes local-volume mounts, so it is not an isolated experiment disk.
- Runtime: `/usr/local/bin/ollama` exists and `qwen2.5:7b` is installed.
- Candidate artifacts: a historical `/mnt/nvme3n1/qcfuse_cache/phase2_results_prophetkv_ruler_vt.jsonl` was found. Its identity and state-class coverage were not opened or accepted as a StateTier trace.

Follow-up read-only check (authorized continuation): the file is 17,038 bytes,
modified 2026-07-14, SHA-256
`7c0f7208f4e07b4cd9548e58225f8eab8bbfd7d860a46d68764a52af69dac437`. The first
three records contain only `idx`, `ttft`, `metric`, and `text`; no model-state
class, reuse, dependency, deadline, residency, or transition field is present.

## Decision

`NOT_RUN` — the packet's artifact prerequisite is not met: the inspected file
is a generic historical result rather than a multi-state trace, and the
candidate NVMe is shared with active services. The StateTier hypothesis is
therefore neither supported nor refuted.

## Exact next gate

Obtain or record a provenance-verified trace/workload containing at least two state classes and their reuse/dependency/deadline metadata, then repeat the host/storage audit. If no such trace can be obtained without disturbing shared services, stop StateTier E000 and revise the design to a clearly bounded single-state experiment.
