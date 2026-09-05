#!/usr/bin/env python3
import runpy,sys
from pathlib import Path
d=runpy.run_path('/mnt/nvme1/chenhao/modelstateio-runtime/incoming/run_kvg_e001.py',run_name='kvg_e001');g=d['main'].__globals__
g['O']=Path('/mnt/nvme1/chenhao/modelstateio-runtime/logs/MSIO-KVG-E001R1');g['S']=g['O']/'slot-state'
sys.exit(d['main']())
