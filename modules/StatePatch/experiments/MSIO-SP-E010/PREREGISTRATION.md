# MSIO-SP-E010 static adapter lifecycle contract

## Objective

Verify the minimal exact-artifact lifecycle contract with three isolated,
CPU-only CLI invocations: base-only, base plus seed-43 LoRA, then base-only
again after the attached invocation has exited.

## Frozen protocol

- Binary: existing isolated `llama-cli`; base and seed-43 GGUF identities from
  E009.
- All arms use the same fixed prompt, `--seed 123`, temperature zero, bounded
  token count, CPU-only layer setting, and per-arm timeout.
- Order is fixed `none -> attached -> none-after`; each arm launches a new
  process. The final arm verifies no persistent adapter state crosses process
  boundaries, not an in-process detach API.

## Pass rule

All three commands exit zero with bounded output and no residue. The first and
last base-only output byte hashes must match; the attached output must differ
from base-only. If the adapter has no observable effect or base output does not
restore, this exact static lifecycle contract is Technical No-Go.

## Boundary

This is not online attach/detach, task-quality, capacity, concurrency,
isolation, I/O, or performance evidence.
