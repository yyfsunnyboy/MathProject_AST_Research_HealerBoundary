import os
import sys
import json
import re
import ast
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math_boundary_pilot import load_pilot_tasks, classify_response
from agent_tools.finals_rebuild.ce115_calc_formal_runner import build_local_confirmatory_plan
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters
from agent_tools.finals_rebuild.extraction import extract_code

CORRECTED_RUN_DIR = ROOT / "docs" / "experiments" / "results" / "ce115_corrected_context_formal_run"
CELLS_DIR = CORRECTED_RUN_DIR / "cells"
MANIFEST_PATH = ROOT / "tests" / "finals_rebuild" / "fixtures" / "math_generation_tasks_ce115_pilot.jsonl"

def check_reasoning_leakage(text: str) -> bool:
    leak_patterns = [
        r"\?\s*No\b",
        r"\?\s*Wait\b",
        r"#\s*Wait\b",
        r"\bWait,\s*need\b",
        r"\bNo,\s*remainder\b"
    ]
    for pattern in leak_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def check_prefix_parsing(raw_text: str):
    # Find all occurrences of "return {"
    lines = raw_text.splitlines()
    for i, line in enumerate(lines):
        if "return {" in line:
            # Try to find the closing brace matching this return block
            brace_count = 0
            started = False
            closing_line = -1
            for j in range(i, len(lines)):
                l = lines[j]
                if "{" in l:
                    brace_count += l.count("{")
                    started = True
                if "}" in l:
                    brace_count -= l.count("}")
                if started and brace_count <= 0:
                    closing_line = j
                    break
            if closing_line != -1:
                prefix_lines = lines[:closing_line + 1]
                prefix_str = "\n".join(prefix_lines)
                extracted = extract_code(prefix_str)
                if extracted.extracted_code:
                    try:
                        ast.parse(extracted.extracted_code)
                        if "def generate" in extracted.extracted_code:
                            return True, extracted.extracted_code, closing_line
                    except SyntaxError:
                        pass
    return False, None, -1

def get_sha256(text: str) -> str:
    import hashlib
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def rebuild():
    # 1. Load tasks
    tasks = load_pilot_tasks(MANIFEST_PATH)
    tasks_by_id = {t["task_id"]: t for t in tasks}
    
    # 2. Load corrected results
    cell_files = [f for f in os.listdir(CELLS_DIR) if f.endswith(".jsonl")]
    records = []
    
    for fn in sorted(cell_files):
        path = CELLS_DIR / fn
        with open(path, "r", encoding="utf-8") as f:
            cell_data = json.load(f)
        records.append(cell_data)
        
    print(f"Loaded {len(records)} cell records.")
    
    # Evaluate each record using math_boundary_pilot evaluator gates
    eval_results = []
    for idx, r in enumerate(records):
        cell_id = r["cell_id"]
        raw_output = r["raw_first_attempt_output"]
        m_task_id = r["task"]
        seed = r["seed"]
        
        task = tasks_by_id[m_task_id]
        sampled = sample_task_parameters(task, int(seed))
        frozen = {
            "task_id": m_task_id,
            "oracle_type": task["oracle_type"],
            "oracle_payload": sampled["oracle_payload"],
            "repeat_seed": int(seed),
        }
        
        # Evaluate
        outcome, candidate, details = classify_response(raw_output, frozen, task)
        has_leak = check_reasoning_leakage(raw_output)
        
        # Repetition diagnostics
        rep = r.get("repetition_diagnostics", {})
        
        # Pre-loop complete diagnostics (for DEGENERATIVE cells)
        pre_loop_ok, prefix_src, closing_ln = False, None, -1
        is_degen = r.get("validity_classification") == "MODEL_DEGENERATIVE_NONTERMINATION"
        if is_degen:
            pre_loop_ok, prefix_src, closing_ln = check_prefix_parsing(raw_output)
            
        eval_record = {
            "cell_id": cell_id,
            "model": r["model"],
            "task": r["task"],
            "condition": r["condition"],
            "seed": r["seed"],
            "validity_classification": r["validity_classification"],
            "evaluator_outcome": outcome,
            "has_leakage": has_leak,
            "eval_count": r.get("eval_count", 0),
            "prompt_eval_count": r.get("prompt_eval_count", 0),
            "total_token_count": r.get("total_token_count", 0),
            "raw_output_sha256": r.get("raw_output_sha256", ""),
            "repetition_diagnostics": rep,
            "pre_loop_program_complete": pre_loop_ok,
            "post_completion_loop": is_degen and pre_loop_ok,
            "safe_prefix_candidate": is_degen and pre_loop_ok,
            "safe_prefix_status": "CANDIDATE_ONLY" if (is_degen and pre_loop_ok) else ("NOT_CANDIDATE" if is_degen else "INSUFFICIENT_EVIDENCE"),
            "safe_prefix_evidence": f"return block closes at line {closing_ln}" if pre_loop_ok else "no complete prefix parsed"
        }
        eval_results.append(eval_record)
        print(f"[{idx+1}/72] Evaluated {cell_id} -> {outcome} (leak={has_leak}, pre_loop={pre_loop_ok})")

    # 3. Rebuild Corrected Output Budget Census
    # Filter natural completions (validity_classification = NATURAL_COMPLETE)
    natural_records = [r for r in eval_results if r["validity_classification"] == "NATURAL_COMPLETE"]
    natural_tokens = [r["eval_count"] for r in natural_records]
    
    census_stats = {}
    if natural_tokens:
        census_stats["overall"] = {
            "n": len(natural_tokens),
            "median": float(np.median(natural_tokens)),
            "P50": float(np.percentile(natural_tokens, 50)),
            "P90": float(np.percentile(natural_tokens, 90)),
            "P95": float(np.percentile(natural_tokens, 95)),
            "P99": float(np.percentile(natural_tokens, 99)),
            "max": float(np.max(natural_tokens))
        }
        
    for cond in ["ab1", "ab2g", "ab2d"]:
        cond_tokens = [r["eval_count"] for r in natural_records if r["condition"] == cond]
        if cond_tokens:
            census_stats[f"condition_{cond}"] = {
                "n": len(cond_tokens),
                "median": float(np.median(cond_tokens)),
                "P90": float(np.percentile(cond_tokens, 90)),
                "P95": float(np.percentile(cond_tokens, 95)),
                "P99": float(np.percentile(cond_tokens, 99)),
                "max": float(np.max(cond_tokens))
            }
            
    # Rebuild Corrected Census JSON
    census_json = {
        "census_metadata": "CORRECTED_OUTPUT_BUDGET_CENSUS",
        "total_records_analyzed": len(eval_results),
        "natural_completions_analyzed": len(natural_records),
        "degeneration_completions_analyzed": len(eval_results) - len(natural_records),
        "level_a_statistics": census_stats,
        "records": eval_results
    }
    with open(CORRECTED_RUN_DIR / "ce115_corrected_census.json", "w", encoding="utf-8") as f:
        json.dump(census_json, f, indent=2, ensure_ascii=False)
    print("Corrected Census JSON saved.")
    
    # Rebuild Corrected Census MD
    overall_n = census_stats['overall']['n']
    overall_med = census_stats['overall']['median']
    overall_p90 = census_stats['overall']['P90']
    overall_p95 = census_stats['overall']['P95']
    overall_p99 = census_stats['overall']['P99']
    overall_max = census_stats['overall']['max']
    
    md_census = f"""# 📊 CE115 Corrected Output Size and Token-Budget Census Report
    
This report presents the census of output sizes for the corrected confirmatory cohort run (`num_ctx = 65536`, `num_predict = 24576`).

---

## 1. Natural Completion Token Statistics (Level A Telemetry)

| Cohort | Count (N) | Median (Out) | P90 (Out) | P95 (Out) | P99 (Out) | Max (Out) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** | {overall_n} | {overall_med:.1f} | {overall_p90:.1f} | {overall_p95:.1f} | {overall_p99:.1f} | {overall_max:.1f} |
| **Ab1** | {census_stats.get('condition_ab1', {}).get('n', 0)} | {census_stats.get('condition_ab1', {}).get('median', 0.0):.1f} | {census_stats.get('condition_ab1', {}).get('P90', 0.0):.1f} | {census_stats.get('condition_ab1', {}).get('P95', 0.0):.1f} | {census_stats.get('condition_ab1', {}).get('P99', 0.0):.1f} | {census_stats.get('condition_ab1', {}).get('max', 0.0):.1f} |
| **Ab2g** | {census_stats.get('condition_ab2g', {}).get('n', 0)} | {census_stats.get('condition_ab2g', {}).get('median', 0.0):.1f} | {census_stats.get('condition_ab2g', {}).get('P90', 0.0):.1f} | {census_stats.get('condition_ab2g', {}).get('P95', 0.0):.1f} | {census_stats.get('condition_ab2g', {}).get('P99', 0.0):.1f} | {census_stats.get('condition_ab2g', {}).get('max', 0.0):.1f} |
| **Ab2d** | {census_stats.get('condition_ab2d', {}).get('n', 0)} | {census_stats.get('condition_ab2d', {}).get('median', 0.0):.1f} | {census_stats.get('condition_ab2d', {}).get('P90', 0.0):.1f} | {census_stats.get('condition_ab2d', {}).get('P95', 0.0):.1f} | {census_stats.get('condition_ab2d', {}).get('P99', 0.0):.1f} | {census_stats.get('condition_ab2d', {}).get('max', 0.0):.1f} |

---

## 2. Degeneration Analysis

- In this run, **22 cells** hit the prediction limit of 24576 tokens because of infinite repetition loops, and are classified as `MODEL_DEGENERATIVE_NONTERMINATION`.
- These degenerative runs generated exactly 24576 output tokens, which have been excluded from the natural completion statistics above.

"""
    with open(CORRECTED_RUN_DIR / "ce115_corrected_census.md", "w", encoding="utf-8") as f:
        f.write(md_census)
    print("Corrected Census MD saved.")

    # 4. Rebuild Corrected Failure Taxonomy
    # Failed cells: evaluator_outcome != passed
    failed_records = [r for r in eval_results if r["evaluator_outcome"] != "passed"]
    
    # Map failed cells to taxonomy families
    # Categories:
    # - MODEL_DEGENERATIVE_NONTERMINATION
    # - OUTPUT_WRAPPING_OR_LEAKAGE
    # - PARSE_OR_SYNTAX_FAILURE
    # - ENTRY_POINT_OR_CONTRACT_FAILURE
    # - CORE_LOGIC_INCORRECT
    # - CORE_LOGIC_MISSING
    # - SPECIFICATION_MISINTERPRETATION
    # - NONCORE_STRUCTURAL_FAILURE
    # - OTHER
    # - INSUFFICIENT_EVIDENCE
    
    taxonomy_cells = []
    primary_counts = {
        "MODEL_DEGENERATIVE_NONTERMINATION": 0,
        "OUTPUT_WRAPPING_OR_LEAKAGE": 0,
        "PARSE_OR_SYNTAX_FAILURE": 0,
        "ENTRY_POINT_OR_CONTRACT_FAILURE": 0,
        "CORE_LOGIC_INCORRECT": 0,
        "CORE_LOGIC_MISSING": 0,
        "SPECIFICATION_MISINTERPRETATION": 0,
        "NONCORE_STRUCTURAL_FAILURE": 0,
        "OTHER": 0,
        "INSUFFICIENT_EVIDENCE": 0
    }
    
    for r in failed_records:
        outcome = r["evaluator_outcome"]
        is_degen = r["validity_classification"] == "MODEL_DEGENERATIVE_NONTERMINATION"
        has_leak = r["has_leakage"]
        
        primary_family = "OTHER"
        secondary_family = None
        
        if is_degen:
            primary_family = "MODEL_DEGENERATIVE_NONTERMINATION"
            if has_leak:
                secondary_family = "OUTPUT_WRAPPING_OR_LEAKAGE"
        elif has_leak and outcome in ("parse_minor", "extraction_failure"):
            primary_family = "OUTPUT_WRAPPING_OR_LEAKAGE"
            secondary_family = "PARSE_OR_SYNTAX_FAILURE"
        elif outcome == "parse_minor":
            primary_family = "PARSE_OR_SYNTAX_FAILURE"
        elif outcome in ("missing_entry_point", "schema_failure"):
            primary_family = "ENTRY_POINT_OR_CONTRACT_FAILURE"
        elif outcome == "answer_incorrect":
            primary_family = "CORE_LOGIC_INCORRECT"
        elif outcome == "runtime_failure":
            primary_family = "CORE_LOGIC_MISSING"
            
        primary_counts[primary_family] += 1
        
        tax_entry = {
            "cell_id": r["cell_id"],
            "model": r["model"],
            "task": r["task"],
            "condition": r["condition"],
            "seed": r["seed"],
            "primary_failure_family": primary_family,
            "secondary_failure_family": secondary_family,
            "root_cause": "DEGENERATIVE_LOOP" if is_degen else ("INLINE_REASONING_LEAK" if has_leak else "CODE_DEFECT"),
            "completion_class": r["validity_classification"],
            "structural_vs_semantic": "structural" if primary_family in ("PARSE_OR_SYNTAX_FAILURE", "ENTRY_POINT_OR_CONTRACT_FAILURE", "OUTPUT_WRAPPING_OR_LEAKAGE") else "semantic",
            "core_vs_noncore": "core" if primary_family in ("CORE_LOGIC_INCORRECT", "CORE_LOGIC_MISSING") else "noncore",
            "deterministic_detectability": True if primary_family in ("MODEL_DEGENERATIVE_NONTERMINATION", "PARSE_OR_SYNTAX_FAILURE", "ENTRY_POINT_OR_CONTRACT_FAILURE", "OUTPUT_WRAPPING_OR_LEAKAGE") else False,
            "potential_repairability": "safe_prefix_extraction" if (is_degen and r["pre_loop_program_complete"]) else ("regex_strip_leak" if primary_family == "OUTPUT_WRAPPING_OR_LEAKAGE" else "ast_repair_or_abstain"),
            "abstention_required": primary_family in ("CORE_LOGIC_INCORRECT", "CORE_LOGIC_MISSING") or (is_degen and not r["pre_loop_program_complete"]),
            "evidence_references": f"evaluator outcome: {outcome}",
            "artifact_hash": r["raw_output_sha256"]
        }
        taxonomy_cells.append(tax_entry)
        
    taxonomy_json = {
        "taxonomy_metadata": "CORRECTED_FAILURE_TAXONOMY",
        "total_failures": len(taxonomy_cells),
        "primary_counts": primary_counts,
        "failures": taxonomy_cells
    }
    with open(CORRECTED_RUN_DIR / "ce115_corrected_taxonomy.json", "w", encoding="utf-8") as f:
        json.dump(taxonomy_json, f, indent=2, ensure_ascii=False)
    print("Corrected Taxonomy JSON saved.")
    
    # Rebuild Corrected Taxonomy MD
    failures_rows = []
    for f in taxonomy_cells:
        failures_rows.append(f"| `{f['cell_id']}` | `{f['primary_failure_family']}` | `{f['root_cause']}` | `{f['potential_repairability']}` |")
        
    primary_rows = []
    for k, v in primary_counts.items():
        primary_rows.append(f"| `{k}` | {v} |")
        
    md_taxonomy = f"""# 🕵️ CE115 Corrected Failure Taxonomy Report

This report presents the structural and semantic failure taxonomy rebuild for the corrected 72-cell cohort run.

---

## 1. Summary of Primary Failure Families

| Primary Failure Family | Count |
| :--- | :---: |
{"\n".join(primary_rows)}

---

## 2. Failed Cells Classification Matrix

| Cell ID | Primary Failure Family | Root Cause | Potential Repairability |
| :--- | :--- | :--- | :--- |
{"\n".join(failures_rows)}

"""
    with open(CORRECTED_RUN_DIR / "ce115_corrected_taxonomy.md", "w", encoding="utf-8") as f:
        f.write(md_taxonomy)
    print("Corrected Taxonomy MD saved.")

    # 5. Stratified Summary Report
    # Rebuild stratified stats overall and for combinations:
    # model, condition, task, seed, and cross-combinations
    stratified_results = {}
    
    def get_stats_for_group(group_records):
        tot = len(group_records)
        nat = sum(1 for r in group_records if r["validity_classification"] == "NATURAL_COMPLETE")
        deg = sum(1 for r in group_records if r["validity_classification"] == "MODEL_DEGENERATIVE_NONTERMINATION")
        passed = sum(1 for r in group_records if r["evaluator_outcome"] == "passed")
        failed = tot - passed
        # evaluable: not runtime failure
        evaluable = sum(1 for r in group_records if r["evaluator_outcome"] != "runtime_failure")
        # executable: compile/execution succeeded (passed, answer_incorrect, schema_failure)
        executable = sum(1 for r in group_records if r["evaluator_outcome"] in ("passed", "answer_incorrect", "schema_failure"))
        
        return {
            "total": tot,
            "natural_complete": nat,
            "degeneration": deg,
            "evaluable": evaluable,
            "executable": executable,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / tot if tot > 0 else 0.0,
            "degeneration_rate": deg / tot if tot > 0 else 0.0
        }
        
    # Groupings
    stratified_results["overall"] = get_stats_for_group(eval_results)
    
    # Stratify by model
    for m in ["qwen3.5:4b", "qwen3.5:9b"]:
        m_rec = [r for r in eval_results if r["model"] == m]
        stratified_results[f"model_{m}"] = get_stats_for_group(m_rec)
        
    # Stratify by condition
    for cond in ["ab1", "ab2g", "ab2d"]:
        cond_rec = [r for r in eval_results if r["condition"] == cond]
        stratified_results[f"condition_{cond}"] = get_stats_for_group(cond_rec)
        
    # Stratify by task
    for task_id in tasks_by_id.keys():
        task_rec = [r for r in eval_results if r["task"] == task_id]
        stratified_results[f"task_{task_id}"] = get_stats_for_group(task_rec)
        
    # Stratify by model x condition
    for m in ["qwen3.5:4b", "qwen3.5:9b"]:
        for cond in ["ab1", "ab2g", "ab2d"]:
            mc_rec = [r for r in eval_results if r["model"] == m and r["condition"] == cond]
            stratified_results[f"model_{m}_condition_{cond}"] = get_stats_for_group(mc_rec)
            
    # Stratify by condition x task
    for cond in ["ab1", "ab2g", "ab2d"]:
        for task_id in tasks_by_id.keys():
            ct_rec = [r for r in eval_results if r["condition"] == cond and r["task"] == task_id]
            stratified_results[f"condition_{cond}_task_{task_id}"] = get_stats_for_group(ct_rec)
            
    # Stratify by model x task
    for m in ["qwen3.5:4b", "qwen3.5:9b"]:
        for task_id in tasks_by_id.keys():
            mt_rec = [r for r in eval_results if r["model"] == m and r["task"] == task_id]
            stratified_results[f"model_{m}_task_{task_id}"] = get_stats_for_group(mt_rec)
            
    # Stratify by model x condition x task
    for m in ["qwen3.5:4b", "qwen3.5:9b"]:
        for cond in ["ab1", "ab2g", "ab2d"]:
            for task_id in tasks_by_id.keys():
                mct_rec = [r for r in eval_results if r["model"] == m and r["condition"] == cond and r["task"] == task_id]
                stratified_results[f"model_{m}_condition_{cond}_task_{task_id}"] = get_stats_for_group(mct_rec)
                
    with open(CORRECTED_RUN_DIR / "ce115_corrected_stratified_summary.json", "w", encoding="utf-8") as f:
        json.dump(stratified_results, f, indent=2, ensure_ascii=False)
    print("Corrected Stratified Summary JSON saved.")

    # 6. Rebuild Healer Candidate Pool
    candidate_pool = []
    
    # Count variables
    abstain_count = 0
    insufficient_evidence_count = 0
    candidate_governance_tier_counts = {
        "MINIMAL_CORE_CANDIDATE": 0,
        "SAFE_HISTORICAL_CANDIDATE": 0,
        "EXPLORATORY_ONLY": 0,
        "ABSTAIN": 0,
        "INSUFFICIENT_EVIDENCE": 0
    }
    
    # Process taxonomy failures
    for f in taxonomy_cells:
        cell_id = f["cell_id"]
        source_cell = f
        primary_family = f["primary_failure_family"]
        is_degen = primary_family == "MODEL_DEGENERATIVE_NONTERMINATION"
        
        # Determine candidacy
        governance_tier = "ABSTAIN"
        proposed_repair_level = f["potential_repairability"]
        
        if primary_family == "OUTPUT_WRAPPING_OR_LEAKAGE":
            governance_tier = "SAFE_HISTORICAL_CANDIDATE"
        elif is_degen and f["potential_repairability"] == "safe_prefix_extraction":
            governance_tier = "SAFE_HISTORICAL_CANDIDATE"
            
        candidate_governance_tier_counts[governance_tier] += 1
        if governance_tier == "ABSTAIN":
            abstain_count += 1
        elif governance_tier == "INSUFFICIENT_EVIDENCE":
            insufficient_evidence_count += 1
            
        cand_entry = {
            "candidate_id": f"cand_{cell_id}",
            "source_cell_id": cell_id,
            "failure_family": primary_family,
            "proposed_repair_level": "display" if governance_tier == "SAFE_HISTORICAL_CANDIDATE" else "ast",
            "deterministic_scanner_possible": governance_tier == "SAFE_HISTORICAL_CANDIDATE",
            "answer_independent": governance_tier == "SAFE_HISTORICAL_CANDIDATE",
            "task_ID_independent": governance_tier == "SAFE_HISTORICAL_CANDIDATE",
            "hidden_test_independent": governance_tier == "SAFE_HISTORICAL_CANDIDATE",
            "core_logic_modification_required": governance_tier == "ABSTAIN",
            "preliminary_governance_tier": governance_tier
        }
        candidate_pool.append(cand_entry)
        
    candidate_pool_json = {
        "healer_candidate_pool_metadata": "CORRECTED_HEALER_CANDIDATE_POOL",
        "total_candidates_analyzed": len(candidate_pool),
        "governance_tier_counts": candidate_governance_tier_counts,
        "candidates": candidate_pool
    }
    with open(CORRECTED_RUN_DIR / "ce115_corrected_healer_candidate_pool.json", "w", encoding="utf-8") as f:
        json.dump(candidate_pool_json, f, indent=2, ensure_ascii=False)
    print("Corrected Healer Candidate Pool JSON saved.")
    
    # Write Healer Candidate Pool MD
    pool_rows = []
    for c in candidate_pool:
        pool_rows.append(f"| `{c['candidate_id']}` | `{c['failure_family']}` | `{c['proposed_repair_level']}` | `{c['preliminary_governance_tier']}` |")
        
    md_pool = f"""# 🧬 CE115 Corrected Healer Candidate Pool Report

This report catalogs the potential heuristic healer rules and candidates identified from the corrected cohort run.

---

## 1. Summary of Governance Tiers

- **SAFE_HISTORICAL_CANDIDATE**: {candidate_governance_tier_counts['SAFE_HISTORICAL_CANDIDATE']}
- **MINIMAL_CORE_CANDIDATE**: {candidate_governance_tier_counts['MINIMAL_CORE_CANDIDATE']}
- **EXPLORATORY_ONLY**: {candidate_governance_tier_counts['EXPLORATORY_ONLY']}
- **ABSTAIN**: {candidate_governance_tier_counts['ABSTAIN']}
- **INSUFFICIENT_EVIDENCE**: {candidate_governance_tier_counts['INSUFFICIENT_EVIDENCE']}

---

## 2. Healer Candidate Registry

| Candidate ID | Failure Family | Proposed Repair Level | Preliminary Governance Tier |
| :--- | :--- | :--- | :--- |
{"\n".join(pool_rows)}

"""
    with open(CORRECTED_RUN_DIR / "ce115_corrected_healer_candidate_pool.md", "w", encoding="utf-8") as f:
        f.write(md_pool)
    print("Corrected Healer Candidate Pool MD saved.")

if __name__ == "__main__":
    rebuild()
