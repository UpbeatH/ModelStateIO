#!/usr/bin/env python3
import ctypes,hashlib,json,mmap,os,subprocess,sys,threading,time
from pathlib import Path
R=Path('/mnt/nvme1/chenhao/modelstateio-runtime');M=R/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf';B=R/'build-d230ddd-cuda116-sm70/bin/llama-cli';Q=R/'incoming/measure_once_e007.py';O=R/'logs/MSIO-CP-E022R1';W=O/'raw';C=8<<20
S=[['none','completed','concurrent'],['completed','concurrent','none'],['concurrent','none','completed']]*2
def h(p):
 x=hashlib.sha256()
 with open(p,'rb') as f:
  for q in iter(lambda:f.read(C),b''):x.update(q)
 return x.hexdigest()
def resident(fd,n):
 ps=os.sysconf('SC_PAGE_SIZE');k=(n+ps-1)//ps;z=mmap.mmap(fd,n,access=mmap.ACCESS_COPY);v=(ctypes.c_ubyte*k)()
 if ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(ctypes.addressof(ctypes.c_char.from_buffer(z))),ctypes.c_size_t(n),v):raise OSError(ctypes.get_errno(),'mincore')
 r=sum(bool(i&1) for i in v)/k;z.close();return r
def main():
 if h(M)!='74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db' or h(B)!='39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24' or h(Q)!='6626a424176fb47a09cfb6e133e23600514dbca4d16d296eee5f5acedb847506':return 90
 O.mkdir(parents=True,exist_ok=False);W.mkdir();rows=[];n=M.stat().st_size;t=n*75//100
 for bi,order in enumerate(S,1):
  for pi,arm in enumerate(order,1):
   if subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0:return 91
   trial=f'b{bi}-p{pi}-{arm}'
   with open(M,'rb',buffering=0) as f:os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
   time.sleep(2)
   with open(M,'rb',buffering=0) as f:cold=resident(f.fileno(),n)
   if cold>.2:return 92
   st={'read':0,'start':None,'end':None,'err':None}
   def bg():
    try:
     st['start']=time.monotonic();left=t
     with open(M,'rb',buffering=0) as f:
      while left:
       d=f.read(min(C,left));
       if not d:break
       st['read']+=len(d);left-=len(d)
     st['end']=time.monotonic()
    except Exception as e:st['err']=repr(e)
   worker=None;ann=time.monotonic()
   if arm!='none':worker=threading.Thread(target=bg);worker.start()
   if arm=='completed':
    while time.monotonic()<ann+.8:time.sleep(.01)
    if worker.is_alive():return 93
   arrival=time.monotonic();active_at_arrival=bool(worker and worker.is_alive());end_at_arrival=st['end'];bytes_at_arrival=st['read']
   if arm=='concurrent' and not active_at_arrival:return 94
   with open(M,'rb',buffering=0) as f:ready=resident(f.fileno(),n)
   if arm=='completed' and ready<.7:return 95
   launched=time.monotonic();rc=subprocess.run([sys.executable,str(Q),'--binary',str(B),'--model',str(M),'--mode','mmap','--trial',trial,'--output-dir',str(W)],timeout=130).returncode
   if worker:worker.join(10)
   if worker and (worker.is_alive() or st['err'] or st['read']!=t):return 96
   z=json.loads((W/f'{trial}.receipt.json').read_text());z.update({'experiment':'MSIO-CP-E022R1','block':bi,'position':pi,'arm':arm,'cold_fraction':cold,'arrival_resident_fraction':ready,'prefetched_bytes':st['read'],'bytes_at_arrival':bytes_at_arrival,'prefetch_active_at_arrival':active_at_arrival,'background_end_at_arrival':end_at_arrival,'background_complete_s':None if st['end'] is None else st['end']-ann,'arrival_to_ok_s':launched-arrival+z['time_to_ok_s']});(W/f'{trial}.e022r1.json').write_text(json.dumps(z,sort_keys=True)+'\n');rows.append(z)
   if rc or subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0:return 97
   time.sleep(2)
 (O/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n');(O/'COMPLETED').touch();return 0
if __name__=='__main__':sys.exit(main())
