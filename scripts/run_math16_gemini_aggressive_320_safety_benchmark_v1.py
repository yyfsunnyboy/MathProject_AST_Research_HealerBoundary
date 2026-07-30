# -*- coding: utf-8 -*-
"""Gated formal entrypoint for Gemini Aggressive 320-cell safety benchmark v1.

Default behavior refuses formal 320-cell execution and does not invoke the
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

from agent_tools.finals_rebuild.math16_gemini_aggressive_320_safety_benchmark_v1 import (  # noqa: E402
    FormalExecutionBlocked,
    run_formal_safety_benchmark,
    run_preflight,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Gemini Aggressive 320-cell safety benchmark runner (formal gated)"
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
        help="Authorize formal 320-cell benchmark (blocked unless explicitly set)",
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
            run_formal_safety_benchmark(
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
        f"ok={report['ok']} n={report['population']['n_cells']} "
        f"pass={report['population']['n_input_pass']} "
        f"fail={report['population']['n_input_fail']} "
        f"formal_benchmark_executed={report['formal_benchmark_executed']} "
        f"evaluator_invocations={report['evaluator_invocations']}"
    )
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
