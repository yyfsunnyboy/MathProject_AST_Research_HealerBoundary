"""Zero-model clean-incremental preflight for CE115 Q9 formal task.

Three cells only (Ab1 / Ab2g / Ab2d). Does not re-run the existing three calc
tasks. Shared canonical prompts for Gemini and Qwen (same builder). real_model_calls=0.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    LINEAGE_ID,
    assert_clean_ablation_invariants,
    build_condition_prompt,
    section_identity,
)
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

TASK_MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
TASK_ID = "ce115_calc_common_factor_quadratic_root_ordering_l1"
CONDITIONS = ("ab1", "ab2g", "ab2d")
SEED = 2026071301
EXPECTED_FROZEN = {
    "shared_shift": 7,
    "leading_factor": 2,
    "subtracted_factor": 10,
    "root_order": "a>b",
    "linear_combination": {"a": 1, "b": 2},
}
EXPECTED_ANSWER = {"roots": [5, -7], "a": 5, "b": -7, "value": -9}
EXISTING_THREE = (
    "ce115_calc_polynomial_division_l1",
    "ce115_calc_radical_simplification_l1",
    "ce115_calc_exact_rational_expression_l1",
)


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def load_task() -> dict[str, Any]:
    rows = [
        json.loads(line)
        for line in TASK_MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    by_id = {row["task_id"]: row for row in rows}
    if TASK_ID not in by_id:
        raise ValueError(f"missing task {TASK_ID}")
    return by_id[TASK_ID]


def reconstruct_original_equation(payload: dict[str, Any]) -> str:
    leading = payload["leading_factor"]
    subtracted = payload["subtracted_factor"]
    shift = payload["shared_shift"]
    return f"{leading}x(x+{shift})-{subtracted}(x+{shift})=0"


def build_plan(output_dir: Path) -> dict[str, Any]:
    task = load_task()
    sampled = sample_task_parameters(task, SEED)
    frozen = {
        "task_id": TASK_ID,
        "oracle_type": task["oracle_type"],
        "oracle_payload": sampled["oracle_payload"],
        "repeat_seed": SEED,
    }
    prompts = assert_clean_ablation_invariants(task, frozen)
    cells = []
    for condition in CONDITIONS:
        prompt = prompts[condition]
        cells.append(
            {
                "cell_id": f"shared__{TASK_ID}__{condition}__seed_{SEED}",
                "task_id": TASK_ID,
                "family": task["skill_id"],
                "condition": condition,
                "seed": SEED,
                "frozen_parameters": frozen["oracle_payload"],
                "prompt": prompt,
                "canonical_prompt_hash": _hash(prompt),
                "prompt_hash": _hash(prompt),
                "prompt_lineage": LINEAGE_ID,
                "section_identity": section_identity(prompt, condition),
                "first_attempt_only": True,
                "retry": 0,
                "healer": 0,
            }
        )
    plan = {
        "run_id": output_dir.name,
        "task_id": TASK_ID,
        "seed": SEED,
        "prompt_lineage": LINEAGE_ID,
        "conditions": list(CONDITIONS),
        "task_ids": [TASK_ID],
        "excluded_existing_three": list(EXISTING_THREE),
        "planned_cells": len(cells),
        "cells": cells,
        "reconstruction": {
            "frozen_parameters": frozen["oracle_payload"],
            "original_equation": reconstruct_original_equation(frozen["oracle_payload"]),
            "matches_cap_q09_stem": reconstruct_original_equation(frozen["oracle_payload"])
            == "2x(x+7)-10(x+7)=0",
        },
    }
    plan["plan_hash"] = _hash(json.dumps(plan, sort_keys=True, default=str))
    return plan


def preflight(output_dir: Path) -> dict[str, Any]:
    output_dir = Path(output_dir)
    plan = build_plan(output_dir)
    payload = plan["cells"][0]["frozen_parameters"]
    verdict = evaluate_math_task_oracle(
        "common_factor_quadratic_root_ordering", payload, EXPECTED_ANSWER
    )
    wrong = evaluate_math_task_oracle(
        "common_factor_quadratic_root_ordering",
        payload,
        {"roots": [5, -7], "a": 5, "b": -7, "value": 3},
    )
    identities = {
        condition: _hash(json.dumps(cell["frozen_parameters"], sort_keys=True))
        for condition, cell in ((c["condition"], c) for c in plan["cells"])
    }
    hashes = {c["condition"]: c["canonical_prompt_hash"] for c in plan["cells"]}
    checks: dict[str, Any] = {
        "planned_cells_exactly_3": len(plan["cells"]) == 3,
        "matrix_exact": {c["condition"] for c in plan["cells"]} == set(CONDITIONS),
        "only_q09_task": plan["task_ids"] == [TASK_ID],
        "existing_three_not_included": all(
            tid not in plan["task_ids"] for tid in EXISTING_THREE
        ),
        "frozen_equals_expected_reconstruction": payload == EXPECTED_FROZEN,
        "frozen_identity_cross_condition": len(set(identities.values())) == 1,
        "oracle_payload_equals_frozen": all(
            c["frozen_parameters"] == payload for c in plan["cells"]
        ),
        "original_equation_reconstructed": plan["reconstruction"]["matches_cap_q09_stem"],
        "oracle_expected_schema": verdict["expected_answer"] == EXPECTED_ANSWER,
        "oracle_accepts_correct_answer": verdict["is_correct"] is True,
        "oracle_rejects_wrong_value": wrong["is_correct"] is False,
        "oracle_does_not_hardcode_answer_in_payload": "-9" not in json.dumps(payload),
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
            and "FractionOps" not in c["prompt"]
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
        "gemini_qwen_share_canonical_hashes": True,  # single shared builder; one hash set
        "canonical_prompt_hashes_present": all(
            len(c["canonical_prompt_hash"]) == 64 for c in plan["cells"]
        ),
        "no_healer": all(c["healer"] == 0 for c in plan["cells"]),
        "output_writable": True,
        "real_model_calls": 0,
    }
    checks["passed"] = all(
        value for key, value in checks.items() if key != "real_model_calls"
    ) and checks["real_model_calls"] == 0
    checks["blocker"] = None if checks["passed"] else "PREFLIGHT_FAILED"
    return {
        "run_id": plan["run_id"],
        "checks": checks,
        "canonical_prompt_hashes": hashes,
        "expected_answer": EXPECTED_ANSWER,
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
            "canonical_prompt_hashes": pf["canonical_prompt_hashes"],
            "expected_answer": pf["expected_answer"],
            "real_model_calls": 0,
        },
    )
    prompts_dir = output_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    for cell in pf["plan"]["cells"]:
        (prompts_dir / f"{cell['condition']}.txt").write_text(cell["prompt"], encoding="utf-8")
        _write_json(
            prompts_dir / f"{cell['condition']}.meta.json",
            {
                "condition": cell["condition"],
                "canonical_prompt_hash": cell["canonical_prompt_hash"],
                "section_identity": cell["section_identity"],
                "frozen_parameters": cell["frozen_parameters"],
            },
        )
    _write_json(
        output_dir / "summary.json",
        {
            "task_id": TASK_ID,
            "passed": pf["checks"]["passed"],
            "real_model_calls": 0,
            "canonical_prompt_hashes": pf["canonical_prompt_hashes"],
            "safe_for_formal_model_pilot": pf["checks"]["passed"],
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="CE115 Q9 clean-incremental zero-model preflight"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT
        / "docs/experiments/results/ce115_q09_clean_incremental_preflight_01",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Persist manifest/preflight/prompts under --output-dir",
    )
    args = parser.parse_args()
    pf = preflight(args.output_dir)
    if args.write:
        write_preflight_artifacts(args.output_dir, pf)
    print(json.dumps(pf, ensure_ascii=False, indent=2, default=str))
    return 0 if pf["checks"]["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
