# -*- coding: utf-8 -*-
"""Run Contract Checker schema coverage audit (zero model / zero evaluator)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.aggressive_healer_contract_v2.checker_audit import (  # noqa: E402
    run_checker_schema_audit,
)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--audit", action="store_true", help="Run full residual+PASS schema audit")
    args = p.parse_args(argv)
    if not args.audit:
        p.error("Specify --audit")
    summary = run_checker_schema_audit(write=True)
    print(
        json.dumps(
            {
                "n_residual_fail": summary["n_residual_fail"],
                "decision_distribution": summary["decision_distribution"],
                "dimension_violation_counts": summary["dimension_violation_counts"],
                "ast_uncheckable_n": summary["ast_uncheckable_n"],
                "ast_uncheckable_correct": summary["ast_uncheckable_correct"],
                "rewrite13": summary["rewrite13"],
                "menu_78": {
                    "n": summary["menu_78"]["n"],
                    "full_plan_process_violation_misapply": summary["menu_78"][
                        "full_plan_process_violation_misapply"
                    ],
                    "ok": summary["menu_78"]["ok"],
                },
                "pass_381": summary["pass_381"],
                "known6_all_match": summary["known6"]["all_match"],
                "ready": summary["ready"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if summary["ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
