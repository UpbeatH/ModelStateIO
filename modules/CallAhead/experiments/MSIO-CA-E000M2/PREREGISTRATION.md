# MSIO-CA-E000M2 independent-family material gate

Status: frozen before acquisition. Date: 2026-09-05.

## Frozen artifact

- Repository: `HuggingFaceTB/SmolLM2-1.7B-Instruct-GGUF`
- Revision: `2d4a76a30b4af41ecd395c35725ac11688d4cfe4`
- File: `smollm2-1.7b-instruct-q4_k_m.gguf`
- Official URL: <https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B-Instruct-GGUF/resolve/2d4a76a30b4af41ecd395c35725ac11688d4cfe4/smollm2-1.7b-instruct-q4_k_m.gguf>
- License: Apache-2.0, as declared by the official repository.
- Expected size: `1,055,609,536` bytes.
- Expected SHA-256 / linked object identifier:
  `decd2598bc2c8ed08c19adc3c8fdd461ee19ed5708679d1c54ef54a5a30d4f33`.

The identity fields were captured from the official pinned resolver before
download. This family differs from Qwen and prevents E000 from counting three
variants or copies of one base model.

## Frozen method and decision

Perform the same no-writer preflight and direct official-CDN, single-process,
byte-zero download used by E000M1R2, writing only
`incoming/.callahead-smollm2-1.7b-q4_k_m.gguf.part`. Require the final path to
be absent. Exact size and SHA-256 are mandatory before an atomic rename to
`incoming/smollm2-1.7b-instruct-q4_k_m.gguf`, followed by a second identity and
owner check.

`PASS` requires exact identity. Any concurrent writer, existing conflicting
path, size/hash mismatch or license/revision inconsistency stops the gate.
Do not install, launch a model/server, change cache/system/CUDA/driver/service,
touch g129/PFS/Lustre or access other users. This is acquisition evidence only.

