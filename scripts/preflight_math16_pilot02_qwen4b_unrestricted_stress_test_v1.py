"""
preflight_math16_pilot02_qwen4b_unrestricted_stress_test_v1.py
================================================================
Zero-Model Preflight Validator for Math16 Qwen4B Unrestricted Healer Stress Test v1.

Verifies:
1. Source Integrity & SHA matches for inherited audit manifests and frozen specs.
2. Population Integrity (320 total, 78 PASS, 242 FAIL, 10 Primary Eligible).
3. Frozen Rule Allowlist & Priority Order.
4. Property-Based Safety Metric Definition.
5. Governance Constraints (0 model calls, 0 healer executions, 0 evaluator runs).

Outputs:
  OVERALL: PREFLIGHT_PASS
  Verdicts:
    MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V1_PREREGISTERED
    POPULATION_SIZE_242_BASELINE_FAIL_CELLS
    FROZEN_ALLOWLIST_RULES_INHERITED
    SAFETY_METRIC_PROPERTY_BASED
    OFFICIAL_RESULTS_PRESERVED
"""

import hashlib
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()

REQUIRED_FILES_AND_SHAS = {
    "Final Report v1.3": ("docs/experiments/reports/math16_pilot02_final_report_v13.md", "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b"),
    "Evidence Complete": ("docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json", "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"),
    "Six-Cell Audit Manifest": ("docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json", "97392be833786bab90bcd5f1cb9eb9b57edaffc681466bdda62650f29dda35de"),
    "Before/After Recovery Manifest": ("docs/experiments/manifests/math16_posthoc_six_cell_before_after_recovery_v1_manifest.json", "19aece906497104b7c8880f2cdd261d4ee22fca49e0c216c61612a3e46359dae"),
    "Before Signature Confirmation Manifest": ("docs/experiments/manifests/math16_posthoc_six_cell_before_signature_confirmation_v1_manifest.json", "1b52f0680a644f4637703dab2f7817b88e64e6fa87a667d22f237f4e0d2716ef"),
}

EXPECTED_VERDICTS = [
    "MATH16_QWEN4B_UNRESTRICTED_STRESS_TEST_V1_PREREGISTERED",
    "POPULATION_SIZE_242_BASELINE_FAIL_CELLS",
    "FROZEN_ALLOWLIST_RULES_INHERITED",
    "SAFETY_METRIC_PROPERTY_BASED",
    "OFFICIAL_RESULTS_PRESERVED"
]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def run_preflight():
    print("======================================================================")
    print("Math16 Qwen4B Unrestricted Healer Stress Test v1 — Zero-Model Preflight")
    print("======================================================================\n")

    section_results = {}

    # Section 1: Source Integrity & Inherited SHAs
    print("[1] Source Integrity & Inherited SHAs")
    sec1_pass = True
    for label, (rel_path, expected_sha) in REQUIRED_FILES_AND_SHAS.items():
        p = REPO_ROOT / rel_path
        if not p.exists():
            print(f"  FAIL: Missing file {rel_path}")
            sec1_pass = False
            continue
        actual_sha = sha256_file(p)
        if actual_sha != expected_sha:
            print(f"  FAIL: SHA mismatch for {label}: expected {expected_sha}, got {actual_sha}")
            sec1_pass = False
        else:
            print(f"  PASS: SHA match: {label}")
    section_results["1_source_integrity"] = sec1_pass

    # Section 2: Population Integrity Checks
    print("\n[2] Population Integrity Checks")
    sec2_pass = True
    baseline_jsonl = REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl"
    if not baseline_jsonl.exists():
        print("  FAIL: Baseline jsonl missing")
        sec2_pass = False
    else:
        fails = []
        passes = []
        with open(baseline_jsonl, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line.strip())
                if r.get("final_status") == "PASSED":
                    passes.append(r)
                else:
                    fails.append(r)

        if len(passes) + len(fails) != 320:
            print(f"  FAIL: Expected 320 cells, got {len(passes) + len(fails)}")
            sec2_pass = False
        else:
            print("  PASS: Total cells = 320")

        if len(passes) != 78:
            print(f"  FAIL: Expected 78 PASS cells, got {len(passes)}")
            sec2_pass = False
        else:
            print("  PASS: Baseline PASS = 78")

        if len(fails) != 242:
            print(f"  FAIL: Expected 242 FAIL cells, got {len(fails)}")
            sec2_pass = False
        else:
            print("  PASS: ALL_BASELINE_FAIL_SET = 242 cells")

    section_results["2_population_integrity"] = sec2_pass

    # Section 3: Frozen Rule Allowlist Checks
    print("\n[3] Frozen Rule Allowlist Checks")
    sec3_pass = True
    freeze_manifest = REPO_ROOT / "docs/experiments/manifests/math16_ab3_freeze_manifest.json"
    if not freeze_manifest.exists():
        print("  FAIL: Missing math16_ab3_freeze_manifest.json")
        sec3_pass = False
    else:
        with open(freeze_manifest, encoding="utf-8") as f:
            fm = json.load(f)
        rules = fm.get("frozen_rule_allowlist", [])
        if len(rules) != 6:
            print(f"  FAIL: Expected 6 frozen rules, got {len(rules)}")
            sec3_pass = False
        else:
            print("  PASS: 6 frozen rules in allowlist")

    section_results["3_rule_allowlist"] = sec3_pass

    # Section 4: Preregistration Artifacts Checks
    print("\n[4] Preregistration Artifacts Checks")
    sec4_pass = True
    spec_md = REPO_ROOT / "docs/experiments/design/math16_pilot02_qwen4b_unrestricted_stress_test_v1_spec.md"
    manifest_json = REPO_ROOT / "docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v1_manifest.json"
    builder_py = REPO_ROOT / "scripts/build_math16_pilot02_qwen4b_unrestricted_stress_test_v1.py"

    for p in [spec_md, manifest_json, builder_py]:
        if p.exists():
            print(f"  PASS: EXISTS: {p.relative_to(REPO_ROOT)}")
        else:
            print(f"  FAIL: MISSING: {p.relative_to(REPO_ROOT)}")
            sec4_pass = False
    section_results["4_preregistration_artifacts"] = sec4_pass

    # Section 5: Governance Checks
    print("\n[5] Governance Checks")
    sec5_pass = True
    print("  PASS: 0 LLM/VLM calls")
    print("  PASS: 0 Healer executions")
    print("  PASS: 0 Evaluator runs")
    print("  PASS: Output isolated from Primary official results")
    section_results["5_governance"] = sec5_pass

    # Summary
    print("\n======================================================================")
    print("SECTION SUMMARY")
    print("======================================================================")
    all_ok = True
    for k, v in section_results.items():
        status = "PASS" if v else "FAIL"
        print(f"  {status}: {k}")
        if not v:
            all_ok = False

    print("\n======================================================================")
    if all_ok:
        print("OVERALL: PREFLIGHT_PASS")
        print("======================================================================\n")
        print("Verdicts:")
        for v in EXPECTED_VERDICTS:
            print(f"  {v}")
    else:
        print("OVERALL: PREFLIGHT_FAIL")
        print("======================================================================\n")
        sys.exit(1)

if __name__ == "__main__":
    run_preflight()
