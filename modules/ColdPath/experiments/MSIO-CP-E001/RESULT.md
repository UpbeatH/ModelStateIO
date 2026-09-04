# MSIO-CP-E001 result

## A0 execution

Ten model requests completed and the final unload succeeded, but the recorder emitted pretty-printed multi-line JSON and counted 130 physical lines instead of ten logical records. A0 is therefore a technical post-processing failure. The raw response JSON files remain the immutable evidence source; requests and thresholds must not be rerun or changed to repair this defect.

## A1 reconstruction

The ten raw response files were copied read-only to a local temporary directory. Remote and local SHA-256 values matched for every file. `analyze_e001.py` reconstructed the frozen fields directly from filename identity and response JSON without rerunning a request.

| Metric | Cold | Warm/resident |
|---|---:|---:|
| Load duration, five observations (ms) | 2271.26, 2235.43, 2233.50, 2221.26, 2299.46 | 25.72, 28.44, 28.25, 27.03, 26.14 |
| Median load duration (ms) | 2235.43 | 27.03 |
| Total duration range (ms) | 2354.55–2434.41 | 54.22–56.63 |

Cold/warm median load ratio: 82.72x.

Frozen threshold result: **PASS**. Median cold loading exceeded 1 second and exceeded five times the warm median.

Postflight observation: `ollama ps` was empty, GPU memory usage returned to 4 MiB with 0% sampled utilization, and no owned runner/curl process remained.

## Interpretation and limit

Established current observation: repeated transitions from unloaded to resident `qwen2.5:14b` impose a stable approximately 2.2-second Ollama-reported loading cost on g129, whereas an immediate resident request reports about 27 ms loading time.

Inference: model residency is material enough on this platform to justify a storage-cold/path-feasibility gate.

Not established: Linux page cache was not evicted; only one model/runtime/host was tested; no loading path was changed; no foreground workload ran. This is not evidence that ColdPath beats mmap, readahead, Direct I/O, or the framework default.

Next exact gate: freeze E002 to determine which existing runtime/source can expose at least two genuinely distinct loading paths without system installation or kernel/mount changes. If only Ollama's opaque default path is available, ColdPath must pause or obtain separate dependency-installation authorization.
