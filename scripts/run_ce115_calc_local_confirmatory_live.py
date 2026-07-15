#!/usr/bin/env python3
"""Milestone 4A — live formal local confirmatory run (frozen 72-cell plan).

Injects local Ollama transport into ce115_calc_formal_runner.run_local_confirmatory.
Resume skips valid executed cells; never overwrites artifacts; no retry; no Healer.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
EXPECTED_DIGESTS = {
    "qwen3.5:4b": "2a654d98e6fb",
    "qwen3.5:9b": "6488c96fa5fa",
}
EXPECTED_OLLAMA_VERSION_PREFIX = "0.32.0"


def _http_json(url: str, *, data: bytes | None = None, timeout_s: float) -> Any:
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310 — local Ollama
        return json.loads(resp.read().decode("utf-8"))


def qualify_ollama(*, base_url: str, timeout_s: float) -> dict[str, Any]:
    tags = _http_json(base_url.rstrip("/") + "/api/tags", timeout_s=timeout_s)
    models = {m["name"]: m for m in tags.get("models") or [] if isinstance(m, dict) and m.get("name")}
    checked: dict[str, str] = {}
    for tag, prefix in EXPECTED_DIGESTS.items():
        entry = models.get(tag)
        if entry is None:
            raise RuntimeError(f"required model missing from Ollama: {tag}")
        digest = str(entry.get("digest") or "")
        if prefix not in digest:
            raise RuntimeError(f"digest mismatch for {tag}: expected prefix {prefix}, got {digest}")
        checked[tag] = digest
    return {"models": checked, "model_count": len(models)}


def _make_ollama_transport(
    *,
    base_url: str,
    timeout_s: float,
    call_counter: dict[str, int],
    progress_path: Path,
    max_calls: int | None,
):
    def transport(payload: dict[str, Any]) -> dict[str, Any]:
        call_counter["model_calls"] = int(call_counter.get("model_calls", 0)) + 1
        n = call_counter["model_calls"]
        if max_calls is not None and n > max_calls:
            raise RuntimeError(f"refusing model call #{n}: exceeds max_calls={max_calls}")

        if payload.get("think") is not False:
            raise RuntimeError(f"payload.think must be false, got {payload.get('think')!r}")
        options = payload.get("options") or {}
        if options.get("temperature") != 0.0:
            raise RuntimeError(f"temperature must be 0.0, got {options.get('temperature')!r}")
        if "seed" not in options:
            raise RuntimeError("seed missing from request options")
        for forbidden in ("top_p", "top_k", "presence_penalty", "num_predict"):
            if forbidden in options:
                raise RuntimeError(f"forbidden option present: {forbidden}")
        model = payload.get("model")
        if model not in EXPECTED_DIGESTS:
            raise RuntimeError(f"unexpected model tag in payload: {model!r}")

        started = time.time()
        data = json.dumps(payload).encode("utf-8")
        body = _http_json(base_url.rstrip("/") + "/api/chat", data=data, timeout_s=timeout_s)
        elapsed = time.time() - started
        progress_path.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "call_index": n,
            "model": model,
            "seed": options.get("seed"),
            "elapsed_s": round(elapsed, 3),
            "eval_count": body.get("eval_count"),
            "total_duration": body.get("total_duration"),
        }
        with progress_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event, ensure_ascii=False) + "\n")
            fh.flush()
        print(
            f"[m4a] model_call={n} model={model} seed={options.get('seed')} "
            f"elapsed_s={elapsed:.1f}",
            flush=True,
        )
        return body

    return transport


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CE115 formal local confirmatory live run")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "docs/experiments/manifests/ce115_calc_main_experiment_manifest.json",
    )
    parser.add_argument("--local-confirmatory", action="store_true", required=True)
    parser.add_argument("--write-artifacts", action="store_true", required=True)
    parser.add_argument("--resume", action="store_true", default=True)
    parser.add_argument("--no-resume", action="store_true", help="Disable resume (dangerous).")
    parser.add_argument("--ollama-url", type=str, default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument(
        "--max-calls",
        type=int,
        default=71,
        help="Safety cap on new model calls this session (default 71 remaining).",
    )
    parser.add_argument(
        "--progress-log",
        type=Path,
        default=ROOT / "docs/experiments/logs/ce115_m4a_run_progress.jsonl",
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=ROOT / "docs/experiments/logs/ce115_m4a_run_summary.json",
    )
    parser.add_argument(
        "--expected-ollama-version",
        type=str,
        default=EXPECTED_OLLAMA_VERSION_PREFIX,
    )
    args = parser.parse_args(argv)

    if args.no_resume:
        print("error: --no-resume refused for formal confirmatory safety", file=sys.stderr)
        return 2

    from agent_tools.finals_rebuild.ce115_calc_formal_runner import (
        FormalRunnerError,
        load_executed_cell_ids,
        run_local_confirmatory,
    )

    results_dir = ROOT / "docs/experiments/results/ce115_calc_local_confirmatory"
    before = load_executed_cell_ids(results_dir)
    print(
        json.dumps(
            {
                "phase": "preflight",
                "already_executed": len(before),
                "already_cell_ids": sorted(before),
                "max_calls": args.max_calls,
            },
            ensure_ascii=False,
            indent=2,
        ),
        flush=True,
    )

    try:
        qual = qualify_ollama(base_url=args.ollama_url, timeout_s=30.0)
    except Exception as exc:  # noqa: BLE001
        print(f"error: ollama qualification failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3

    # Best-effort version check via CLI text if present in env; digest check is authoritative.
    print(json.dumps({"ollama_qualification": qual}, ensure_ascii=False, indent=2), flush=True)

    call_counter = {"model_calls": 0}
    transport = _make_ollama_transport(
        base_url=args.ollama_url,
        timeout_s=args.timeout,
        call_counter=call_counter,
        progress_path=args.progress_log,
        max_calls=args.max_calls,
    )

    started = time.time()
    try:
        result = run_local_confirmatory(
            args.manifest,
            transport=transport,
            repo_root=ROOT,
            write_artifacts=True,
            resume=True,
            run_id="ce115_calc_local_confirmatory",
            cell_limit=args.max_calls,
        )
    except FormalRunnerError as exc:
        print(f"error: formal runner blocked: {exc}", file=sys.stderr)
        return 4
    except (urllib.error.URLError, TimeoutError, RuntimeError, OSError) as exc:
        print(f"error: transport/runtime failure: {type(exc).__name__}: {exc}", file=sys.stderr)
        after = load_executed_cell_ids(results_dir)
        summary = {
            "status": "BLOCKED",
            "error": f"{type(exc).__name__}: {exc}",
            "elapsed_s": round(time.time() - started, 3),
            "model_calls_this_session": call_counter["model_calls"],
            "executed_before": len(before),
            "executed_after": len(after),
            "executed_cell_ids_after": sorted(after),
        }
        args.summary_out.parent.mkdir(parents=True, exist_ok=True)
        args.summary_out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 5

    after = load_executed_cell_ids(results_dir)
    summary = {
        "status": "OK",
        "elapsed_s": round(time.time() - started, 3),
        "planned_cells": result.get("planned_cells"),
        "selected_cells": result.get("selected_cells"),
        "executed_cells_this_session": result.get("executed_cells"),
        "skipped_executed_cells": result.get("skipped_executed_cells"),
        "transport_calls": result.get("transport_calls"),
        "model_calls_this_session": call_counter["model_calls"],
        "executed_before": len(before),
        "executed_after": len(after),
        "executed_cell_ids_after": sorted(after),
        "manifest_hash": result.get("manifest_hash"),
        "local_confirmatory_frozen": result.get("local_confirmatory_frozen"),
        "outcomes": {
            str(r.get("outcome")): sum(1 for x in (result.get("rows") or []) if x.get("outcome") == r.get("outcome"))
            for r in (result.get("rows") or [])
        },
        "session_row_outcomes": [r.get("outcome") for r in (result.get("rows") or [])],
        "session_row_cell_ids": [r.get("cell_id") for r in (result.get("rows") or [])],
    }
    # Fix outcomes aggregation properly
    outcome_counts: dict[str, int] = {}
    for row in result.get("rows") or []:
        key = str(row.get("outcome"))
        outcome_counts[key] = outcome_counts.get(key, 0) + 1
    summary["outcomes"] = outcome_counts

    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)

    if len(after) != 72:
        print(
            f"warning: executed_after={len(after)} expected 72 "
            f"(session_new={result.get('executed_cells')})",
            file=sys.stderr,
        )
        return 6
    if call_counter["model_calls"] != int(result.get("transport_calls") or -1):
        print("error: call counter drift", file=sys.stderr)
        return 7
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
