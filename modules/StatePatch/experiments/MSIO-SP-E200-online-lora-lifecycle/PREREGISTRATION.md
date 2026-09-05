# MSIO-SP-E200 online LoRA lifecycle qualification

Status: frozen local protocol; execution requires a separately authorized
target-native commit/push and a fresh g130 audit. This is a technical
qualification, not a CCF-B performance claim.

## Question

Can the existing isolated llama.cpp server expose a repeatable, user-local
online adapter lifecycle for two provenance-recorded LoRA adapters, with a
base-only restoration check and no residual GPU/server process?

## Established preflight evidence

- g130 private runtime contains `llama-server` and `llama-cli` in
  `build-d230ddd-cuda116-sm70/bin/`.
- `llama-server --help` advertises `--lora-init-without-apply` and later
  application through `POST /lora-adapters`.
- Two distinct SatSec adapter GGUF files are present under the private
  `statepatch-e009-output/` root; each is 17,619,584 bytes.
- Upstream llama.cpp documents `GET/POST /lora-adapters`; upstream also warns
  that global hot-swap is safe only when slots are idle. E200 therefore uses
  serial, idle-only transitions and claims neither multi-tenant concurrency nor
  per-request isolation.

## Frozen action and observation space

1. Verify exact base/adapters by path, size and SHA-256; verify private CUDA
   11.6 dynamic-library use and zero initial GPU allocation.
2. Start one user-local server with both adapters loaded at scale zero.
3. Perform the fixed sequence: base request; apply adapter A; same request;
   disable A; same request; apply adapter B; same request; disable B; same
   request. Each transition is permitted only after the server reports no
   active request/slot.
4. Record every HTTP request/response, server log, return code, adapter list,
   process/GPU readback and final cleanup receipt.

## Technical Go

All identity and cleanup checks pass; every transition returns success; the
base-only outputs before/after each disable are byte-identical under fixed
decoding; each adapter has a reproducible distinguishable output on its
predeclared prompt; and no request is active during a global adapter change.

## Stop conditions

Any identity mismatch, adapter API absence, server failure, active-request
transition, base-restoration failure, adapter non-effect, residual process/GPU
allocation, global/system mutation, or missing ledger is a technical No-Go.
No retry, load increase, concurrent-tenant trial, capacity claim or performance
metric is allowed in E200.

## Research boundary

Passing E200 only establishes an online lifecycle capability. A paper candidate
would still require a real adapter reuse trace, capacity conflict, correctness
oracle, equal-budget baseline, charged transition cost and tenant-isolation
evidence in a separately frozen successor.
