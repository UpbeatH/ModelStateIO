# MSIO-SP-E003 exact-base multi-adapter acquisition gate

## Objective

Qualify a lawful, provenance-complete material set for a later multi-adapter
StatePatch gate. This gate is acquisition and identity verification only; it
does not convert, attach, serve, score prompts, create an artificial lifecycle
trace, or measure performance.

## Frozen sources

- Base: `Qwen/Qwen2.5-0.5B-Instruct` at revision
  `7ae557604adf67be50417f59c2c2f167def9a775`, Apache-2.0.
- Adapters: `paolocmo/satsec-decomposition-qwen2.5-0.5b-adapters` at revision
  `c17f3c2f8a6da46e7ab138703a214d0df3f91e2d`, Apache-2.0; variants
  `training-seeds/seed-43` and `training-seeds/seed-44`.

## Pass rule

PASS requires the exact base revision named in both adapter manifests, two
distinct adapter tensor digests, Apache-2.0 source metadata, complete byte
downloads, and local SHA-256 agreement with each LFS pointer. Any mismatch is
an artifact No-Go. Raw files remain outside Git.

## Boundary

Even a PASS does not establish a lifecycle trace, a capacity conflict, task
quality, adapter isolation, conversion compatibility, or a CCF-B mechanism.
Any conversion needs a separately authorized private dependency environment.
