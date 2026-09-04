#!/usr/bin/env python3
import argparse, json, os, subprocess, time
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--phase', choices=('before', 'after'), required=True)
    p.add_argument('--trial', required=True)
    p.add_argument('--settle-index', type=int, required=True)
    p.add_argument('--status', type=int, required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    raw = subprocess.run(['pgrep', '-a', '-u', str(os.getuid()), '-f', '[l]lama-cli'], capture_output=True, text=True).stdout
    processes = []
    for line in raw.splitlines():
        parts = line.split(maxsplit=1)
        processes.append({'pid': int(parts[0]), 'cmd': parts[1] if len(parts) > 1 else ''})
    gpu = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,utilization.gpu', '--format=csv,noheader'], capture_output=True, text=True).stdout.strip()
    receipt = {'timestamp_ns': time.time_ns(), 'phase': a.phase, 'trial': a.trial, 'settle_index': a.settle_index, 'command_status': a.status, 'processes': processes, 'gpu': gpu, 'decision': 'SETTLED' if not processes else 'PROCESS_PRESENT'}
    Path(a.output).write_text(json.dumps(receipt, sort_keys=True) + '\n', encoding='utf-8')
    return 0 if not processes else 1

if __name__ == '__main__':
    raise SystemExit(main())

