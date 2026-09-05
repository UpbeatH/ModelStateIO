# MSIO-SP-E001R1 result

Status: **GO (technical lifecycle qualification only)**.

## Established observations

- The repaired adapter-only GGUF has SHA-256
  `47c8ee49846d2c6b4037a832b936dc84876fd9cf14b2c69df8668d0dc7c1cb96`.
- The fixed base GGUF retains SHA-256
  `74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db`.
- A loopback-only private server loaded the adapter with its initial global
  scale set to 1.0.  All three control requests returned `success:true`.
- Under the frozen deterministic completion request, disabled state 1 and
  disabled state 2 produced the same content SHA-256
  `18a705ab970c574cf55255e419494505d12933434af83af3ac3640b9c33618c6`;
  enabled state produced
  `3b65430e130ac348f6aa23a5d7152a871181adf3cea9b0ed3a93a3e57f21d364`.
- The final adapter endpoint reported scale 0.0, and the server's own cleanup
  completed.  No E001R1 server process remained when checked after the run.

Raw receipts remain outside Git at
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-SP-E001R1/20260905T094819+0800/`.
The result JSON is 369 bytes and the runtime binary SHA-256 is
`4a141eb5995d1a192cb544d89b68cef71d85e092b98d7026dbba0da08f22d15f`.

## Bounded inference

For this one exact base/adapter pair, the user-local runtime supports a
reversible global LoRA scale lifecycle.  This does **not** show adapter
isolation, multi-tenant safety, model quality, loading cost, storage benefit,
or a controller advantage.  The run used a single slot; its request-cache
behavior must not be used as a performance measurement.

## Next gate

Do not launch an optimization matrix.  First obtain a provenance-complete
lifecycle trace that identifies more than one adapter or version and exposes a
real capacity conflict.  Without it, StatePatch remains a technical component,
not a CCF-B paper line.
