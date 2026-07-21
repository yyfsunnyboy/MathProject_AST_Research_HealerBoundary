# -*- coding: utf-8 -*-
"""Math16 Pilot-02 Full 320-cell Evaluation Revision v4_r001 (offline).

Re-scores existing raw_response with post-ORACLE_SCHEMA_AUDIT_V1 oracle normalize.
Never calls Gemini or any other LLM. Does not overwrite v3_r001 artifacts.

Blinded baseline → Taxonomy v3 → frozen MathHealerRunner → summaries/report.
Never calls Gemini or any other LLM.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

EVAL_MANIFEST_PATH = ROOT / "docs/experiments/manifests/math16_pilot02_full_evaluation_v4_r001_manifest.json"
V3_BASELINE_PATH = ROOT / "docs/experiments/results/math16_pilot02_full_evaluation_v3_r001/cell_level_baseline.jsonl"
ORACLE_SCHEMA_AUDIT_V1 = "docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1.md"
TAXONOMY_JSON_PATH = ROOT / "docs/experiments/taxonomy/ai_generated_program_failure_taxonomy_v3.json"
TAXONOMY_MD_PATH = ROOT / "docs/決賽文件/20260720_AI 生成程式共同失敗分類標準_實際使用版 v3.md"
SPEC_MANIFEST_PATH = ROOT / "docs/experiments/prompts/ab2d_spec/manifest.json"
INTEGER_BASELINE_PATH = (
    ROOT / "docs/experiments/results/math16_pilot02_integer_evaluation_v3_r001/cell_level_baseline.jsonl"
)

EXPECTED_TAXONOMY_SHA = "7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304"
RESULTS_PARENT = ROOT / "docs/experiments/results"

CONDITION_DISPLAY = {
    "ab1": "Ab1",
    "ab2g": "Ab2g",
    "ab2d": "Ab2d+api",
    "ab2d_spec": "Ab2d+spec",
}
FAMILY_DISPLAY = {
    "integer": "Integer",
    "polynomial": "Polynomial",
    "radical": "Radical",
    "fraction": "Fraction",
}

# Retraceable to docs/experiments/audits/math16_pilot02_oracle_schema_audit_v1.md
SCHEMA_GAP_BY_TASK: dict[str, str] = {
    "ce111_q02_polynomial_division_remainder": "GAP_CONFIRMED:evaluate_polynomial_division_remainder_only",
    "ce111_q08_polynomial_factor_parameter_recovery": "GAP_CONFIRMED:evaluate_polynomial_factor_parameter_recovery",
    "ce115_calc_polynomial_factor_roots_l1": "GAP_CONFIRMED:evaluate_math16_polynomial_factor_roots",
    "ce111_q10_ordered_quadratic_roots_radical": "GAP_CONFIRMED:evaluate_compound_radical_result",
    "ce112_q04_radical_simplification": "GAP_SUSPECTED:evaluate_radical_simplification_canonical",
    "ce115_calc_radical_simplification_l1": "GAP_SUSPECTED:evaluate_math16_radical_simplification",
    "ce111_q05_exact_fraction_expression": "GAP_SUSPECTED:evaluate_exact_fraction_canonical",
    "ce112_q12_independent_probability_fraction": "GAP_SUSPECTED:evaluate_exact_fraction_canonical",
    "ce113_q01_negative_fraction_subtraction": "GAP_SUSPECTED:evaluate_exact_fraction_canonical",
    "ce115_calc_exact_rational_expression_l1": "GAP_SUSPECTED:evaluate_math16_exact_rational_expression",
}


def _load_v3_baseline_index() -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for line in V3_BASELINE_PATH.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        index[row["cell_id"]] = row
    if len(index) != 320:
        raise ValueError(f"Expected 320 v3 baseline rows, got {len(index)}")
    return index



def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _runtime_fingerprint(raw_manifest: dict[str, Any]) -> str:
    keys = [
        "experiment_id",
        "model_provider",
        "model_tag",
        "model_version",
        "runtime",
        "runtime_version",
        "thinking_mode",
        "temperature",
        "top_p",
        "top_k",
        "max_output_tokens",
        "timeout_seconds",
        "retry_policy",
        "seed_list",
        "source_commit",
    ]
    sub = {k: raw_manifest[k] for k in keys}
    serialized = json.dumps(sub, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _load_family_and_api_policy() -> tuple[dict[str, str], dict[str, str]]:
    spec = json.loads(SPEC_MANIFEST_PATH.read_text(encoding="utf-8"))
    family: dict[str, str] = {}
    api_policy: dict[str, str] = {}
    for task in spec["tasks"]:
        family[task["task_id"]] = task["family"]
        api_policy[task["task_id"]] = task["api_policy"]
    return family, api_policy


def _empty_layer_counter() -> dict[str, int]:
    return {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5": 0}


def _gate_init() -> dict[str, str]:
    return {
        "g1_parse": "PASS",
        "g2_execution": "PASS",
        "g3_contract": "PASS",
        "g3e_entry_point": "PASS",
        "g3a_required_api": "NOT_APPLICABLE",
        "g3s_output_schema": "PASS",
        "g3c_canonical_form": "NOT_APPLICABLE",
        "g4_correctness": "PASS",
    }


def classify_outcome_to_v3(
    outcome: str,
    details: dict[str, Any],
    *,
    api_policy: str,
) -> dict[str, Any]:
    gates = _gate_init()
    if api_policy in {"API-only", "mixed"}:
        gates["g3a_required_api"] = "PASS"

    primary_failure_layer = "PASSED"
    final_status = "PASSED"
    failure_subtype = None
    mechanism_tags: list[str] = []
    exception_type = None
    exception_message = None
    first_failure_location = None
    failure_chain: list[dict[str, Any]] = []
    classification_status = "ADJUDICATED"
    outcome_validity = "VALID_MODEL_OUTCOME"

    # classify_math16_response flattens detail=* into the top-level details dict.
    detail = details.get("detail") if isinstance(details.get("detail"), dict) else {}
    g2_gate = ((details.get("evaluation_gates") or {}).get("g2_executability") or {})

    if outcome in {"empty_response", "catastrophic_truncation", "extraction_failure", "parse_minor"}:
        gates["g1_parse"] = "FAIL"
        gates["g2_execution"] = "NOT_ASSESSED"
        gates["g3_contract"] = "NOT_ASSESSED"
        gates["g3e_entry_point"] = "NOT_ASSESSED"
        if api_policy in {"API-only", "mixed"}:
            gates["g3a_required_api"] = "NOT_ASSESSED"
        gates["g3s_output_schema"] = "NOT_ASSESSED"
        gates["g4_correctness"] = "NOT_ASSESSED"
        final_status = "FAILED"
        primary_failure_layer = "L1"
        failure_subtype = "PARSE_ERROR"
        mechanism_tags = ["candidate_extraction_failure"]
        first_failure_location = "g1_parse"
        if outcome == "catastrophic_truncation":
            mechanism_tags.append("truncation")
        if outcome == "parse_minor":
            mechanism_tags = ["format_contamination"]
            exception_type = "SyntaxError"
            exception_message = str(
                detail.get("parse_error") or details.get("parse_error") or ""
            )
        failure_chain = [{"stage": "baseline", "layer": "L1", "outcome": outcome}]
    elif outcome == "missing_entry_point":
        gates["g3e_entry_point"] = "FAIL"
        gates["g3_contract"] = "FAIL"
        gates["g4_correctness"] = "NOT_ASSESSED"
        final_status = "FAILED"
        primary_failure_layer = "L2"
        failure_subtype = "ENTRY_POINT_MISMATCH"
        entry_count = detail.get("entry_point_count") or details.get("entry_point_count")
        if isinstance(entry_count, int) and entry_count > 1:
            mechanism_tags = ["ambiguous_entry_point"]
        else:
            mechanism_tags = ["entry_point_mismatch"]
        first_failure_location = "g3e_entry_point"
        failure_chain = [{"stage": "baseline", "layer": "L2", "outcome": outcome}]
    elif outcome == "runtime_failure":
        gates["g2_execution"] = "FAIL"
        gates["g3_contract"] = "NOT_ASSESSED"
        gates["g4_correctness"] = "NOT_ASSESSED"
        final_status = "FAILED"
        err_msg = str(
            detail.get("runtime_error")
            or details.get("runtime_error")
            or g2_gate.get("exception_message")
            or ""
        )
        exception_message = err_msg
        exception_type = g2_gate.get("exception_type")
        if not exception_type and ":" in err_msg:
            exception_type = err_msg.split(":", 1)[0].strip()
        ops_tokens = (
            "IntegerOps",
            "PolynomialOps",
            "RadicalOps",
            "FractionOps",
            "domain_function_library",
            "Ops.",
        )
        # Prefer L3 for clear Domain API import / call / routing failures.
        if exception_type in {"ImportError", "ModuleNotFoundError"} and "domain_function_library" in err_msg:
            primary_failure_layer = "L3"
            failure_subtype = "DOMAIN_API_IMPORT_ERROR"
            mechanism_tags = ["domain_api_import_error"]
            first_failure_location = (
                "g3a_required_api" if api_policy in {"API-only", "mixed"} else "g2_execution"
            )
            if api_policy in {"API-only", "mixed"}:
                gates["g3a_required_api"] = "FAIL"
        elif any(tok in err_msg for tok in ops_tokens):
            primary_failure_layer = "L3"
            failure_subtype = "DOMAIN_API_CALL_ERROR"
            mechanism_tags = ["invalid_api_call"]
            first_failure_location = "domain_api"
            if api_policy in {"API-only", "mixed"}:
                gates["g3a_required_api"] = "FAIL"
        else:
            primary_failure_layer = "L4"
            failure_subtype = "RUNTIME_EXCEPTION"
            if "import" in err_msg.lower() or exception_type in {"ImportError", "ModuleNotFoundError"}:
                mechanism_tags = ["general_missing_import"]
            elif exception_type == "NameError":
                mechanism_tags = ["undefined_name"]
            elif exception_type in {"RecursionError"}:
                mechanism_tags = ["recursion_failure"]
            elif exception_type in {"TimeoutError"}:
                mechanism_tags = ["execution_timeout"]
            else:
                mechanism_tags = ["control_flow_failure"]
            first_failure_location = "g2_execution"
        failure_chain = [{"stage": "baseline", "layer": primary_failure_layer, "outcome": outcome}]
    elif outcome == "schema_failure":
        gates["g3s_output_schema"] = "FAIL"
        gates["g3_contract"] = "FAIL"
        gates["g4_correctness"] = "NOT_ASSESSED"
        final_status = "FAILED"
        primary_failure_layer = "L2"
        failure_subtype = "OUTPUT_SCHEMA_MISMATCH"
        mechanism_tags = ["output_packaging", "schema_mismatch"]
        first_failure_location = "g3s_output_schema"
        failure_chain = [{"stage": "baseline", "layer": "L2", "outcome": outcome}]
    elif outcome in {"answer_incorrect", "latex_mismatch", "structural_mismatch"}:
        gates["g4_correctness"] = "FAIL"
        final_status = "FAILED"
        primary_failure_layer = "L5"
        failure_subtype = "CORRECTNESS_FAIL"
        mechanism_tags = ["algorithmic_error"]
        if outcome == "latex_mismatch":
            mechanism_tags = ["canonical_form_mismatch"]
            gates["g3c_canonical_form"] = "FAIL"
        first_failure_location = "g4_correctness"
        failure_chain = [{"stage": "baseline", "layer": "L5", "outcome": outcome}]
    elif outcome == "passed":
        final_status = "PASSED"
        primary_failure_layer = "PASSED"
        failure_chain = []
    else:
        # Unknown classifier outcome — do NOT map to L5.
        final_status = "FAILED"
        primary_failure_layer = None
        classification_status = "PENDING_REVIEW"
        outcome_validity = "PENDING_REVIEW"
        mechanism_tags = ["needs_human_review"]
        first_failure_location = "unknown"
        failure_chain = [{"stage": "baseline", "layer": "UNKNOWN", "outcome": outcome}]

    return {
        "gates": gates,
        "final_status": final_status,
        "baseline_outcome": final_status,
        "primary_failure_layer": None if primary_failure_layer == "PASSED" else primary_failure_layer,
        "earliest_blocking_layer": None if primary_failure_layer == "PASSED" else primary_failure_layer,
        "failure_subtype": failure_subtype,
        "mechanism_tags": mechanism_tags,
        "exception_type": exception_type,
        "exception_class": exception_type,
        "exception_message": exception_message,
        "first_failure_location": first_failure_location,
        "failure_chain": failure_chain,
        "classification_status": classification_status,
        "outcome_validity": outcome_validity,
        "classifier_outcome": outcome,
    }


def probe_healer_hits(source: str, context: dict[str, Any]) -> list[str]:
    from agent_tools.finals_rebuild.ce115_research_healer_runner import (
        RULE_ALLOWLIST,
        RULE_REGISTRY,
    )

    hits: list[str] = []
    if not source or not source.strip():
        return hits
    for rule_id in RULE_ALLOWLIST:
        rule = RULE_REGISTRY[rule_id]
        applicable, _, _ = rule.is_applicable(source, context)
        if not applicable:
            continue
        triggered, _ = rule.is_triggered(source, context)
        if triggered:
            hits.append(rule_id)
    return hits


def decide_healer_eligibility(
    *,
    baseline_passed: bool,
    source: str | None,
    context: dict[str, Any],
    mechanism_tags: list[str],
    classification_status: str,
) -> dict[str, Any]:
    if baseline_passed:
        return {
            "healer_eligible": False,
            "healer_eligibility": "noneligible",
            "eligibility_reason": "Baseline first attempt passed.",
            "healer_decision": "no_trigger",
            "matched_rule": None,
            "probe_hits": [],
        }
    if classification_status == "PENDING_REVIEW":
        return {
            "healer_eligible": False,
            "healer_eligibility": "undetermined",
            "eligibility_reason": "Pending review; healer abstains.",
            "healer_decision": "abstained",
            "matched_rule": None,
            "probe_hits": [],
        }
    if "ambiguous_entry_point" in mechanism_tags:
        return {
            "healer_eligible": False,
            "healer_eligibility": "noneligible",
            "eligibility_reason": "Ambiguous entry point; frozen healer abstains.",
            "healer_decision": "abstained",
            "matched_rule": None,
            "probe_hits": [],
        }
    if not source:
        return {
            "healer_eligible": False,
            "healer_eligibility": "noneligible",
            "eligibility_reason": "No extractable candidate source for frozen healer.",
            "healer_decision": "abstained",
            "matched_rule": None,
            "probe_hits": [],
        }
    hits = probe_healer_hits(source, context)
    if hits:
        return {
            "healer_eligible": True,
            "healer_eligibility": "eligible",
            "eligibility_reason": "Frozen precondition symptom matched: " + ", ".join(hits),
            "healer_decision": None,  # filled after run
            "matched_rule": hits[0],
            "probe_hits": hits,
        }
    return {
        "healer_eligible": False,
        "healer_eligibility": "noneligible",
        "eligibility_reason": "No frozen allowlist rule triggered.",
        "healer_decision": "abstained",
        "matched_rule": None,
        "probe_hits": [],
    }


def do_preflight_checks(manifest: dict[str, Any]) -> dict[str, Any]:
    print("Executing zero-result full evaluation preflight...")

    if not TAXONOMY_MD_PATH.exists():
        raise FileNotFoundError(f"Taxonomy Markdown not found at: {TAXONOMY_MD_PATH}")
    md_sha = _hash_file(TAXONOMY_MD_PATH)
    if md_sha != EXPECTED_TAXONOMY_SHA:
        raise ValueError(f"Taxonomy Markdown SHA mismatch. Expected {EXPECTED_TAXONOMY_SHA}, got {md_sha}")
    print(f"Taxonomy Markdown verified. SHA-256: {md_sha}")

    if not TAXONOMY_JSON_PATH.exists():
        raise FileNotFoundError(f"Taxonomy JSON not found at: {TAXONOMY_JSON_PATH}")
    tax = json.loads(TAXONOMY_JSON_PATH.read_text(encoding="utf-8"))
    if tax.get("source_file_sha256") != md_sha:
        raise ValueError("Taxonomy JSON source SHA does not match MD file SHA")

    if manifest.get("evaluation_revision") != "v4_r001":
        raise ValueError("Manifest evaluation_revision mismatch")
    if manifest.get("taxonomy_file_sha256") != md_sha:
        raise ValueError("Manifest taxonomy SHA mismatch")

    inv_path = ROOT / manifest["inventory_reference"]
    if not inv_path.exists():
        raise FileNotFoundError(f"Inventory not found: {inv_path}")
    inv_sha = _hash_file(inv_path)
    if inv_sha != manifest["inventory_file_sha256"]:
        raise ValueError(f"Inventory SHA mismatch: expected {manifest['inventory_file_sha256']}, got {inv_sha}")

    inventory = json.loads(inv_path.read_text(encoding="utf-8"))
    if len(inventory) != manifest["expected_cell_count"]:
        raise ValueError(f"Inventory size mismatch: {len(inventory)}")

    cell_ids = [c["cell_id"] for c in inventory]
    if len(set(cell_ids)) != 320:
        raise ValueError(f"Duplicate cell_ids: unique={len(set(cell_ids))}")

    family_map, _api = _load_family_and_api_policy()
    cond_counts = Counter(c["condition"] for c in inventory)
    seed_counts = Counter(c["seed"] for c in inventory)
    family_counts = Counter(family_map[c["task_id"]] for c in inventory)
    reused_counts = Counter(bool(c.get("reused")) for c in inventory)

    if dict(cond_counts) != {c: 80 for c in ("ab1", "ab2g", "ab2d", "ab2d_spec")}:
        raise ValueError(f"Condition geometry mismatch: {dict(cond_counts)}")
    if any(seed_counts[s] != 64 for s in manifest["seed_list"]):
        raise ValueError(f"Seed geometry mismatch: {dict(seed_counts)}")
    if dict(family_counts) != {f: 80 for f in ("integer", "polynomial", "radical", "fraction")}:
        raise ValueError(f"Family geometry mismatch: {dict(family_counts)}")
    if reused_counts[True] != 80 or reused_counts[False] != 240:
        raise ValueError(f"Reused geometry mismatch: {dict(reused_counts)}")

    fingerprints: dict[str, str] = {}
    for key, rel in manifest["raw_result_roots"].items():
        raw_root = ROOT / rel
        raw_manifest = json.loads((raw_root / "manifest.json").read_text(encoding="utf-8"))
        fingerprints[key] = _runtime_fingerprint(raw_manifest)

    prompt_unchanged = 0
    raw_present = 0
    for cell in inventory:
        cell_dir = RESULTS_PARENT / cell["output_relative_path"]
        artifact_path = cell_dir / "artifact.json"
        raw_path = cell_dir / "raw_response.txt"
        prompt_path = cell_dir / "prompt.txt"
        if not artifact_path.exists() or not raw_path.exists() or not prompt_path.exists():
            raise FileNotFoundError(f"Missing cell assets for {cell['cell_id']}")
        art = json.loads(artifact_path.read_text(encoding="utf-8"))
        if art.get("persisted_complete") is not True:
            raise ValueError(f"Incomplete cell: {cell['cell_id']}")
        if art.get("prompt_sha256") != cell["prompt_sha256"]:
            raise ValueError(f"Prompt SHA mismatch for {cell['cell_id']}")
        expected_fp = fingerprints["integer_reused"] if cell.get("reused") else fingerprints["full_new"]
        if art.get("runtime_config_fingerprint") != expected_fp:
            raise ValueError(
                f"Runtime fingerprint mismatch for {cell['cell_id']}: "
                f"{art.get('runtime_config_fingerprint')} != {expected_fp}"
            )
        prompt_unchanged += 1
        raw_present += 1

    from agent_tools.finals_rebuild.ce115_research_healer_runner import RULE_ALLOWLIST

    expected_allowlist = set(manifest["healer_allowlist"])
    if set(RULE_ALLOWLIST) != expected_allowlist:
        raise ValueError(f"Frozen healer allowlist mismatch: {RULE_ALLOWLIST}")

    report = {
        "taxonomy_md_sha256": md_sha,
        "inventory_sha256": inv_sha,
        "expected_cell_count": 320,
        "unique_cell_ids": 320,
        "duplicate": 0,
        "missing": 0,
        "condition_counts": dict(cond_counts),
        "family_counts": dict(family_counts),
        "seed_counts": {str(k): v for k, v in seed_counts.items()},
        "reused_counts": {"integer_80": reused_counts[True], "new_240": reused_counts[False]},
        "runtime_fingerprints": fingerprints,
        "prompt_sha_verified": prompt_unchanged,
        "raw_present": raw_present,
        "healer_allowlist": list(RULE_ALLOWLIST),
    }
    print("--- Zero-Result Preflight Report ---")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Zero-Result Preflight PASS.")
    return report


def _inc_layer(bucket: dict[str, Any], layer: str | None) -> None:
    if layer in bucket:
        bucket[layer] += 1


def run_evaluation(manifest: dict[str, Any]) -> None:
    from agent_tools.finals_rebuild.ce115_research_healer_runner import (
        MathHealerRunner,
        RULE_ALLOWLIST,
    )
    from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id
    from scripts.run_math16_latex_v1_gemini_live import classify_math16_response, extract_code

    print("Starting full Math16 320-cell offline v4 re-score (0 LLM calls)...")
    family_map, api_policy_map = _load_family_and_api_policy()
    tasks = tasks_by_id()
    inventory = json.loads((ROOT / manifest["inventory_reference"]).read_text(encoding="utf-8"))
    v3_index = _load_v3_baseline_index()
    eval_hash = _hash_file(ROOT / "scripts/evaluate_math16_pilot02_full_v4.py")
    taxonomy_hash = _hash_file(TAXONOMY_MD_PATH)
    oracle_hash = _hash_file(ROOT / "agent_tools/finals_rebuild/math16_oracles.py")
    schema_flip_count = 0
    schema_flip_by_gap: dict[str, int] = {}

    output_dir = RESULTS_PARENT / manifest["evaluation_id"]
    output_dir.mkdir(parents=True, exist_ok=True)
    execution_manifest_file = output_dir / "execution_manifest.json"
    if execution_manifest_file.exists():
        existing = json.loads(execution_manifest_file.read_text(encoding="utf-8"))
        if existing.get("evaluation_revision") != manifest["evaluation_revision"]:
            raise RuntimeError("Incompatible evaluation revision directory exists")

    healer_runner = MathHealerRunner(max_passes=int(manifest["healer_max_passes"]))

    fingerprints: dict[str, str] = {}
    for key, rel in manifest["raw_result_roots"].items():
        raw_manifest = json.loads((ROOT / rel / "manifest.json").read_text(encoding="utf-8"))
        fingerprints[key] = _runtime_fingerprint(raw_manifest)

    cell_level_baseline: list[dict[str, Any]] = []
    healer_results: list[dict[str, Any]] = []
    evaluation_inventory: list[dict[str, Any]] = []

    total_count = 0
    baseline_passed = 0
    post_healer_passed = 0
    layers_count = _empty_layer_counter()
    validity_count = {
        "VALID_MODEL_OUTCOME": 0,
        "INVALID_EVALUATOR": 0,
        "INVALID_CONTRACT": 0,
        "INVALID_INFRASTRUCTURE": 0,
        "PENDING_REVIEW": 0,
    }
    mechanism_counts: Counter[str] = Counter()
    exception_counts: Counter[str] = Counter()
    g_stats = {
        "G1_FAIL": 0,
        "G2_FAIL": 0,
        "G3_FAIL": 0,
        "G4_FAIL": 0,
        "G1_PASS": 0,
        "G2_PASS": 0,
        "G3_PASS": 0,
        "G4_PASS": 0,
    }

    healer_eligibility_count = {"eligible": 0, "noneligible": 0, "undetermined": 0}
    healer_decision_count = {
        "transformed": 0,
        "abstained": 0,
        "no_trigger": 0,
        "rejected": 0,
        "not_run": 0,
    }
    healer_outcome_count = {
        "rescue_to_pass": 0,
        "changed_partial_progress": 0,
        "preserved_pass": 0,
        "unchanged_fail": 0,
        "regression": 0,
        "rollback": 0,
        "not_assessed": 0,
    }

    condition_stats: dict[str, dict[str, Any]] = {}
    family_stats: dict[str, dict[str, Any]] = {}
    task_stats: dict[str, dict[str, Any]] = {}
    seed_stats: dict[str, dict[str, Any]] = {}
    condition_family_task: dict[str, Any] = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

    def _ensure_bucket(store: dict[str, dict[str, Any]], key: str) -> dict[str, Any]:
        if key not in store:
            store[key] = {
                "total": 0,
                "baseline_passed": 0,
                "baseline_failed": 0,
                "post_healer_passed": 0,
                "post_healer_failed": 0,
                "eligible": 0,
                "transformed": 0,
                "rescued": 0,
                "regressed": 0,
                "abstained": 0,
                "preserved_pass": 0,
                **_empty_layer_counter(),
            }
        return store[key]

    for idx, cell in enumerate(inventory):
        cell_id = cell["cell_id"]
        tid = cell["task_id"]
        cond = cell["condition"]
        seed = cell["seed"]
        family = family_map[tid]
        api_policy = api_policy_map[tid]
        reused = bool(cell.get("reused"))
        cell_dir = RESULTS_PARENT / cell["output_relative_path"]
        art = json.loads((cell_dir / "artifact.json").read_text(encoding="utf-8"))
        raw_response = (cell_dir / "raw_response.txt").read_text(encoding="utf-8")
        prompt_text = (cell_dir / "prompt.txt").read_text(encoding="utf-8")
        runtime_fp = fingerprints["integer_reused"] if reused else fingerprints["full_new"]

        task = tasks[tid]
        frozen = frozen_for_prompt(task)
        frozen_params = frozen["oracle_payload"]

        outcome, source, details = classify_math16_response(
            raw_response,
            frozen_params=frozen_params,
            audit_oracle_payload=task["oracle_payload"],
            task=task,
        )
        mapped = classify_outcome_to_v3(outcome, details, api_policy=api_policy)
        gates = mapped["gates"]

        total_count += 1
        is_pass = mapped["final_status"] == "PASSED"
        if is_pass:
            baseline_passed += 1
        else:
            _inc_layer(layers_count, mapped["primary_failure_layer"])

        validity_count[mapped["outcome_validity"]] = validity_count.get(mapped["outcome_validity"], 0) + 1
        for tag in mapped["mechanism_tags"]:
            mechanism_counts[tag] += 1
        if mapped["exception_class"]:
            exception_counts[mapped["exception_class"]] += 1

        for gkey, gstat in (
            ("g1_parse", "G1"),
            ("g2_execution", "G2"),
            ("g3_contract", "G3"),
            ("g4_correctness", "G4"),
        ):
            if gates[gkey] == "FAIL":
                g_stats[f"{gstat}_FAIL"] += 1
            elif gates[gkey] == "PASS":
                g_stats[f"{gstat}_PASS"] += 1

        context = {"task": task, "frozen": frozen_params}
        eligibility = decide_healer_eligibility(
            baseline_passed=is_pass,
            source=source,
            context=context,
            mechanism_tags=mapped["mechanism_tags"],
            classification_status=mapped["classification_status"],
        )

        healer_ran = False
        transformed = False
        repaired_source = None
        repaired_sha = None
        rolled_back = False
        matched_rule = eligibility["matched_rule"]
        healer_decision = eligibility["healer_decision"]
        post_status = mapped["final_status"]
        post_layer = mapped["primary_failure_layer"]
        post_outcome_label = "PASSED" if is_pass else (mapped["primary_failure_layer"] or "UNKNOWN")
        healer_outcome = "preserved_pass" if is_pass else "unchanged_fail"
        provenance: list[dict[str, Any]] = []
        post_classifier_outcome = outcome

        if eligibility["healer_eligible"]:
            assert source is not None
            result = healer_runner.run(source, context=context)
            healer_ran = True
            provenance = [
                {
                    "pass_index": p.pass_index,
                    "selected_rule_id": p.selected_rule_id,
                    "changed": p.changed,
                    "final_status": p.final_status,
                    "stop_reason": p.stop_reason,
                }
                for p in result.provenance
            ]
            changed = any(p.changed for p in result.provenance)
            rolled_back = bool(result.rolled_back)
            if changed and not rolled_back:
                transformed = True
                healer_decision = "transformed"
                repaired_source = result.output_source
                repaired_sha = _hash_text(repaired_source)
                matched_rule = next(
                    (p.selected_rule_id for p in result.provenance if p.changed),
                    matched_rule,
                )
                post_outcome, _post_source, _post_details = classify_math16_response(
                    repaired_source,
                    frozen_params=frozen_params,
                    audit_oracle_payload=task["oracle_payload"],
                    task=task,
                )
                post_classifier_outcome = post_outcome
                post_mapped = classify_outcome_to_v3(post_outcome, _post_details, api_policy=api_policy)
                post_status = post_mapped["final_status"]
                post_layer = post_mapped["primary_failure_layer"]
                post_outcome_label = "PASSED" if post_status == "PASSED" else (post_layer or "UNKNOWN")
                if is_pass and post_status != "PASSED":
                    healer_outcome = "regression"
                elif (not is_pass) and post_status == "PASSED":
                    healer_outcome = "rescue_to_pass"
                else:
                    healer_outcome = "changed_partial_progress"
            elif rolled_back:
                healer_decision = "transformed"
                transformed = True
                healer_outcome = "rollback"
                repaired_sha = None
            else:
                healer_decision = "abstained"
                healer_outcome = "unchanged_fail"

        # Boolean convenience flags (mutually exclusive rescued/regressed)
        rescued = healer_outcome == "rescue_to_pass"
        regressed = healer_outcome == "regression"
        preserved_pass = healer_outcome == "preserved_pass"
        abstained = healer_decision == "abstained"

        if post_status == "PASSED":
            post_healer_passed += 1

        healer_eligibility_count[eligibility["healer_eligibility"]] += 1
        healer_decision_count[healer_decision or "not_run"] += 1
        healer_outcome_count[healer_outcome] += 1

        for store, key in (
            (condition_stats, cond),
            (family_stats, family),
            (task_stats, tid),
            (seed_stats, str(seed)),
        ):
            b = _ensure_bucket(store, key)
            b["total"] += 1
            if is_pass:
                b["baseline_passed"] += 1
            else:
                b["baseline_failed"] += 1
                _inc_layer(b, mapped["primary_failure_layer"])
            if post_status == "PASSED":
                b["post_healer_passed"] += 1
            else:
                b["post_healer_failed"] += 1
            if eligibility["healer_eligible"]:
                b["eligible"] += 1
            if transformed:
                b["transformed"] += 1
            if rescued:
                b["rescued"] += 1
            if regressed:
                b["regressed"] += 1
            if abstained:
                b["abstained"] += 1
            if preserved_pass:
                b["preserved_pass"] += 1

        # per condition × family × task pass rates (baseline)
        cft = condition_family_task[cond][family][tid]
        cft.setdefault("total", 0)
        cft.setdefault("baseline_passed", 0)
        cft.setdefault("post_healer_passed", 0)
        cft["total"] += 1
        if is_pass:
            cft["baseline_passed"] += 1
        if post_status == "PASSED":
            cft["post_healer_passed"] += 1

        extracted = extract_code(raw_response)
        cand_code = extracted.extracted_code or ""
        cand_hash = _hash_text(cand_code) if cand_code else None
        raw_hash = _hash_text(raw_response)
        prompt_hash_actual = _hash_text(prompt_text.replace("\r\n", "\n"))

        inv_row = {
            "cell_id": cell_id,
            "task_id": tid,
            "family": family,
            "condition": cond,
            "condition_display": CONDITION_DISPLAY[cond],
            "seed": seed,
            "raw_response_path": str((cell_dir / "raw_response.txt").relative_to(ROOT)).replace("\\", "/"),
            "prompt_sha256": cell["prompt_sha256"],
            "runtime_fingerprint": runtime_fp,
            "generation_status": "complete",
            "source_inventory": "reused_integer" if reused else "full_new",
            "reused": reused,
            "output_relative_path": cell["output_relative_path"],
        }
        evaluation_inventory.append(inv_row)

        cell_record = {
            "dataset": "CE115_Math16",
            "task_id": tid,
            "family": family,
            "cell_id": cell_id,
            "model": "gemini-3.5-flash",
            "condition": cond,
            "condition_display": CONDITION_DISPLAY[cond],
            "seed": seed,
            "evidence_role": "post_hoc_exploratory",
            "split_id": (
                "math16_pilot02_integer_gemini_freeze_v1"
                if reused
                else "math16_pilot02_full_gemini_freeze_v1"
            ),
            "run_id": (
                "math16_pilot02_integer_gemini_freeze_v1"
                if reused
                else "math16_pilot02_full_gemini_freeze_v1"
            ),
            "prompt_hash": cell["prompt_sha256"],
            "prompt_sha256_verified": prompt_hash_actual == cell["prompt_sha256"]
            or art.get("prompt_sha256") == cell["prompt_sha256"],
            "candidate_hash": cand_hash,
            "raw_response_hash": raw_hash,
            "runtime_fingerprint": runtime_fp,
            "evaluator_hash": eval_hash,
            "evaluation_revision": manifest["evaluation_revision"],
            "infrastructure_valid": True,
            "raw_response_present": True,
            "candidate_present": bool(cand_code),
            "api_policy": api_policy,
            "g1_parse": gates["g1_parse"],
            "g2_execution": gates["g2_execution"],
            "g3_contract": gates["g3_contract"],
            "g3e_entry_point": gates["g3e_entry_point"],
            "g3a_required_api": gates["g3a_required_api"],
            "g3s_output_schema": gates["g3s_output_schema"],
            "g3c_canonical_form": gates["g3c_canonical_form"],
            "g4_correctness": gates["g4_correctness"],
            "G1": gates["g1_parse"],
            "G2": gates["g2_execution"],
            "G3": gates["g3_contract"],
            "G4": gates["g4_correctness"],
            "final_status": mapped["final_status"],
            "baseline_outcome": mapped["baseline_outcome"],
            "legacy_failure_category": art.get("evaluator_status"),
            "classification_status": mapped["classification_status"],
            "primary_failure_layer": mapped["primary_failure_layer"],
            "earliest_blocking_layer": mapped["earliest_blocking_layer"],
            "failure_subtype": mapped["failure_subtype"],
            "mechanism_tags": mapped["mechanism_tags"],
            "outcome_validity": mapped["outcome_validity"],
            "responsibility_notes": "Model generated code logic.",
            "failure_chain": mapped["failure_chain"],
            "exception_type": mapped["exception_type"],
            "exception_class": mapped["exception_class"],
            "exception_message": mapped["exception_message"],
            "first_failure_location": mapped["first_failure_location"],
            "classifier_outcome": mapped["classifier_outcome"],
            "healer_eligible": eligibility["healer_eligible"],
            "healer_eligibility": eligibility["healer_eligibility"],
            "eligibility_reason": eligibility["eligibility_reason"],
            "healer_decision": healer_decision,
            "matched_rule": matched_rule,
            "transformed": transformed,
            "healer_outcome": healer_outcome,
            "post_healer_outcome": post_outcome_label,
            "rescued": rescued,
            "regressed": regressed,
            "preserved_pass": preserved_pass,
            "abstained": abstained,
            "review_status": "adjudicated" if mapped["classification_status"] == "ADJUDICATED" else "pending_review",
            "reviewer_id": "automatic_evaluator",
            "reviewed_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "notes": "",
        }
        v3_row = v3_index[cell_id]
        v3_pass = v3_row["final_status"] == "PASSED"
        v4_pass = mapped["final_status"] == "PASSED"
        changed = v3_pass != v4_pass
        gap_id = SCHEMA_GAP_BY_TASK.get(tid)
        if changed:
            schema_flip_count += 1
            if gap_id:
                schema_flip_by_gap[gap_id] = schema_flip_by_gap.get(gap_id, 0) + 1
        cell_record.update(
            {
                "v3_final_status": v3_row["final_status"],
                "v3_primary_failure_layer": v3_row.get("primary_failure_layer"),
                "v4_final_status": mapped["final_status"],
                "v4_primary_failure_layer": mapped["primary_failure_layer"],
                "changed_by_evaluator_fix": changed,
                "schema_gap_id": gap_id if changed else (gap_id if gap_id else None),
                "schema_gap_id_on_change": gap_id if changed else None,
                "v3_evaluation_revision": "v3_r001",
                "oracle_source_sha256": oracle_hash,
            }
        )
        # Keep schema_gap_id even when unchanged for GAP tasks (traceability).
        if gap_id and not changed:
            cell_record["schema_gap_id"] = gap_id
        cell_level_baseline.append(cell_record)

        healer_record = {
            "cell_id": cell_id,
            "task_id": tid,
            "family": family,
            "condition": cond,
            "condition_display": CONDITION_DISPLAY[cond],
            "seed": seed,
            "baseline_status": "PASSED" if is_pass else (mapped["primary_failure_layer"] or "UNKNOWN"),
            "baseline_outcome": mapped["baseline_outcome"],
            "healer_ran": healer_ran,
            "healer_eligible": eligibility["healer_eligible"],
            "healer_eligibility": eligibility["healer_eligibility"],
            "healer_decision": healer_decision,
            "matched_rule": matched_rule,
            "probe_hits": eligibility["probe_hits"],
            "transformed": transformed,
            "changed": transformed,
            "rolled_back": rolled_back,
            "repaired_source_sha256": repaired_sha,
            "healer_outcome": healer_outcome,
            "post_healer_outcome": post_outcome_label,
            "post_healer_status": post_outcome_label,
            "post_classifier_outcome": post_classifier_outcome,
            "rescued": rescued,
            "regressed": regressed,
            "preserved_pass": preserved_pass,
            "abstained": abstained,
            "allowlist": list(RULE_ALLOWLIST),
            "max_passes": int(manifest["healer_max_passes"]),
            "provenance": provenance,
            "final_status": post_outcome_label,
        }
        healer_results.append(healer_record)

        print(
            f"[{idx + 1}/320] {cell_id} baseline={mapped['final_status']} "
            f"layer={mapped['primary_failure_layer']} "
            f"healer={healer_decision}/{healer_outcome}"
        )

    # ---- Integer reproducibility check against existing revision ----
    integer_repro = {"checked": 0, "matched": 0, "mismatched": []}
    if INTEGER_BASELINE_PATH.exists():
        prior = {
            json.loads(line)["cell_id"]: json.loads(line)
            for line in INTEGER_BASELINE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        for row in cell_level_baseline:
            if row["family"] != "integer":
                continue
            integer_repro["checked"] += 1
            old = prior.get(row["cell_id"])
            if old is None:
                integer_repro["mismatched"].append({"cell_id": row["cell_id"], "reason": "missing_in_prior"})
                continue
            if old.get("final_status") != row["final_status"]:
                integer_repro["mismatched"].append(
                    {
                        "cell_id": row["cell_id"],
                        "prior": old.get("final_status"),
                        "current": row["final_status"],
                    }
                )
            else:
                integer_repro["matched"] += 1
    if integer_repro["checked"] != 80 or integer_repro["matched"] != 80 or integer_repro["mismatched"]:
        raise RuntimeError(f"Integer reproducibility failed: {integer_repro}")

    # ---- consistency checks ----
    assert len(cell_level_baseline) == 320
    assert len(healer_results) == 320
    assert baseline_passed + (total_count - baseline_passed) == 320
    assert post_healer_passed + (total_count - post_healer_passed) == 320
    assert sum(condition_stats[c]["total"] for c in CONDITION_DISPLAY) == 320
    assert sum(family_stats[f]["total"] for f in FAMILY_DISPLAY) == 320
    assert sum(seed_stats[str(s)]["total"] for s in manifest["seed_list"]) == 320
    for h in healer_results:
        if h["rescued"] and h["regressed"]:
            raise RuntimeError(f"rescued and regressed both true: {h['cell_id']}")
        if h["preserved_pass"] and h["rescued"]:
            raise RuntimeError(f"preserved_pass counted as rescued: {h['cell_id']}")

    # ---- paired condition differences ----
    def _pass_set(cond: str, stage: str) -> set[str]:
        out = set()
        for row, hrow in zip(cell_level_baseline, healer_results):
            if row["condition"] != cond:
                continue
            ok = row["final_status"] == "PASSED" if stage == "baseline" else hrow["final_status"] == "PASSED"
            if ok:
                out.add(f"{row['task_id']}__{row['seed']}")
        return out

    def _paired_diff(a: str, b: str, stage: str = "baseline") -> dict[str, Any]:
        # Pair by task_id + seed across conditions
        a_map = {}
        b_map = {}
        source = cell_level_baseline if stage == "baseline" else None
        for row, hrow in zip(cell_level_baseline, healer_results):
            key = f"{row['task_id']}__{row['seed']}"
            passed = row["final_status"] == "PASSED" if stage == "baseline" else hrow["final_status"] == "PASSED"
            if row["condition"] == a:
                a_map[key] = passed
            if row["condition"] == b:
                b_map[key] = passed
        keys = sorted(set(a_map) & set(b_map))
        a_pass = sum(1 for k in keys if a_map[k])
        b_pass = sum(1 for k in keys if b_map[k])
        delta_cells = sum(1 for k in keys if a_map[k] and not b_map[k]) - sum(
            1 for k in keys if b_map[k] and not a_map[k]
        )
        # signed: a - b
        family_delta: dict[str, dict[str, Any]] = {}
        for fam in FAMILY_DISPLAY:
            fkeys = [k for k in keys if family_map[k.split("__")[0]] == fam]
            fa = sum(1 for k in fkeys if a_map[k])
            fb = sum(1 for k in fkeys if b_map[k])
            family_delta[fam] = {
                "a_pass": fa,
                "b_pass": fb,
                "delta": fa - fb,
                "n": len(fkeys),
                "a_rate": fa / len(fkeys) if fkeys else 0.0,
                "b_rate": fb / len(fkeys) if fkeys else 0.0,
            }
        seed_delta: dict[str, dict[str, Any]] = {}
        for seed in manifest["seed_list"]:
            skeys = [k for k in keys if k.endswith(f"__{seed}")]
            sa = sum(1 for k in skeys if a_map[k])
            sb = sum(1 for k in skeys if b_map[k])
            seed_delta[str(seed)] = {
                "a_pass": sa,
                "b_pass": sb,
                "delta": sa - sb,
                "n": len(skeys),
            }
        _ = source
        return {
            "comparison": f"{CONDITION_DISPLAY[a]} - {CONDITION_DISPLAY[b]}",
            "condition_a": a,
            "condition_b": b,
            "stage": stage,
            "paired_n": len(keys),
            "a_pass": a_pass,
            "b_pass": b_pass,
            "a_pass_fraction": f"{a_pass}/{len(keys)}",
            "b_pass_fraction": f"{b_pass}/{len(keys)}",
            "a_rate_pct": round(100.0 * a_pass / len(keys), 2) if keys else 0.0,
            "b_rate_pct": round(100.0 * b_pass / len(keys), 2) if keys else 0.0,
            "delta_pass": a_pass - b_pass,
            "delta_rate_pct": round(100.0 * (a_pass - b_pass) / len(keys), 2) if keys else 0.0,
            "paired_net_cell_advantage_a_minus_b": delta_cells,
            "family_stratified": family_delta,
            "seed_consistency": seed_delta,
        }

    comparisons = {
        "Ab2g_minus_Ab1": _paired_diff("ab2g", "ab1"),
        "Ab2d_api_minus_Ab2g": _paired_diff("ab2d", "ab2g"),
        "Ab2d_spec_minus_Ab2g": _paired_diff("ab2d_spec", "ab2g"),
        "Ab2d_spec_minus_Ab2d_api": _paired_diff("ab2d_spec", "ab2d"),
        "post_healer_minus_baseline": {
            "comparison": "post-Healer - baseline",
            "baseline_pass": baseline_passed,
            "post_healer_pass": post_healer_passed,
            "baseline_fraction": f"{baseline_passed}/320",
            "post_healer_fraction": f"{post_healer_passed}/320",
            "delta_pass": post_healer_passed - baseline_passed,
            "delta_rate_pct": round(100.0 * (post_healer_passed - baseline_passed) / 320, 2),
            "rescued": healer_outcome_count["rescue_to_pass"],
            "regressed": healer_outcome_count["regression"],
            "family_stratified": {
                fam: {
                    "baseline_pass": family_stats[fam]["baseline_passed"],
                    "post_healer_pass": family_stats[fam]["post_healer_passed"],
                    "delta": family_stats[fam]["post_healer_passed"] - family_stats[fam]["baseline_passed"],
                    "n": family_stats[fam]["total"],
                }
                for fam in FAMILY_DISPLAY
            },
            "seed_consistency": {
                str(seed): {
                    "baseline_pass": seed_stats[str(seed)]["baseline_passed"],
                    "post_healer_pass": seed_stats[str(seed)]["post_healer_passed"],
                    "delta": seed_stats[str(seed)]["post_healer_passed"]
                    - seed_stats[str(seed)]["baseline_passed"],
                    "n": seed_stats[str(seed)]["total"],
                }
                for seed in manifest["seed_list"]
            },
        },
    }

    # ceiling / discrimination judgments
    family_judgments = {}
    for fam, label in FAMILY_DISPLAY.items():
        st = family_stats[fam]
        rates = {}
        for cond in CONDITION_DISPLAY:
            # family×condition = 20 cells (4 tasks × 5 seeds)
            n = 0
            p = 0
            for row in cell_level_baseline:
                if row["family"] == fam and row["condition"] == cond:
                    n += 1
                    if row["final_status"] == "PASSED":
                        p += 1
            rates[CONDITION_DISPLAY[cond]] = {"pass": p, "n": n, "rate_pct": round(100.0 * p / n, 2) if n else 0.0}
        rate_values = [v["rate_pct"] for v in rates.values()]
        ceiling = st["baseline_passed"] == st["total"]
        discrimination = max(rate_values) - min(rate_values) if rate_values else 0.0
        l2 = st["L2"]
        l3 = st["L3"]
        l4 = st["L4"]
        l5 = st["L5"]
        l2_l4_exposure = (l2 + l3 + l4) > 0
        healer_window = st["eligible"] > 0  # frozen allowlist actually matched
        pure_l5 = st["baseline_failed"] > 0 and l5 == st["baseline_failed"] and (l2 + l3 + l4 + st["L1"]) == 0
        family_judgments[fam] = {
            "family_display": label,
            "baseline_pass_fraction": f"{st['baseline_passed']}/{st['total']}",
            "ceiling_effect": ceiling,
            "condition_discrimination_pp": round(discrimination, 2),
            "still_discriminative": discrimination > 0 and not ceiling,
            "layer_counts": {k: st[k] for k in ("L0", "L1", "L2", "L3", "L4", "L5")},
            "l2_l4_layer_exposure": l2_l4_exposure,
            "healer_window_l2_l4": healer_window,
            "eligible": st["eligible"],
            "rescued": st["rescued"],
            "pure_l5_semantic_failures": pure_l5,
            "too_easy_to_discriminate": ceiling,
            "condition_rates": rates,
        }

    # ---- write outputs ----
    execution_manifest = dict(manifest)
    execution_manifest["executed_at_utc"] = datetime.now(timezone.utc).isoformat()
    execution_manifest["evaluator_hash"] = eval_hash
    execution_manifest["taxonomy_hash"] = taxonomy_hash
    execution_manifest["runtime_fingerprints"] = fingerprints
    execution_manifest["integer_reproducibility"] = integer_repro
    execution_manifest["llm_calls"] = 0
    execution_manifest["api_cost_usd"] = 0.0
    execution_manifest_file.write_text(
        json.dumps(execution_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    (output_dir / "evaluation_inventory.json").write_text(
        json.dumps(evaluation_inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with (output_dir / "cell_level_baseline.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for r in cell_level_baseline:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    with (output_dir / "healer_results.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for r in healer_results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    baseline_summary = {
        "evaluation_revision": manifest["evaluation_revision"],
        "evaluator_hash": eval_hash,
        "taxonomy_hash": taxonomy_hash,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total": total_count,
        "passed": baseline_passed,
        "failed": total_count - baseline_passed,
        "pass_fraction": f"{baseline_passed}/{total_count}",
        "pass_rate": baseline_passed / total_count if total_count else 0.0,
        "outcome_validity_distribution": validity_count,
        "failure_layer_distribution": layers_count,
        "mechanism_tags_distribution": dict(mechanism_counts),
        "exception_class_distribution": dict(exception_counts),
        "gate_stats": g_stats,
        "integer_reproducibility": integer_repro,
    }
    (output_dir / "baseline_summary.json").write_text(
        json.dumps(baseline_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    post_healer_summary = {
        "evaluation_revision": manifest["evaluation_revision"],
        "evaluator_hash": eval_hash,
        "taxonomy_hash": taxonomy_hash,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "total": total_count,
        "baseline_passed": baseline_passed,
        "final_passed": post_healer_passed,
        "baseline_pass_fraction": f"{baseline_passed}/{total_count}",
        "final_pass_fraction": f"{post_healer_passed}/{total_count}",
        "final_pass_rate": post_healer_passed / total_count if total_count else 0.0,
        "uplift_abs": post_healer_passed - baseline_passed,
        "uplift_pct": round(100.0 * (post_healer_passed - baseline_passed) / total_count, 4),
        "healer_eligibility_distribution": healer_eligibility_count,
        "healer_decision_distribution": healer_decision_count,
        "healer_outcome_distribution": healer_outcome_count,
        "eligible": healer_eligibility_count["eligible"],
        "transformed": healer_decision_count["transformed"],
        "rescued": healer_outcome_count["rescue_to_pass"],
        "regressed": healer_outcome_count["regression"],
        "abstained": healer_decision_count["abstained"],
        "preserved_pass": healer_outcome_count["preserved_pass"],
    }
    (output_dir / "post_healer_summary.json").write_text(
        json.dumps(post_healer_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    def _serialize_stats(stats: dict[str, dict[str, Any]]) -> dict[str, Any]:
        out = {}
        for k, v in stats.items():
            item = dict(v)
            item["baseline_pass_fraction"] = f"{v['baseline_passed']}/{v['total']}"
            item["post_healer_pass_fraction"] = f"{v['post_healer_passed']}/{v['total']}"
            item["baseline_pass_rate_pct"] = round(100.0 * v["baseline_passed"] / v["total"], 2) if v["total"] else 0.0
            item["post_healer_pass_rate_pct"] = (
                round(100.0 * v["post_healer_passed"] / v["total"], 2) if v["total"] else 0.0
            )
            out[k] = item
        return out

    condition_summary = {
        "display_map": CONDITION_DISPLAY,
        "stats": {
            CONDITION_DISPLAY[k]: _serialize_stats({k: condition_stats[k]})[k]
            for k in CONDITION_DISPLAY
        },
        "machine_stats": _serialize_stats(condition_stats),
    }
    (output_dir / "condition_summary.json").write_text(
        json.dumps(condition_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    family_summary = {
        "display_map": FAMILY_DISPLAY,
        "stats": {
            FAMILY_DISPLAY[k]: _serialize_stats({k: family_stats[k]})[k] for k in FAMILY_DISPLAY
        },
        "machine_stats": _serialize_stats(family_stats),
        "judgments": {
            FAMILY_DISPLAY[k]: family_judgments[k] for k in FAMILY_DISPLAY
        },
    }
    (output_dir / "family_summary.json").write_text(
        json.dumps(family_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # task summary with per-condition /5
    task_summary_out: dict[str, Any] = {}
    for tid in manifest["task_ids"]:
        st = task_stats[tid]
        per_cond = {}
        for cond, disp in CONDITION_DISPLAY.items():
            n = 0
            bp = 0
            pp = 0
            for row, hrow in zip(cell_level_baseline, healer_results):
                if row["task_id"] != tid or row["condition"] != cond:
                    continue
                n += 1
                if row["final_status"] == "PASSED":
                    bp += 1
                if hrow["final_status"] == "PASSED":
                    pp += 1
            per_cond[disp] = {
                "baseline_pass_fraction": f"{bp}/{n}",
                "post_healer_pass_fraction": f"{pp}/{n}",
                "baseline_passed": bp,
                "post_healer_passed": pp,
                "n": n,
            }
        task_summary_out[tid] = {
            **_serialize_stats({tid: st})[tid],
            "family": family_map[tid],
            "family_display": FAMILY_DISPLAY[family_map[tid]],
            "per_condition": per_cond,
            "layer_counts": {k: st[k] for k in ("L0", "L1", "L2", "L3", "L4", "L5")},
        }
    (output_dir / "task_summary.json").write_text(
        json.dumps(task_summary_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    seed_summary = _serialize_stats(seed_stats)
    (output_dir / "seed_summary.json").write_text(
        json.dumps(seed_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # nest condition_family_task with display names
    cft_out: dict[str, Any] = {}
    for cond, fams in condition_family_task.items():
        cft_out[CONDITION_DISPLAY[cond]] = {}
        for fam, tasks_map in fams.items():
            cft_out[CONDITION_DISPLAY[cond]][FAMILY_DISPLAY[fam]] = {}
            for tid, vals in tasks_map.items():
                cft_out[CONDITION_DISPLAY[cond]][FAMILY_DISPLAY[fam]][tid] = {
                    **vals,
                    "baseline_pass_fraction": f"{vals['baseline_passed']}/{vals['total']}",
                    "post_healer_pass_fraction": f"{vals['post_healer_passed']}/{vals['total']}",
                }
    condition_family_task_tables = {
        "tables": cft_out,
        "comparisons": comparisons,
    }
    (output_dir / "condition_family_task_tables.json").write_text(
        json.dumps(condition_family_task_tables, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    failure_taxonomy_summary = {
        "L0_L5": layers_count,
        "G1_G4": g_stats,
        "mechanism_tags": dict(mechanism_counts),
        "exception_class": dict(exception_counts),
        "outcome_validity": validity_count,
        "failure_chain_nonempty": sum(1 for r in cell_level_baseline if r["failure_chain"]),
        "pending_review": sum(1 for r in cell_level_baseline if r["classification_status"] == "PENDING_REVIEW"),
        "by_family_layers": {
            FAMILY_DISPLAY[f]: {k: family_stats[f][k] for k in ("L0", "L1", "L2", "L3", "L4", "L5")}
            for f in FAMILY_DISPLAY
        },
    }
    (output_dir / "failure_taxonomy_summary.json").write_text(
        json.dumps(failure_taxonomy_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ---- markdown report ----
    v3_passed = sum(1 for r in cell_level_baseline if r.get("v3_final_status") == "PASSED")
    flip_fail_to_pass = sum(
        1
        for r in cell_level_baseline
        if r.get("changed_by_evaluator_fix")
        and r.get("v3_final_status") != "PASSED"
        and r.get("v4_final_status") == "PASSED"
    )
    flip_pass_to_fail = sum(
        1
        for r in cell_level_baseline
        if r.get("changed_by_evaluator_fix")
        and r.get("v3_final_status") == "PASSED"
        and r.get("v4_final_status") != "PASSED"
    )
    gap_task_effect: dict[str, dict[str, int | str]] = {}
    for tid, gap in SCHEMA_GAP_BY_TASK.items():
        rows = [r for r in cell_level_baseline if r["task_id"] == tid]
        gap_task_effect[tid] = {
            "v3_pass": sum(1 for r in rows if r.get("v3_final_status") == "PASSED"),
            "v4_pass": sum(1 for r in rows if r.get("v4_final_status") == "PASSED"),
            "flips": sum(1 for r in rows if r.get("changed_by_evaluator_fix")),
            "n": len(rows),
            "gap": gap,
        }
    v3_v4_summary = {
        "v3_baseline_pass": f"{v3_passed}/320",
        "v4_baseline_pass": f"{baseline_passed}/320",
        "delta_pass": baseline_passed - v3_passed,
        "changed_by_evaluator_fix": schema_flip_count,
        "fail_to_pass": flip_fail_to_pass,
        "pass_to_fail": flip_pass_to_fail,
        "flips_by_gap": schema_flip_by_gap,
        "gap_task_effect": gap_task_effect,
        "oracle_source_sha256": oracle_hash,
        "audit_reference": ORACLE_SCHEMA_AUDIT_V1,
        "confound_note": (
            "GAP_CONFIRMED packaging/type false negatives addressed; "
            "GAP_SUSPECTED latex coupling relaxed to structural judge "
            "(latex recorded as presentation). Condition deltas should no longer "
            "be confounded by the confirmed schema gaps; residual L3 API-misuse "
            "and true L5 errors remain."
        ),
    }
    (output_dir / "v3_v4_comparison_summary.json").write_text(
        json.dumps(v3_v4_summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    report_path = output_dir / "math16_pilot02_full_v4_report.md"
    md: list[str] = [
        "# Math16 Pilot-02 Full Evaluation Revision v4_r001 Report (post schema-normalize re-score)",
        "",
        "Offline blinded baseline + Taxonomy v3 + frozen deterministic Healer for the complete Math16 320-cell inventory.",
        "",
        "## 1. Metadata",
        f"- **Evaluation ID**: `{manifest['evaluation_id']}`",
        f"- **Revision**: `{manifest['evaluation_revision']}`",
        f"- **Taxonomy SHA-256**: `{taxonomy_hash}`",
        f"- **Evaluator SHA-256**: `{eval_hash}`",
        f"- **Source Commit**: `{manifest['source_commit']}`",
        f"- **LLM calls**: `0`",
        f"- **API cost**: `$0.00`",
        f"- **Integer reproducibility**: `{integer_repro['matched']}/80 matched`",
        "",
        "## 2. Overall",
        f"- Baseline pass: `{baseline_passed}/320` ({100.0 * baseline_passed / 320:.2f}%)",
        f"- Post-Healer pass: `{post_healer_passed}/320` ({100.0 * post_healer_passed / 320:.2f}%)",
        f"- Baseline fail: `{320 - baseline_passed}/320`",
        f"- Eligible: `{healer_eligibility_count['eligible']}`",
        f"- Transformed: `{healer_decision_count['transformed']}`",
        f"- Rescued: `{healer_outcome_count['rescue_to_pass']}`",
        f"- Regressed: `{healer_outcome_count['regression']}`",
        f"- Abstained: `{healer_decision_count['abstained']}`",
        f"- Preserved pass: `{healer_outcome_count['preserved_pass']}`",
        "",
        "## 3. By condition (display names; machine id `ab2d` = Ab2d+api)",
        "| Condition | Baseline pass | Post-Healer pass | Eligible | Rescued | Regressed |",
        "| :--- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for cond, disp in CONDITION_DISPLAY.items():
        st = condition_stats[cond]
        md.append(
            f"| **{disp}** | {st['baseline_passed']}/80 | {st['post_healer_passed']}/80 | "
            f"{st['eligible']} | {st['rescued']} | {st['regressed']} |"
        )

    md.extend(
        [
            "",
            "> Ab2d+api 與 Ab2d+spec 為完整介入策略比較，不是單純 API 有無的因果估計。",
            "",
            "## 4. By family",
            "| Family | Baseline pass | Post-Healer pass | L2 | L3 | L4 | L5 | Ceiling | Discriminative | L2–L4 exposure | Frozen Healer window |",
            "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :---: | :---: | :---: |",
        ]
    )
    for fam, disp in FAMILY_DISPLAY.items():
        st = family_stats[fam]
        j = family_judgments[fam]
        md.append(
            f"| **{disp}** | {st['baseline_passed']}/80 | {st['post_healer_passed']}/80 | "
            f"{st['L2']} | {st['L3']} | {st['L4']} | {st['L5']} | "
            f"{'Y' if j['ceiling_effect'] else 'N'} | "
            f"{'Y' if j['still_discriminative'] else 'N'} | "
            f"{'Y' if j['l2_l4_layer_exposure'] else 'N'} | "
            f"{'Y' if j['healer_window_l2_l4'] else 'N'} |"
        )

    md.extend(
        [
            "",
            "## 5. By task (20 cells = 4 conditions × 5 seeds)",
            "| Task | Family | Baseline | Post-Healer | Ab1 | Ab2g | Ab2d+api | Ab2d+spec | Eligible | Rescued |",
            "| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for tid in manifest["task_ids"]:
        ts = task_summary_out[tid]
        pc = ts["per_condition"]
        md.append(
            f"| `{tid}` | {ts['family_display']} | {ts['baseline_pass_fraction']} | "
            f"{ts['post_healer_pass_fraction']} | "
            f"{pc['Ab1']['baseline_pass_fraction']} | {pc['Ab2g']['baseline_pass_fraction']} | "
            f"{pc['Ab2d+api']['baseline_pass_fraction']} | {pc['Ab2d+spec']['baseline_pass_fraction']} | "
            f"{ts['eligible']} | {ts['rescued']} |"
        )

    md.extend(
        [
            "",
            "## 6. By seed",
            "| Seed | Baseline pass | Post-Healer pass | Eligible | Rescued |",
            "| :--- | ---: | ---: | ---: | ---: |",
        ]
    )
    for seed in manifest["seed_list"]:
        st = seed_stats[str(seed)]
        md.append(
            f"| `{seed}` | {st['baseline_passed']}/64 | {st['post_healer_passed']}/64 | "
            f"{st['eligible']} | {st['rescued']} |"
        )

    md.extend(
        [
            "",
            "## 7. G1–G4",
            f"- G1 FAIL: `{g_stats['G1_FAIL']}` / PASS: `{g_stats['G1_PASS']}`",
            f"- G2 FAIL: `{g_stats['G2_FAIL']}` / PASS: `{g_stats['G2_PASS']}`",
            f"- G3 FAIL: `{g_stats['G3_FAIL']}` / PASS: `{g_stats['G3_PASS']}`",
            f"- G4 FAIL: `{g_stats['G4_FAIL']}` / PASS: `{g_stats['G4_PASS']}`",
            "",
            "## 8. L0–L5 (baseline failures only)",
            f"- L0: `{layers_count['L0']}`",
            f"- L1: `{layers_count['L1']}`",
            f"- L2: `{layers_count['L2']}`",
            f"- L3: `{layers_count['L3']}`",
            f"- L4: `{layers_count['L4']}`",
            f"- L5: `{layers_count['L5']}`",
            "",
            "## 9. Formal condition differences (paired by task×seed)",
        ]
    )
    for key, comp in comparisons.items():
        if key == "post_healer_minus_baseline":
            md.append(
                f"- **post-Healer − baseline**: `{comp['delta_pass']}` "
                f"({comp['post_healer_fraction']} − {comp['baseline_fraction']}; "
                f"{comp['delta_rate_pct']} pp)"
            )
        else:
            md.append(
                f"- **{comp['comparison']}**: `{comp['delta_pass']}` "
                f"({comp['a_pass_fraction']} − {comp['b_pass_fraction']}; "
                f"{comp['delta_rate_pct']} pp)"
            )

    md.extend(
        [
            "",
            "## 10. Ceiling / discrimination / Healer window",
        ]
    )
    for fam, disp in FAMILY_DISPLAY.items():
        j = family_judgments[fam]
        md.append(
            f"- **{disp}**: ceiling={j['ceiling_effect']}, "
            f"discriminative={j['still_discriminative']} "
            f"(spread {j['condition_discrimination_pp']} pp), "
            f"L2–L4 exposure={j['l2_l4_layer_exposure']}, "
            f"frozen_healer_window={j['healer_window_l2_l4']}, "
            f"pure_L5={j['pure_l5_semantic_failures']}"
        )

    md.extend(
        [
            "",
            "## 11. v3 → v4 comparison (evaluator schema normalize)",
            f"- v3 baseline pass: `{v3_passed}/320`",
            f"- v4 baseline pass: `{baseline_passed}/320`",
            f"- delta: `{baseline_passed - v3_passed}` "
            f"(fail→pass `{flip_fail_to_pass}`, pass→fail `{flip_pass_to_fail}`)",
            f"- cells with `changed_by_evaluator_fix=true`: `{schema_flip_count}`",
            f"- oracle SHA-256: `{oracle_hash}`",
            f"- audit reference: `{ORACLE_SCHEMA_AUDIT_V1}` (**immutable V1; not modified**)",
            "",
            "### GAP task effects (pass /20)",
            "| Task | Gap | v3 | v4 | flips | V1 corrected estimate |",
            "| :--- | :--- | ---: | ---: | ---: | :--- |",
        ]
    )
    v1_estimates = {
        "ce111_q02_polynomial_division_remainder": "18/20",
        "ce111_q08_polynomial_factor_parameter_recovery": "16/20",
        "ce115_calc_polynomial_factor_roots_l1": "20/20",
        "ce111_q10_ordered_quadratic_roots_radical": "20/20",
        "ce112_q04_radical_simplification": "20/20 (no L5 hit)",
        "ce115_calc_radical_simplification_l1": "20/20 (no L5 hit)",
        "ce111_q05_exact_fraction_expression": "n/a (L3 dominant)",
        "ce112_q12_independent_probability_fraction": "n/a (L3 dominant)",
        "ce113_q01_negative_fraction_subtraction": "n/a (L3 dominant)",
        "ce115_calc_exact_rational_expression_l1": "20/20 (no L5 hit)",
    }
    for tid in SCHEMA_GAP_BY_TASK:
        eff = gap_task_effect[tid]
        md.append(
            f"| `{tid}` | `{eff['gap']}` | {eff['v3_pass']}/20 | {eff['v4_pass']}/20 | "
            f"{eff['flips']} | {v1_estimates.get(tid, '—')} |"
        )
    md.extend(
        [
            "",
            "### Confound status",
            "- GAP_CONFIRMED packaging/type false negatives are addressed in this revision.",
            "- GAP_SUSPECTED latex coupling was relaxed to structural judge "
            "(latex kept as presentation / `latex_ok`); this completes the incomplete "
            "`math16_latex_semantic_v2` rollout recorded in V1.",
            "- Condition-level deltas in §9 should no longer be confounded by the four "
            "confirmed schema gaps.",
            "- Residual risks: Ab2d+spec L3 Domain-API misuse remains a separate confound; "
            "true mathematical L5 errors remain.",
            "",
            "## 12. Integrity",
            f"- Inventory unique cells: `320`",
            f"- Raw/prompt/fingerprint verified in preflight",
            f"- Integer prior revision match: `80/80`",
            f"- Healer allowlist frozen: `{', '.join(RULE_ALLOWLIST)}`",
            f"- v3 artifacts left intact under `math16_pilot02_full_evaluation_v3_r001/`",
            "",
            "## 13. Method notes",
            "- No Gemini or other LLM calls during evaluation (`LLM calls=0`, `$0.00`).",
            "- Display label `Ab2d+api` maps from machine condition `ab2d` without rewriting raw identity.",
            "- Unknown classifier outcomes are `PENDING_REVIEW`, never auto-mapped to L5.",
            "- Frozen Healer runs only on `healer_eligible=true` cells; ambiguous entry-points abstain.",
            "- Re-score uses existing raw_response only; frozen prompts/contracts/answers unchanged.",
            "",
            "ORACLE_SCHEMA_FIX_APPLIED",
            "EVALUATION_V4_RESCORED_ZERO_MODEL_CALLS",
            "MATH16_320_BLINDED_V4_RESCORE_COMPLETE",
            "FROZEN_HEALER_EVALUATION_COMPLETE",
            "V3_V4_COMPARISON_READY",
            "",
        ]
    )
    report_path.write_text("\n".join(md), encoding="utf-8")
    print(f"Report written: {report_path}")
    print(f"v3→v4 delta pass: {baseline_passed - v3_passed} (flips={schema_flip_count})")
    print("ORACLE_SCHEMA_FIX_APPLIED")
    print("EVALUATION_V4_RESCORED_ZERO_MODEL_CALLS")
    print("MATH16_320_BLINDED_V4_RESCORE_COMPLETE")
    print("FROZEN_HEALER_EVALUATION_COMPLETE")
    print("V3_V4_COMPARISON_READY")


def main() -> int:
    parser = argparse.ArgumentParser(description="Math16 Pilot-02 full 320-cell evaluation v4")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--preflight-only", action="store_true")
    group.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    try:
        if not EVAL_MANIFEST_PATH.exists():
            raise FileNotFoundError(f"Missing evaluation manifest: {EVAL_MANIFEST_PATH}")
        manifest = json.loads(EVAL_MANIFEST_PATH.read_text(encoding="utf-8"))
        do_preflight_checks(manifest)
        if args.preflight_only:
            return 0
        run_evaluation(manifest)
        return 0
    except Exception:
        import traceback

        traceback.print_exc()
        print("MATH16_320_EVALUATION_INCOMPLETE")
        print("ANALYSIS_BLOCKED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
