#!/usr/bin/env python3
import runpy,sys
from pathlib import Path

d=runpy.run_path('/mnt/nvme1/chenhao/modelstateio-runtime/incoming/run_kvg_e002.py',run_name='kvg_e002')
g=d['main'].__globals__
g['O']=Path('/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-KVG-E002R1')
g['S']=g['O']/'slot-state'
old=g['subprocess'].Popen
def patched(args,**kw):
    i=args.index('--slot-save-path')
    return old(args[:i]+['--cache-ram','0']+args[i:],**kw)
g['subprocess'].Popen=patched
sys.exit(d['main']())
