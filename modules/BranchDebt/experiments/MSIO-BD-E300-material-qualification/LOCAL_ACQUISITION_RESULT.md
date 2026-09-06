# E300 local model acquisition result

Date: 2026-09-06. Evidence level: lawful artifact acquisition and local
identity only; no loadability, capacity or performance claim.

## Established observation

All 11 frozen GGUF shards were downloaded from the pinned official Qwen
revisions into `D:\Temp\ModelStateIO-BranchDebt-E300`. The final R4 acquisition
ended with `complete` after resuming the last shard from a preserved partial.

An independent second pass reopened every final file and recomputed its size
and SHA-256 against `MODEL_ACQUISITION.tsv`:

- verified rows: 11/11;
- total bytes: `36,933,341,696`;
- residual `.part` files: 0;
- mismatched size or digest: 0.

The per-file immutable identities remain in the frozen manifest. Raw download
progress and acquisition logs remain outside Git under `D:\Temp`.

## Transfer boundary

Both default SFTP-mode SCP and legacy SCP were tested within the global bounded
transfer rule. Each moved only a few MiB in several minutes and was stopped;
neither is a viable 36.9 GB transfer path. Their incomplete remote `.part`
files are not evidence and are ignored by the promotion script.

The required human action is a single Termius upload of the 11 final `.gguf`
files from the local directory above to:

`/mnt/nvme1/chenhao/modelstateio-runtime/incoming/models-e300/`

After upload, `verify_and_promote_models.sh` will independently verify all 11
files before any move, create the three router-compatible shard directories,
and refuse overwrite or mismatch. E300 remains incomplete until that remote
verification, model loadability, measured HBM conflict and the prospective
trace all pass.
