#!/usr/bin/env python3
import ctypes, hashlib, json, mmap, os, subprocess, sys, time
from pathlib import Path

ROOT=Path('/mnt/nvme1/chenhao/modelstateio-runtime'); MODEL=ROOT/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf'
BINARY=ROOT/'build-d230ddd-cuda116-sm70/bin/llama-cli'; MEASURE=ROOT/'incoming/measure_once_e007.py'
OUT=ROOT/'logs/MSIO-CP-E019'; RAW=OUT/'raw'; CHUNK=8<<20
ORDERS=[[0,25,50,75,100],[25,50,75,100,0],[50,75,100,0,25],[75,100,0,25,50],[100,0,25,50,75],[100,75,50,25,0]]

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(CHUNK),b''): h.update(b)
    return h.hexdigest()

def residency(fd,n):
    ps=os.sysconf('SC_PAGE_SIZE'); pages=(n+ps-1)//ps; mm=mmap.mmap(fd,n,access=mmap.ACCESS_COPY)
    addr=ctypes.addressof(ctypes.c_char.from_buffer(mm)); vec=(ctypes.c_ubyte*pages)()
    if ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(addr),ctypes.c_size_t(n),vec): raise OSError(ctypes.get_errno(),'mincore')
    result=sum(bool(x&1) for x in vec)/pages; mm.close(); return result

def main():
    if sha(MODEL)!='74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db': return 90
    if sha(BINARY)!='39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24': return 91
    OUT.mkdir(parents=True,exist_ok=False); RAW.mkdir(); rows=[]; size=MODEL.stat().st_size
    for bi,order in enumerate(ORDERS,1):
        for pos,pct in enumerate(order,1):
            if subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 92
            trial=f'b{bi}-p{pos}-f{pct:03d}'
            with open(MODEL,'rb',buffering=0) as f:
                os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED); time.sleep(2)
                cold=residency(f.fileno(),size)
                if cold>0.20: return 93
                remaining=size*pct//100; started=time.monotonic()
                while remaining:
                    data=f.read(min(CHUNK,remaining))
                    if not data: break
                    remaining-=len(data)
                prep=time.monotonic()-started; ready=residency(f.fileno(),size)
                if pct and ready+0.05<pct/100: return 94
            rc=subprocess.run([sys.executable,str(MEASURE),'--binary',str(BINARY),'--model',str(MODEL),'--mode','mmap','--trial',trial,'--output-dir',str(RAW)],timeout=130).returncode
            receipt=json.loads((RAW/f'{trial}.receipt.json').read_text())
            receipt.update({'experiment':'MSIO-CP-E019','block':bi,'position':pos,'fraction':pct/100,'prefetched_bytes':size*pct//100,'cold_fraction':cold,'ready_fraction':ready,'prefetch_s':prep})
            (RAW/f'{trial}.e019.json').write_text(json.dumps(receipt,sort_keys=True)+'\n'); rows.append(receipt)
            if rc or subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 95
            time.sleep(2)
    (OUT/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n'); (OUT/'COMPLETED').touch(); return 0

if __name__=='__main__': sys.exit(main())
