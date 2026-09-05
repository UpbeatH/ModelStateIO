# MSIO-SP-E200 online LoRA lifecycle result

Date: 2026-09-06. Status: **technical Go; research No-Go for the current
StatePatch candidate**.

## Established observation

- The exact committed runner at `e5fed1135db9860f323778000a35a23717221536`
  completed once on g130's private runtime root. It used the isolated CUDA
  11.6 library path, one loopback-only server, and the frozen five-request
  sequence.
- The base, both adapters, and server were SHA-256 recorded before use. The
  three base-only responses have the same content hash
  `7ee798ad4e2d5666bdbf4e001b8d8f73295dc4089101a16fe81f2305be181546`.
  Each enabled adapter produced the different hash
  `d8852d1b464ea18ffc3f02c27b079ba5ad338e4e41eacfa5d4b2fdae286fc92f`.
- The idle-only transition checks, HTTP ledger, and server cleanup completed.
  Post-run audit found no `llama-server` listener on port 18181 and GPU 0
  reported 0 MiB allocation. Raw receipts remain only at
  `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-SP-E200/`; they are not
  committed and have not been declared backed up.

## Inference and decision

E200 establishes that this llama.cpp build can perform a user-local,
idle-only online lifecycle with base restoration. It does **not** establish
per-request isolation, a correctness oracle, adapter diversity (the two
adapters had the same observed output for this prompt), capacity admission,
charged transition cost, or any performance result.

The material needed for a defensible successor is still absent: a
provenance-complete adapter reuse/lifecycle trace with finite state capacity
and a task-quality oracle. Creating one from this fixed prompt or relabelling
the server sequence would be synthetic evidence, not a systems workload.
Therefore the present StatePatch paper candidate remains **Research No-Go**.

## Re-entry condition

Only a newly obtained, lawful real trace meeting those fields can open a new
experiment ID. Its first gate must compare an online admission/eviction policy
against equal-information, equal-action and equal-runtime baselines while
charging transition work and measuring correctness plus tenant harm.
