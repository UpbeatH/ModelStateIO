#!/usr/bin/env python3
import hashlib, json, os, subprocess, sys, time, urllib.request
from pathlib import Path

R = Path('/mnt/nvme1/chenhao/modelstateio-runtime')
B = R/'build-d230ddd-cuda116-sm70/bin/llama-server'
M = R/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf'
O = R/'logs/MSIO-KVG-E003'
MS = '74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db'
BLOCKS = [('short', 'alpha '*20, 'RP'), ('long', 'alpha '*180, 'RP'),
          ('short', 'alpha '*20, 'PR'), ('long', 'alpha '*180, 'PR'),
          ('short', 'alpha '*20, 'RP'), ('long', 'alpha '*180, 'RP')]
PORT = '18083'

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for x in iter(lambda: f.read(8 << 20), b''): h.update(x)
    return h.hexdigest()

def post(path, payload):
    q = urllib.request.Request('http://127.0.0.1:'+PORT+path,
        data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'}, method='POST')
    t = time.monotonic()
    with urllib.request.urlopen(q, timeout=60) as x: out = json.load(x)
    return out, time.monotonic()-t

def wait_ready():
    for _ in range(100):
        try:
            with urllib.request.urlopen('http://127.0.0.1:'+PORT+'/health', timeout=2) as x:
                if x.status == 200: return
        except Exception: time.sleep(1)
    raise RuntimeError('server readiness timeout')

def main():
    if O.exists() or sha(M) != MS or not B.exists(): return 90
    if subprocess.run(['pgrep','-x','llama-server'], stdout=subprocess.DEVNULL).returncode == 0: return 91
    O.mkdir(parents=True); rows=[]
    suffix = ' Continue with exactly OK.'
    opts = {'cache_prompt':False, 'n_predict':3, 'temperature':0, 'seed':1}
    try:
        for number, (case, prefix, order) in enumerate(BLOCKS, 1):
            bo=O/f'b{number}-{case}'; state=bo/'slot-state'; bo.mkdir(); state.mkdir()
            log=open(bo/'server.log','w'); p=None
            try:
                p=subprocess.Popen([str(B),'-m',str(M),'--host','127.0.0.1','--port',PORT,
                    '-ngl','99','-c','1024','-np','3','--cache-ram','0','--no-cache-prompt',
                    '--slot-save-path',str(state)], stdout=log, stderr=subprocess.STDOUT,
                    env={**os.environ,'LD_LIBRARY_PATH':'/usr/local/cuda-11.6/lib64'})
                wait_ready()
                warm=[]
                for _ in range(2): warm.append(post('/completion',{**opts,'prompt':'warm '*32,'id_slot':2})[1])
                full=prefix+suffix
                base, base_wall = post('/completion',{**opts,'prompt':prefix,'id_slot':1,'n_predict':0})
                saved, save_wall = post('/slots/1?action=save',{'filename':'state.bin'})
                arms={}
                for arm in order:
                    if arm == 'R':
                        out, wall=post('/completion',{**opts,'prompt':full,'id_slot':2}); arms['recompute']={'out':out,'wall_s':wall}
                    else:
                        restored, restore_wall=post('/slots/0?action=restore',{'filename':'state.bin'})
                        out, resume_wall=post('/completion',{**opts,'prompt':suffix,'id_slot':0})
                        arms['persist']={'out':out,'restore':restored,'restore_wall_s':restore_wall,'resume_wall_s':resume_wall,'wall_s':save_wall+restore_wall+resume_wall}
                row={'block':number,'case':case,'order':order,'prefix_chars':len(prefix),'warmup_wall_s':warm,
                     'base':base,'base_wall_s':base_wall,'saved':saved,'save_wall_s':save_wall,
                     'recompute':arms['recompute'],'persist':arms['persist'],
                     'state_bytes':(state/'state.bin').stat().st_size,
                     'equal_content':arms['recompute']['out'].get('content') == arms['persist']['out'].get('content')}
                (bo/'receipt.json').write_text(json.dumps(row,sort_keys=True)+'\n'); rows.append(row)
                if (saved.get('n_saved',0)<=0 or arms['persist']['restore'].get('n_restored',0)<=0
                    or row['state_bytes']<=0 or not row['equal_content']): return 93
                for slot in (0,1,2): post(f'/slots/{slot}?action=erase',{})
            finally:
                if p:
                    p.terminate()
                    try: p.wait(timeout=30)
                    except subprocess.TimeoutExpired: p.kill(); p.wait(timeout=10)
                log.close()
                if subprocess.run(['pgrep','-x','llama-server'],stdout=subprocess.DEVNULL).returncode == 0: return 94
        (O/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n'); return 0
    except Exception as e:
        (O/'exception.txt').write_text(repr(e)+'\n'); return 92

if __name__ == '__main__': sys.exit(main())
