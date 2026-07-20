import os
import json
import hashlib
from typing import Mapping, Any

# Adjust paths to import our modules
import sys
sys.path.append(r"C:\Projects\MathProject_AST_Research_HealerBoundary")

from agent_tools.finals_rebuild.ce115_research_healer_runner import MathHealerRunner
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def calculate_file_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    print("=== Qwen Run 002 Delimiter Extended & Prose Narrow Healer Pipeline ===")
    
    # 1. Define Predictions Baseline (46 units: 4 delim, 9 prose, 13 passed, 10 complex, 10 synthetic)
    delim_targets = {
        "qwen35_4b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301": "predicted_abstain",
        "qwen35_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301": "predicted_abstain",
        "qwen35_4b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301": "predicted_rescue_or_expose",
        "qwen35_9b__ce111_q10_ordered_quadratic_roots_radical__ab2g__seed_2026071301": "predicted_abstain"
    }

    prose_targets = {
        "qwen35_4b__ce111_q05_exact_fraction_expression__ab2g__seed_2026071301": "predicted_rescue_or_expose",
        "qwen35_4b__ce111_q10_ordered_quadratic_roots_radical__ab2d__seed_2026071301": "predicted_rescue_or_expose",
        "qwen35_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071301": "predicted_abstain",
        "qwen35_4b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301": "predicted_rescue_or_expose",
        "qwen35_9b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026071301": "predicted_abstain",
        "qwen35_9b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026071301": "predicted_rescue_or_expose",
        "qwen35_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071301": "predicted_rescue_or_expose",
        "qwen35_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301": "predicted_rescue_or_expose",
        "qwen35_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301": "predicted_rescue_or_expose"
    }
    
    passed_control = [
        "qwen35_4b__ce112_q01_negative_integer_power__ab1__seed_2026071301",
        "qwen35_4b__ce112_q01_negative_integer_power__ab2g__seed_2026071301",
        "qwen35_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026071301",
        "qwen35_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301",
        "qwen35_4b__ce113_q01_negative_fraction_subtraction__ab1__seed_2026071301",
        "qwen35_4b__ce111_q08_polynomial_factor_parameter_recovery__ab1__seed_2026071301",
        "qwen35_9b__ce112_q09_divisor_multiple_intersection__ab2g__seed_2026071301",
        "qwen35_9b__ce112_q01_negative_integer_power__ab2g__seed_2026071301",
        "qwen35_9b__ce111_q03_prime_factor_selection__ab2g__seed_2026071301",
        "qwen35_9b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026071301",
        "qwen35_9b__ce113_q01_negative_fraction_subtraction__ab1__seed_2026071301",
        "qwen35_9b__ce112_q12_independent_probability_fraction__ab2g__seed_2026071301",
        "qwen35_9b__ce112_q01_negative_integer_power__ab1__seed_2026071301"
    ]
    
    complex_control = [
        "qwen35_4b__ce112_q12_independent_probability_fraction__ab1__seed_2026071301",
        "qwen35_4b__ce112_q12_independent_probability_fraction__ab2g__seed_2026071301",
        "qwen35_4b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301",
        "qwen35_9b__ce113_q01_negative_fraction_subtraction__ab2d__seed_2026071301",
        "qwen35_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301",
        "qwen35_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301",
        "qwen35_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301",
        "qwen35_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301"
    ]

    synthetic_cases = [f"synthetic_negative_case_{i}" for i in range(1, 11)]
    
    predictions = {}
    predictions.update(delim_targets)
    predictions.update(prose_targets)
    for cell_id in passed_control + complex_control + synthetic_cases:
        predictions[cell_id] = "predicted_no_trigger"
        
    predictions_path = r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\results\qwen_math16_run_002_delimiter_extended_predictions.json"
    os.makedirs(os.path.dirname(predictions_path), exist_ok=True)
    with open(predictions_path, "w", encoding="utf-8") as f:
        json.dump(predictions, f, ensure_ascii=False, indent=2)
        
    pred_hash = calculate_file_sha256(predictions_path)
    print(f"Predictions Locked SHA-256: {pred_hash}")

    # 2. Healer Pipeline Runner Execution
    run_dirs = [
        r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\results\qwen35_4b_math16_ab123_run_002",
        r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\results\qwen35_9b_math16_ab123_run_002"
    ]
    
    # Define synthetic sources
    synth_sources = {
        "synthetic_negative_case_1": """def generate(level=1, **kwargs):
    x = 5 # Let's find the sum of these two products
    return x""",
        "synthetic_negative_case_2": """def generate(level=1, **kwargs):
    '''This is a docstring describing generate method'''
    x = 5
    return x""",
        "synthetic_negative_case_3": """def generate(level=1, **kwargs):
    msg = "To find the exact fraction, we first calculate the value"
    return msg""",
        "synthetic_negative_case_4": """def generate(level=1, **kwargs):
    correct_val = "Wait, let's check if D is positive"
    return correct_val""",
        "synthetic_negative_case_5": """def generate(level=1, **kwargs):
    exact_fraction_sum = 10
    return exact_fraction_sum""",
        "synthetic_negative_case_6": """def generate(level=1, **kwargs):
    print("Compute the sum of these two products:")
    return 0""",
        "synthetic_negative_case_7": """def generate(level=1, **kwargs):
    y = 10 # note: a = 5
    return y""",
        "synthetic_negative_case_8": """def generate(level=1, **kwargs):
    # We first find the sum
    # of these two products
    return 1""",
        "synthetic_negative_case_9": """def generate(level=1, **kwargs):
    a, b = 1, 2
    return f"Calculate this sum: {a} + {b}" """,
        "synthetic_negative_case_10": """def generate(level=1, **kwargs):
    # Check for perfect square to ensure integer roots
    return 10"""
    }

    results = []
    runner = MathHealerRunner(max_passes=3)
    
    for cell_id, pred_outcome in predictions.items():
        if cell_id in synthetic_cases:
            # Synthetic negative control test
            source = synth_sources[cell_id]
            res = runner.run(source, context={})
            changed_any = any(pp.changed for pp in res.provenance)
            actual_outcome = "no_trigger" if not changed_any else "triggered"
            print(f"Synthetic Unit: {cell_id}\n  Pred: {pred_outcome} -> Actual: {actual_outcome}")
            results.append({
                "cell_id": cell_id,
                "predicted_outcome": pred_outcome,
                "actual_outcome": actual_outcome
            })
            continue

        # Find cell folder path
        run_dir = run_dirs[0] if "qwen35_4b" in cell_id else run_dirs[1]
        cell_path = os.path.join(run_dir, "cells", cell_id)
        art_path = os.path.join(cell_path, "artifact.json")
        cand_path = os.path.join(cell_path, "extracted_candidate.py")
        
        if not os.path.exists(cand_path):
            print(f"Skipping {cell_id} (missing candidate file)")
            continue
            
        with open(cand_path, "r", encoding="utf-8") as f:
            source = f.read()
            
        with open(art_path, "r", encoding="utf-8") as f:
            art = json.load(f)
            
        task_metadata = dict(art.get("audit_oracle_payload", {}))
        task_metadata.update({
            "skill_id": art["task_id"],
            "oracle_type": art["family"]
        })
        frozen_params = art.get("frozen_parameters", {})
        
        context = {
            "task": task_metadata,
            "frozen": frozen_params
        }
        
        res = runner.run(source, context=context)
        
        changed_any = False
        for pp in res.provenance:
            if pp.changed:
                changed_any = True
                break
                
        actual_outcome = "no_trigger"
        if changed_any:
            if res.rolled_back:
                actual_outcome = "triggered_rolled_back"
            else:
                new_source = res.output_source
                # Re-evaluate
                outcome, _code, details = classify_response(
                    new_source,
                    {"oracle_payload": dict(frozen_params)},
                    dict(task_metadata),
                )
                print(f"Cell {cell_id} modified. Rerun evaluator verdict: {outcome}")
                
                # Check if rescued
                if outcome == "PASSED":
                    actual_outcome = "rescue_to_pass"
                else:
                    actual_outcome = f"triggered_changed_still_fail({outcome})"
                
                # Save H1 source code and update artifact.json hashes & provenance
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
                    "outcome": actual_outcome,
                    "healer_passes": [
                        {
                            "pass_index": p.pass_index,
                            "phase": p.validation.get("phase"),
                            "triggered_rule": p.selected_rule_id,
                            "changed": p.changed,
                            "outcome": p.validation.get("evaluator_outcome") or p.stop_reason
                        }
                        for p in res.provenance if p.selected_rule_id is not None
                    ]
                }
                with open(art_path, "w", encoding="utf-8") as wf:
                    json.dump(art, wf, ensure_ascii=False, indent=2)
                    
        print(f"Cell: {cell_id}\n  Pred: {pred_outcome} -> Actual: {actual_outcome}")
        results.append({
            "cell_id": cell_id,
            "predicted_outcome": pred_outcome,
            "actual_outcome": actual_outcome
        })
        
    # Write report raw data
    out_report_path = r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\results\healer_delimiter_extended_report_data.json"
    with open(out_report_path, "w", encoding="utf-8") as f:
        json.dump({
            "pred_hash": pred_hash,
            "results": results
        }, f, ensure_ascii=False, indent=2)
    print(f"\nReport raw data written to {out_report_path}")

if __name__ == "__main__":
    main()
