#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys,time,urllib.request
from pathlib import Path
R=Path('/mnt/nvme1/chenhao/modelstateio-runtime');B=R/'build-d230ddd-cuda116-sm70/bin/llama-server';M=R/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf';O=R/'logs/MSIO-KVG-E002';S=O/'slot-state';PORT='18082';MS='74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db'
CASES=[('short','alpha '*20),('long','alpha '*180)]*3
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb')as f:
  for x in iter(lambda:f.read(8<<20),b''):h.update(x)
 return h.hexdigest()
def post(path,payload):
 q=urllib.request.Request('http://127.0.0.1:'+PORT+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST');t=time.monotonic()
 with urllib.request.urlopen(q,timeout=60)as x:r=json.load(x)
 return r,time.monotonic()-t
def main():
 if O.exists() or sha(M)!=MS:return 90
 if subprocess.run(['pgrep','-x','llama-server'],stdout=subprocess.DEVNULL).returncode==0:return 91
 O.mkdir(parents=True);S.mkdir();log=open(O/'server.log','w');p=None;rows=[]
 try:
  p=subprocess.Popen([str(B),'-m',str(M),'--host','127.0.0.1','--port',PORT,'-ngl','99','-c','1024','-np','3','--slot-save-path',str(S)],stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'LD_LIBRARY_PATH':'/usr/local/cuda-11.6/lib64'})
  for _ in range(100):
   try:
    with urllib.request.urlopen('http://127.0.0.1:'+PORT+'/health',timeout=2)as x:
     if x.status==200:break
   except Exception:time.sleep(1)
  else:return 92
  for block,(case,prefix) in enumerate(CASES,1):
   suffix=' Continue with exactly OK.'; full=prefix+suffix; opts={'cache_prompt':True,'n_predict':3,'temperature':0,'seed':1}
   recompute,recompute_wall=post('/completion',{**opts,'prompt':full,'id_slot':2})
   base,_=post('/completion',{**opts,'prompt':prefix,'id_slot':1,'n_predict':0})
   saved,save_wall=post('/slots/1?action=save',{'filename':f'{case}-{block}.bin'})
   restored,restore_wall=post('/slots/0?action=restore',{'filename':f'{case}-{block}.bin'})
   resumed,resumed_wall=post('/completion',{**opts,'prompt':full,'id_slot':0})
   row={'block':block,'case':case,'prefix_chars':len(prefix),'recompute':recompute,'recompute_wall_s':recompute_wall,'base':base,'saved':saved,'save_wall_s':save_wall,'restored':restored,'restore_wall_s':restore_wall,'resumed':resumed,'resumed_wall_s':resumed_wall,'incremental_persist_s':save_wall+restore_wall+resumed_wall,'state_bytes':(S/f'{case}-{block}.bin').stat().st_size,'equal_content':recompute.get('content')==resumed.get('content')}
   rows.append(row);(O/f'b{block}-{case}.json').write_text(json.dumps(row,sort_keys=True)+'\n')
   if saved.get('n_saved',0)<=0 or restored.get('n_restored',0)<=0 or row['state_bytes']<=0 or not row['equal_content']:return 93
   for slot in (0,1,2):post(f'/slots/{slot}?action=erase',{})
  (O/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n');return 0
 finally:
  if p:
   p.terminate()
   try:p.wait(timeout=30)
   except subprocess.TimeoutExpired:p.kill();p.wait(timeout=10)
  log.close()
  if subprocess.run(['pgrep','-x','llama-server'],stdout=subprocess.DEVNULL).returncode==0:return 94
if __name__=='__main__':sys.exit(main())
