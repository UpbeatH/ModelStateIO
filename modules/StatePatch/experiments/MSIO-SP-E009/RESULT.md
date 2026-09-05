# MSIO-SP-E009 result: exact-artifact conversion

## Decision

**Technical GO for exact base plus two-adapter conversion.** All transferred
artifacts match E003 byte/hash identities, both manifests name revision
`7ae557604adf67be50417f59c2c2f167def9a775` with rank 16 and the seven declared
target modules, and all three GGUF conversions completed.

## Outputs

- Base BF16 GGUF: 994156896 bytes,
  `ef326c3564da9222293f3548f075f4f6adaf08f8d5315512c45f385bf04f2528`.
- Seed-43 LoRA BF16 GGUF: 17619584 bytes,
  `3e20776262aadb231173b345aa9afb1500f766d5502fcc00deef9a54817e8aa6`.
- Seed-44 LoRA BF16 GGUF: 17619584 bytes,
  `72a3c438c18a350db39efd2bb9925c03d61a93eec7675867defc0a623b5638b5`.

Raw command logs and output checksums remain outside Git under
`modelstateio-runtime/logs/MSIO-SP-E009/`. Conversion used CPU only; GPU use
remained 0 MiB. This is not adapter-effect, lifecycle, quality, capacity,
isolation, or performance evidence.
