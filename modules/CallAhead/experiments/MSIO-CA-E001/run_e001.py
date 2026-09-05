#!/usr/bin/env python3
import ctypes
import hashlib
import json
import math
import mmap
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

R = Path('/mnt/nvme1/chenhao/modelstateio-runtime')
SERVER = R/'build-d230ddd-cuda116-sm70/bin/llama-server'
CLI = R/'build-d230ddd-cuda116-sm70/bin/llama-cli'
FG = R/'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf'
BG = R/'incoming/qwen2.5-1.5b-instruct-q4_k_m.gguf'
OUT = R/'logs/MSIO-CA-E001'; RAW = OUT/'raw'
LOCK = R/'locks/MSIO-CA-E001.lock'
PORT = 18111
FG_SHA = '74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db'
BG_SHA = '6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e'
FG_SIZE = 491400032; BG_SIZE = 1117320736
CHUNK = 8 << 20
BUDGET = (int(BG_SIZE*.75)//CHUNK)*CHUNK
RATE = 256 << 20
REQUESTS = 160; INTERVAL = .025
ORDERS = [
 ['none','eager75','paced75'], ['eager75','paced75','none'],
 ['paced75','none','eager75'], ['none','paced75','eager75'],
 ['paced75','eager75','none'], ['eager75','none','paced75']]

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(CHUNK),b''):h.update(b)
 return h.hexdigest()

def gpu():
 p=subprocess.run(['nvidia-smi','--query-gpu=index,memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
 rows=[]
 for line in p.stdout.splitlines():
  q=[x.strip() for x in line.split(',')]
  if len(q)==3:rows.append({'index':int(q[0]),'memory_used_mib':int(q[1]),'utilization_pct':int(q[2])})
 return {'returncode':p.returncode,'rows':rows,'stderr':p.stderr[-1024:]}

def meminfo():
 keep={'MemTotal','MemAvailable','Cached','Buffers','SwapTotal','SwapFree'}; out={}
 for line in Path('/proc/meminfo').read_text().splitlines():
  k,v=line.split(':',1)
  if k in keep:out[k]=v.strip()
 return out

def process(pid):
 stat=Path(f'/proc/{pid}/stat').read_text().split(); status={}
 for line in Path(f'/proc/{pid}/status').read_text().splitlines():
  if ':' in line:
   k,v=line.split(':',1)
   if k in {'State','VmRSS','VmHWM','Threads'}:status[k]=v.strip()
 return {'pid':pid,**status,'minflt':int(stat[9]),'majflt':int(stat[11]),'utime_ticks':int(stat[13]),'stime_ticks':int(stat[14])}

def io_stats():
 out={}
 for line in Path('/proc/self/io').read_text().splitlines():
  k,v=line.split(':',1);out[k]=int(v)
 return out

def disk_stats():
 p=Path('/sys/block/nvme1n1/stat')
 return [int(x) for x in p.read_text().split()] if p.exists() else None

def resident(path,n):
 libc=ctypes.CDLL(None,use_errno=True);libc.mmap.restype=ctypes.c_void_p
 fd=os.open(path,os.O_RDONLY)
 try:
  addr=libc.mmap(None,n,1,2,fd,0)
  if addr in (None,ctypes.c_void_p(-1).value):raise OSError(ctypes.get_errno(),'mmap')
  try:
   pages=(n+mmap.PAGESIZE-1)//mmap.PAGESIZE;vec=(ctypes.c_ubyte*pages)()
   if libc.mincore(ctypes.c_void_p(addr),ctypes.c_size_t(n),vec):raise OSError(ctypes.get_errno(),'mincore')
   count=sum(1 for x in vec if x&1)
   return {'pages':pages,'resident_pages':count,'resident_fraction':count/pages}
  finally:libc.munmap(ctypes.c_void_p(addr),ctypes.c_size_t(n))
 finally:os.close(fd)

def drop_bg():
 fd=os.open(BG,os.O_RDONLY)
 try:os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED)
 finally:os.close(fd)
 time.sleep(2)
 return resident(BG,BG_SIZE)

def prepare(arm,state):
 state.update({'start_monotonic':time.monotonic(),'requested_bytes':0 if arm=='none' else BUDGET,'actual_bytes':0,'completed':False,'thread_native_id':threading.get_native_id()})
 if arm=='none':
  state.update({'end_monotonic':time.monotonic(),'duration_s':0.0,'achieved_bps':0.0,'completed':True});return
 fd=os.open(BG,os.O_RDONLY)
 try:
  done=0
  while done<BUDGET:
   b=os.read(fd,min(CHUNK,BUDGET-done))
   if not b:break
   done+=len(b)
   if arm=='paced75':
    target=done/RATE; elapsed=time.monotonic()-state['start_monotonic']
    if target>elapsed:time.sleep(target-elapsed)
  end=time.monotonic(); state.update({'actual_bytes':done,'end_monotonic':end,'duration_s':end-state['start_monotonic'],'achieved_bps':done/(end-state['start_monotonic']),'completed':True})
 except Exception as e:state['exception']=repr(e)
 finally:os.close(fd)

def post():
 payload={'prompt':'Reply with exactly OK.','n_predict':1,'temperature':0.0,'seed':1,'cache_prompt':False}
 q=urllib.request.Request(f'http://127.0.0.1:{PORT}/completion',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
 t=time.monotonic()
 with urllib.request.urlopen(q,timeout=30) as x:
  body=x.read(1<<20); data=json.loads(body)
  return {'http_status':x.status,'latency_s':time.monotonic()-t,'content_present':bool(data.get('content')),'content':data.get('content','')}

def ready():
 until=time.monotonic()+90; last=None
 while time.monotonic()<until:
  try:
   with urllib.request.urlopen(f'http://127.0.0.1:{PORT}/health',timeout=2) as x:
    if x.status==200:return
  except Exception as e:last=repr(e);time.sleep(.5)
 raise RuntimeError('readiness timeout '+str(last))

def probe(label):
 cmd=[str(CLI),'--model',str(BG),'--load-mode','mmap','--single-turn','--simple-io','--no-display-prompt','--prompt','Reply with exactly OK.','--predict','1','--seed','1','--temp','0','--n-gpu-layers','99','--ctx-size','256','--batch-size','64','--threads','4','--threads-batch','4']
 t=time.monotonic();p=subprocess.run(cmd,env={**os.environ,'LD_LIBRARY_PATH':'/usr/local/cuda-11.6/lib64'},stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120);wall=time.monotonic()-t
 (RAW/f'{label}.probe.stdout').write_bytes(p.stdout);(RAW/f'{label}.probe.stderr').write_bytes(p.stderr)
 return {'command':cmd,'returncode':p.returncode,'wall_s':wall,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr),'stdout_nonempty':bool(p.stdout.strip())}

def port_free():
 with socket.socket() as s:s.bind(('127.0.0.1',PORT))

def any_model_process():
 p=subprocess.run(['pgrep','-u',str(os.getuid()),'-x','llama-server'],stdout=subprocess.PIPE)
 q=subprocess.run(['pgrep','-u',str(os.getuid()),'-x','llama-cli'],stdout=subprocess.PIPE)
 return bool(p.stdout.strip() or q.stdout.strip())

def main():
 if OUT.exists() or LOCK.exists():return 90
 LOCK.parent.mkdir(parents=True,exist_ok=True);LOCK.write_text(str(os.getpid())+'\n')
 server=None;log=None;receipt={'experiment_id':'MSIO-CA-E001','started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'orders':ORDERS,'rows':[]};rc=92
 try:
  OUT.mkdir(parents=True);RAW.mkdir();port_free()
  if any_model_process() or not gpu()['rows'] or gpu()['rows'][0]['memory_used_mib']!=0:raise RuntimeError('busy preflight')
  ids={'server':{'size':SERVER.stat().st_size,'sha256':sha(SERVER)},'cli':{'size':CLI.stat().st_size,'sha256':sha(CLI)},'foreground':{'size':FG.stat().st_size,'sha256':sha(FG)},'background':{'size':BG.stat().st_size,'sha256':sha(BG)}};receipt['identities']=ids
  if ids['foreground']!={'size':FG_SIZE,'sha256':FG_SHA} or ids['background']!={'size':BG_SIZE,'sha256':BG_SHA}:raise RuntimeError('model identity mismatch')
  receipt['preflight']={'gpu':gpu(),'meminfo':meminfo(),'disk_stats':disk_stats()}
  log=open(OUT/'server.log','wb');cmd=[str(SERVER),'-m',str(FG),'--host','127.0.0.1','--port',str(PORT),'-ngl','99','-c','512','-np','1','--cache-ram','0']
  receipt['server_command']=cmd;server=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env={**os.environ,'LD_LIBRARY_PATH':'/usr/local/cuda-11.6/lib64'});receipt['server_pid']=server.pid;ready()
  for _ in range(8):post()
  for block,order in enumerate(ORDERS,1):
   for position,arm in enumerate(order,1):
    label=f'b{block:02d}-p{position}-{arm}';cold=drop_bg()
    if cold['resident_fraction']>.20:raise RuntimeError(label+' cold-state failure')
    before={'server':process(server.pid),'self_io':io_stats(),'meminfo':meminfo(),'gpu':gpu(),'disk_stats':disk_stats()}
    prep={};worker=threading.Thread(target=prepare,args=(arm,prep),daemon=True);t0=time.monotonic();worker.start();requests=[]
    for i in range(REQUESTS):
     target=t0+i*INTERVAL;now=time.monotonic()
     if target>now:time.sleep(target-now)
     actual=time.monotonic();row=post();row.update({'index':i,'scheduled_offset_s':i*INTERVAL,'actual_offset_s':actual-t0,'schedule_lag_s':actual-target,'worker_alive_after':worker.is_alive()});requests.append(row)
    worker.join(timeout=30)
    if worker.is_alive():raise RuntimeError(label+' preparation timeout')
    after_prep=resident(BG,BG_SIZE);after={'server':process(server.pid),'self_io':io_stats(),'meminfo':meminfo(),'gpu':gpu(),'disk_stats':disk_stats()}
    pr=probe(label);row={'label':label,'block':block,'position':position,'arm':arm,'cold':cold,'after_preparation':after_prep,'preparation':prep,'requests':requests,'background_probe':pr,'before':before,'after':after}
    (RAW/f'{label}.json').write_text(json.dumps(row,sort_keys=True)+'\n');receipt['rows'].append(row)
    if len(requests)!=REQUESTS or any(x['http_status']!=200 or not x['content_present'] for x in requests):raise RuntimeError(label+' foreground correctness')
    expected=0 if arm=='none' else BUDGET
    if prep.get('exception') or not prep.get('completed') or prep.get('actual_bytes')!=expected:raise RuntimeError(label+' preparation contract')
    if arm=='paced75' and prep['achieved_bps']>RATE*1.10:raise RuntimeError(label+' pacing contract')
    if arm!='none' and after_prep['resident_fraction']<.70:raise RuntimeError(label+' residency contract')
    if pr['returncode'] or not pr['stdout_nonempty'] or pr['stdout_bytes']>1<<20 or pr['stderr_bytes']>1<<20:raise RuntimeError(label+' readiness probe')
    if subprocess.run(['pgrep','-u',str(os.getuid()),'-x','llama-cli'],stdout=subprocess.DEVNULL).returncode==0:raise RuntimeError(label+' residual cli')
  receipt['completed']=True;rc=0
 except Exception as e:receipt['exception']=repr(e);receipt['completed']=False;rc=92
 finally:
  if server is not None and server.poll() is None:
   server.terminate()
   try:server.wait(timeout=20)
   except subprocess.TimeoutExpired:server.kill();server.wait(timeout=10)
  if log:log.close()
  cleanup={'model_process_present':any_model_process(),'gpu':gpu()};receipt['cleanup']=cleanup;receipt['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
  if cleanup['model_process_present'] or not cleanup['gpu']['rows'] or cleanup['gpu']['rows'][0]['memory_used_mib']!=0:
   receipt['completed']=False;receipt['cleanup_failure']=True;rc=93
  if OUT.exists():(OUT/'receipts.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
  try:LOCK.unlink()
  except FileNotFoundError:pass
 return rc

if __name__=='__main__':sys.exit(main())
