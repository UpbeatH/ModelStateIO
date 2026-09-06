#!/usr/bin/env bash
set -euo pipefail

token=${1:-}
if [[ "$token" != "PROMOTE-MSIO-BD-E300" ]]; then
  echo "authorization token mismatch" >&2
  exit 64
fi
runtime=/mnt/nvme1/chenhao/modelstateio-runtime
incoming="$runtime/incoming/models-e300"
destination="$runtime/models/branchdebt-e300"
receipt_dir="$runtime/experiments/MSIO-BD-E300/acquisition"
manifest=${MODEL_MANIFEST:-}
[[ -n "$manifest" && -f "$manifest" ]] || { echo "MODEL_MANIFEST is required" >&2; exit 66; }
[[ -d "$incoming" ]] || { echo "missing incoming directory" >&2; exit 66; }
mkdir -p "$receipt_dir"
exec 9>"$receipt_dir/.promote.lock"
flock -n 9 || { echo "promotion already active" >&2; exit 75; }

target_dir() {
  case "$1" in
    Qwen2.5-7B-Instruct-Q4_K_M) echo "$destination/qwen2.5-7b-instruct-q4_k_m" ;;
    Qwen2.5-14B-Instruct-Q4_K_M) echo "$destination/qwen2.5-14b-instruct-q4_k_m" ;;
    Qwen2.5-32B-Instruct-Q5_K_M) echo "$destination/qwen2.5-32b-instruct-q5_k_m" ;;
    *) return 1 ;;
  esac
}

# First pass is read-only and all-or-nothing: every final-name upload must match.
rows=0
while IFS=$'\t' read -r model revision file bytes sha; do
  path="$incoming/$file"
  [[ -f "$path" ]] || { echo "waiting for uploaded file: $file" >&2; exit 75; }
  [[ $(stat -c %s "$path") == "$bytes" ]] || { echo "size mismatch: $path" >&2; exit 65; }
  [[ $(sha256sum "$path" | awk '{print $1}') == "$sha" ]] || { echo "hash mismatch: $path" >&2; exit 65; }
  target_dir "$model" >/dev/null || { echo "unexpected model: $model" >&2; exit 65; }
  rows=$((rows + 1))
done < <(tail -n +2 "$manifest")
[[ $rows == 11 ]] || { echo "expected 11 frozen manifest rows, got $rows" >&2; exit 65; }

mkdir -p "$destination"
while IFS=$'\t' read -r model revision file bytes sha; do
  dir=$(target_dir "$model")
  mkdir -p "$dir"
  final="$dir/$file"
  if [[ -e "$final" ]]; then
    echo "refusing existing destination: $final" >&2
    exit 65
  fi
  mv "$incoming/$file" "$final"
done < <(tail -n +2 "$manifest")

receipt="$receipt_dir/PROMOTED.tsv"
printf 'model\trevision\tfile\tbytes\tsha256\tpath\n' >"$receipt"
while IFS=$'\t' read -r model revision file bytes sha; do
  dir=$(target_dir "$model")
  final="$dir/$file"
  actual=$(sha256sum "$final" | awk '{print $1}')
  [[ $(stat -c %s "$final") == "$bytes" && "$actual" == "$sha" ]] || {
    echo "post-promotion identity failure: $final" >&2; exit 70;
  }
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$model" "$revision" "$file" "$bytes" "$actual" "$final" >>"$receipt"
done < <(tail -n +2 "$manifest")
sha256sum "$receipt"
echo "PROMOTION_COMPLETE rows=$rows"
