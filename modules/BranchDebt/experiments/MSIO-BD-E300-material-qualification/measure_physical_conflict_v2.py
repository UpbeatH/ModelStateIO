#!/usr/bin/env python3
import json,os,re,signal,subprocess,sys,time,urllib.request
R='/mnt/nvme1/chenhao/modelstateio-runtime'; MR=R+'/models/branchdebt-e300'; O=R+'/experiments/MSIO-BD-E300/capacity/physical-conflict.json'; S=R+'/build-d230ddd-cuda116-sm70/bin/llama-server'; P=18200; MS=['qwen2.5-7b-instruct-q4_k_m','qwen2.5-14b-instruct-q4_k_m','qwen2.5-32b-instruct-q5_k_m']
def ids():
 try:return [int(x) for x in subprocess.check_output(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],text=True,stderr=subprocess.DEVNULL).split() if x.isdigit()]
 except:return []
def main():
 os.makedirs(os.path.dirname(O),exist_ok=True); assert not ids()
 p=subprocess.Popen([S,'--host','127.0.0.1','--port',str(P),'--models-dir',MR,'--models-max','0','--no-models-autoload','--ctx-size','4096','--n-gpu-layers','999'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,preexec_fn=os.setsid); rs=[]
 try:
  for _ in range(60):
   try:urllib.request.urlopen('http://127.0.0.1:%d/models'%P,timeout=2);break
   except:time.sleep(1)
  for m in MS:
   try:
    q=urllib.request.Request('http://127.0.0.1:%d/models/load'%P,json.dumps({'model':m}).encode(),{'Content-Type':'application/json'});rs.append({'model':m,'request_ok':True,'response':urllib.request.urlopen(q,timeout=30).read().decode()[:1000],'pids_at_check':ids()})
   except Exception as e:rs.append({'model':m,'request_ok':False,'error':str(e),'pids_at_check':ids()})
   time.sleep(2)
 finally:
  try:os.killpg(p.pid,signal.SIGTERM);p.wait(15)
  except:os.killpg(p.pid,signal.SIGKILL)
 log=p.stdout.read()[-20000:]; obs=bool(re.search(r'out of memory|memory allocation|cudaMalloc|CUDA error|failed to fit params|free device memory|status 1',log,re.I)); rec={'experiment_id':'MSIO-BD-E300','observed':obs,'models_max':0,'attempted_models':MS,'load_results':rs,'cause':'gpu_memory_capacity' if obs else 'not_observed','cleanup_ok':not ids(),'server_log_tail':log,'evidence_level':'direct_physical_receipt'}
 with open(O,'w') as f:json.dump(rec,f,indent=2,sort_keys=True)
 print(json.dumps(rec,sort_keys=True));return 0 if obs and rec['cleanup_ok'] else 2
if __name__=='__main__':sys.exit(main())
