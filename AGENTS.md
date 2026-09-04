# ModelStateIO operating instructions

This is a local-first research line for storage-aware management of model state on a single node. "Model state" includes weights, experts, adapters, and KV cache. The line is method-neutral: an LLM, RL, or Bayesian optimizer is never a contribution by itself.

- Begin with the frozen local qualification gate. Do not connect to a remote host, run a GPU experiment, install software, or alter system/storage settings without a separate executable task packet and authorization.
- Keep `PFSOpt` as the only cluster-active line unless the global handoff explicitly changes that decision.
- Label paper evidence, local observation, inference, hypothesis, target, and recommendation separately.
- A local validator proves only protocol completeness. It is not system-performance evidence.
- Keep raw data, logs, traces, models, and checkpoints outside Git under a future host-native data root.
- Do not stage, commit, push, or create a Git repository without separate authorization.

