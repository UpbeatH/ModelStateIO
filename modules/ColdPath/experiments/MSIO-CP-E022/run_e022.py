#!/usr/bin/env python3
import ctypes, hashlib, json, mmap, os, subprocess, sys, threading, time
from pathlib import Path

ROOT=Path('/mnt/nvme1/chenhao/modelstateio-runtime'); MODEL=ROOT/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf'
BINARY=ROOT/'build-d230ddd-cuda116-sm70/bin/llama-cli'; MEASURE=ROOT/'incoming/measure_once_e007.py'
OUT=ROOT/'logs/MSIO-CP-E022'; RAW=OUT/'raw'; CHUNK=8<<20; ORDERS=[['none','completed','concurrent'],['completed','concurrent','none'],['concurrent','none','completed']]*2

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(CHUNK),b''): h.update(b)
 return h.hexdigest()
def residency(fd,n):
 ps=os.sysconf('SC_PAGE_SIZE'); pages=(n+ps-1)//ps; mm=mmap.mmap(fd,n,access=mmap.ACCESS_COPY); vec=(ctypes.c_ubyte*pages)()
 if ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(ctypes.addressof(ctypes.c_char.from_buffer(mm))),ctypes.c_size_t(n),vec): raise OSError(ctypes.get_errno(),'mincore')
 v=sum(bool(x&1) for x in vec)/pages; mm.close(); return v
def main():
 if sha(MODEL)!='74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db': return 90
 if sha(BINARY)!='39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24': return 91
 if sha(MEASURE)!='6626a424176fb47a09cfb6e133e23600514dbca4d16d296eee5f5acedb847506': return 96
 OUT.mkdir(parents=True,exist_ok=False); RAW.mkdir(); rows=[]; size=MODEL.stat().st_size; target=size*75//100
 for block,order in enumerate(ORDERS,1):
  for position,arm in enumerate(order,1):
   if subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 92
   trial=f'b{block}-p{position}-{arm}'
   with open(MODEL,'rb',buffering=0) as f: os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
   time.sleep(2)
   with open(MODEL,'rb',buffering=0) as f: cold=residency(f.fileno(),size)
   if cold>0.20:return 93
   state={'read':0,'start':None,'end':None,'error':None}
   def prefetch():
    try:
     state['start']=time.monotonic(); remain=target
     with open(MODEL,'rb',buffering=0) as f:
      while remain:
       d=f.read(min(CHUNK,remain))
       if not d: break
       state['read']+=len(d); remain-=len(d)
     state['end']=time.monotonic()
    except Exception as e: state['error']=repr(e)
   announced=time.monotonic(); worker=None
   if arm!='none': worker=threading.Thread(target=prefetch); worker.start()
   if arm=='completed':
    deadline=announced+0.8
    while time.monotonic()<deadline: time.sleep(min(.01,deadline-time.monotonic()))
    if worker.is_alive(): return 94
   arrived=time.monotonic()
   if arm=='concurrent' and not worker.is_alive(): return 95
   with open(MODEL,'rb',buffering=0) as f: ready=residency(f.fileno(),size)
   if arm=='completed' and ready<0.70:return 97
   launched=time.monotonic(); rc=subprocess.run([sys.executable,str(MEASURE),'--binary',str(BINARY),'--model',str(MODEL),'--mode','mmap','--trial',trial,'--output-dir',str(RAW)],timeout=130).returncode
   if worker: worker.join(timeout=10)
   if worker and (worker.is_alive() or state['error'] or state['read']!=target): return 98
   receipt=json.loads((RAW/f'{trial}.receipt.json').read_text()); receipt.update({'experiment':'MSIO-CP-E022','block':block,'position':position,'arm':arm,'cold_fraction':cold,'arrival_resident_fraction':ready,'prefetched_bytes':state['read'],'background_complete_s':None if state['end'] is None else state['end']-announced,'prefetch_active_at_arrival':bool(worker and state['end'] is None),'arrival_to_ok_s':launched-arrived+receipt['time_to_ok_s'],'trigger_to_ok_s':launched-announced+receipt['time_to_ok_s']})
   (RAW/f'{trial}.e022.json').write_text(json.dumps(receipt,sort_keys=True)+'\n'); rows.append(receipt)
   if rc or subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0:return 99
   time.sleep(2)
 (OUT/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n');(OUT/'COMPLETED').touch();return 0
if __name__=='__main__':sys.exit(main())
