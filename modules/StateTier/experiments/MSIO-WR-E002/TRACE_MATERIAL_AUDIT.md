# MSIO-WR-E002: public request-trace material audit

Status: **No-Go for WeightResidency re-entry on this trace alone**.

## Verified artifact

The legally public, anonymized Qwen trace was acquired outside Git at
`C:\Temp\ModelStateIO-acquire\2026-09-05\qwen-trace\qwen_traceA_blksz_16.jsonl`.
It is 56,354,493 bytes with SHA-256
`07cedc9ed8aff301994ac68ed4aede8123b7603673575eeba9dd677de663db17`.

One full pass found 43,058 records and 43,058 chat identifiers.  The only
record fields are `chat_id`, `parent_chat_id`, `timestamp`, `input_length`,
`output_length`, `type`, `turn`, and `hash_ids`.  It has 2,530,337 unique block
identifiers, of which 1,184,783 recur; the maximum observed block reuse count
is 21,972.  It therefore supports a bounded trace study of timing and block
reuse, not an invented workload.

## Why it does not reopen WeightResidency

There is no model, base-version, adapter-version, weight size, residency,
capacity, admission, eviction, or load-completion field.  A multi-model weight
controller would have to assign these fields synthetically after observing the
trace.  That would not demonstrate a real model-residency conflict, and would
not meet the earlier re-entry condition of a provenance-complete multi-model
request corpus.

## Decision

Do not use this trace to run or tune a WeightResidency controller.  It is
retained only as a possible future workload component after a separately
obtained trace identifies at least three traceable model or adapter identities,
their effective sizes, and request-to-state association.  This decision leaves
the prior WeightResidency scope No-Go in force.
