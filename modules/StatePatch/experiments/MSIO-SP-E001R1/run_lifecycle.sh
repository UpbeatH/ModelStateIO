#!/usr/bin/env bash
# Bounded E001R1 runner. E001 artifacts and receipts are never overwritten.
set -euo pipefail

runtime=/mnt/nvme1/chenhao/modelstateio-runtime
bin="$runtime/build-d230ddd-cuda116-sm70/bin/llama-server"
base="$runtime/incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf"
adapter="$runtime/artifacts/statepatch-e001r1/qwen2.5-0.5b-gsm8k-lora.gguf"
out="$runtime/logs/MSIO-SP-E001R1/$(date +%Y%m%dT%H%M%S%z)"
port=18098
mkdir -p "$out"

test ! -e "$out/RESULT.json"
test -x "$bin" && test -f "$base" && test -f "$adapter"
test -z "$(pgrep -u "$USER" -f "llama-server.*--port $port" || true)"

cleanup() {
  if [[ -n "${server_pid:-}" ]] && kill -0 "$server_pid" 2>/dev/null; then
    kill "$server_pid" 2>/dev/null || true
    wait "$server_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT

export LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
sha256sum "$bin" "$base" "$adapter" > "$out/identities.sha256"
timeout 90 "$bin" -m "$base" --lora "$adapter" --lora-init-without-apply \
  --host 127.0.0.1 --port "$port" --ctx-size 512 --parallel 1 --n-gpu-layers 99 \
  >"$out/server.log" 2>&1 &
server_pid=$!

for _ in $(seq 1 45); do
  if curl --silent --show-error --fail --max-time 2 "http://127.0.0.1:$port/lora-adapters" > "$out/adapters.initial.json"; then break; fi
  sleep 1
done
test -s "$out/adapters.initial.json"

prompt='What is 17 plus 25? Answer with only the number.'
request() {
  local label=$1
  curl --silent --show-error --fail --max-time 30 -H 'Content-Type: application/json' \
    -d "{\"prompt\":\"$prompt\",\"n_predict\":16,\"temperature\":0.0,\"seed\":42,\"cache_prompt\":false}" \
    "http://127.0.0.1:$port/completion" > "$out/$label.json"
  python3 - "$out/$label.json" > "$out/$label.content" <<'PY'
import json, sys
obj = json.load(open(sys.argv[1], encoding='utf-8'))
value = obj.get('content')
if not isinstance(value, str): raise SystemExit('response lacks string content')
print(value, end='')
PY
}

curl --silent --show-error --fail --max-time 10 -H 'Content-Type: application/json' -d '[{"id":0,"scale":0.0}]' "http://127.0.0.1:$port/lora-adapters" > "$out/control.disabled-1.json"
request disabled_1
curl --silent --show-error --fail --max-time 10 -H 'Content-Type: application/json' -d '[{"id":0,"scale":1.0}]' "http://127.0.0.1:$port/lora-adapters" > "$out/control.enabled.json"
request enabled
curl --silent --show-error --fail --max-time 10 -H 'Content-Type: application/json' -d '[]' "http://127.0.0.1:$port/lora-adapters" > "$out/control.disabled-2.json"
request disabled_2
curl --silent --show-error --fail --max-time 10 "http://127.0.0.1:$port/lora-adapters" > "$out/adapters.final.json"

python3 - "$out" > "$out/RESULT.json" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
def read(name): return (root / (name + '.content')).read_text(encoding='utf-8')
def digest(value): return hashlib.sha256(value.encode()).hexdigest()
a, b, c = map(read, ('disabled_1', 'enabled', 'disabled_2'))
print(json.dumps({'disabled_equal': a == c, 'enabled_differs': a != b,
 'content_sha256': {'disabled_1': digest(a), 'enabled': digest(b), 'disabled_2': digest(c)},
 'decision': 'GO (technical)' if a == c and a != b else 'NO-GO'}, sort_keys=True, indent=2))
PY
cat "$out/RESULT.json"
