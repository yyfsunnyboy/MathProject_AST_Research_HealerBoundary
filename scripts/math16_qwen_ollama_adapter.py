"""Math16 Qwen local inference adapter via Ollama.

Call convention matches Gemini Math16 runners:

    call_qwen_with_retries(prompt) -> {
        "raw_text": str,
        "metadata": dict,       # generation + token stats + attempt summary
        "api_attempts": list,   # per-attempt records for the same cell
    }

Runtime mode: non-thinking (`think: false` at /api/chat top-level).
Sampling frozen for both 4B/9B from Qwen official instruct/non-thinking
recommendations: temperature=0.7, top_p=0.8, top_k=20. presence_penalty is
omitted (Ollama default). `ollama show` Parameters still list thinking-mode
defaults (1.0 / 0.95 / presence_penalty=1.5) and are intentionally not used.

Does not build Math16 prompts, evaluate answers, or write formal run artifacts.
"""
from __future__ import annotations

import json
import time
import urllib.error
from typing import Any, Callable

from scripts.ce115_qwen_ollama_transport import (
    ALLOWED_MODELS,
    API_CHAT,
    MODEL_ID,
    NUM_CTX,
    NUM_PREDICT,
    _http_json,
    probe_ollama,
)

# Gemini Math16 (ce115_v4_gemini_transport) freezes max_output_tokens=24576.
GEMINI_ALIGNED_NUM_PREDICT = NUM_PREDICT  # 24576
assert GEMINI_ALIGNED_NUM_PREDICT == 24576

DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_SEED = 2026071301
REQUEST_TIMEOUT_SECONDS = 1800
MAX_ATTEMPTS = 3
BACKOFF_SECONDS = (5, 20, 60)

# Non-thinking instruct sampling (same freeze for qwen3.5:4b and :9b).
TEMPERATURE = 0.7
TOP_P = 0.8
TOP_K = 20
VENDOR_SAMPLING_SOURCE = (
    "Qwen official instruct/non-thinking recommendations "
    "(temperature=0.7, top_p=0.8, top_k=20); "
    "presence_penalty omitted (Ollama default); "
    "ollama show Parameters remain thinking-mode defaults "
    "(temperature=1, top_p=0.95, presence_penalty=1.5) and are not used; "
    "identical freeze for qwen3.5:4b and qwen3.5:9b"
)

FROZEN_INFERENCE_CONFIG: dict[str, Any] = {
    "provider": "ollama",
    "base_url": DEFAULT_BASE_URL,
    "model": MODEL_ID,
    "allowed_models": list(ALLOWED_MODELS),
    "api": API_CHAT,
    "stream": False,
    "think": False,
    "runtime_mode": "non_thinking",
    "temperature": TEMPERATURE,
    "top_p": TOP_P,
    "top_k": TOP_K,
    "vendor_sampling_source": VENDOR_SAMPLING_SOURCE,
    "num_predict": GEMINI_ALIGNED_NUM_PREDICT,
    "num_predict_alignment": (
        "Aligned to Gemini Math16 MAX_OUTPUT_TOKENS=24576 "
        "(scripts/ce115_v4_gemini_transport.py); not reduced to 4096."
    ),
    "num_ctx": NUM_CTX,
    "seed_default": DEFAULT_SEED,
    "request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
    "retry": {
        "max_attempts": MAX_ATTEMPTS,
        "backoff_seconds": list(BACKOFF_SECONDS),
        "retryable": ["timeout", "connection_failure", "empty_response"],
        "exhausted_layer": "L0",
        "exhausted_validity": "INVALID_INFRASTRUCTURE",
        "same_cell": True,
    },
    "unset_options_use_ollama_defaults": {
        "presence_penalty": "ollama_default",
        "min_p": "ollama_default",
        "typical_p": "ollama_default",
        "repeat_last_n": "ollama_default",
        "repeat_penalty": "ollama_default",
        "frequency_penalty": "ollama_default",
        "mirostat": "ollama_default",
        "mirostat_tau": "ollama_default",
        "mirostat_eta": "ollama_default",
        "tfs_z": "ollama_default",
    },
}


class InvalidInfrastructureError(RuntimeError):
    """Raised when retryable infrastructure failures exhaust max attempts (L0)."""

    def __init__(
        self,
        message: str,
        *,
        api_attempts: list[dict[str, Any]],
        layer: str = "L0",
        validity: str = "INVALID_INFRASTRUCTURE",
    ) -> None:
        super().__init__(message)
        self.api_attempts = list(api_attempts)
        self.layer = layer
        self.validity = validity

    def as_metadata(self) -> dict[str, Any]:
        return {
            "layer": self.layer,
            "validity": self.validity,
            "api_attempt_count": len(self.api_attempts),
            "api_attempts": self.api_attempts,
            "first_valid_attempt": None,
        }


def frozen_inference_config() -> dict[str, Any]:
    """Return a deep-ish copy of frozen adapter settings for run manifests."""
    import copy

    return copy.deepcopy(FROZEN_INFERENCE_CONFIG)


def _error_text(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {exc}".lower()


def is_retryable_error(exc: BaseException) -> bool:
    """Timeout, connection failure, and empty-response errors are retryable."""
    if isinstance(exc, EmptyResponseError):
        return True
    if isinstance(exc, (TimeoutError, ConnectionError, urllib.error.URLError)):
        return True
    text = _error_text(exc)
    markers = (
        "timeout",
        "timed out",
        "connection",
        "unreachable",
        "temporarily unavailable",
        "empty response",
        "empty_response",
        "connection reset",
        "connection aborted",
        "winerror 10061",
        "10061",
    )
    return any(marker in text for marker in markers)


class EmptyResponseError(RuntimeError):
    """Model returned an empty / whitespace-only message.content."""


TransportFn = Callable[..., dict[str, Any]]


def build_math16_chat_payload(
    prompt: str,
    *,
    seed: int = DEFAULT_SEED,
    model: str = MODEL_ID,
) -> dict[str, Any]:
    """Build /api/chat body with vendor-recommended sampling (think=false)."""
    if model not in ALLOWED_MODELS:
        raise RuntimeError(f"model must be one of {ALLOWED_MODELS}, got {model}")
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        # Native Ollama /api/chat top-level think flag (not under options).
        "think": False,
        "options": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "top_k": TOP_K,
            "seed": int(seed),
            "num_ctx": NUM_CTX,
            "num_predict": GEMINI_ALIGNED_NUM_PREDICT,
        },
    }
    if payload.get("think") is not False:
        raise RuntimeError("think must be false at /api/chat top-level")
    if "think" in (payload.get("options") or {}):
        raise RuntimeError("think must not be nested under options")
    if "presence_penalty" in (payload.get("options") or {}):
        raise RuntimeError("presence_penalty must be omitted (Ollama default)")
    return payload


def call_ollama_once_math16(
    prompt: str,
    *,
    seed: int = DEFAULT_SEED,
    model: str = MODEL_ID,
    base_url: str = DEFAULT_BASE_URL,
    timeout_s: float = REQUEST_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Exactly one Ollama /api/chat call with Math16 vendor sampling. No retry."""
    payload = build_math16_chat_payload(prompt, seed=seed, model=model)
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
        },
    }
    return {"raw_text": raw, "metadata": meta}


def call_qwen_once(
    prompt: str,
    *,
    seed: int = DEFAULT_SEED,
    model: str = MODEL_ID,
    base_url: str = DEFAULT_BASE_URL,
    timeout_s: float = REQUEST_TIMEOUT_SECONDS,
    transport: TransportFn | None = None,
) -> dict[str, Any]:
    """Exactly one Ollama /api/chat call. No retry. Matches Gemini once-call shape."""
    caller = transport or call_ollama_once_math16
    response = caller(
        prompt,
        seed=int(seed),
        model=model,
        base_url=base_url,
        timeout_s=timeout_s,
    )
    raw = response.get("raw_text")
    if not isinstance(raw, str) or not raw.strip():
        raise EmptyResponseError("empty response from Ollama message.content")
    meta = dict(response.get("metadata") or {})
    meta.setdefault("model", model)
    meta.setdefault("requested_model", model)
    meta.setdefault("runtime", "ollama")
    meta.setdefault("base_url", base_url.rstrip("/"))
    meta["inference_config"] = {
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "top_k": TOP_K,
        "num_predict": GEMINI_ALIGNED_NUM_PREDICT,
        "num_ctx": NUM_CTX,
        "think": False,
        "runtime_mode": "non_thinking",
        "stream": False,
        "seed": int(seed),
        "request_timeout_seconds": timeout_s,
        "vendor_sampling_source": VENDOR_SAMPLING_SOURCE,
        "presence_penalty": "ollama_default_unset",
    }
    meta["retry"] = 0
    meta["first_attempt_only"] = True
    return {"raw_text": raw, "metadata": meta}


def call_qwen_with_retries(
    prompt: str,
    *,
    seed: int = DEFAULT_SEED,
    model: str = MODEL_ID,
    base_url: str = DEFAULT_BASE_URL,
    timeout_s: float = REQUEST_TIMEOUT_SECONDS,
    transport: TransportFn | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    """Retrying adapter entrypoint for Math16 cells (same-cell attempts).

    Retries on timeout, connection failure, and empty response.
    Exhaustion raises InvalidInfrastructureError (L0 / INVALID_INFRASTRUCTURE).
    """
    attempts: list[dict[str, Any]] = []
    for attempt_index in range(1, MAX_ATTEMPTS + 1):
        started = time.monotonic()
        try:
            response = call_qwen_once(
                prompt,
                seed=seed,
                model=model,
                base_url=base_url,
                timeout_s=timeout_s,
                transport=transport,
            )
            wall = time.monotonic() - started
            attempts.append(
                {
                    "attempt": attempt_index,
                    "status": "success",
                    "wall_clock_seconds": wall,
                    "exception_type": None,
                    "exception_message": None,
                    "retryable": False,
                }
            )
            meta = dict(response.get("metadata") or {})
            meta["api_attempts"] = attempts
            meta["api_attempt_count"] = len(attempts)
            meta["first_valid_attempt"] = attempt_index
            meta["retry"] = attempt_index - 1
            meta["first_attempt_only"] = attempt_index == 1
            meta["adapter"] = "math16_qwen_ollama_adapter"
            meta["model_version"] = meta.get("model") or model
            return {
                "raw_text": response["raw_text"],
                "metadata": meta,
                "api_attempts": attempts,
            }
        except BaseException as exc:
            wall = time.monotonic() - started
            retryable = is_retryable_error(exc)
            attempts.append(
                {
                    "attempt": attempt_index,
                    "status": "error",
                    "wall_clock_seconds": wall,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "retryable": retryable,
                }
            )
            if not retryable:
                raise RuntimeError(
                    f"API_FAILURE non-retryable after {attempt_index} attempt(s): "
                    f"{type(exc).__name__}: {exc}"
                ) from exc
            if attempt_index == MAX_ATTEMPTS:
                raise InvalidInfrastructureError(
                    f"L0 INVALID_INFRASTRUCTURE after {attempt_index} attempts: "
                    f"{type(exc).__name__}: {exc}",
                    api_attempts=attempts,
                ) from exc
            sleep(BACKOFF_SECONDS[attempt_index - 1])
    raise InvalidInfrastructureError(
        "L0 INVALID_INFRASTRUCTURE unreachable",
        api_attempts=attempts,
    )


def build_cell_generation_record(response: dict[str, Any]) -> dict[str, Any]:
    """Map adapter response into fields aligned with Math16 cell artifact schema."""
    meta = dict(response.get("metadata") or {})
    attempts = list(response.get("api_attempts") or meta.get("api_attempts") or [])
    return {
        "raw_response": response.get("raw_text"),
        "model": meta.get("model") or MODEL_ID,
        "model_version": meta.get("model_version") or meta.get("model") or MODEL_ID,
        "runtime": meta.get("runtime") or "ollama",
        "runtime_version": meta.get("runtime_version"),
        "inference_config": meta.get("inference_config") or frozen_inference_config(),
        "token_metadata": {
            "prompt_eval_count": meta.get("prompt_eval_count"),
            "eval_count": meta.get("eval_count"),
            "total_token_count": meta.get("total_token_count"),
            "total_duration": meta.get("total_duration"),
            "load_duration": meta.get("load_duration"),
            "prompt_eval_duration": meta.get("prompt_eval_duration"),
            "eval_duration": meta.get("eval_duration"),
            "done": meta.get("done"),
            "done_reason": meta.get("done_reason"),
            "latency_ms": meta.get("latency_ms"),
        },
        "duration_metadata": {
            "wall_clock_seconds": sum(
                float(a.get("wall_clock_seconds") or 0.0) for a in attempts
            ),
            "provider_duration": meta.get("latency_ms"),
            "per_attempt_wall_clock_seconds": [
                a.get("wall_clock_seconds") for a in attempts
            ],
        },
        "api_attempts": attempts,
        "api_attempt_count": len(attempts),
        "provenance": {
            "adapter": "math16_qwen_ollama_adapter",
            "api_retry_same_cell": True,
            "healer": 0,
            "model_calls": sum(1 for a in attempts if a.get("status") == "success"),
            "api_attempt_count": len(attempts),
            "first_valid_attempt": meta.get("first_valid_attempt"),
        },
    }


# Compatibility alias used by older smoke imports / tests.
build_chat_payload = build_math16_chat_payload

__all__ = [
    "BACKOFF_SECONDS",
    "DEFAULT_BASE_URL",
    "DEFAULT_SEED",
    "FROZEN_INFERENCE_CONFIG",
    "GEMINI_ALIGNED_NUM_PREDICT",
    "InvalidInfrastructureError",
    "MAX_ATTEMPTS",
    "MODEL_ID",
    "REQUEST_TIMEOUT_SECONDS",
    "TEMPERATURE",
    "TOP_K",
    "TOP_P",
    "VENDOR_SAMPLING_SOURCE",
    "build_cell_generation_record",
    "build_chat_payload",
    "build_math16_chat_payload",
    "call_ollama_once_math16",
    "call_qwen_once",
    "call_qwen_with_retries",
    "frozen_inference_config",
    "is_retryable_error",
    "probe_ollama",
]
