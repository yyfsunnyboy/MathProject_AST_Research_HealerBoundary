#!/usr/bin/env python3
"""Write sample fixture JSONL for Milestone 3E latex/report tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.generator_success import FAIL, PASS, serialize_artifact

OUT = Path(__file__).with_name("sample_cells.jsonl")


def _gates(g6_formal: str = PASS) -> dict:
    return {
        "g1_evaluability": {"status": PASS, "reason": "ok"},
        "g2_executability": {"status": PASS, "reason": "ok"},
        "g3_contract_compliance": {"status": PASS, "reason": "ok"},
        "g4_semantic_correctness": {"status": PASS, "reason": "ok"},
        "g5_problem_presentation": {"status": PASS, "reason": "ok"},
        "g6_math_notation": {"status": g6_formal, "reason": "formal_lint"},
    }


def base(cell_id: str, **extra):
    row = {
        "record_state": "executed",
        "run_type": "fixture_sample",
        "included_in_formal_analysis": False,
        "cell_id": cell_id,
        "task_id": "ce115_calc_radical_simplification_l1",
        "prompt_condition": "ab1",
        "seed": 2026071301,
        "model_tag": "fixture-model",
        "difficulty": "l1",
        "prompt_text": "FIXTURE PROMPT",
        "prompt_hash": "0" * 64,
        "raw_first_attempt_output": "def generate():\n    return {}",
        "candidate_extracted": "def generate():\n    return {}",
        "ledger_stage": "observed",
        "retry_count": 0,
        "request_count": 0,
        "healer_enabled": False,
        "healer": {"eligible": False, "attempted": False, "rescued": False, "regression": False},
        "evaluation_gates": _gates(),
        "composite_outcomes": {
            "technical_pass": PASS,
            "presentation_pass": PASS,
            "full_pass": PASS,
        },
        "outcome": "passed",
        "observation_status": "observed_success",
        "token_duration_diagnostics": {
            "prompt_eval_count": 10,
            "eval_count": 20,
            "total_duration": 1000,
        },
    }
    row.update(extra)
    return row


def main() -> None:
    rows = [
        base(
            "fixture_renderer_pass_human_2",
            actual_question_text=r"Simplify $\sqrt{12}$.",
            correct_answer=r"$2\sqrt{3}$",
        ),
        base(
            "fixture_renderer_pass_human_1",
            actual_question_text=r"Simplify $\sqrt{12}$.",
            correct_answer=r"$2\sqrt{3}$",
        ),
        base(
            "fixture_renderer_pass_human_0",
            actual_question_text=r"Simplify $\sqrt{12}$.",
            correct_answer=r"$2\sqrt{3}$",
        ),
        base(
            "fixture_question_pass_answer_fail",
            actual_question_text=r"Simplify $\sqrt{8}$.",
            correct_answer=r"$\unknowncmd{2}$",
        ),
        base(
            "fixture_answer_pass_question_fail",
            actual_question_text=r"Simplify $\unknowncmd{12}$.",
            correct_answer=r"$2\sqrt{3}$",
        ),
        base(
            "fixture_unmatched_delimiter",
            actual_question_text=r"Simplify $\sqrt{12}.",
            correct_answer=r"$2\sqrt{3}$",
            evaluation_gates=_gates(FAIL),
            composite_outcomes={
                "technical_pass": PASS,
                "presentation_pass": FAIL,
                "full_pass": FAIL,
            },
        ),
        base(
            "fixture_unsupported_command",
            actual_question_text=r"Compute $\notacommand{1+2}$.",
            correct_answer=r"$3$",
        ),
        base(
            "fixture_raw_latex_visible",
            actual_question_text=r"Compute \frac{1}{2} without delimiters.",
            correct_answer=r"$1/2$",
        ),
        base(
            "fixture_review_incomplete",
            actual_question_text=r"Simplify $\sqrt{18}$.",
            correct_answer=r"$3\sqrt{2}$",
        ),
        {
            "record_state": "planned",
            "cell_id": "fixture_planned_only",
            "task_id": "ce115_calc_radical_simplification_l1",
            "prompt_condition": "ab1",
            "seed": 2026071302,
            "model_tag": "fixture-model",
            "difficulty": "l1",
            "prompt_text": "PLANNED ONLY",
            "evaluation_gates": None,
            "composite_outcomes": None,
            "actual_question_text": None,
            "correct_answer": None,
            "retry_count": 0,
        },
    ]
    # planned_only should not be in executed rows file — only in planned list.
    executed = [r for r in rows if r.get("record_state") == "executed"]
    OUT.write_text("\n".join(serialize_artifact(r) for r in executed) + "\n", encoding="utf-8")
    print(f"wrote {OUT} rows={len(executed)}")


if __name__ == "__main__":
    main()
