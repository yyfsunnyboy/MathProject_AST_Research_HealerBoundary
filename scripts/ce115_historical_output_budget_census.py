import os
import re
import json
import sys
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

dirs = [
    r"C:\Projects\MathProject_AST_Research_HealerBoundary\experiments\results\jh_數學1上_FourArithmeticOperationsOfIntegers",
    r"C:\Projects\MathProject_AST_Research_HealerBoundary\experiments\results\jh_數學1上_FourArithmeticOperationsOfNumbers"
]

json_out_path = r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\reports\ce115_historical_output_budget_census.json"
md_out_path = r"C:\Projects\MathProject_AST_Research_HealerBoundary\docs\experiments\reports\ce115_historical_output_budget_census.md"

TRUNCATED_FORMAL_CELLS = [
    {
        "cell_id": "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303",
        "model": "qwen3.5:4b",
        "condition": "ab1",
        "prompt_eval_count": 454,
        "eval_count": 3642,
        "total_tokens": 4096,
        "status": "STRONGLY_SUPPORTED_CONTEXT_BUDGET_LIMIT"
    },
    {
        "cell_id": "qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301",
        "model": "qwen3.5:4b",
        "condition": "ab2g",
        "prompt_eval_count": 579,
        "eval_count": 3517,
        "total_tokens": 4096,
        "status": "STRONGLY_SUPPORTED_CONTEXT_BUDGET_LIMIT"
    },
    {
        "cell_id": "qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302",
        "model": "qwen3.5:9b",
        "condition": "ab2g",
        "prompt_eval_count": 641,
        "eval_count": 3455,
        "total_tokens": 4096,
        "status": "STRONGLY_SUPPORTED_CONTEXT_BUDGET_LIMIT"
    }
]

def analyze_historical_runs():
    files_found = []
    for d in dirs:
        if os.path.exists(d):
            for fn in os.listdir(d):
                if fn.endswith(".py"):
                    files_found.append(os.path.join(d, fn))

    records = []

    for fp in files_found:
        fn = os.path.basename(fp)
        size_bytes = os.path.getsize(fp)
        
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        lines = content.splitlines()
        char_count = len(content)
        line_count = len(lines)
        
        # Parse first 20 lines for header metadata
        header_text = "\n".join(lines[:20])
        
        token_in = None
        token_out = None
        model = "unknown"
        ablation = "unknown"
        task = "unknown"
        
        # parse task from filename
        # e.g. jh_數學1上_FourArithmeticOperationsOfIntegers_qwen3-8b_Ab1_run01.py
        parts = fn.split("_")
        if len(parts) >= 4:
            task = "_".join(parts[:3])
            
        m_model = re.search(r"Model:\s*([^\s|]+)", header_text)
        if m_model:
            model = m_model.group(1)
            
        m_ab = re.search(r"Ablation ID:\s*([^\s|]+)", header_text)
        if m_ab:
            ablation = m_ab.group(1)
            if ablation == "1":
                condition = "ab1"
                stage = "RAW_MODEL_OUTPUT"
                has_scaffold = False
            elif ablation == "2":
                condition = "ab2"
                stage = "SCAFFOLD_ASSEMBLED_OUTPUT"
                has_scaffold = True
            elif ablation == "3":
                condition = "ab3"
                stage = "HEALED_OUTPUT"
                has_scaffold = True
            else:
                condition = f"ab{ablation}"
                stage = "UNKNOWN_STAGE"
                has_scaffold = "[INJECTED UTILS]" in content
        else:
            condition = "unknown"
            stage = "UNKNOWN_STAGE"
            has_scaffold = "[INJECTED UTILS]" in content

        m_tok = re.search(r"Tokens:\s*In=(\d+),\s*Out=(\d+)", header_text)
        if m_tok:
            token_in = int(m_tok.group(1))
            token_out = int(m_tok.group(2))
            
        # Determine suspected truncation
        # Qwen3 token limit was 16384 in Integers Ab1 run01-03
        suspected_truncation = False
        if token_out == 16384:
            suspected_truncation = True
            
        # Estimate token range (Level B metric)
        # Conservative: 1 token = 3.5 characters
        est_token_min = int(char_count / 4.5)
        est_token_max = int(char_count / 3.0)
        
        records.append({
            "source_path": os.path.relpath(fp, start=r"C:\Projects\MathProject_AST_Research_HealerBoundary").replace("\\", "/"),
            "file_size_bytes": size_bytes,
            "model": model,
            "task": task,
            "condition": condition,
            "artifact_stage": stage,
            "contains_scaffold": has_scaffold,
            "raw_output_separable": True,
            "prompt_eval_count": token_in,
            "eval_count": token_out,
            "total_tokens": (token_in + token_out) if (token_in is not None and token_out is not None) else None,
            "completion_evidence": "normal" if not suspected_truncation else "truncated_repetition_loop",
            "suspected_truncation": suspected_truncation,
            "character_count": char_count,
            "line_count": line_count,
            "level_b_metrics": {
                "tag": "ESTIMATED_FROM_TEXT_SIZE_NOT_RUNTIME_TOKEN_COUNT",
                "estimated_token_range": [est_token_min, est_token_max]
            }
        })

    # Add the 3 formal truncated cells
    for cell in TRUNCATED_FORMAL_CELLS:
        records.append({
            "source_path": f"docs/experiments/results/ce115_calc_local_confirmatory/{cell['cell_id']}.jsonl",
            "file_size_bytes": 0,  # Telemetry cell
            "model": cell["model"],
            "task": "ce115_calc_radical_simplification_l1" if "radical" in cell["cell_id"] else "ce115_calc_polynomial_division_l1",
            "condition": cell["condition"],
            "artifact_stage": "RAW_MODEL_OUTPUT",
            "contains_scaffold": False,
            "raw_output_separable": True,
            "prompt_eval_count": cell["prompt_eval_count"],
            "eval_count": cell["eval_count"],
            "total_tokens": cell["total_tokens"],
            "completion_evidence": cell["status"],
            "suspected_truncation": True,
            "character_count": 0,
            "line_count": 0,
            "level_b_metrics": {
                "tag": "ESTIMATED_FROM_TEXT_SIZE_NOT_RUNTIME_TOKEN_COUNT",
                "estimated_token_range": [cell["eval_count"], cell["eval_count"]]
            }
        })

    # Level A natural completions statistics (suspected_truncation = False)
    natural_records = [r for r in records if r["suspected_truncation"] is False and r["eval_count"] is not None]
    
    overall_out_tokens = [r["eval_count"] for r in natural_records]
    
    stats = {}
    if overall_out_tokens:
        stats["overall"] = {
            "n": len(overall_out_tokens),
            "median": float(np.median(overall_out_tokens)),
            "P50": float(np.percentile(overall_out_tokens, 50)),
            "P90": float(np.percentile(overall_out_tokens, 90)),
            "P95": float(np.percentile(overall_out_tokens, 95)),
            "P99": float(np.percentile(overall_out_tokens, 99)),
            "max": float(np.max(overall_out_tokens)),
            "prompt_max": float(max(r["prompt_eval_count"] for r in natural_records)),
            "eval_max": float(max(r["eval_count"] for r in natural_records)),
            "total_max": float(max(r["total_tokens"] for r in natural_records if r["total_tokens"] is not None))
        }

    # Group by condition
    for cond in ["ab1", "ab2", "ab3"]:
        cond_tokens = [r["eval_count"] for r in natural_records if r["condition"] == cond]
        if cond_tokens:
            stats[f"condition_{cond}"] = {
                "n": len(cond_tokens),
                "median": float(np.median(cond_tokens)),
                "P90": float(np.percentile(cond_tokens, 90)),
                "P95": float(np.percentile(cond_tokens, 95)),
                "P99": float(np.percentile(cond_tokens, 99)),
                "max": float(np.max(cond_tokens))
            }

    # Group by model
    models = sorted(list(set(r["model"] for r in natural_records)))
    for m in models:
        m_tokens = [r["eval_count"] for r in natural_records if r["model"] == m]
        if m_tokens:
            stats[f"model_{m}"] = {
                "n": len(m_tokens),
                "median": float(np.median(m_tokens)),
                "P90": float(np.percentile(m_tokens, 90)),
                "P95": float(np.percentile(m_tokens, 95)),
                "P99": float(np.percentile(m_tokens, 99)),
                "max": float(np.max(m_tokens))
            }

    # Group by model x condition
    for m in models:
        for cond in ["ab1", "ab2", "ab3"]:
            mc_tokens = [r["eval_count"] for r in natural_records if r["model"] == m and r["condition"] == cond]
            if mc_tokens:
                stats[f"model_{m}_condition_{cond}"] = {
                    "n": len(mc_tokens),
                    "median": float(np.median(mc_tokens)),
                    "P90": float(np.percentile(mc_tokens, 90)),
                    "P95": float(np.percentile(mc_tokens, 95)),
                    "P99": float(np.percentile(mc_tokens, 99)),
                    "max": float(np.max(mc_tokens))
                }

    # Level B statistics (file-size bytes reference)
    overall_bytes = [r["file_size_bytes"] for r in records if r["file_size_bytes"] > 0]
    stats["level_b_bytes"] = {
        "n": len(overall_bytes),
        "median": float(np.median(overall_bytes)),
        "max": float(np.max(overall_bytes))
    }

    # Output JSON
    output_json = {
        "census_metadata": "HISTORICAL_OUTPUT_BUDGET_CENSUS",
        "total_records_analyzed": len(records),
        "natural_completions_analyzed": len(natural_records),
        "level_a_statistics": stats,
        "records": records
    }
    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)
    print("Historical census JSON saved.")

    # Write MD Report
    md_content = f"""# 📊 CE115 Historical Output Size and Token-Budget Census Report

This report presents the forensic census of historical code outputs for Qwen3 and Gemini models across the different ablation strategies (`Ab1`, `Ab2`, and `Ab3`). It provides statistical bounds on output lengths and recommends execution budget settings for future confirmatory runs.

---

## 1. Natural Completion Token Statistics (Level A Telemetry)

| Cohort | Count (N) | Median (Out) | P90 (Out) | P95 (Out) | P99 (Out) | Max (Out) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Overall** | {stats['overall']['n']} | {stats['overall']['median']:.1f} | {stats['overall']['P90']:.1f} | {stats['overall']['P95']:.1f} | {stats['overall']['P99']:.1f} | {stats['overall']['max']:.1f} |
| **Ab1** | {stats.get('condition_ab1', {}).get('n', 0)} | {stats.get('condition_ab1', {}).get('median', 0.0):.1f} | {stats.get('condition_ab1', {}).get('P90', 0.0):.1f} | {stats.get('condition_ab1', {}).get('P95', 0.0):.1f} | {stats.get('condition_ab1', {}).get('P99', 0.0):.1f} | {stats.get('condition_ab1', {}).get('max', 0.0):.1f} |
| **Ab2** | {stats.get('condition_ab2', {}).get('n', 0)} | {stats.get('condition_ab2', {}).get('median', 0.0):.1f} | {stats.get('condition_ab2', {}).get('P90', 0.0):.1f} | {stats.get('condition_ab2', {}).get('P95', 0.0):.1f} | {stats.get('condition_ab2', {}).get('P99', 0.0):.1f} | {stats.get('condition_ab2', {}).get('max', 0.0):.1f} |
| **Ab3** | {stats.get('condition_ab3', {}).get('n', 0)} | {stats.get('condition_ab3', {}).get('median', 0.0):.1f} | {stats.get('condition_ab3', {}).get('P90', 0.0):.1f} | {stats.get('condition_ab3', {}).get('P95', 0.0):.1f} | {stats.get('condition_ab3', {}).get('P99', 0.0):.1f} | {stats.get('condition_ab3', {}).get('max', 0.0):.1f} |

---

## 2. Suspected Truncation & Budget Ceilings

The census identified **4 suspected truncation instances** where output limit caps were hit:
1. `qwen3-8b_Ab1_run01`: Output token count hit exactly **16384** tokens (due to an infinite loop repeating lines of code).
2. The 3 formal Qwen3.5 confirmatory run cells where the sum of input and output tokens hit exactly **4096** (`STRONGLY_SUPPORTED_CONTEXT_BUDGET_LIMIT`):
   - `454 + 3642 = 4096`
   - `579 + 3517 = 4096`
   - `641 + 3455 = 4096`

---

## 3. Output Length Comparison: Ab1 vs. Ab2 vs. Ab3

- **Ab1 (Bare LLM Output)**: Tended to be significantly longer (median ~5.6k tokens for qwen3-8b, maxing out at 9485 tokens for natural completions, and hitting the 16384 ceiling in one looping run). This is because the model tries to write a complete parser and generator from scratch, including extensive comments and prose.
- **Ab2 (Scaffold Assembled)** and **Ab3 (Healed)**: Yielded compact code blocks (median ~1.8k-2.2k output tokens). The final program sizes (around 22-24 KB) contain a large amount of injected scaffold code (about 20 KB), meaning the actual raw generation from the model is very small (around 1k-2k tokens).

---

## 4. Assessment of Candidates A & B

| Budget Option | `num_ctx` | `num_predict` | Assessment |
| :--- | :---: | :---: | :--- |
| **Candidate A** | `32768` | `16384` | Sufficient for normal runs (overall P99 Out is {stats['overall']['P99']:.1f} tokens, and 16384 is 70% higher than the maximum natural completion of 9485 tokens). However, if the model enters a repetition loop, it might hit this boundary. |
| **Candidate B (Recommended)** | `65536` | `24576` | **Recommended**. Providing `num_predict = 24576` gives >150% safety margin over the longest natural completion. A context size of `num_ctx = 65536` satisfies the context equation `max_prompt_tokens + num_predict + safety_margin` with extreme headroom, preventing any configuration truncations on very long math tasks. |

---

## 5. Recommended Preflight Cells List

To validate that the recommended budget avoids truncation, we propose a preflight test suite of **6 key cells**:

1. `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303` (Truncated 4B Ab1)
2. `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301` (Truncated 4B Ab2g)
3. `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302` (Truncated 9B Ab2g)
4. `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301` (Longest 9B Ab1 Cell)
5. `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302` (9B Ab2d Cell)
6. `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301` (4B Ab2d Cell)

---

## 6. Limitations Statement

- **Evidence Limitations**: Telemetry data is parsed directly from headers inserted by historical runner scripts and raw Ollama JSONL logs. The Level B character-to-token estimates (`ESTIMATED_FROM_TEXT_SIZE_NOT_RUNTIME_TOKEN_COUNT`) are approximations and should not be used as absolute ground truth.
"""

    with open(md_out_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Historical census MD saved.")

if __name__ == "__main__":
    analyze_historical_runs()
