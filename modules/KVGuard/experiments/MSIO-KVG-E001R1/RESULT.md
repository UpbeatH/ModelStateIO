# MSIO-KVG-E001R1 result

## Established observation

The isolated `llama-server` target built after disabling only the unrelated
prebuilt-UI download path. One loopback slot-state round trip then completed:
slot 1 saved 9 tokens and 111,356 bytes in 0.627 ms; slot 0 restored 9 tokens
and 111,356 bytes in 0.474 ms. The deterministic continuation content matched
exactly on the original and restored slots (`No further action`). The raw
receipt SHA-256 is
`253f39db75ed34b02c8ce7c15aff3e8112812e4ecc73618f1342a3255a83b27b` at
`/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-KVG-E001R1/`.

The post-run audit found zero `llama-server` processes and 0 MiB GPU use.

## Decision

**GO: KV state lifecycle capability.** This proves only that the isolated
runtime can safely save and restore one owned sequence state with exact
continuation equivalence. It is not evidence for a policy, latency improvement,
capacity benefit, cancellation safety, multi-tenant behavior or paper novelty.

## Next falsification gate

E002 must establish a real action reversal: under the same model and explicit
state-size budget, a short context must prefer recomputation while a longer
context prefers save/restore, relative to equal-information always-recompute
and always-save baselines. If no reversal exists, stop KVGuard.
