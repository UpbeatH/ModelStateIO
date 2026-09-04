#!/usr/bin/env python3
import json,runpy,sys
from pathlib import Path
d=runpy.run_path('/mnt/nvme1/chenhao/modelstateio-runtime/incoming/run_e025.py',run_name='e025module');g=d['main'].__globals__
g['M']=Path('/mnt/nvme1/chenhao/modelstateio-runtime/incoming/qwen2.5-7b-instruct-q4_k_m.gguf');g['O']=Path('/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-CP-E026R1');g['W']=g['O']/'raw';g['H'][0]='2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730'
rc=d['main']()
if rc==0:
 for p in g['W'].glob('*.e025.json'):
  x=json.loads(p.read_text());x['experiment']='MSIO-CP-E026R1';q=p.with_name(p.name.replace('.e025.json','.e026r1.json'));q.write_text(json.dumps(x,sort_keys=True)+'\n');p.unlink()
 r=g['O']/'receipts.json';a=json.loads(r.read_text())
 for x in a:x['experiment']='MSIO-CP-E026R1'
 r.write_text(json.dumps(a,indent=2,sort_keys=True)+'\n')
sys.exit(rc)
