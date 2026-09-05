# MSIO-SP-E006R1 converter-subset bootstrap correction

## Objective

Repeat only the unexecuted converter-dependency qualification from E006 after
read-only verification that the official PyPA endpoint
`https://bootstrap.pypa.io/get-pip.py` returns HTTPS 200. E006 remains closed.

## Frozen scope

- Reuse only the E005 private Python 3.10 executable.
- New package target:
  `/mnt/nvme1/chenhao/modelstateio-runtime/python-libs/statepatch-e006r1`.
- Download the verified official PyPA script, record its URL/bytes/SHA-256,
  bootstrap pip into the E005 private prefix, then install the current
  llama.cpp `requirements-convert_lora_to_gguf.txt` dependency tree as binary
  wheels into the new target with no cache.
- Run only both converter `--help` paths under source `gguf-py` plus the new
  target. No model conversion, model/server launch, GPU use, source edit,
  `sudo`, system package manager, global environment, or other-user path.

## Pass rule

Both help commands must exit zero, with no residual llama/converter process
and 0 MiB GPU allocation. Any bootstrap, install, import, or scope failure is
Technical No-Go for this new ID.
