"""Minimal Ollama /api/chat transport for CE115 Qwen 3.5 4B three-condition pilot.

Preflight uses only /api/version and /api/tags — never /api/chat.
Live calls use top-level think=false, first attempt only, no retry.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

MODEL_ID = "qwen3.5:4b"
EXPECTED_DIGEST_PREFIX = "2a654d98e6fb"
EXPECTED_OLLAMA_VERSION_PREFIX = "0.32.0"
DEFAULT_BASE_URL = "http://127.0.0.1:11434"
API_CHAT = "/api/chat"
REQUEST_TIMEOUT_SECONDS = 1800
NUM_CTX = 65536
NUM_PREDICT = 24576
TEMPERATURE = 0.0


def _http_json(url: str, *, data: bytes | None = None, timeout_s: float) -> Any:
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:  # noqa: S310 — local Ollama
        return json.loads(resp.read().decode("utf-8"))


def build_chat_payload(prompt: str, *, seed: int, model: str = MODEL_ID) -> dict[str, Any]:
    """Build /api/chat body. think must be top-level false."""
    if model != MODEL_ID:
        raise RuntimeError(f"model must be exactly {MODEL_ID}, got {model}")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,
        "options": {
            "temperature": TEMPERATURE,
            "seed": int(seed),
            "num_ctx": NUM_CTX,
            "num_predict": NUM_PREDICT,
        },
    }
    if payload.get("think") is not False:
        raise RuntimeError("think must be false at /api/chat top-level")
    if "think" in (payload.get("options") or {}):
        raise RuntimeError("think must not be nested under options")
    return payload


def probe_ollama(*, base_url: str = DEFAULT_BASE_URL, timeout_s: float = 10.0) -> dict[str, Any]:
    """Service + model availability only. Zero /api/chat calls."""
    version_data = _http_json(base_url.rstrip("/") + "/api/version", timeout_s=timeout_s)
    version = version_data.get("version") if isinstance(version_data, dict) else None
    if not isinstance(version, str) or not version.strip():
        raise RuntimeError(f"GET /api/version returned no usable version: {version_data!r}")
    version_ok = version.startswith(EXPECTED_OLLAMA_VERSION_PREFIX)

    tags = _http_json(base_url.rstrip("/") + "/api/tags", timeout_s=timeout_s)
    models = {
        m.get("name") or m.get("model"): m
        for m in (tags.get("models") or [])
        if isinstance(m, dict) and (m.get("name") or m.get("model"))
    }
    entry = models.get(MODEL_ID)
    if entry is None:
        raise RuntimeError(f"model {MODEL_ID!r} not found in /api/tags")
    digest = str(entry.get("digest") or "")
    digest_ok = EXPECTED_DIGEST_PREFIX in digest
    if not digest_ok:
        raise RuntimeError(
            f"digest mismatch for {MODEL_ID}: expected prefix {EXPECTED_DIGEST_PREFIX}, got {digest}"
        )
    return {
        "base_url": base_url.rstrip("/"),
        "runtime": "ollama",
        "runtime_version": version,
        "version_ok": version_ok,
        "model": MODEL_ID,
        "model_present": True,
        "model_digest": digest,
        "digest_ok": digest_ok,
        "api_chat": API_CHAT,
        "think_false_top_level": True,
        "chat_calls": 0,
    }


def call_ollama_once(
    prompt: str,
    *,
    seed: int,
    model: str = MODEL_ID,
    base_url: str = DEFAULT_BASE_URL,
    timeout_s: float = REQUEST_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Exactly one first-attempt Ollama /api/chat call. No retry."""
    payload = build_chat_payload(prompt, seed=seed, model=model)
    started = time.monotonic()
    try:
        body = _http_json(
            base_url.rstrip("/") + API_CHAT,
            data=json.dumps(payload).encode("utf-8"),
            timeout_s=timeout_s,
        )
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ConnectionError(f"Ollama unreachable: {exc}") from exc
    wall = time.monotonic() - started

    raw = (body.get("message") or {}).get("content")
    if not isinstance(raw, str):
        raise RuntimeError("model response missing message.content string")

    prompt_eval = body.get("prompt_eval_count")
    eval_count = body.get("eval_count")
    total_tokens = None
    if isinstance(prompt_eval, int) and isinstance(eval_count, int):
        total_tokens = prompt_eval + eval_count
    elif isinstance(eval_count, int):
        total_tokens = eval_count

    meta = {
        "model": model,
        "requested_model": model,
        "runtime": "ollama",
        "api_endpoint": API_CHAT,
        "think": False,
        "seed": int(seed),
        "prompt_eval_count": prompt_eval,
        "eval_count": eval_count,
        "total_token_count": total_tokens,
        "total_duration": body.get("total_duration"),
        "load_duration": body.get("load_duration"),
        "prompt_eval_duration": body.get("prompt_eval_duration"),
        "eval_duration": body.get("eval_duration"),
        "done": body.get("done"),
        "done_reason": body.get("done_reason"),
        "latency_ms": int(wall * 1000),
        "first_attempt_only": True,
        "retry": 0,
        "request_payload": {
            "model": payload["model"],
            "stream": payload["stream"],
            "think": payload["think"],
            "options": payload["options"],
            # prompt content omitted from metadata; stored separately as prompt.txt
        },
    }
    return {"raw_text": raw, "metadata": meta}
