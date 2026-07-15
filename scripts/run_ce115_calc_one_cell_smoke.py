#!/usr/bin/env python3
"""Milestone 3F — one-cell live confirmatory smoke via formal runner + injected Ollama.

Uses frozen cell.prompt_text / prompt_hash / request settings / output path.
Exactly one model call; no retry; no Healer.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
EXPECTED_DIGEST_PREFIX = "2a654d98e6fb"


def _make_ollama_transport(*, base_url: str, timeout_s: float, call_counter: dict[str, int], sink: dict[str, Any]):
    def transport(payload: dict[str, Any]) -> dict[str, Any]:
        call_counter["model_calls"] = int(call_counter.get("model_calls", 0)) + 1
        if call_counter["model_calls"] > 1:
            raise RuntimeError("refusing second model call in one-cell smoke")
        sink["request_payload"] = payload
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            base_url.rstrip("/") + "/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310 — local Ollama
            body = json.loads(resp.read().decode("utf-8"))
        sink["response"] = body
        return body

    return transport


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CE115 one-cell formal confirmatory smoke")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "docs/experiments/manifests/ce115_calc_main_experiment_manifest.json",
    )
    parser.add_argument("--local-confirmatory", action="store_true", required=True)
    parser.add_argument("--cell-id", type=str, required=True)
    parser.add_argument("--write-artifacts", action="store_true")
    parser.add_argument("--ollama-url", type=str, default=DEFAULT_OLLAMA_URL)
    parser.add_argument("--timeout", type=float, default=600.0)
    args = parser.parse_args(argv)

    from agent_tools.finals_rebuild.ce115_calc_formal_runner import (
        FormalRunnerError,
        build_local_confirmatory_plan,
        build_ollama_request_payload,
        run_local_confirmatory,
    )
    from agent_tools.finals_rebuild.ce115_calc_prompt_freeze import prompt_sha256

    plan = build_local_confirmatory_plan(args.manifest, repo_root=ROOT)
    matches = [c for c in plan["cells"] if c["cell_id"] == args.cell_id]
    if len(matches) != 1:
        print(f"error: cell_id not unique in plan: matches={len(matches)}", file=sys.stderr)
        return 2
    cell = matches[0]
    if cell.get("model_digest") != EXPECTED_DIGEST_PREFIX:
        print(
            f"error: cell model_digest {cell.get('model_digest')!r} != "
            f"{EXPECTED_DIGEST_PREFIX!r}",
            file=sys.stderr,
        )
        return 2
    recomputed = prompt_sha256(cell["prompt_text"])
    if recomputed != cell["prompt_hash"]:
        print(
            f"error: frozen prompt hash drift: {recomputed} != {cell['prompt_hash']}",
            file=sys.stderr,
        )
        return 2
    payload = build_ollama_request_payload(cell)
    if payload.get("think") is not False:
        print("error: payload.think must be false", file=sys.stderr)
        return 2
    if payload.get("options", {}).get("temperature") != 0.0:
        print("error: temperature must be 0.0", file=sys.stderr)
        return 2
    if int(payload.get("options", {}).get("seed")) != int(cell["seed"]):
        print("error: seed mismatch", file=sys.stderr)
        return 2
    for forbidden in ("top_p", "top_k", "presence_penalty", "num_predict"):
        if forbidden in payload.get("options", {}):
            print(f"error: forbidden option present: {forbidden}", file=sys.stderr)
            return 2

    out_path = ROOT / cell["output_path"]
    if out_path.exists() and out_path.stat().st_size > 0:
        print(f"error: refusing overwrite of existing artifact: {out_path}", file=sys.stderr)
        return 2

    call_counter = {"model_calls": 0}
    sink: dict[str, Any] = {}
    transport = _make_ollama_transport(
        base_url=args.ollama_url,
        timeout_s=args.timeout,
        call_counter=call_counter,
        sink=sink,
    )
    try:
        result = run_local_confirmatory(
            args.manifest,
            transport=transport,
            repo_root=ROOT,
            write_artifacts=args.write_artifacts,
            cell_ids={args.cell_id},
            cell_limit=1,
            resume=True,
            run_id="ce115_calc_local_confirmatory_smoke_3f",
        )
    except FormalRunnerError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
        print(f"error: transport failure: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3

    rows = result.get("rows") or []
    if len(rows) != 1:
        print(f"error: expected 1 executed row, got {len(rows)}", file=sys.stderr)
        return 4
    row = rows[0]
    if row.get("prompt_hash") != cell["prompt_hash"]:
        print("error: executed row prompt_hash drift", file=sys.stderr)
        return 5
    if int(result.get("model_calls") or 0) != 1 or call_counter["model_calls"] != 1:
        print("error: model_calls != 1", file=sys.stderr)
        return 6

    raw_response = sink.get("response") or {}
    message = raw_response.get("message") if isinstance(raw_response.get("message"), dict) else {}
    thinking_val = message.get("thinking")
    thinking_status = {
        "thinking_key_present": "thinking" in message,
        "thinking_is_none": thinking_val is None,
        "thinking_is_empty_str": isinstance(thinking_val, str) and thinking_val.strip() == "",
        "thinking_has_content": isinstance(thinking_val, str) and bool(thinking_val.strip()),
        "thinking_type": type(thinking_val).__name__ if thinking_val is not None else None,
        "thinking_preview": (thinking_val[:200] if isinstance(thinking_val, str) else None),
    }
    sent = sink.get("request_payload") or {}
    summary = {
        "cell_id": row.get("cell_id"),
        "task_id": row.get("task_id"),
        "model_tag": row.get("model_tag"),
        "model_digest": row.get("model_digest"),
        "prompt_condition": row.get("prompt_condition"),
        "seed": row.get("seed"),
        "prompt_hash": row.get("prompt_hash"),
        "record_state": row.get("record_state"),
        "outcome": row.get("outcome"),
        "retry_count": row.get("retry_count"),
        "request_count": row.get("request_count"),
        "healer_enabled": row.get("healer_enabled"),
        "output_path": cell["output_path"],
        "artifact_written": bool(args.write_artifacts and out_path.is_file()),
        "model_calls": result.get("model_calls"),
        "call_counter_model_calls": call_counter["model_calls"],
        "request_payload_options": row.get("request_payload_options"),
        "sent_payload_think": sent.get("think"),
        "sent_payload_options": sent.get("options"),
        "temperature": row.get("temperature"),
        "think": cell.get("think"),
        "thinking_requested": cell.get("thinking_requested"),
        "thinking_status": thinking_status,
        "observation_status": row.get("observation_status"),
        "composite_outcomes": row.get("composite_outcomes"),
        "gates": {
            name: (row.get("evaluation_gates") or {}).get(name, {}).get("status")
            for name in (
                "g1_evaluability",
                "g2_executability",
                "g3_contract_compliance",
                "g4_semantic_correctness",
                "g5_problem_presentation",
                "g6_math_notation",
            )
        },
        "candidate_extracted_present": bool(row.get("candidate_extracted")),
        "actual_question_text_present": isinstance(row.get("actual_question_text"), str),
        "raw_output_chars": len(row.get("raw_first_attempt_output") or ""),
        "token_duration_diagnostics": row.get("token_duration_diagnostics"),
        "preflight_payload_think": payload.get("think"),
        "preflight_payload_options": payload.get("options"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"model_calls={result.get('model_calls')}")
    print(f"executed_cells={result.get('executed_cells')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
