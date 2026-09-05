#!/usr/bin/env python3
import hashlib, json, os, subprocess, sys, time, urllib.request
from pathlib import Path

R=Path('/mnt/nvme1/chenhao/modelstateio-runtime')
B=R/'build-d230ddd-cuda116-sm70/bin/llama-server'
M=R/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf'
O=R/'logs/MSIO-KVG-E004'
MS='74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db'
PORT='18084'
CASES={'short':'alpha '*20,'long':'alpha '*180}
POLICIES=('retain','save','recompute','controller')
LIFE=('return','abandon')

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for x in iter(lambda:f.read(8<<20),b''):h.update(x)
 return h.hexdigest()
def post(path,payload):
 q=urllib.request.Request('http://127.0.0.1:'+PORT+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
 t=time.monotonic()
 with urllib.request.urlopen(q,timeout=60) as x: out=json.load(x)
 return out,time.monotonic()-t
def ready():
 for _ in range(100):
  try:
   with urllib.request.urlopen('http://127.0.0.1:'+PORT+'/health',timeout=2) as x:
    if x.status==200:return
  except Exception:time.sleep(1)
 raise RuntimeError('server readiness timeout')
def erase():
 return post('/slots/0?action=erase',{})[0]
def start(block):
 d=O/f'b{block:02d}'; st=d/'slot-state'; d.mkdir();st.mkdir(); log=open(d/'server.log','w')
 p=subprocess.Popen([str(B),'-m',str(M),'--host','127.0.0.1','--port',PORT,'-ngl','99','-c','1024','-np','1','--cache-ram','0','--slot-save-path',str(st)],stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'LD_LIBRARY_PATH':'/usr/local/cuda-11.6/lib64'})
 ready()
 opts={'cache_prompt':True,'n_predict':3,'temperature':0,'seed':1}
 for _ in range(2):post('/completion',{**opts,'prompt':'warm '*32,'id_slot':0})
 erase()
 return d,st,log,p,opts
def stop(p,log):
 p.terminate()
 try:p.wait(timeout=30)
 except subprocess.TimeoutExpired:p.kill();p.wait(timeout=10)
 log.close()
 if subprocess.run(['pgrep','-x','llama-server'],stdout=subprocess.DEVNULL).returncode==0:raise RuntimeError('residual server')
def main():
 if O.exists() or not B.exists() or sha(M)!=MS:return 90
 if subprocess.run(['pgrep','-x','llama-server'],stdout=subprocess.DEVNULL).returncode==0:return 91
 O.mkdir(parents=True); rows=[]; n=0; suffix=' Continue with exactly OK.'
 try:
  for rep in range(1,4):
   for case,prefix in CASES.items():
    full=prefix+suffix
    for life in LIFE:
     for policy in POLICIES:
      n+=1; d=st=log=p=None
      try:
       d,st,log,p,opts=start(n)
       reference,_=post('/completion',{**opts,'prompt':full,'id_slot':0}); erase()
       base,base_s=post('/completion',{**opts,'prompt':prefix,'id_slot':0,'n_predict':0})
       effective=policy
       if policy=='controller':
        effective='drop' if life=='abandon' else ('save' if case=='long' else 'recompute')
       saved=save_s=None; state_bytes=0; b=None; b_s=None; restored=restore_s=None; a=None; a_s=None
       b_admitted=False
       if effective=='retain':
        a,a_s=post('/completion',{**opts,'prompt':full,'id_slot':0})
       else:
        if effective=='save':
         saved,save_s=post('/slots/0?action=save',{'filename':'state.bin'})
         state_bytes=(st/'state.bin').stat().st_size
        erase()
        b,b_s=post('/completion',{**opts,'prompt':'foreground admission check','id_slot':0,'n_predict':1})
        b_admitted=bool(b.get('content',''))
        if life=='return':
         if effective=='save':
          restored,restore_s=post('/slots/0?action=restore',{'filename':'state.bin'})
          a,tail_s=post('/completion',{**opts,'prompt':full,'id_slot':0})
          a_s=save_s+restore_s+tail_s
         else:
          a,a_s=post('/completion',{**opts,'prompt':full,'id_slot':0})
       equal=(life=='abandon' or (a is not None and a.get('content')==reference.get('content')))
       row={'block':n,'rep':rep,'case':case,'life':life,'policy':policy,'effective_action':effective,'base_s':base_s,'base_prompt_n':base['timings']['prompt_n'],'b_admitted':b_admitted,'b_s':b_s,'saved':saved,'save_s':save_s,'restored':restored,'restore_s':restore_s,'state_bytes':state_bytes,'a_s':a_s,'equal_content':equal,'reference_content':reference.get('content'),'a_content':None if a is None else a.get('content')}
       (d/'receipt.json').write_text(json.dumps(row,sort_keys=True)+'\n');rows.append(row)
       if (life=='return' and not equal) or (effective!='retain' and not b_admitted) or (effective=='save' and (not saved or saved.get('n_saved',0)<=0 or state_bytes<=0)) or (effective=='save' and life=='return' and (not restored or restored.get('n_restored',0)<=0)):return 93
       erase()
      finally:
       if p:stop(p,log)
  (O/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n')
  return 0
 except Exception as e:
  (O/'exception.txt').write_text(repr(e)+'\n')
  return 92
if __name__=='__main__':sys.exit(main())
