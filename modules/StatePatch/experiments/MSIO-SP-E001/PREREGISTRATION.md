# MSIO-SP-E001: provenance and reversible LoRA lifecycle gate

Status: frozen before execution.

## Objective

Qualify only whether an exact, externally published LoRA adapter can be
converted and reversibly controlled against the already verified local Qwen
GGUF base.  This is neither a latency experiment nor a model-quality claim.

## Fixed inputs

- Base: `Qwen2.5-0.5B-Instruct` Q4_K_M GGUF, SHA-256
  `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`.
- Adapter configuration: `adapter_config.json`, SHA-256
  `d2ed6f1499f53ddf1885bf046db3ef5ce570aadd1109f1b3c259c1a7594ff921`.
- Adapter tensors: `adapter_model.safetensors`, SHA-256
  `6cf3bfc966172a31875a8121176b28dccac992de460282f350ac080afffa7a8c`.
- Runtime: private CUDA-11.6 llama.cpp build on g130; no global CUDA, driver,
  service, cache, Lustre, or PFS changes are allowed.

## Procedure

1. Read the adapter config and tensor metadata using a project-private Python
   dependency directory.  Abort on any base/rank/shape/name mismatch.
2. Produce a new adapter-only GGUF in the project-private runtime directory;
   hash it and record the mapping.
3. Start a loopback-only server with the immutable base and adapter loaded but
   initially disabled.  Under one fixed prompt and deterministic decoding,
   capture bounded responses for: disabled, enabled at scale 1, disabled
   again.  Cap each request and server lifetime; remove only the process this
   task started.
4. Pass only if the control endpoint acknowledges all three states, the two
   disabled observations agree byte-for-byte, and the enabled observation is
   observably different.  A mismatch, timeout, nonzero exit, or residual
   process is No-Go for this gate.

## What will be measured

Artifact checksums, tensor mapping, endpoint acknowledgements, response
hashes, process cleanup, and fixed-state correctness.  No throughput,
latency, energy, or storage benefit is measured or claimed.

## Decision rule

`GO (technical)` requires every frozen check.  Otherwise record `NO-GO` with
the first failing condition and do not change thresholds or repeat until a new
protocol explicitly addresses that failure.
