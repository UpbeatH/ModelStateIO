# MSIO-CE-D003 experiment and paper plan

Status: local plan frozen; no model call, remote audit, or experiment executed.

## Stage 0: completed local design work

- preserve D000--D002 as development-only evidence;
- freeze the research question, semantic contract, D003-A population, and
  Go/No-Go rule;
- validate only the reference gate semantics and packet consistency.

This stage produces no system or performance evidence.

## Stage 1: D003-A proposal/actuation affected-set screen

When the cluster is available and execution is separately authorized:

1. freeze a six-cell, 30-call proposal packet and raw-response destination;
2. conduct a read-only runtime/model/action-surface admission;
3. account for all 30 proposal positions and execute every schema-valid
   candidate in frozen order from its verified pre-state;
4. retain all acknowledgement, effective, physical, semantic, outcome,
   rollback, and cleanup receipts;
5. score once with the frozen adjudicator and Wilson interval.

Expected wall-clock after an execution window exists: one half day for packet
and admission, one half to one day for execution and one day for audit/analysis.
Do not schedule a larger matrix before the D003-A decision.

## Stage 2: D003-B tuning-consequence gate, conditional on D003-A Go

### Material

- keep the two D003-A contexts for development;
- add one provenance-complete held-out model or materially different workload;
- freeze a candidate bank before opening its outcomes;
- use two capacity/load strata and three counterbalanced blocks per stratum;
- each policy receives the same maximum of eight executed candidates per block,
  the same candidate bank, observations, timeout, and model-call budget.

### Compared policies

1. LLM proposer with requested/ACK-only history;
2. LLM proposer with typed semantic receipt history;
3. deterministic space-filling proposer with typed semantic receipt history;
4. full-bank oracle as a non-deployable upper bound.

Schema and literal-equality variants are scored as ablations without receiving
extra executions. Policy state is reset between blocks. Block order is
counterbalanced and fixed before outcomes.

### Outcomes

- primary: normalized simple regret of the final selected configuration among
  independently verified configurations;
- co-primary alternative declared before execution: trials-to-best-valid
  configuration;
- silent false admissions, invalid-history fraction, duplicate-effective-state
  waste, TTFT/p95, throughput, HBM/DRAM use, load bytes/time, correctness,
  gate overhead, and cleanup failures.

`D003_B_GO` requires H3, zero silent false admissions, complete correctness,
and gate CPU/wall overhead no greater than 2% of the measured end-to-end trial
time. A larger overhead may be reported but fails this fast gate.

If the receipt-aware LLM arm does not beat requested/ACK-only history, stop.
If it beats ACK-only but not the deterministic receipt-aware proposer, retain
only the generic actuation-aware tuning claim and remove LLM superiority.

## Stage 3: D003-C untouched confirmation and paper gate

Only after D003-B Go:

- freeze one new model family or runtime context before inspecting outcomes;
- reuse the D003-B mechanism and thresholds without confirmation retuning;
- include at least three objectives/workload structures and two capacity
  pressure strata overall;
- reproduce at least half the primary D003-B effect and at least a 10%
  improvement over the strongest deployable baseline in the independent
  context;
- complete typed-receipt ablations, overhead attribution, failure analysis,
  and a primary-source novelty review;
- release compact receipts, manifests, analysis, tables, and plotting code;
  keep raw logs/models externally with verified hashes.

Only D003-A through D003-C plus an independent context and cleared novelty can
support a CCF-B-targeted manuscript. D000--D002 remain motivation/development
and are not pooled into confirmatory intervals.

## No-Go fallback: D004 parameter envelope

If D003-A is `NO_GO_AFFECTED_SET`, do not tune the threshold or inject faults.
Preserve the 30 proposal receipts and open a new-ID exploratory collection only
after a separate freeze and execution authorization.

The D004 purpose is data accumulation, anomaly discovery, and upper/lower
performance-envelope mapping, not rescue of D003. The initial bounded design is:

- factors: supported loading mode, effective GPU-layer fraction, context size,
  batch size, and thread count;
- three provenance-complete model states if locally available;
- 12 deterministic space-filling configurations per model, followed by one
  repeat of every provisional top-2, bottom-2, failure, or effective-state
  anomaly; no outcome-based replacement beyond these frozen repeat rules;
- responses: TTFT, p50/p95 request time, throughput, load time/bytes,
  CPU/RSS, HBM, correctness, requested/effective mapping, and failure class;
- report median and full range by model, robust upper/lower envelopes, duplicate
  effective configurations, discontinuities, and all anomalous receipts.

D004 may generate a new phenomenon lead only if an anomaly repeats, has a
physical/state receipt, is not explained by a direct fixed defect, and appears
in at least two model contexts. Otherwise it remains a reusable tuning dataset.

## Fast submission path after evidence Go

The fastest defensible sequence after cluster availability is:

1. D003-A decision in 2--3 working days;
2. D003-B implementation and execution in 5--7 working days;
3. novelty audit and D003-C packet in parallel with D003-B analysis;
4. untouched confirmation and robustness in 1--2 weeks;
5. figures, manuscript skeleton, and artifact audit in 2 weeks;
6. select the nearest verified CCF-B venue only after the evidence level and
   official deadline are checked.

Failure at any gate immediately switches to D004 or another portfolio line;
it does not consume the full paper schedule.
