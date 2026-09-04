# MSIO-CP-E000 result

Run date: 2026-09-04.

## A0

Technical failure: the frozen `lsblk` column set was unsupported on the older hosts, and the unbounded mount/process output was too large for an auditable return. No remote state was changed and no host was selected from the truncated evidence.

## A1 compatible audit

All four required SSH aliases resolved to the expected hostnames. Each exposed one Tesla V100S-PCIE-32GB GPU.

| Host | GPU observation | Local storage/runtime observation | Decision |
|---|---|---|---|
| g127 | 0 MiB, 1% sampled utilization | root NVMe 89% used; Ollama and qwen2.5:7b present; persistent MinIO/K3s activity | reject for first gate |
| g128 | 4 MiB, 0% sampled utilization | multiple mounted NVMe devices; Ollama models present; Milvus at about 148% CPU during sample | reject as busy |
| g129 | 4 MiB, 0% sampled utilization; no compute process | NVMe root with about 1.34 TB available; Ollama 0.5.13 and qwen2.5:14b present; 492 GiB available RAM | select for E001 |
| g130 | 0 MiB, 1% sampled utilization | `/mnt/nvme1` with about 2.45 TB available; Ollama/model present; six users and persistent MinIO/K3s activity | reserve, do not use |

Observation boundary: the samples establish point-in-time readiness only. They do not guarantee exclusive access or future availability. `findmnt -S '/dev/nvme*'` returned no rows on these older tools even though `lsblk` and `df` agreed on the device/mount mappings; selection relied on the agreeing latter two sources and did not authorize raw-device access.

Decision: E000 PASS for preparing a tiny g129 model-residency gate. No benchmark ran during E000.
