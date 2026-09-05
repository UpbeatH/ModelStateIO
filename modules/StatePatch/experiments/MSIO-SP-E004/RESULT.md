# MSIO-SP-E004 result: private conversion-environment qualification

## Decision

**Technical No-Go for the frozen Python 3.8 environment.** The private
dependency installation succeeded, but the checked llama.cpp converter cannot
be imported by `/usr/bin/python3` 3.8.10. No model conversion, model load,
server, GPU use, or performance experiment was run.

## Established observations

- Target created: `/mnt/nvme1/chenhao/modelstateio-runtime/python-libs/statepatch-e004`
  (about 1.0 GB; user-owned private path).
- Installed there only: `torch 2.4.1+cpu`, `transformers 4.45.2`,
  `sentencepiece 0.2.0`, and their resolved dependencies. `torch` came from
  the PyTorch CPU index; the remaining packages came through the configured
  private pip resolution.
- `transformers 4.45.2` was selected because it supports Python >=3.8; the
  source requirement's `transformers 4.57.6` requires Python >=3.9.
- Importing `convert_hf_to_gguf.py --help` with the private `PYTHONPATH`
  failed before argument parsing in `conversion/base.py:63`:
  `TypeError: 'type' object is not subscriptable` at `dict[str, Any]`.
  This is a Python 3.8 language-level incompatibility, not a missing package.
- No `llama-cli`, `llama-server`, or converter process remained; `nvidia-smi`
  reported 0 MiB allocated.

## Evidence location

Raw installation and qualification logs, including package metadata hashes,
are outside Git at
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-SP-E004/`.

## Interpretation and boundary

The private-package isolation is feasible. The frozen existing-interpreter
conversion path is not. This result does not invalidate the exact base and
adapter artifacts, and it is not evidence about adapter conversion, lifecycle,
quality, storage cost, or system performance.

## Next gate

Do not patch the converter or use a global interpreter. A separate, explicitly
authorized E005 may audit whether an already-installed private Python >=3.9 is
available in the permitted runtime; otherwise it must freeze a user-local
runtime acquisition/build plan before any conversion attempt.
