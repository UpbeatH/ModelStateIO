#!/usr/bin/env bash
set -euo pipefail

runtime_root=/mnt/nvme1/chenhao/modelstateio-runtime
experiment_root="$runtime_root/logs/MSIO-CP-E007"
lock_root="$runtime_root/locks/MSIO-CP-E007.lock"
binary_file="$runtime_root/build-d230ddd-cuda116-sm70/bin/llama-cli"
model_file="$runtime_root/incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf"
measure_file="$runtime_root/incoming/measure_once_e007.py"
analyze_file="$runtime_root/incoming/analyze_e007.py"
expected_binary=39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24
expected_model=74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db

mkdir -p "$runtime_root/locks"
if ! mkdir "$lock_root" 2>/dev/null; then
  echo "E007_LOCKED"
  exit 75
fi
trap 'rmdir "$lock_root" 2>/dev/null || true' EXIT

mkdir -p "$experiment_root/raw"
test "$(sha256sum "$binary_file" | cut -d' ' -f1)" = "$expected_binary"
test "$(sha256sum "$model_file" | cut -d' ' -f1)" = "$expected_model"
test "$(df --output=avail -B1 "$runtime_root" | tail -n1)" -ge 2147483648
test "$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | tr -d ' ')" -le 16
test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
python3 -m py_compile "$measure_file" "$analyze_file"
LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64 ldd "$binary_file" > "$experiment_root/ldd-cuda116.txt"
grep -q '/usr/local/cuda-11.6/lib64/libcudart' "$experiment_root/ldd-cuda116.txt"
grep -q '/usr/local/cuda-11.6/lib64/libcublas' "$experiment_root/ldd-cuda116.txt"
sha256sum "$binary_file" "$model_file" "$measure_file" "$analyze_file" > "$experiment_root/input-sha256.txt"
nvidia-smi --query-gpu=timestamp,name,memory.used,utilization.gpu --format=csv,noheader > "$experiment_root/gpu-before.txt"

printf '%s\t%s\t%s\n' block position mode > "$experiment_root/schedule.tsv"
printf '%s\n' \
  '1 1 mmap' '1 2 none' '1 3 dio' \
  '2 1 none' '2 2 dio' '2 3 mmap' \
  '3 1 dio' '3 2 mmap' '3 3 none' \
  '4 1 mmap' '4 2 dio' '4 3 none' \
  '5 1 dio' '5 2 none' '5 3 mmap' \
  '6 1 none' '6 2 mmap' '6 3 dio' |
while read -r block position mode; do
  trial_id="b${block}-p${position}-${mode}"
  printf '%s\t%s\t%s\n' "$block" "$position" "$mode" >> "$experiment_root/schedule.tsv"
  python3 "$measure_file" --binary "$binary_file" --model "$model_file" --mode "$mode" \
    --trial "$trial_id" --output-dir "$experiment_root/raw"
  test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
  sleep 2
done

set +e
python3 "$analyze_file" "$experiment_root/raw" "$experiment_root/compact-result.json" > "$experiment_root/analysis.stdout.txt" 2> "$experiment_root/analysis.stderr.txt"
analysis_status=$?
set -e
printf '%s\n' "$analysis_status" > "$experiment_root/analysis.exit"
nvidia-smi --query-gpu=timestamp,name,memory.used,utilization.gpu --format=csv,noheader > "$experiment_root/gpu-after.txt"
test "$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | tr -d ' ')" -le 16
test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
sha256sum "$experiment_root"/*.txt "$experiment_root"/*.tsv "$experiment_root"/*.json "$experiment_root"/*.exit > "$experiment_root/SHA256SUMS.txt"
touch "$experiment_root/COMPLETED"
if test "$analysis_status" = 0; then
  echo "E007_PASS"
else
  echo "E007_NO_GO"
  exit "$analysis_status"
fi

