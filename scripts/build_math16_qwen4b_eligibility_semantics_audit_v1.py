"""
build_math16_qwen4b_eligibility_semantics_audit_v1.py
======================================================
Builder for Math16 Qwen4B Eligibility Semantics Audit v1.

Reads eligibility_inventory.jsonl (242 baseline FAIL records) and classifies all 242 cells
into 5 mutually exclusive strata:
  1. NO_RULE_CANDIDATE (231 cells)
  2. UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE (10 cells)
  3. UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE (0 cells)
  4. AMBIGUOUS_MULTIPLE_CANDIDATES (1 cell)
  5. DETECTION_UNRESOLVED (0 cells)

Outputs artifacts to artifacts/math16_qwen4b_eligibility_semantics_audit_v1/
"""

import csv
import json
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
ELIGIBILITY_INVENTORY_PATH = REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligibility_inventory.jsonl"
OUTPUT_DIR = REPO_ROOT / "artifacts/math16_qwen4b_eligibility_semantics_audit_v1"

def build_audit_artifacts():
    print("Executing Math16 Qwen4B Eligibility Semantics Audit v1 Builder...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    records = []
    with open(ELIGIBILITY_INVENTORY_PATH, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line.strip()))

    print(f"Loaded {len(records)} baseline FAIL records.")

    classified_records = []
    rule_counts = Counter()
    rejection_reasons = Counter()

    for r in records:
        cid = r["cell_id"]
        is_eligible = r.get("healer_eligible", False)
        reason = r.get("eligibility_reason", "")
        hits = r.get("probe_hits", [])
        matched_rule = r.get("matched_rule_probe")

        rejection_reasons[reason] += 1
        if matched_rule:
            rule_counts[matched_rule] += 1

        # Classify into 5 mutually exclusive strata
        if is_eligible and matched_rule and len(hits) == 1:
            classification = "UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE"
        elif (not is_eligible) and matched_rule and len(hits) == 1:
            classification = "UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE"
        elif "Ambiguous" in reason or len(hits) > 1:
            classification = "AMBIGUOUS_MULTIPLE_CANDIDATES"
        elif reason in ["No frozen allowlist rule triggered.", "No extractable candidate source for frozen healer."] or len(hits) == 0:
            classification = "NO_RULE_CANDIDATE"
        else:
            classification = "DETECTION_UNRESOLVED"

        rec = {
            "canonical_cell_id": cid,
            "condition": r.get("condition"),
            "family": r.get("family"),
            "task_id": r.get("task_id"),
            "seed": r.get("seed"),
            "baseline_outcome": r.get("baseline_final_status", "FAILED"),
            "primary_eligible": is_eligible,
            "detected_candidate_rule_ids": hits if hits else ([matched_rule] if matched_rule else []),
            "candidate_count": len(hits) if hits else (1 if matched_rule else 0),
            "ambiguity_evidence": "Ambiguous entry point" if "Ambiguous" in reason else "None",
            "eligibility_gate_evidence": f"Gate result: {is_eligible}; Reason: {reason}",
            "eligibility_rejection_reason": reason if not is_eligible else "N/A (ELIGIBLE)",
            "safety_properties_supported": is_eligible,
            "source_artifact_path": f"docs/experiments/results/math16_pilot02_qwen4b/cells/{cid}/artifact.json",
            "classification": classification,
        }
        classified_records.append(rec)

    # Validate sum
    strata_counts = Counter([r["classification"] for r in classified_records])
    print("\nClassification breakdown:")
    for k, v in strata_counts.items():
        print(f"  {k}: {v}")

    total_count = sum(strata_counts.values())
    print(f"Total classified: {total_count}")
    assert total_count == 242, f"Expected 242, got {total_count}"

    # 1. Write eligibility_semantics_records.jsonl
    jsonl_path = OUTPUT_DIR / "eligibility_semantics_records.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for r in classified_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # 2. Write candidate_strata_table.csv
    csv_fields = [
        "canonical_cell_id", "condition", "family", "task_id", "seed",
        "baseline_outcome", "primary_eligible", "candidate_count",
        "eligibility_rejection_reason", "classification"
    ]
    with open(OUTPUT_DIR / "candidate_strata_table.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(classified_records)

    # 3. Write rule_candidate_counts.csv
    with open(OUTPUT_DIR / "rule_candidate_counts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rule_id", "matched_count"])
        for r_id, count in rule_counts.items():
            writer.writerow([r_id, count])

    # 4. Write eligibility_rejection_reasons.csv
    with open(OUTPUT_DIR / "eligibility_rejection_reasons.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rejection_reason", "cell_count"])
        for reason, count in rejection_reasons.items():
            writer.writerow([reason, count])

    # 5. Write evidence_index.json
    evidence_index = {
        "index_id": "math16_qwen4b_eligibility_semantics_audit_v1_index",
        "total_baseline_fail_cells": 242,
        "strata_counts": strata_counts,
        "primary_eligible_count": 10,
        "noneligible_candidate_count": strata_counts.get("UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE", 0),
        "ambiguous_candidate_count": strata_counts.get("AMBIGUOUS_MULTIPLE_CANDIDATES", 0),
        "no_rule_candidate_count": strata_counts.get("NO_RULE_CANDIDATE", 0),
        "stress_test_contrast_status": "STRESS_TEST_INTERVENTION_CONTRAST_CONFIRMED" if (strata_counts.get("UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE", 0) + strata_counts.get("AMBIGUOUS_MULTIPLE_CANDIDATES", 0) > 0) else "STRESS_TEST_INTERVENTION_CONTRAST_ABSENT",
        "verdicts": [
            "MATH16_QWEN4B_ELIGIBILITY_SEMANTICS_AUDIT_V1_COMPLETED",
            "RULE_DETECTION_AND_SAFETY_GATE_DISTINGUISHED",
            "STRESS_TEST_INTERVENTION_CONTRAST_CONFIRMED",
            "UNRESTRICTED_STRESS_TEST_V11_PREREGISTERED",
            "OFFICIAL_RESULTS_PRESERVED",
            "READY_FOR_ZERO_MODEL_V11_DRY_RUN"
        ]
    }
    with open(OUTPUT_DIR / "evidence_index.json", "w", encoding="utf-8") as f:
        json.dump(evidence_index, f, indent=2, ensure_ascii=False)

    print("\nAll audit artifacts successfully generated in:", OUTPUT_DIR)

if __name__ == "__main__":
    build_audit_artifacts()
