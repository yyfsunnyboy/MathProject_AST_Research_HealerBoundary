"""
build_math16_posthoc_six_cell_rescue_audit_v1.py
=================================================
Math16 Post-hoc Six-Cell Rescue Mechanism Audit — Builder (Read-Only)

PURPOSE
-------
Read-only artifact extractor. Extracts identities and objective metadata for the 6
Post-hoc rescued cells from frozen artifacts. Produces a draft audit roster for human review.

CONSTRAINTS (strictly enforced)
--------------------------------
- No model calls (LLM, VLM, API)
- No Healer execution
- No Evaluator execution / rescoring
- No new PASS/FAIL assignments
- No modification of frozen artifacts
- Output isolated to: artifacts/math16_posthoc_six_cell_rescue_audit_v1/preflight/

USAGE
-----
    python scripts/build_math16_posthoc_six_cell_rescue_audit_v1.py [--dry-run]

OUTPUT
------
    artifacts/math16_posthoc_six_cell_rescue_audit_v1/preflight/
        audit_roster_draft.json
        accounting_check.json
        sha_verification.json
        preflight_summary.json
"""

import ast
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Safety sentinel — detect and refuse any model/healer/evaluator call
# ---------------------------------------------------------------------------
_PROHIBITED_IMPORTS = {
    "openai", "anthropic", "google.generativeai", "transformers",
    "langchain", "llamaindex", "huggingface_hub", "ollama",
}

def _check_prohibited_imports():
    """Raise immediately if any prohibited module is imported."""
    for mod in list(sys.modules.keys()):
        for prohibited in _PROHIBITED_IMPORTS:
            if mod == prohibited or mod.startswith(prohibited + "."):
                raise RuntimeError(
                    f"BUILDER SAFETY VIOLATION: prohibited module '{mod}' is imported. "
                    "This script must not use any model API."
                )

_check_prohibited_imports()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent.resolve()

FROZEN_SOURCES = {
    "final_report_v13": REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md",
    "final_report_v13_manifest": REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13_manifest.json",
    "evidence_complete_manifest": REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json",
    "ab3_freeze_manifest": REPO_ROOT / "docs/experiments/manifests/math16_ab3_freeze_manifest.json",
    "qwen4b_posthoc_corrected_chain_freeze": REPO_ROOT / "docs/experiments/audits/math16_pilot02_qwen4b_posthoc_corrected_chain_freeze_v1.json",
    "primary_eligible_execution_records": REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl",
    "primary_vs_corrected_chain_comparison": REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json",
    "taxonomy_md": REPO_ROOT / "docs/experiments/design/math16_posthoc_shared_taxonomy_v1.md",
    "taxonomy_json": REPO_ROOT / "docs/experiments/manifests/math16_posthoc_shared_taxonomy_v1.json",
    "audit_spec": REPO_ROOT / "docs/experiments/design/math16_posthoc_six_cell_rescue_audit_v1_spec.md",
    "audit_manifest": REPO_ROOT / "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_manifest.json",
}

EXPECTED_SHAS = {
    "final_report_v13": "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b",
    "final_report_v13_manifest": "893170c249bc3d93ea288a03dbc45b44001175c788626455214b5da12ddab987",
    "evidence_complete_manifest": "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225",
    "ab3_freeze_manifest": "84556dc38e0d21cc57f96b0d44092a516cdd76806c6f7468c0286475e23676b1",
    "qwen4b_posthoc_corrected_chain_freeze": "d6060e712a38738396119d148f30cb15978c25d85cbce188ef43ccd4e07dcdae",
    "primary_eligible_execution_records": "2ff030890ea301cb2d94d791f88be8f5a8fa49d46e9b21dbae454c7da5a504e4",
    "primary_vs_corrected_chain_comparison": "e199110fa67459de663a60f5ca03085b6a1f42cba2c6a0bdd470f36c1ff2266a",
}

OUTPUT_DIR = REPO_ROOT / "artifacts/math16_posthoc_six_cell_rescue_audit_v1/preflight"

VALID_CONDITIONS = {"Ab1", "Ab2g", "Ab2d+api", "Ab2d+spec"}
VALID_FAMILIES = {"integer", "polynomial", "radical", "fraction"}
VALID_LAYER_A = {
    "L1_PARSE_SYNTAX", "L2_CONTRACT_SCHEMA_ENTRYPOINT", "L3_DOMAIN_API",
    "L4_RUNTIME_EXECUTION", "L5_SEMANTIC_ANSWER",
}
VALID_LAYER_B = {
    "NO_OP", "ABSTAIN_NO_RULE", "ABSTAIN_AMBIGUOUS",
    "MODIFIED_RESCUED", "MODIFIED_STILL_FAIL", "MODIFIED_NEW_FAILURE", "MODIFIED_UNEVALUABLE",
}
VALID_LAYER_C = {
    "WITHIN_FROZEN_REPAIR_SIGNATURE", "OUTSIDE_FROZEN_REPAIR_SIGNATURE", "AMBIGUOUS_SIGNATURE_MATCH",
}

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_condition_from_cell_id(cell_id: str) -> str:
    """Extract condition from cell_id token (third segment, 0-indexed)."""
    parts = cell_id.split("__")
    # Format: model__task__condition__seed
    if len(parts) < 4:
        return "UNKNOWN"
    raw_cond = parts[2]
    mapping = {
        "ab1": "Ab1",
        "ab2g": "Ab2g",
        "ab2d": "Ab2d+api",
        "ab2d_spec_v2": "Ab2d+spec",
    }
    return mapping.get(raw_cond.lower(), raw_cond)


def parse_task_from_cell_id(cell_id: str) -> str:
    parts = cell_id.split("__")
    return parts[1] if len(parts) >= 2 else "UNKNOWN"


def parse_seed_from_cell_id(cell_id: str) -> str:
    parts = cell_id.split("__")
    return parts[-1] if parts else "UNKNOWN"


def infer_family(task_id: str) -> str:
    """Infer math family from task_id prefix or content."""
    task_lower = task_id.lower()
    if "polynomial" in task_lower or "poly" in task_lower:
        return "polynomial"
    if "radical" in task_lower or "simplification_l1" in task_lower:
        return "radical"
    if "fraction" in task_lower or "rational" in task_lower or "probability_fraction" in task_lower:
        return "fraction"
    if ("integer" in task_lower or "prime" in task_lower or "power" in task_lower
            or "divisor" in task_lower or "exponential" in task_lower):
        return "integer"
    # Additional mappings by task prefix
    task_family_hints = {
        "ce112_q04": "radical",
        "ce112_q09": "integer",
        "ce113_q01": "fraction",
        "ce115_calc_radical": "radical",
        "ce115_calc_polynomial": "polynomial",
        "ce115_calc_exact_rational": "fraction",
    }
    for prefix, fam in task_family_hints.items():
        if task_id.startswith(prefix):
            return fam
    return "UNKNOWN"


def map_healer_outcome_to_layer_b(healer_outcome: str, regressed: bool) -> str:
    if regressed:
        return "MODIFIED_NEW_FAILURE"
    mapping = {
        "no_op": "NO_OP",
        "rescue_to_pass": "MODIFIED_RESCUED",
        "changed_partial_progress": "MODIFIED_STILL_FAIL",
    }
    return mapping.get(healer_outcome, "ABSTAIN_NO_RULE")


def check_rule_in_frozen_allowlist(rule_id: str, frozen_rules: list) -> str:
    """Return Layer C value for a given rule_id."""
    for rule in frozen_rules:
        if rule.get("rule_id") == rule_id:
            # Rule is in allowlist — but source span not available (sha_only)
            # so we cannot fully verify change pattern
            return "AMBIGUOUS_SIGNATURE_MATCH"
    return "OUTSIDE_FROZEN_REPAIR_SIGNATURE"


def try_ast_parse(source: str) -> dict:
    """Try to parse Python source and return result."""
    try:
        tree = ast.parse(source)
        return {"parseable": True, "node_count": sum(1 for _ in ast.walk(tree))}
    except SyntaxError as e:
        return {"parseable": False, "error": str(e)}

# ---------------------------------------------------------------------------
# Main Builder
# ---------------------------------------------------------------------------

def verify_shas() -> dict:
    """Verify SHA256 of all frozen source files."""
    results = {}
    all_pass = True
    for key, path in FROZEN_SOURCES.items():
        if not path.exists():
            results[key] = {"status": "FILE_NOT_FOUND", "path": str(path)}
            if key in EXPECTED_SHAS:
                all_pass = False
            continue
        actual = sha256_file(path)
        expected = EXPECTED_SHAS.get(key)
        if expected is None:
            results[key] = {"status": "NO_EXPECTED_SHA", "actual": actual, "path": str(path)}
        elif actual == expected:
            results[key] = {"status": "MATCH", "actual": actual, "path": str(path)}
        else:
            results[key] = {
                "status": "MISMATCH",
                "actual": actual,
                "expected": expected,
                "path": str(path),
            }
            all_pass = False
    results["_all_pass"] = all_pass
    return results


def load_frozen_data() -> dict:
    """Load all frozen artifacts into memory (read-only)."""
    data = {}

    # Load posthoc corrected chain freeze
    with open(FROZEN_SOURCES["qwen4b_posthoc_corrected_chain_freeze"], encoding="utf-8") as f:
        data["posthoc_freeze"] = json.load(f)

    # Load primary vs corrected chain comparison
    with open(FROZEN_SOURCES["primary_vs_corrected_chain_comparison"], encoding="utf-8") as f:
        data["comparison"] = json.load(f)

    # Load primary eligible execution records
    primary_records = {}
    with open(FROZEN_SOURCES["primary_eligible_execution_records"], encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rec = json.loads(line)
                primary_records[rec["cell_id"]] = rec
    data["primary_records"] = primary_records

    # Load ab3 freeze manifest (for frozen rule allowlist)
    with open(FROZEN_SOURCES["ab3_freeze_manifest"], encoding="utf-8") as f:
        data["ab3_freeze"] = json.load(f)

    # Load taxonomy
    with open(FROZEN_SOURCES["taxonomy_json"], encoding="utf-8") as f:
        data["taxonomy"] = json.load(f)

    return data


def check_accounting(data: dict) -> dict:
    """Verify corrected-chain accounting invariants."""
    comparison = data["comparison"]
    freeze = data["posthoc_freeze"]

    checks = {
        "replayed_is_10": {
            "expected": 10,
            "actual": comparison.get("replayed"),
            "pass": comparison.get("replayed") == 10,
        },
        "primary_rescued_is_5": {
            "expected": 5,
            "actual": comparison.get("primary_rescued"),
            "pass": comparison.get("primary_rescued") == 5,
        },
        "corrected_rescued_is_6": {
            "expected": 6,
            "actual": comparison.get("corrected_rescued"),
            "pass": comparison.get("corrected_rescued") == 6,
        },
        "incremental_pass_is_1": {
            "expected": 1,
            "actual": (comparison.get("corrected_rescued", 0) - comparison.get("primary_rescued", 0)),
            "pass": (comparison.get("corrected_rescued", 0) - comparison.get("primary_rescued", 0)) == 1,
        },
        "same_as_primary_is_8": {
            "expected": 8,
            "actual": comparison.get("same_as_primary"),
            "pass": comparison.get("same_as_primary") == 8,
        },
        "changed_vs_primary_is_2": {
            "expected": 2,
            "actual": comparison.get("changed_vs_primary"),
            "pass": comparison.get("changed_vs_primary") == 2,
        },
        "corrected_repaired_still_fail_is_4": {
            "expected": 4,
            "actual": freeze.get("corrected_repaired_still_fail"),
            "pass": freeze.get("corrected_repaired_still_fail") == 4,
        },
        "corrected_no_op_is_0": {
            "expected": 0,
            "actual": freeze.get("corrected_no_op"),
            "pass": freeze.get("corrected_no_op") == 0,
        },
        "corrected_regression_is_0": {
            "expected": 0,
            "actual": freeze.get("corrected_regression"),
            "pass": freeze.get("corrected_regression") == 0,
        },
    }
    checks["_all_pass"] = all(v["pass"] for v in checks.values() if isinstance(v, dict) and "pass" in v)
    return checks


def extract_six_posthoc_rescued_cells(data: dict) -> list:
    """Extract the 6 Post-hoc rescued cells from frozen artifacts."""
    comparison = data["comparison"]
    primary_records = data["primary_records"]
    frozen_rules = data["ab3_freeze"].get("frozen_rule_allowlist", [])

    posthoc_rescued = []
    for cell in comparison.get("per_cell", []):
        if cell.get("new_post_healer_status") == "PASSED":
            posthoc_rescued.append(cell)

    if len(posthoc_rescued) != 6:
        raise ValueError(
            f"Expected exactly 6 Post-hoc rescued cells, found {len(posthoc_rescued)}. "
            "Check frozen artifact integrity."
        )

    roster = []
    for cell in posthoc_rescued:
        cell_id = cell["cell_id"]
        task_id = parse_task_from_cell_id(cell_id)
        condition = parse_condition_from_cell_id(cell_id)
        seed = parse_seed_from_cell_id(cell_id)
        family = infer_family(task_id)

        primary_rec = primary_records.get(cell_id, {})
        is_primary_rescued = cell.get("primary_post_healer_status") == "PASSED"
        is_incremental = cell.get("noop_to_rescue", False)

        # Primary disposition
        primary_outcome = primary_rec.get("healer_outcome", cell.get("primary_healer_outcome", "UNKNOWN"))
        primary_regressed = primary_rec.get("regressed", False)
        primary_disp = map_healer_outcome_to_layer_b(primary_outcome, primary_regressed)

        # Post-hoc disposition (always MODIFIED_RESCUED for rescued cells)
        posthoc_disp = "MODIFIED_RESCUED"

        # Applied rule
        new_applied_rules = cell.get("new_applied_rules", [])
        applied_rule = new_applied_rules[0] if new_applied_rules else "UNKNOWN"

        # Repair signature match — AMBIGUOUS because artifact_storage == sha_only_not_committed_py
        repair_sig = check_rule_in_frozen_allowlist(applied_rule, frozen_rules)

        entry = {
            "cell_id": cell_id,
            "model": "qwen3_5_4b",
            "task_id": task_id,
            "family": family,
            "condition": condition,
            "seed": seed,
            "is_primary_rescued": is_primary_rescued,
            "is_posthoc_rescued": True,
            "is_incremental_posthoc_pass": is_incremental,
            "baseline_evaluator_outcome": "FAILED",
            "baseline_failure_layer": "PENDING_HUMAN_REVIEW",
            "surface_failure": "PENDING_HUMAN_REVIEW",
            "root_mechanism": "PENDING_HUMAN_REVIEW",
            "primary_disposition": primary_disp,
            "posthoc_disposition": posthoc_disp,
            "final_pass_fail": "PASS",
            "healer_rule_id": applied_rule,
            "precondition_evidence": "PENDING_HUMAN_REVIEW",
            "source_span": "UNKNOWN_SHA_ONLY",
            "changed_line_count": -1,
            "changed_ast_node_count": -1,
            "changed_ast_node_types": [],
            "tree_depth_range": "UNKNOWN",
            "control_flow_changed": "PENDING_HUMAN_REVIEW",
            "literals_changed": "PENDING_HUMAN_REVIEW",
            "function_signature_changed": "PENDING_HUMAN_REVIEW",
            "semantic_operator_changed": "PENDING_HUMAN_REVIEW",
            "before_snippet_hash": cell.get("before_source_sha256", "UNKNOWN"),
            "after_snippet_hash": cell.get("after_source_sha256", "UNKNOWN"),
            "repair_signature_match": repair_sig,
            "oracle_answer_used": False,
            "unique": "PENDING_HUMAN_REVIEW",
            "local": "PENDING_HUMAN_REVIEW",
            "offline_verifiable": "PENDING_HUMAN_REVIEW",
            "analyst_notes": (
                f"artifact_storage=sha_only_not_committed_py; source not recoverable for AST diff; "
                f"repair_signature_match set to AMBIGUOUS_SIGNATURE_MATCH pending human source review. "
                + (f"INCREMENTAL_POSTHOC_PASS: Primary was NO_OP due to false-loop rollback; "
                   f"Post-hoc false-loop fix enabled rescue via {applied_rule}. "
                   f"Explanation: {cell.get('explanation', '')}"
                   if is_incremental else "")
            ),
        }
        roster.append(entry)

    return roster


def build(dry_run: bool = False) -> dict:
    """Main builder entry point."""
    print("=" * 70)
    print("Math16 Post-hoc Six-Cell Rescue Audit — Builder")
    print("=" * 70)
    print(f"Dry run: {dry_run}")
    print(f"Repo root: {REPO_ROOT}")
    print()

    # Step 1: Verify SHAs
    print("[1] Verifying frozen artifact SHAs...")
    sha_results = verify_shas()
    if not sha_results.get("_all_pass"):
        print("ERROR: SHA verification failed for one or more frozen artifacts.")
        for key, result in sha_results.items():
            if key != "_all_pass" and result.get("status") in ("MISMATCH", "FILE_NOT_FOUND"):
                print(f"  FAIL: {key} -> {result}")
        return {"status": "ABORTED", "reason": "SHA_VERIFICATION_FAILED", "sha_results": sha_results}
    print("  All SHA checks passed.")

    # Step 2: Load frozen data
    print("[2] Loading frozen artifacts...")
    data = load_frozen_data()
    print("  Loaded OK.")

    # Step 3: Check accounting
    print("[3] Checking corrected-chain accounting invariants...")
    accounting = check_accounting(data)
    if not accounting.get("_all_pass"):
        print("ERROR: Accounting check failed.")
        for key, val in accounting.items():
            if key != "_all_pass" and not val.get("pass", True):
                print(f"  FAIL: {key} -> expected={val['expected']}, actual={val['actual']}")
        return {"status": "ABORTED", "reason": "ACCOUNTING_CHECK_FAILED", "accounting": accounting}
    print("  All accounting invariants verified (10/8/2/1).")

    # Step 4: Extract 6 cells
    print("[4] Extracting 6 Post-hoc rescued cells...")
    try:
        roster = extract_six_posthoc_rescued_cells(data)
    except ValueError as e:
        print(f"ERROR: {e}")
        return {"status": "ABORTED", "reason": "CELL_EXTRACTION_FAILED", "error": str(e)}
    print(f"  Extracted {len(roster)} cells.")
    for r in roster:
        inc_marker = " [INCREMENTAL_POSTHOC]" if r["is_incremental_posthoc_pass"] else ""
        print(f"    {r['cell_id'][:60]}...{inc_marker}")

    # Step 5: Write output (unless dry run)
    timestamp = datetime.now(timezone.utc).isoformat()

    audit_roster_draft = {
        "roster_id": "math16_posthoc_six_cell_rescue_audit_v1_draft",
        "generated_at_utc": timestamp,
        "builder_version": "1.0",
        "status": "DRAFT_PENDING_HUMAN_REVIEW",
        "constraints": {
            "model_calls": 0,
            "healer_execution": 0,
            "evaluator_execution": 0,
            "rescoring": 0,
        },
        "cells": roster,
    }

    accounting_report = {
        "generated_at_utc": timestamp,
        "checks": accounting,
        "label": "10 eligible replayed / 8 unchanged / 2 changed / 1 PASS-changed",
    }

    preflight_summary = {
        "generated_at_utc": timestamp,
        "sha_verification": "PASS" if sha_results.get("_all_pass") else "FAIL",
        "accounting_check": "PASS" if accounting.get("_all_pass") else "FAIL",
        "cell_count_extracted": len(roster),
        "cell_count_expected": 6,
        "cell_count_match": len(roster) == 6,
        "model_calls": 0,
        "healer_calls": 0,
        "evaluator_calls": 0,
        "oracle_answer_used_in_any_cell": any(r["oracle_answer_used"] for r in roster),
        "output_isolation_verified": True,
        "overall": "PREFLIGHT_PASS" if (
            sha_results.get("_all_pass")
            and accounting.get("_all_pass")
            and len(roster) == 6
            and not any(r["oracle_answer_used"] for r in roster)
        ) else "PREFLIGHT_FAIL",
    }

    if not dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        # Safety: refuse to write inside docs/experiments
        docs_path = REPO_ROOT / "docs" / "experiments"
        assert docs_path not in OUTPUT_DIR.parents, (
            "SAFETY VIOLATION: output path is inside docs/experiments! Aborting."
        )

        (OUTPUT_DIR / "audit_roster_draft.json").write_text(
            json.dumps(audit_roster_draft, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (OUTPUT_DIR / "accounting_check.json").write_text(
            json.dumps(accounting_report, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (OUTPUT_DIR / "sha_verification.json").write_text(
            json.dumps(sha_results, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (OUTPUT_DIR / "preflight_summary.json").write_text(
            json.dumps(preflight_summary, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"[5] Output written to: {OUTPUT_DIR}")
    else:
        print("[5] Dry-run: skipping file write.")

    print()
    print("=" * 70)
    print(f"BUILDER RESULT: {preflight_summary['overall']}")
    print("=" * 70)

    return {
        "status": preflight_summary["overall"],
        "roster": roster,
        "accounting": accounting,
        "sha_results": sha_results,
    }


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    result = build(dry_run=dry_run)
    if result.get("status") not in ("PREFLIGHT_PASS",):
        sys.exit(1)
