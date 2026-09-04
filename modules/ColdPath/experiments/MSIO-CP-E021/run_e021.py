#!/usr/bin/env python3
import ctypes, hashlib, json, mmap, os, subprocess, sys, time
from pathlib import Path

ROOT=Path('/mnt/nvme1/chenhao/modelstateio-runtime'); MODEL=ROOT/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf'
BINARY=ROOT/'build-d230ddd-cuda116-sm70/bin/llama-cli'; MEASURE=ROOT/'incoming/measure_once_e007.py'
OUT=ROOT/'logs/MSIO-CP-E021'; RAW=OUT/'raw'; CHUNK=8<<20; FRACTION=.75
ORDERS=[['none','lead0','lead300','lead700'],['lead0','lead300','lead700','none'],['lead300','lead700','none','lead0'],['lead700','none','lead0','lead300'],['none','lead700','lead300','lead0'],['lead300','lead0','none','lead700']]
DELAYS={'lead0':0.0,'lead300':.300,'lead700':.700}

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(CHUNK),b''): h.update(b)
    return h.hexdigest()

def resident(fd,n):
    ps=os.sysconf('SC_PAGE_SIZE'); pages=(n+ps-1)//ps; mm=mmap.mmap(fd,n,access=mmap.ACCESS_COPY)
    addr=ctypes.addressof(ctypes.c_char.from_buffer(mm)); vec=(ctypes.c_ubyte*pages)()
    if ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(addr),ctypes.c_size_t(n),vec): raise OSError(ctypes.get_errno(),'mincore')
    v=sum(bool(x&1) for x in vec)/pages; mm.close(); return v

def main():
    if sha(MODEL)!='74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db': return 90
    if sha(BINARY)!='39a6fb1233811c9d6bf5d646ec17f810562a9f78eb6a9cb558940479913dbe24': return 91
    if OUT.exists(): return 92
    OUT.mkdir(parents=True); RAW.mkdir(); rows=[]; size=MODEL.stat().st_size; requested=(int(size*FRACTION)//CHUNK)*CHUNK
    for bi,order in enumerate(ORDERS,1):
        for pos,arm in enumerate(order,1):
            if subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 93
            trial=f'b{bi}-p{pos}-{arm}'; worker=None; triggered=None
            with MODEL.open('rb',buffering=0) as f:
                os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED); time.sleep(2); cold=resident(f.fileno(),size)
            if cold>.20: return 94
            if arm!='none':
                triggered=time.monotonic(); worker=subprocess.Popen(['dd',f'if={MODEL}','of=/dev/null','bs=8M',f'count={requested//CHUNK}','status=none'],stdout=subprocess.DEVNULL,stderr=open(OUT/f'{trial}.dd.stderr','w'))
                time.sleep(DELAYS[arm])
            with MODEL.open('rb',buffering=0) as f: at_arrival=resident(f.fileno(),size)
            active=worker is not None and worker.poll() is None
            rc=subprocess.run([sys.executable,str(MEASURE),'--binary',str(BINARY),'--model',str(MODEL),'--mode','mmap','--trial',trial,'--output-dir',str(RAW)],timeout=130).returncode
            receipt=json.loads((RAW/f'{trial}.receipt.json').read_text()); arrival=time.monotonic()
            bg_rc=0; bg_s=0.0
            if worker is not None:
                worker.wait(timeout=60); bg_rc=worker.returncode; bg_s=time.monotonic()-triggered
            receipt.update({'experiment':'MSIO-CP-E021','block':bi,'position':pos,'arm':arm,'lead_s':DELAYS.get(arm,0.0),'prefetched_bytes':requested if arm!='none' else 0,'cold_fraction':cold,'arrival_resident_fraction':at_arrival,'prefetch_active_at_arrival':active,'background_rc':bg_rc,'background_complete_s':bg_s,'trigger_to_ok_s':(arrival-triggered) if triggered else receipt['time_to_ok_s']})
            (RAW/f'{trial}.e021.json').write_text(json.dumps(receipt,sort_keys=True)+'\n'); rows.append(receipt)
            if rc or bg_rc or subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: return 95
            time.sleep(2)
    (OUT/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n'); (OUT/'COMPLETED').touch(); return 0

if __name__=='__main__': sys.exit(main())
