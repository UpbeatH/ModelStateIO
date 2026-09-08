# MSIO-CE-D003 proof-carrying configuration tuning

Status: **local design frozen; no proposal generation or system execution**.
Date: 2026-09-08.

Working paper concept: **Proof-Carrying Configuration Tuning for Model-State
Runtimes**. The name is a research hypothesis, not a novelty claim.

## 1. Research problem

An LLM tuner normally records a requested configuration `x` and an observed
outcome `y`. Model-state runtimes may accept `x` while canonicalizing it,
applying only part of it, applying it at the wrong lifecycle point, or exposing
too little readback to establish what actually ran. The resulting pair
`(x, y)` is then a mislabeled tuning sample.

D003 asks whether a tuner should instead record `(intent, effective state, y)`
only after a typed semantic contract is proven. For example, requested
`n_gpu_layers=999` can legitimately realize the semantic intent "all 42 model
layers offloaded"; raw equality is the wrong test. Conversely, a successful
process start is not proof that a requested I/O path, placement, residency, or
lifecycle order became effective.

The candidate mechanism separates two planes:

1. an LLM proposes a bounded configuration, objective, rationale, and semantic
   intent;
2. a deterministic receipt gate compiles that intent into runtime-specific
   predicates and admits the outcome to tuning history only after effective,
   state-lineage, correctness, cleanup, and rollback receipts satisfy them.

The gate never chooses a performance action. It validates whether the action
that a proposer chose is the action whose outcome may be learned from.

## 2. Evidence reused, and its limits

| Existing artifact | Reused as | Not reused as |
| --- | --- | --- |
| D000, 108 normalized episodes | schema vocabulary, parser fixtures, requested/effective/state separation | prospective prevalence or tuning benefit |
| D001, 12 curated scenarios | development examples of null/harmful counterevidence and veto semantics | model accuracy or generalization |
| D002-TR1-P1, 24 calls | evidence that the tested LLM/API/prompt is unsuitable as the final action selector; motivation for the two-plane design | evidence that DeepSeek is intrinsically conservative or that the new mechanism works |
| E800, E003, E006A, CA-E001 and CSR-E100 receipts | development fixtures for semantic predicates and lifecycle fields | fresh confirmation samples |

All of these outcomes were exposed before D003. They may test code but may not
enter a confirmatory effect estimate.

## 3. Candidate gap and novelty boundary

The hypothesized gap is not "configuration validation" and not "adding an LLM."
It is the contamination of an iterative model-state tuning history when a
syntactically valid, acknowledged request is not equivalent to the effective
physical and lifecycle state attributed to the outcome.

A paper contribution would require all three of the following:

- a nontrivial natural post-acknowledgement affected set across at least two
  independent action families;
- a typed semantic receipt layer that distinguishes benign canonicalization
  from silent non-realization better than schema, acknowledgement, and literal
  equality baselines;
- downstream tuning benefit under equal proposal, execution, and model-call
  budgets, plus held-out confirmation.

Before a paper claim, a primary-source audit must compare the exact mechanism
with safe Bayesian optimization, constrained/autonomic tuning, configuration
validation, control-plane reconciliation, and LLM systems-tuning work. A match
that already joins semantic actuation proof to tuning-history admission is a
novelty No-Go. Absence of a search hit is not novelty evidence.

## 4. Research questions

- **RQ1, affected set:** Among prospectively generated, schema-valid LLM
  proposals, how often does acknowledgement fail to establish the intended
  effective model-state action?
- **RQ2, gate correctness:** Can typed predicates reject silent
  non-realization while admitting benign runtime canonicalization?
- **RQ3, tuning consequence:** Under equal budgets, does receipt-aware history
  reduce simple regret or trials-to-best-valid configuration relative to
  requested-only and acknowledgement-only histories?
- **RQ4, LLM value:** Does the LLM proposer add value beyond a deterministic
  space-filling proposer when both use the same receipt gate?

## 5. Hypotheses

- **H1:** The lower bound of a two-sided 95% Wilson interval for natural
  post-ACK semantic non-realization exceeds 10% in a frozen 30-proposal screen,
  with cases in at least two action families.
- **H2:** The semantic gate has zero silent false admissions and zero false
  rejection of independently verified canonicalizations in the screen.
- **H3:** On held-out blocks, receipt-aware history reduces paired normalized
  simple regret by at least 15% or trials-to-best-valid by at least 25% versus
  the strongest requested/ACK-only baseline, with a prospectively frozen
  paired interval excluding zero.
- **H4:** Any claimed LLM benefit must beat the deterministic proposer using
  the same gate. Failure of H4 removes the LLM-superiority claim but need not
  invalidate H1--H3.

H1--H4 are prospective targets. No current result supports them.

## 6. Semantic action contract

Every proposal declares:

- exact runtime and model-state identity;
- bounded raw parameters and objective;
- a semantic intent independent of the raw spelling;
- required control-plane, physical, semantic, and lineage observations;
- freshness and ordering requirements;
- timeout, correctness, cleanup, fallback, and rollback predicates.

The deterministic gate returns one of:

| Class | Meaning | Enter tuning history? |
| --- | --- | --- |
| `PRECHECK_REJECTED` | unsupported or out-of-range before execution | no |
| `ACK_REJECTED` | runtime rejected the request | no |
| `EFFECTIVE_UNVERIFIED` | required readback missing, stale, or identity-mismatched | no |
| `SEMANTIC_MISMATCH` | observed state violates the intent predicate | no |
| `CANONICALIZED_VERIFIED` | raw value changed but semantic intent is proven | yes |
| `EFFECTIVE_VERIFIED` | requested and effective semantics are proven | yes |
| `OUTCOME_INVALID` | workload failed or correctness failed | no |
| `ROLLBACK_FAILED` / `CLEANUP_FAILED` | terminal state is not proven | no |

Rejected outcomes remain visible in failure accounting; they are not deleted.

## 7. Strong baselines

All baselines see the same proposal, documentation snapshot, action budget,
timeout, and raw observations.

1. schema/range validation only;
2. process success or API acknowledgement only;
3. literal requested-versus-effective equality;
4. typed semantic receipt gate;
5. deterministic space-filling proposer plus the same semantic gate;
6. an offline fully observed oracle, reported only as an upper bound.

The central comparison is 2 versus 4. Baseline 3 tests whether semantic
canonicalization, rather than extra logging alone, is necessary. Baseline 5
prevents an LLM from receiving credit for value supplied by the receipt layer.

## 8. Claim ladder

| Highest passed stage | Permitted statement |
| --- | --- |
| local design/tests | protocol and reference semantics are internally consistent |
| D003-A | a bounded natural proposal set contains a material actuation-label affected set |
| D003-B | receipt-aware attribution changes tuning outcome in one runtime context |
| D003-C | the effect holds on an untouched model/workload context |
| independent context + novelty/ablations | candidate systems-paper evidence exists |

No local validator, historical replay, or fault injection is real-system
performance evidence.

## 9. Immediate stop conditions

Stop the paper route if any of the following occurs:

- post-ACK cases are only invalid syntax caught by the schema baseline;
- H1 fails or all qualifying cases belong to one runtime-specific action;
- literal equality matches the semantic gate after canonicalization is handled;
- relabeling effective state does not change downstream selection or regret;
- a simple deterministic proposer with the same receipts dominates the claimed
  LLM-specific contribution;
- the primary-source audit finds the complete mechanism already established;
- benefit depends on injected faults, outcome-selected cases, or confirmation
  retuning.

If H1 fails, D003 ends as a scientific No-Go and opens only the separately
identified parameter-envelope collection described in `EXPERIMENT_PLAN.md`.
