"""Read-only Healer pre-scan for Qwen Math16 run_002 eligible cells.

Classifies candidate rule families per failure_classification_standard_v2 §7.1.
Does NOT mutate artifacts, call models, or apply repairs.
Judgment uses raw_response + AST only (no oracle / expected answers).
"""
from __future__ import annotations

import ast
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "docs/experiments/results"
OUT = RESULTS / "qwen_math16_run_002_healer_prescan.json"

RUNS = (
    ("qwen35_4b_math16_ab123_run_002", "qwen3.5:4b"),
    ("qwen35_9b_math16_ab123_run_002", "qwen3.5:9b"),
)

THINK_RE = re.compile(r"</?think>", re.I)
GEN_DEF_RE = re.compile(r"^\s*def\s+(\w+)\s*\(", re.M)


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _extract_code_candidate(raw: str) -> str | None:
    """Best-effort code body from raw response without evaluator oracle."""
    if not raw or not raw.strip():
        return None
    text = THINK_RE.sub("", raw)
    # fenced python blocks
    blocks = re.findall(r"```(?:python)?\s*([\s\S]*?)```", text, flags=re.I)
    if blocks:
        # prefer block containing def
        for b in blocks:
            if "def " in b:
                return b.strip()
        return blocks[-1].strip()
    # fallback: from first def to end-ish
    m = re.search(r"(?m)^(def\s+\w+\s*\()", text)
    if m:
        return text[m.start() :].strip()
    return None


def _parse_ok(code: str | None) -> tuple[bool, ast.AST | None, str | None]:
    if not code:
        return False, None, "no_code"
    try:
        tree = ast.parse(code)
        return True, tree, None
    except SyntaxError as exc:
        return False, None, f"{exc.msg} @ line {exc.lineno}"


def _top_level_funcs(tree: ast.AST) -> list[str]:
    return [
        n.name
        for n in getattr(tree, "body", [])
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]


def _looks_packaging_only(code: str, tree: ast.AST) -> tuple[bool, str]:
    """Heuristic: code parses; return is scalar/string-ish vs dict packaging."""
    # Find generate() or last function return patterns
    funcs = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    if not funcs:
        return False, "no function defs"
    # Prefer generate
    target = next((f for f in funcs if f.name == "generate"), funcs[-1])
    returns: list[ast.AST] = []
    for node in ast.walk(target):
        if isinstance(node, ast.Return) and node.value is not None:
            returns.append(node.value)
    if not returns:
        return False, "no return statements"
    # If any return is a dict/Call(dict)/dict display → likely not bare packaging miss
    for val in returns:
        if isinstance(val, ast.Dict):
            return False, "returns dict already"
        if isinstance(val, ast.Call) and isinstance(val.func, ast.Name) and val.func.id == "dict":
            return False, "returns dict() call"
    # Bare string / number / Name / BinOp → packaging candidate
    kinds = {type(v).__name__ for v in returns}
    if kinds <= {"Constant", "Str", "Num", "Name", "JoinedStr", "BinOp", "UnaryOp", "Attribute"}:
        return True, f"returns non-dict values ({sorted(kinds)}) suggesting schema wrap needed"
    # list/tuple of simple values also packaging-ish
    if all(isinstance(v, (ast.List, ast.Tuple, ast.Constant, ast.Name)) for v in returns):
        return True, "returns list/tuple/scalar rather than required object schema"
    return False, f"return shapes mixed/complex ({sorted(kinds)})"


def _unique_entrypoint_rename(tree: ast.AST) -> tuple[bool, str]:
    funcs = _top_level_funcs(tree)
    if len(funcs) != 1:
        return False, f"top-level funcs={funcs!r} (need exactly one)"
    name = funcs[0]
    if name == "generate":
        return False, "already named generate"
    # Check arity loosely: has args
    fn = next(n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
    argc = len(fn.args.args) + len(fn.args.kwonlyargs)
    return True, f"single def {name}(argc≈{argc}) could rename to generate if signature compatible"


def _mechanical_syntax(raw: str, code: str | None, err: str | None) -> tuple[bool, str]:
    if THINK_RE.search(raw or ""):
        return False, "think tags present — not mechanical"
    if not err:
        return False, "parses already"
    # Degenerate: huge / repeated
    if code and len(code) > 30000:
        return False, "oversized candidate — likely degenerate/runaway"
    msg = (err or "").lower()
    # Unique safe cases
    if "was never closed" in msg or "eof while scanning" in msg or "unterminated" in msg:
        return True, f"unclosed literal/paren: {err}"
    if "expected ':'" in msg and "line" in msg:
        # Too ambiguous often
        return False, f"missing colon but intent unclear: {err}"
    if "unexpected eof" in msg or "unexpected end" in msg:
        return True, f"truncation/EOF closable?: {err}"
    if "invalid syntax" in msg and "f-string" in msg:
        return False, f"f-string syntax — often needs rewrite: {err}"
    if "f-string" in msg and ("}" in msg or "single" in msg):
        return False, f"f-string brace issue needs judgment: {err}"
    return False, f"syntax error not uniquely mechanical: {err}"


def _mechanical_wiring(code: str, tree: ast.AST) -> tuple[bool, str]:
    """Detect kwargs/frozen path wiring mistakes without checking oracle."""
    text = code
    hits = []
    if re.search(r"kwargs\s*\[\s*['\"]frozen", text):
        hits.append("kwargs['frozen…'] direct index")
    if re.search(r"kwargs\.get\(\s*['\"]frozen", text):
        hits.append("kwargs.get('frozen…')")
    if "frozen_params" in text and "kwargs" in text:
        # assignment from kwargs
        if re.search(r"frozen_params\s*=\s*kwargs", text):
            hits.append("frozen_params = kwargs…")
    # empty kwargs pattern then KeyError-prone
    if "kwargs.get(" in text or "kwargs[" in text:
        # If uses kwargs for params that should be function args
        if "def generate" in text and "kwargs" in text:
            hits.append("generate uses kwargs lookup")
    if not hits:
        return False, "no clear kwargs/frozen wiring anti-pattern"
    # Only claim mechanical if parse ok and pattern is simple KeyError-prone path
    if "kwargs[" in text and "frozen" in text:
        return True, "likely KeyError wiring on kwargs/frozen path: " + "; ".join(hits)
    return False, "kwargs present but not uniquely mechanical: " + "; ".join(hits)


def _is_degenerate(raw: str) -> bool:
    if len(raw) < 2000:
        return False
    sample = raw[-20000:] if len(raw) > 20000 else raw
    lines = [ln for ln in sample.splitlines() if len(ln.strip()) > 5]
    if lines:
        top_c = Counter(lines).most_common(1)[0][1]
        if top_c >= 10:
            return True
    for n in (40, 80):
        counts = Counter(sample[i : i + n] for i in range(0, len(sample) - n, n))
        if counts:
            chunk, c = counts.most_common(1)[0]
            if c >= 8 and chunk.strip():
                return True
    return False


def classify_cell(art: dict[str, Any], raw: str) -> dict[str, Any]:
    layer = (art.get("failure_layer") or {}).get("primary_layer")
    status = art.get("evaluator_status")
    code = _extract_code_candidate(raw)
    ok, tree, err = _parse_ok(code)

    # Hard excludes
    if layer == "L5" or status in {"ANSWER_INCORRECT", "INTRINSIC_SAFETY"}:
        return {
            "candidate_rule": "NO_SAFE_RULE",
            "evidence": f"L5/semantic status={status}; Healer禁止重解題",
        }
    if art.get("suspected_invalid") or THINK_RE.search(raw):
        return {
            "candidate_rule": "NO_SAFE_RULE",
            "evidence": "think標籤殘留或 suspected_invalid — 需猜測意圖，不算機械修復",
        }
    if _is_degenerate(raw):
        return {
            "candidate_rule": "NO_SAFE_RULE",
            "evidence": "退化重複/ runaway 輸出，無法唯一安全修復",
        }

    # L1 mechanical
    if layer == "L1" or status in {
        "PARSE_MINOR",
        "EXTRACTION_FAILURE",
        "MISSING_ENTRY_POINT",
        "CATASTROPHIC_TRUNCATION",
        "EMPTY_RESPONSE",
    }:
        mech, ev = _mechanical_syntax(raw, code, err)
        if mech:
            return {"candidate_rule": "L1_MECHANICAL", "evidence": ev}
        # missing entry point with unique func → L3 rename
        if ok and tree is not None:
            uniq, uev = _unique_entrypoint_rename(tree)
            if uniq and status == "MISSING_ENTRY_POINT":
                return {"candidate_rule": "L3_UNIQUE_ENTRYPOINT", "evidence": uev}
        return {
            "candidate_rule": "NO_SAFE_RULE",
            "evidence": ev if not ok else f"L1/parse-class but not uniquely mechanical ({status})",
        }

    # L2 packaging
    if layer == "L2" or status == "SCHEMA_FAILURE":
        if ok and tree is not None:
            pack, pev = _looks_packaging_only(code or "", tree)
            if pack:
                return {"candidate_rule": "L2_PACKAGING", "evidence": pev}
            return {"candidate_rule": "NO_SAFE_RULE", "evidence": pev}
        return {
            "candidate_rule": "NO_SAFE_RULE",
            "evidence": f"schema-class but cannot parse for packaging check: {err}",
        }

    # STRUCTURAL/LATEX often labeled L3 in qwen preliminary — packaging-adjacent
    if status in {"STRUCTURAL_MISMATCH", "LATEX_MISMATCH"}:
        if ok and tree is not None:
            pack, pev = _looks_packaging_only(code or "", tree)
            if pack:
                return {
                    "candidate_rule": "L2_PACKAGING",
                    "evidence": f"structural/latex class with packaging-like returns: {pev}",
                }
        return {
            "candidate_rule": "NO_SAFE_RULE",
            "evidence": f"structural/latex mismatch; not uniquely packaging-fixable without oracle",
        }

    # L3 unique entrypoint / API-ish
    if layer == "L3":
        if ok and tree is not None:
            uniq, uev = _unique_entrypoint_rename(tree)
            if uniq:
                return {"candidate_rule": "L3_UNIQUE_ENTRYPOINT", "evidence": uev}
        return {
            "candidate_rule": "NO_SAFE_RULE",
            "evidence": "L3 but not unique rename-only entrypoint (API misuse likely)",
        }

    # L4 wiring
    if layer == "L4" or status in {"EXECUTION_FAILURE", "RUNTIME_FAILURE"}:
        if ok and tree is not None:
            wire, wev = _mechanical_wiring(code or "", tree)
            if wire:
                return {"candidate_rule": "L4_MECHANICAL_WIRING", "evidence": wev}
            return {"candidate_rule": "NO_SAFE_RULE", "evidence": wev}
        return {
            "candidate_rule": "NO_SAFE_RULE",
            "evidence": f"runtime-class but unparseable for wiring check: {err}",
        }

    return {
        "candidate_rule": "NO_SAFE_RULE",
        "evidence": f"unclassified layer={layer} status={status}",
    }


def main() -> int:
    cells_out: list[dict[str, Any]] = []
    by_model_rule: dict[str, Counter[str]] = defaultdict(Counter)

    for run_id, model in RUNS:
        run_dir = RESULTS / run_id
        for cell_dir in sorted((run_dir / "cells").iterdir()):
            art_path = cell_dir / "artifact.json"
            if not art_path.exists():
                continue
            art = _load(art_path)
            fl = art.get("failure_layer") or {}
            eligible = bool(fl.get("healer_eligible")) or bool(
                (art.get("healer") or {}).get("healer_eligible")
            )
            if not eligible:
                continue
            raw_path = cell_dir / "raw_response.txt"
            raw = raw_path.read_text(encoding="utf-8", errors="replace") if raw_path.exists() else ""
            decision = classify_cell(art, raw)
            row = {
                "run_id": run_id,
                "model": model,
                "cell_id": art["cell_id"],
                "task_id": art.get("task_id"),
                "condition": art.get("condition"),
                "evaluator_status": art.get("evaluator_status"),
                "primary_layer": fl.get("primary_layer"),
                "candidate_rule": decision["candidate_rule"],
                "evidence": decision["evidence"],
            }
            cells_out.append(row)
            by_model_rule[model][decision["candidate_rule"]] += 1

    # Optimistic = all non-NO_SAFE; pessimistic = only L2_PACKAGING + clear L1_MECHANICAL
    opt = sum(1 for c in cells_out if c["candidate_rule"] != "NO_SAFE_RULE")
    pess = sum(
        1
        for c in cells_out
        if c["candidate_rule"] in {"L2_PACKAGING", "L1_MECHANICAL"}
    )

    payload = {
        "policy": {
            "artifacts_mutated": False,
            "model_calls": 0,
            "repairs_executed": False,
            "oracle_inspected": False,
            "basis": "raw_response + AST only; v2 §7.1 Healer boundary",
        },
        "eligible_total": len(cells_out),
        "by_model_rule_counts": {
            model: dict(counter) for model, counter in sorted(by_model_rule.items())
        },
        "safe_fix_estimate": {
            "optimistic_non_no_safe_rule": opt,
            "pessimistic_l2_or_l1_mechanical_only": pess,
        },
        "suggested_rules_to_implement": [
            {
                "id": "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
                "family": "L2_PACKAGING",
                "note": "Wrap bare scalar/string correct_answer into required dict schema",
            },
            {
                "id": "L2_DICT_FROM_NAMED_RETURNS",
                "family": "L2_PACKAGING",
                "note": "Assemble required keys when values computed but packaging wrong",
            },
            {
                "id": "L1_UNCLOSED_LITERAL_OR_PAREN",
                "family": "L1_MECHANICAL",
                "note": "Only when SyntaxError uniquely indicates one unclosed delimiter",
            },
            {
                "id": "L3_RENAME_UNIQUE_ENTRYPOINT_TO_GENERATE",
                "family": "L3_UNIQUE_ENTRYPOINT",
                "note": "Only exactly one top-level function and compatible arity",
            },
            {
                "id": "L4_KWARGS_FROZEN_PATH_REWRITE",
                "family": "L4_MECHANICAL_WIRING",
                "note": "Rewrite kwargs['frozen…'] to frozen_params signature path",
            },
        ],
        "cells": cells_out,
    }
    OUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "output": str(OUT),
                "eligible_total": len(cells_out),
                "by_model_rule_counts": payload["by_model_rule_counts"],
                "safe_fix_estimate": payload["safe_fix_estimate"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
