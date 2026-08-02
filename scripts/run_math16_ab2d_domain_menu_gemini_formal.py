# -*- coding: utf-8 -*-
"""Math16 Ab2d+domain-menu Gemini formal runner.

Default is fail-closed (no live calls without ``--execute-api``).
Live parameters come from Math16 frozen model_settings (not CE115).
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

from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (
    ARTIFACT_ROOT_REL,
    CONDITION,
    EXPERIMENT_ID,
    MANIFEST_REL,
    PROMPT_DIR_REL,
    TEMPLATE_DIR_REL,
    run_zero_model_preflight,
)
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest

FORMAL_RUNNER_REL = "scripts/run_math16_ab2d_domain_menu_gemini_formal.py"
QUAL_ROOT = ROOT / ARTIFACT_ROOT_REL / "qualification"
FORMAL_ROOT = ROOT / ARTIFACT_ROOT_REL / "formal" / "gemini"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integration_check() -> dict[str, Any]:
    pool = load_pool_manifest(ROOT)
    manifest_path = ROOT / MANIFEST_REL
    if not manifest_path.exists():
        run_zero_model_preflight(ROOT)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    prompt_dir = ROOT / PROMPT_DIR_REL
    n_prompts = len(list(prompt_dir.glob("*.txt"))) if prompt_dir.exists() else 0
    return {
        "condition": CONDITION,
        "experiment_id": EXPERIMENT_ID,
        "formal_runner_path": FORMAL_RUNNER_REL,
        "qualification_root": str(QUAL_ROOT).replace("\\", "/"),
        "formal_output_root": str(FORMAL_ROOT).replace("\\", "/"),
        "manifest_path": MANIFEST_REL,
        "template_dir": TEMPLATE_DIR_REL,
        "prompt_dir": PROMPT_DIR_REL,
        "n_prompts_on_disk": n_prompts,
        "n_tasks_expected": 16,
        "pool_identity_hash": pool["pool_identity_hash"],
        "task_freeze_hash": pool["task_freeze_hash"],
        "manifest_id": manifest.get("manifest_id"),
        "domain_blocks_byte_identical": manifest.get("domain_blocks_byte_identical"),
        "model_calls": 0,
        "execute_api_enabled": False,
        "parameter_authority": (
            "artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/model_settings.json"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--integration-check",
        action="store_true",
        help="Print runner/namespace metadata (zero model calls).",
    )
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="Run zero-model domain-menu prompt preflight.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Verify Math16 formal 80-cell plan (zero model calls).",
    )
    parser.add_argument(
        "--execute-api",
        action="store_true",
        help="Live formal generation (explicit opt-in; Math16 settings).",
    )
    args = parser.parse_args(argv)

    if args.preflight:
        summary = run_zero_model_preflight(ROOT)
        print(
            json.dumps(
                {
                    k: summary[k]
                    for k in (
                        "preflight_id",
                        "n_prompts",
                        "prompts_complete",
                        "domain_blocks_byte_identical",
                        "cross_domain_isolation_ok",
                        "solution_plan_clean",
                        "answer_leakage_clean",
                        "overall_pass",
                        "model_calls",
                    )
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0 if summary["overall_pass"] else 1

    if args.integration_check:
        info = integration_check()
        info["formal_runner_sha256"] = sha256_file(ROOT / FORMAL_RUNNER_REL)
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return 0 if info["n_prompts_on_disk"] == 16 else 1

    if args.dry_run or args.execute_api:
        from agent_tools.finals_rebuild.math16_ab2d_formal_execution import run_model_condition

        summary = run_model_condition(
            condition="ab2d_domain_menu",
            model_key="gemini",
            dry_run=bool(args.dry_run),
            execute_api=bool(args.execute_api),
        )
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    # Fail-closed default: no live path without --execute-api.
    raise SystemExit(
        "EXECUTE_API_BLOCKED: pass --execute-api for live formal generation, "
        "or use --dry-run / --integration-check / --preflight."
    )


if __name__ == "__main__":
    raise SystemExit(main())
