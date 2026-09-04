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

E002 stopped with a technical NO-GO: the current runtime exposed no supported second path with effective-setting readback. Internal binary symbols are not a path implementation. Do not rerun with undocumented API fields.

## Stage E006 — load-mode realization gate

The later isolated llama.cpp revision on g130 documents `mmap`, `none`, and `dio` loading modes, so E002's runtime-specific platform conclusion is stale for that binary. E006 performs one correctness-only smoke per mode and uses path-filtered open-call receipts to require `O_DIRECT` for `dio`. It does not clear caches or compare timing. Only a PASS can justify designing a randomized repeated loading-path measurement protocol.

E006 passed. E007 is the prospective warm-state measurement qualification: six counterbalanced three-arm blocks, process-start-to-first-exact-response instrumentation, frozen correctness checks, and a robust-CV threshold. It decides only whether the measurement is stable enough for a later comparison; it does not rank paths.

E007 stopped at 11/18 because its driver did not identify the exact guard failure. E008 is a local-only runner-observability correction with explicit stop reasons, PID/command snapshots, and bounded cleanup-settle branches; it must pass before any new repeated measurement ID.

E008 generated the expected fixture receipts but its transferred shell parser had a quoting defect. E008R1 is the new-ID integration correction using shell-native receipt checks; E007 and E008 remain closed.
