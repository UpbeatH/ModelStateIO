#!/usr/bin/env bash
set -euo pipefail

runtime_root=/mnt/nvme1/chenhao/modelstateio-runtime
experiment_root="$runtime_root/logs/MSIO-CP-E009"
raw_root="$experiment_root/raw"
lock_root="$runtime_root/locks/MSIO-CP-E009.lock"
binary_file="$runtime_root/build-d230ddd-cuda116-sm70/bin/llama-cli"
model_file="$runtime_root/incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf"
measure_file="$runtime_root/incoming/measure_once_e007.py"
analyze_file="$runtime_root/incoming/analyze_e007.py"
guard_file="$runtime_root/incoming/guard_snapshot_e009.py"
expected_binary=39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24
expected_model=74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db
expected_measure=6626a424176fb47a09cfb6e133e23600514dbca4d16d296eee5f5acedb847506
expected_analyze=aa77e9f899b91f267cca0ac97a120054d9ce0707d530f36530edbb121ba4cb80

mkdir -p "$runtime_root/locks"
if ! mkdir "$lock_root" 2>/dev/null; then echo E009_LOCKED; exit 75; fi
trap 'rmdir "$lock_root" 2>/dev/null || true' EXIT
mkdir -p "$raw_root"
test "$(sha256sum "$binary_file" | cut -d' ' -f1)" = "$expected_binary"
test "$(sha256sum "$model_file" | cut -d' ' -f1)" = "$expected_model"
test "$(sha256sum "$measure_file" | cut -d' ' -f1)" = "$expected_measure"
test "$(sha256sum "$analyze_file" | cut -d' ' -f1)" = "$expected_analyze"
test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
python3 -m py_compile "$measure_file" "$analyze_file" "$guard_file"
LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64 ldd "$binary_file" > "$experiment_root/ldd-cuda116.txt"
grep -q '/usr/local/cuda-11.6/lib64/libcudart' "$experiment_root/ldd-cuda116.txt"
grep -q '/usr/local/cuda-11.6/lib64/libcublas' "$experiment_root/ldd-cuda116.txt"
sha256sum "$binary_file" "$model_file" "$measure_file" "$analyze_file" "$guard_file" > "$experiment_root/input-sha256.txt"
nvidia-smi --query-gpu=timestamp,name,memory.used,utilization.gpu --format=csv,noheader > "$experiment_root/gpu-before.txt"
printf '%s\t%s\t%s\n' block position mode > "$experiment_root/schedule.tsv"
printf '%s\n' '1 1 mmap' '1 2 none' '1 3 dio' '2 1 none' '2 2 dio' '2 3 mmap' '3 1 dio' '3 2 mmap' '3 3 none' '4 1 mmap' '4 2 dio' '4 3 none' '5 1 dio' '5 2 none' '5 3 mmap' '6 1 none' '6 2 mmap' '6 3 dio' |
while read -r block position mode; do
  trial_id="b${block}-p${position}-${mode}"
  printf '%s\t%s\t%s\n' "$block" "$position" "$mode" >> "$experiment_root/schedule.tsv"
  python3 "$guard_file" --phase before --trial "$trial_id" --settle-index 0 --status 0 --output "$raw_root/$trial_id.before.guard.json"
  set +e
  python3 "$measure_file" --binary "$binary_file" --model "$model_file" --mode "$mode" --trial "$trial_id" --output-dir "$raw_root"
  trial_status=$?
  set -e
  python3 "$guard_file" --phase after --trial "$trial_id" --settle-index 0 --status "$trial_status" --output "$raw_root/$trial_id.after0.guard.json" || true
  if test "$trial_status" != 0; then printf '%s\n' "trial_failure:$trial_status" > "$experiment_root/STOP_REASON"; exit 86; fi
  for settle_index in 1 2; do
    if test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"; then break; fi
    sleep 1
    python3 "$guard_file" --phase after --trial "$trial_id" --settle-index "$settle_index" --status "$trial_status" --output "$raw_root/$trial_id.after${settle_index}.guard.json" || true
  done
  if test -n "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"; then printf '%s\n' persistent_process_after_bounded_settle > "$experiment_root/STOP_REASON"; exit 87; fi
  sleep 2
done
set +e
python3 "$analyze_file" "$raw_root" "$experiment_root/compact-result.json" > "$experiment_root/analysis.stdout.txt" 2> "$experiment_root/analysis.stderr.txt"
analysis_status=$?
set -e
printf '%s\n' "$analysis_status" > "$experiment_root/analysis.exit"
nvidia-smi --query-gpu=timestamp,name,memory.used,utilization.gpu --format=csv,noheader > "$experiment_root/gpu-after.txt"
test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
sha256sum "$experiment_root"/*.txt "$experiment_root"/*.tsv "$experiment_root"/*.json "$experiment_root"/*.exit > "$experiment_root/SHA256SUMS.txt"
touch "$experiment_root/COMPLETED"
if test "$analysis_status" = 0; then echo E009_PASS; else echo E009_NO_GO; exit "$analysis_status"; fi

