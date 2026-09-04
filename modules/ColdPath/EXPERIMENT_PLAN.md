# ColdPath experiment plan

## Stage Q0 — completed locally

Validate that the three-route portfolio has unique questions, explicit hypotheses, baselines, metrics, Go/No-Go rules, and no cluster-active ModelStateIO module. See `../../experiments/MSIO-Q000/RESULT.md`.

## Stage E000 — next gate, not executed

1. Produce a separate execution packet using the workspace template.
2. Read-only audit one candidate V100S host: GPU/driver/CUDA, CPU/NUMA, RAM/swap, local NVMe identity/mount/filesystem/free space, active jobs/processes, llama.cpp/runtime revision, and available model artifacts/checksums.
3. Stop if the host is busy, storage identity is ambiguous, required artifacts are absent, or the action paths cannot be implemented without installation/system writes.
4. Run a tiny capability matrix only after separate execution authorization: one small model, default/mmap/buffered/direct-supported arms, cold and warm states, five repetitions, randomized order.
5. Primary metric: p95 time-to-ready (process start to first correct token). Secondary: TTFT, read bytes/bandwidth, CPU time, peak HBM/DRAM, GPU idle fraction, and foreground p99 harm.

The capability run cannot support a paper claim. It only decides whether to freeze a larger preregistration.

## Stage E001 — completed

The model-residency materiality gate passed on g129. See `experiments/MSIO-CP-E001/RESULT.md`. Because Linux page cache was not evicted, this advances only to path-feasibility design, not to a performance claim.

## Stage E002 — next gate

Inspect existing source/runtime capabilities and freeze a safe storage-cold protocol with at least two semantically distinct paths. E002 is read-only and must not start a model request. Do not install or patch software, drop global caches, remount filesystems, or use raw devices under the current authority. Stop if distinct paths cannot be exposed without one of those actions.
