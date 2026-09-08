#!/usr/bin/env python3
"""Build a deterministic, development-only receipt corpus from local evidence."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
MODELSTATEIO_ROOT = HERE.parents[1]
WORKSPACE_ROOT = MODELSTATEIO_ROOT.parent
DEFAULT_PD_ROOT = Path("D:/Temp/ModelStateIO-PlacementStateGap/MSIO-PD-E003")
DEFAULT_E006_ROOT = (
    WORKSPACE_ROOT
    / "ModelStateIO-data"
    / "MSIO-NI-E006A-COARSE-WINDOW-20260907T211919Z"
    / "extracted"
    / "MSIO-NI-E006A-COARSE-WINDOW"
)
SCHEMA_VERSION = "modelstateio-decision-episode-v0"
EXPOSURE = "historical_outcome_opened_before_normalization"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact(locator: str, path: Path) -> dict[str, str]:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {"locator": locator, "sha256": sha256(path)}


def nullable_number(value: str) -> float | str | None:
    if value == "none" or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return value


def base_episode(
    episode_id: str,
    experiment_id: str,
    role: str,
    analysis_unit: str,
    artifacts: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "episode_id": episode_id,
        "experiment_id": experiment_id,
        "development_exposed": True,
        "decision_stage": "post_action_validation",
        "evidence_role": role,
        "analysis_unit": analysis_unit,
        "source": {"outcome_exposure": EXPOSURE, "artifacts": artifacts},
    }


def callahead_episodes() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    compact = (
        MODELSTATEIO_ROOT
        / "modules/CallAhead/experiments/MSIO-CA-E001/compact_result.json"
    )
    protocol = (
        MODELSTATEIO_ROOT
        / "modules/CallAhead/experiments/MSIO-CA-E001/PREREGISTRATION.md"
    )
    arts = [
        artifact("modelstateio://CallAhead/E001/compact_result.json", compact),
        artifact("modelstateio://CallAhead/E001/PREREGISTRATION.md", protocol),
    ]
    source = load_json(compact)
    globally_valid = bool(source["all_correctness_action_cleanup_checks_passed"])
    episodes = []
    for row in source["trials"]:
        arm = row["arm"]
        requested_bytes = 0 if arm == "none" else 830_472_192
        requested_fraction = 0.0 if arm == "none" else 0.75
        rate_ceiling = 268_435_456 if arm == "paced75" else None
        ep = base_episode(
            f"MSIO-CA-E001-{row['label']}",
            "MSIO-CA-E001",
            "DEVELOPMENT_ACTION_RECEIPT",
            "counterbalanced_trial_160_foreground_requests",
            arts,
        )
        ep.update(
            {
                "context_before": {
                    "block": row["block"],
                    "position": row["position"],
                    "cold_residency_fraction": row["cold_residency_fraction"],
                    "foreground_request_count": 160,
                },
                "requested_receipt": {
                    "action": "file_scoped_background_preparation",
                    "parameters": {
                        "arm": arm,
                        "target_fraction": requested_fraction,
                        "fraction_abs_tolerance": 0.01,
                        "target_bytes": requested_bytes,
                        "rate_ceiling_bytes_per_s": rate_ceiling,
                    },
                    "scope": {"background_model_file_only": True},
                },
                "effective_receipt": {
                    "accepted": None,
                    "control_plane_verified": None,
                    "physical_verified": True,
                    "semantic_verified": globally_valid,
                    "application_class": "PHYSICALLY_EFFECTIVE",
                    "observations": {
                        "preparation_bytes": row["preparation_bytes"],
                        "preparation_bytes_per_s": row["preparation_bps"],
                        "prepared_residency_fraction": row["prepared_residency_fraction"],
                        "background_probe_returncode": row["background_probe_returncode"],
                    },
                },
                "state_receipt": {
                    "before": {"file_residency_fraction": row["cold_residency_fraction"]},
                    "after_action": {
                        "file_residency_fraction": row["prepared_residency_fraction"]
                    },
                    "after_workload": {},
                    "after_cleanup": {"experiment_global_cleanup_passed": globally_valid},
                    "lineage": ["file_scoped_fadvise", "mincore", arm],
                },
                "outcome_receipt": {
                    "status": "OBSERVED_ABSOLUTE_TRIAL",
                    "metrics": {
                        "preparation_s": row["preparation_s"],
                        "background_ready_s": row["background_ready_s"],
                        "foreground_p50_s": row["foreground_p50_s"],
                        "foreground_p95_s": row["foreground_p95_s"],
                        "max_schedule_lag_s": row["max_schedule_lag_s"],
                    },
                    "correctness": {
                        "passed": globally_valid,
                        "basis": "experiment_global_action_correctness_cleanup_gate",
                    },
                    "uncertainty": {
                        "paired_block_analysis_required": True,
                        "single_trial_not_independent_claim": True,
                    },
                },
                "rollback_receipt": {
                    "required": False,
                    "verified": globally_valid,
                    "observations": {"experiment_global_cleanup_passed": globally_valid},
                },
            }
        )
        episodes.append(ep)
    inventory = [{
        "experiment_id": "MSIO-CA-E001",
        "admission": "ADAPTED",
        "analysis_unit": "18 counterbalanced trials; paired block is inferential unit",
        "role": "action-effect receipt and null/counterevidence source",
        "local_source": str(compact),
        "source_sha256": sha256(compact),
        "limitation": "historical outcome exposed; foreground requests within trial are not independent episodes",
    }]
    return episodes, inventory


def cache_state_rank_episodes() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    compact = (
        MODELSTATEIO_ROOT
        / "modules/CacheStateRank/experiments/MSIO-CSR-E100-rank-reversal/compact-result.json"
    )
    result = (
        MODELSTATEIO_ROOT
        / "modules/CacheStateRank/experiments/MSIO-CSR-E100-rank-reversal/RESULT.md"
    )
    arts = [
        artifact("modelstateio://CacheStateRank/E100/compact-result.json", compact),
        artifact("modelstateio://CacheStateRank/E100/RESULT.md", result),
    ]
    source = load_json(compact)
    episodes = []
    for state in ("cold", "warm"):
        for mode in ("mmap", "none", "dio"):
            ep = base_episode(
                f"MSIO-CSR-E100-{state}-{mode}",
                "MSIO-CSR-E100",
                "DEVELOPMENT_NULL_COUNTEREVIDENCE",
                "state_mode_aggregate_of_six_trials",
                arts,
            )
            state_value = source["cold_residency_max"] if state == "cold" else source["warm_residency_min"]
            ep.update(
                {
                    "context_before": {"cache_state": state, "qualified_residency_boundary": state_value},
                    "requested_receipt": {
                        "action": "model_loading_mode",
                        "parameters": {"mode": mode},
                        "scope": {"one_pinned_gguf": True},
                    },
                    "effective_receipt": {
                        "accepted": True,
                        "control_plane_verified": None,
                        "physical_verified": True,
                        "semantic_verified": True,
                        "application_class": "SEMANTICALLY_EFFECTIVE",
                        "observations": {"qualified_cache_state": state},
                    },
                    "state_receipt": {
                        "before": {"cache_state": state, "residency_boundary": state_value},
                        "after_action": {},
                        "after_workload": {},
                        "after_cleanup": {"experiment_result_reports_empty_process_and_gpu_state": True},
                        "lineage": ["file_scoped_state_preparation", "mincore_qualification", mode],
                    },
                    "outcome_receipt": {
                        "status": "NO_MATERIAL_CROSS_STATE_RANK_REVERSAL",
                        "metrics": {
                            "median_wall_s": source["medians_s"][state][mode],
                            "robust_cv": source["robust_cv"][state][mode],
                            "is_state_winner": source["winners"][state] == mode,
                            "winner": source["winners"][state],
                        },
                        "correctness": {"passed": True, "valid_trials_total": source["valid_trials"]},
                        "uncertainty": {"aggregate_only": True, "trials_per_state_mode": 6},
                    },
                    "rollback_receipt": {
                        "required": False,
                        "verified": True,
                        "observations": {"basis": "aggregate_result_cleanup_statement"},
                    },
                }
            )
            episodes.append(ep)
    inventory = [{
        "experiment_id": "MSIO-CSR-E100",
        "admission": "ADAPTED_AGGREGATE_ONLY",
        "analysis_unit": "six state-mode aggregates, each from six trials",
        "role": "qualified state change with null action-rank reversal",
        "local_source": str(compact),
        "source_sha256": sha256(compact),
        "limitation": "per-trial receipts are not local; no row-level reconstruction",
    }]
    return episodes, inventory


def placement_state_gap_episodes(pd_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    receipts = pd_root / "receipts.json"
    environment = pd_root / "environment.json"
    analysis = pd_root / "analysis.json"
    arts = [
        artifact("external://PD-E003/receipts.json", receipts),
        artifact("external://PD-E003/environment.json", environment),
        artifact("external://PD-E003/analysis.json", analysis),
    ]
    rows = load_json(receipts)
    env = load_json(environment)
    episodes = []
    lineage_by_arm = {
        "late_atomic": ["model_constructed_cpu_oriented", "context_constructed", "atomic_placement", "epoch_reset"],
        "early_atomic": ["model_constructed_cpu_oriented", "atomic_placement", "context_constructed"],
        "native_gpu": ["model_constructed_native_gpu", "context_constructed"],
    }
    for row in rows:
        state = row["state"]
        state_ok = (
            state["declared_dev"] == "CUDA0"
            and int(state["tensor_gpu"]) == int(state["tensor_total"])
            and int(state["tensor_cpu"]) == 0
        )
        valid = bool(row["valid"])
        ep = base_episode(
            f"MSIO-PD-E003-b{row['block']:02d}-{row['model']}-{row['arm']}",
            "MSIO-PD-E003",
            "DEVELOPMENT_STATE_LINEAGE",
            "counterbalanced_model_block_arm_cell_three_requests",
            arts,
        )
        ep.update(
            {
                "context_before": {
                    "host": env["host"],
                    "block": row["block"],
                    "model": row["model"],
                    "runtime_lib_sha256": env["libllama_sha256"],
                },
                "requested_receipt": {
                    "action": "placement_and_context_construction_order",
                    "parameters": {"arm": row["arm"]},
                    "scope": {"all_enumerated_transformer_tensors": True},
                },
                "effective_receipt": {
                    "accepted": True,
                    "control_plane_verified": True,
                    "physical_verified": state_ok,
                    "semantic_verified": valid,
                    "application_class": "SEMANTICALLY_EFFECTIVE" if state_ok and valid else "INCONSISTENT",
                    "observations": {
                        "declared_dev": state["declared_dev"],
                        "tensor_total": int(state["tensor_total"]),
                        "tensor_gpu": int(state["tensor_gpu"]),
                        "tensor_cpu": int(state["tensor_cpu"]),
                    },
                },
                "state_receipt": {
                    "before": {"construction_home": "native_gpu" if row["arm"] == "native_gpu" else "cpu_oriented"},
                    "after_action": {
                        "declared_dev": state["declared_dev"],
                        "tensor_gpu": int(state["tensor_gpu"]),
                        "tensor_cpu": int(state["tensor_cpu"]),
                    },
                    "after_workload": {"request_count": len(row["requests"])},
                    "after_cleanup": {"post_gpu": row["post_gpu"]},
                    "lineage": lineage_by_arm[row["arm"]],
                },
                "outcome_receipt": {
                    "status": "VALID_CELL" if valid else "INVALID_CELL",
                    "metrics": {
                        "request_ms": [request["request_ms"] for request in row["requests"]],
                        "median_request_ms": statistics.median(request["request_ms"] for request in row["requests"]),
                        "load_ms": float(row["meta"]["load_ms"]),
                        "context_ms": float(row["meta"]["context_ms"]),
                        "copy_ms": float(row["meta"]["copy_ms"]),
                        "lease_bytes": int(row["meta"]["lease_bytes"]),
                        "peak_gpu_mib": row["peak_gpu_mib"],
                        "peak_rss_kib": row["peak_rss_kib"],
                    },
                    "correctness": {
                        "passed": valid and all(request["valid"] == 1 for request in row["requests"]),
                        "top_tokens": [request["top"] for request in row["requests"]],
                        "logits_sha256": row["logits_sha256"],
                    },
                    "uncertainty": {"paired_model_block_comparison_required": True},
                },
                "rollback_receipt": {
                    "required": row["arm"] != "native_gpu",
                    "verified": valid and not row["post_gpu"],
                    "observations": {
                        "program_summary_valid": valid,
                        "post_gpu": row["post_gpu"],
                    },
                },
            }
        )
        episodes.append(ep)
    inventory = [{
        "experiment_id": "MSIO-PD-E003",
        "admission": "ADAPTED_VERIFIED_COMPACT_COPY",
        "analysis_unit": "54 model-block-arm cells; three requests retained within each cell",
        "role": "same visible placement with different state lineage",
        "local_source": str(receipts),
        "source_sha256": sha256(receipts),
        "limitation": "historical causal experiment on one patched runtime and one V100S",
    }]
    return episodes, inventory


def model_statuses(path: Path) -> dict[str, str]:
    data = load_json(path)
    return {entry["id"]: entry["status"]["value"] for entry in data["data"]}


def transition_order_episodes(e006_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    receipts_root = e006_root / "receipts"
    conditions_tsv = receipts_root / "conditions.tsv"
    schedule_tsv = receipts_root / "sweep-schedule.tsv"
    summary = receipts_root / "E006A-SUMMARY.txt"
    shared_arts = [
        artifact("external://NI-E006A/receipts/conditions.tsv", conditions_tsv),
        artifact("external://NI-E006A/receipts/sweep-schedule.tsv", schedule_tsv),
        artifact("external://NI-E006A/receipts/E006A-SUMMARY.txt", summary),
    ]
    episodes = []
    with conditions_tsv.open("r", encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source, delimiter="\t"))
    for row in rows:
        condition_name = f"row-{int(row['row']):02d}-rep{row['repetition']}-{row['revision']}-{row['mode']}"
        condition_root = e006_root / "conditions" / condition_name
        initial_models = condition_root / "initial-models.json"
        final_models = condition_root / "final-models.json"
        residual = condition_root / "residual.txt"
        port_after = condition_root / "port-after.txt"
        cleanup_action = condition_root / "cleanup-action.txt"
        row_arts = shared_arts + [
            artifact(f"external://NI-E006A/conditions/{condition_name}/initial-models.json", initial_models),
            artifact(f"external://NI-E006A/conditions/{condition_name}/final-models.json", final_models),
            artifact(f"external://NI-E006A/conditions/{condition_name}/residual.txt", residual),
            artifact(f"external://NI-E006A/conditions/{condition_name}/port-after.txt", port_after),
            artifact(f"external://NI-E006A/conditions/{condition_name}/cleanup-action.txt", cleanup_action),
        ]
        valid = row["valid"] == "1"
        completed = row["b_complete"] == "1" and row["c_complete"] == "1"
        residual_empty = not residual.read_text(encoding="utf-8").strip()
        port_listener_empty = not port_after.read_text(encoding="utf-8").strip()
        clean = residual_empty and port_listener_empty
        actual_gap = float(row["actual_c_minus_b_ms"])
        ep = base_episode(
            f"MSIO-NI-E006A-row-{int(row['row']):02d}",
            "MSIO-NI-E006A",
            "DEVELOPMENT_DIAGNOSTIC_COUNTEREXAMPLE",
            "scheduled_revision_mode_repetition_row",
            row_arts,
        )
        ep.update(
            {
                "context_before": {
                    "row": int(row["row"]),
                    "repetition": int(row["repetition"]),
                    "revision": row["revision"],
                    "initial_model_status": model_statuses(initial_models),
                },
                "requested_receipt": {
                    "action": "request_admission_order",
                    "parameters": {
                        "mode": row["mode"],
                        "nominal_c_minus_b_ms": nullable_number(row["nominal_c_minus_b_ms"]),
                    },
                    "scope": {"requests": ["B", "C"]},
                },
                "effective_receipt": {
                    "accepted": True,
                    "control_plane_verified": valid,
                    "physical_verified": valid,
                    "semantic_verified": valid and completed,
                    "application_class": "SEMANTICALLY_EFFECTIVE" if valid and completed else "INCONSISTENT",
                    "observations": {
                        "actual_c_minus_b_ms": actual_gap,
                        "first_complete": row["first_complete"],
                        "b_complete": row["b_complete"] == "1",
                        "c_complete": row["c_complete"] == "1",
                    },
                },
                "state_receipt": {
                    "before": {"model_status": model_statuses(initial_models)},
                    "after_action": {"actual_c_minus_b_ms": actual_gap},
                    "after_workload": {
                        "model_status": model_statuses(final_models),
                        "stall_target": None if row["stall_target"] == "NONE" else row["stall_target"],
                        "nudge_sent": row["nudge_sent"] == "1",
                        "nudge_release": row["nudge_release"] == "1",
                    },
                    "after_cleanup": {
                        "residual_empty": residual_empty,
                        "port_listener_empty": port_listener_empty,
                    },
                    "lineage": [row["revision"], row["mode"], "measured_submission_gap"],
                },
                "outcome_receipt": {
                    "status": row["classification"],
                    "metrics": {
                        "b_latency_s": float(row["b_latency_s"]),
                        "c_latency_s": float(row["c_latency_s"]),
                        "completion_gap_s": float(row["completion_gap_s"]),
                        "start_mono": float(row["start_mono"]),
                        "end_mono": float(row["end_mono"]),
                    },
                    "correctness": {
                        "passed": valid and completed,
                        "basis": "independently_validated_completed_responses",
                    },
                    "uncertainty": {
                        "exploratory": True,
                        "repetitions_per_revision_mode": 3,
                        "row_not_independent_generalization_claim": True,
                    },
                },
                "rollback_receipt": {
                    "required": True,
                    "verified": clean,
                    "observations": {
                        "cleanup_action": cleanup_action.read_text(encoding="utf-8").strip(),
                        "residual_empty": residual_empty,
                        "port_listener_empty": port_listener_empty,
                    },
                },
            }
        )
        episodes.append(ep)
    inventory = [{
        "experiment_id": "MSIO-NI-E006A",
        "admission": "ADAPTED_VERIFIED_RETURN",
        "analysis_unit": "30 scheduled revision-mode-repetition rows",
        "role": "nominal-versus-actual order receipt and fixed-defect diagnostic counterexample",
        "local_source": str(conditions_tsv),
        "source_sha256": sha256(conditions_tsv),
        "limitation": "exploratory, one runtime family, no common upstream logical arrival timestamps",
    }]
    return episodes, inventory


def blocked_inventory() -> list[dict[str, str]]:
    return [
        {
            "experiment_id": "MSIO-LB-E800",
            "admission": "BLOCKED_SOURCE_NOT_LOCAL",
            "analysis_unit": "technical action qualification",
            "role": "control-plane load readback positive example",
            "local_source": "",
            "source_sha256": "",
            "limitation": "remote receipt.json is not present locally; RESULT.md is not expanded into cells",
        },
        {
            "experiment_id": "MSIO-LB-E801",
            "admission": "BLOCKED_SOURCE_NOT_LOCAL",
            "analysis_unit": "12 context-arm cells",
            "role": "alternating positive versus grouped null context evidence",
            "local_source": "",
            "source_sha256": "9984d58289bdbd2d47f0c577e8ebc401bfd0b730de84ab94c9dd14e5e6535a9c",
            "limitation": "hash is reported in RESULT.md but receipts.json is not locally reverified",
        },
        {
            "experiment_id": "MSIO-LL-E939",
            "admission": "BLOCKED_SOURCE_NOT_LOCAL",
            "analysis_unit": "nine capacity-conflict cells",
            "role": "physically feasible but harmful action evidence",
            "local_source": "",
            "source_sha256": "4496b23cab8813d9c5ef8270b85b7a939e511ac10d83c67d65e6454ae65fee24",
            "limitation": "hash is reported in RESULT.md but receipts.json is not locally reverified; dev_layer claim is source-audit inference",
        },
        {
            "experiment_id": "MSIO-IR-E920",
            "admission": "BLOCKED_SOURCE_NOT_LOCAL",
            "analysis_unit": "six paired interference blocks",
            "role": "uncertain/null affected-set counterevidence",
            "local_source": "",
            "source_sha256": "ce678fc949c3a2d2699a3d69453ca888a0821b3b28ce0e35848fdb435667377d",
            "limitation": "reported summary hash only; original machine-readable rows are not local",
        },
    ]


def policy_view(episode: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in episode.items()
        if key not in {"outcome_receipt", "rollback_receipt"}
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as target:
        for row in rows:
            target.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            target.write("\n")


def write_inventory(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "experiment_id",
        "admission",
        "analysis_unit",
        "role",
        "local_source",
        "source_sha256",
        "limitation",
    ]
    with path.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pd-e003-root", type=Path, default=DEFAULT_PD_ROOT)
    parser.add_argument("--e006a-root", type=Path, default=DEFAULT_E006_ROOT)
    parser.add_argument("--output-dir", type=Path, default=HERE)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    episodes: list[dict[str, Any]] = []
    inventory: list[dict[str, str]] = []
    for builder in (callahead_episodes, cache_state_rank_episodes):
        built, rows = builder()
        episodes.extend(built)
        inventory.extend(rows)
    built, rows = placement_state_gap_episodes(args.pd_e003_root)
    episodes.extend(built)
    inventory.extend(rows)
    built, rows = transition_order_episodes(args.e006a_root)
    episodes.extend(built)
    inventory.extend(rows)
    inventory.extend(blocked_inventory())

    episodes.sort(key=lambda row: row["episode_id"])
    inventory.sort(key=lambda row: row["experiment_id"])
    write_jsonl(args.output_dir / "dev-corpus.jsonl", episodes)
    write_jsonl(args.output_dir / "policy-view.jsonl", [policy_view(row) for row in episodes])
    write_inventory(args.output_dir / "EVIDENCE-INVENTORY.tsv", inventory)
    print(json.dumps({
        "episodes": len(episodes),
        "adapted_sources": sum(row["admission"].startswith("ADAPTED") for row in inventory),
        "blocked_sources": sum(row["admission"].startswith("BLOCKED") for row in inventory),
        "output_dir": str(args.output_dir.resolve()),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
