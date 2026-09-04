# MSIO-LS-E000 preregistration: state-I/O affected-set gate

Status: frozen design; no result yet. Date: 2026-09-04 (Asia/Shanghai).

## Question

Does one full 7B model-weight read, when overlapped with a foreground 0.5B
cold launch on the same NVMe, reproducibly increase the foreground
time-to-exact-output compared with deferring that identical read until after
the foreground launch?

## Mechanism and boundary

The background operation is a 7B GGUF weight-file read using `dd iflag=direct`
and no GPU. The foreground is a cold 0.5B llama.cpp launch. This isolates a
storage queue/device externality from GPU-compute saturation. It is an
affected-set *causal qualification*, not an actual multi-model serving policy
or a paper claim.

## Frozen configuration

- Host/runtime/model identities: g127 and the isolated CUDA llama.cpp, 0.5B,
  and 7B GGUF artifacts recorded in MSIO-ST-I001.
- Before every foreground launch, file-scoped `POSIX_FADV_DONTNEED` is applied
  only to the owned 0.5B foreground model. A `mincore` receipt must show at
  most 20% residency after a two-second settle; otherwise stop technical.
- Before the first measured block, `strace` must show that the 7B background
  `dd` opens its model file using `O_DIRECT`; otherwise stop technical.
- Foreground action: fixed `llama-cli --load-mode mmap -ngl 99 --no-warmup
  --single-turn -n 1` and the exact prompt `Reply with exactly: R`.
- Each of six paired blocks has two arms: `defer` runs the full background read
  immediately after foreground completion; `overlap` starts it immediately
  before foreground launch and requires live-PID overlap. Both arms complete
  one full background read. Order is AB/BA/AB/BA/AB/BA.
- No cache drop, system parameter write, mount/service change, retry, process
  kill, or background GPU use is permitted. A failed sample is retained and
  ends the gate.

## Outcomes and decision

Primary outcome: foreground wall time to an exact standalone `R`; secondary:
resident fraction, background exit/duration, verified overlap, max RSS and
GPU snapshots. Report all six pair differences `overlap - defer`, empirical
per-arm p95, median contrast, and a fixed-seed block bootstrap interval.

**Go** only if all 12 foreground runs are correct, all six background reads
are effective and overlap their foreground run, at least five of six paired
contrasts are positive, paired-median degradation is at least 10%, empirical
p95 degradation is at least 15%, and the bootstrap lower bound is above zero.
Otherwise **No-Go** for LoadShield on this isolated storage-I/O mechanism.

Even a Go establishes only a single-node causal opportunity. A later policy
must beat deferred/FIFO, greedy, fixed cap, shortest-load and deadline/slack
baselines under equal offered work without starvation.

## Evidence root

Raw material: `/mnt/nvme3n1/chenhao/modelstateio-runtime/logs/MSIO-LS-E000/`.
Git receives only compact results, source hashes, and reviewed decision text.
