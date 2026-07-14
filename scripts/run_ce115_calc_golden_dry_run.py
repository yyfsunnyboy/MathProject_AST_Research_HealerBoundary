#!/usr/bin/env python3
"""No-model infrastructure dry run for corrected CE115 calc L1 tasks.

Guarantees: no Ollama, Gemini, HTTP, or network clients are imported or called.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Explicit offline surface — do not import generation runners or HTTP clients.
from agent_tools.finals_rebuild.ce115_calc_golden_dry_run import (  # noqa: E402
    run_golden_dry_run,
    write_dry_run_summary,
)

DEFAULT_OUTPUT = ROOT / "tests" / "finals_rebuild" / "artifacts" / "ce115_calc_golden_dry_run.jsonl"
DEFAULT_SUMMARY = ROOT / "tests" / "finals_rebuild" / "artifacts" / "ce115_calc_golden_dry_run_summary.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synthetic no-model CE115 calc infrastructure dry run")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--run-id", default="ce115-calc-golden-dry-run")
    args = parser.parse_args(argv)
    records = run_golden_dry_run(output_path=args.output, run_id=args.run_id)
    write_dry_run_summary(records, args.summary)
    print(
        f"wrote {len(records)} synthetic dry-run records to {args.output} "
        f"(full PASS {sum(r['composite_outcomes']['full_pass'] == 'PASS' for r in records)}/{len(records)}; "
        "model_called=false; excluded from formal analysis)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
