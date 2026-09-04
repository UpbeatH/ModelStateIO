# StateTier experiment plan

Status: local-active in this branch, cluster-inactive.

## E000 — state-identity necessity gate

The first experiment is not a performance comparison. It asks whether at least two state classes (weights/experts, adapters, KV) prefer different actions under the same capacity pressure because of reuse horizon, recomputation cost, dirtiness, dependency position, or restore deadline. If not, stop the route.

### Provisional target

`g127-chenhao` is the selected candidate from the 2026-09-04 read-only audit. Observed: one V100S-PCIE-32GB, 0 MiB reported GPU memory use, 503 GiB RAM with 452 GiB available, no swap, `/mnt/nvme3n1` ext4 with about 1.3 TB free, and no user GPU compute process. This observation is time-bound and must be repeated immediately before execution. g128 was not selected because Milvus streamingnode was observed at about 159% CPU and several data services were active.

### Required packet contents before execution

- exact checked-out revision and external data root;
- model-state trace/schema and two or more state classes;
- fixed capacity-pressure levels, request sequences, randomization, and repetitions;
- equal bytes, equal action count, equal runtime, and capacity-matched baselines;
- primary metric: held-out p95 restore/TTFT; secondary metrics: hit rate, restore bytes, throughput, peak HBM/DRAM, CPU, write amplification, correctness;
- action allowlist, readback, timeout, rollback, and abstention to a safe default;
- literal stop conditions for host contention, missing artifacts, unsupported direct I/O, or identity ambiguity.

No controller implementation, system parameter write, remote experiment, or software installation is authorized by this document.

