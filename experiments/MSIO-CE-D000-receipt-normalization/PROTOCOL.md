# MSIO-CE-D000 historical receipt normalization protocol

Status: frozen local development transformation. Date: 2026-09-08.

## Purpose and evidence boundary

This task tests whether selected historical ModelStateIO artifacts can be
normalized into auditable decision episodes with separate requested,
effective, state, outcome, and rollback receipts. It is a post-outcome data
engineering task. It does not evaluate an LLM, optimizer, controller, or new
systems mechanism and cannot provide confirmatory performance evidence.

Every emitted episode is marked `development_exposed=true`. Historical
ModelStateIO outcomes were known before this schema and extraction logic were
defined. They may be used for schema development, deterministic validator
tests, counterevidence retrieval development, and case-study selection, but
not as an untouched test set for a future tuning method.

## Frozen source admission rule

A source enters the v0 corpus only when a machine-readable compact receipt is
available locally and its SHA-256 can be recomputed. A narrative `RESULT.md`
alone is insufficient for reconstructing per-cell episodes. Such sources
remain in the inventory as `BLOCKED_SOURCE_NOT_LOCAL`.

The admitted sources are:

1. MSIO-CA-E001 repository compact result;
2. MSIO-CSR-E100 repository compact result plus its result boundary;
3. MSIO-PD-E003 verified compact local receipt, environment, and analysis
   copies;
4. MSIO-NI-E006A verified local returned compact receipts and condition state
   files.

MSIO-LB-E800, MSIO-LB-E801, MSIO-LL-E939, and MSIO-IR-E920 are inventory-only
until their original machine-readable receipts are present locally and
verified. Their published aggregate values must not be expanded into invented
per-cell rows.

## Normalization rules

- Preserve the original analysis unit. Do not treat repeated requests inside
  a trial as independent tuning decisions.
- Preserve null, harmful, diagnostic, and technically invalid outcomes.
- Use `null` or an explicit unverified class for missing readback; do not
  infer an effective value from the requested value.
- Acknowledgement, control-plane readback, physical readback, and semantic
  correctness are separate fields.
- Record state lineage when action timing relative to model/context
  construction is load-bearing.
- Preserve source locators and SHA-256 values. Generated corpus rows do not
  replace the source artifacts.
- Generate a policy view that excludes outcome and rollback fields. It is a
  post-action validation view, not a claim that the historical rows are blind.

## Local validation gate

The local gate passes only if:

- all source hashes are recomputed;
- every episode satisfies the local schema checks;
- episode identifiers are unique;
- all episodes are development-exposed and none is labeled confirmatory;
- policy views contain no outcome or rollback receipt;
- two independent builds from unchanged inputs are byte-identical;
- the frozen unit tests for requested/effective distinction, state lineage,
  and nominal/actual timing pass.

A pass establishes a reusable development evidence substrate only. The next
scientific gate must prospectively freeze a method and collect new, unexposed
episodes.
