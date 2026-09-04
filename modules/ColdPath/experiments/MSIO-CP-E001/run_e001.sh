#!/usr/bin/env bash
set -euo pipefail

out_dir="${1:?external output directory required}"
mkdir -p "$out_dir"
results="$out_dir/results.jsonl"
ledger="$out_dir/command-ledger.txt"
: > "$results"
: > "$ledger"

record() {
  printf '%s\t%s\n' "$(date -Iseconds)" "$*" | tee -a "$ledger"
}

unload() {
  record "POST unload qwen2.5:14b"
  curl --fail --silent --show-error --max-time 60 \
    http://127.0.0.1:11434/api/generate \
    -H 'Content-Type: application/json' \
    -d '{"model":"qwen2.5:14b","keep_alive":0}' >/dev/null
  for _ in $(seq 1 30); do
    if ! ollama ps | grep -q 'qwen2.5:14b'; then
      return 0
    fi
    sleep 1
  done
  record "FAIL model remained resident"
  return 1
}

request() {
  local rep="$1"
  local state="$2"
  local response="$out_dir/rep-${rep}-${state}.json"
  record "POST rep=$rep state=$state"
  curl --fail --silent --show-error --max-time 300 \
    http://127.0.0.1:11434/api/generate \
    -H 'Content-Type: application/json' \
    -d '{"model":"qwen2.5:14b","prompt":"Return one token.","stream":false,"keep_alive":"10m","options":{"temperature":0,"num_predict":1,"seed":20260904}}' \
    > "$response"
  jq -c -e --argjson rep "$rep" --arg state "$state" \
    '{rep:$rep,state:$state,done,done_reason,response,load_duration,total_duration,prompt_eval_duration,eval_duration,prompt_eval_count,eval_count} | select(.done == true) | select(.load_duration|numbers) | select(.total_duration|numbers)' \
    "$response" >> "$results"
}

record "BEGIN host=$(hostname) model=qwen2.5:14b"
nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv,noheader,nounits | tee "$out_dir/gpu-pre.txt"
ollama --version | tee "$out_dir/ollama-version.txt"
ollama show qwen2.5:14b | tee "$out_dir/model-show.txt"

for rep in $(seq 1 5); do
  unload
  request "$rep" cold
  request "$rep" warm
done

unload
ollama ps | tee "$out_dir/ollama-ps-post.txt"
nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv,noheader,nounits | tee "$out_dir/gpu-post.txt"
sha256sum "$results" "$ledger" "$out_dir"/rep-*.json > "$out_dir/SHA256SUMS"
record "END valid_rows=$(wc -l < "$results")"
