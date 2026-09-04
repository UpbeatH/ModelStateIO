#!/usr/bin/env python3
import ctypes, hashlib, json, mmap, os, subprocess, sys, time
from pathlib import Path

ROOT=Path('/mnt/nvme1/chenhao/modelstateio-runtime')
MODEL=ROOT/'incoming/qwen2.5-7b-instruct-q4_k_m.gguf'
BIN=ROOT/'build-d230ddd-cuda116-sm70/bin/llama-cli'
MEASURE=ROOT/'incoming/measure_once_e007.py'
OUT=ROOT/'logs/MSIO-CP-E023'; RAW=OUT/'raw'; CHUNK=8<<20; LEAD=3.5
ORDERS=[['none','lead3500'],['lead3500','none']]*3

def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(CHUNK),b''): h.update(block)
 return h.hexdigest()

def resident(fd,n):
 page=os.sysconf('SC_PAGE_SIZE'); pages=(n+page-1)//page
 mm=mmap.mmap(fd,n,access=mmap.ACCESS_COPY)
 address=ctypes.addressof(ctypes.c_char.from_buffer(mm)); vec=(ctypes.c_ubyte*pages)()
 if ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(address),ctypes.c_size_t(n),vec):
  raise OSError(ctypes.get_errno(),'mincore')
 fraction=sum(bool(value&1) for value in vec)/pages; mm.close(); return fraction

def main():
 if digest(MODEL)!='2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730': return 90
 if digest(BIN)!='39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24': return 91
 if digest(MEASURE)!='6626a424176fb47a09cfb6e133e23600514dbca4d16d296eee5f5acedb847506': return 92
 if OUT.exists(): return 93
 OUT.mkdir(parents=True); RAW.mkdir(); size=MODEL.stat().st_size; target=int(size*.75); rows=[]
 for block,order in enumerate(ORDERS,1):
  for position,arm in enumerate(order,1):
   if subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 94
   trial=f'b{block}-p{position}-{arm}'
   with open(MODEL,'rb',buffering=0) as f:
    os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED); time.sleep(2); cold=resident(f.fileno(),size)
    if cold>.20: return 95
    prep=0.; ready=cold
    if arm=='lead3500':
     started=time.monotonic(); done=0
     while done<target:
      data=f.read(min(CHUNK,target-done))
      if not data: break
      done+=len(data)
     prep=time.monotonic()-started; ready=resident(f.fileno(),size)
     if done!=target or ready<.70 or prep>LEAD: return 96
     time.sleep(LEAD-prep)
   rc=subprocess.run([sys.executable,str(MEASURE),'--binary',str(BIN),'--model',str(MODEL),'--mode','mmap','--trial',trial,'--output-dir',str(RAW)],timeout=180).returncode
   receipt=json.loads((RAW/f'{trial}.receipt.json').read_text())
   receipt.update({'experiment':'MSIO-CP-E023','block':block,'position':position,'arm':arm,'lead_s':LEAD if arm=='lead3500' else 0.,'prefetched_bytes':target if arm=='lead3500' else 0,'cold_fraction':cold,'ready_fraction':ready,'prefetch_s':prep})
   (RAW/f'{trial}.e023.json').write_text(json.dumps(receipt,sort_keys=True)+'\n'); rows.append(receipt)
   if rc or subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 97
   time.sleep(2)
 (OUT/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n'); (OUT/'COMPLETED').touch(); return 0

if __name__=='__main__': sys.exit(main())
