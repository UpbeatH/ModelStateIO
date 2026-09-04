# MSIO-WR-E001 preregistration: loading-path weight residency gate

Status: frozen design; no result yet. Date: 2026-09-04 (Asia/Shanghai).

## Question and hypothesis

**Question.** For two fixed Qwen GGUF footprints on g127, does the effective
loading path (`mmap` versus `none`) produce a repeatable cold-start TTFT or
wall-time difference that remains correct and does not simply exchange it for
excessive memory or I/O cost?

**Hypothesis.** The paths can change cold-start cost because `mmap` has a
file-backed mapping whereas `none` performs non-mmap loading. This is a
bounded mechanism study, not a multi-state policy or a CCF-B contribution.

## Frozen scope

- Host: `g127-chenhao`; abort before first sample if another user GPU process,
  insufficient free NVMe space (< 50 GiB), or host-wide memory pressure is
  observed.
- Runtime: user-local llama.cpp CUDA build recorded in MSIO-ST-I001;
  `-ngl 99 --no-warmup --single-turn -n 1`.
- Models: isolated 0.5B and 7B Q4_K_M GGUF files and hashes recorded in
  MSIO-ST-I001. Do not read from the Ollama model root.
- Treatments: `--load-mode mmap` and `--load-mode none` only. `dio` is
  excluded because it lacked an observed O_DIRECT receipt.
- Request: `Reply with exactly: R`; correctness requires process exit 0 and
  a standalone `R` output.
- Outcome: wall time in milliseconds measured by `/usr/bin/time`; secondary
  maximum RSS and sampled GPU peak memory. No claim about steady-state
  throughput, cache eviction, or production serving follows.

## Design and fairness

For each model, run three paired blocks. Each block contains one `mmap` and
one `none` run, with order AB/BA/AB for blocks 1/2/3. Both treatments receive
the same prompt, tokens, GPU offload, runtime binary, timeout (240 s), and
one fresh process. Before each run, record host state; no cache-drop, process
kill, system parameter write, or shared-storage interference is permitted.

Primary within-block contrast is `none_ms - mmap_ms`. Report all six raw
pairs per model, median contrast, and min/max; no inferential p-value is
planned. A timeout, incorrect output, or unavailable model is a failed sample
and is not silently replaced.

## Go / No-Go

**Go to a larger bounded validation** only if both models have three correct
pairs, no host-abort condition, and the same-direction median absolute
contrast is at least 10% of the paired median wall time. Otherwise **No-Go**
for this loading-path hypothesis on the tested host. Either outcome remains
below CCF-B evidence: a future paper route needs stronger novelty, controlled
cache/pressure evidence, robust workloads, and equal-budget baselines.

## Evidence handling

Raw logs stay under
`/mnt/nvme3n1/chenhao/modelstateio-runtime/logs/MSIO-WR-E001/`; Git receives
only a compact manifest and reviewed result summary. Record command, model
hash, start/end timestamps, exit status, output correctness, and telemetry for
every attempted sample.
