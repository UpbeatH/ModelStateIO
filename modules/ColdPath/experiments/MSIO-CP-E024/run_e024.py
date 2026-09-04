#!/usr/bin/env python3
import ctypes, hashlib, json, mmap, os, subprocess, sys, threading, time
from pathlib import Path

ROOT=Path('/mnt/nvme1/chenhao/modelstateio-runtime')
MODEL=ROOT/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf'
BINARY=ROOT/'build-d230ddd-cuda116-sm70/bin/llama-cli'
MEASURE=ROOT/'incoming/measure_once_e007.py'
OUT=ROOT/'logs/MSIO-CP-E024'; RAW=OUT/'raw'; CHUNK=8<<20; FRACTION=.75
MODEL_SHA='74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db'
BIN_SHA='39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24'
MEASURE_SHA='6626a424176fb47a09cfb6e133e23600514dbca4d16d296eee5f5acedb847506'
CASES=[('insufficient_known',.6,.6),('early_arrival_error',1.1,.6),('accurate_sufficient',1.1,1.1)]*3
ORDERS=[['none','fixed75','guarded75'],['fixed75','guarded75','none'],['guarded75','none','fixed75']]*3

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for data in iter(lambda:f.read(CHUNK),b''): h.update(data)
    return h.hexdigest()

def resident(fd,n):
    page=os.sysconf('SC_PAGE_SIZE'); pages=(n+page-1)//page
    mm=mmap.mmap(fd,n,access=mmap.ACCESS_COPY); vec=(ctypes.c_ubyte*pages)()
    rc=ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(ctypes.addressof(ctypes.c_char.from_buffer(mm))),ctypes.c_size_t(n),vec)
    if rc: raise OSError(ctypes.get_errno(),'mincore')
    fraction=sum(bool(v&1) for v in vec)/pages; mm.close(); return fraction

def main():
    if sha(MODEL)!=MODEL_SHA or sha(BINARY)!=BIN_SHA or sha(MEASURE)!=MEASURE_SHA: return 90
    if OUT.exists(): return 91
    OUT.mkdir(parents=True); RAW.mkdir(); rows=[]; size=MODEL.stat().st_size; requested=int(size*FRACTION)
    for block,(case,announced,actual) in enumerate(CASES,1):
        for position,arm in enumerate(ORDERS[block-1],1):
            if subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 92
            trial=f'b{block}-p{position}-{case}-{arm}'
            with open(MODEL,'rb',buffering=0) as f: os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
            time.sleep(2)
            with open(MODEL,'rb',buffering=0) as f: cold=resident(f.fileno(),size)
            if cold>.20: return 93
            trigger = arm=='fixed75' or (arm=='guarded75' and announced>=1.0)
            state={'read':0,'start':None,'end':None,'error':None}
            def prefetch():
                try:
                    state['start']=time.monotonic(); left=requested
                    with open(MODEL,'rb',buffering=0) as f:
                        while left:
                            chunk=f.read(min(CHUNK,left))
                            if not chunk: raise RuntimeError('short read')
                            state['read']+=len(chunk); left-=len(chunk)
                    state['end']=time.monotonic()
                except Exception as exc: state['error']=repr(exc)
            notice=time.monotonic(); worker=None
            if trigger: worker=threading.Thread(target=prefetch); worker.start()
            while time.monotonic()<notice+actual: time.sleep(.005)
            arrival=time.monotonic(); active=bool(worker and worker.is_alive()); bytes_at_arrival=state['read']; end_at_arrival=state['end']
            with open(MODEL,'rb',buffering=0) as f: arrival_resident=resident(f.fileno(),size)
            launched=time.monotonic()
            rc=subprocess.run([sys.executable,str(MEASURE),'--binary',str(BINARY),'--model',str(MODEL),'--mode','mmap','--trial',trial,'--output-dir',str(RAW)],timeout=130).returncode
            if worker: worker.join(30)
            if worker and (worker.is_alive() or state['error'] or state['read']!=requested): return 94
            receipt=json.loads((RAW/f'{trial}.receipt.json').read_text())
            receipt.update({'experiment':'MSIO-CP-E024','block':block,'position':position,'case':case,'arm':arm,'announced_lead_s':announced,'actual_lead_s':actual,'lead_error_s':actual-announced,'policy_triggered':trigger,'prefetched_bytes':state['read'],'bytes_at_arrival':bytes_at_arrival,'cold_fraction':cold,'arrival_resident_fraction':arrival_resident,'prefetch_active_at_arrival':active,'background_end_at_arrival':end_at_arrival,'background_complete_s':None if state['end'] is None else state['end']-notice,'arrival_to_ok_s':launched-arrival+receipt['time_to_ok_s'],'trigger_to_ok_s':time.monotonic()-notice})
            (RAW/f'{trial}.e024.json').write_text(json.dumps(receipt,sort_keys=True)+'\n'); rows.append(receipt)
            if rc or subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 95
            time.sleep(2)
    (OUT/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n'); (OUT/'COMPLETED').touch(); return 0

if __name__=='__main__': sys.exit(main())
