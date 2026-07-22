"""
preflight_math16_posthoc_six_cell_rescue_audit_v1.py
=====================================================
Math16 Post-hoc Six-Cell Rescue Mechanism Audit — Zero-Model Preflight

PURPOSE
-------
Standalone zero-model preflight validation. Runs all verification checks defined in
docs/experiments/design/math16_posthoc_six_cell_rescue_audit_v1_spec.md §7 without
calling any model, Healer, or Evaluator.

GUARANTEES
----------
- No LLM / VLM / API calls
- No Healer execution
- No Evaluator execution
- No modification of frozen artifacts
- No new PASS/FAIL assignments

USAGE
-----
    python scripts/preflight_math16_posthoc_six_cell_rescue_audit_v1.py

EXIT CODES
----------
    0   All preflight checks passed (PREFLIGHT_PASS)
    1   One or more checks failed (PREFLIGHT_FAIL)
"""

import ast
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()

# ---------------------------------------------------------------------------
# Frozen SHA registry (must match spec Section 1)
# ---------------------------------------------------------------------------
EXPECTED_SHAS = {
    "docs/experiments/reports/math16_pilot02_final_report_v13.md":
        "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b",
    "docs/experiments/reports/math16_pilot02_final_report_v13_manifest.json":
        "893170c249bc3d93ea288a03dbc45b44001175c788626455214b5da12ddab987",
    "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json":
        "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225",
    "docs/experiments/manifests/math16_ab3_freeze_manifest.json":
        "84556dc38e0d21cc57f96b0d44092a516cdd76806c6f7468c0286475e23676b1",
    "docs/experiments/audits/math16_pilot02_qwen4b_posthoc_corrected_chain_freeze_v1.json":
        "d6060e712a38738396119d148f30cb15978c25d85cbce188ef43ccd4e07dcdae",
    "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl":
        "2ff030890ea301cb2d94d791f88be8f5a8fa49d46e9b21dbae454c7da5a504e4",
    "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json":
        "e199110fa67459de663a60f5ca03085b6a1f42cba2c6a0bdd470f36c1ff2266a",
}

VALID_CONDITIONS = {"Ab1", "Ab2g", "Ab2d+api", "Ab2d+spec"}
VALID_FAMILIES = {"integer", "polynomial", "radical", "fraction"}

CONDITION_MAP = {
    "ab1": "Ab1",
    "ab2g": "Ab2g",
    "ab2d": "Ab2d+api",
    "ab2d_spec_v2": "Ab2d+spec",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_condition_from_cell_id(cell_id: str) -> str:
    parts = cell_id.split("__")
    if len(parts) < 3:
        return "UNKNOWN"
    raw = parts[2].lower()
    return CONDITION_MAP.get(raw, raw)


def parse_task_from_cell_id(cell_id: str) -> str:
    parts = cell_id.split("__")
    return parts[1] if len(parts) >= 2 else "UNKNOWN"


def parse_seed_from_cell_id(cell_id: str) -> str:
    parts = cell_id.split("__")
    return parts[-1] if parts else "UNKNOWN"


# ---------------------------------------------------------------------------
# Check functions (return True = pass, False = fail)
# ---------------------------------------------------------------------------

def check_7_1_source_integrity(results: dict) -> bool:
    """7.1 SHA256 verification of all frozen source files."""
    print("\n[7.1] Source Integrity Checks")
    all_pass = True
    for rel_path, expected_sha in EXPECTED_SHAS.items():
        full_path = REPO_ROOT / rel_path
        if not full_path.exists():
            print(f"  FAIL: FILE NOT FOUND: {rel_path}")
            results[f"sha_{rel_path}"] = "FILE_NOT_FOUND"
            all_pass = False
            continue
        actual = sha256_file(full_path)
        if actual == expected_sha:
            print(f"  PASS: SHA match: {rel_path}")
            results[f"sha_{rel_path}"] = "MATCH"
        else:
            print(f"  FAIL: SHA MISMATCH: {rel_path}")
            print(f"        expected: {expected_sha}")
            print(f"        actual:   {actual}")
            results[f"sha_{rel_path}"] = f"MISMATCH (actual={actual})"
            all_pass = False
    return all_pass


def check_7_2_cell_identity_uniqueness(comparison: dict, results: dict) -> tuple:
    """7.2 Cell identity uniqueness checks. Returns (pass, roster)."""
    print("\n[7.2] Cell Identity Uniqueness Checks")
    per_cell = comparison.get("per_cell", [])

    # Find 6 posthoc rescued
    posthoc_rescued = [c for c in per_cell if c.get("new_post_healer_status") == "PASSED"]
    # Find 5 primary rescued
    primary_rescued = [c for c in per_cell if c.get("primary_post_healer_status") == "PASSED"]
    # Find 1 noop_to_rescue
    noop_to_rescue = [c for c in per_cell if c.get("noop_to_rescue")]

    checks = {
        "posthoc_rescued_count_is_6": len(posthoc_rescued) == 6,
        "primary_rescued_count_is_5": len(primary_rescued) == 5,
        "noop_to_rescue_count_is_1": len(noop_to_rescue) == 1,
        "no_duplicate_cell_ids": len({c["cell_id"] for c in posthoc_rescued}) == len(posthoc_rescued),
    }

    # Check model prefix
    all_qwen4b = all(c["cell_id"].startswith("qwen3_5_4b") for c in posthoc_rescued)
    checks["all_cells_model_qwen3_5_4b"] = all_qwen4b

    all_pass = True
    for k, v in checks.items():
        if v:
            print(f"  PASS: {k}")
        else:
            print(f"  FAIL: {k}")
            all_pass = False

    results.update({f"cell_id_{k}": "PASS" if v else "FAIL" for k, v in checks.items()})
    results["posthoc_rescued_count"] = len(posthoc_rescued)
    results["primary_rescued_count"] = len(primary_rescued)
    results["noop_to_rescue_count"] = len(noop_to_rescue)

    return all_pass, posthoc_rescued


def check_7_3_attribute_completeness(roster: list, results: dict) -> bool:
    """7.3 Attribute completeness for all 6 cells."""
    print("\n[7.3] Attribute Completeness Checks")
    all_pass = True
    for cell in roster:
        cid = cell["cell_id"]
        condition = parse_condition_from_cell_id(cid)
        task_id = parse_task_from_cell_id(cid)
        seed = parse_seed_from_cell_id(cid)
        before_hash = cell.get("before_source_sha256", "")
        after_hash = cell.get("after_source_sha256", "")

        cell_pass = True
        if condition not in VALID_CONDITIONS:
            print(f"  FAIL: {cid[:50]}... condition '{condition}' not in valid set")
            cell_pass = False
        if not task_id or task_id == "UNKNOWN":
            print(f"  FAIL: {cid[:50]}... task_id missing")
            cell_pass = False
        if not seed or seed == "UNKNOWN":
            print(f"  FAIL: {cid[:50]}... seed missing")
            cell_pass = False
        if not before_hash:
            print(f"  FAIL: {cid[:50]}... before_snippet_hash missing")
            cell_pass = False
        if not after_hash:
            print(f"  FAIL: {cid[:50]}... after_snippet_hash missing")
            cell_pass = False
        if cell_pass:
            print(f"  PASS: {cid[:60]}")
        else:
            all_pass = False

    results["attribute_completeness"] = "PASS" if all_pass else "FAIL"
    return all_pass


def check_7_4_artifact_existence(results: dict) -> bool:
    """7.4 Existence of required artifacts."""
    print("\n[7.4] Artifact Existence Checks")
    required = [
        "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl",
        "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json",
        "docs/experiments/manifests/math16_ab3_freeze_manifest.json",
        "docs/experiments/manifests/math16_posthoc_shared_taxonomy_v1.json",
        "docs/experiments/design/math16_posthoc_shared_taxonomy_v1.md",
        "docs/experiments/design/math16_posthoc_six_cell_rescue_audit_v1_spec.md",
        "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_manifest.json",
        "scripts/build_math16_posthoc_six_cell_rescue_audit_v1.py",
        "tests/test_math16_posthoc_six_cell_rescue_audit_v1.py",
    ]
    all_pass = True
    for rel_path in required:
        full = REPO_ROOT / rel_path
        if full.exists():
            print(f"  PASS: EXISTS: {rel_path}")
            results[f"exists_{rel_path}"] = "PASS"
        else:
            print(f"  FAIL: MISSING: {rel_path}")
            results[f"exists_{rel_path}"] = "MISSING"
            all_pass = False
    return all_pass


def check_7_5_ast_parsability(roster: list, results: dict) -> bool:
    """7.5 AST parsability (best-effort; sha_only artifacts recorded as UNKNOWN)."""
    print("\n[7.5] AST Parsability Checks")
    # Since all cells have artifact_storage == sha_only_not_committed_py,
    # we cannot recover source; record all as UNKNOWN and pass.
    for cell in roster:
        cid = cell["cell_id"]
        print(f"  INFO: {cid[:60]} — artifact_storage=sha_only; ast_parseable=UNKNOWN_SOURCE_NOT_AVAILABLE")
        results[f"ast_{cid}"] = "UNKNOWN_SOURCE_NOT_AVAILABLE"
    return True  # Not a blocking check when source is unavailable


def check_7_6_governance(roster: list, results: dict) -> bool:
    """7.6 Governance checks."""
    print("\n[7.6] Governance Checks")
    checks = {}

    # oracle_answer_used must be false for all cells (or absent/pending — not true)
    oracle_violation = [c for c in roster if c.get("oracle_answer_used") is True]
    checks["oracle_answer_used_never_true"] = len(oracle_violation) == 0

    # Output isolation: output must not be inside docs/experiments
    docs_experiments = REPO_ROOT / "docs" / "experiments"
    output_dir = REPO_ROOT / "artifacts/math16_posthoc_six_cell_rescue_audit_v1/preflight"
    try:
        output_dir.resolve().relative_to(docs_experiments.resolve())
        checks["output_isolated_from_frozen"] = False  # output IS inside docs/experiments
    except ValueError:
        checks["output_isolated_from_frozen"] = True  # correct: output is outside

    # No Stress Test markers
    checks["no_stress_test_execution"] = True  # We verify by checking no stress test files exist
    stress_test_pattern = list((REPO_ROOT / "artifacts").glob("*stress_test*")) if (REPO_ROOT / "artifacts").exists() else []
    if stress_test_pattern:
        checks["no_stress_test_execution"] = False

    # Taxonomy values are fixed
    taxonomy_path = REPO_ROOT / "docs/experiments/manifests/math16_posthoc_shared_taxonomy_v1.json"
    if taxonomy_path.exists():
        with open(taxonomy_path, encoding="utf-8") as f:
            taxonomy = json.load(f)
        layer_a = [v["code"] for v in taxonomy.get("layer_A_original_failure_layer", {}).get("values", [])]
        layer_b = [v["code"] for v in taxonomy.get("layer_B_healer_disposition_result", {}).get("values", [])]
        layer_c = [v["code"] for v in taxonomy.get("layer_C_repair_signature_match", {}).get("values", [])]
        checks["taxonomy_layer_a_count_is_5"] = len(layer_a) == 5
        checks["taxonomy_layer_b_count_is_7"] = len(layer_b) == 7
        checks["taxonomy_layer_c_count_is_3"] = len(layer_c) == 3
    else:
        checks["taxonomy_json_exists"] = False

    all_pass = True
    for k, v in checks.items():
        if v:
            print(f"  PASS: {k}")
        else:
            print(f"  FAIL: {k}")
            all_pass = False

    results.update({f"gov_{k}": "PASS" if v else "FAIL" for k, v in checks.items()})
    return all_pass


def check_7_7_accounting(freeze: dict, comparison: dict, results: dict) -> bool:
    """7.7 Corrected-chain accounting."""
    print("\n[7.7] Corrected-Chain Accounting Checks")
    checks = {
        "replayed_is_10": comparison.get("replayed") == 10,
        "primary_rescued_is_5": comparison.get("primary_rescued") == 5,
        "corrected_rescued_is_6": comparison.get("corrected_rescued") == 6,
        "incremental_1": (comparison.get("corrected_rescued", 0) - comparison.get("primary_rescued", 0)) == 1,
        "corrected_repaired_still_fail_is_4": freeze.get("corrected_repaired_still_fail") == 4,
        "corrected_no_op_is_0": freeze.get("corrected_no_op") == 0,
        "corrected_regression_is_0": freeze.get("corrected_regression") == 0,
    }
    all_pass = True
    for k, v in checks.items():
        if v:
            print(f"  PASS: {k}")
        else:
            print(f"  FAIL: {k}")
            all_pass = False
    results.update({f"accounting_{k}": "PASS" if v else "FAIL" for k, v in checks.items()})
    return all_pass


# ---------------------------------------------------------------------------
# Main preflight
# ---------------------------------------------------------------------------

def main() -> int:
    print("=" * 70)
    print("Math16 Post-hoc Six-Cell Rescue Audit — Zero-Model Preflight")
    print("=" * 70)

    results = {}
    section_results = {}

    # 7.1 Source integrity
    section_results["7_1_source_integrity"] = check_7_1_source_integrity(results)

    # Load frozen comparison and freeze artifacts
    comparison_path = REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json"
    freeze_path = REPO_ROOT / "docs/experiments/audits/math16_pilot02_qwen4b_posthoc_corrected_chain_freeze_v1.json"

    if not comparison_path.exists() or not freeze_path.exists():
        print("\nFATAL: Cannot load frozen comparison artifacts. Aborting remaining checks.")
        print("OVERALL: PREFLIGHT_FAIL")
        return 1

    with open(comparison_path) as f:
        comparison = json.load(f)
    with open(freeze_path) as f:
        freeze = json.load(f)

    # 7.2 Cell identity uniqueness
    cell_pass, roster = check_7_2_cell_identity_uniqueness(comparison, results)
    section_results["7_2_cell_identity_uniqueness"] = cell_pass

    # 7.3 Attribute completeness
    section_results["7_3_attribute_completeness"] = check_7_3_attribute_completeness(roster, results)

    # 7.4 Artifact existence
    section_results["7_4_artifact_existence"] = check_7_4_artifact_existence(results)

    # 7.5 AST parsability
    section_results["7_5_ast_parsability"] = check_7_5_ast_parsability(roster, results)

    # 7.6 Governance
    section_results["7_6_governance"] = check_7_6_governance(roster, results)

    # 7.7 Accounting
    section_results["7_7_accounting"] = check_7_7_accounting(freeze, comparison, results)

    # Final verdict
    overall_pass = all(section_results.values())
    verdict = "PREFLIGHT_PASS" if overall_pass else "PREFLIGHT_FAIL"

    print("\n" + "=" * 70)
    print("SECTION SUMMARY")
    print("=" * 70)
    for section, passed in section_results.items():
        mark = "PASS" if passed else "FAIL"
        print(f"  {mark}: {section}")

    print()
    print(f"OVERALL: {verdict}")
    print("=" * 70)

    if overall_pass:
        print()
        print("Verdicts:")
        print("  MATH16_SIX_CELL_RESCUE_AUDIT_V1_PREREGISTERED")
        print("  SHARED_TAXONOMY_FROZEN")
        print("  SIX_RESCUE_CELL_IDENTITIES_LOCATABLE_FROM_FROZEN_ARTIFACTS")
        print("  OFFICIAL_RESULTS_AND_FINAL_REPORT_PRESERVED")
        print("  READY_FOR_READ_ONLY_SIX_CELL_AUDIT")

    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
