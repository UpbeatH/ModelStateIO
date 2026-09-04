#!/usr/bin/env bash
set -euo pipefail

runtime_root=/mnt/nvme1/chenhao/modelstateio-runtime
experiment_root="$runtime_root/logs/MSIO-CP-E006"
lock_root="$runtime_root/locks/MSIO-CP-E006.lock"
binary_file="$runtime_root/build-d230ddd-cuda116-sm70/bin/llama-cli"
model_file="$runtime_root/incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf"
expected_binary=39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24
expected_model=74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db

mkdir -p "$runtime_root/locks"
if ! mkdir "$lock_root" 2>/dev/null; then
  echo "E006_LOCKED"
  exit 75
fi
trap 'rmdir "$lock_root" 2>/dev/null || true' EXIT

mkdir -p "$experiment_root"
test "$(sha256sum "$binary_file" | cut -d' ' -f1)" = "$expected_binary"
test "$(sha256sum "$model_file" | cut -d' ' -f1)" = "$expected_model"
test "$(df --output=avail -B1 "$runtime_root" | tail -n1)" -ge 2147483648
test "$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | tr -d ' ')" -le 16
test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
strace -h 2>&1 | grep -q -- '--trace-path'
LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64 ldd "$binary_file" > "$experiment_root/ldd-cuda116.txt"
grep -q '/usr/local/cuda-11.6/lib64/libcudart' "$experiment_root/ldd-cuda116.txt"
grep -q '/usr/local/cuda-11.6/lib64/libcublas' "$experiment_root/ldd-cuda116.txt"
sha256sum "$binary_file" "$model_file" > "$experiment_root/input-sha256.txt"
nvidia-smi --query-gpu=timestamp,name,memory.used,utilization.gpu --format=csv,noheader > "$experiment_root/gpu-before.txt"

run_arm() {
  arm="$1"
  stdout_file="$experiment_root/$arm.stdout.txt"
  stderr_file="$experiment_root/$arm.stderr.txt"
  trace_file="$experiment_root/$arm.open.trace"
  set +e
  (
    ulimit -f 4096
    LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64 timeout 120 strace -f -qq -e trace=open,openat -P "$model_file" -o "$trace_file" \
      "$binary_file" --model "$model_file" --load-mode "$arm" --single-turn --simple-io --no-display-prompt \
      --prompt 'Reply with exactly OK.' --predict 1 --seed 1 --temp 0 --n-gpu-layers 99 --ctx-size 256 \
      --batch-size 64 --threads 4 --threads-batch 4
  ) > "$stdout_file" 2> "$stderr_file"
  arm_status=$?
  set -e
  printf '%s\n' "$arm_status" > "$experiment_root/$arm.exit"
  test "$arm_status" = 0
  test "$(wc -c < "$stdout_file")" -le 2097152
  test "$(wc -c < "$stderr_file")" -le 2097152
  test "$(wc -c < "$trace_file")" -le 2097152
  grep -Fxq 'OK' "$stdout_file"
  grep -Fq 'Exiting...' "$stdout_file"
  grep -Fq "$model_file" "$trace_file"
  test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
}

run_arm mmap
! grep -Fq 'O_DIRECT' "$experiment_root/mmap.open.trace"
run_arm none
! grep -Fq 'O_DIRECT' "$experiment_root/none.open.trace"
run_arm dio
grep -Fq 'O_DIRECT' "$experiment_root/dio.open.trace"

nvidia-smi --query-gpu=timestamp,name,memory.used,utilization.gpu --format=csv,noheader > "$experiment_root/gpu-after.txt"
test "$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | tr -d ' ')" -le 16
sha256sum "$experiment_root"/*.txt "$experiment_root"/*.exit "$experiment_root"/*.trace > "$experiment_root/SHA256SUMS.txt"
touch "$experiment_root/COMPLETED"
echo "E006_PASS"
