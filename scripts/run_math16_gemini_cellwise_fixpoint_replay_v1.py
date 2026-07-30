# -*- coding: utf-8 -*-
"""Gated formal entrypoint for Gemini cell-wise fixpoint replay v1.

Default behavior refuses formal 31-cell execution and does not invoke the
observational evaluator. Authorized runs require ``--allow-formal-execution``
plus either an injected callback or ``--inject-authoritative-evaluator``.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_gemini_cellwise_fixpoint_replay_v1 import (  # noqa: E402
    FormalExecutionBlocked,
    run_formal_fixpoint_replay,
    run_preflight,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gemini cell-wise fixpoint replay runner (formal gated)"
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        default=True,
        help="Run zero-execution preflight only (default)",
    )
    parser.add_argument(
        "--allow-formal-execution",
        action="store_true",
        help="Authorize formal 31-cell replay (blocked unless explicitly set)",
    )
    parser.add_argument(
        "--inject-authoritative-evaluator",
        action="store_true",
        help=(
            "When formal execution is authorized, inject the pinned Math16 "
            "observational evaluator factory"
        ),
    )
    args = parser.parse_args(argv)

    if args.allow_formal_execution:
        try:
            run_formal_fixpoint_replay(
                allow_formal_execution=True,
                inject_authoritative_evaluator=args.inject_authoritative_evaluator,
            )
        except FormalExecutionBlocked as exc:
            print(f"blocked: {exc}", file=sys.stderr)
            return 2
        except Exception as exc:  # noqa: BLE001
            print(f"formal_refused: {exc}", file=sys.stderr)
            return 2
        return 0

    report = run_preflight()
    print(
        "preflight_only "
        f"ok={report['ok']} active={report['population']['active_fail_n']} "
        f"excluded={report['population']['excluded_pass_n']} "
        f"formal_replay_executed={report['formal_replay_executed']} "
        f"evaluator_invocations={report['evaluator_invocations']}"
    )
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
