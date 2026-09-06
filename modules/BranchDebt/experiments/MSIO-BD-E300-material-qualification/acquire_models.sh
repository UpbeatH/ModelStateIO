#!/usr/bin/env bash
set -euo pipefail

token=${1:-}
target=${2:-}
manifest=${3:-}
expected_target=/mnt/nvme1/chenhao/modelstateio-runtime/branchdebt-e300-models

if [[ "$token" != "ACQUIRE-MSIO-BD-E300" ]]; then
  echo "authorization token mismatch" >&2
  exit 2
fi
if [[ "$target" != "$expected_target" ]]; then
  echo "target must equal $expected_target" >&2
  exit 2
fi
if [[ ! -f "$manifest" ]]; then
  echo "missing manifest: $manifest" >&2
  exit 2
fi

mkdir -p "$target"
exec 9>"$target/.acquire.lock"
flock -n 9 || { echo "another acquisition is active" >&2; exit 3; }

tail -n +2 "$manifest" | while IFS=$'\t' read -r model revision file bytes digest; do
  case "$model" in
    Qwen2.5-7B-*) repo=Qwen/Qwen2.5-7B-Instruct-GGUF ;;
    Qwen2.5-14B-*) repo=Qwen/Qwen2.5-14B-Instruct-GGUF ;;
    Qwen2.5-32B-*) repo=Qwen/Qwen2.5-32B-Instruct-GGUF ;;
    *) echo "unexpected model: $model" >&2; exit 4 ;;
  esac
  final="$target/$file"
  part="$final.part"
  if [[ -f "$final" ]]; then
    actual_bytes=$(stat -c '%s' "$final")
    actual_digest=$(sha256sum "$final" | awk '{print $1}')
    if [[ "$actual_bytes" == "$bytes" && "$actual_digest" == "$digest" ]]; then
      printf 'verified-existing\t%s\t%s\t%s\n' "$file" "$bytes" "$digest"
      continue
    fi
    echo "refusing mismatched final file: $final" >&2
    exit 5
  fi
  if [[ -f "$part" ]] && (( $(stat -c '%s' "$part") > bytes )); then
    echo "oversized partial file: $part" >&2
    exit 6
  fi
  url="https://huggingface.co/$repo/resolve/$revision/$file"
  printf 'download\t%s\t%s\n' "$file" "$url"
  curl --fail --location --retry 2 --retry-delay 5 --connect-timeout 20 \
    --max-time 2700 --speed-limit 1024 --speed-time 60 --continue-at - \
    --output "$part" "$url"
  actual_bytes=$(stat -c '%s' "$part")
  actual_digest=$(sha256sum "$part" | awk '{print $1}')
  if [[ "$actual_bytes" != "$bytes" || "$actual_digest" != "$digest" ]]; then
    echo "identity mismatch for $part" >&2
    exit 7
  fi
  mv "$part" "$final"
  printf 'verified-new\t%s\t%s\t%s\n' "$file" "$bytes" "$digest"
done

printf 'complete\t%s\n' "$(date -u +%FT%TZ)"
