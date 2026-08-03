"""Zero-model preflight for Math16 Ab2d V2.

For all 32 frozen V2 prompt files:
  - extract every ```python fence and ast.parse() it (0 syntax errors expected)
For the shared per-domain "Generic domain code example" fence and the 16 full-plan
"Task-specific scaffold" fences specifically:
  - execute them locally (no model call) against each task's real frozen_literal
  - check the exact 3-key schema and oracle_payload == frozen_params
  - check the computed correct_answer against the real oracle evaluator (is_correct)
Domain-menu's per-task runtime-skeleton fence intentionally contains `...` placeholders
and is not executed (syntax-checked only) -- this is by design, mirroring what domain-menu
withholds from the model.

Writes docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_zero_model_preflight.{json,md}
"""
from __future__ import annotations

import ast
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_ab2d_v2_scaffolds import TASK_SCAFFOLDS_V2  # noqa: E402
from agent_tools.finals_rebuild.math16_pool import build_pool_tasks  # noqa: E402
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle  # noqa: E402
from core.prompts.domain_function_library import (  # noqa: E402
    FractionOps,
    IntegerOps,
    PolynomialOps,
    RadicalOps,
)

MENU_DIR = ROOT / "docs/experiments/prompts/ab2d_domain_menu_v2/prompts"
FULL_DIR = ROOT / "docs/experiments/prompts/ab2d_full_v2/prompts"
OUT_JSON = ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_zero_model_preflight.json"
OUT_MD = ROOT / "docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_zero_model_preflight.md"

EXEC_NS = {
    "IntegerOps": IntegerOps, "FractionOps": FractionOps,
    "RadicalOps": RadicalOps, "PolynomialOps": PolynomialOps,
    "Fraction": Fraction,
}

FENCE_RE = re.compile(r"```python\n(.*?)```", re.S)


def _all_fences(text: str) -> list[str]:
    return FENCE_RE.findall(text)


def _ast_parse_all_fences(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fences = _all_fences(text)
    results = []
    for i, code in enumerate(fences):
        try:
            ast.parse(code)
            results.append({"fence_index": i, "parse_ok": True, "error": None})
        except SyntaxError as exc:
            results.append({"fence_index": i, "parse_ok": False, "error": str(exc)})
    return {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "n_fences": len(fences), "fences": results}


def _execute_last_fence_as_generate(path: Path, task: dict) -> dict:
    text = path.read_text(encoding="utf-8")
    fences = _all_fences(text)
    code = fences[-1]
    ns = dict(EXEC_NS)
    out = {"path": str(path.relative_to(ROOT)).replace("\\", "/")}
    try:
        exec(compile(code, f"<{task['task_id']}>", "exec"), ns)
        value = ns["generate"]()
    except Exception as exc:  # noqa: BLE001
        out.update(execution_ok=False, error=f"{type(exc).__name__}: {exc}")
        return out
    out["execution_ok"] = True
    out["schema_ok"] = set(value) == {"question_text", "correct_answer", "oracle_payload"}
    out["oracle_payload_equals_frozen"] = value.get("oracle_payload") == task["frozen_params"]
    result = evaluate_math_task_oracle(task["oracle_type"], task["oracle_payload"], value.get("correct_answer"))
    out["answer_correct"] = bool(result.get("is_correct"))
    out["oracle_result"] = result
    return out


def main() -> dict:
    tasks = {t["task_id"]: t for t in build_pool_tasks()}
    all_files = sorted(MENU_DIR.glob("*.txt")) + sorted(FULL_DIR.glob("*.txt"))

    parse_rows = [_ast_parse_all_fences(p) for p in all_files]
    n_fences_total = sum(r["n_fences"] for r in parse_rows)
    n_parse_fail = sum(1 for r in parse_rows for f in r["fences"] if not f["parse_ok"])

    exec_rows = []
    for task_id, task in tasks.items():
        exec_rows.append(_execute_last_fence_as_generate(FULL_DIR / f"{task_id}.txt", task))

    n_exec_fail = sum(1 for r in exec_rows if not r.get("execution_ok"))
    n_schema_fail = sum(1 for r in exec_rows if r.get("execution_ok") and not r.get("schema_ok"))
    n_oracle_payload_fail = sum(
        1 for r in exec_rows if r.get("execution_ok") and not r.get("oracle_payload_equals_frozen")
    )
    n_answer_wrong = sum(1 for r in exec_rows if r.get("execution_ok") and not r.get("answer_correct"))

    result = {
        "experiment_id": "math16_ab2d_menu_vs_full_runtime_contract_v2",
        "n_prompt_files": len(all_files),
        "n_code_fences_total": n_fences_total,
        "n_ast_parse_failures": n_parse_fail,
        "n_full_plan_scaffolds_executed": len(exec_rows),
        "n_execution_failures": n_exec_fail,
        "n_schema_failures": n_schema_fail,
        "n_oracle_payload_mismatches": n_oracle_payload_fail,
        "n_answers_incorrect": n_answer_wrong,
        "parse_rows": parse_rows,
        "execution_rows": exec_rows,
    }
    result["overall_pass"] = (
        n_parse_fail == 0
        and n_exec_fail == 0
        and n_schema_fail == 0
        and n_oracle_payload_fail == 0
        and n_answer_wrong == 0
    )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    md_lines = [
        "# Math16 Ab2d V2 -- zero-model preflight",
        "",
        f"- prompt files scanned: {result['n_prompt_files']}",
        f"- code fences AST-parsed: {n_fences_total}, failures: **{n_parse_fail}**",
        f"- full-plan scaffolds executed locally: {len(exec_rows)}",
        f"- execution failures: **{n_exec_fail}**",
        f"- schema failures (not exactly 3 keys): **{n_schema_fail}**",
        f"- oracle_payload mismatches: **{n_oracle_payload_fail}**",
        f"- answers objectively incorrect (per oracle evaluator): **{n_answer_wrong}**",
        f"- overall_pass: **{result['overall_pass']}**",
        "",
        "| task_id | execution_ok | schema_ok | oracle_payload_ok | answer_correct |",
        "|---|---|---|---|---|",
    ]
    for r, tid in zip(exec_rows, tasks.keys()):
        md_lines.append(
            f"| {tid} | {r.get('execution_ok')} | {r.get('schema_ok')} | "
            f"{r.get('oracle_payload_equals_frozen')} | {r.get('answer_correct')} |"
        )
    OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8", newline="\n")
    return result


if __name__ == "__main__":
    r = main()
    print(json.dumps({k: r[k] for k in (
        "n_prompt_files", "n_code_fences_total", "n_ast_parse_failures",
        "n_full_plan_scaffolds_executed", "n_execution_failures", "n_schema_failures",
        "n_oracle_payload_mismatches", "n_answers_incorrect", "overall_pass",
    )}, ensure_ascii=False, indent=2))
