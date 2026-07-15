#!/usr/bin/env python3
"""Milestone 4C — offline answer_incorrect equivalence forensic (no model calls).

Re-executes stored candidate programs via classify_response and compares
submitted vs oracle with (1) current strict oracle checker and (2) independent
exact-equivalence helpers. Never writes formal result JSONL.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

RESULTS = ROOT / "docs/experiments/results/ce115_calc_local_confirmatory"
OUT_JSON = ROOT / "docs/experiments/analysis/ce115_answer_incorrect_forensic.json"
OUT_MD = ROOT / "docs/experiments/analysis/ce115_answer_incorrect_forensic.md"


def _as_fraction(value: Any) -> Fraction | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, Fraction):
        return value
    if isinstance(value, float):
        # Reject binary float as authoritative; only allow exact decimal strings.
        return None
    if isinstance(value, str):
        text = value.strip().replace(" ", "")
        if not text:
            return None
        try:
            return Fraction(text)
        except (ValueError, ZeroDivisionError):
            return None
    return None


def exact_numbers_equal(a: Any, b: Any) -> bool:
    fa, fb = _as_fraction(a), _as_fraction(b)
    if fa is None or fb is None:
        return a == b
    return fa == fb


def exact_sequence_equal(a: Any, b: Any, *, sorted_ok: bool = False) -> bool:
    if not isinstance(a, list) or not isinstance(b, list):
        return False
    if len(a) != len(b):
        return False
    if sorted_ok:
        try:
            aa = sorted(_as_fraction(x) or Fraction(0) for x in a)
            bb = sorted(_as_fraction(x) or Fraction(0) for x in b)
            if any(_as_fraction(x) is None for x in a) or any(_as_fraction(x) is None for x in b):
                return sorted(a, key=str) == sorted(b, key=str)
            return aa == bb
        except TypeError:
            return sorted(map(str, a)) == sorted(map(str, b))
    return all(exact_numbers_equal(x, y) for x, y in zip(a, b))


def independent_equivalence(
    oracle_type: str,
    expected: Any,
    submitted: Any,
) -> dict[str, Any]:
    """Exact equivalence beyond string/dict identity."""
    if expected is None:
        return {"equivalent": False, "reason": "expected_unavailable"}
    if submitted is None:
        return {"equivalent": False, "reason": "submitted_unavailable"}

    if oracle_type == "exact_rational_expression":
        if not isinstance(expected, dict) or not isinstance(submitted, dict):
            return {"equivalent": False, "reason": "shape_mismatch"}
        eq = exact_numbers_equal(expected.get("value"), submitted.get("value"))
        return {
            "equivalent": eq,
            "reason": "rational_exact_equal" if eq else "rational_not_equal",
            "normalized_expected": str(_as_fraction(expected.get("value"))),
            "normalized_submitted": str(_as_fraction(submitted.get("value"))),
        }

    if oracle_type == "radical_simplification":
        if not isinstance(expected, dict) or not isinstance(submitted, dict):
            return {"equivalent": False, "reason": "shape_mismatch"}
        eq = (
            exact_numbers_equal(expected.get("coefficient"), submitted.get("coefficient"))
            and exact_numbers_equal(expected.get("radicand"), submitted.get("radicand"))
        )
        return {
            "equivalent": eq,
            "reason": "radical_pair_equal" if eq else "radical_pair_not_equal",
        }

    if oracle_type == "polynomial_division_general":
        if not isinstance(expected, dict) or not isinstance(submitted, dict):
            return {"equivalent": False, "reason": "shape_mismatch"}
        q_ok = exact_sequence_equal(
            expected.get("quotient_coefficients"),
            submitted.get("quotient_coefficients"),
        )
        r_ok = exact_sequence_equal(
            expected.get("remainder_coefficients"),
            submitted.get("remainder_coefficients"),
        )
        # Also accept alternate key "remainder" when scalar.
        if not r_ok and "remainder" in submitted:
            exp_r = expected.get("remainder_coefficients")
            if isinstance(exp_r, list) and len(exp_r) == 1:
                r_ok = exact_numbers_equal(exp_r[0], submitted.get("remainder"))
        eq = q_ok and r_ok
        return {
            "equivalent": eq,
            "reason": "poly_div_equal" if eq else "poly_div_not_equal",
            "quotient_equal": q_ok,
            "remainder_equal": r_ok,
        }

    if oracle_type == "polynomial_factor_roots":
        if not isinstance(expected, dict) or not isinstance(submitted, dict):
            return {"equivalent": False, "reason": "shape_mismatch"}
        eq = exact_sequence_equal(expected.get("roots"), submitted.get("roots"), sorted_ok=True)
        # Multiset equality via Fraction when possible
        return {
            "equivalent": eq,
            "reason": "root_set_equal" if eq else "root_set_not_equal",
        }

    # Fallback to identity
    identity = submitted == expected
    return {
        "equivalent": identity,
        "reason": "identity_fallback",
    }


def classify_forensic(
    *,
    observed_outcome: str,
    current_is_correct: bool | None,
    independent: dict[str, Any],
    reclassified_outcome: str | None,
) -> str:
    if reclassified_outcome and reclassified_outcome != "answer_incorrect":
        return "EXECUTION_OR_EXTRACTION_MISCLASSIFIED"
    if current_is_correct is True:
        return "INSUFFICIENT_EVIDENCE"
    if independent.get("equivalent") is True and current_is_correct is False:
        # Strict checker said wrong, exact math says equal → false negative / checker shape
        reason = str(independent.get("reason") or "")
        if "equal" in reason and "not_equal" not in reason:
            # Heuristic: rational 0.25 vs 1/4 style → EQUIVALENCE_FALSE_NEGATIVE
            # coefficient type int vs str with same value also EQUIVALENCE
            return "EQUIVALENCE_FALSE_NEGATIVE"
        return "CHECKER_OR_NORMALIZATION_BUG"
    if independent.get("equivalent") is False and current_is_correct is False:
        return "TRUE_ANSWER_ERROR"
    return "INSUFFICIENT_EVIDENCE"


def load_answer_incorrect_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(RESULTS.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("outcome") == "answer_incorrect":
                row["_path"] = str(path.relative_to(ROOT)).replace("\\", "/")
                rows.append(row)
    return rows


def gate_funnel(all_rows: list[dict[str, Any]]) -> dict[str, Any]:
    def status(row: dict[str, Any], gate: str) -> str:
        return str(((row.get("evaluation_gates") or {}).get(gate) or {}).get("status") or "MISSING")

    def funnel_for(subset: list[dict[str, Any]]) -> dict[str, Any]:
        n = len(subset)
        g1_pass = sum(1 for r in subset if status(r, "g1_evaluability") == "PASS")
        g2_assessed = sum(1 for r in subset if status(r, "g2_executability") not in {"NOT_ASSESSED", "MISSING"})
        g2_pass = sum(1 for r in subset if status(r, "g2_executability") == "PASS")
        g3_assessed = sum(1 for r in subset if status(r, "g3_contract_compliance") not in {"NOT_ASSESSED", "MISSING"})
        g3_pass = sum(1 for r in subset if status(r, "g3_contract_compliance") == "PASS")
        g4_assessed = sum(1 for r in subset if status(r, "g4_semantic_correctness") not in {"NOT_ASSESSED", "MISSING"})
        g4_pass = sum(1 for r in subset if status(r, "g4_semantic_correctness") == "PASS")
        g4_fail = sum(1 for r in subset if status(r, "g4_semantic_correctness") == "FAIL")
        ans_inc = sum(1 for r in subset if r.get("outcome") == "answer_incorrect")
        return {
            "n_cells": n,
            "g1_pass": f"{g1_pass} / {n}",
            "g2_assessed": f"{g2_assessed} / {n}",
            "g2_pass": f"{g2_pass} / {g2_assessed}" if g2_assessed else f"0 / 0",
            "g3_assessed": f"{g3_assessed} / {n}",
            "g3_pass": f"{g3_pass} / {g3_assessed}" if g3_assessed else f"0 / 0",
            "g4_assessed": f"{g4_assessed} / {n}",
            "g4_pass": f"{g4_pass} / {g4_assessed}" if g4_assessed else f"0 / 0",
            "g4_fail": f"{g4_fail} / {g4_assessed}" if g4_assessed else f"0 / 0",
            "answer_incorrect_over_g4_assessed": (
                f"{ans_inc} / {g4_assessed}" if g4_assessed else "0 / 0"
            ),
            "answer_incorrect_over_n": f"{ans_inc} / {n}",
        }

    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_cond: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in all_rows:
        by_model[str(row.get("model_tag"))].append(row)
        by_cond[str(row.get("prompt_condition"))].append(row)
    return {
        "by_model": {k: funnel_for(v) for k, v in sorted(by_model.items())},
        "by_condition": {k: funnel_for(v) for k, v in sorted(by_cond.items())},
        "overall": funnel_for(all_rows),
    }


def main() -> int:
    from agent_tools.finals_rebuild.ce115_calc_golden_generators import formal_l1_tasks
    from agent_tools.finals_rebuild.math_boundary_pilot import (
        _execute_generate,
        classify_response,
    )
    from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
    from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

    tasks = formal_l1_tasks()
    ai_rows = load_answer_incorrect_rows()
    if len(ai_rows) != 16:
        print(f"warning: expected 16 answer_incorrect, got {len(ai_rows)}", file=sys.stderr)

    all_rows: list[dict[str, Any]] = []
    for path in sorted(RESULTS.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                all_rows.append(json.loads(line))

    cases: list[dict[str, Any]] = []
    for row in ai_rows:
        task = tasks[row["task_id"]]
        oracle_payload = sample_task_parameters(task, int(row["seed"]))["oracle_payload"]
        frozen = {
            "task_id": row["task_id"],
            "oracle_type": task["oracle_type"],
            "oracle_payload": oracle_payload,
            "repeat_seed": row["seed"],
        }
        raw = row.get("raw_first_attempt_output") or ""
        outcome, source, details = classify_response(raw, frozen, task)

        submitted: Any = None
        exec_status = None
        exec_error = None
        returned_value: Any = None
        if source:
            exec_status, returned_value, exec_error = _execute_generate(
                source, skill_id=task["skill_id"]
            )
            if exec_status == "passed" and isinstance(returned_value, dict):
                submitted = returned_value.get("correct_answer")

        oracle_verdict = evaluate_math_task_oracle(task["oracle_type"], oracle_payload, submitted)
        independent = independent_equivalence(
            task["oracle_type"],
            oracle_verdict.get("expected_answer"),
            submitted,
        )
        # Detect 1/4 vs 0.25 style explicitly
        equiv_rationale = None
        if task["oracle_type"] == "exact_rational_expression" and isinstance(submitted, dict):
            exp_v = (oracle_verdict.get("expected_answer") or {}).get("value")
            sub_v = submitted.get("value")
            if (
                independent.get("equivalent")
                and str(exp_v) != str(sub_v)
                and _as_fraction(exp_v) is not None
                and _as_fraction(sub_v) is not None
            ):
                equiv_rationale = f"decimal_or_unreduced_form: expected={exp_v!r} submitted={sub_v!r}"

        label = classify_forensic(
            observed_outcome=str(row.get("outcome")),
            current_is_correct=oracle_verdict.get("is_correct"),
            independent=independent,
            reclassified_outcome=outcome,
        )

        if independent.get("equivalent") and not oracle_verdict.get("is_correct"):
            label = "EQUIVALENCE_FALSE_NEGATIVE"
            if isinstance(submitted, dict) and isinstance(oracle_verdict.get("expected_answer"), dict):
                exp = oracle_verdict["expected_answer"]
                if task["oracle_type"] == "radical_simplification":
                    for key in ("coefficient", "radicand"):
                        if type(exp.get(key)) != type(submitted.get(key)) and exact_numbers_equal(
                            exp.get(key), submitted.get(key)
                        ):
                            label = "CHECKER_OR_NORMALIZATION_BUG"
                if task["oracle_type"] in {"polynomial_division_general", "polynomial_factor_roots"}:
                    if independent.get("equivalent"):
                        label = "EQUIVALENCE_FALSE_NEGATIVE"

        cases.append(
            {
                "cell_id": row["cell_id"],
                "model": row.get("model_tag"),
                "condition": row.get("prompt_condition"),
                "task": row.get("task_id"),
                "seed": row.get("seed"),
                "artifact_path": row["_path"],
                "candidate_program_present": bool(row.get("candidate_extracted")),
                "reexec_outcome": outcome,
                "model_returned_answer": submitted,
                "oracle_expected_answer": oracle_verdict.get("expected_answer"),
                "current_checker": "evaluate_math_task_oracle + submitted == expected",
                "current_is_correct": oracle_verdict.get("is_correct"),
                "normalization_before": {
                    "submitted": submitted,
                    "expected": oracle_verdict.get("expected_answer"),
                },
                "normalization_after": {
                    "independent": independent,
                    "equiv_rationale": equiv_rationale,
                },
                "current_verdict": "answer_incorrect",
                "independent_exact_equivalence_verdict": independent,
                "forensic_class": label,
                "discrepancy_reason": (
                    equiv_rationale
                    or independent.get("reason")
                    or details.get("mismatch_reason")
                    or "oracle_mismatch"
                ),
                "evidence": {
                    "g4_status": ((row.get("evaluation_gates") or {}).get("g4_semantic_correctness") or {}).get(
                        "status"
                    ),
                    "oracle_payload": oracle_payload,
                    "details_expected_answer": (details or {}).get("expected_answer")
                    if isinstance(details, dict)
                    else None,
                    "candidate_sha_len": len(row.get("candidate_extracted") or ""),
                    "exec_status": exec_status,
                    "exec_error": exec_error,
                    "returned_value_keys": list(returned_value.keys())
                    if isinstance(returned_value, dict)
                    else None,
                },
            }
        )

    class_counts = Counter(c["forensic_class"] for c in cases)
    by_model = Counter((c["model"], c["forensic_class"]) for c in cases)
    by_cond = Counter((c["condition"], c["forensic_class"]) for c in cases)
    by_task = Counter((c["task"], c["forensic_class"]) for c in cases)

    need_pipeline = class_counts.get("EQUIVALENCE_FALSE_NEGATIVE", 0) + class_counts.get(
        "CHECKER_OR_NORMALIZATION_BUG", 0
    ) > 0

    report = {
        "scope": "outcome=answer_incorrect only",
        "n_cases": len(cases),
        "class_counts": dict(class_counts),
        "by_model_class": {f"{m}|{k}": n for (m, k), n in sorted(by_model.items())},
        "by_condition_class": {f"{c}|{k}": n for (c, k), n in sorted(by_cond.items())},
        "by_task_class": {f"{t}|{k}": n for (t, k), n in sorted(by_task.items())},
        "condition_task_distribution": {
            "by_condition": dict(Counter(c["condition"] for c in cases)),
            "by_task": dict(Counter(c["task"] for c in cases)),
            "by_model": dict(Counter(c["model"] for c in cases)),
        },
        "found_quarter_decimal_style_false_negative": any(
            c.get("normalization_after", {}).get("equiv_rationale") for c in cases
        ),
        "pipeline_corrected_ledger_recommended": need_pipeline,
        "gate_funnel": gate_funnel(all_rows),
        "cases": cases,
        "notes": [
            "Observed JSONL artifacts were not modified.",
            "Independent equivalence uses fractions.Fraction for rationals; no float tolerance.",
            "Current production checker uses strict submitted == expected identity.",
        ],
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    lines = [
        "# CE115 answer_incorrect forensic (16 cells)",
        "",
        "## Summary counts",
        "",
        f"- cases: **{len(cases)}**",
        f"- TRUE_ANSWER_ERROR: **{class_counts.get('TRUE_ANSWER_ERROR', 0)}**",
        f"- EQUIVALENCE_FALSE_NEGATIVE: **{class_counts.get('EQUIVALENCE_FALSE_NEGATIVE', 0)}**",
        f"- CHECKER_OR_NORMALIZATION_BUG: **{class_counts.get('CHECKER_OR_NORMALIZATION_BUG', 0)}**",
        f"- EXECUTION_OR_EXTRACTION_MISCLASSIFIED: **{class_counts.get('EXECUTION_OR_EXTRACTION_MISCLASSIFIED', 0)}**",
        f"- INSUFFICIENT_EVIDENCE: **{class_counts.get('INSUFFICIENT_EVIDENCE', 0)}**",
        f"- found 1/4↔0.25-style FN signal: **{report['found_quarter_decimal_style_false_negative']}**",
        f"- pipeline-corrected ledger recommended: **{need_pipeline}**",
        "",
        "## Distribution of the 16",
        "",
        f"- by model: `{report['condition_task_distribution']['by_model']}`",
        f"- by condition: `{report['condition_task_distribution']['by_condition']}`",
        f"- by task: `{report['condition_task_distribution']['by_task']}`",
        "",
        "## Gate funnel",
        "",
        "```json",
        json.dumps(report["gate_funnel"], ensure_ascii=False, indent=2),
        "```",
        "",
        "## Per-cell",
        "",
    ]
    for c in cases:
        lines.extend(
            [
                f"### `{c['cell_id']}`",
                "",
                f"- class: **{c['forensic_class']}**",
                f"- model/condition/task/seed: {c['model']} / {c['condition']} / {c['task']} / {c['seed']}",
                f"- expected: `{json.dumps(c['oracle_expected_answer'], ensure_ascii=False)}`",
                f"- submitted: `{json.dumps(c['model_returned_answer'], ensure_ascii=False)}`",
                f"- independent: `{json.dumps(c['independent_exact_equivalence_verdict'], ensure_ascii=False)}`",
                f"- discrepancy: {c['discrepancy_reason']}",
                "",
            ]
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"json": str(OUT_JSON), "md": str(OUT_MD), "class_counts": dict(class_counts)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
