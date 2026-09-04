from pathlib import Path

result = Path(__file__).parents[1] / "MSIO-CP-E012" / "RESULT.md"
text = result.read_text(encoding="utf-8").lower()
required = ["provenance reanalysis", "18", "no_go", "0.15", "no model or gpu execution"]
for token in required:
    assert token in text, f"missing evidence token: {token}"
forbidden = ["cold-start benefit", "universal superiority", "optimizer gain", "generalization"]
assert not any(token in text for token in forbidden)
print("PASS: bounded interpretation and preserved No-Go")
