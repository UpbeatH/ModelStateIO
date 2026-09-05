# MSIO-SP-E003 exact-base multi-adapter acquisition result

## Established acquisition evidence

Raw material was legally downloaded to the Git-external local root
`C:\Temp\ModelStateIO-acquire\2026-09-05\statepatch-exact-base\`.

| material | source revision | bytes | SHA-256 |
| --- | --- | ---: | --- |
| Qwen2.5-0.5B-Instruct `model.safetensors` | `7ae557604adf67be50417f59c2c2f167def9a775` | 988,097,824 | `fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe` |
| SatSec seed-43 adapter | `c17f3c2f8a6da46e7ab138703a214d0df3f91e2d` | 35,237,104 | `7dfc14a58e5cb529ac73b110650a559cb58e3983921cb76ac598b84def746021` |
| SatSec seed-44 adapter | `c17f3c2f8a6da46e7ab138703a214d0df3f91e2d` | 35,237,104 | `a4d7c254a0cce0b7d4f92124a8bc5639db0d9c1d714b322298537f6192c74d19` |

Both adapter manifests name the exact Qwen revision above and have rank 16,
the same seven declared target modules, and distinct manifests/configurations.
The official base and adapter repository metadata both declare Apache-2.0.

## Decision

**GO for exact-base, two-adapter acquisition only.** This removes the previous
artifact-provenance blocker for these two seed variants. It does not activate a
paper line: there is still no real multi-adapter lifecycle/reuse trace, capacity
conflict, task-quality oracle, or tenant-isolation measurement.

## Conversion stop

Read-only g130 inspection found `convert_hf_to_gguf.py` and
`convert_lora_to_gguf.py`, but their imports fail because the isolated runtime
has neither `torch` nor `transformers`; the local Python environment lacks them
as well. No dependency, model, source, remote file, server, or GPU state was
modified. A separate explicit authorization is required to install those
libraries in a project-private environment and then freeze a conversion gate.
