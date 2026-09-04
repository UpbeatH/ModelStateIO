# WeightResidency / ColdPath validation decision

Decision date: 2026-09-04.

## `NO-GO` for CCF-B evidence on the current g127 Ollama platform

T003 established reproducible cold versus resident behavior for one model.
T005 established execution across two context footprints. T006 established a
bounded background-read externality probe. However, T004 confirmed that the
platform contains only `qwen2.5:7b`, and the runtime exposes no second
controllable loading path, KV/adapter residency signal, or isolated storage
device. The strongest fixed-path and multi-model comparisons required for a
CCF-B systems claim therefore cannot be run under the current platform.

The decision is a scope/evidence No-Go, not an impossibility claim about model
weight residency. The retained evidence supports only an engineering
feasibility result: a single-node API can distinguish cold and warm model
residency and remain correct under one bounded read load.

## Re-entry conditions

Reopen only with a separately frozen protocol that provides either (a) a
second approved model plus multiple effective loading paths and an isolated
storage root, or (b) a new, explicitly bounded research question whose
novelty and CCF-B evidence requirements are re-justified. Do not continue
automatic pressure repetitions under the current interface.

## Re-entry audit (2026-09-04)

The environmental part of condition (a) is now met for a new, bounded study:
g127 has a user-local CUDA llama.cpp runtime, a separately stored 0.5B GGUF
model, and syscall-level receipts distinguishing `mmap` from `none`. Requested
`dio` did not show `O_DIRECT` and is not an eligible treatment. The old
Ollama-only No-Go remains the historical decision for the multi-state claim;
this audit authorizes only protocol authoring and a new falsification gate for
single-state WeightResidency.
