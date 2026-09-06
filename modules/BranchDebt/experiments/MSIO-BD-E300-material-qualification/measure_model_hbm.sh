#!/usr/bin/env bash
set -euo pipefail

token=${1:-}
alias_name=${2:-}
if [[ "$token" != "MEASURE-MSIO-BD-E300" ]]; then
  echo "authorization token mismatch" >&2
  exit 64
fi

runtime=/mnt/nvme1/chenhao/modelstateio-runtime
model_dir="$runtime/models/branchdebt-e300"
output_dir="$runtime/experiments/MSIO-BD-E300/capacity"
server="$runtime/build-d230ddd-cuda116-sm70/bin/llama-server"
manifest=${MODEL_MANIFEST:-}
case "$alias_name" in
  qwen2.5-7b-instruct-q4_k_m)
    manifest_model=Qwen2.5-7B-Instruct-Q4_K_M
    first=qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf
    port=18107 ;;
  qwen2.5-14b-instruct-q4_k_m)
    manifest_model=Qwen2.5-14B-Instruct-Q4_K_M
    first=qwen2.5-14b-instruct-q4_k_m-00001-of-00003.gguf
    port=18114 ;;
  qwen2.5-32b-instruct-q5_k_m)
    manifest_model=Qwen2.5-32B-Instruct-Q5_K_M
    first=qwen2.5-32b-instruct-q5_k_m-00001-of-00006.gguf
    port=18132 ;;
  *) echo "unknown frozen model alias" >&2; exit 64 ;;
esac

[[ -n "$manifest" && -f "$manifest" ]] || { echo "MODEL_MANIFEST is required" >&2; exit 66; }
[[ -x "$server" ]] || { echo "missing frozen llama-server" >&2; exit 66; }
mkdir -p "$output_dir"
lock="$output_dir/.measure.lock"
exec 9>"$lock"
flock -n 9 || { echo "capacity measurement already active" >&2; exit 75; }

if nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | grep -q '[0-9]'; then
  echo "GPU has an existing compute process; technical stop" >&2
  exit 75
fi
if ldd "$server" | grep -q 'not found'; then
  echo "llama-server has unresolved libraries" >&2
  exit 66
fi

count=0
while IFS=$'\t' read -r model revision file bytes sha; do
  [[ "$model" == "$manifest_model" ]] || continue
  path="$model_dir/$file"
  [[ -f "$path" ]] || { echo "missing shard: $path" >&2; exit 66; }
  [[ $(stat -c %s "$path") == "$bytes" ]] || { echo "size mismatch: $path" >&2; exit 65; }
  [[ $(sha256sum "$path" | awk '{print $1}') == "$sha" ]] || { echo "hash mismatch: $path" >&2; exit 65; }
  count=$((count + 1))
done < <(tail -n +2 "$manifest")
[[ $count -gt 0 ]] || { echo "no manifest rows for $manifest_model" >&2; exit 65; }

stamp=$(date -u +%Y%m%dT%H%M%SZ)
log="$output_dir/${alias_name}-${stamp}.log"
samples="$output_dir/${alias_name}-${stamp}-hbm.tsv"
receipt="$output_dir/${alias_name}-${stamp}.json"
pid=''
cleanup() {
  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    kill -TERM "$pid" 2>/dev/null || true
    for _ in $(seq 1 50); do kill -0 "$pid" 2>/dev/null || break; sleep 0.1; done
    kill -KILL "$pid" 2>/dev/null || true
    wait "$pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

total_mib=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1 | tr -d ' ')
start_ns=$(date +%s%N)
CUDA_VISIBLE_DEVICES=0 LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64 \
  "$server" -m "$model_dir/$first" -c 4096 -ngl 999 --no-warmup \
  --host 127.0.0.1 --port "$port" >"$log" 2>&1 &
pid=$!

ready=0
for _ in $(seq 1 1200); do
  kill -0 "$pid" 2>/dev/null || break
  used=$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits 2>/dev/null \
    | awk -F, -v p="$pid" '$1+0==p {gsub(/ /,"",$2); print $2}')
  [[ -n "$used" ]] && printf '%s\t%s\n' "$(date +%s%N)" "$used" >>"$samples"
  if curl --fail --silent --max-time 1 "http://127.0.0.1:$port/health" >/dev/null 2>&1; then
    ready=1
    break
  fi
  sleep 0.25
done
[[ $ready == 1 ]] || { echo "server did not become healthy" >&2; exit 70; }
for _ in $(seq 1 50); do
  used=$(nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader,nounits 2>/dev/null \
    | awk -F, -v p="$pid" '$1+0==p {gsub(/ /,"",$2); print $2}')
  [[ -n "$used" ]] && printf '%s\t%s\n' "$(date +%s%N)" "$used" >>"$samples"
  sleep 0.1
done
peak_mib=$(awk 'BEGIN{m=0} $2>m{m=$2} END{print m}' "$samples")
ready_ns=$(date +%s%N)
python3 - "$receipt" "$alias_name" "$pid" "$total_mib" "$peak_mib" "$start_ns" "$ready_ns" "$first" <<'PY'
import json, sys
path, alias_name, pid, total, peak, start, ready, first = sys.argv[1:]
record = {
    "schema_version": "1.0",
    "experiment_id": "MSIO-BD-E300",
    "model_alias": alias_name,
    "server_pid": int(pid),
    "gpu_total_mib": int(total),
    "peak_model_hbm_mib": int(peak),
    "load_to_health_ms": (int(ready) - int(start)) / 1000000.0,
    "first_shard": first,
    "context_size": 4096,
    "gpu_layers": 999,
    "evidence_level": "technical per-model loadability and HBM measurement"
}
with open(path, "w") as stream:
    json.dump(record, stream, indent=2, sort_keys=True)
    stream.write("\n")
PY
cat "$receipt"
