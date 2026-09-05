# MSIO-CP-E030 ArrivalSplit source-capability audit result

## Established observations

Read-only inspection of g130's isolated llama.cpp source found
`server_context::impl::load_model` as one path described in source as "load the
model and initialize llama_context".  That path obtains the target model and
context together before later server-state use.  The core loader calls
`model->load_tensors(...)` before the model is returned.  The server's public
help exposes model paths/load modes and router options, but no documented hook
to begin exact-model preparation at request admission and synchronize it with a
separately measurable non-I/O initialization phase.

The server router does contain queue and LRU paths for `--models-dir` and
`--models-max`; this is a different multi-model admission mechanism, not the
proposed within-load split.  The inspected binary SHA-256 is
`4a141eb5995d1a192cb544d89b68cef71d85e092b98d7026dbba0da08f22d15f`.

## Decision

**NO-GO for ArrivalSplit on the unmodified runtime.** An external concurrent
read would not establish a request-integrated, separable loading mechanism and
would duplicate the bounded overlap already observed in E025/E026R1.  No model
was launched, no source was modified, and no performance result was generated.

## Narrow follow-up

The router's documented queue/LRU implementation supports a separate
`QueueAwareWarm` capability audit, but only if two provenance-auditable local
model states and an admission workload can be identified. It must not reuse
this result as evidence of performance or novelty.
