# -*- coding: utf-8 -*-
"""Zero-execution preflight for Qwen4B cell-wise fixpoint replay protocol v1.

Does not apply healers to the 232-cell population, does not call a model, and
does not execute formal fixpoint replay.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_qwen4b_cellwise_fixpoint_replay_v1 import (  # noqa: E402
    FormalExecutionBlocked,
    run_formal_fixpoint_replay,
    run_preflight,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Qwen4B cell-wise fixpoint replay preflight (zero-execution)"
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional path to write the preflight report JSON",
    )
    parser.add_argument(
        "--attempt-formal",
        action="store_true",
        help="Demonstrate that formal replay is blocked without authorization",
    )
    args = parser.parse_args(argv)

    report = run_preflight()
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text + "\n", encoding="utf-8", newline="\n")

    if args.attempt_formal:
        try:
            run_formal_fixpoint_replay(allow_formal_execution=False)
            print("ERROR: formal replay should have been blocked", file=sys.stderr)
            return 2
        except FormalExecutionBlocked as exc:
            print(f"formal_blocked_ok: {exc}")

    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
