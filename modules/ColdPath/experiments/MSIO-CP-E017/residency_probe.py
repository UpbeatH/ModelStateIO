#!/usr/bin/env python3
import ctypes
import hashlib
import json
import mmap
import os
import subprocess
import sys
import time
from pathlib import Path

MODEL = Path("/mnt/nvme1/chenhao/modelstateio-runtime/incoming/qwen2.5-0.5b-instruct-q4_k_m.gguf")
EXPECTED = "74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db"
CHUNK = 8 * 1024 * 1024

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()

def resident(fd, length):
    page = os.sysconf("SC_PAGE_SIZE")
    pages = (length + page - 1) // page
    mm = mmap.mmap(fd, length, access=mmap.ACCESS_COPY)
    address = ctypes.addressof(ctypes.c_char.from_buffer(mm))
    vec = (ctypes.c_ubyte * pages)()
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.mincore(ctypes.c_void_p(address), ctypes.c_size_t(length), vec) != 0:
        raise OSError(ctypes.get_errno(), "mincore")
    count = sum(1 for value in vec if value & 1)
    mm.close()
    return count, pages

def main():
    if subprocess.run(["pgrep", "-x", "llama-cli"], stdout=subprocess.DEVNULL).returncode == 0:
        raise SystemExit("llama-cli present")
    st = MODEL.stat()
    if not MODEL.is_file() or st.st_uid != os.getuid() or digest(MODEL) != EXPECTED:
        raise SystemExit("identity gate failed")
    with MODEL.open("rb", buffering=0) as f:
        before, pages = resident(f.fileno(), st.st_size)
        os.posix_fadvise(f.fileno(), 0, 0, os.POSIX_FADV_DONTNEED)
        time.sleep(2)
        cold, _ = resident(f.fileno(), st.st_size)
        while f.read(CHUNK):
            pass
        time.sleep(1)
        warm, _ = resident(f.fileno(), st.st_size)
    result = {"experiment":"MSIO-CP-E017", "bytes":st.st_size, "pages":pages,
              "resident_before":before, "resident_after_dontneed":cold,
              "resident_after_prefetch":warm,
              "cold_fraction":cold/pages, "prefetch_fraction":warm/pages}
    result["decision"] = "PASS" if cold/pages <= 0.20 and warm/pages >= 0.80 else "NO_GO"
    print(json.dumps(result, sort_keys=True))
    return 0 if result["decision"] == "PASS" else 3

if __name__ == "__main__":
    sys.exit(main())
