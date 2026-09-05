# MSIO-CA-E201 expanded real-trace audit

Date: 2026-09-06. Status: **material No-Go**. This is a second, independent
source qualification for the new branch-debt candidate; it does not replay an
existing experiment or alter the closed E001 threshold.

## Frozen required fields

The candidate requires one lawful source that jointly supplies: at least three
immutable state identities; a program-visible pre-arrival notice; actual
arrival and completion; a dependency or branch; a finite **physical** state
capacity conflict; and a documented source/license/collection procedure.

## Sources inspected

| source | verified useful fields | missing frozen field(s) | decision |
| --- | --- | --- | --- |
| [FineServe](https://github.com/hihiztc1/FineServe) | real desensitized multi-model arrival traces; timestamp and aggregate architecture/scale | per-request immutable model identity, dependency/branch, pre-arrival frontier, residency/bytes and capacity conflict | reject |
| [TraceLab](https://github.com/uw-syfi/TraceLab) | real coding-agent sessions, provider/model fields, ordered tool/LLM events and timing | its public schema has no physical model-state identity/version, capacity/residency event, or capacity-conflict observation; event order alone is not a prospective frontier | reject |
| [AgentTrace](https://github.com/pagarsky/agent-trace) | open Apache-2.0 tool-agent rows with model artifact metadata, spans and timings | the release is partitioned by two model identities, and it has no multi-state capacity/residency conflict or prospective branch frontier | reject |
| [agent-llm-traces](https://huggingface.co/datasets/DiscoPosse/agent-llm-traces) | OpenTelemetry parent spans, timestamps and model identifiers across several providers | no disclosed local model-state bytes/residency/capacity or physical eviction/reload result; hosted provider identifiers cannot be relabelled as local immutable states | reject |

## Established evidence and inference

These materials are useful evidence that real multi-model or program-structured
agent traces now exist. None is the causal input required by CallAhead. In
particular, defining a capacity after observing an event sequence, assigning a
local model file to an observed hosted-model record, or treating a child span
as a pre-arrival notice would introduce information or state not present in the
source.

## Decision

The expanded source set still supplies no lawful, provenance-complete trace
with actual model-state competition. `MSIO-CA-E201` therefore closes the
CallAhead branch-debt/foreground-harm candidate as a **material No-Go**. No
controller, replay or GPU run is justified from these traces.

## Narrow re-entry condition

Only a trace collected prospectively from an executable open workflow that
records the stated frontier and state lifecycle **before** outcomes are opened,
with at least three immutable local state artifacts and a measured finite
capacity conflict, can reopen a new experiment ID.
