"""Annotate Math16 Qwen run_001 artifacts as INVALID_INFRASTRUCTURE (additive only).

Does not delete or rewrite original cell content fields (raw_response, evaluator, etc.).
Adds outcome_validity + reasons at cell artifact and run-level JSON files.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUN_DIRS = [
    ROOT / "docs/experiments/results/qwen35_4b_math16_ab123_run_001",
    ROOT / "docs/experiments/results/qwen35_9b_math16_ab123_run_001",
]

REASONS = [
    "舊版 Ollama 0.32.0 無 RENDERER 支援",
    "不支援頂層 think 參數，致 thinking 內容混入輸出",
    "採樣參數與實際模式不匹配",
]

REASON_SUMMARY = (
    "舊版 Ollama 0.32.0 無 RENDERER 支援且不支援頂層 think 參數，"
    "致 thinking 內容混入輸出;採樣參數與實際模式不匹配"
)


def _annotation(run_id: str) -> dict:
    return {
        "outcome_validity": "INVALID_INFRASTRUCTURE",
        "outcome_validity_annotation": {
            "annotated_at": datetime.now(timezone.utc).isoformat(),
            "annotation_only": True,
            "original_content_unchanged": True,
            "superseding_run_expected": run_id.replace("run_001", "run_002"),
            "reasons": list(REASONS),
            "reason_summary": REASON_SUMMARY,
            "note": (
                "Post-hoc validity mark after call-layer forensic; "
                "raw_response / evaluator outcomes retained as-is."
            ),
        },
    }


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dump(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def annotate_run(run_dir: Path) -> dict:
    if not run_dir.is_dir():
        raise FileNotFoundError(run_dir)
    run_id = run_dir.name
    ann = _annotation(run_id)
    cells_dir = run_dir / "cells"
    cell_count = 0
    for artifact_path in sorted(cells_dir.glob("*/artifact.json")):
        data = _load(artifact_path)
        # Additive fields only; never strip existing keys.
        data["outcome_validity"] = ann["outcome_validity"]
        data["outcome_validity_annotation"] = ann["outcome_validity_annotation"]
        _dump(artifact_path, data)
        cell_count += 1

    for name in ("summary.json", "manifest.json", "cell_results.json", "checkpoint.json"):
        path = run_dir / name
        if not path.exists():
            continue
        data = _load(path)
        if isinstance(data, dict):
            data["outcome_validity"] = ann["outcome_validity"]
            data["outcome_validity_annotation"] = ann["outcome_validity_annotation"]
            _dump(path, data)
        elif isinstance(data, list):
            for row in data:
                if isinstance(row, dict):
                    row["outcome_validity"] = ann["outcome_validity"]
                    row["outcome_validity_annotation"] = ann["outcome_validity_annotation"]
            _dump(path, data)

    marker = run_dir / "OUTCOME_VALIDITY.json"
    _dump(
        marker,
        {
            "run_id": run_id,
            **ann,
            "cells_annotated": cell_count,
        },
    )
    return {"run_id": run_id, "cells_annotated": cell_count}


def main() -> int:
    results = [annotate_run(d) for d in RUN_DIRS]
    print(json.dumps({"annotated": results, "reasons": REASONS}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
