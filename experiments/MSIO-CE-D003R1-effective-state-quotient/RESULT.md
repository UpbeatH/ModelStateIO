# MSIO-CE-D003R1 result

Date: 2026-09-08. Decision: `NO_GO_EFFECTIVE_QUOTIENT_GAP`.

## Observation

- All 30 scheduled configurations completed on g127: two Qwen2.5 GGUF
  models, 15 deterministic configurations per model, 30/30 usable responses
  and 30/30 clean process/GPU cleanup checks.
- The 30 requested configurations produced 16 observed execution-plan
  classes. Fourteen executions (46.67%) repeated an already represented class.
- Every repeated class stayed inside a predeclared expected-equivalence label:
  `auto`/`all`/saturated numeric GPU-layer requests, `auto` resolving to
  `mmap`, and `ubatch` being capped by `batch`. No repeated class crossed the
  expected labels.
- FlashAttention `on` and `off` remained distinct effective classes on both
  models. Their single observations suggest request-time differences, but this
  is an ordinary documented runtime knob, has one trial per cell, and is not a
  quotient-tuning contribution.

## Decision

The measured 46.67% raw-space duplication is removable by deterministic
front-end normalization; this experiment found no non-obvious effective-state
equivalence that justifies a new runtime-aware quotient tuner. Together with
the historical D000 result that 108/108 valid ModelStateIO episodes were
effectively applied, the present evidence does not support either the original
post-ACK-contamination route or the revised equivalence-class route as a CCF-B
paper mainline.

Do not expand this matrix, add an LLM proposer, or install a second runtime to
rescue D003. Re-entry requires a new natural incident or independently observed
runtime behavior that cannot be removed by documented normalization.

## Technical correction and evidence

The first analysis incorrectly treated any occurrence of the text "Flash
Attention enabled" as the final state and briefly merged `on` with `off`.
Raw logs showed the final `llama_context: flash_attn` field unambiguously. The
analyzer was corrected to use the final field; the corrected class count is 16
and the unexpected-cross-label count is zero. No trial was rerun or removed.

- Remote raw root:
  `/mnt/nvme3n1/chenhao/modelstateio-runtime/experiments/MSIO-CE-D003R1-EFFECTIVE-STATE-QUOTIENT`
  (65 files, 4,733,681 bytes).
- Local external copy:
  `D:\Workspace\Working\Working\Research\ModelStateIO-data\MSIO-CE-D003R1-EFFECTIVE-STATE-QUOTIENT-20260908`.
- `receipts.json` SHA-256:
  `4e4af92ea5b357c8d0e33d82cba6a5c32fc4086273feeeb98e5feb6cc15575d9`;
  the local and remote copies match.
- The corrected local and remote analyses are structurally identical; their
  byte hashes differ only because Windows and Linux emitted different newline
  encodings.

Evidence level: exploratory, one llama.cpp runtime, one V100S host. This is a
fast research-route decision, not a publication result or novelty claim.
