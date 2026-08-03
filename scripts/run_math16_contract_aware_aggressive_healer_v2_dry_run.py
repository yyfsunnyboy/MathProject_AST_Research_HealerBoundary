# -*- coding: utf-8 -*-
"""CLI dry-run for Contract-Aware Aggressive Healer v2 (no LLM, no formal overwrite)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.aggressive_healer_contract_v2.pipeline import (  # noqa: E402
    run_frozen_validation_bundle,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run-all", action="store_true", help="Build contracts, freeze, validate.")
    args = p.parse_args(argv)
    if not args.dry_run_all:
        p.error("Specify --dry-run-all")
    result = run_frozen_validation_bundle(write_artifacts=True)
    s = result["summary"]
    print(
        json.dumps(
            {
                "contracts_loaded": s["contracts_loaded"],
                "rule_accept_counts": s["rule_accept_counts"],
                "rule_abstain_counts": s["rule_abstain_counts"],
                "development_n_accept_cells": s["development_replay"]["n_accept_cells"],
                "development_accept_cells": s["development_replay"]["accept_cells"],
                "safety": s["safety_benchmark_381"],
                "menu": {
                    "n": s["menu_validation_78"]["n_cells"],
                    "n_with_repair": s["menu_validation_78"]["n_with_proposed_repair"],
                    "full_plan_forced": s["menu_validation_78"]["full_plan_rules_forced_count"],
                },
                "frozen_manifest_sha256": s["frozen_manifest_sha256"],
                "rules_modified_after_freeze": s["rules_modified_after_freeze"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    # Gate readiness
    ok = (
        s["contracts_loaded"] == 32
        and s["safety_benchmark_381"]["source_modification"] == 0
        and s["safety_benchmark_381"]["proposed_repair"] == 0
        and s["menu_validation_78"]["full_plan_rules_forced_count"] == 0
        and s["rules_modified_after_freeze"] is False
    )
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
