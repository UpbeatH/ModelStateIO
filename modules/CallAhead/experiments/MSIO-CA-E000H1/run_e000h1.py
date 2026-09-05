#!/usr/bin/env python3
import ctypes
import hashlib
import json
import mmap
import os
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path('/mnt/nvme1/chenhao/modelstateio-runtime')
BIN = ROOT / 'build-d230ddd-cuda116-sm70/bin/llama-server'
FG = ROOT / 'incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf'
BG = ROOT / 'incoming/qwen2.5-1.5b-instruct-q4_k_m.gguf'
OUT = ROOT / 'logs/MSIO-CA-E000H1'
LOCK = ROOT / 'locks/MSIO-CA-E000H1.lock'
PORT = 18110
FG_SIZE = 491400032
BG_SIZE = 1117320736
FG_SHA = '74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db'
BG_SHA = '6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e'
CHUNK = 8 << 20
BG_BUDGET = (int(BG_SIZE * 0.75) // CHUNK) * CHUNK
RATE_BPS = 256 << 20
LOG_LIMIT = 1 << 20
SERVER_START_TIMEOUT = 90.0
REQUEST_TIMEOUT = 30.0
WHOLE_TIMEOUT = 180.0


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(CHUNK), b''):
            h.update(block)
    return h.hexdigest()


def gpu_snapshot():
    cmd = ['nvidia-smi', '--query-gpu=index,name,memory.used,utilization.gpu',
           '--format=csv,noheader,nounits']
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, timeout=10)
    rows = []
    for line in p.stdout.splitlines():
        parts = [x.strip() for x in line.split(',')]
        if len(parts) == 4:
            rows.append({'index': int(parts[0]), 'name': parts[1],
                         'memory_used_mib': int(parts[2]),
                         'utilization_pct': int(parts[3])})
    return {'returncode': p.returncode, 'rows': rows,
            'stderr': p.stderr[-2048:]}


def meminfo():
    wanted = {'MemTotal', 'MemAvailable', 'Cached', 'Buffers', 'SwapTotal', 'SwapFree'}
    out = {}
    for line in Path('/proc/meminfo').read_text().splitlines():
        key, value = line.split(':', 1)
        if key in wanted:
            out[key] = value.strip()
    return out


def proc_sample(pid):
    status = {}
    for line in Path(f'/proc/{pid}/status').read_text().splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            if k in {'State', 'VmRSS', 'VmHWM', 'Threads'}:
                status[k] = v.strip()
    stat = Path(f'/proc/{pid}/stat').read_text().split()
    return {'pid': pid, **status, 'utime_ticks': int(stat[13]),
            'stime_ticks': int(stat[14])}


def port_free():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', PORT))


def mincore_residency(path, length):
    libc = ctypes.CDLL(None, use_errno=True)
    libc.mmap.restype = ctypes.c_void_p
    libc.mmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int,
                          ctypes.c_int, ctypes.c_int, ctypes.c_long]
    libc.mincore.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                             ctypes.POINTER(ctypes.c_ubyte)]
    libc.munmap.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    prot_read, map_private = 1, 2
    fd = os.open(path, os.O_RDONLY)
    try:
        addr = libc.mmap(None, length, prot_read, map_private, fd, 0)
        if addr in (None, ctypes.c_void_p(-1).value):
            raise OSError(ctypes.get_errno(), 'mmap failed')
        try:
            pages = (length + mmap.PAGESIZE - 1) // mmap.PAGESIZE
            vec = (ctypes.c_ubyte * pages)()
            if libc.mincore(addr, length, vec) != 0:
                raise OSError(ctypes.get_errno(), 'mincore failed')
            resident = sum(1 for x in vec if x & 1)
            return {'pages': pages, 'resident_pages': resident,
                    'resident_fraction': resident / pages}
        finally:
            libc.munmap(addr, length)
    finally:
        os.close(fd)


def post_completion():
    payload = {'prompt': 'Reply with exactly OK.', 'n_predict': 1,
               'temperature': 0.0, 'seed': 1, 'cache_prompt': False}
    req = urllib.request.Request(
        f'http://127.0.0.1:{PORT}/completion',
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json'}, method='POST')
    start = time.monotonic()
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
        body = response.read(LOG_LIMIT + 1)
        if len(body) > LOG_LIMIT:
            raise RuntimeError('response exceeds frozen output cap')
        parsed = json.loads(body)
        return {'http_status': response.status,
                'latency_s': time.monotonic() - start,
                'content_present': bool(parsed.get('content')),
                'content': parsed.get('content', ''),
                'json_keys': sorted(parsed.keys())}


def wait_ready():
    deadline = time.monotonic() + SERVER_START_TIMEOUT
    last = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(
                    f'http://127.0.0.1:{PORT}/health', timeout=2) as r:
                if r.status == 200:
                    return {'http_status': r.status, 'ready_monotonic': time.monotonic()}
        except Exception as exc:
            last = repr(exc)
            time.sleep(0.5)
    raise RuntimeError(f'server readiness timeout: {last}')


def preparation_worker(state):
    state['pid'] = os.getpid()
    state['thread_native_id'] = threading.get_native_id()
    state['start_monotonic'] = time.monotonic()
    fd = os.open(BG, os.O_RDONLY)
    try:
        if hasattr(os, 'posix_fadvise'):
            os.posix_fadvise(fd, 0, BG_BUDGET, os.POSIX_FADV_DONTNEED)
        state['residency_before'] = mincore_residency(BG, BG_BUDGET)
        actual = 0
        while actual < BG_BUDGET:
            block = os.read(fd, min(CHUNK, BG_BUDGET - actual))
            if not block:
                break
            actual += len(block)
            target = actual / RATE_BPS
            elapsed = time.monotonic() - state['start_monotonic']
            if target > elapsed:
                time.sleep(target - elapsed)
        state['actual_bytes'] = actual
        state['end_monotonic'] = time.monotonic()
        state['duration_s'] = state['end_monotonic'] - state['start_monotonic']
        state['achieved_bps'] = actual / state['duration_s']
        state['residency_after'] = mincore_residency(BG, BG_BUDGET)
        state['completed'] = True
    except Exception as exc:
        state['exception'] = repr(exc)
    finally:
        os.close(fd)


def matching_processes():
    p = subprocess.run(['pgrep', '-u', str(os.getuid()), '-f',
                        f'llama-server.*--port {PORT}'], text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return [int(x) for x in p.stdout.split() if x.isdigit()]


def main():
    start = time.monotonic()
    rc = 92
    receipt = {'experiment_id': 'MSIO-CA-E000H1',
               'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               'contract': {'background_budget_bytes': BG_BUDGET,
                            'chunk_bytes': CHUNK, 'rate_ceiling_bps': RATE_BPS,
                            'request_count': 4, 'port': PORT,
                            'whole_timeout_s': WHOLE_TIMEOUT}}
    server = None
    server_log = None
    worker = None
    try:
        if OUT.exists() or LOCK.exists():
            return 90
        LOCK.parent.mkdir(parents=True, exist_ok=True)
        LOCK.write_text(str(os.getpid()) + '\n')
        OUT.mkdir(parents=True)
        port_free()
        if matching_processes():
            raise RuntimeError('matching task server already exists')
        if gpu_snapshot()['rows'][0]['memory_used_mib'] != 0:
            raise RuntimeError('GPU is not idle at preflight')
        identities = {
            'binary': {'path': str(BIN), 'size': BIN.stat().st_size,
                       'sha256': sha256(BIN)},
            'foreground': {'path': str(FG), 'size': FG.stat().st_size,
                           'sha256': sha256(FG)},
            'background': {'path': str(BG), 'size': BG.stat().st_size,
                           'sha256': sha256(BG)}}
        receipt['identities'] = identities
        if identities['foreground']['size'] != FG_SIZE or identities['foreground']['sha256'] != FG_SHA:
            raise RuntimeError('foreground identity mismatch')
        if identities['background']['size'] != BG_SIZE or identities['background']['sha256'] != BG_SHA:
            raise RuntimeError('background identity mismatch')
        receipt['preflight'] = {'gpu': gpu_snapshot(), 'meminfo': meminfo(),
                                'port_free': True}
        server_log = (OUT / 'server.log').open('wb')
        env = {**os.environ, 'LD_LIBRARY_PATH': '/usr/local/cuda-11.6/lib64'}
        cmd = [str(BIN), '-m', str(FG), '--host', '127.0.0.1',
               '--port', str(PORT), '-ngl', '99', '-c', '512', '-np', '1',
               '--cache-ram', '0']
        receipt['server_command'] = cmd
        server = subprocess.Popen(cmd, stdout=server_log,
                                  stderr=subprocess.STDOUT, env=env)
        receipt['server_pid'] = server.pid
        receipt['ready'] = wait_ready()
        receipt['server_sample_ready'] = proc_sample(server.pid)
        prep = {'requested_bytes': BG_BUDGET, 'rate_ceiling_bps': RATE_BPS,
                'completed': False}
        worker = threading.Thread(target=preparation_worker, args=(prep,),
                                  name='callahead-preparation', daemon=True)
        worker.start()
        time.sleep(0.05)
        requests = []
        for index in range(4):
            row = post_completion()
            row['index'] = index
            row['worker_alive_after_request'] = worker.is_alive()
            requests.append(row)
        worker.join(timeout=max(0.0, WHOLE_TIMEOUT - (time.monotonic() - start)))
        if worker.is_alive():
            raise RuntimeError('preparation worker exceeded whole timeout')
        receipt['requests'] = requests
        receipt['preparation'] = prep
        receipt['during'] = {'server': proc_sample(server.pid),
                             'meminfo': meminfo(), 'gpu': gpu_snapshot()}
        if time.monotonic() - start > WHOLE_TIMEOUT:
            raise RuntimeError('whole smoke timeout exceeded')
        if len(requests) != 4 or any(x['http_status'] != 200 or not x['content_present'] for x in requests):
            raise RuntimeError('foreground request contract failed')
        if prep.get('exception') or not prep.get('completed') or prep.get('actual_bytes') != BG_BUDGET:
            raise RuntimeError('preparation byte contract failed')
        if prep['achieved_bps'] > RATE_BPS * 1.10:
            raise RuntimeError('preparation rate contract failed')
        receipt['technical_contract_passed'] = True
        rc = 0
    except Exception as exc:
        receipt['exception'] = repr(exc)
        receipt['technical_contract_passed'] = False
        rc = 92
    finally:
        if server is not None and server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=20)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait(timeout=10)
        if server_log is not None:
            server_log.close()
        receipt['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        receipt['elapsed_s'] = time.monotonic() - start
        cleanup = {'matching_processes': matching_processes(),
                   'gpu': gpu_snapshot()}
        receipt['cleanup'] = cleanup
        if OUT.exists():
            log_path = OUT / 'server.log'
            receipt['logs'] = {'server_log': str(log_path),
                               'server_log_bytes': log_path.stat().st_size if log_path.exists() else None,
                               'limit_bytes': LOG_LIMIT}
            clean_gpu = (cleanup['gpu']['rows'] and
                         cleanup['gpu']['rows'][0]['memory_used_mib'] == 0)
            log_bounded = (receipt['logs']['server_log_bytes'] is not None and
                           receipt['logs']['server_log_bytes'] <= LOG_LIMIT)
            if cleanup['matching_processes'] or not clean_gpu or not log_bounded:
                receipt['technical_contract_passed'] = False
                receipt['cleanup_contract_failed'] = True
                if rc == 0:
                    rc = 93
            try:
                (OUT / 'receipt.json').write_text(
                    json.dumps(receipt, indent=2, sort_keys=True) + '\n')
            except Exception:
                pass
        try:
            LOCK.unlink()
        except FileNotFoundError:
            pass
    return rc


if __name__ == '__main__':
    sys.exit(main())
