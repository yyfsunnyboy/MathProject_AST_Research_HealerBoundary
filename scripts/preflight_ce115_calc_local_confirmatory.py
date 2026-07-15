#!/usr/bin/env python3
"""Zero-model preflight for CE115 local confirmatory 72-cell expansion.

Usage:
  python scripts/preflight_ce115_calc_local_confirmatory.py \\
    --manifest docs/experiments/manifests/ce115_calc_main_experiment_manifest.json \\
    --dry-run

Never calls Ollama, Gemini, HTTP clients, or model subprocesses.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Pure planning only — do not import math_boundary_pilot or any transport layer.
from agent_tools.finals_rebuild.ce115_calc_run_plan import (  # noqa: E402
    assert_no_transport_imports_in_source,
    module_source_guard,
    plan_summary_for_cli,
    run_preflight,
)


def _guard_this_script() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    assert_no_transport_imports_in_source(source)
    module_source_guard()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CE115 local confirmatory zero-model preflight")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "docs/experiments/manifests/ce115_calc_main_experiment_manifest.json",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        required=True,
        help="Required. Expand and validate plan only; never call models or write formal results.",
    )
    args = parser.parse_args(argv)
    if not args.dry_run:
        print("error: --dry-run is required", file=sys.stderr)
        return 2

    _guard_this_script()
    summary = run_preflight(args.manifest, repo_root=ROOT, write_results=False)
    payload = plan_summary_for_cli(summary)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"planned_cells = {payload['planned_cells']}")
    print(f"duplicate_cells = {payload['duplicate_cells']}")
    print(f"duplicate_paths = {payload['duplicate_paths']}")
    print(f"prompt_hash_mismatches = {payload['prompt_hash_mismatches']}")
    print(f"request_setting_mismatches = {payload['request_setting_mismatches']}")
    print(f"model_calls = {payload['model_calls']}")
    print(f"verdict = {payload['verdict']}")
    return 0 if payload["verdict"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
