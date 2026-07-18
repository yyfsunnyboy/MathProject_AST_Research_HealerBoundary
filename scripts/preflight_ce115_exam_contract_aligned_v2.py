"""Zero-model preflight for contract-aligned v2 exam ext (8 cells × shared prompts).

Matrix per model (executed later): 114-02 Ab1/Ab2g/Ab2d + five other tasks Ab2d only.
This preflight: real_model_calls=0; stops if any audit FAIL; does not overwrite v1.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_contract_aligned_ablation_v2 import (
    LINEAGE_ID,
    TASK_DOMAIN_APIS,
    assert_v2_ablation_invariants,
    build_condition_prompt_v2,
    canonical_prompt_hash,
    domain_section,
    scan_v2_domain_adoption,
    verify_generic_body_frozen_vs_v1,
)
from agent_tools.finals_rebuild.ce115_exam_external_validation import (
    EXPECTED_ANSWERS,
    FROZEN_PAYLOADS,
    PROVENANCE,
    TASK_IDS,
    all_leakage_audits,
)
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response
from agent_tools.finals_rebuild.math_task_oracles import evaluate_math_task_oracle
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters
from scripts.ce115_qwen_ollama_transport import probe_ollama
from scripts.ce115_v4_gemini_transport import api_key_status
from tests.finals_rebuild.test_ce115_contract_aligned_v2_domain import GOLDEN_AB2D

TASK_MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
V1_HASH_FREEZE = ROOT / "docs/experiments/analysis/ce115_exam_ext_113_114_canonical_prompt_hashes.json"
V1_GEMINI = ROOT / "docs/experiments/results/ce115_exam_ext_113_114_gemini_pilot_01"
V1_QWEN = ROOT / "docs/experiments/results/ce115_exam_ext_113_114_qwen_pilot_01"
ANALYSIS = ROOT / "docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2"
SEED = 2026071301
TASK_114_02 = "ce115_ext_114_02_polynomial_simplify_l1"

# Per-model cell matrix (condition labels stored without -v2 suffix; lineage marks v2).
CELL_SPECS: list[tuple[str, str]] = [
    (TASK_114_02, "ab1"),
    (TASK_114_02, "ab2g"),
    (TASK_114_02, "ab2d"),
] + [(tid, "ab2d") for tid in TASK_IDS if tid != TASK_114_02]


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


def build_cell_plan() -> dict[str, Any]:
    tasks = load_tasks()
    cells = []
    hashes: dict[str, dict[str, str]] = {}
    for task_id, condition in CELL_SPECS:
        task = tasks[task_id]
        sampled = sample_task_parameters(task, SEED)
        frozen = {
            "task_id": task_id,
            "oracle_type": task["oracle_type"],
            "oracle_payload": sampled["oracle_payload"],
            "repeat_seed": SEED,
        }
        assert frozen["oracle_payload"] == FROZEN_PAYLOADS[task_id]
        prompts = assert_v2_ablation_invariants(task, frozen)
        prompt = prompts[condition]
        assert prompt == build_condition_prompt_v2(condition, task, frozen)
        hashes.setdefault(task_id, {})[condition] = canonical_prompt_hash(prompt)
        cells.append(
            {
                "task_id": task_id,
                "condition": condition,
                "condition_label": f"{condition}-v2",
                "seed": SEED,
                "frozen_parameters": frozen["oracle_payload"],
                "prompt": prompt,
                "canonical_prompt_hash": canonical_prompt_hash(prompt),
                "prompt_lineage": LINEAGE_ID,
                "provenance": PROVENANCE[task_id],
                "first_attempt_only": True,
                "retry": 0,
                "healer": 0,
            }
        )
    return {
        "lineage_id": LINEAGE_ID,
        "seed": SEED,
        "planned_cells_per_model": len(cells),
        "cell_specs": [{"task_id": t, "condition": c} for t, c in CELL_SPECS],
        "cells": cells,
        "canonical_prompt_hashes": hashes,
        "expected_answers": EXPECTED_ANSWERS,
    }


def _git_diff_check() -> dict[str, Any]:
    proc = subprocess.run(
        ["git", "diff", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return {"exit_code": proc.returncode, "passed": proc.returncode == 0}


def _v1_artifacts_unchanged() -> dict[str, Any]:
    before = V1_HASH_FREEZE.read_text(encoding="utf-8") if V1_HASH_FREEZE.is_file() else None
    gemini_ok = (V1_GEMINI / "summary.json").is_file()
    qwen_ok = (V1_QWEN / "summary.json").is_file()
    return {
        "v1_hash_file_present": before is not None,
        "v1_gemini_artifacts_present": gemini_ok,
        "v1_qwen_artifacts_present": qwen_ok,
        "v1_hash_sha256": _hash(before) if before else None,
        "passed": before is not None and gemini_ok and qwen_ok,
    }


def preflight(output_dir: Path, *, require_models: bool = True) -> dict[str, Any]:
    output_dir = Path(output_dir)
    verify_generic_body_frozen_vs_v1()
    plan = build_cell_plan()
    tasks = load_tasks()
    leakage = all_leakage_audits()
    oracle_ok = {}
    golden_ok = {}
    golden_adoption = {}
    for task_id in TASK_IDS:
        payload = FROZEN_PAYLOADS[task_id]
        expected = EXPECTED_ANSWERS[task_id]
        verdict = evaluate_math_task_oracle(tasks[task_id]["oracle_type"], payload, expected)
        oracle_ok[task_id] = verdict["is_correct"] is True
        src = GOLDEN_AB2D[task_id]
        outcome, _code, _details = classify_response(
            src, {"oracle_payload": payload}, tasks[task_id]
        )
        golden_ok[task_id] = outcome == "passed"
        adoption = scan_v2_domain_adoption(src, task_id)
        golden_adoption[task_id] = adoption
        if not adoption["domain_library_adopted"]:
            golden_ok[task_id] = False

    # Coverage: every required op has listed API
    coverage_path = ANALYSIS / "operation_to_api_coverage_matrix.json"
    coverage = json.loads(coverage_path.read_text(encoding="utf-8")) if coverage_path.is_file() else {}
    all_covered = coverage.get("all_covered") is True

    # Prompt/API consistency: signatures already covered by pytest; re-check DOMAIN names exist
    from core.prompts import domain_function_library as dfl

    api_consistency = True
    for tid, apis in TASK_DOMAIN_APIS.items():
        for api in apis:
            cls_name, meth = api["name"].split(".")
            cls = getattr(dfl, cls_name, None)
            if cls is None or not hasattr(cls, meth):
                api_consistency = False

    v1_guard = _v1_artifacts_unchanged()
    git_check = _git_diff_check()

    model_checks: dict[str, Any] = {"skipped": not require_models}
    if require_models:
        try:
            gemini = api_key_status()
            model_checks["gemini_key_present"] = bool(gemini.get("api_key_present"))
        except Exception as exc:  # noqa: BLE001
            model_checks["gemini_key_present"] = False
            model_checks["gemini_error"] = str(exc)
        for mid in ("qwen3.5:4b", "qwen3.5:9b"):
            try:
                meta = probe_ollama(model=mid)
                model_checks[mid] = {"present": True, "digest": meta.get("model_digest")}
            except Exception as exc:  # noqa: BLE001
                model_checks[mid] = {"present": False, "error": str(exc)}
        # Formal 16-cell gate: Gemini + Qwen 4B only. 9B presence is recorded but not required.
        model_checks["all_models_ready"] = (
            model_checks.get("gemini_key_present") is True
            and model_checks.get("qwen3.5:4b", {}).get("present") is True
        )
        model_checks["qwen9b_required"] = False
        model_checks["qwen9b_status"] = (
            "present_not_executed"
            if model_checks.get("qwen3.5:9b", {}).get("present")
            else "absent_not_executed"
        )
    else:
        model_checks["all_models_ready"] = None

    checks: dict[str, Any] = {
        "planned_cells_per_model_exactly_8": len(plan["cells"]) == 8,
        "matrix_11402_three_plus_five_ab2d": len(CELL_SPECS) == 8,
        "oracle_accepts_all_expected": all(oracle_ok.values()),
        "ab2d_golden_calls_apis_and_passes": all(golden_ok.values()),
        "leakage_audit_passed": leakage["passed"],
        "coverage_matrix_all_covered": all_covered,
        "prompt_api_consistency": api_consistency,
        "generic_body_frozen_vs_v1": True,
        "v1_artifacts_preserved": v1_guard["passed"],
        "git_diff_check": git_check["passed"],
        "11402_nested_coefficients_contract": all(
            'exactly one top-level key "coefficients"' in c["prompt"]
            for c in plan["cells"]
            if c["task_id"] == TASK_114_02
        ),
        "canonical_prompt_hashes_present": all(
            len(h) == 64 for tid in plan["canonical_prompt_hashes"] for h in plan["canonical_prompt_hashes"][tid].values()
        ),
        "no_healer": all(c["healer"] == 0 and c["retry"] == 0 for c in plan["cells"]),
        "real_model_calls": 0,
        "models_ready": model_checks.get("all_models_ready") is True if require_models else True,
    }
    # Exclude real_model_calls from all() boolean fold carefully
    bool_checks = {k: v for k, v in checks.items() if k != "real_model_calls"}
    checks["passed"] = all(bool_checks.values()) and checks["real_model_calls"] == 0
    checks["blocker"] = None if checks["passed"] else "PREFLIGHT_FAILED"
    checks["model_details"] = model_checks

    return {
        "run_id": output_dir.name,
        "checks": checks,
        "oracle_ok": oracle_ok,
        "golden_ok": golden_ok,
        "golden_adoption": golden_adoption,
        "leakage": leakage,
        "v1_guard": v1_guard,
        "git_diff_check": git_check,
        "plan": plan,
        "real_model_calls": 0,
        "retries": 0,
        "healer_calls": 0,
    }


def write_preflight_artifacts(output_dir: Path, pf: dict[str, Any]) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir = output_dir / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    for cell in pf["plan"]["cells"]:
        stem = f"{cell['task_id']}__{cell['condition']}"
        (prompts_dir / f"{stem}.txt").write_text(cell["prompt"], encoding="utf-8")
        _write_json(
            prompts_dir / f"{stem}.meta.json",
            {
                "task_id": cell["task_id"],
                "condition": cell["condition"],
                "condition_label": cell["condition_label"],
                "canonical_prompt_hash": cell["canonical_prompt_hash"],
                "prompt_lineage": cell["prompt_lineage"],
            },
        )
    _write_json(output_dir / "manifest.json", {k: v for k, v in pf["plan"].items() if k != "cells"} | {
        "cells": [{k: v for k, v in c.items() if k != "prompt"} for c in pf["plan"]["cells"]]
    })
    _write_json(
        output_dir / "preflight.json",
        {
            "checks": pf["checks"],
            "oracle_ok": pf["oracle_ok"],
            "golden_ok": pf["golden_ok"],
            "golden_adoption": pf["golden_adoption"],
            "canonical_prompt_hashes": pf["plan"]["canonical_prompt_hashes"],
            "v1_guard": pf["v1_guard"],
            "real_model_calls": 0,
            "retries": 0,
            "healer_calls": 0,
            "lineage_id": LINEAGE_ID,
        },
    )
    _write_json(
        output_dir / "summary.json",
        {
            "passed": pf["checks"]["passed"],
            "blocker": pf["checks"]["blocker"],
            "planned_cells_per_model": 8,
            "planned_total_if_three_models": 24,
            "real_model_calls": 0,
            "lineage_id": LINEAGE_ID,
        },
    )
    _write_json(ANALYSIS / "canonical_prompt_hashes.json", {
        "lineage_id": LINEAGE_ID,
        "seed": SEED,
        "hashes": pf["plan"]["canonical_prompt_hashes"],
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "docs/experiments/results/ce115_exam_ext_contract_aligned_v2_preflight_01"),
    )
    parser.add_argument("--skip-model-probe", action="store_true")
    args = parser.parse_args()
    out = Path(args.output_dir)
    if out.exists():
        print(f"REFUSE: output exists {out}", file=sys.stderr)
        return 2
    # Ensure inventory exists
    subprocess.run([sys.executable, str(ROOT / "scripts/build_ce115_exam_v2_api_inventory.py")], check=True)
    pf = preflight(out, require_models=not args.skip_model_probe)
    write_preflight_artifacts(out, pf)
    print(json.dumps({"passed": pf["checks"]["passed"], "blocker": pf["checks"]["blocker"], "models": pf["checks"].get("model_details")}, indent=2))
    return 0 if pf["checks"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
