# MSIO-SP-E006 converter-subset qualification on private Python 3.10

## Objective

Qualify only the actual HF and LoRA converter import paths under the E005
private Python 3.10 runtime. This is deliberately narrower than E005's failed
complete-standard-library criterion; `sqlite3` remains unavailable and is not
used as a pass criterion here.

## Frozen scope

- Interpreter: only
  `/mnt/nvme1/chenhao/modelstateio-runtime/python-runtime/statepatch-e005/prefix/bin/python3.10`.
- Package target:
  `/mnt/nvme1/chenhao/modelstateio-runtime/python-libs/statepatch-e006`.
- Bootstrap pip from official PyPA HTTPS only, record URL/bytes/SHA-256; install
  the current llama.cpp `requirements-convert_lora_to_gguf.txt` dependency tree
  into the package target using binary wheels and no cache.
- Use the source-tree `gguf-py` first on `PYTHONPATH`. No source editing,
  model conversion, model/server launch, GPU use, system package manager,
  `sudo`, global path, or access outside the permitted private runtime.

## Pass rule

PASS requires a zero-exit import/help execution for both
`convert_hf_to_gguf.py --help` and `convert_lora_to_gguf.py --help` under the
frozen private interpreter and paths, plus no llama/converter residue and 0 MiB
GPU use. Failed dependency resolution, an import failure, or a scope violation
is Technical No-Go for conversion; it does not justify changing the converter
or system environment.

## Boundary

This gate does not convert the acquired base or adapters. It is only an
environment qualification for a later, independently frozen conversion gate.
