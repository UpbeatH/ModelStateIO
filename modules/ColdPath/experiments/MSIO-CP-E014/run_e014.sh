#!/usr/bin/env bash
set -euo pipefail

runtime_root=/mnt/nvme1/chenhao/modelstateio-runtime
experiment=MSIO-CP-E014
experiment_root="$runtime_root/logs/$experiment"
raw_root="$experiment_root/raw"
lock_root="$runtime_root/locks/$experiment.lock"
binary_file="$runtime_root/build-d230ddd-cuda116-sm70/bin/llama-cli"
model_file="$runtime_root/incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf"
measure_file="$runtime_root/incoming/measure_once_e007.py"
guard_file="$runtime_root/incoming/guard_snapshot_e009r1.py"
analyze_file="$runtime_root/incoming/analyze_e014.py"

test "$(sha256sum "$binary_file" | cut -d' ' -f1)" = 39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24
test "$(sha256sum "$model_file" | cut -d' ' -f1)" = 74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db
test "$(sha256sum "$measure_file" | cut -d' ' -f1)" = 6626a424176fb47a09cfb6e133e23600514dbca4d16d296eee5f5acedb847506
test "$(sha256sum "$guard_file" | cut -d' ' -f1)" = a6f542700928630655ab67c03e3769d97e5fb625e1f8e328c818d66957ff407e
test "$(sha256sum "$analyze_file" | cut -d' ' -f1)" = 3aae338427dddefb71f742f5258158360d8eeac71629c4c4183bba020f006653
test -z "$(pgrep -x llama-cli || true)"
mkdir -p "$runtime_root/locks"
if ! mkdir "$lock_root" 2>/dev/null; then echo "$experiment LOCKED"; exit 75; fi
trap 'rmdir "$lock_root" 2>/dev/null || true' EXIT
mkdir -p "$raw_root"
test ! -e "$experiment_root/COMPLETED"
python3 -m py_compile "$measure_file" "$guard_file" "$analyze_file"
sha256sum "$binary_file" "$model_file" "$measure_file" "$guard_file" "$analyze_file" > "$experiment_root/input-sha256.txt"
nvidia-smi --query-gpu=timestamp,name,memory.used,utilization.gpu --format=csv,noheader > "$experiment_root/gpu-before.txt"
printf 'block\tposition\tmode\n' > "$experiment_root/schedule.tsv"
printf '%s\n' '1 1 mmap' '1 2 none' '1 3 dio' '2 1 none' '2 2 dio' '2 3 mmap' '3 1 dio' '3 2 mmap' '3 3 none' '4 1 mmap' '4 2 dio' '4 3 none' '5 1 dio' '5 2 none' '5 3 mmap' '6 1 none' '6 2 mmap' '6 3 dio' |
while read -r block position mode; do
  trial_id="b${block}-p${position}-${mode}"
  printf '%s\t%s\t%s\n' "$block" "$position" "$mode" >> "$experiment_root/schedule.tsv"
  python3 "$guard_file" --phase before --trial "$trial_id" --settle-index 0 --status 0 --output "$raw_root/$trial_id.before.guard.json"
  set +e; python3 "$measure_file" --binary "$binary_file" --model "$model_file" --mode "$mode" --trial "$trial_id" --output-dir "$raw_root"; rc=$?; set -e
  python3 "$guard_file" --phase after --trial "$trial_id" --settle-index 0 --status "$rc" --output "$raw_root/$trial_id.after.guard.json" || true
  if test "$rc" != 0 || test -n "$(pgrep -x llama-cli || true)"; then printf 'trial_failure:%s\n' "$rc" > "$experiment_root/STOP_REASON"; exit 86; fi
  sleep 2
done
set +e; python3 "$analyze_file" --receipt-dir "$raw_root" --experiment "$experiment" --output "$experiment_root/compact-result.json" > "$experiment_root/analysis.stdout.txt" 2> "$experiment_root/analysis.stderr.txt"; analysis_rc=$?; set -e
printf '%s\n' "$analysis_rc" > "$experiment_root/analysis.exit"
nvidia-smi --query-gpu=timestamp,name,memory.used,utilization.gpu --format=csv,noheader > "$experiment_root/gpu-after.txt"
test -z "$(pgrep -x llama-cli || true)"
sha256sum "$experiment_root"/*.txt "$experiment_root"/*.tsv "$experiment_root"/*.json "$experiment_root"/*.exit > "$experiment_root/SHA256SUMS.txt"
touch "$experiment_root/COMPLETED"
test "$analysis_rc" = 0 && echo "$experiment PASS" || { echo "$experiment NO_GO"; exit "$analysis_rc"; }
