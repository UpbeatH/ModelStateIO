# MSIO-CE-D003R1 effective-state quotient fast gate

Date: 2026-09-08. Status: authorized exploratory execution.

This is the lean replacement for the original D003-A post-ACK mismatch screen.
Historical ModelStateIO evidence contains 108/108 effective actions, so another
LLM proposal/validation study is not the shortest path to a paper.

## Question

Do distinct, valid llama.cpp request configurations collapse to the same
effective execution plan often enough that an effective-state quotient could
save a configuration tuner's execution budget beyond documented aliases and
simple range clipping?

## Fast gate

- one pinned standalone llama.cpp runtime on g127;
- Qwen2.5-0.5B and Qwen2.5-7B GGUF models;
- 15 deterministic configurations per model (30 total);
- requested dimensions: GPU layers, load mode, context, batch/ubatch,
  FlashAttention and KV type;
- observed plan: realized load mode, offloaded layers, context/batch/ubatch,
  actual FlashAttention state, KV buffers, model-file mapping and GPU memory;
- one deterministic request checks that a usable outcome was produced.

The stage continues only if at least one repeated effective class crosses the
predeclared expected-equivalence labels, is not explained by an invalid action,
and the measured duplicate-execution fraction is at least 20%. Otherwise the
quotient-tuning route stops. This stage is exploratory and single-runtime; a
positive result still requires an independent backend and equal-budget tuning
comparison before it is paper evidence.

Raw logs and receipts remain outside Git in the task-owned g127 result root.
No LLM proposer, package installation, PFS action, system setting, service
change, cache drop, commit or push is part of this gate.
