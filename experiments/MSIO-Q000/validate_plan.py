import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "roadmap.json").read_text(encoding="utf-8"))

errors = []
routes = data.get("routes", [])
required = {
    "name", "status", "question", "hypothesis", "primary_metric",
    "strong_baselines", "go_rule", "no_go_rule",
}

if data.get("cluster_active") is not False:
    errors.append("ModelStateIO must remain cluster-inactive")
if len(routes) != 3:
    errors.append(f"expected 3 routes, found {len(routes)}")

names = [route.get("name") for route in routes]
if len(set(names)) != len(names):
    errors.append("route names are not unique")
if sum(route.get("status") == "local_active" for route in routes) != 1:
    errors.append("exactly one route must be local-active")

for index, route in enumerate(routes):
    missing = sorted(required - set(route))
    if missing:
        errors.append(f"route {index} missing: {', '.join(missing)}")
    for field in required - {"strong_baselines"}:
        if not str(route.get(field, "")).strip():
            errors.append(f"route {index} has empty {field}")
    if len(route.get("strong_baselines", [])) < 3:
        errors.append(f"route {index} has fewer than 3 strong baselines")

if errors:
    raise SystemExit("FAIL\n" + "\n".join(f"- {item}" for item in errors))

print("PASS: 3 distinct routes; one local-active; zero cluster-active; all required gates present")

