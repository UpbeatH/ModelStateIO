#!/usr/bin/env bash
set -euo pipefail

runtime_root=/mnt/nvme1/chenhao/modelstateio-runtime
experiment_root="$runtime_root/logs/MSIO-CP-E008"
mkdir -p "$experiment_root"
test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
python3 -m unittest discover -s "$runtime_root/incoming" -p 'test_guard_receipt.py' > "$experiment_root/unit.stdout.txt" 2> "$experiment_root/unit.stderr.txt"
for case_name in no-process transient-fixture persistent-fixture; do
  python3 "$runtime_root/incoming/guard_receipt.py" --case "$case_name" --output "$experiment_root/$case_name.receipt.json"
done
test "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[\"decision\"])' "$experiment_root/no-process.receipt.json")" = PASS
test "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[\"decision\"])' "$experiment_root/transient-fixture.receipt.json")" = SETTLED
test "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[\"decision\"])' "$experiment_root/persistent-fixture.receipt.json")" = NO_GO
test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
sha256sum "$experiment_root"/*.txt "$experiment_root"/*.json > "$experiment_root/SHA256SUMS.txt"
touch "$experiment_root/COMPLETED"
echo E008_PASS
