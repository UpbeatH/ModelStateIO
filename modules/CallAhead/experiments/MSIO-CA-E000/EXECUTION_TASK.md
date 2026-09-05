# MSIO-CA-E000 read-only execution task

## 1. Identity and authority

- Task ID: `MSIO-CA-E000-A0`
- Module: `ModelStateIO/modules/CallAhead`
- Local repository: `D:\Workspace\Working\Working\Research\ModelStateIO`
- Control/target host: `g130-chenhao`
- Allowed remote root: `/mnt/nvme1/chenhao/modelstateio-runtime`
- Authorized operation: read-only inspection for the user-authorized CallAhead
  validation goal.
- Excluded: g129, PFS/Lustre, other hosts, other users, downloads, installs,
  model/server launch, cache manipulation, source edits and process signals.

## 2. Research boundary

- Question: can the current material and runtime support a later E001 protocol?
- Pass/blocked/No-Go rules: exactly those in `PREREGISTRATION.md`.
- Evidence ceiling: material and capability qualification only.

## 3. Frozen audit commands

Run the commands below through the configured SSH alias. A missing command or
path is recorded as an observation; it is not repaired during A0.

```bash
set -eu
ROOT=/mnt/nvme1/chenhao/modelstateio-runtime
printf 'TIME='; date -u +%Y-%m-%dT%H:%M:%SZ
printf 'HOST='; hostname
id
test -d "$ROOT"
stat -c 'ROOT owner=%U group=%G mode=%a path=%n' "$ROOT"
df -B1 "$ROOT"
nvidia-smi --query-gpu=index,name,uuid,memory.total,memory.used,utilization.gpu --format=csv,noheader
ps -u "$(id -u)" -o pid=,etimes=,comm=,args= | grep -E 'llama|ollama|modelstate|prefetch' || true
find "$ROOT" -maxdepth 2 -type f -printf '%s\t%TY-%Tm-%TdT%TH:%TM:%TS\t%p\n' | sort
find "$ROOT" -maxdepth 3 -type d -printf '%p\n' | sort
command -v python3 || true
command -v gcc || true
command -v fio || true
command -v stress-ng || true
command -v taskset || true
command -v ionice || true
command -v systemd-run || true
command -v cgexec || true
find "$ROOT" -maxdepth 4 -type f \( -name 'llama-server' -o -name 'llama-cli' \) -printf '%s\t%p\n' | sort
find "$ROOT" -maxdepth 4 -type d -name .git -printf '%h\n' | sort
```

Do not hash GGUF files in A0 because a multi-gigabyte read would itself alter
page-cache residency. Compare path and size with prior hash-pinned receipts;
full rehash belongs to a later controlled material subgate.

## 4. Stops and postflight

Stop on target-host mismatch, root ownership ambiguity, path escape, active
unknown model workload, or any command that would require elevated privilege.
No cleanup is expected because A0 creates no remote file or process. Re-run the
GPU/process queries at the end to prove that inspection launched nothing.

## 5. Required result

Record command outputs, missing tools/paths, current model count and identity
status, router/source location, safety blockers and a decision against all five
requirements. Do not propose or run E001 unless E000 reaches PASS.
