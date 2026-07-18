"""Zero-model preflight: 113/114 six-task external validation (6×3=18 cells).

Shared clean-incremental builder (Gemini/Qwen identical hashes). real_model_calls=0.
Does not modify existing CE115 calc/q09 artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    LINEAGE_ID,
    assert_clean_ablation_invariants,
    section_identity,
)
from agent_tools.finals_rebuild.ce115_exam_external_validation import (
    EXPECTED_ANSWERS,
    FROZEN_PAYLOADS,
    LINEAGE_NOTE,
    PROVENANCE,
    TASK_IDS,
    all_leakage_audits,
)
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

TASK_MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
CONDITIONS = ("ab1", "ab2g", "ab2d")
SEED = 2026071301
EXISTING_CORE = (
    "ce115_calc_polynomial_division_l1",
    "ce115_calc_radical_simplification_l1",
    "ce115_calc_exact_rational_expression_l1",
    "ce115_calc_common_factor_quadratic_root_ordering_l1",
)

# Minimal synthetic generate() bodies that return frozen + expected (oracle path only).
SYNTHETIC_GOLDEN: dict[str, str] = {
    "ce115_ext_114_01_power_laws_l1": '''
def generate(level=1, **kwargs):
    frozen = {"expression": "7**10 * 7**2 / 7**4", "required_form": "power_of_same_base", "base": 7}
    return {"question_text": "rewrite as power of 7", "correct_answer": {"base": 7, "exponent": 8}, "oracle_payload": frozen}
''',
    "ce115_ext_114_02_polynomial_simplify_l1": '''
def generate(level=1, **kwargs):
    frozen = {"expression": "(5*x**2 - 2*x) - (4 - 3*x)"}
    return {"question_text": "simplify", "correct_answer": {"coefficients": {"2": 5, "1": 1, "0": -4}}, "oracle_payload": frozen}
''',
    "ce115_ext_114_04_linear_system_l1": '''
def generate(level=1, **kwargs):
    frozen = {"equations": ["37*x + 2*y = 81", "23*x - 2*y = 39"], "target_expression": "x + 2*y"}
    return {"question_text": "solve and evaluate", "correct_answer": {"x": 2, "y": "7/2", "value": 9}, "oracle_payload": frozen}
''',
    "ce115_ext_114_08_radical_product_l1": '''
def generate(level=1, **kwargs):
    frozen = {"expression": "(2*sqrt(3) + sqrt(6))*sqrt(2)"}
    return {"question_text": "simplify radicals", "correct_answer": {"terms": [{"coefficient": 2, "radicand": 3}, {"coefficient": 2, "radicand": 6}]}, "oracle_payload": frozen}
''',
    "ce115_ext_113_10_factorization_l1": '''
def generate(level=1, **kwargs):
    frozen = {"expression": "5*x*(5*x - 2) - 4*(5*x - 2)**2", "required_form": "fully_factored"}
    return {"question_text": "factor", "correct_answer": {"factors": [{"x_coefficient": 5, "constant": -2}, {"x_coefficient": -15, "constant": 8}]}, "oracle_payload": frozen}
''',
    "ce115_ext_113_11_rationalize_l1": '''
def generate(level=1, **kwargs):
    frozen = {"expression": "9/(4 - sqrt(7))", "required_form": "a + b*sqrt(7)", "target_expression": "a + b"}
    return {"question_text": "rationalize", "correct_answer": {"a": 4, "b": 1, "radicand": 7, "value": 5}, "oracle_payload": frozen}
''',
}


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def load_tasks() -> dict[str, dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in TASK_MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    by_id = {row["task_id"]: row for row in rows}
    missing = [tid for tid in TASK_IDS if tid not in by_id]
    if missing:
        raise ValueError(f"missing fixture tasks: {missing}")
    return {tid: by_id[tid] for tid in TASK_IDS}


def build_plan(output_dir: Path) -> dict[str, Any]:
    tasks = load_tasks()
    cells = []
    hashes: dict[str, dict[str, str]] = {}
    for task_id in TASK_IDS:
        task = tasks[task_id]
        sampled = sample_task_parameters(task, SEED)
        frozen = {
            "task_id": task_id,
            "oracle_type": task["oracle_type"],
            "oracle_payload": sampled["oracle_payload"],
            "repeat_seed": SEED,
        }
        if frozen["oracle_payload"] != FROZEN_PAYLOADS[task_id]:
            raise ValueError(f"frozen mismatch for {task_id}")
        prompts = assert_clean_ablation_invariants(task, frozen)
        hashes[task_id] = {}
        for condition in CONDITIONS:
            prompt = prompts[condition]
            cell_id = f"shared__{task_id}__{condition}__seed_{SEED}"
            cells.append(
                {
                    "cell_id": cell_id,
                    "task_id": task_id,
                    "family": task["skill_id"],
                    "condition": condition,
                    "seed": SEED,
                    "frozen_parameters": frozen["oracle_payload"],
                    "prompt": prompt,
                    "canonical_prompt_hash": _hash(prompt),
                    "prompt_hash": _hash(prompt),
                    "prompt_lineage": LINEAGE_ID,
                    "section_identity": section_identity(prompt, condition),
                    "provenance": PROVENANCE[task_id],
                    "first_attempt_only": True,
                    "retry": 0,
                    "healer": 0,
                }
            )
            hashes[task_id][condition] = _hash(prompt)
    plan = {
        "run_id": output_dir.name,
        "cohort": LINEAGE_NOTE,
        "seed": SEED,
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS),
        "task_ids": list(TASK_IDS),
        "excluded_existing_core": list(EXISTING_CORE),
        "planned_cells": len(cells),
        "cells": cells,
        "canonical_prompt_hashes": hashes,
        "expected_answers": EXPECTED_ANSWERS,
    }
    plan["plan_hash"] = _hash(json.dumps(plan, sort_keys=True, default=str))
    return plan


def _git_diff_check() -> dict[str, Any]:
    proc = subprocess.run(
        ["git", "diff", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "exit_code": proc.returncode,
        "passed": proc.returncode == 0,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
    }


def preflight(output_dir: Path) -> dict[str, Any]:
    output_dir = Path(output_dir)
    plan = build_plan(output_dir)
    tasks = load_tasks()
    leakage = all_leakage_audits()
    oracle_ok = {}
    synthetic_ok = {}
    for task_id in TASK_IDS:
        payload = FROZEN_PAYLOADS[task_id]
        expected = EXPECTED_ANSWERS[task_id]
        verdict = evaluate_math_task_oracle(tasks[task_id]["oracle_type"], payload, expected)
        oracle_ok[task_id] = verdict["is_correct"] is True and verdict["expected_answer"] == expected
        outcome, _src, _details = classify_response(
            SYNTHETIC_GOLDEN[task_id],
            {"oracle_payload": payload},
            tasks[task_id],
        )
        synthetic_ok[task_id] = outcome == "passed"
    hashes = plan["canonical_prompt_hashes"]
    git_check = _git_diff_check()
    checks: dict[str, Any] = {
        "planned_cells_exactly_18": len(plan["cells"]) == 18,
        "matrix_6x3": (
            {c["task_id"] for c in plan["cells"]} == set(TASK_IDS)
            and {c["condition"] for c in plan["cells"]} == set(CONDITIONS)
        ),
        "existing_core_not_included": all(tid not in plan["task_ids"] for tid in EXISTING_CORE),
        "frozen_identity_per_task": all(
            FROZEN_PAYLOADS[tid] == next(
                c["frozen_parameters"] for c in plan["cells"] if c["task_id"] == tid
            )
            for tid in TASK_IDS
        ),
        "oracle_accepts_all_expected": all(oracle_ok.values()),
        "synthetic_golden_all_pass": all(synthetic_ok.values()),
        "leakage_audit_passed": leakage["passed"],
        "seed_consistent": {c["seed"] for c in plan["cells"]} == {SEED},
        "prompt_builders_nonempty": all(c["prompt"].strip() for c in plan["cells"]),
        "clean_incremental_ab1": all(
            "## Clean-incremental GENERIC" not in c["prompt"]
            and "## Clean-incremental DOMAIN" not in c["prompt"]
            for c in plan["cells"]
            if c["condition"] == "ab1"
        ),
        "clean_incremental_ab2g": all(
            "## Clean-incremental GENERIC" in c["prompt"]
            and "## Clean-incremental DOMAIN" not in c["prompt"]
            for c in plan["cells"]
            if c["condition"] == "ab2g"
        ),
        "clean_incremental_ab2d": all(
            "## Clean-incremental GENERIC" in c["prompt"]
            and "## Clean-incremental DOMAIN" in c["prompt"]
            and "CE115 Ab2d-Assembly domain contract" not in c["prompt"]
            for c in plan["cells"]
            if c["condition"] == "ab2d"
        ),
        "generic_shared_not_rewritten": all(
            "## Clean-incremental GENERIC\n"
            "Output complete Python source only. Do not use Markdown fences or explanatory prose. "
            "Preserve frozen parameters exactly. Verify that generate() exists. "
            "Verify that the return value has exactly the three required top-level keys. "
            "Verify field types match the stated contract and that oracle_payload equals the frozen parameters."
            in c["prompt"]
            for c in plan["cells"]
            if c["condition"] in {"ab2g", "ab2d"}
        ),
        "canonical_prompt_hashes_present": all(
            len(h) == 64 for tid in hashes for h in hashes[tid].values()
        ),
        "no_healer": all(c["healer"] == 0 and c["retry"] == 0 for c in plan["cells"]),
        "git_diff_check": git_check["passed"],
        "real_model_calls": 0,
    }
    checks["passed"] = all(
        value for key, value in checks.items() if key != "real_model_calls"
    ) and checks["real_model_calls"] == 0
    checks["blocker"] = None if checks["passed"] else "PREFLIGHT_FAILED"
    return {
        "run_id": plan["run_id"],
        "checks": checks,
        "oracle_ok": oracle_ok,
        "synthetic_ok": synthetic_ok,
        "leakage": leakage,
        "canonical_prompt_hashes": hashes,
        "git_diff_check": git_check,
        "plan": plan,
    }


def write_preflight_artifacts(output_dir: Path, pf: dict[str, Any]) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "manifest.json", pf["plan"])
    _write_json(
        output_dir / "preflight.json",
        {
            "checks": pf["checks"],
            "oracle_ok": pf["oracle_ok"],
            "synthetic_ok": pf["synthetic_ok"],
            "canonical_prompt_hashes": pf["canonical_prompt_hashes"],
            "git_diff_check": pf["git_diff_check"],
            "real_model_calls": 0,
        },
    )
    _write_json(output_dir / "leakage_audit.json", pf["leakage"])
    prompts_dir = output_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    for cell in pf["plan"]["cells"]:
        stem = f"{cell['task_id']}__{cell['condition']}"
        (prompts_dir / f"{stem}.txt").write_text(cell["prompt"], encoding="utf-8")
        _write_json(
            prompts_dir / f"{stem}.meta.json",
            {
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "canonical_prompt_hash": cell["canonical_prompt_hash"],
                "section_identity": cell["section_identity"],
                "frozen_parameters": cell["frozen_parameters"],
                "provenance": cell["provenance"],
            },
        )
    _write_json(
        output_dir / "summary.json",
        {
            "cohort": LINEAGE_NOTE,
            "task_ids": list(TASK_IDS),
            "planned_cells": 18,
            "passed": pf["checks"]["passed"],
            "real_model_calls": 0,
            "canonical_prompt_hashes": pf["canonical_prompt_hashes"],
            "safe_for_gemini_pilot": pf["checks"]["passed"],
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="CE115 exam external-validation zero-model preflight")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "docs/experiments/results/ce115_exam_ext_113_114_preflight_01",
    )
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    pf = preflight(args.output_dir)
    if args.write:
        write_preflight_artifacts(args.output_dir, pf)
    print(
        json.dumps(
            {
                "passed": pf["checks"]["passed"],
                "blocker": pf["checks"]["blocker"],
                "real_model_calls": 0,
                "canonical_prompt_hashes": pf["canonical_prompt_hashes"],
                "checks": pf["checks"],
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )
    return 0 if pf["checks"]["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
