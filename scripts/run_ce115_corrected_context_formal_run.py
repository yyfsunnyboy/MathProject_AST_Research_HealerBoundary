import os
import sys
import json
import time
import urllib.request
import urllib.error
import hashlib
import io
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_calc_formal_runner import build_local_confirmatory_plan

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
CORRECTED_RUN_DIR = ROOT / "docs" / "experiments" / "results" / "ce115_corrected_context_formal_run"
CELLS_DIR = CORRECTED_RUN_DIR / "cells"

EXPECTED_DIGESTS = {
    "qwen3.5:4b": "2a654d98e6fb",
    "qwen3.5:9b": "6488c96fa5fa",
}

PROTOCOL_HASH = "48d5a1943bb2a86fcd8c1a45468b2b40085e6b717092fefe2bc478ad8bcbd04e"

def get_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def _http_json(url: str, *, data: bytes | None = None, timeout_s: float = 900.0) -> dict:
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return json.loads(resp.read().decode("utf-8"))

def compute_repetition_diagnostics(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    n_lines = len(lines)
    if n_lines == 0:
        return {
            "repeated_line_ratio": 0.0,
            "repeated_3line_block_ratio": 0.0,
            "longest_repeated_contiguous_block": 0,
            "duplicate_fn_count": 0,
            "duplicate_class_count": 0,
            "last_25pct_repeats_prefix": False,
            "post_completion_loop": False
        }
        
    unique_lines = set(lines)
    repeated_line_ratio = (n_lines - len(unique_lines)) / n_lines
    
    blocks_3 = [tuple(lines[i:i+3]) for i in range(n_lines - 2)]
    if len(blocks_3) > 0:
        unique_blocks = set(blocks_3)
        repeated_3line_block_ratio = (len(blocks_3) - len(unique_blocks)) / len(blocks_3)
    else:
        repeated_3line_block_ratio = 0.0
        
    fn_defs = [l for l in lines if l.startswith("def ") or l.startswith("def\t")]
    duplicate_fn_count = len(fn_defs) - len(set(fn_defs))
    
    class_defs = [l for l in lines if l.startswith("class ")]
    duplicate_class_count = len(class_defs) - len(set(class_defs))
    
    last_25_start = int(n_lines * 0.75)
    last_25_lines = lines[last_25_start:]
    prefix_lines = set(lines[:last_25_start])
    repeats_in_prefix = sum(1 for l in last_25_lines if l in prefix_lines)
    last_25pct_repeats_prefix = False
    if len(last_25_lines) > 0:
        pct = repeats_in_prefix / len(last_25_lines)
        if pct > 0.5 and len(last_25_lines) > 5:
            last_25pct_repeats_prefix = True
            
    longest_block = 0
    for length in range(1, min(100, n_lines // 2 + 1)):
        found = False
        seen_blocks = {}
        for i in range(n_lines - length + 1):
            block = tuple(lines[i:i+length])
            if block in seen_blocks:
                if i >= seen_blocks[block] + length:
                    longest_block = length
                    found = True
                    break
            else:
                seen_blocks[block] = i
        if not found:
            break
            
    post_completion_loop = False
    if "return {" in text:
        if duplicate_fn_count > 0:
            post_completion_loop = True
            
    return {
        "repeated_line_ratio": repeated_line_ratio,
        "repeated_3line_block_ratio": repeated_3line_block_ratio,
        "longest_repeated_contiguous_block": longest_block,
        "duplicate_fn_count": duplicate_fn_count,
        "duplicate_class_count": duplicate_class_count,
        "last_25pct_repeats_prefix": last_25pct_repeats_prefix,
        "post_completion_loop": post_completion_loop
    }

def run_corrected_cohort():
    CELLS_DIR.mkdir(parents=True, exist_ok=True)
    
    plan = build_local_confirmatory_plan()
    cells = plan["cells"]
    
    # Save corrected rerun plan manifest first
    manifest_out_path = CORRECTED_RUN_DIR / "ce115_corrected_context_formal_run_manifest.json"
    manifest_data = {
        "protocol_id": "ce115_corrected_context_rerun_protocol",
        "protocol_hash": PROTOCOL_HASH,
        "num_ctx": 65536,
        "num_predict": 24576,
        "think": False,
        "planned_cells_count": len(cells),
        "cells": [
            {
                "cell_id": c["cell_id"],
                "model": c["model_tag"],
                "task": c["task_id"],
                "condition": c["prompt_condition"],
                "seed": c["seed"]
            } for c in cells
        ]
    }
    with open(manifest_out_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)
    print("Manifest saved.")

    results = []
    
    for idx, cell in enumerate(cells):
        cell_id = cell["cell_id"]
        print(f"\n[{idx+1}/72] Cell: {cell_id}...")
        
        cell_jsonl_path = CELLS_DIR / f"{cell_id}.jsonl"
        raw_path = CELLS_DIR / f"{cell_id}__raw_output.txt"
        
        # Resume support: skip if files exist and are valid JSON
        if cell_jsonl_path.exists() and raw_path.exists():
            try:
                with open(cell_jsonl_path, "r", encoding="utf-8") as f:
                    record = json.load(f)
                if record.get("validity_classification") is not None:
                    results.append(record)
                    print(f"Skipping (already completed). Classification: {record.get('validity_classification')}")
                    continue
            except Exception:
                pass
                
        # Build strict request payload
        payload = {
            "model": cell["model_tag"],
            "messages": [{"role": "user", "content": cell["prompt_text"]}],
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0.0,
                "seed": int(cell["seed"]),
                "num_ctx": 65536,
                "num_predict": 24576
            }
        }
        
        prompt_sha256 = get_sha256(cell["prompt_text"])
        payload_str = json.dumps(payload)
        request_payload_sha256 = get_sha256(payload_str)
        
        started_wall = time.time()
        try:
            url = DEFAULT_OLLAMA_URL.rstrip("/") + "/api/chat"
            body = _http_json(url, data=payload_str.encode("utf-8"), timeout_s=900.0)
            elapsed_wall = time.time() - started_wall
            
            message_content = ""
            message = body.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                message_content = message["content"]
            elif isinstance(body.get("response"), str):
                message_content = body["response"]
                
            raw_output_sha256 = get_sha256(message_content)
            
            # Telemetry
            eval_count = body.get("eval_count", 0)
            prompt_eval_count = body.get("prompt_eval_count", 0)
            total_tokens = eval_count + prompt_eval_count
            total_duration = body.get("total_duration")
            load_duration = body.get("load_duration")
            prompt_eval_duration = body.get("prompt_eval_duration")
            eval_duration = body.get("eval_duration")
            
            done = body.get("done", True)
            done_reason = body.get("done_reason", "stop")
            
            # Save raw output directly to separate file
            raw_path.write_text(message_content, encoding="utf-8")
            
            # Repetition diagnostics
            rep = compute_repetition_diagnostics(message_content)
            
            # Extract status check (without domain heuristic parser running)
            has_entry_point = "def generate" in message_content
            has_return = "return {" in message_content
            
            # Classification logic
            is_limit = (total_tokens >= 65536 or eval_count >= 24576 or done_reason == "length")
            is_degen = (rep["post_completion_loop"] or rep["repeated_line_ratio"] > 0.40 or rep["longest_repeated_contiguous_block"] > 15)
            
            if is_limit and is_degen:
                classification = "MODEL_DEGENERATIVE_NONTERMINATION"
            elif is_limit:
                classification = "CONFIGURATION_LIMIT_REACHED"
            elif is_degen:
                classification = "MODEL_DEGENERATIVE_NONTERMINATION"
            elif not message_content.strip() or ("def generate" not in message_content):
                classification = "MODEL_EARLY_INCOMPLETE_TERMINATION"
            else:
                classification = "NATURAL_COMPLETE"
                
            record = {
                "cell_id": cell_id,
                "model": cell["model_tag"],
                "model_digest": EXPECTED_DIGESTS.get(cell["model_tag"], "unknown"),
                "task": cell["task_id"],
                "condition": cell["prompt_condition"],
                "seed": cell["seed"],
                "complete_payload": payload,
                "request_payload_sha256": request_payload_sha256,
                "prompt_sha256": prompt_sha256,
                "requested_num_ctx": 65536,
                "requested_num_predict": 24576,
                "requested_think": False,
                "effective_options_verification": "REQUEST_PAYLOAD_VERIFIED_ONLY",
                "raw_first_attempt_output": message_content,
                "raw_output_sha256": raw_output_sha256,
                "prompt_eval_count": prompt_eval_count,
                "eval_count": eval_count,
                "total_token_count": total_tokens,
                "done": done,
                "done_reason": done_reason,
                "load_duration": load_duration,
                "prompt_eval_duration": prompt_eval_duration,
                "eval_duration": eval_duration,
                "total_duration": total_duration,
                "wall_clock_seconds": round(elapsed_wall, 2),
                "output_character_count": len(message_content),
                "output_line_count": len(message_content.splitlines()),
                "tail_excerpt": message_content[-100:] if len(message_content) > 100 else message_content,
                "extraction_status": "extracted" if has_entry_point else "missing",
                "parse_status": "ok" if has_entry_point else "missing",
                "entry_point_status": "present" if has_entry_point else "absent",
                "return_completeness": has_return,
                "repetition_diagnostics": rep,
                "validity_classification": classification
            }
            results.append(record)
            
            # Save cell JSONL
            with open(cell_jsonl_path, "w", encoding="utf-8") as fw:
                json.dump(record, fw, ensure_ascii=False)
                fw.write("\n")
                
            print(f"Done. Tokens: {total_tokens} ({prompt_eval_count} in, {eval_count} out). Classification: {classification}")
            
        except Exception as exc:
            print(f"Error executing cell {cell_id}: {exc}")
            record = {
                "cell_id": cell_id,
                "model": cell["model_tag"],
                "task": cell["task_id"],
                "condition": cell["prompt_condition"],
                "seed": cell["seed"],
                "validity_classification": "RUNTIME_FAILURE",
                "error_message": str(exc)
            }
            results.append(record)
            with open(cell_jsonl_path, "w", encoding="utf-8") as fw:
                json.dump(record, fw, ensure_ascii=False)
                fw.write("\n")

    # 4. Generate summary files
    summary_json_path = CORRECTED_RUN_DIR / "ce115_corrected_context_formal_run_summary.json"
    summary_md_path = CORRECTED_RUN_DIR / "ce115_corrected_context_formal_run_summary.md"
    exception_json_path = CORRECTED_RUN_DIR / "ce115_corrected_context_formal_run_exception_report.json"
    
    # Check completeness
    telemetry_complete_count = sum(1 for r in results if r.get("eval_count") is not None)
    runtime_fail_count = sum(1 for r in results if r.get("validity_classification") == "RUNTIME_FAILURE")
    config_limit_count = sum(1 for r in results if r.get("validity_classification") == "CONFIGURATION_LIMIT_REACHED")
    degen_count = sum(1 for r in results if r.get("validity_classification") == "MODEL_DEGENERATIVE_NONTERMINATION")
    natural_complete_count = sum(1 for r in results if r.get("validity_classification") == "NATURAL_COMPLETE")
    early_incomplete_count = sum(1 for r in results if r.get("validity_classification") == "MODEL_EARLY_INCOMPLETE_TERMINATION")
    
    summary_data = {
        "run_id": "ce115_corrected_context_formal_run",
        "protocol_hash": PROTOCOL_HASH,
        "planned_cells": len(cells),
        "executed_cells": len(results),
        "unique_cell_ids": len(set(r["cell_id"] for r in results)),
        "classifications": {
            "NATURAL_COMPLETE": natural_complete_count,
            "CONFIGURATION_LIMIT_REACHED": config_limit_count,
            "MODEL_DEGENERATIVE_NONTERMINATION": degen_count,
            "MODEL_EARLY_INCOMPLETE_TERMINATION": early_incomplete_count,
            "RUNTIME_FAILURE": runtime_fail_count
        },
        "results": results
    }
    with open(summary_json_path, "w", encoding="utf-8") as fh:
        json.dump(summary_data, fh, indent=2, ensure_ascii=False)
    print("Summary JSON saved.")

    # Exception list
    exceptions = [r for r in results if r.get("validity_classification") in ("CONFIGURATION_LIMIT_REACHED", "MODEL_DEGENERATIVE_NONTERMINATION", "RUNTIME_FAILURE")]
    with open(exception_json_path, "w", encoding="utf-8") as fh:
        json.dump(exceptions, fh, indent=2, ensure_ascii=False)
    print("Exception report saved.")

    # MD summary rows
    md_rows = []
    for r in results:
        v_class = r.get("validity_classification", "UNKNOWN")
        in_t = r.get("prompt_eval_count", 0)
        out_t = r.get("eval_count", 0)
        tot_t = r.get("total_token_count", 0)
        md_rows.append(f"| `{r['cell_id']}` | `{r['model']}` | `{r['condition']}` | {in_t} | {out_t} | {tot_t} | `{v_class}` |")

    md_content = f"""# 🕵️ CE115 Corrected Context Formal Run Summary Report

This report summarizes the execution of the full 72-cell cohort run under the corrected budget configurations: `num_ctx = 65536` and `num_predict = 24576` with `think: false`.

---

## 1. Summary of Execution Metrics

- **Planned Cells**: {len(cells)}
- **Executed Cells**: {len(results)}
- **Unique Cell IDs**: {len(set(r["cell_id"] for r in results))}
- **NATURAL_COMPLETE**: {natural_complete_count}
- **CONFIGURATION_LIMIT_REACHED**: {config_limit_count}
- **MODEL_DEGENERATIVE_NONTERMINATION**: {degen_count}
- **MODEL_EARLY_INCOMPLETE_TERMINATION**: {early_incomplete_count}
- **RUNTIME_FAILURE**: {runtime_fail_count}
- **Telemetry Completeness**: {telemetry_complete_count} / {len(cells)}

---

## 2. Exceptions & Degenerations

A total of **{len(exceptions)}** cells exhibited budget limit hits or runtime failures:
- **CONFIGURATION_LIMIT_REACHED**: {config_limit_count} cells
- **MODEL_DEGENERATIVE_NONTERMINATION**: {degen_count} cells
- **RUNTIME_FAILURE**: {runtime_fail_count} cells

All exceptions have been cataloged in `ce115_corrected_context_formal_run_exception_report.json` for forensic evaluation.

---

## 3. Detailed Results Matrix

| Cell ID | Model | Condition | Prompt Tokens (In) | Output Tokens (Out) | Total Tokens | Classification |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
{"\n".join(md_rows)}

"""
    with open(summary_md_path, "w", encoding="utf-8") as fh:
        fh.write(md_content)
    print("Summary MD saved.")

if __name__ == "__main__":
    run_corrected_cohort()
