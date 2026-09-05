# MSIO-SP-E002 result

Status: **inconclusive compatibility observation; no paper-line activation**.

## Established observations

- The fixed `seed-43` source tensor file was transferred with SHA-256
  `7dfc14a58e5cb529ac73b110650a559cb58e3983921cb76ac598b84def746021`.
- Strict conversion validated all 168 expected LoRA tensor pairs and produced
  a GGUF adapter with SHA-256
  `6d85ebfd886918702a535503790c1af5acc13a83f79483ec7820be2694216f00`.
- The local server loaded the adapter and each scale-control request returned
  `success:true`.
- Under the single frozen generic prompt, the disabled, enabled, and disabled
  responses had the same content SHA-256
  `e22822d88dea343a0c9a015ad9eb8d6b6cd0f78a17e268be986991bee3151c54`.

Raw receipts are outside Git at
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-SP-E002/20260905T101847+0800/`.

## Limitations and safety observation

The source adapter declares an exact base-model revision but the available Q4
GGUF does not expose a verifiable matching revision.  The generic prompt was
not a task-quality evaluation.  Equal output therefore does not prove the
adapter has no model-level effect; it only fails to provide an observable
effect under this frozen request.  It must not be followed by post-hoc prompt
selection or latency comparisons.

During cleanup, the runtime reported a CUDA error after a second interrupt.
No E002 server process remained, GPU memory returned to zero, and no core file
was found within the inspected private runtime root.  Still, this makes the
runner unsuitable for extension until its signal handling is redesigned under
a new protocol.

## Decision

Do not rerun E002.  StatePatch remains only an E001R1 single-adapter technical
lifecycle qualification.  A multi-adapter research gate requires an exact-base
artifact chain, an independently justified task-correctness oracle, a
multi-adapter lifecycle trace, and a cleanup-safe runner.
