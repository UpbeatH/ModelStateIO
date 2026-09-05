# MSIO-SP-E010 result: CLI argument integration failure

## Decision

**Technical No-Go; no model arm executed.** The frozen shell wrapper expanded
the prompt into separate arguments and `llama-cli` stopped on `invalid
argument: one` before model loading. E010 is closed and must not be rerun.

## Boundary

No output contract, adapter effect, lifecycle observation, or performance
result was obtained. At postflight, an unrelated existing GPU allocation of
14738 MiB was observed; no process was altered. A new E010R1 may change only
argument quoting and must retain CPU-only `-ngl 0` execution.
