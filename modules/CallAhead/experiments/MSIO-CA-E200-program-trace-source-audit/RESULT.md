# MSIO-CA-E200 program-trace source audit

Status: **material No-Go**. Date: 2026-09-06. This is a source/data
qualification only; it opens no GPU run and does not modify MSIO-CA-E001.

## Frozen admission requirements

The new branch-debt candidate requires a permissively obtainable trace with
at least three immutable state identities, a program-visible notice before
arrival, actual arrival/completion, a dependency or branch field, and a
finite-capacity conflict. It must also disclose source, license/permission and
generation procedure.

## Audited public candidates

- LLMRouterBench documents per-instance query, prompt, raw prediction,
  ground-truth, score, token counts and cost across 33 models, but its stated
  schema contains no program dependency, notice time, actual arrival, state
  bytes/residency or capacity-conflict field. Source:
  https://github.com/ynulihao/LLMRouterBench
- LLMRouter/xRouteBench exposes router training/evaluation pipelines and
  recorded routing outcomes, not a provenance-complete application execution
  trace with the required pre-arrival frontier and state competition. Source:
  https://github.com/ulab-uiuc/LLMRouter
- RouterArena validates model-choice prediction files and may invoke selected
  APIs, but it similarly specifies query/model predictions rather than a
  program dependency or physical-state lifecycle. Source:
  https://github.com/RouteWorks/RouterArena

## Decision

None of the inspected public materials supplies the frozen causal input. Using
their per-query records to reconstruct notice from future arrival or attach
model identities after outcomes would violate the CallAhead information
contract. Therefore this source set is **No-Go** for CallAhead; no download,
replay, controller implementation or GPU experiment is authorized from it.

Re-entry requires a newly identified trace that satisfies every frozen field,
or an openly licensed, executed application workflow whose program frontier
and state identities can be prospectively recorded before its outcomes open.
