# MSIO-CE-D001 counterevidence evaluator protocol

Status: frozen local development evaluation. Date: 2026-09-08.

## Question

Can a locally auditable evaluator preserve the distinction between positive,
null, harmful, technical-only, and scope-limited historical evidence when it
forms `apply`, `probe`, or `abstain` decisions under an explicit decision
contract?

D001 is a harness and corpus sanity gate. All source outcomes were already
known, and the scenario contracts and oracles are development-exposed. It is
not an LLM evaluation, an independent test, a novelty result, or evidence that
counterevidence retrieval improves a live system.

## Decision semantics

- `apply`: the candidate action meets the scenario's stated benefit and safety
  contract in the exact represented scope.
- `probe`: actuation is technically plausible, but a required state,
  applicability field, common timestamp, uncertainty bound, or distinguishing
  observation is absent.
- `abstain`: matching evidence is null or harmful under the stated threshold,
  the action is semantically inconsistent, or the proposed justification is a
  direct fixed defect rather than a correct-backend policy opportunity.

These decisions are local labels for development scenarios. They do not grant
authority to change a system.

## Frozen scenarios

Twelve scenarios cover:

1. eager preparation under an explicit readiness target and foreground-harm
   budget;
2. pacing necessity under the original CallAhead harm premise;
3. cache-state-conditioned loading-mode switching;
4. alternating and grouped fixed-partial-residency contexts separately;
5. LayerLease under the E939 equal-budget performance contract;
6. exact Qwen early-placement and cross-architecture 50% contracts separately;
7. FIX_HEAD scheduling with missing common logical arrivals;
8. PR_BASE order control on an already-fixed defect;
9. interference-aware control under E920's affected-set threshold;
10. E800's technical co-residency action qualification.

Each scenario records its metric direction, materiality threshold, safety
constraints, context tags, and development oracle. Metrics from different
experiments are not collapsed into one scalar utility.

## Baselines and equal budget

The evaluator runs three deterministic development baselines:

- `receipt_only`: uses only whether the question is a technical-effectiveness
  contract with effective readback; all performance questions default to
  `probe`.
- `positive_only`: retrieves at most three compatible positive or technical-Go
  evidence cards.
- `counterevidence_aware`: retrieves at most three compatible cards from all
  polarities. A matching harmful/null veto yields `abstain`; a load-bearing
  scope veto yields `probe`; otherwise material positive evidence may yield
  `apply`.

Both retrieval baselines use the same structured compatibility function,
ranking, top-k value, card fields, and maximum evidence-text budget. Only the
eligible polarity set differs. Card implications and scenario oracles are
hidden from generated model-input packets.

## Validation gate

D001 passes as a local harness only if:

- every source artifact is hash-addressed;
- all twelve scenario contracts are unique and have nonempty oracle bases;
- all model-input packets omit oracle, implication, veto, and source outcome
  labels;
- complete experiment groups are retained as development material;
- both retrieval modes use top-k three and the same text budget;
- the counterevidence-aware baseline retrieves a veto basis for every
  `probe`/`abstain` oracle and does not suppress exact-scope `apply` cases;
- mutation tests prove that removing the load-bearing counterevidence changes
  at least one decision;
- two builds are byte-identical.

Even a perfect D001 score is expected from a curated development sanity set
and must not be reported as model accuracy. A later LLM run requires a frozen
model/version/prompt/seed/budget record, and a scientific result requires new
prospectively hidden real-system episodes.
