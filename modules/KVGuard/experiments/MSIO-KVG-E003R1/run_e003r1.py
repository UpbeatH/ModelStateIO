#!/usr/bin/env python3
import runpy, sys
from pathlib import Path

d = runpy.run_path('/mnt/nvme1/chenhao/modelstateio-runtime/incoming/run_kvg_e003.py', run_name='kvg_e003')
g = d['main'].__globals__
g['O'] = Path('/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-KVG-E003R1')

old_popen = g['subprocess'].Popen
def patched_popen(args, **kw):
    if args and str(args[0]).endswith('llama-server'):
        args = [x for x in args if x != '--no-cache-prompt']
    return old_popen(args, **kw)
g['subprocess'].Popen = patched_popen

old_post = g['post']
current_prefix = {'value': None}
def patched_post(path, payload):
    payload = dict(payload)
    if path == '/completion':
        payload['cache_prompt'] = True
        if payload.get('id_slot') == 1 and payload.get('n_predict') == 0:
            current_prefix['value'] = payload['prompt']
        elif payload.get('id_slot') == 0 and payload.get('prompt') == ' Continue with exactly OK.':
            if current_prefix['value'] is None:
                raise RuntimeError('missing base prefix before restore')
            payload['prompt'] = current_prefix['value'] + payload['prompt']
    return old_post(path, payload)
g['post'] = patched_post
sys.exit(d['main']())
