"""One-shot live smoke test for Math16 Qwen Ollama adapter.

Uses a non-Math16 fixed prompt. Marks output as smoke_test and never writes
into formal Math16 / Ab2d-v2 result directories.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.math16_qwen_ollama_adapter import (  # noqa: E402
    DEFAULT_BASE_URL,
    MODEL_ID,
    build_cell_generation_record,
    call_qwen_with_retries,
    frozen_inference_config,
    probe_ollama,
)

SMOKE_PROMPT = "print hello"
SMOKE_LABEL = "smoke_test"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Optional output directory (default: system temp, never formal results).",
    )
    args = parser.parse_args()

    out_dir = args.output_dir
    if out_dir is None:
        out_dir = Path(tempfile.mkdtemp(prefix="math16_qwen_ollama_adapter_smoke_"))
    else:
        out_dir = out_dir.resolve()
        formal_root = (ROOT / "docs/experiments/results").resolve()
        if out_dir == formal_root or formal_root in out_dir.parents:
            # Allow only an explicit nonformal smoke subtree.
            if "_smoke_nonformal" not in out_dir.parts:
                raise SystemExit(
                    "Refusing to write smoke output under formal docs/experiments/results "
                    "unless path includes _smoke_nonformal."
                )
    out_dir.mkdir(parents=True, exist_ok=True)

    probe = probe_ollama(base_url=DEFAULT_BASE_URL, model=MODEL_ID)
    started = time.monotonic()
    response = call_qwen_with_retries(SMOKE_PROMPT, base_url=DEFAULT_BASE_URL, model=MODEL_ID)
    wall = time.monotonic() - started
    record = build_cell_generation_record(response)
    artifact = {
        "smoke_test": True,
        "label": SMOKE_LABEL,
        "formal_run": False,
        "math16_pool": False,
        "prompt": SMOKE_PROMPT,
        "probe": probe,
        "frozen_inference_config": frozen_inference_config(),
        "response": record,
        "wall_clock_seconds_total": wall,
        "raw_text_preview": (response["raw_text"] or "")[:500],
    }

    raw_path = out_dir / "raw_response.txt"
    artifact_path = out_dir / "smoke_artifact.json"
    raw_path.write_text(response["raw_text"], encoding="utf-8", newline="\n")
    artifact_path.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    summary = {
        "passed": bool(str(response["raw_text"]).strip()),
        "smoke_test": True,
        "model": MODEL_ID,
        "wall_clock_seconds": wall,
        "api_attempt_count": record["api_attempt_count"],
        "eval_count": record["token_metadata"].get("eval_count"),
        "output_dir": str(out_dir),
        "raw_response_chars": len(response["raw_text"]),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
