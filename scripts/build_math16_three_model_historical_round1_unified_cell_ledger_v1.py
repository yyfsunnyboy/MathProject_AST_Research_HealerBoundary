#!/usr/bin/env python3
"""Build the Math16 three-model Historical Round 1 unified cell ledger.

This builder is deliberately evidence-only. It does not import or execute any
model, healer, candidate, replay, or evaluator code.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "math16_three_model_historical_round1_unified_cell_ledger_v1"
ACCOUNT_NAMESPACE = "historical_round1"
STAGES = ("C0", "C1", "C2", "C3", "C4", "C5a", "C5b", "C5c")
MODEL_ORDER = ("qwen4b", "qwen9b", "gemini")
PROVENANCE_VALUES = {
    "DIRECT",
    "MANIFEST_DERIVED",
    "OVERLAY",
    "DIAGNOSTIC_PENDING",
    "NOT_PERSISTED",
    "NOT_APPLICABLE",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


ROOT = repo_root()
RESULTS = ROOT / "docs" / "experiments" / "results"
MANIFESTS = ROOT / "docs" / "experiments" / "manifests"
REPORTS = ROOT / "docs" / "experiments" / "reports"
OUTPUT_DIR = RESULTS / SCHEMA_VERSION
LEDGER_PATH = OUTPUT_DIR / "unified_cell_ledger.jsonl"
VALIDATION_PATH = OUTPUT_DIR / "validation_summary.json"
SHA_MANIFEST_PATH = OUTPUT_DIR / "sha256_manifest.json"


def rel(path: Path | str) -> str:
    p = Path(path)
    if p.is_absolute():
        p = p.relative_to(ROOT)
    return p.as_posix()


def long_path(path: Path | str) -> str:
    absolute = str(Path(path).resolve())
    if os.name == "nt" and not absolute.startswith("\\\\?\\"):
        return "\\\\?\\" + absolute
    return absolute


def read_text(path: Path | str) -> str:
    with open(long_path(path), "r", encoding="utf-8", newline=None) as handle:
        return handle.read()


def read_bytes(path: Path | str) -> bytes:
    with open(long_path(path), "rb") as handle:
        return handle.read()


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in read_text(path).splitlines() if line.strip()]


def load_csv(path: Path) -> list[dict[str, str]]:
    with open(long_path(path), "r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_status(value: Any) -> str:
    if value in {"PASS", "PASSED"}:
        return "PASS"
    if value in {"FAIL", "FAILED"}:
        return "FAIL"
    raise ValueError(f"Unsupported PASS/FAIL status: {value!r}")


def canonical_condition(raw_condition: str) -> str:
    aliases = {
        "ab1": "AB1",
        "ab2d": "AB2D",
        "ab2g": "AB2G",
        "ab2d_spec": "AB2D_SPEC",
        "ab2d_spec_v2": "AB2D_SPEC",
    }
    if raw_condition not in aliases:
        raise ValueError(f"Unknown raw condition: {raw_condition}")
    return aliases[raw_condition]


def canonical_identity(task_id: str, condition: str, seed: int) -> str:
    return f"Math16::{task_id}::{canonical_condition(condition)}::{seed}"


def sha256_bytes(path: Path | str) -> str:
    return hashlib.sha256(read_bytes(path)).hexdigest()


def sha256_source_text(path: Path | str) -> str:
    return hashlib.sha256(read_text(path).encode("utf-8")).hexdigest()


def as_map(rows: Iterable[dict[str, Any]], key: str = "cell_id") -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        value = row[key]
        if value in result:
            raise ValueError(f"Duplicate {key}: {value}")
        result[value] = row
    return result


def q4_cell_id(row: dict[str, Any]) -> str:
    return row.get("cell_id") or row["cell_identity"]["cell_id"]


def q4_map(rows: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        cell_id = q4_cell_id(row)
        if cell_id in result:
            raise ValueError(f"Duplicate cell_id: {cell_id}")
        result[cell_id] = row
    return result


def stage_record(
    *,
    status: Any,
    source_path: str,
    source_sha256: str,
    status_provenance: str,
    source_provenance: str,
    evidence_refs: list[str],
    account_basis: str,
) -> dict[str, Any]:
    if status_provenance not in PROVENANCE_VALUES:
        raise ValueError(status_provenance)
    if source_provenance not in PROVENANCE_VALUES:
        raise ValueError(source_provenance)
    return {
        "status": normalize_status(status),
        "source_path": source_path,
        "source_sha256": source_sha256,
        "status_provenance": status_provenance,
        "source_provenance": source_provenance,
        "account_basis": account_basis,
        "evidence_refs": evidence_refs,
    }


def explicit_select(account: str, choices: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if account not in choices:
        raise ValueError(f"Formal account {account!r} not present in choices")
    return choices[account]


def aggregate_ever(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Coverage-aware TRUE/FALSE/NULL aggregation for one metric."""
    applicable = [event for event in events if event["applicable"]]
    explicit = [event for event in applicable if event["value"] is not None]
    true_events = [event for event in explicit if event["value"] is True]
    false_events = [event for event in explicit if event["value"] is False]
    unknown_events = [event for event in applicable if event["value"] is None]
    coverage_complete = not unknown_events
    if true_events:
        value: bool | None = True
    elif coverage_complete:
        value = False
    else:
        value = None
    if value is None:
        provenance = "DIAGNOSTIC_PENDING"
    elif any(event["provenance"] == "MANIFEST_DERIVED" for event in explicit):
        provenance = "MANIFEST_DERIVED"
    else:
        provenance = "DIRECT"
    return {
        "value": value,
        "coverage_complete": coverage_complete,
        "true_event_count": len(true_events),
        "false_event_count": len(false_events),
        "unknown_event_count": len(unknown_events),
        "provenance": provenance,
    }


def event(
    value: bool | None,
    *,
    applicable: bool,
    provenance: str,
) -> dict[str, Any]:
    if provenance not in PROVENANCE_VALUES:
        raise ValueError(provenance)
    if not applicable and value is not None:
        raise ValueError("NOT_APPLICABLE event cannot carry a boolean")
    return {"value": value, "applicable": applicable, "provenance": provenance}


def git_head() -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        text=True,
        encoding="utf-8",
    ).strip()


THREE_MODEL_SUMMARY_PATH = MANIFESTS / "math16_three_model_round1_summary_v1.json"
AGGRESSIVE_OVERLAY_PATH = MANIFESTS / "math16_aggressive_round1_corrected_overlay_v1.json"
BASELINE_FROZEN_PATH = (
    RESULTS / "math16_pilot02_qwen4b_evaluation_v4_r001" / "cell_level_baseline.jsonl"
)
BASELINE_CROSSWALK_PATH = REPORTS / "math16_method1_method2_extraction_closure_320.csv"


def authoritative_paths(model: str) -> list[tuple[str, Path]]:
    suffix = {
        "qwen9b": "qwen9b_fail_gated_authoritative_v1",
        "gemini": "gemini_fail_gated_authoritative_v1",
    }[model]
    definitions = [
        ("C0_C1", "math16_c0_c1_tier_a_reproducibility"),
        ("C1_C2", "math16_c1_c2_tier_b_reproducibility"),
        ("C2_C3", "math16_c2_c3_tier_c1_reproducibility"),
        ("C3_C4", "math16_c3_c4_tier_c2_reproducibility"),
        ("C4_C5a", "math16_c4_c5a_tier_d_d3_d1_reproducibility"),
        ("C5a_C5b", "math16_c5a_c5b_tier_d_d5_reproducibility"),
        ("C5b_C5c", "math16_c5b_c5c_tier_d_d2_reproducibility"),
    ]
    return [
        (name, RESULTS / f"{base}_{suffix}" / "transition_journal.jsonl")
        for name, base in definitions
    ]


def build_authoritative_model(model: str) -> tuple[list[dict[str, Any]], list[Path]]:
    stage_paths = authoritative_paths(model)
    stage_maps = {name: as_map(load_jsonl(path)) for name, path in stage_paths}
    input_paths = [path for _, path in stage_paths]
    first = stage_maps["C0_C1"]
    cell_ids = sorted(first)
    if len(cell_ids) != 320:
        raise ValueError(f"{model}: expected 320 C0_C1 cells, got {len(cell_ids)}")
    for name, rows in stage_maps.items():
        if set(rows) != set(cell_ids):
            raise ValueError(f"{model}: identity mismatch at {name}")

    transitions = (
        ("C0_C1", "C0", "C1"),
        ("C1_C2", "C1", "C2"),
        ("C2_C3", "C2", "C3"),
        ("C3_C4", "C3", "C4"),
        ("C4_C5a", "C4", "C5a"),
        ("C5a_C5b", "C5a", "C5b"),
        ("C5b_C5c", "C5b", "C5c"),
    )
    built: list[dict[str, Any]] = []
    for cell_id in cell_ids:
        first_row = first[cell_id]
        raw_task_id = first_row["task_id"]
        raw_condition = first_row["condition"]
        raw_seed = int(first_row["seed"])
        model_raw = first_row["model"]
        stages: dict[str, dict[str, Any]] = {}
        metric_events: dict[str, list[dict[str, Any]]] = {
            metric: [] for metric in ("eligible", "triggered", "modified", "abstained")
        }
        for index, (transition_name, pre_stage, post_stage) in enumerate(transitions):
            row = stage_maps[transition_name][cell_id]
            path = dict(stage_paths)[transition_name]
            evidence = [f"{rel(path)}#cell_id={cell_id}"]
            if index == 0:
                stages[pre_stage] = stage_record(
                    status=row["pre_status"],
                    source_path=row["pre_source_path"],
                    source_sha256=row["pre_source_sha256"],
                    status_provenance="DIRECT",
                    source_provenance="DIRECT",
                    evidence_refs=evidence,
                    account_basis="HISTORICAL_FROZEN",
                )
            stages[post_stage] = stage_record(
                status=row["post_status"],
                source_path=row["post_source_path"],
                source_sha256=row["post_source_sha256"],
                status_provenance="DIRECT",
                source_provenance="DIRECT",
                evidence_refs=evidence,
                account_basis="HISTORICAL_FROZEN",
            )
            eligible_key = "eligible_any" if "eligible_any" in row else "eligible"
            for metric, key in (
                ("eligible", eligible_key),
                ("triggered", "triggered"),
                ("modified", "modified"),
                ("abstained", "abstained"),
            ):
                if key not in row or not isinstance(row[key], bool):
                    raise ValueError(f"{model} {transition_name} missing boolean {key}")
                metric_events[metric].append(
                    event(row[key], applicable=True, provenance="DIRECT")
                )

        ever = {metric: aggregate_ever(events) for metric, events in metric_events.items()}
        baseline_frozen = {
            "status": stages["C0"]["status"],
            "source_path": stages["C0"]["source_path"],
            "source_sha256": stages["C0"]["source_sha256"],
            "status_provenance": "DIRECT",
            "source_provenance": "DIRECT",
            "evidence_refs": stages["C0"]["evidence_refs"],
        }
        baseline_corrected = {
            "status": None,
            "source_path": None,
            "source_sha256": None,
            "status_provenance": "NOT_APPLICABLE",
            "source_provenance": "NOT_APPLICABLE",
            "evidence_refs": [],
        }
        final_frozen = {
            "status": stages["C5c"]["status"],
            "source_path": stages["C5c"]["source_path"],
            "source_sha256": stages["C5c"]["source_sha256"],
            "status_provenance": "DIRECT",
            "source_provenance": "DIRECT",
            "evidence_refs": stages["C5c"]["evidence_refs"],
        }
        final_corrected = {
            "status": None,
            "source_path": None,
            "source_sha256": None,
            "status_provenance": "NOT_APPLICABLE",
            "source_provenance": "NOT_APPLICABLE",
            "evidence_refs": [],
        }
        formal_baseline_account = "BASELINE_FROZEN"
        formal_final_account = "FINAL_FROZEN"
        formal_baseline = explicit_select(
            formal_baseline_account,
            {"BASELINE_FROZEN": baseline_frozen, "BASELINE_CORRECTED": baseline_corrected},
        )
        formal_final = explicit_select(
            formal_final_account,
            {"FINAL_FROZEN": final_frozen, "AGGRESSIVE_CORRECTED": final_corrected},
        )
        built.append(
            make_row(
                model_group=model,
                model_raw=model_raw,
                raw_cell_id=cell_id,
                raw_task_id=raw_task_id,
                raw_condition=raw_condition,
                raw_seed=raw_seed,
                stages=stages,
                baseline_frozen=baseline_frozen,
                baseline_corrected=baseline_corrected,
                formal_baseline_account=formal_baseline_account,
                formal_baseline=formal_baseline,
                final_frozen=final_frozen,
                final_corrected=final_corrected,
                formal_final_account=formal_final_account,
                formal_final=formal_final,
                ever=ever,
                evidence_refs=sorted({ref for stage in stages.values() for ref in stage["evidence_refs"]}),
                lineage_exception_id=None,
            )
        )
    return built, input_paths


def q4_input_paths() -> dict[str, Path]:
    return {
        "c0_c1": RESULTS / "math16_c0_c1_tier_a_reproducibility_v1" / "transition_journal.jsonl",
        "c0_raw_dir": RESULTS / "math16_method2_all_cell_replay_v1" / "raw_sources",
        "c1_final_dir": RESULTS / "math16_c0_c1_tier_a_reproducibility_v1" / "final_sources",
        "b_census": MANIFESTS / "math16_c1_c2_tier_b_residual_supply_v1.json",
        "b_dev": RESULTS / "math16_c1_c2_tier_b_development_replay_v1" / "cell_results.jsonl",
        "c1_census": MANIFESTS / "math16_c2_c3_tier_c1_residual_supply_v1.json",
        "c2_census": MANIFESTS / "math16_c2_c4_tier_c2_residual_supply_v1.json",
        "c2_dev": RESULTS / "math16_c2_c4_tier_c2_development_replay_v1" / "cell_results.jsonl",
        "c4_closure": MANIFESTS / "math16_c4_final_source_closure_v1.json",
        "d_supply": MANIFESTS / "math16_c4_c5_tier_d_supply_v1.json",
        "d_dev": RESULTS / "math16_c4_c5_tier_d_d3_d1_development_replay_v1" / "cell_results.jsonl",
        "c5a_closure": MANIFESTS / "math16_c5a_final_source_closure_v1.json",
        "d5_d2_census": MANIFESTS / "math16_c5a_tier_d_d5_d2_residual_supply_v1.json",
        "d5_dev": RESULTS / "math16_c5a_tier_d_d5_development_replay_v1" / "cell_results.jsonl",
        "d2_dev": RESULTS / "math16_c5a_tier_d_d2_development_replay_v1" / "cell_results.jsonl",
    }


def manifest_eligible(status: str, token: str) -> bool:
    return status == token


def q4_metric_events(
    *,
    cell_id: str,
    stages: dict[str, dict[str, Any]],
    c0_c1: dict[str, Any],
    b_census: dict[str, dict[str, Any]],
    b_dev: dict[str, dict[str, Any]],
    c1_census: dict[str, dict[str, Any]],
    c2_census: dict[str, dict[str, Any]],
    c2_dev: dict[str, dict[str, Any]],
    d_supply: dict[str, dict[str, Any]],
    d_dev: dict[str, dict[str, Any]],
    d5_d2_census: dict[str, dict[str, Any]],
    d5_dev: dict[str, dict[str, Any]],
    d2_dev: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    metrics = {name: [] for name in ("eligible", "triggered", "modified", "abstained")}

    # A: full transition journal. Abstention was not persisted.
    metrics["eligible"].append(event(bool(c0_c1["eligible"]), applicable=True, provenance="DIRECT"))
    metrics["triggered"].append(
        event(bool(c0_c1["rule_triggered"]), applicable=True, provenance="DIRECT")
    )
    metrics["modified"].append(
        event(bool(c0_c1["source_changed"]), applicable=True, provenance="DIRECT")
    )
    metrics["abstained"].append(event(None, applicable=True, provenance="NOT_PERSISTED"))

    def add_stage(
        *,
        applicable: bool,
        development_row: dict[str, Any] | None,
        eligible_value: bool | None,
        eligible_provenance: str,
        composite: bool = True,
    ) -> None:
        if not applicable:
            for metric in metrics:
                metrics[metric].append(
                    event(None, applicable=False, provenance="NOT_APPLICABLE")
                )
            return
        if development_row is not None:
            eligibility = (
                bool(development_row["eligible"])
                if "eligible" in development_row
                else eligible_value
            )
            metrics["eligible"].append(
                event(eligibility, applicable=True, provenance="DIRECT")
            )
            for metric in ("triggered", "modified", "abstained"):
                value = development_row.get(metric)
                if not isinstance(value, bool):
                    value = None
                metrics[metric].append(
                    event(
                        value,
                        applicable=True,
                        provenance="DIRECT" if value is not None else "NOT_PERSISTED",
                    )
                )
            return
        metrics["eligible"].append(
            event(eligible_value, applicable=True, provenance=eligible_provenance)
        )
        # Missing mutation rows are not silently converted to FALSE.
        for metric in ("triggered", "modified", "abstained"):
            metrics[metric].append(
                event(None, applicable=True, provenance="NOT_PERSISTED")
            )

    # B applies only to C1 FAIL cells.
    b_applicable = stages["C1"]["status"] == "FAIL"
    b_manifest = b_census.get(cell_id)
    b_eligible = bool(b_manifest["eligible_rule_ids"]) if b_manifest else None
    add_stage(
        applicable=b_applicable,
        development_row=b_dev.get(cell_id),
        eligible_value=b_eligible,
        eligible_provenance="MANIFEST_DERIVED" if b_manifest else "NOT_PERSISTED",
    )

    # C1 applies to formal C2 FAIL cells. The corrected phantom cell is absent
    # from the frozen residual census and therefore remains coverage-incomplete.
    c1_applicable = stages["C2"]["status"] == "FAIL"
    c1_manifest = c1_census.get(cell_id)
    c1_eligible = (
        manifest_eligible(c1_manifest["status"], "C1_ELIGIBLE") if c1_manifest else None
    )
    add_stage(
        applicable=c1_applicable,
        development_row=None,
        eligible_value=c1_eligible,
        eligible_provenance="MANIFEST_DERIVED" if c1_manifest else "NOT_PERSISTED",
    )

    # C2 applies to formal C3 FAIL cells.
    c2_applicable = stages["C3"]["status"] == "FAIL"
    c2_manifest = c2_census.get(cell_id)
    c2_eligible = (
        manifest_eligible(c2_manifest["status"], "C2_ELIGIBLE") if c2_manifest else None
    )
    add_stage(
        applicable=c2_applicable,
        development_row=c2_dev.get(cell_id),
        eligible_value=c2_eligible,
        eligible_provenance="MANIFEST_DERIVED" if c2_manifest else "NOT_PERSISTED",
    )

    # D3 and D1 are two ordered events within C4->C5a.
    d_applicable = stages["C4"]["status"] == "FAIL"
    d_manifest = d_supply.get(cell_id)
    d_development = d_dev.get(cell_id)
    for rule_id, eligible_key in (
        ("TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1", "d3_eligible"),
        ("TIER_D_OPS_SHADOW_REMOVAL_V1", "d1_eligible"),
    ):
        per_rule = (
            (d_development.get("per_rule") or {}).get(rule_id)
            if d_development
            else None
        )
        if per_rule is not None:
            dev_row = {
                "eligible": bool(per_rule.get("census_eligible")),
                "triggered": per_rule.get("triggered"),
                "modified": per_rule.get("modified"),
                "abstained": per_rule.get("abstained"),
            }
        elif d_development is not None:
            dev_row = {
                "eligible": bool(d_development.get(eligible_key)),
                "triggered": None,
                "modified": None,
                "abstained": None,
            }
        else:
            dev_row = None
        rule_status = (
            (d_manifest.get("rules") or {}).get(rule_id, {}).get("status")
            if d_manifest
            else None
        )
        add_stage(
            applicable=d_applicable,
            development_row=dev_row,
            eligible_value=(rule_status == "ELIGIBLE") if rule_status is not None else None,
            eligible_provenance="MANIFEST_DERIVED" if rule_status is not None else "NOT_PERSISTED",
        )

    # D5 and D2.
    dd_manifest = d5_d2_census.get(cell_id)
    for pre_stage, dev_map, key, eligible_token in (
        ("C5a", d5_dev, "d5", "D5_RANKED_ELIGIBLE"),
        ("C5b", d2_dev, "d2", "D2_ELIGIBLE"),
    ):
        applicable = stages[pre_stage]["status"] == "FAIL"
        status = (dd_manifest.get(key) or {}).get("status") if dd_manifest else None
        add_stage(
            applicable=applicable,
            development_row=dev_map.get(cell_id),
            eligible_value=(status == eligible_token) if status is not None else None,
            eligible_provenance="MANIFEST_DERIVED" if status is not None else "NOT_PERSISTED",
        )

    return {metric: aggregate_ever(values) for metric, values in metrics.items()}


def build_qwen4b(
    overlay: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[Path]]:
    paths = q4_input_paths()
    c0_c1 = q4_map(load_jsonl(paths["c0_c1"]))
    baseline_frozen = as_map(load_jsonl(BASELINE_FROZEN_PATH))
    crosswalk = as_map(load_csv(BASELINE_CROSSWALK_PATH))
    b_census_obj = load_json(paths["b_census"])
    b_census = as_map(b_census_obj["cells"])
    b_dev = q4_map(load_jsonl(paths["b_dev"]))
    c1_census = as_map(load_json(paths["c1_census"])["cells"])
    c2_census = as_map(load_json(paths["c2_census"])["cells"])
    c2_dev = q4_map(load_jsonl(paths["c2_dev"]))
    c4_closure = as_map(load_json(paths["c4_closure"])["cells"])
    d_supply = as_map(load_json(paths["d_supply"])["cells"])
    d_dev = q4_map(load_jsonl(paths["d_dev"]))
    c5a_closure = as_map(load_json(paths["c5a_closure"])["cells"])
    d5_d2_census = as_map(load_json(paths["d5_d2_census"])["cells"])
    d5_dev = q4_map(load_jsonl(paths["d5_dev"]))
    d2_dev = q4_map(load_jsonl(paths["d2_dev"]))

    cell_ids = sorted(c0_c1)
    expected = set(cell_ids)
    if len(cell_ids) != 320:
        raise ValueError(f"qwen4b expected 320 identities, got {len(cell_ids)}")
    for name, mapping in (("baseline_frozen", baseline_frozen), ("crosswalk", crosswalk)):
        if set(mapping) != expected:
            raise ValueError(f"qwen4b {name} identity mismatch")
    if set(c5a_closure) != expected:
        raise ValueError("qwen4b C5a closure identity mismatch")

    anomaly = overlay["anomalous_cell"]
    anomaly_id = anomaly["cell_id"]
    if anomaly_id not in expected:
        raise ValueError("Overlay anomalous cell is not in qwen4b population")

    built: list[dict[str, Any]] = []
    for cell_id in cell_ids:
        c01 = c0_c1[cell_id]
        identity = c01["cell_identity"]
        raw_task_id = identity["task_id"]
        raw_condition = identity["condition"]
        raw_seed = int(identity["seed"])
        c0_source_path = rel(paths["c0_raw_dir"] / f"{cell_id}.py")
        c1_source_path = rel(paths["c1_final_dir"] / f"{cell_id}.py")

        # Formal Historical stage curve. C0 is the corrected baseline account.
        stages: dict[str, dict[str, Any]] = {}
        stages["C0"] = stage_record(
            status=crosswalk[cell_id]["method2_raw_status"],
            source_path=c0_source_path,
            source_sha256=crosswalk[cell_id]["method2_raw_source_sha256"],
            status_provenance="OVERLAY",
            source_provenance="MANIFEST_DERIVED",
            evidence_refs=[
                f"{rel(BASELINE_CROSSWALK_PATH)}#cell_id={cell_id}",
                f"{rel(paths['c0_c1'])}#cell_id={cell_id}",
            ],
            account_basis="BASELINE_CORRECTED",
        )
        stages["C1"] = stage_record(
            status=c01["final_status"],
            source_path=c1_source_path,
            source_sha256=c01["final_source_sha256"],
            status_provenance="DIRECT",
            source_provenance="MANIFEST_DERIVED",
            evidence_refs=[f"{rel(paths['c0_c1'])}#cell_id={cell_id}"],
            account_basis="HISTORICAL_FROZEN",
        )

        # C2 frozen transition, then explicit overlay correction if applicable.
        if cell_id in b_dev:
            b = b_dev[cell_id]
            c2_status = b["post_pass_fail"]
            c2_path = b["post_source_path"]
            c2_sha = b["post_source_sha256"]
            c2_status_prov = c2_source_prov = "DIRECT"
            c2_refs = [f"{rel(paths['b_dev'])}#cell_id={cell_id}"]
        else:
            c2_status = stages["C1"]["status"]
            c2_path = stages["C1"]["source_path"]
            c2_sha = stages["C1"]["source_sha256"]
            c2_status_prov = c2_source_prov = "MANIFEST_DERIVED"
            c2_refs = [f"{rel(paths['b_census'])}#cell_id={cell_id}"]
        if cell_id == anomaly_id:
            c2_status = anomaly["sealed_source_revalidated_final_status"]
            c2_path = anomaly["c5a_final_source_path"]
            c2_sha = anomaly["c5a_final_source_sha256_text_utf8"]
            c2_status_prov = c2_source_prov = "OVERLAY"
            c2_refs.append(f"{rel(AGGRESSIVE_OVERLAY_PATH)}#anomalous_cell")
        stages["C2"] = stage_record(
            status=c2_status,
            source_path=c2_path,
            source_sha256=c2_sha,
            status_provenance=c2_status_prov,
            source_provenance=c2_source_prov,
            evidence_refs=c2_refs,
            account_basis="AGGRESSIVE_CORRECTED" if cell_id == anomaly_id else "HISTORICAL_FROZEN",
        )
        stages["C3"] = dict(stages["C2"])
        stages["C3"]["evidence_refs"] = list(stages["C2"]["evidence_refs"]) + [
            f"{rel(paths['c1_census'])}#cell_id={cell_id}"
        ]

        # C4.
        if cell_id in c2_dev and cell_id != anomaly_id:
            c2d = c2_dev[cell_id]
            stages["C4"] = stage_record(
                status=c2d["post_pass_fail"],
                source_path=c2d["post_source_path"],
                source_sha256=c2d["post_source_sha256"],
                status_provenance="DIRECT",
                source_provenance="DIRECT",
                evidence_refs=[f"{rel(paths['c2_dev'])}#cell_id={cell_id}"],
                account_basis="HISTORICAL_FROZEN",
            )
        else:
            stages["C4"] = dict(stages["C3"])
            stages["C4"]["evidence_refs"] = list(stages["C3"]["evidence_refs"]) + [
                f"{rel(paths['c2_census'])}#cell_id={cell_id}"
            ]

        # Frozen C5a closure, corrected for the one overlay cell.
        c5 = c5a_closure[cell_id]
        c5a_status = c5["c5a_outcome"]
        c5a_path = c5["c5a_final_source_path"]
        c5a_sha = c5["c5a_final_source_sha256"]
        c5a_status_prov = c5a_source_prov = "MANIFEST_DERIVED"
        c5a_refs = [f"{rel(paths['c5a_closure'])}#cell_id={cell_id}"]
        if cell_id == anomaly_id:
            c5a_status = anomaly["sealed_source_revalidated_final_status"]
            c5a_path = anomaly["c5a_final_source_path"]
            c5a_sha = anomaly["c5a_final_source_sha256_text_utf8"]
            c5a_status_prov = c5a_source_prov = "OVERLAY"
            c5a_refs.append(f"{rel(AGGRESSIVE_OVERLAY_PATH)}#anomalous_cell")
        stages["C5a"] = stage_record(
            status=c5a_status,
            source_path=c5a_path,
            source_sha256=c5a_sha,
            status_provenance=c5a_status_prov,
            source_provenance=c5a_source_prov,
            evidence_refs=c5a_refs,
            account_basis="AGGRESSIVE_CORRECTED" if cell_id == anomaly_id else "HISTORICAL_FROZEN",
        )

        # D5 and D2 overrides never change PASS/FAIL in the frozen evidence.
        if cell_id in d5_dev:
            d5 = d5_dev[cell_id]
            stages["C5b"] = stage_record(
                status=d5["post_pass_fail"],
                source_path=d5["post_source_path"],
                source_sha256=d5["post_source_sha256"],
                status_provenance="DIRECT",
                source_provenance="DIRECT",
                evidence_refs=[f"{rel(paths['d5_dev'])}#cell_id={cell_id}"],
                account_basis="HISTORICAL_FROZEN",
            )
        else:
            stages["C5b"] = dict(stages["C5a"])
            stages["C5b"]["evidence_refs"] = list(stages["C5a"]["evidence_refs"]) + [
                f"{rel(paths['d5_d2_census'])}#cell_id={cell_id}"
            ]
        if cell_id in d2_dev:
            d2 = d2_dev[cell_id]
            stages["C5c"] = stage_record(
                status=d2["post_pass_fail"],
                source_path=d2["post_source_path"],
                source_sha256=d2["post_source_sha256"],
                status_provenance="DIRECT",
                source_provenance="DIRECT",
                evidence_refs=[f"{rel(paths['d2_dev'])}#cell_id={cell_id}"],
                account_basis="HISTORICAL_FROZEN",
            )
        else:
            stages["C5c"] = dict(stages["C5b"])
            stages["C5c"]["evidence_refs"] = list(stages["C5b"]["evidence_refs"]) + [
                f"{rel(paths['d5_d2_census'])}#cell_id={cell_id}"
            ]

        frozen_baseline_row = baseline_frozen[cell_id]
        baseline_frozen_account = {
            "status": normalize_status(frozen_baseline_row["final_status"]),
            "source_path": None,
            "source_sha256": frozen_baseline_row["raw_artifact_sha256"],
            "status_provenance": "DIRECT",
            "source_provenance": "NOT_PERSISTED",
            "evidence_refs": [f"{rel(BASELINE_FROZEN_PATH)}#cell_id={cell_id}"],
        }
        baseline_corrected_account = {
            "status": normalize_status(crosswalk[cell_id]["method2_raw_status"]),
            "source_path": c0_source_path,
            "source_sha256": crosswalk[cell_id]["method2_raw_source_sha256"],
            "status_provenance": "OVERLAY",
            "source_provenance": "OVERLAY",
            "evidence_refs": [f"{rel(BASELINE_CROSSWALK_PATH)}#cell_id={cell_id}"],
        }
        formal_baseline_account = "BASELINE_CORRECTED"
        formal_baseline = explicit_select(
            formal_baseline_account,
            {
                "BASELINE_FROZEN": baseline_frozen_account,
                "BASELINE_CORRECTED": baseline_corrected_account,
            },
        )

        # The frozen final account is reconstructed without applying the overlay.
        frozen_final = dict(c5a_closure[cell_id])
        frozen_final_status = normalize_status(frozen_final["c5a_outcome"])
        frozen_final_path = frozen_final["c5a_final_source_path"]
        frozen_final_sha = frozen_final["c5a_final_source_sha256"]
        frozen_final_refs = [f"{rel(paths['c5a_closure'])}#cell_id={cell_id}"]
        if cell_id in d5_dev:
            d5 = d5_dev[cell_id]
            frozen_final_status = normalize_status(d5["post_pass_fail"])
            frozen_final_path = d5["post_source_path"]
            frozen_final_sha = d5["post_source_sha256"]
            frozen_final_refs.append(f"{rel(paths['d5_dev'])}#cell_id={cell_id}")
        if cell_id in d2_dev:
            d2 = d2_dev[cell_id]
            frozen_final_status = normalize_status(d2["post_pass_fail"])
            frozen_final_path = d2["post_source_path"]
            frozen_final_sha = d2["post_source_sha256"]
            frozen_final_refs.append(f"{rel(paths['d2_dev'])}#cell_id={cell_id}")
        final_frozen_account = {
            "status": frozen_final_status,
            "source_path": frozen_final_path,
            "source_sha256": frozen_final_sha,
            "status_provenance": "MANIFEST_DERIVED",
            "source_provenance": "MANIFEST_DERIVED",
            "evidence_refs": frozen_final_refs,
        }
        if cell_id == anomaly_id:
            corrected_status = normalize_status(anomaly["sealed_source_revalidated_final_status"])
            corrected_path = anomaly["c5a_final_source_path"]
            corrected_sha = anomaly["c5a_final_source_sha256_text_utf8"]
        else:
            # Explicit overlay application: the overlay declares one unique
            # mismatch; all other cells retain their frozen final fact.
            corrected_status = final_frozen_account["status"]
            corrected_path = final_frozen_account["source_path"]
            corrected_sha = final_frozen_account["source_sha256"]
        final_corrected_account = {
            "status": corrected_status,
            "source_path": corrected_path,
            "source_sha256": corrected_sha,
            "status_provenance": "OVERLAY",
            "source_provenance": "OVERLAY",
            "evidence_refs": frozen_final_refs
            + [f"{rel(AGGRESSIVE_OVERLAY_PATH)}#qwen4b_aggressive_round1"],
        }
        formal_final_account = "AGGRESSIVE_CORRECTED"
        formal_final = explicit_select(
            formal_final_account,
            {
                "FINAL_FROZEN": final_frozen_account,
                "AGGRESSIVE_CORRECTED": final_corrected_account,
            },
        )

        ever = q4_metric_events(
            cell_id=cell_id,
            stages=stages,
            c0_c1=c01,
            b_census=b_census,
            b_dev=b_dev,
            c1_census=c1_census,
            c2_census=c2_census,
            c2_dev=c2_dev,
            d_supply=d_supply,
            d_dev=d_dev,
            d5_d2_census=d5_d2_census,
            d5_dev=d5_dev,
            d2_dev=d2_dev,
        )
        evidence_refs = sorted(
            {
                ref
                for stage in stages.values()
                for ref in stage["evidence_refs"]
            }
            | {
                f"{rel(BASELINE_FROZEN_PATH)}#cell_id={cell_id}",
                f"{rel(BASELINE_CROSSWALK_PATH)}#cell_id={cell_id}",
                f"{rel(AGGRESSIVE_OVERLAY_PATH)}#qwen4b_aggressive_round1",
            }
        )
        built.append(
            make_row(
                model_group="qwen4b",
                model_raw=frozen_baseline_row["model"],
                raw_cell_id=cell_id,
                raw_task_id=raw_task_id,
                raw_condition=raw_condition,
                raw_seed=raw_seed,
                stages=stages,
                baseline_frozen=baseline_frozen_account,
                baseline_corrected=baseline_corrected_account,
                formal_baseline_account=formal_baseline_account,
                formal_baseline=formal_baseline,
                final_frozen=final_frozen_account,
                final_corrected=final_corrected_account,
                formal_final_account=formal_final_account,
                formal_final=formal_final,
                ever=ever,
                evidence_refs=evidence_refs,
                lineage_exception_id=(
                    "math16_qwen4b_c4_c5a_source_label_promotion_mismatch_v1"
                    if cell_id == anomaly_id
                    else None
                ),
            )
        )

    input_paths = [
        BASELINE_FROZEN_PATH,
        BASELINE_CROSSWALK_PATH,
        AGGRESSIVE_OVERLAY_PATH,
        THREE_MODEL_SUMMARY_PATH,
    ] + [path for name, path in paths.items() if not name.endswith("_dir")]
    return built, input_paths


def make_row(
    *,
    model_group: str,
    model_raw: str,
    raw_cell_id: str,
    raw_task_id: str,
    raw_condition: str,
    raw_seed: int,
    stages: dict[str, dict[str, Any]],
    baseline_frozen: dict[str, Any],
    baseline_corrected: dict[str, Any],
    formal_baseline_account: str,
    formal_baseline: dict[str, Any],
    final_frozen: dict[str, Any],
    final_corrected: dict[str, Any],
    formal_final_account: str,
    formal_final: dict[str, Any],
    ever: dict[str, dict[str, Any]],
    evidence_refs: list[str],
    lineage_exception_id: str | None,
) -> dict[str, Any]:
    baseline_status = formal_baseline["status"]
    final_status = formal_final["status"]
    rescue = baseline_status == "FAIL" and final_status == "PASS"
    regression = baseline_status == "PASS" and final_status == "FAIL"
    preserved_pass = baseline_status == "PASS" and final_status == "PASS"
    ever_modified = ever["modified"]["value"]
    if baseline_status == "FAIL" and final_status == "FAIL":
        if ever_modified is True:
            unchanged_fail: bool | None = False
            modified_still_failed: bool | None = True
        elif ever_modified is False:
            unchanged_fail = True
            modified_still_failed = False
        else:
            unchanged_fail = None
            modified_still_failed = None
    else:
        unchanged_fail = False
        modified_still_failed = False

    row: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "account_namespace": ACCOUNT_NAMESPACE,
        "dataset_id": "Math16",
        "model_group": model_group,
        "model": model_raw,
        "raw_cell_id": raw_cell_id,
        "raw_task_id": raw_task_id,
        "raw_condition": raw_condition,
        "raw_seed": raw_seed,
        "canonical_condition": canonical_condition(raw_condition),
        "canonical_identity": canonical_identity(raw_task_id, raw_condition, raw_seed),
    }
    for stage in STAGES:
        if stage not in stages:
            raise ValueError(f"{raw_cell_id}: missing stage {stage}")
        row[stage] = stages[stage]
    row.update(
        {
            "baseline_frozen_status": baseline_frozen["status"],
            "baseline_frozen_source_path": baseline_frozen["source_path"],
            "baseline_frozen_source_sha256": baseline_frozen["source_sha256"],
            "baseline_frozen_status_provenance": baseline_frozen["status_provenance"],
            "baseline_frozen_source_provenance": baseline_frozen["source_provenance"],
            "baseline_corrected_status": baseline_corrected["status"],
            "baseline_corrected_source_path": baseline_corrected["source_path"],
            "baseline_corrected_source_sha256": baseline_corrected["source_sha256"],
            "baseline_corrected_status_provenance": baseline_corrected["status_provenance"],
            "baseline_corrected_source_provenance": baseline_corrected["source_provenance"],
            "formal_baseline_account": formal_baseline_account,
            "formal_baseline_status": formal_baseline["status"],
            "formal_baseline_source_path": formal_baseline["source_path"],
            "formal_baseline_source_sha256": formal_baseline["source_sha256"],
            "final_frozen_status": final_frozen["status"],
            "final_frozen_source_path": final_frozen["source_path"],
            "final_frozen_source_sha256": final_frozen["source_sha256"],
            "final_frozen_status_provenance": final_frozen["status_provenance"],
            "final_frozen_source_provenance": final_frozen["source_provenance"],
            "final_corrected_status": final_corrected["status"],
            "final_corrected_source_path": final_corrected["source_path"],
            "final_corrected_source_sha256": final_corrected["source_sha256"],
            "final_corrected_status_provenance": final_corrected["status_provenance"],
            "final_corrected_source_provenance": final_corrected["source_provenance"],
            "formal_final_account": formal_final_account,
            "formal_final_status": formal_final["status"],
            "formal_final_source_path": formal_final["source_path"],
            "formal_final_source_sha256": formal_final["source_sha256"],
            "formal_rescue": rescue,
            "formal_regression": regression,
            "formal_preserved_pass": preserved_pass,
            "formal_unchanged_fail": unchanged_fail,
            "modified_still_failed": modified_still_failed,
            "modified_still_failed_provenance": (
                ever["modified"]["provenance"]
                if modified_still_failed is not None
                else "DIAGNOSTIC_PENDING"
            ),
            "lineage_exception_id": lineage_exception_id,
            "evidence_refs": evidence_refs,
        }
    )
    for metric in ("eligible", "triggered", "modified", "abstained"):
        aggregate = ever[metric]
        row[f"ever_{metric}"] = aggregate["value"]
        row[f"ever_{metric}_coverage_complete"] = aggregate["coverage_complete"]
        row[f"ever_{metric}_true_event_count"] = aggregate["true_event_count"]
        row[f"ever_{metric}_false_event_count"] = aggregate["false_event_count"]
        row[f"ever_{metric}_unknown_event_count"] = aggregate["unknown_event_count"]
        row[f"ever_{metric}_provenance"] = aggregate["provenance"]
    return row


def validate_sources(rows: list[dict[str, Any]]) -> dict[str, Any]:
    missing: list[dict[str, str]] = []
    mismatches: list[dict[str, str]] = []
    checked = 0
    cache: dict[str, str] = {}
    for row in rows:
        for stage in STAGES:
            record = row[stage]
            source_path = record["source_path"]
            expected_sha = record["source_sha256"]
            checked += 1
            absolute = ROOT / source_path
            try:
                if source_path not in cache:
                    cache[source_path] = sha256_source_text(absolute)
            except FileNotFoundError:
                missing.append(
                    {"raw_cell_id": row["raw_cell_id"], "stage": stage, "path": source_path}
                )
                continue
            if cache[source_path] != expected_sha:
                mismatches.append(
                    {
                        "raw_cell_id": row["raw_cell_id"],
                        "stage": stage,
                        "path": source_path,
                        "expected": expected_sha,
                        "actual": cache[source_path],
                    }
                )
    return {
        "stage_source_checks": checked,
        "unique_stage_source_paths": len(cache),
        "source_path_missing": len(missing),
        "source_sha_mismatch": len(mismatches),
        "missing_examples": missing[:10],
        "mismatch_examples": mismatches[:10],
    }


def value_distribution(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts = Counter("NULL" if row[field] is None else str(row[field]).upper() for row in rows)
    return {key: counts.get(key, 0) for key in ("TRUE", "FALSE", "NULL")}


def pass_count(rows: list[dict[str, Any]], field: str) -> int:
    return sum(row[field] == "PASS" for row in rows)


def validate(
    rows: list[dict[str, Any]],
    *,
    summary: dict[str, Any],
    overlay: dict[str, Any],
    head: str,
) -> dict[str, Any]:
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    model_rows = {model: [row for row in rows if row["model_group"] == model] for model in MODEL_ORDER}
    require(len(rows) == 960, f"row_count={len(rows)} expected=960")
    for model in MODEL_ORDER:
        require(len(model_rows[model]) == 320, f"{model}_rows={len(model_rows[model])}")

    pk = [
        (row["account_namespace"], row["model_group"], row["canonical_identity"])
        for row in rows
    ]
    raw_pk = [(row["account_namespace"], row["raw_cell_id"]) for row in rows]
    require(len(pk) == len(set(pk)), "primary_key_duplicate")
    require(len(raw_pk) == len(set(raw_pk)), "raw_identity_duplicate")

    canonical_sets = {
        model: {row["canonical_identity"] for row in model_rows[model]}
        for model in MODEL_ORDER
    }
    common = set.intersection(*canonical_sets.values())
    union = set.union(*canonical_sets.values())
    require(len(common) == 320, f"canonical_common={len(common)}")
    require(len(union) == 320, f"canonical_union={len(union)}")
    unmatched = sum(len(union - identities) for identities in canonical_sets.values())
    require(unmatched == 0, f"canonical_unmatched={unmatched}")

    qwen_raw_spec = sum(
        row["raw_condition"] == "ab2d_spec_v2"
        for model in ("qwen4b", "qwen9b")
        for row in model_rows[model]
    )
    gemini_raw_spec = sum(
        row["raw_condition"] == "ab2d_spec" for row in model_rows["gemini"]
    )
    require(qwen_raw_spec == 160, f"qwen_raw_ab2d_spec_v2={qwen_raw_spec}")
    require(gemini_raw_spec == 80, f"gemini_raw_ab2d_spec={gemini_raw_spec}")

    source_validation = validate_sources(rows)
    require(source_validation["source_path_missing"] == 0, "source_path_missing")
    require(source_validation["source_sha_mismatch"] == 0, "source_sha_mismatch")

    q4 = model_rows["qwen4b"]
    q9 = model_rows["qwen9b"]
    gem = model_rows["gemini"]
    calculated = {
        "qwen4b": {
            "baseline_frozen_pass": pass_count(q4, "baseline_frozen_status"),
            "baseline_corrected_pass": pass_count(q4, "baseline_corrected_status"),
            "final_frozen_pass": pass_count(q4, "final_frozen_status"),
            "final_corrected_pass": pass_count(q4, "final_corrected_status"),
            "formal_baseline_pass": pass_count(q4, "formal_baseline_status"),
            "formal_final_pass": pass_count(q4, "formal_final_status"),
            "formal_rescue": sum(row["formal_rescue"] for row in q4),
        },
        "qwen9b": {
            "formal_baseline_pass": pass_count(q9, "formal_baseline_status"),
            "formal_final_pass": pass_count(q9, "formal_final_status"),
            "formal_rescue": sum(row["formal_rescue"] for row in q9),
        },
        "gemini": {
            "formal_baseline_pass": pass_count(gem, "formal_baseline_status"),
            "formal_final_pass": pass_count(gem, "formal_final_status"),
            "formal_rescue": sum(row["formal_rescue"] for row in gem),
        },
    }
    required_counts = {
        "qwen4b": {
            "baseline_frozen_pass": 78,
            "baseline_corrected_pass": 79,
            "final_frozen_pass": 88,
            "final_corrected_pass": 87,
            "formal_baseline_pass": 79,
            "formal_final_pass": 87,
            "formal_rescue": 8,
        },
        "qwen9b": {
            "formal_baseline_pass": 101,
            "formal_final_pass": 102,
            "formal_rescue": 1,
        },
        "gemini": {
            "formal_baseline_pass": 289,
            "formal_final_pass": 289,
            "formal_rescue": 0,
        },
    }
    require(calculated == required_counts, f"formal_counts={calculated!r}")

    # Independently cross-check input headline artifacts.
    require(summary["models"]["qwen4b"]["baseline_pass"] == 79, "summary q4 baseline")
    require(summary["models"]["qwen4b"]["final_pass"] == 88, "summary q4 frozen final")
    require(summary["models"]["qwen9b"]["baseline_pass"] == 101, "summary q9 baseline")
    require(summary["models"]["qwen9b"]["final_pass"] == 102, "summary q9 final")
    require(summary["models"]["gemini"]["baseline_pass"] == 289, "summary gem baseline")
    require(summary["models"]["gemini"]["final_pass"] == 289, "summary gem final")
    require(
        overlay["qwen4b_aggressive_round1"]["frozen"]["final_pass"] == 88,
        "overlay q4 frozen final",
    )
    require(
        overlay["qwen4b_aggressive_round1"]["corrected"]["final_pass"] == 87,
        "overlay q4 corrected final",
    )
    require(
        overlay["qwen4b_aggressive_round1"]["corrected"]["verified_rescue"] == 8,
        "overlay q4 corrected rescue",
    )

    formal_baseline_total = sum(
        pass_count(model_rows[model], "formal_baseline_status") for model in MODEL_ORDER
    )
    formal_final_total = sum(
        pass_count(model_rows[model], "formal_final_status") for model in MODEL_ORDER
    )
    require(formal_baseline_total == 469, f"formal_baseline_total={formal_baseline_total}")
    require(formal_final_total == 478, f"formal_final_total={formal_final_total}")

    require(
        all(row["account_namespace"] == ACCOUNT_NAMESPACE for row in rows),
        "non-historical namespace present",
    )
    namespace_counts = Counter(row["account_namespace"] for row in rows)
    safety_rows = namespace_counts.get("safety_benchmark", 0)
    fixpoint_rows = namespace_counts.get("post_final_fixpoint", 0)
    require(safety_rows == 0, "safety rows present")
    require(fixpoint_rows == 0, "fixpoint rows present")

    for row in rows:
        for metric in ("eligible", "triggered", "modified", "abstained"):
            value = row[f"ever_{metric}"]
            coverage = row[f"ever_{metric}_coverage_complete"]
            true_count = row[f"ever_{metric}_true_event_count"]
            if value is False:
                require(coverage, f"{row['raw_cell_id']} ever_{metric}=FALSE incomplete")
            if value is None:
                require(
                    not coverage and true_count == 0,
                    f"{row['raw_cell_id']} ever_{metric}=NULL invalid",
                )
            if value is True:
                require(true_count > 0, f"{row['raw_cell_id']} ever_{metric}=TRUE no evidence")
        if row["model_group"] == "qwen4b":
            if (
                row["ever_modified"] is False
                and row["ever_modified_provenance"] != "DIRECT"
            ):
                errors.append(
                    f"{row['raw_cell_id']} q4 modified FALSE without complete DIRECT events"
                )
        for key, value in row.items():
            if key.endswith("_provenance") and value not in PROVENANCE_VALUES:
                errors.append(f"{row['raw_cell_id']} bad provenance {key}={value}")

    stage_pass_curves = {
        model: {
            stage: sum(row[stage]["status"] == "PASS" for row in model_rows[model])
            for stage in STAGES
        }
        for model in MODEL_ORDER
    }
    expected_curves = {
        "qwen4b": overlay["qwen4b_aggressive_round1"]["corrected"]["pass_curve"],
        "qwen9b": summary["models"]["qwen9b"]["pass_curve"],
        "gemini": summary["models"]["gemini"]["pass_curve"],
    }
    require(stage_pass_curves == expected_curves, f"stage_pass_curves={stage_pass_curves!r}")

    lineage_exceptions = [
        row for row in rows if row["lineage_exception_id"] is not None
    ]
    require(len(lineage_exceptions) == 1, f"lineage_exception_count={len(lineage_exceptions)}")
    require(
        lineage_exceptions
        and lineage_exceptions[0]["raw_cell_id"] == overlay["anomalous_cell"]["cell_id"],
        "lineage exception cell mismatch",
    )

    ever_distribution = {
        model: {
            metric: value_distribution(model_rows[model], f"ever_{metric}")
            for metric in ("eligible", "triggered", "modified", "abstained")
        }
        for model in MODEL_ORDER
    }
    summary_object = {
        "schema_version": SCHEMA_VERSION,
        "account_namespace": ACCOUNT_NAMESPACE,
        "head": head,
        "verdict": "PASS" if not errors else "FAIL",
        "row_counts": {
            "total": len(rows),
            "by_model": {model: len(model_rows[model]) for model in MODEL_ORDER},
            "safety_benchmark": safety_rows,
            "post_final_fixpoint": fixpoint_rows,
        },
        "identity_validation": {
            "primary_key_duplicates": len(pk) - len(set(pk)),
            "raw_identity_duplicates": len(raw_pk) - len(set(raw_pk)),
            "canonical_identity_common": len(common),
            "canonical_identity_union": len(union),
            "canonical_unmatched": unmatched,
            "qwen_raw_ab2d_spec_v2": qwen_raw_spec,
            "gemini_raw_ab2d_spec": gemini_raw_spec,
        },
        "source_validation": source_validation,
        "formal_accounts": calculated,
        "formal_totals": {
            "baseline_pass": formal_baseline_total,
            "final_pass": formal_final_total,
            "rescue": sum(row["formal_rescue"] for row in rows),
            "regression": sum(row["formal_regression"] for row in rows),
        },
        "stage_pass_curves": stage_pass_curves,
        "ever_distribution": ever_distribution,
        "lineage_exception_count": len(lineage_exceptions),
        "lineage_exception_cell_id": (
            lineage_exceptions[0]["raw_cell_id"] if lineage_exceptions else None
        ),
        "invariants": {
            "exactly_960_rows": len(rows) == 960,
            "each_model_320": all(len(model_rows[m]) == 320 for m in MODEL_ORDER),
            "pk_duplicate_zero": len(pk) == len(set(pk)),
            "raw_identity_duplicate_zero": len(raw_pk) == len(set(raw_pk)),
            "canonical_common_320_unmatched_zero": len(common) == len(union) == 320
            and unmatched == 0,
            "raw_condition_alias_preserved": qwen_raw_spec == 160
            and gemini_raw_spec == 80,
            "source_path_missing_zero": source_validation["source_path_missing"] == 0,
            "source_sha_mismatch_zero": source_validation["source_sha_mismatch"] == 0,
            "q4_four_accounts_and_formal": calculated["qwen4b"]
            == required_counts["qwen4b"],
            "q9_formal_101_102": calculated["qwen9b"]
            == required_counts["qwen9b"],
            "gemini_formal_289_289": calculated["gemini"]
            == required_counts["gemini"],
            "formal_total_469_478": formal_baseline_total == 469
            and formal_final_total == 478,
            "safety_fixpoint_excluded": safety_rows == 0 and fixpoint_rows == 0,
            "coverage_aware_ever_aggregation": not any(
                row[f"ever_{metric}"] is False
                and not row[f"ever_{metric}_coverage_complete"]
                for row in rows
                for metric in ("eligible", "triggered", "modified", "abstained")
            ),
            "q4_missing_mutation_not_false": not any(
                row["model_group"] == "qwen4b"
                and row["ever_modified"] is False
                and row["ever_modified_provenance"] != "DIRECT"
                for row in rows
            ),
            "one_sealed_lineage_exception": len(lineage_exceptions) == 1,
        },
        "errors": errors,
    }
    if errors:
        raise RuntimeError(json.dumps(summary_object, ensure_ascii=False, indent=2))
    return summary_object


def canonical_json(value: Any, *, pretty: bool = False) -> str:
    if pretty:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with open(long_path(temp), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.replace(long_path(temp), long_path(path))


def build_sha_manifest(
    *,
    head: str,
    input_paths: list[Path],
) -> dict[str, Any]:
    artifacts = []
    for path in (Path(__file__).resolve(), LEDGER_PATH, VALIDATION_PATH):
        artifacts.append(
            {
                "path": rel(path),
                "sha256": sha256_bytes(path),
                "size_bytes": len(read_bytes(path)),
            }
        )
    evidence_inputs = []
    seen: set[str] = set()
    for path in sorted(input_paths, key=lambda p: rel(p)):
        relative = rel(path)
        if relative in seen:
            continue
        seen.add(relative)
        evidence_inputs.append(
            {
                "path": relative,
                "sha256": sha256_bytes(path),
                "size_bytes": len(read_bytes(path)),
            }
        )
    return {
        "manifest_id": f"{SCHEMA_VERSION}_sha256_manifest",
        "schema_version": SCHEMA_VERSION,
        "head": head,
        "hash_algorithm": "SHA-256",
        "source_text_hash_policy": "UTF-8 text with universal-newline normalization for stage source validation",
        "manifest_self_hash": "EXCLUDED_BY_DESIGN",
        "artifacts": artifacts,
        "evidence_inputs": evidence_inputs,
        "declarations": [
            "historical_round1_only",
            "safety_benchmark_excluded",
            "post_final_fixpoint_excluded",
            "no_model_healer_candidate_replay_or_evaluator_execution",
            "frozen_and_corrected_accounts_preserved_separately",
        ],
    }


def main() -> None:
    head = git_head()
    summary = load_json(THREE_MODEL_SUMMARY_PATH)
    overlay = load_json(AGGRESSIVE_OVERLAY_PATH)
    q4_rows, q4_inputs = build_qwen4b(overlay)
    q9_rows, q9_inputs = build_authoritative_model("qwen9b")
    gemini_rows, gemini_inputs = build_authoritative_model("gemini")
    rows = q4_rows + q9_rows + gemini_rows
    rows.sort(
        key=lambda row: (
            MODEL_ORDER.index(row["model_group"]),
            row["canonical_identity"],
            row["raw_cell_id"],
        )
    )
    validation = validate(rows, summary=summary, overlay=overlay, head=head)

    ledger_text = "\n".join(canonical_json(row) for row in rows) + "\n"
    validation_text = canonical_json(validation, pretty=True)
    write_atomic(LEDGER_PATH, ledger_text)
    write_atomic(VALIDATION_PATH, validation_text)
    sha_manifest = build_sha_manifest(
        head=head,
        input_paths=q4_inputs
        + q9_inputs
        + gemini_inputs
        + [THREE_MODEL_SUMMARY_PATH, AGGRESSIVE_OVERLAY_PATH],
    )
    write_atomic(SHA_MANIFEST_PATH, canonical_json(sha_manifest, pretty=True))
    print(
        canonical_json(
            {
                "verdict": validation["verdict"],
                "ledger": rel(LEDGER_PATH),
                "validation": rel(VALIDATION_PATH),
                "sha_manifest": rel(SHA_MANIFEST_PATH),
                "rows": validation["row_counts"],
            },
            pretty=True,
        ),
        end="",
    )


if __name__ == "__main__":
    main()
