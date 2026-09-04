#!/usr/bin/env python3
import ctypes, hashlib, json, mmap, os, subprocess, sys, time
from pathlib import Path
ROOT=Path('/mnt/nvme1/chenhao/modelstateio-runtime'); MODEL=ROOT/'incoming/qwen2.5-7b-instruct-q4_k_m.gguf'; BIN=ROOT/'build-d230ddd-cuda116-sm70/bin/llama-cli'; MEASURE=ROOT/'incoming/measure_once_e007.py'; OUT=ROOT/'logs/MSIO-CP-E022'; RAW=OUT/'raw'; CHUNK=8<<20; LEAD=3.5
ORDERS=[['none','lead3500'],['lead3500','none'],['none','lead3500'],['lead3500','none'],['none','lead3500'],['lead3500','none']]
def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(CHUNK),b''): h.update(b)
 return h.hexdigest()
def resident(fd,n):
 page=os.sysconf('SC_PAGE_SIZE'); pages=(n+page-1)//page; mm=mmap.mmap(fd,n,access=mmap.ACCESS_COPY); a=ctypes.addressof(ctypes.c_char.from_buffer(mm)); v=(ctypes.c_ubyte*pages)()
 if ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(a),ctypes.c_size_t(n),v): raise OSError(ctypes.get_errno(),'mincore')
 x=sum(bool(z&1) for z in v)/pages; mm.close(); return x
def main():
 if digest(MODEL)!='2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730': return 90
 if digest(BIN)!='39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24' or digest(MEASURE)!='6626a424176fb47a09cfb6e133e23600514dbca4d16d296eee5f5acedb847506': return 91
 if OUT.exists(): return 92
 OUT.mkdir(parents=True); RAW.mkdir(); n=MODEL.stat().st_size; target=int(n*.75); rows=[]
 for block,order in enumerate(ORDERS,1):
  for pos,arm in enumerate(order,1):
   if subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 93
   trial=f'b{block}-p{pos}-{arm}'
   with open(MODEL,'rb',buffering=0) as f:
    os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED); time.sleep(2); cold=resident(f.fileno(),n)
    if cold>.20: return 94
    prep=0.; ready=cold
    if arm=='lead3500':
     t=time.monotonic(); done=0
     while done<target:
      b=f.read(min(CHUNK,target-done))
      if not b: break
      done+=len(b)
     prep=time.monotonic()-t; ready=resident(f.fileno(),n)
     if done!=target or ready<.70 or prep>LEAD: return 95
     time.sleep(LEAD-prep)
   rc=subprocess.run([sys.executable,str(MEASURE),'--binary',str(BIN),'--model',str(MODEL),'--mode','mmap','--trial',trial,'--output-dir',str(RAW)],timeout=180).returncode
   rec=json.loads((RAW/f'{trial}.receipt.json').read_text()); rec.update({'experiment':'MSIO-CP-E022','block':block,'position':pos,'arm':arm,'lead_s':LEAD if arm=='lead3500' else 0.,'prefetched_bytes':target if arm=='lead3500' else 0,'cold_fraction':cold,'ready_fraction':ready,'prefetch_s':prep}); (RAW/f'{trial}.e022.json').write_text(json.dumps(rec,sort_keys=True)+'\n'); rows.append(rec)
   if rc or subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 96
   time.sleep(2)
 (OUT/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n'); (OUT/'COMPLETED').touch(); return 0
if __name__=='__main__': sys.exit(main())
