#!/usr/bin/env python3
import hashlib,json,os,subprocess,sys,time,urllib.request
from pathlib import Path
R=Path('/mnt/nvme1/chenhao/modelstateio-runtime'); B=R/'build-d230ddd-cuda116-sm70/bin/llama-server'; M=R/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf'; O=R/'logs/MSIO-KVG-E001'; S=O/'slot-state'; PORT='18081'
MS='74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for x in iter(lambda:f.read(8<<20),b''):h.update(x)
 return h.hexdigest()
def post(path,payload):
 q=urllib.request.Request('http://127.0.0.1:'+PORT+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
 with urllib.request.urlopen(q,timeout=40) as x:return json.load(x)
def main():
 if O.exists() or sha(M)!=MS:return 90
 if subprocess.run(['pgrep','-x','llama-server'],stdout=subprocess.DEVNULL).returncode==0:return 91
 O.mkdir(parents=True);S.mkdir(); log=open(O/'server.log','w'); p=None
 try:
  p=subprocess.Popen([str(B),'-m',str(M),'--host','127.0.0.1','--port',PORT,'-ngl','99','-c','512','--slot-save-path',str(S)],stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'LD_LIBRARY_PATH':'/usr/local/cuda-11.6/lib64'})
  for _ in range(90):
   try:
    with urllib.request.urlopen('http://127.0.0.1:'+PORT+'/health',timeout=2) as x:
     if x.status==200:break
   except Exception:time.sleep(1)
  else:return 92
  base={'prompt':'The verification tag is STATE_OK.','id_slot':1,'cache_prompt':True,'n_predict':3,'temperature':0,'seed':1}
  first=post('/completion',base); saved=post('/slots/1?action=save',{'filename':'slot1.bin'}); restored=post('/slots/0?action=restore',{'filename':'slot1.bin'})
  follow={'prompt':'The verification tag is STATE_OK. Continue with exactly OK.','cache_prompt':True,'n_predict':3,'temperature':0,'seed':1}
  a=post('/completion',{**follow,'id_slot':1}); b=post('/completion',{**follow,'id_slot':0})
  result={'first':first,'saved':saved,'restored':restored,'slot1':a,'slot0':b,'state_bytes':(S/'slot1.bin').stat().st_size}
  (O/'receipt.json').write_text(json.dumps(result,sort_keys=True)+'\n')
  if saved.get('n_saved',0)<=0 or restored.get('n_restored',0)<=0 or result['state_bytes']<=0 or a.get('content')!=b.get('content'):return 93
  return 0
 finally:
  if p:
   p.terminate()
   try:p.wait(timeout=30)
   except subprocess.TimeoutExpired:p.kill();p.wait(timeout=10)
  log.close()
  if subprocess.run(['pgrep','-x','llama-server'],stdout=subprocess.DEVNULL).returncode==0:return 94
if __name__=='__main__':sys.exit(main())
