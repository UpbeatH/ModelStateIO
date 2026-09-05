# MSIO-SP-E008 converter dependency qualification on repaired Python

## Objective

Install and qualify the current llama.cpp HF/LoRA converter dependency tree
against the E007R2 private Python runtime.

## Frozen scope

- Interpreter: `python-runtime/statepatch-e007r2/prefix/bin/python3.10`.
- New package target: `python-libs/statepatch-e008`.
- Bootstrap pip only into the E007R2 private prefix from the official PyPA
  script; install `requirements-convert_lora_to_gguf.txt` as binary wheels,
  no cache, into the new target.
- Execute only the two converter `--help` commands with source `gguf-py`
  first in `PYTHONPATH`; no model conversion/load/server/GPU action.

## Pass rule

Both help commands exit zero, zero GPU allocation, and no converter/model
residue. Any failure is Technical No-Go for this ID.
