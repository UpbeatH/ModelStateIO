#!/usr/bin/env bash
# E002 bounded compatibility runner; raw output is deliberately Git-external.
set -euo pipefail
r=/mnt/nvme1/chenhao/modelstateio-runtime
b="$r/build-d230ddd-cuda116-sm70/bin/llama-server"
m="$r/incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf"
a="$r/artifacts/statepatch-e002/seed43.gguf"
o="$r/logs/MSIO-SP-E002/$(date +%Y%m%dT%H%M%S%z)"; p=18099
mkdir -p "$o"; test -x "$b" && test -f "$m" && test -f "$a"
test -z "$(pgrep -u "$USER" -f "llama-server.*--port $p" || true)"
cleanup(){ [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null && kill "$pid" 2>/dev/null || true; }
trap cleanup EXIT
export LD_LIBRARY_PATH=/usr/local/cuda-11.6/lib64${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
sha256sum "$b" "$m" "$a" > "$o/identities.sha256"
timeout 90 "$b" -m "$m" --lora "$a" --lora-init-without-apply --host 127.0.0.1 --port "$p" --ctx-size 512 --parallel 1 --n-gpu-layers 99 >"$o/server.log" 2>&1 & pid=$!
for _ in $(seq 1 45); do curl -sf --max-time 2 "http://127.0.0.1:$p/lora-adapters" >"$o/adapters.initial.json" && break; sleep 1; done
test -s "$o/adapters.initial.json"
request(){ local x=$1; curl -sf --max-time 30 -H 'Content-Type: application/json' -d '{"prompt":"Reply with exactly the word ready.","n_predict":8,"temperature":0.0,"seed":42,"cache_prompt":false}' "http://127.0.0.1:$p/completion" >"$o/$x.json"; python3 - "$o/$x.json" >"$o/$x.content" <<'PY'
import json,sys
x=json.load(open(sys.argv[1])); assert isinstance(x.get('content'),str); print(x['content'],end='')
PY
}
curl -sf --max-time 10 -H 'Content-Type: application/json' -d '[{"id":0,"scale":0.0}]' "http://127.0.0.1:$p/lora-adapters" >"$o/disable1.json"; request disabled_1
curl -sf --max-time 10 -H 'Content-Type: application/json' -d '[{"id":0,"scale":1.0}]' "http://127.0.0.1:$p/lora-adapters" >"$o/enable.json"; request enabled
curl -sf --max-time 10 -H 'Content-Type: application/json' -d '[]' "http://127.0.0.1:$p/lora-adapters" >"$o/disable2.json"; request disabled_2
python3 - "$o" >"$o/RESULT.json" <<'PY'
import hashlib,json,pathlib,sys
r=pathlib.Path(sys.argv[1]); read=lambda x:(r/(x+'.content')).read_text(); a,b,c=map(read,['disabled_1','enabled','disabled_2']); h=lambda x:hashlib.sha256(x.encode()).hexdigest(); print(json.dumps({'disabled_equal':a==c,'enabled_differs':a!=b,'content_sha256':{'disabled_1':h(a),'enabled':h(b),'disabled_2':h(c)},'decision':'GO (technical compatibility)' if a==c and a!=b else 'NO-GO'},indent=2,sort_keys=True))
PY
cat "$o/RESULT.json"
