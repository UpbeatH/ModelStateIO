# StateTier decision

Decision date: 2026-09-04.

## `NO-GO`: unified multi-state StateTier on the current platform

The route required evidence that at least two independently distinguishable
model-state classes could be observed and controlled under capacity pressure.
T001 found no verified multi-state trace. T001's HTTP diagnostic established a
real cold/warm weight lifecycle, and T002 established model residency plus an
API context array, but `/api/ps` exposed no KV size, residency tier, eviction,
migration, adapter, or expert event. The two `ollama run` probes timed out and
the API probes cannot expose a second storage-managed state class.

Because the preregistered stop rule was “stop if no second class can be
observed,” the unified StateTier hypothesis is **No-Go** for this platform and
runtime. No performance claim, cross-runtime claim, or general impossibility
claim follows.

## Reusable bounded alternative

A future `WeightResidency` study may measure cold/warm model-weight loading,
but it must be a new research question with new novelty analysis, baselines,
and thresholds. It cannot inherit the StateTier multi-state claim or consume
cluster priority automatically.

