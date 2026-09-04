# MSIO-CP-E000 read-only qualification packet

Frozen: 2026-09-04. Operator: primary design agent under explicit user authorization for this named validation.

## Identity and authority

- Module/experiment: `ColdPath / MSIO-CP-E000`.
- Candidate aliases: `g127-chenhao`, `g128-chenhao`, `g129-chenhao`, `g130-chenhao`.
- Authorized: SSH connection and read-only inspection commands below.
- Forbidden: creating/modifying/removing remote files; installing software; starting or killing processes; loading models; running inference/benchmarks; changing GPU, kernel, mount, cache, or storage settings.

## Question and evidence boundary

Question: does any candidate host currently expose an idle V100S-class GPU, an identifiable local NVMe data path, a usable existing LLM runtime/model artifact, and enough free capacity to justify freezing a tiny ColdPath capability experiment?

This task can establish current platform readiness only. It cannot establish loading-path support, correctness, causality, novelty, or performance.

## Mandatory commands

Run independently on each alias with a 30-second SSH connection timeout and no interactive prompts:

```bash
hostname
date -Iseconds
id
nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu,temperature.gpu,power.draw --format=csv,noheader,nounits
nvidia-smi pmon -c 1
uptime
free -h
swapon --show --noheadings
lsblk -b -o NAME,KNAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,MODEL,SERIAL,ROTA
findmnt -rn -o SOURCE,TARGET,FSTYPE,OPTIONS
df -B1 --output=source,target,size,used,avail,fstype
ps -eo pid,user,etimes,pcpu,pmem,comm,args --sort=-pcpu
command -v llama-cli llama-server ollama python3 nvcc
ollama list
find /mnt /data /home/chenhao -maxdepth 4 -type f \( -iname '*.gguf' -o -iname '*.safetensors' -o -iname '*.bin' \) -printf '%p\t%s\t%TY-%Tm-%TdT%TH:%TM:%TS\n'
```

Permission errors from bounded `find` are recorded, not repaired. Do not use `sudo`.

## Stop and selection rules

- Stop a host on SSH failure or identity mismatch.
- Mark busy if GPU utilization is nonzero with an attributable process, or an unrelated high-load job is present.
- Mark storage ambiguous if no local NVMe-backed mounted path can be identified from `lsblk` and `findmnt`.
- Mark artifact-incomplete if no usable runtime or model file can be found without installation/download.
- A host qualifies for capability-packet preparation only when all four conditions are satisfied: idle GPU, identifiable NVMe path, existing runtime, existing model.
- Do not run the capability experiment during E000 even if a host qualifies.

## Return package

Record timestamp, host identity, GPU state, workload state, memory/swap, device-to-mount mapping, free bytes, runtime paths, model artifact paths/sizes, permission gaps, per-host decision, and the exact next gate. Do not copy full process arguments that expose credentials.

