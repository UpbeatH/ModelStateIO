# MSIO-SP-E004 private conversion-environment qualification

## Objective

Install only the minimum Python dependencies needed by the existing isolated
llama.cpp conversion scripts, into a new user-owned private directory. Then
verify imports and conversion-script help without converting a model, starting
a server, or using a GPU.

## Scope and isolation

- Target: `g130-chenhao:/mnt/nvme1/chenhao/modelstateio-runtime/python-libs/statepatch-e004`.
- Python: the existing `/usr/bin/python3` only. No `sudo`, system site-packages,
  global CUDA, driver, service, cache, Lustre/PFS, or g129 changes.
- Candidate packages and versions are selected only after read-only inspection
  of converter imports and Python compatibility. Installation must use
  `python3 -m pip --target` and must record resolved versions plus wheel/source
  hashes outside Git.

## Pass rule

PASS requires a fresh private directory; successful imports for every actual
converter dependency; `convert_hf_to_gguf.py --help` and
`convert_lora_to_gguf.py --help` exiting zero under a private `PYTHONPATH`; no
active model/server process, zero GPU allocation, and no changes outside the
private directory.  Any failed dependency resolution or scope violation is
Technical No-Go and no conversion follows.

## Boundary

This is environment feasibility only.  It does not authorize model conversion,
file transfer, adapter attachment, lifecycle workload, capacity experiment, or
performance claim.  Raw pip logs and wheels remain outside Git.
