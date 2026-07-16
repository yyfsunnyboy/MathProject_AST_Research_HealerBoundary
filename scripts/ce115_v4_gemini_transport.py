"""Minimal Gemini transport for CE115 v4 positive control.

Reads GEMINI_API_KEY only from process environment.
Never logs, hashes, or persists the key value.
Uses installed google.generativeai / google-genai directly — no Flask import path.
"""
from __future__ import annotations

import importlib.metadata
import os
from typing import Any


MODEL_ID = "gemini-3.5-flash"
REQUEST_TIMEOUT_SECONDS = 600
MAX_OUTPUT_TOKENS = 24576
TEMPERATURE = 0.0


def api_key_status() -> dict[str, Any]:
    present = bool(os.environ.get("GEMINI_API_KEY"))
    return {
        "api_key_source": "environment",
        "api_key_present": present,
    }


def runtime_version() -> str | None:
    for package in ("google-genai", "google-generativeai"):
        try:
            return f"{package} {importlib.metadata.version(package)}"
        except importlib.metadata.PackageNotFoundError:
            continue
    return None


def assert_no_key_leak(payload: Any) -> None:
    text = str(payload)
    key = os.environ.get("GEMINI_API_KEY") or ""
    if "x-goog-api-key" in text.lower():
        raise AssertionError("x-goog-api-key must not appear in artifacts")
    if "authorization:" in text.lower() and "bearer" in text.lower():
        raise AssertionError("Authorization bearer must not appear in artifacts")
    if key and key in text:
        raise AssertionError("API key value leaked into artifact payload")


def build_redacted_request(prompt: str, *, model: str = MODEL_ID) -> dict[str, Any]:
    """Public request metadata only — no API key fields."""
    return {
        "provider": "gemini",
        "model": model,
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generation_config": {
            "temperature": TEMPERATURE,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
        },
        "tools": None,
        "code_execution": False,
        "function_calling": False,
        "api_key_source": "environment",
        "api_key_present": bool(os.environ.get("GEMINI_API_KEY")),
    }


def _call_with_new_sdk(prompt: str, model: str, api_key: str) -> tuple[str, dict[str, Any]]:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        temperature=TEMPERATURE,
        max_output_tokens=MAX_OUTPUT_TOKENS,
        # Explicitly no tools / code execution
    )
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    raw = getattr(response, "text", None)
    if not isinstance(raw, str):
        raise RuntimeError("gemini response missing text string")
    usage = getattr(response, "usage_metadata", None)
    meta = {
        "sdk": "google-genai",
        "prompt_token_count": getattr(usage, "prompt_token_count", None) if usage else None,
        "candidates_token_count": getattr(usage, "candidates_token_count", None) if usage else None,
        "total_token_count": getattr(usage, "total_token_count", None) if usage else None,
    }
    return raw, meta


def _call_with_old_sdk(prompt: str, model: str, api_key: str) -> tuple[str, dict[str, Any]]:
    import warnings

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")
        import google.generativeai as genai

    genai.configure(api_key=api_key, transport="rest")
    model_client = genai.GenerativeModel(
        model_name=model,
        # No tools / function declarations — text-only generation
    )
    generation_config = {
        "temperature": TEMPERATURE,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
    }
    response = model_client.generate_content(
        prompt,
        generation_config=generation_config,
        request_options={"timeout": REQUEST_TIMEOUT_SECONDS},
    )
    raw = getattr(response, "text", None)
    if not isinstance(raw, str):
        raise RuntimeError("gemini response missing text string")
    usage = getattr(response, "usage_metadata", None)
    meta = {
        "sdk": "google-generativeai",
        "prompt_token_count": getattr(usage, "prompt_token_count", None) if usage else None,
        "candidates_token_count": getattr(usage, "candidates_token_count", None) if usage else None,
        "total_token_count": getattr(usage, "total_token_count", None) if usage else None,
    }
    return raw, meta


def call_gemini_once(prompt: str, *, model: str = MODEL_ID) -> dict[str, Any]:
    """Exactly one first-attempt Gemini text call. No retry. No tools."""
    status = api_key_status()
    if not status["api_key_present"]:
        raise RuntimeError("API_KEY_REQUIRED")
    if model != MODEL_ID:
        raise RuntimeError(f"model must be exactly {MODEL_ID}, got {model}")

    api_key = os.environ["GEMINI_API_KEY"]
    try:
        import importlib.util

        if importlib.util.find_spec("google.genai") is not None:
            raw, sdk_meta = _call_with_new_sdk(prompt, model, api_key)
            sdk_new = True
        else:
            raw, sdk_meta = _call_with_old_sdk(prompt, model, api_key)
            sdk_new = False
    finally:
        # Drop local reference promptly; never persist.
        api_key = ""

    meta = {
        "model": model,
        "requested_model": model,
        "runtime": "gemini",
        "runtime_version": runtime_version(),
        "sdk_new": sdk_new,
        "prompt_token_count": sdk_meta.get("prompt_token_count"),
        "candidates_token_count": sdk_meta.get("candidates_token_count"),
        "total_token_count": sdk_meta.get("total_token_count"),
        "latency_ms": None,
        "tools_enabled": False,
        "code_execution_enabled": False,
        "function_calling_enabled": False,
        "first_attempt_only": True,
        "retry": 0,
        "sdk": sdk_meta.get("sdk"),
        **status,
    }
    out = {"raw_text": raw, "metadata": meta}
    assert_no_key_leak(out)
    return out
