# -*- coding: utf-8 -*-
"""Shared CLI for Math16 Ab2d formal runners (Math16 settings authority)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_ab2d_formal_execution import (  # noqa: E402
    MODEL_ORDER,
    assert_prior_model_audit_passed,
    audit_cell_plan,
    completeness_report,
    run_model_condition,
    zero_model_preflight_480,
)


def build_parser(condition: str, model_key: str) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            f"Math16 Ab2d formal runner: condition={condition} model={model_key}. "
            "Parameters from Math16 frozen model_settings (not CE115)."
        )
    )
    p.add_argument("--dry-run", action="store_true", help="Plan/verify only; zero model calls.")
    p.add_argument(
        "--execute-api",
        action="store_true",
        help="Live formal generation (fail-closed unless explicitly set).",
    )
    p.add_argument(
        "--preflight",
        action="store_true",
        help="Rebuild manifests + audit 480-cell plan (zero model calls).",
    )
    p.add_argument(
        "--completeness",
        action="store_true",
        help="Report complete/incomplete cells for this condition/model.",
    )
    p.add_argument(
        "--enforce-sequence",
        action="store_true",
        help="Require prior model 160/160 complete before execute-api.",
    )
    return p


def run_cli(condition: str, model_key: str, argv: list[str] | None = None) -> int:
    if model_key not in MODEL_ORDER:
        raise SystemExit(f"invalid model_key: {model_key}")
    parser = build_parser(condition, model_key)
    args = parser.parse_args(argv)

    if args.preflight:
        result = zero_model_preflight_480()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["overall_pass"] else 2

    if args.completeness:
        report = completeness_report(condition, model_key)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["all_complete"] else 1

    if args.execute_api:
        if args.enforce_sequence:
            assert_prior_model_audit_passed(model_key)
        summary = run_model_condition(
            condition=condition, model_key=model_key, execute_api=True, dry_run=False
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    if args.dry_run:
        summary = run_model_condition(
            condition=condition, model_key=model_key, execute_api=False, dry_run=True
        )
        plan = audit_cell_plan(both_conditions=True)
        out: dict[str, Any] = {"runner": summary, "plan_audit": plan}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if summary["model_calls"] == 0 else 2

    parser.error("Specify --dry-run, --preflight, --completeness, or --execute-api")
    return 2
