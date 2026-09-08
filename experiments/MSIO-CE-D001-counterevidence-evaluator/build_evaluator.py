#!/usr/bin/env python3
"""Build D001 evidence cards, scenarios, model inputs, and rule baselines."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MSIO = HERE.parents[1]
TOP_K = 3
TEXT_BUDGET_CHARS = 1800


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source(locator: str, path: Path) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"locator": locator, "sha256": sha(path)}


def card(
    card_id: str,
    experiment_id: str,
    polarity: str,
    tags: dict[str, str],
    claim: str,
    observation: str,
    uncertainty: str,
    applicability: str,
    implications: dict[str, str],
    veto: bool,
    artifact: dict[str, str],
) -> dict[str, Any]:
    return {
        "card_id": card_id,
        "experiment_id": experiment_id,
        "development_exposed": True,
        "polarity": polarity,
        "tags": tags,
        "claim": claim,
        "observation": observation,
        "uncertainty": uncertainty,
        "applicability": applicability,
        "implications": implications,
        "veto": veto,
        "source": artifact,
    }


def build_cards() -> list[dict[str, Any]]:
    ca = MSIO / "modules/CallAhead/experiments/MSIO-CA-E001/RESULT.md"
    csr = MSIO / "modules/CacheStateRank/experiments/MSIO-CSR-E100-rank-reversal/RESULT.md"
    e800 = MSIO / "modules/LayerBudget/experiments/MSIO-LB-E800-action-qualification/RESULT.md"
    e801 = MSIO / "modules/LayerBudget/experiments/MSIO-LB-E801-locality-reversal/RESULT.md"
    e938 = MSIO / "modules/LayerLease/experiments/MSIO-LL-E938R2-epoch-safe-reclaim/RESULT.md"
    e939 = MSIO / "modules/LayerLease/experiments/MSIO-LL-E939-capacity-conflict/RESULT.md"
    pd = MSIO / "phenomena/PlacementStateGap/experiments/MSIO-PD-E003-context-capture/RESULT.md"
    e006 = MSIO / "experiments/MSIO-NI-E006-transition-window-mapping/E006A-RESULT.md"
    ir = MSIO / "modules/InterferenceReceipt/experiments/MSIO-IR-E920/RESULT.md"
    return [
        card("CA-READINESS-POS", "MSIO-CA-E001", "POSITIVE",
             {"system": "callahead", "action": "eager75"},
             "Eager file preparation improves background readiness.",
             "Median readiness benefit was about 0.4015 s.",
             "Six paired blocks; development-exposed.",
             "One V100S, two pinned small GGUF models, exact E001 load.",
             {"ca_readiness_budget": "APPLY", "ca_pacing_necessity": "PROBE"}, False,
             source("modelstateio://CallAhead/E001/RESULT.md", ca)),
        card("CA-HARM-NULL", "MSIO-CA-E001", "NULL",
             {"system": "callahead", "action": "eager75"},
             "Eager preparation did not establish material foreground p95 harm.",
             "Median relative harm was 0.12%; 95% interval [-3.01%, 5.90%].",
             "The interval crosses zero and stays below the 10% harm premise.",
             "Exact E001 foreground workload and preparation range only.",
             {"ca_readiness_budget": "APPLY", "ca_pacing_necessity": "ABSTAIN"}, True,
             source("modelstateio://CallAhead/E001/RESULT.md", ca)),
        card("CSR-STATE-TECH", "MSIO-CSR-E100", "TECHNICAL_GO",
             {"system": "cache_state_rank", "action": "state_conditioned_mode"},
             "The experiment created and verified sharply separated cache states.",
             "Cold residency was 0% and warm residency was 100%.",
             "State preparation is a precondition, not an action benefit.",
             "One 0.5B GGUF and one pinned llama.cpp runtime.",
             {"csr_rank_reversal": "PROBE"}, False,
             source("modelstateio://CacheStateRank/E100/RESULT.md", csr)),
        card("CSR-REVERSAL-NULL", "MSIO-CSR-E100", "NULL",
             {"system": "cache_state_rank", "action": "state_conditioned_mode"},
             "Cache state did not reverse the best loading mode.",
             "mmap was the median winner in both cold and warm states.",
             "All robust CV values were at most 0.0403; required reversal was absent.",
             "Rejects only the E100 three-mode action-ranking mechanism.",
             {"csr_rank_reversal": "ABSTAIN"}, True,
             source("modelstateio://CacheStateRank/E100/RESULT.md", csr)),
        card("LB-E800-TECH", "MSIO-LB-E800", "TECHNICAL_GO",
             {"system": "layer_budget", "action": "coexist_partial"},
             "The fixed [999,999,40] layer budget is executable under the observed capacity conflict.",
             "All three models read back loaded and returned exact OK responses.",
             "Technical qualification only; no performance benefit established.",
             "Exact three Qwen model set and pinned native router.",
             {"lb_e800_effectiveness": "APPLY", "lb_alternating_benefit": "PROBE", "lb_grouped_benefit": "PROBE"}, False,
             source("modelstateio://LayerBudget/E800/RESULT.md", e800)),
        card("LB-ALT-POS", "MSIO-LB-E801", "POSITIVE",
             {"system": "layer_budget", "action": "coexist_partial", "trace": "alternating"},
             "Fixed partial co-residency avoids repeated native-LRU reload debt on the alternating trace.",
             "Median total-wall benefit was 27.61%; interval [25.24%, 30.62%].",
             "Three paired blocks; exact synthetic alternating trace.",
             "Not evidence for an adaptive allocator or production generality.",
             {"lb_alternating_benefit": "APPLY"}, False,
             source("modelstateio://LayerBudget/E801/RESULT.md", e801)),
        card("LB-GROUPED-NULL", "MSIO-LB-E801", "NULL",
             {"system": "layer_budget", "action": "coexist_partial", "trace": "grouped"},
             "Fixed partial co-residency has no material stable advantage on the grouped trace.",
             "Median benefit was 1.82%; interval [-2.85%, 6.87%].",
             "Three paired blocks and mixed direction.",
             "Exact synthetic grouped trace only.",
             {"lb_grouped_benefit": "ABSTAIN"}, True,
             source("modelstateio://LayerBudget/E801/RESULT.md", e801)),
        card("LL-E938-TECH", "MSIO-LL-E938R2", "TECHNICAL_GO",
             {"system": "layer_lease", "action": "live_layer_lease"},
             "Epoch-safe repeated tensor migration and reclamation is technically feasible.",
             "Six of six CPU/CUDA/CPU events completed without token mismatch or residue.",
             "Small-model technical feasibility without physical HBM conflict.",
             "Does not establish an end-to-end fast path.",
             {"layerlease_capacity_benefit": "PROBE"}, False,
             source("modelstateio://LayerLease/E938R2/RESULT.md", e938)),
        card("LL-E939-HARM", "MSIO-LL-E939", "HARMFUL",
             {"system": "layer_lease", "action": "live_layer_lease"},
             "The qualified live lease mechanism is materially slower under the capacity-conflict trace.",
             "Median effects were -44.73% versus native LRU and -81.68% versus static partial residency.",
             "All three paired blocks were harmful against both baselines.",
             "Construction-time dev_layer metadata remained CPU-oriented by source audit.",
             {"layerlease_capacity_benefit": "ABSTAIN"}, True,
             source("modelstateio://LayerLease/E939/RESULT.md", e939)),
        card("PD-QWEN-POS", "MSIO-PD-E003", "POSITIVE",
             {"system": "placement_state_gap", "action": "early_atomic", "model_scope": "qwen"},
             "Early atomic placement is faster than late placement while preserving native semantics on both Qwen models.",
             "Median improvements were 29.68% and 21.76%; early/native logits matched exactly.",
             "Six blocks per model; historical patched-runtime result.",
             "Exact Qwen models, one V100S, one isolated llama.cpp runtime.",
             {"pd_qwen_15pct": "APPLY"}, False,
             source("modelstateio://PlacementStateGap/E003/RESULT.md", pd)),
        card("PD-CROSSARCH-NULL", "MSIO-PD-E003", "NULL",
             {"system": "placement_state_gap", "action": "early_atomic", "model_scope": "cross_architecture"},
             "The all-model 50% materiality contract failed.",
             "Qwen improvements of 29.68% and 21.76% were below the frozen 50% threshold.",
             "The favorable SmolLM2 subset cannot replace the all-model rule.",
             "Causal source explanation only; no named controller activated.",
             {"pd_crossarch_50pct": "ABSTAIN"}, True,
             source("modelstateio://PlacementStateGap/E003/RESULT.md", pd)),
        card("E006-PRBASE-HARM", "MSIO-NI-E006A", "HARMFUL",
             {"system": "transition_order", "action": "order_policy", "revision": "PR_BASE"},
             "Concurrent PR_BASE orders reproducibly expose directional stalls.",
             "Each C-first, simultaneous, and B-first concurrent mode stalled 3/3.",
             "Three repeats per mode give wide exact stall-rate intervals.",
             "The behavior belongs to an already-fixed lifecycle defect.",
             {"e006_prbase_policy": "ABSTAIN"}, True,
             source("modelstateio://NI-E006A/E006A-RESULT.md", e006)),
        card("E006-FIXHEAD-POS", "MSIO-NI-E006A", "POSITIVE",
             {"system": "transition_order", "action": "order_policy", "revision": "FIX_HEAD"},
             "The corrected backend completed all tested modes without the PR_BASE stall.",
             "FIX_HEAD stalled in 0/15 rows.",
             "Only three repeats per cell and descriptive latency ranges.",
             "Shows correct-backend execution, not scheduling benefit.",
             {"e006_fixhead_scheduler": "APPLY"}, False,
             source("modelstateio://NI-E006A/E006A-RESULT.md", e006)),
        card("E006-ARRIVAL-SCOPE", "MSIO-NI-E006A", "SCOPE_LIMIT",
             {"system": "transition_order", "action": "order_policy", "revision": "FIX_HEAD"},
             "E006A cannot establish an order-policy benefit without common upstream logical arrivals.",
             "Measured makespans start at first server submission, not scheduler arrival.",
             "No weighted latency, throughput, or fairness comparison is identified.",
             "A new mainline must timestamp arrivals before admission.",
             {"e006_fixhead_scheduler": "PROBE"}, True,
             source("modelstateio://NI-E006A/E006A-RESULT.md", e006)),
        card("IR-E920-NULL", "MSIO-IR-E920", "NULL",
             {"system": "interference_receipt", "action": "interference_aware_control"},
             "The tested sequential-read interferer did not establish a material affected set.",
             "Median slowdown was 1.75%; interval [-21.02%, 4.42%].",
             "Six paired blocks; interval crosses zero.",
             "Rejects only the tested single-device read pressure and 0.5B mmap load.",
             {"ir_e920_affected_set": "ABSTAIN"}, True,
             source("modelstateio://InterferenceReceipt/E920/RESULT.md", ir)),
    ]


def scenario(
    scenario_id: str,
    contract_id: str,
    contract_type: str,
    tags: dict[str, str],
    objective: dict[str, Any],
    safety: list[str],
    question: str,
    oracle: str,
    oracle_basis: list[str],
) -> dict[str, Any]:
    return {
        "scenario_id": scenario_id,
        "development_exposed": True,
        "contract_id": contract_id,
        "contract_type": contract_type,
        "tags": tags,
        "objective": objective,
        "safety_constraints": safety,
        "question": question,
        "allowed_decisions": ["APPLY", "PROBE", "ABSTAIN"],
        "oracle_decision": oracle,
        "oracle_basis": oracle_basis,
    }


def build_scenarios() -> list[dict[str, Any]]:
    correctness = ["correctness passes", "cleanup passes", "effective state is verified"]
    return [
        scenario("S01-CA-READINESS", "ca_readiness_budget", "performance",
                 {"system": "callahead", "action": "eager75"},
                 {"metric": "readiness_benefit_s", "direction": "maximize", "minimum": 0.2, "foreground_p95_harm_upper_max": 0.10},
                 correctness, "Apply eager75 for at least 0.2 s readiness benefit if the 95% upper harm bound is at most 10%?",
                 "APPLY", ["CA-READINESS-POS", "CA-HARM-NULL"]),
        scenario("S02-CA-PACING-NECESSITY", "ca_pacing_necessity", "performance",
                 {"system": "callahead", "action": "eager75"},
                 {"metric": "eager_relative_p95_harm", "direction": "minimum_harm_premise", "minimum": 0.10, "ci_lower_above": 0.0},
                 correctness, "Deploy pacing because eager preparation causes material foreground harm?",
                 "ABSTAIN", ["CA-HARM-NULL"]),
        scenario("S03-CSR-SELECTOR", "csr_rank_reversal", "performance",
                 {"system": "cache_state_rank", "action": "state_conditioned_mode"},
                 {"metric": "cross_state_winner_reversal", "required": True, "minimum_saving": 0.10},
                 correctness, "Enable a cache-state-conditioned loading-mode selector?",
                 "ABSTAIN", ["CSR-REVERSAL-NULL"]),
        scenario("S04-LB-ALTERNATING", "lb_alternating_benefit", "performance",
                 {"system": "layer_budget", "action": "coexist_partial", "trace": "alternating"},
                 {"metric": "paired_total_wall_benefit", "direction": "maximize", "minimum": 0.15, "ci_lower_above": 0.0},
                 correctness, "Apply fixed partial co-residency for the exact alternating trace?",
                 "APPLY", ["LB-ALT-POS", "LB-E800-TECH"]),
        scenario("S05-LB-GROUPED", "lb_grouped_benefit", "performance",
                 {"system": "layer_budget", "action": "coexist_partial", "trace": "grouped"},
                 {"metric": "paired_total_wall_benefit", "direction": "maximize", "minimum": 0.15, "ci_lower_above": 0.0},
                 correctness, "Apply fixed partial co-residency for the exact grouped trace?",
                 "ABSTAIN", ["LB-GROUPED-NULL"]),
        scenario("S06-LAYERLEASE-CAPACITY", "layerlease_capacity_benefit", "performance",
                 {"system": "layer_lease", "action": "live_layer_lease"},
                 {"metric": "paired_total_wall_benefit_vs_both_baselines", "direction": "maximize", "minimum": 0.15},
                 correctness, "Apply live LayerLease under the E939 capacity-conflict trace?",
                 "ABSTAIN", ["LL-E939-HARM"]),
        scenario("S07-PD-QWEN", "pd_qwen_15pct", "performance",
                 {"system": "placement_state_gap", "action": "early_atomic", "model_scope": "qwen"},
                 {"metric": "early_vs_late_request_time_improvement", "direction": "maximize", "minimum": 0.15},
                 correctness, "Apply early atomic placement for the exact two-Qwen represented scope?",
                 "APPLY", ["PD-QWEN-POS"]),
        scenario("S08-PD-CROSSARCH", "pd_crossarch_50pct", "performance",
                 {"system": "placement_state_gap", "action": "early_atomic", "model_scope": "cross_architecture"},
                 {"metric": "early_vs_late_improvement_every_model", "direction": "maximize", "minimum": 0.50},
                 correctness, "Promote early placement under the frozen every-model 50% cross-architecture contract?",
                 "ABSTAIN", ["PD-CROSSARCH-NULL"]),
        scenario("S09-E006-FIXHEAD", "e006_fixhead_scheduler", "performance",
                 {"system": "transition_order", "action": "order_policy", "revision": "FIX_HEAD"},
                 {"metric": "weighted_end_to_end_latency", "direction": "minimize", "minimum_relative_benefit": 0.15},
                 correctness + ["common pre-admission logical arrivals", "no throughput or fairness loss"],
                 "Apply an order policy on FIX_HEAD as a scheduling optimization?",
                 "PROBE", ["E006-ARRIVAL-SCOPE"]),
        scenario("S10-E006-PRBASE", "e006_prbase_policy", "performance",
                 {"system": "transition_order", "action": "order_policy", "revision": "PR_BASE"},
                 {"metric": "stall_avoidance_on_correct_backend", "required": True},
                 correctness + ["not explained by a direct fixed defect"],
                 "Use PR_BASE order control as the policy opportunity?",
                 "ABSTAIN", ["E006-PRBASE-HARM"]),
        scenario("S11-IR-AFFECTED-SET", "ir_e920_affected_set", "performance",
                 {"system": "interference_receipt", "action": "interference_aware_control"},
                 {"metric": "paired_slowdown", "direction": "minimum_affected_set", "minimum": 0.10, "ci_lower_above": 0.0},
                 correctness, "Apply an interference-aware controller for the E920 tested pressure?",
                 "ABSTAIN", ["IR-E920-NULL"]),
        scenario("S12-E800-EFFECTIVE", "lb_e800_effectiveness", "technical_effectiveness",
                 {"system": "layer_budget", "action": "coexist_partial"},
                 {"metric": "requested_effective_co_residency", "required": True},
                 correctness, "Accept the exact [999,999,40] configuration as technically effective?",
                 "APPLY", ["LB-E800-TECH"]),
    ]


def compatible(card_tags: dict[str, str], scenario_tags: dict[str, str]) -> bool:
    return all(key not in scenario_tags or scenario_tags[key] == value for key, value in card_tags.items())


def retrieve(cards: list[dict[str, Any]], item: dict[str, Any], positive_only: bool) -> list[dict[str, Any]]:
    candidates = []
    for evidence in cards:
        if item["contract_id"] not in evidence["implications"]:
            continue
        if not compatible(evidence["tags"], item["tags"]):
            continue
        if positive_only and evidence["polarity"] not in {"POSITIVE", "TECHNICAL_GO"}:
            continue
        score = sum(item["tags"].get(key) == value for key, value in evidence["tags"].items())
        candidates.append((score, evidence["card_id"], evidence))
    candidates.sort(key=lambda row: (-row[0], row[1]))
    return [row[2] for row in candidates[:TOP_K]]


def decide(item: dict[str, Any], retrieved: list[dict[str, Any]]) -> str:
    implications = [
        (evidence["implications"][item["contract_id"]], evidence["veto"])
        for evidence in retrieved
    ]
    vetoes = [decision for decision, veto in implications if veto]
    if "ABSTAIN" in vetoes:
        return "ABSTAIN"
    if "PROBE" in vetoes:
        return "PROBE"
    if any(decision == "APPLY" for decision, _ in implications):
        return "APPLY"
    return "PROBE"


def receipt_only_decision(item: dict[str, Any]) -> str:
    return "APPLY" if item["contract_type"] == "technical_effectiveness" else "PROBE"


def visible_card(evidence: dict[str, Any]) -> dict[str, Any]:
    return {
        key: evidence[key]
        for key in ("card_id", "experiment_id", "tags", "claim", "observation", "uncertainty", "applicability", "source")
    }


def model_input(item: dict[str, Any], mode: str, retrieved: list[dict[str, Any]]) -> dict[str, Any]:
    packet = {
        "scenario_id": item["scenario_id"],
        "mode": mode,
        "decision_contract": {
            "contract_id": item["contract_id"],
            "objective": item["objective"],
            "safety_constraints": item["safety_constraints"],
            "allowed_decisions": item["allowed_decisions"],
        },
        "context": item["tags"],
        "question": item["question"],
        "evidence": [visible_card(evidence) for evidence in retrieved],
        "instruction": "Return APPLY, PROBE, or ABSTAIN and cite card_ids. Do not assume requested state equals effective state.",
        "max_evidence_chars": TEXT_BUDGET_CHARS,
    }
    rendered = json.dumps(packet["evidence"], sort_keys=True)
    if len(rendered) > TEXT_BUDGET_CHARS:
        raise AssertionError((item["scenario_id"], mode, len(rendered)))
    return packet


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as target:
        for row in rows:
            target.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")


def evaluate_predictions(scenarios: list[dict[str, Any]], predictions: dict[str, str]) -> dict[str, Any]:
    correct = sum(predictions[item["scenario_id"]] == item["oracle_decision"] for item in scenarios)
    premature_apply = sum(
        predictions[item["scenario_id"]] == "APPLY" and item["oracle_decision"] != "APPLY"
        for item in scenarios
    )
    harmful_apply = sum(
        predictions[item["scenario_id"]] == "APPLY" and item["oracle_decision"] == "ABSTAIN"
        for item in scenarios
    )
    missed_abstain = sum(
        predictions[item["scenario_id"]] != "ABSTAIN" and item["oracle_decision"] == "ABSTAIN"
        for item in scenarios
    )
    decision_recall = {}
    for decision in ("APPLY", "PROBE", "ABSTAIN"):
        population = sum(item["oracle_decision"] == decision for item in scenarios)
        hits = sum(
            item["oracle_decision"] == decision and predictions[item["scenario_id"]] == decision
            for item in scenarios
        )
        decision_recall[decision] = {"correct": hits, "population": population, "recall": hits / population}
    return {
        "correct": correct,
        "total": len(scenarios),
        "accuracy": correct / len(scenarios),
        "premature_apply": premature_apply,
        "harmful_apply": harmful_apply,
        "missed_abstain": missed_abstain,
        "decision_recall": decision_recall,
        "predictions": predictions,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cards = sorted(build_cards(), key=lambda row: row["card_id"])
    scenarios = sorted(build_scenarios(), key=lambda row: row["scenario_id"])
    positive_inputs = []
    balanced_inputs = []
    positive_predictions = {}
    balanced_predictions = {}
    retrieval_audit = []
    for item in scenarios:
        positive = retrieve(cards, item, True)
        balanced = retrieve(cards, item, False)
        positive_inputs.append(model_input(item, "positive_only", positive))
        balanced_inputs.append(model_input(item, "counterevidence_aware", balanced))
        positive_predictions[item["scenario_id"]] = decide(item, positive)
        balanced_predictions[item["scenario_id"]] = decide(item, balanced)
        retrieval_audit.append({
            "scenario_id": item["scenario_id"],
            "positive_only": [row["card_id"] for row in positive],
            "counterevidence_aware": [row["card_id"] for row in balanced],
        })
    receipt_predictions = {item["scenario_id"]: receipt_only_decision(item) for item in scenarios}
    results = {
        "status": "DEVELOPMENT_HARNESS_RESULT",
        "not_llm_evaluation": True,
        "top_k": TOP_K,
        "max_evidence_chars": TEXT_BUDGET_CHARS,
        "baselines": {
            "receipt_only": evaluate_predictions(scenarios, receipt_predictions),
            "positive_only": evaluate_predictions(scenarios, positive_predictions),
            "counterevidence_aware": evaluate_predictions(scenarios, balanced_predictions),
        },
    }
    write_jsonl(args.output_dir / "evidence-cards.jsonl", cards)
    write_jsonl(args.output_dir / "scenarios-with-oracles.jsonl", scenarios)
    write_jsonl(args.output_dir / "model-inputs-positive-only.jsonl", positive_inputs)
    write_jsonl(args.output_dir / "model-inputs-counterevidence-aware.jsonl", balanced_inputs)
    write_jsonl(args.output_dir / "retrieval-audit.jsonl", retrieval_audit)
    (args.output_dir / "baseline-results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({
        "cards": len(cards),
        "scenarios": len(scenarios),
        "baseline_scores": {name: value["correct"] for name, value in results["baselines"].items()},
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
