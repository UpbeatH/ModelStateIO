# MSIO-CE-D002 pinned-model development run protocol

Status: frozen before model output. Date: 2026-09-08.

## Purpose and boundary

D002 tests whether one pinned Codex model can follow the D001 development
contracts when given positive-only versus counterevidence-aware retrieval.
It is not a live-system experiment and all underlying source outcomes and
scenario oracles are development-exposed. A D002 result can establish prompt
following and decision stability on this curated harness only; it cannot
establish generalization, tuning benefit, novelty, or CCF-B readiness.

No D002 model output exists when this protocol is frozen. The D001 prompt
packet bytes and scorer must remain unchanged after the first model response.

## Frozen model and execution identity

- model: `gpt-5.6-luna`;
- reasoning effort: `high`;
- contexts: independent and fresh for every invocation;
- repetitions: three per condition/scenario;
- conditions: `positive_only` and `counterevidence_aware`;
- scenarios: the twelve frozen D001 scenarios;
- total independent invocations: 72;
- temperature: not exposed by the intended Codex task interface;
- seed: not exposed by the intended Codex task interface.

The executor must record the actual client/app build, date, host, returned
model identity if available, per-call status, latency, and raw response hash.
No substitute model is allowed. A different model requires a separately
confirmed model-switch decision and a new experiment ID.

## Frozen prompt and output contract

Each invocation receives exactly one D001 model-input object. The fixed system
instruction requires one JSON object and forbids assumptions that requested
state equals effective state. The only allowed decision values are `APPLY`,
`PROBE`, and `ABSTAIN`.

Required response fields are:

- `scenario_id`;
- `decision`;
- `cited_card_ids`;
- `effective_state_assessment` in `VERIFIED`, `UNVERIFIED`, `MISMATCH`, or
  `NOT_APPLICABLE`;
- `reason`, limited to 600 characters.

The response may cite only cards present in that invocation. It must not gain
access to D001 oracle files, baseline results, retrieval audit, or another
invocation's messages.

## Failure and stopping policy

- A missing call, wrong model, context reuse, non-JSON response, schema error,
  unknown decision, scenario mismatch, invalid citation, or overlength reason
  is an invalid invocation.
- Do not repair or selectively rerun an invalid invocation under D002. Record
  it and complete other scheduled calls only if the executor can preserve
  independent contexts and exact packet bytes.
- More than three invalid calls in either condition is
  `D002_TECHNICAL_STOP_INVALID_OUTPUT_RATE`.
- Any evidence that an oracle or prior response entered a prompt is
  `D002_TECHNICAL_STOP_LEAKAGE`.
- No prediction may trigger a local or remote system action.

## Frozen development scoring

The scorer reports per condition:

- valid calls;
- exact decision agreement;
- `APPLY`, `PROBE`, and `ABSTAIN` recall;
- premature apply count;
- missed abstain count;
- 3/3 within-scenario stability;
- cited-card validity.

The scenario-level decision is the three-call majority among valid calls. A
scenario with fewer than two valid calls has no majority and is incorrect.

`D002_DEVELOPMENT_MODEL_GO_TO_D003_DESIGN` requires all of:

1. at least 33/36 valid calls in each condition;
2. counterevidence-aware majority agreement at least 10/12;
3. counterevidence-aware abstain recall at least 6/7;
4. zero counterevidence-aware premature applies;
5. at least 10/12 counterevidence-aware scenarios stable 3/3;
6. counterevidence-aware exact agreement at least three scenarios higher than
   positive-only;
7. counterevidence-aware apply recall no lower than positive-only.

Failure is a development No-Go for this prompt/model/harness combination, not
a scientific No-Go for counterevidence-aware tuning.

Even a Go opens only D003 prospective design. D003 must collect new hidden
real-system episodes and cannot reuse D001/D002 accuracy as confirmation.
