# MSIO-SP-E200 execution task

Packet status: local draft; do not execute until the packet is committed,
pushed and the selected g130 executor verifies the exact clean revision.

## Authority and boundary

- Target: `g130-chenhao`, only `/mnt/nvme1/chenhao/modelstateio-runtime/`.
- External root: `/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-SP-E200/`.
- Allowed mutation: create that absent owned result root; start one
  loopback-only `llama-server`; send the eight frozen HTTP calls; remove only
  the owned root on a failed pre-start. Preserve it after any server start.
- Forbidden: g129, Lustre/PFS, global cache clearing, system CUDA/driver/
  service changes, installation, model download, other-user paths, concurrent
  request generation, capacity-pressure tests and retries.

## Fresh preflight

1. Verify no `llama-server`/`llama-cli` owned by this task is running and GPU
   0 has no memory allocation attributable to this task.
2. Verify free space, private CUDA 11.6 library visibility, `llama-server`
   executable identity, the BF16 Qwen base and both SatSec adapter identities
   (path, size, SHA-256).
3. Verify `llama-server --help` contains `--lora-init-without-apply` and the
   server returns a parseable `GET /lora-adapters` result before any request.
4. Stop before result-root creation on any mismatch, active server, GPU use,
   occupied loopback port or missing field.

## Frozen run

Start exactly one server bound to `127.0.0.1` with the Qwen BF16 base, both
adapter GGUF files, `--lora-init-without-apply`, private
`LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64`, deterministic decoding and an
explicit timeout. The only state sequence is:

1. base prompt;
2. POST adapter A scale 1 then prompt;
3. POST adapter A scale 0 then prompt;
4. POST adapter B scale 1 then prompt;
5. POST adapter B scale 0 then prompt.

Before every POST and prompt, query server state/slots and stop if any slot is
active. Record request/response bodies, status codes, timestamps, adapter lists,
server log, GPU readbacks, process tree, command ledger and SHA-256 inventory.
The prompts, seed, token bound, temperature and endpoint grammar must be
checked against the current binary help/API before launch and written to the
commit-bound runner; they may not be improvised during execution.

## Decision and cleanup

Technical Go requires success for every identity/API/idle/HTTP/cleanup check,
byte-identical base outputs across the three base arms, a deterministic output
difference for each adapter's predeclared prompt, and zero residual server/GPU
allocation. Any other outcome is a one-shot technical No-Go. Either outcome
remains online-lifecycle capability only: it does not establish capacity,
isolation, performance, a controller or a paper claim.
