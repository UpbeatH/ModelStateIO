# MSIO-SP-E002: wider-target public adapter compatibility gate

Status: frozen before execution.

## Purpose

Test only whether a second public Qwen2.5-0.5B-Instruct LoRA configuration
(rank 16; Q/K/V/O plus gate/up/down targets) can be converted and controlled
by the same user-local runtime.  It is a compatibility gate, not a benchmark.

## Fixed source material

- Public adapter family: `paolocmo/satsec-decomposition-qwen2.5-0.5b-adapters`,
  Apache-2.0.
- Variant: `training-seeds/seed-43`.
- Tensor file size: 35,237,104 bytes; SHA-256
  `7dfc14a58e5cb529ac73b110650a559cb58e3983921cb76ac598b84def746021`.
- Configuration SHA-256:
  `e7729540a95f5514da4e8ff150b035a3b06382b6b2f118215e96ad6d719464c7`.
- The source manifest declares base revision
  `7ae557604adf67be50417f59c2c2f167def9a775`.  The available Q4 GGUF lacks a
  verifiable source revision.  Therefore E002 cannot make a model-quality or
  provenance-equivalence claim even if the runtime accepts it.

## Stop rules

Reject on any mismatch in base name, 24-layer topology, rank-16 target tensor
names, shapes, dtypes, or an inability to set scale 0 then 1 then 0.  Do not
compare latency, quality, or reuse with E001R1; they use distinct adapters and
the base revision relationship is unverified.
