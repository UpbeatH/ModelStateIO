#!/usr/bin/env bash
set -euo pipefail

runtime_root=/mnt/nvme1/chenhao/modelstateio-runtime
experiment_root="$runtime_root/logs/MSIO-CP-E004"
lock_root="$runtime_root/locks/MSIO-CP-E004.lock"
model_file="$runtime_root/incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf"
binary_file="$runtime_root/build-d230ddd-cuda116-sm70/bin/llama-cli"
expected_binary=39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24
expected_model=74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db

mkdir -p "$runtime_root/locks"
if ! mkdir "$lock_root" 2>/dev/null; then
  echo "E004_LOCKED"
  exit 75
fi
trap 'rmdir "$lock_root" 2>/dev/null || true' EXIT

mkdir -p "$experiment_root"
test "$(sha256sum "$binary_file" | cut -d' ' -f1)" = "$expected_binary"
test "$(df --output=avail -B1 "$runtime_root" | tail -n1)" -ge 2147483648
test "$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | tr -d ' ')" -le 16
LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64 ldd "$binary_file" > "$experiment_root/ldd-cuda116.txt"
grep -q '/usr/local/cuda-11.6/lib64/libcudart' "$experiment_root/ldd-cuda116.txt"
grep -q '/usr/local/cuda-11.6/lib64/libcublas' "$experiment_root/ldd-cuda116.txt"

test "$(stat -c %s "$model_file")" = 491400032
test "$(sha256sum "$model_file" | cut -d' ' -f1)" = "$expected_model"
sha256sum "$binary_file" "$model_file" > "$experiment_root/input-sha256.txt"
nvidia-smi --query-gpu=timestamp,name,memory.used,utilization.gpu --format=csv,noheader > "$experiment_root/gpu-before.txt"

set +e
LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64 /usr/bin/time -v timeout 180 "$binary_file" --model "$model_file" --load-mode mmap --n-gpu-layers 99 --ctx-size 256 --batch-size 64 --threads 4 --threads-batch 4 --predict 1 --seed 1 --temp 0 --no-display-prompt --prompt 'Reply OK' > "$experiment_root/smoke.log" 2>&1
smoke_status=$?
set -e
printf '%s\n' "$smoke_status" > "$experiment_root/smoke.exit"
nvidia-smi --query-gpu=timestamp,name,memory.used,utilization.gpu --format=csv,noheader > "$experiment_root/gpu-after.txt"
test "$smoke_status" = 0
grep -Eiq 'offload|CUDA0|model loaded|load time' "$experiment_root/smoke.log"
test -z "$(pgrep -u "$(id -u)" -f "[l]lama-cli.*qwen2.5-0.5b-instruct-q4_k_m.gguf" || true)"
sha256sum "$experiment_root"/*.txt "$experiment_root"/*.log "$experiment_root"/*.exit > "$experiment_root/SHA256SUMS.txt"
touch "$experiment_root/COMPLETED"
echo "E004_PASS"
