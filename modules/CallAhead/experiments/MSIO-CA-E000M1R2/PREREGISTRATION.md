# MSIO-CA-E000M1R2 clean direct-CDN material gate

Status: frozen before execution. Date: 2026-09-05. Artifact identity and
thresholds are unchanged from E000M1.

## Frozen method

1. Confirm no user-owned `curl`, `scp` or task-specific SFTP process is writing
   a CallAhead E000M1 path. Do not signal unrelated sessions.
2. Require the new path
   `/mnt/nvme1/chenhao/modelstateio-runtime/incoming/.callahead-qwen2.5-1.5b-q4_k_m.gguf.r2.part`
   not to exist. Do not reuse the corrupted R1 file.
3. Resolve the exact pinned Hugging Face object locally and pass its signed
   official CDN URL to g130. Download from byte zero with one foreground
   `curl`; range resume is forbidden in R2.
4. Require exact size `1,117,320,736` and SHA-256
   `6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`.
5. Require the final path to be absent, then atomically rename the verified R2
   file to `qwen2.5-1.5b-instruct-q4_k_m.gguf` and repeat owner/size/hash checks.

## Decision and exclusions

`PASS` only on exact identity at the final path. Any writer, existing R2/final
path, size mismatch or digest mismatch stops the gate. This run does not
launch a model or establish performance. All E000M1 safety exclusions remain.

