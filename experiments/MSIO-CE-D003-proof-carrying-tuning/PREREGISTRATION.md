# MSIO-CE-D003-A preregistration

Status: **frozen locally before proposal generation and before system output**.
Date: 2026-09-08.

## Question

Does a prospectively generated set of schema-valid LLM configuration proposals
contain a material rate of acknowledged actions whose intended model-state
semantics are not proven by effective and state receipts?

## Evidence boundary

D003-A is an affected-set and measurement-validity gate, not a performance
claim. Existing D000--D002 and historical ModelStateIO outcomes are
development-exposed and may be used only to implement parsers and tests.

No proposal has been generated and no D003 system action has occurred at this
freeze. Cluster execution is explicitly unauthorized while the cluster is
occupied by other experiments.

## Frozen proposal generation

- Proposer request: TokenRhythm gateway model `deepseek-v4-pro-0813`, thinking
  enabled and requested high reasoning, with returned model identity recorded.
- Each call is stateless, receives one version-pinned documentation snapshot
  plus one objective/context, emits one JSON action contract, uses no tools,
  and is not retried or repaired.
- Six cells are the cross product of two provenance-complete model-state
  contexts and three objectives: cold-start latency, bounded HBM use, and
  steady request throughput.
- Five independent calls per cell yield 30 scheduled proposal positions.
  Duplicate raw configurations remain scheduled and are counted because
  duplicate effective states are part of the tuning-label question. Invalid
  model output and precheck rejection also remain in the fixed denominator as
  non-post-ACK cases; neither can be selectively replaced.
- Outcomes, D001 oracles, previous proposal responses, and performance results
  are forbidden prompt inputs.
- More than three invalid model outputs is a technical stop. With three or
  fewer, they remain visible and count against, rather than disappear from,
  the fixed 30-position affected-set gate. The packet is not expanded to
  replace them.

The proposal packet and documentation hashes must be frozen in a new execution
task before the first model call. This design file does not authorize those
calls.

## Runtime admission before execution

A future executor must verify, without changing shared state:

1. exact runtime source revision, binary and help-text hashes;
2. two exact model artifact identities and their local ownership;
3. user-private output and cache/state-control roots;
4. all requested parameter surfaces and independent readback channels;
5. zero conflicting experiment process and an explicitly authorized execution
   window.

Admission failure is technical and creates no replacement run. No global cache
drop, service change, driver/toolkit change, install, mount, other-user access,
or PFS action is allowed.

## Prospective action families

At least two of these families must qualify from the frozen runtime interface;
otherwise D003-A is a capability No-Go:

- GPU/model-layer placement intent, verified by total/offloaded layer counts
  and ready-state device memory;
- loading-path intent, verified by runtime logs plus model-file open/mapping
  semantics rather than the requested flag alone;
- file-residency preparation intent, verified by file-scoped page residency
  and byte/rate accounting;
- lifecycle placement/order intent, verified by ordered state-lineage events
  and the resulting context-owned state.

The later execution task must select exact supported parameters without
changing H1 or adding a favorable synthetic action family.

## Trial and truth unit

The prevalence unit is one of the 30 frozen proposal positions. Every
schema-valid proposal is executed once from its frozen pre-state; invalid or
precheck-rejected positions are retained as non-post-ACK cases. A post-ACK
mismatch is repeated once only as a technical reproducibility check; the repeat
does not enter the prevalence denominator.

Independent semantic truth is defined before execution for each action family
using at least one control-plane and one physical or semantic observation. The
gate output is scored against the raw-observation adjudicator, not against its
own class label.

## Primary outcome and decision

Primary outcome is the proportion of the 30 scheduled proposal positions that
are accepted by the runtime but fail their frozen semantic intent predicate.
This conservative pipeline-level denominator prevents invalid or unsupported
LLM outputs from inflating the affected-set rate. Benign canonicalization is
not failure. The two-sided 95% Wilson interval is reported.

`D003_A_GO` requires all of:

1. all 30 proposal positions are accounted and every schema-valid proposal is
   executed without outcome-selected replacement;
2. at least 7/30 are natural post-ACK semantic non-realizations, which is the
   smallest count whose two-sided 95% Wilson lower bound exceeds 10%;
3. qualifying cases span at least two action families and two proposal cells;
4. every mismatch repeat has the same semantic class;
5. the semantic gate has zero false admissions and zero false rejection of an
   independently verified canonicalization;
6. correctness, cleanup, and artifact identity are complete for all trials.

`D003_A_NO_GO_AFFECTED_SET` results if items 2 or 3 fail. A schema-only problem
is also No-Go. Gate-scoring disagreement, missing truth readback, contamination,
or identity/cleanup failure is `D003_A_TECHNICAL_STOP`, not scientific evidence.

The 10% prevalence floor is an engineering materiality target for this fast
screen, not a literature-derived law or a paper efficacy threshold.

## Secondary descriptive outcomes

- invalid output and precheck-rejection rates;
- acknowledgement-only false-admission rate;
- literal-equality false rejection of canonicalized actions;
- duplicate requested and duplicate effective configurations;
- distribution by objective, model context, and action family;
- gate latency and observation overhead;
- all failures and unmatched readbacks.

No subgroup can replace the frozen primary population.
