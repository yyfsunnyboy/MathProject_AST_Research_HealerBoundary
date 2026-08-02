# -*- coding: utf-8 -*-
"""Zero-model preflight entry for Math16 Ab2d+domain-menu."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_ab2d_domain_menu import run_zero_model_preflight


def main() -> int:
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
                    "evaluator_reference_smoke_all_pass",
                    "model_calls",
                    "overall_pass",
                    "domain_block_hashes",
                    "namespace",
                )
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if summary["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
