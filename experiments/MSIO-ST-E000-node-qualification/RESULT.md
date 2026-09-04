# MSIO-ST-E000 node qualification

Date: 2026-09-04 (Asia/Shanghai)

Scope: read-only candidate selection for StateTier. No workload, parameter write, installation, mount, or data mutation was performed.

## Observations

| Candidate | GPU | GPU process | Memory/swap | Storage | Activity |
|---|---|---|---|---|---|
| g127-chenhao | V100S 32 GB; 0 MiB used | none reported | 503 GiB total, 452 GiB available, no swap | `/mnt/nvme3n1`, ext4, ~1.3 TB free | MinIO/k3s services exist; low system load (~1.32) |
| g128-chenhao | V100S 32 GB; 4 MiB used | none reported | 503 GiB total, 486 GiB available, no swap | `/data` ~521 GB, `/data1` ~855 GB, `/data2` ~283 GB, `/data3` ~269 GB free | Milvus streamingnode ~159% CPU; multiple services/data mounts |

## Decision

Provisionally select g127 for a future StateTier E000 execution packet. This is a suitability observation, not an availability reservation and not performance evidence. Repeat the audit immediately before execution; stop if GPU, CPU, storage, model identity, or process state differs from the packet.

