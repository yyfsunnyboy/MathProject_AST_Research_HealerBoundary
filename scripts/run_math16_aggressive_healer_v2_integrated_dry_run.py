# -*- coding: utf-8 -*-
"""Aggressive Healer v2 integrated dry-run (zero model, zero formal evaluator)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.aggressive_healer_v2_integrated import (  # noqa: E402
    run_integrated_dry_run_480,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run-all", action="store_true")
    args = p.parse_args(argv)
    if not args.dry_run_all:
        p.error("Specify --dry-run-all")
    summary = run_integrated_dry_run_480(write=True)
    print(
        json.dumps(
            {
                "n_cells": summary["n_cells"],
                "changed": summary["changed"],
                "unchanged": summary["unchanged"],
                "pass_source_modification": summary["pass_source_modification"],
                "pass_pc_accept": summary["pass_pc_accept"],
                "known6_all_match": summary["known6_all_match"],
                "known6_match": summary["known6_match"],
                "stop_reason_counts": summary["stop_reason_counts"],
                "cycle_n": summary["cycle_n"],
                "max_round_n": summary["max_round_n"],
                "certificate_pass": summary["certificate_pass"],
                "certificate_fail": summary["certificate_fail"],
                "pc_rule_accept_counts": summary["pc_rule_accept_counts"],
                "safety_pass": summary["safety_pass"],
                "ready": summary["ready"],
                "integrated_sequence": summary["integrated_sequence"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if summary["ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
