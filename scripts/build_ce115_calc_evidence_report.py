#!/usr/bin/env python3
"""Build offline CE115 calc HTML evidence report (no model / Healer / formal run)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.ce115_calc_evidence_report import (  # noqa: E402
    DEFAULT_MANIFEST,
    DEFAULT_RESULTS_DIR,
    DEFAULT_REVIEWS,
    build_evidence_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    parser.add_argument("--reviews", type=Path, default=DEFAULT_REVIEWS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--fixture-jsonl",
        type=Path,
        default=None,
        help="Optional non-formal fixture JSONL (skips empty formal results).",
    )
    parser.add_argument(
        "--skip-renderer",
        action="store_true",
        help="Build HTML/dataset without launching browser (G6b becomes incomplete).",
    )
    args = parser.parse_args(argv)

    executed_rows = None
    planned_cells = None
    if args.fixture_jsonl is not None:
        rows = []
        for line in args.fixture_jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        executed_rows = rows
        # Fixture-only reports: synthesize planned skeleton from rows + mark missing as planned.
        planned_cells = [
            {
                "cell_id": r["cell_id"],
                "task_id": r.get("task_id"),
                "model_tag": r.get("model_tag"),
                "prompt_condition": r.get("prompt_condition"),
                "seed": r.get("seed"),
                "difficulty": r.get("difficulty") or "l1",
                "prompt_text": r.get("prompt_text"),
                "prompt_hash": r.get("prompt_hash"),
                "output_path": r.get("output_path"),
                "retry_count": r.get("retry_count", 0),
            }
            for r in rows
            if r.get("cell_id")
        ]

    result = build_evidence_report(
        out_dir=args.out_dir,
        results_dir=args.results_dir,
        reviews_path=args.reviews,
        manifest_path=args.manifest,
        planned_cells=planned_cells,
        executed_rows=executed_rows,
        run_renderer=not args.skip_renderer,
        repo_root=ROOT,
    )
    print(json.dumps({
        "out_dir": result["out_dir"],
        "cell_count": result["cell_count"],
        "summary": {
            "planned": result["summary"]["planned"],
            "executed": result["summary"]["executed"],
            "failed": result["summary"]["failed"],
        },
        "call_counts": result["call_counts"],
        "meta": {
            "artifact_hash": result["meta"]["artifact_hash"],
            "report_dataset_hash": result["meta"]["report_dataset_hash"],
            "report_build_hash": result["meta"]["report_build_hash"],
            "browser_summary": result["meta"].get("browser_summary"),
            "formal_artifacts_unchanged": result["meta"].get("formal_artifacts_unchanged"),
        },
    }, ensure_ascii=False, indent=2))
    if result["call_counts"]["model_calls"] != 0:
        return 2
    if result["call_counts"]["healer_calls"] != 0:
        return 3
    if result["call_counts"]["network_calls"] != 0:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
