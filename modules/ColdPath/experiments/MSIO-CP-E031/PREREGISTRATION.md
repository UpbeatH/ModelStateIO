# MSIO-CP-E031 QueueAwareWarm material and router audit

## Question

Can the existing private runtime support a technically valid two-model,
request-admission experiment without inventing model identities or modifying
the upstream server? `QueueAwareWarm` would study bounded loading decisions at
the router's documented queue/LRU boundary, not pre-arrival prediction.

## Procedure and scope

Perform only read-only inspection in g130's allowed private runtime: enumerate
candidate GGUF files at the known `incoming/` boundary; record file sizes and
SHA-256 digests; inspect router preset/configuration documentation and source
for model-ID-to-file binding and `models_max` semantics; audit GPU idle state
and existing processes. Do not launch a server/model, create presets, download,
install, modify source, or access another user's directory.

## Pass rule

PASS requires exactly two or more readable model states with distinct digests,
known local paths, an unambiguous router binding mechanism, and enough free GPU
memory for a safe single-model `models_max=1` experiment. Each model must have
a license/provenance record; an unknown model may be retained only for a
technical feasibility test and cannot support paper evidence.

Otherwise record NO-GO or the narrowed technical limitation. A PASS merely
permits freezing a later equal-budget router protocol; it is not permission to
start it.
