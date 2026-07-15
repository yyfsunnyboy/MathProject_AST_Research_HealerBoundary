#!/usr/bin/env python3
"""Formal CE115 local confirmatory runner entry point.

Milestone 3D: only --plan-only is exercised (no model calls).

  python scripts/run_ce115_calc_local_confirmatory.py \\
    --manifest docs/experiments/manifests/ce115_calc_main_experiment_manifest.json \\
    --plan-only
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _plan_only(manifest: Path) -> int:
    # Plan-only must not import formal runner / pilot / Ollama transport.
    from agent_tools.finals_rebuild.ce115_calc_run_plan import (
        assert_no_transport_imports_in_source,
        plan_summary_for_cli,
        run_preflight,
    )

    assert_no_transport_imports_in_source(Path(__file__).read_text(encoding="utf-8"))
    summary = run_preflight(manifest, repo_root=ROOT, write_results=False)
    payload = plan_summary_for_cli(summary)
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"planned_cells={payload['planned_cells']}")
    print(f"local_confirmatory_frozen={str(payload['local_confirmatory_frozen']).lower()}")
    print(f"prompt_hash_mismatches={payload['prompt_hash_mismatches']}")
    print(f"request_setting_mismatches={payload['request_setting_mismatches']}")
    print(f"existing_output_conflicts={payload['existing_output_conflicts']}")
    print(f"model_calls={payload['model_calls']}")
    print(f"verdict={payload['verdict']}")
    return 0 if payload["verdict"] == "READY" else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CE115 local confirmatory formal runner")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "docs/experiments/manifests/ce115_calc_main_experiment_manifest.json",
    )
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Validate frozen 72-cell plan without calling any model transport.",
    )
    parser.add_argument(
        "--local-confirmatory",
        action="store_true",
        help="Explicit confirmatory mode flag (required with --plan-only for clarity).",
    )
    args = parser.parse_args(argv)

    if args.plan_only:
        return _plan_only(args.manifest)

    print(
        "error: live confirmatory execution is not enabled in this milestone; "
        "pass --plan-only (and optionally --local-confirmatory)",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
