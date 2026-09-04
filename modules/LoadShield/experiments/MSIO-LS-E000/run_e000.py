#!/usr/bin/env python3
import ctypes, hashlib, json, mmap, os, subprocess, sys, time
from pathlib import Path

ROOT=Path('/mnt/nvme3n1/chenhao/modelstateio-runtime')
FG=ROOT/'models/qwen2.5-0.5b-instruct-q4_k_m.gguf'
BG=ROOT/'models/qwen2.5-7b-instruct-q4_k_m.gguf'
BIN=Path('/home/chenhao/modelstateio-runtime/build/llama.cpp-cuda-12.8/bin/llama-cli')
OUT=ROOT/'logs/MSIO-LS-E000'
SCHEDULE=[('b1','defer'),('b1','overlap'),('b2','overlap'),('b2','defer'),('b3','defer'),('b3','overlap'),('b4','overlap'),('b4','defer'),('b5','defer'),('b5','overlap'),('b6','overlap'),('b6','defer')]
SHA={'fg':'74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db','bg':'2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730'}

def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(8<<20),b''): h.update(b)
    return h.hexdigest()

def resident(fd,n):
    page=os.sysconf('SC_PAGE_SIZE'); pages=(n+page-1)//page
    mm=mmap.mmap(fd,n,access=mmap.ACCESS_COPY); addr=ctypes.addressof(ctypes.c_char.from_buffer(mm)); vec=(ctypes.c_ubyte*pages)()
    if ctypes.CDLL(None,use_errno=True).mincore(ctypes.c_void_p(addr),ctypes.c_size_t(n),vec): raise OSError(ctypes.get_errno(),'mincore')
    count=sum(bool(x&1) for x in vec); mm.close(); return count/pages

def gpu(out):
    return subprocess.run(['nvidia-smi','--query-gpu=timestamp,memory.used,utilization.gpu','--format=csv,noheader'],capture_output=True,text=True).stdout.strip()

def dd(out, tag):
    started=time.monotonic()
    p=subprocess.Popen(['dd',f'if={BG}','of=/dev/null','bs=4M','iflag=direct','status=none'],stdout=subprocess.DEVNULL,stderr=open(out/f'{tag}.dd.stderr','w'))
    return p,started

def fg(out,tag):
    t0=time.monotonic()
    p=subprocess.run([str(BIN),'-m',str(FG),'--load-mode','mmap','-ngl','99','--no-warmup','--single-turn','-n','1','-p','Reply with exactly: R'],capture_output=True,text=True,timeout=150)
    (out/f'{tag}.fg.stdout').write_text(p.stdout); (out/f'{tag}.fg.stderr').write_text(p.stderr)
    return p.returncode,time.monotonic()-t0, any(line=='R' for line in p.stdout.splitlines())

def main():
    if OUT.exists(): raise SystemExit('output_exists')
    if not FG.is_file() or not BG.is_file() or not BIN.is_file() or digest(FG)!=SHA['fg'] or digest(BG)!=SHA['bg']: raise SystemExit('identity_gate')
    if subprocess.run(['nvidia-smi','--query-compute-apps=pid','--format=csv,noheader'],capture_output=True,text=True).stdout.strip(): raise SystemExit('foreign_gpu_process')
    OUT.mkdir(parents=True); rows=[]
    trace=OUT/'direct-open.strace'
    probe=subprocess.run(['strace','-f','-e','trace=openat','-yy','-o',str(trace),'dd',f'if={BG}','of=/dev/null','bs=4M','iflag=direct','count=1','status=none'],timeout=30)
    if probe.returncode or 'O_DIRECT' not in trace.read_text(errors='replace'): raise SystemExit('direct_io_not_effective')
    for block,arm in SCHEDULE:
        tag=f'{block}-{arm}'
        if subprocess.run(['pgrep','-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0: raise SystemExit('residual_llama')
        with FG.open('rb',buffering=0) as f:
            os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED); time.sleep(2); cold=resident(f.fileno(),FG.stat().st_size)
        if cold>0.20: raise SystemExit('foreground_not_cold')
        pre=gpu(OUT); bg_pid=None; bg_start=None; overlap=False
        if arm=='overlap':
            bg,bg_start=dd(OUT,tag); bg_pid=bg.pid; time.sleep(0.05); overlap=bg.poll() is None
            if not overlap: raise SystemExit('background_no_overlap')
        rc,wall,correct=fg(OUT,tag)
        if arm=='defer': bg,bg_start=dd(OUT,tag); bg_pid=bg.pid
        bg_rc=bg.wait(timeout=150); bg_wall=time.monotonic()-bg_start
        post=gpu(OUT)
        row={'block':block,'arm':arm,'foreground_rc':rc,'correct':correct,'foreground_wall_s':wall,'cold_fraction':cold,'background_rc':bg_rc,'background_wall_s':bg_wall,'background_pid':bg_pid,'overlap_verified':overlap,'gpu_pre':pre,'gpu_post':post}
        (OUT/f'{tag}.json').write_text(json.dumps(row,sort_keys=True)+'\n'); rows.append(row)
        if rc or not correct or bg_rc: raise SystemExit('sample_failure')
        time.sleep(2)
    (OUT/'receipts.json').write_text(json.dumps(rows,indent=2,sort_keys=True)+'\n'); (OUT/'COMPLETED').touch()

if __name__=='__main__': main()
