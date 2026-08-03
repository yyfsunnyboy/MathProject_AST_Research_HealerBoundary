# -*- coding: utf-8 -*-
"""Sequential orchestrator for Math16 Ab2d V2 menu-vs-full formal 480 cells.

Hard order: Gemini (both V2 conditions) → audit → Qwen 9B → audit → Qwen 4B → final audit.
No parallel / interleaved model execution. V2 prompts + V2 artifact root only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_ab2d_v2_formal_execution import (
    CONDITION_ORDER,
    EXPERIMENT_ID,
    MODEL_ORDER,
    assert_prior_model_audit_passed,
    audit_cell_plan,
    completeness_report,
    run_model_condition,
    zero_model_preflight_480,
)


def integrity_audit_model(model_key: str) -> dict[str, Any]:
    reports = {
        condition: completeness_report(condition, model_key) for condition in CONDITION_ORDER
    }
    complete = sum(r["complete"] for r in reports.values())
    planned = sum(r["planned"] for r in reports.values())
    ok = all(r["all_complete"] for r in reports.values()) and planned == 160
    return {
        "model_key": model_key,
        "planned": planned,
        "complete": complete,
        "pipeline_complete_160": ok,
        "by_condition": reports,
        "ok": ok,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight", action="store_true", help="Zero-model V2 480-cell preflight.")
    parser.add_argument(
        "--dry-run-all",
        action="store_true",
        help="Dry-run all six V2 runners in sequence (zero model calls).",
    )
    parser.add_argument(
        "--execute-sequence",
        action="store_true",
        help="Live sequential formal run with hard audits between models.",
    )
    args = parser.parse_args(argv)

    if args.preflight:
        result = zero_model_preflight_480()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["overall_pass"] else 2

    if args.dry_run_all:
        # Ensure manifests exist, then dry-run all six runners.
        pre = zero_model_preflight_480()
        if not pre["overall_pass"]:
            print(json.dumps({"mode": "dry_run_all", "preflight": pre}, indent=2))
            return 2
        plan = audit_cell_plan(both_conditions=True)
        rows = []
        for model_key in MODEL_ORDER:
            for condition in CONDITION_ORDER:
                rows.append(
                    run_model_condition(
                        condition=condition,
                        model_key=model_key,
                        dry_run=True,
                        execute_api=False,
                    )
                )
        out = {
            "mode": "dry_run_all",
            "experiment_id": EXPERIMENT_ID,
            "preflight_ok": pre["overall_pass"],
            "plan_audit": plan,
            "runners": rows,
            "model_calls": sum(r["model_calls"] for r in rows),
            "parameter_authority": "artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/model_settings.json",
            "artifact_root": "artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2",
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if plan["ok"] and out["model_calls"] == 0 else 2

    if args.execute_sequence:
        audits = []
        for model_key in MODEL_ORDER:
            assert_prior_model_audit_passed(model_key)
            for condition in CONDITION_ORDER:
                run_model_condition(
                    condition=condition,
                    model_key=model_key,
                    execute_api=True,
                    dry_run=False,
                )
            audit = integrity_audit_model(model_key)
            audits.append(audit)
            if not audit["ok"]:
                print(json.dumps({"stopped_after": model_key, "audit": audit}, indent=2))
                return 3
        final = integrity_audit_model("qwen_4b")
        print(
            json.dumps(
                {
                    "verdict": "FORMAL_V2_480_COMPLETE",
                    "experiment_id": EXPERIMENT_ID,
                    "audits": audits,
                    "final_audit": final,
                },
                indent=2,
            )
        )
        return 0

    parser.error("Specify --preflight, --dry-run-all, or --execute-sequence")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
