#!/usr/bin/env python3
import ctypes,hashlib,json,mmap,os,subprocess,sys,threading,time
from pathlib import Path
R=Path('/mnt/nvme1/chenhao/modelstateio-runtime');M=R/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf';B=R/'build-d230ddd-cuda116-sm70/bin/llama-cli';Q=R/'incoming/measure_once_e007.py';O=R/'logs/MSIO-CP-E025';W=O/'raw';C=8<<20
H=['74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db','39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24','6626a424176fb47a09cfb6e133e23600514dbca4d16d296eee5f5acedb847506'];ORD=[['none','fixed75'],['fixed75','none']]*3
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for x in iter(lambda:f.read(C),b''):h.update(x)
 return h.hexdigest()
def resident(fd,n):
 p=os.sysconf('SC_PAGE_SIZE');k=(n+p-1)//p;m=mmap.mmap(fd,n,access=mmap.ACCESS_COPY);v=(ctypes.c_ubyte*k)()
 if ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(ctypes.addressof(ctypes.c_char.from_buffer(m))),ctypes.c_size_t(n),v):raise OSError(ctypes.get_errno(),'mincore')
 z=sum(bool(x&1) for x in v)/k;m.close();return z
def main():
 if [sha(M),sha(B),sha(Q)]!=H:return 90
 if O.exists():return 91
 O.mkdir(parents=True);W.mkdir();rows=[];n=M.stat().st_size;t=n*75//100
 for bi,order in enumerate(ORD,1):
  for pi,arm in enumerate(order,1):
   if subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0:return 92
   trial=f'b{bi}-p{pi}-{arm}'
   with open(M,'rb',buffering=0) as f:os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
   time.sleep(2)
   with open(M,'rb',buffering=0) as f:cold=resident(f.fileno(),n)
   if cold>.2:return 93
   st={'read':0,'end':None,'err':None}
   def bg():
    try:
     left=t
     with open(M,'rb',buffering=0) as f:
      while left:
       d=f.read(min(C,left))
       if not d:raise RuntimeError('short read')
       st['read']+=len(d);left-=len(d)
     st['end']=time.monotonic()
    except Exception as e:st['err']=repr(e)
   notice=time.monotonic();worker=None
   if arm=='fixed75':worker=threading.Thread(target=bg);worker.start()
   while time.monotonic()<notice+.1:time.sleep(.002)
   arrival=time.monotonic();active=bool(worker and worker.is_alive());bytes_at=st['read'];end_at=st['end']
   with open(M,'rb',buffering=0) as f:ready=resident(f.fileno(),n)
   launch=time.monotonic();rc=subprocess.run([sys.executable,str(Q),'--binary',str(B),'--model',str(M),'--mode','mmap','--trial',trial,'--output-dir',str(W)],timeout=130).returncode
   if worker:worker.join(30)
   if worker and(worker.is_alive() or st['err'] or st['read']!=t):return 94
   z=json.loads((W/f'{trial}.receipt.json').read_text());z.update({'experiment':'MSIO-CP-E025','block':bi,'position':pi,'arm':arm,'announced_lead_s':1.1,'actual_lead_s':.1,'lead_error_s':-1.0,'policy_triggered':arm=='fixed75','prefetched_bytes':st['read'],'bytes_at_arrival':bytes_at,'cold_fraction':cold,'arrival_resident_fraction':ready,'prefetch_active_at_arrival':active,'background_end_at_arrival':end_at,'background_complete_s':None if st['end'] is None else st['end']-notice,'arrival_to_ok_s':launch-arrival+z['time_to_ok_s'],'trigger_to_ok_s':time.monotonic()-notice});(W/f'{trial}.e025.json').write_text(json.dumps(z,sort_keys=True)+'\n');rows.append(z)
   if rc or subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0:return 95
   time.sleep(2)
 (O/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n');(O/'COMPLETED').touch();return 0
if __name__=='__main__':sys.exit(main())
