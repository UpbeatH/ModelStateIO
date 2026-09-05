# MSIO-SP-E009 exact-artifact transfer and conversion

## Objective

Transfer the E003 exact Qwen base and two declared SatSec adapters to an
isolated g130 private input root, independently verify their identities, then
convert the base and both adapters to runtime GGUF forms.

## Frozen inputs

- Base `model.safetensors`: 988097824 bytes, SHA-256
  `fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe`.
- Seed-43 adapter: 35237104 bytes, SHA-256
  `7dfc14a58e5cb529ac73b110650a559cb58e3983921cb76ac598b84def746021`.
- Seed-44 adapter: 35237104 bytes, SHA-256
  `a4d7c254a0cce0b7d4f92124a8bc5639db0d9c1d714b322298537f6192c74d19`.
- Converter: E007R2 private Python plus E008 private packages and existing
  llama.cpp source only.

## Pass rule

All three remote byte/hash checks and two adapter manifests must match their
declared base/rank/target-module identities. Conversion must exit zero and
yield non-empty GGUF files, with no model/server process or GPU allocation.

## Boundary

This gate performs format conversion only. It does not load a model, establish
adapter effect, quality, capacity, isolation, lifecycle behavior, or a paper
claim.
