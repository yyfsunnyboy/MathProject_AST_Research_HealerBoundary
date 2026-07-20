import os
import json
import hashlib
import random
import ast
from typing import Mapping, Any

# Adjust paths to import our modules
import sys
sys.path.append(r"C:\Projects\MathProject_AST_Research_HealerBoundary")

from agent_tools.finals_rebuild.ce115_research_healer_runner import MathHealerRunner, RULE_REGISTRY
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response

def calculate_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def run_healer_for_cell(cell_path, task_metadata, frozen_params):
    candidate_path = os.path.join(cell_path, "extracted_candidate.py")
    if not os.path.exists(candidate_path):
        return "no_candidate_file", None, None

    with open(candidate_path, "r", encoding="utf-8") as f:
        source = f.read()

    context = {
        "task": task_metadata,
        "frozen": frozen_params
    }

    # Instantiate MathHealerRunner (which automatically uses the ALLOWLIST containing the new rule)
    runner = MathHealerRunner()
    res = runner.run(source, context=context)

    return "ok", res, source

def main():
    print("=== Qwen Run 002 Healer Execution Pipeline ===")

    # 1. Verification of Predictions baseline
    predictions_path = r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\results\qwen_math16_run_002_healer_predictions.json"
    pred_hash = calculate_sha256(predictions_path)
    print(f"Predictions Hash Locked: {pred_hash}")

    with open(predictions_path, "r", encoding="utf-8") as f:
        predictions = json.load(f)

    # 2. Iterate through predictions (the 57 formal cells)
    run_dirs = [
        r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\results\qwen35_4b_math16_ab123_run_002",
        r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\results\qwen35_9b_math16_ab123_run_002"
    ]

    formal_results = []
    
    for run_dir in run_dirs:
        cells_dir = os.path.join(run_dir, "cells")
        if not os.path.exists(cells_dir):
            continue
        for cell_name in os.listdir(cells_dir):
            cell_path = os.path.join(cells_dir, cell_name)
            art_path = os.path.join(cell_path, "artifact.json")
            if not os.path.exists(art_path):
                continue
            with open(art_path, "r", encoding="utf-8") as f:
                art = json.load(f)
            
            cell_id = art["cell_id"]
            if cell_id not in predictions:
                continue

            pred_outcome = predictions[cell_id]
            print(f"\nProcessing Cell: {cell_id} (Pred: {pred_outcome})")

            # Extract task metadata and frozen params
            task_metadata = dict(art.get("audit_oracle_payload", {}))
            task_metadata.update({
                "skill_id": art["task_id"],
                "oracle_type": art["family"]
            })
            frozen_params = art.get("frozen_parameters", {})

            status, res, raw_source = run_healer_for_cell(cell_path, task_metadata, frozen_params)
            if status != "ok":
                print(f"  Failed to load candidate for {cell_id}")
                formal_results.append({
                    "cell_id": cell_id,
                    "predicted_outcome": pred_outcome,
                    "actual_outcome": "no_candidate",
                    "match": False
                })
                continue

            # Analyze healer run outcomes
            final_status = res.final_status  # "no_op", "changed", "validation_failed", etc.
            healer_outcome = "no_trigger"

            # Check if any rule changed anything
            changed_any = False
            for pp in res.provenance:
                if pp.changed:
                    changed_any = True
                    break

            if not changed_any:
                healer_outcome = "no_trigger"
            else:
                # Some rule changed the code!
                # Check validation (AST compile validation)
                # If final status is validation_failed or rolled_back
                if res.rolled_back:
                    healer_outcome = "triggered_rolled_back"
                else:
                    # Successfully changed and parsed!
                    # Now re-evaluate to see if it is a rescue
                    new_source = res.output_source
                    
                    # We run evaluator
                    outcome, _code, details = classify_response(
                        new_source,
                        {"oracle_payload": dict(frozen_params)},
                        dict(task_metadata),
                    )

                    print(f"  Healed code parsed. Evaluator outcome: {outcome}")

                    # Did it go FAIL -> PASS?
                    # The original status was FAILED (since this is an eligible cell).
                    # Check if new outcome is PASSED
                    if outcome == "PASSED":
                        healer_outcome = "rescue_to_pass"
                        
                        # Save H1 source code and update artifact.json hashes
                        repaired_path = os.path.join(cell_path, "repaired_candidate.py")
                        with open(repaired_path, "w", encoding="utf-8") as rf:
                            rf.write(new_source)
                        
                        h1_hash = sha256_text(new_source)
                        
                        # Read and update artifact.json without overriding H0 readonly fields
                        if "hashes" not in art:
                            art["hashes"] = {}
                        art["hashes"]["repaired_candidate"] = h1_hash
                        art["healer"] = {
                            "attempted": True,
                            "healer_eligible": True,
                            "enabled": True,
                            "outcome": "rescue_to_pass"
                        }
                        # Save back updated artifact.json
                        with open(art_path, "w", encoding="utf-8") as wf:
                            json.dump(art, wf, ensure_ascii=False, indent=2)
                        
                        print(f"  [RESCUED] Repaired candidate saved. Hash: {h1_hash}")
                    else:
                        healer_outcome = "triggered_changed_still_fail"
                        # We also save candidate but it didn't rescue. As per standard, we write it and keep hash
                        repaired_path = os.path.join(cell_path, "repaired_candidate.py")
                        with open(repaired_path, "w", encoding="utf-8") as rf:
                            rf.write(new_source)
                        
                        h1_hash = sha256_text(new_source)
                        if "hashes" not in art:
                            art["hashes"] = {}
                        art["hashes"]["repaired_candidate"] = h1_hash
                        art["healer"] = {
                            "attempted": True,
                            "healer_eligible": True,
                            "enabled": True,
                            "outcome": "triggered_changed_still_fail"
                        }
                        with open(art_path, "w", encoding="utf-8") as wf:
                            json.dump(art, wf, ensure_ascii=False, indent=2)
                        
                        print(f"  [STILL_FAIL] Repaired candidate saved. Hash: {h1_hash}")

            match = False
            if pred_outcome == "predicted_rescue" and healer_outcome == "rescue_to_pass":
                match = True
            elif pred_outcome == "predicted_no_trigger" and healer_outcome == "no_trigger":
                match = True
            elif pred_outcome == "predicted_trigger_uncertain" and healer_outcome in ("triggered_rolled_back", "triggered_changed_still_fail", "rescue_to_pass"):
                match = True

            print(f"  Actual Outcome: {healer_outcome} (Match: {match})")
            formal_results.append({
                "cell_id": cell_id,
                "predicted_outcome": pred_outcome,
                "actual_outcome": healer_outcome,
                "match": match
            })

    # 3. Negative Control (15 PASSED cells)
    print("\n=== Running Negative Control (PASSED cells dry-run) ===")
    
    passed_4b = []
    passed_9b = []
    
    for run_dir in run_dirs:
        cells_dir = os.path.join(run_dir, "cells")
        if not os.path.exists(cells_dir):
            continue
        for cell_name in os.listdir(cells_dir):
            cell_path = os.path.join(cells_dir, cell_name)
            art_path = os.path.join(cell_path, "artifact.json")
            if not os.path.exists(art_path):
                continue
            with open(art_path, "r", encoding="utf-8") as f:
                art = json.load(f)
            
            # Check if H0 status was PASSED
            if art.get("evaluator_status") == "PASSED":
                if "qwen35_4b" in art["cell_id"]:
                    passed_4b.append(art)
                else:
                    passed_9b.append(art)

    print(f"Passed 4B count: {len(passed_4b)}, Passed 9B count: {len(passed_9b)}")
    
    # Random sampling: 7 from 4B, 8 from 9B (using a fixed seed for reproducibility)
    random.seed(20260720)
    sample_4b = random.sample(passed_4b, min(7, len(passed_4b)))
    sample_9b = random.sample(passed_9b, min(8, len(passed_9b)))
    
    control_cells = sample_4b + sample_9b
    print(f"Total sampled control cells: {len(control_cells)} (4B: {len(sample_4b)}, 9B: {len(sample_9b)})")
    
    control_results = []
    runner = MathHealerRunner()
    
    for art in control_cells:
        cell_id = art["cell_id"]
        candidate_path = os.path.join(run_dirs[0] if "qwen35_4b" in cell_id else run_dirs[1], "cells", cell_id, "extracted_candidate.py")
        
        if not os.path.exists(candidate_path):
            print(f"  Missing control candidate for {cell_id}")
            continue
            
        with open(candidate_path, "r", encoding="utf-8") as f:
            source = f.read()
            
        task_metadata = dict(art.get("audit_oracle_payload", {}))
        task_metadata.update({
            "skill_id": art["task_id"],
            "oracle_type": art["family"]
        })
        context = {
            "task": task_metadata,
            "frozen": art.get("frozen_parameters", {})
        }
        
        # Test is_triggered() for ALL 4 active rules
        triggered_rules = []
        for r_id in runner.allowlist:
            rule = RULE_REGISTRY.get(r_id)
            if rule is None:
                continue
            applicable, _, _ = rule.is_applicable(source, context)
            if applicable:
                triggered, _ = rule.is_triggered(source, context)
                if triggered:
                    triggered_rules.append(r_id)
        
        outcome_str = "no_trigger"
        if triggered_rules:
            outcome_str = f"triggered:{','.join(triggered_rules)}"
            print(f"  [WARNING] PASSED cell {cell_id} triggered rules: {triggered_rules}")
        else:
            print(f"  PASSED cell {cell_id} passed dry-run cleanly.")
            
        control_results.append({
            "cell_id": cell_id,
            "predicted_outcome": "predicted_no_trigger",
            "actual_outcome": outcome_str,
            "match": len(triggered_rules) == 0
        })

    # Save outputs to JSON for final report assembly
    report_data = {
        "pred_hash": pred_hash,
        "formal": formal_results,
        "control": control_results
    }
    
    report_out_path = r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\results\healer_run_002_report_data.json"
    with open(report_out_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    print(f"\nReport raw data written to {report_out_path}")

if __name__ == "__main__":
    main()
