#!/usr/bin/env bash
set -euo pipefail

runtime_root=/mnt/nvme1/chenhao/modelstateio-runtime
experiment_root="$runtime_root/logs/MSIO-CP-E008R1"
guard_file="$runtime_root/incoming/guard_receipt.py"
test_file="$runtime_root/incoming/test_guard_receipt.py"
mkdir -p "$experiment_root"
test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
python3 -m unittest discover -s "$runtime_root/incoming" -p 'test_guard_receipt.py' > "$experiment_root/unit.stdout.txt" 2> "$experiment_root/unit.stderr.txt"
python3 "$guard_file" --case no-process --output "$experiment_root/no-process.receipt.json"
python3 "$guard_file" --case transient-fixture --output "$experiment_root/transient-fixture.receipt.json"
python3 "$guard_file" --case persistent-fixture --output "$experiment_root/persistent-fixture.receipt.json"
grep -Fq '"decision": "PASS"' "$experiment_root/no-process.receipt.json"
grep -Fq '"decision": "SETTLED"' "$experiment_root/transient-fixture.receipt.json"
grep -Fq '"decision": "NO_GO"' "$experiment_root/persistent-fixture.receipt.json"
test -z "$(pgrep -u "$(id -u)" -f '[l]lama-cli' || true)"
sha256sum "$experiment_root"/*.txt "$experiment_root"/*.json > "$experiment_root/SHA256SUMS.txt"
touch "$experiment_root/COMPLETED"
echo E008R1_PASS

