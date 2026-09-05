# LayerReadyIO current-runtime source gate

Status: **No-Go on the unmodified runtime**.

## Current source evidence

The checked private llama.cpp revision calls `common_init_from_params` in
`tools/server/server-context.cpp` before assigning `model_tgt` and `ctx_tgt`.
The model construction path calls `model->load_tensors(ml)` in `src/llama.cpp`.
Only after model/context construction succeeds does the server enter `init()`;
the top-level server sets HTTP readiness after `ctx_server.load_model(params)`
returns and logs `model loaded`.

Thus the existing progress callback is load progress, not a contract allowing
a request to execute against a prefix of loaded layers.  No current endpoint
exposes a layer-ready model state.

## Decision

Do not claim or benchmark layer-ready service using a wrapper around the
unmodified binary.  A future re-entry needs a source-level staged-loader
implementation, tensor-use/dependency instrumentation, correctness conditions
for a partial model, and a baseline that charges all deferred work.  That is a
new systems implementation project, not a parameter choice or a small
extension of the current loader.
