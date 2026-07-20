"""Unit tests for Math16 Qwen Ollama adapter (mocked; no live model calls)."""
from __future__ import annotations

import pytest

from scripts import math16_qwen_ollama_adapter as adapter


def _ok_response(text: str = "print('hello')") -> dict:
    return {
        "raw_text": text,
        "metadata": {
            "model": adapter.MODEL_ID,
            "requested_model": adapter.MODEL_ID,
            "runtime": "ollama",
            "prompt_eval_count": 3,
            "eval_count": 5,
            "total_token_count": 8,
            "latency_ms": 12,
            "done": True,
            "done_reason": "stop",
        },
    }


def test_frozen_inference_config_aligns_with_gemini_max_tokens() -> None:
    cfg = adapter.frozen_inference_config()
    # Non-thinking instruct sampling (not ollama show thinking-mode defaults).
    assert cfg["temperature"] == 0.7
    assert cfg["top_p"] == 0.8
    assert cfg["top_k"] == 20
    assert cfg["think"] is False
    assert cfg["runtime_mode"] == "non_thinking"
    assert "presence_penalty" not in cfg
    assert cfg["unset_options_use_ollama_defaults"]["presence_penalty"] == "ollama_default"
    assert cfg["num_predict"] == 24576
    assert cfg["num_ctx"] == 65536
    assert cfg["seed_default"] == 2026071301
    assert cfg["request_timeout_seconds"] == 1800
    assert cfg["model"] == "qwen3.5:4b"
    assert cfg["base_url"] == "http://localhost:11434"
    assert cfg["retry"]["max_attempts"] == 3
    assert cfg["retry"]["backoff_seconds"] == [5, 20, 60]
    assert cfg["retry"]["exhausted_validity"] == "INVALID_INFRASTRUCTURE"
    assert cfg["retry"]["exhausted_layer"] == "L0"
    assert "24576" in cfg["num_predict_alignment"]
    assert "non-thinking" in cfg["vendor_sampling_source"]
    assert "0.7" in cfg["vendor_sampling_source"]


def test_math16_chat_payload_uses_non_thinking_sampling() -> None:
    payload = adapter.build_math16_chat_payload("print hello", seed=2026071301)
    assert payload["think"] is False
    assert "think" not in payload["options"]
    assert payload["options"]["temperature"] == 0.7
    assert payload["options"]["top_p"] == 0.8
    assert payload["options"]["top_k"] == 20
    assert "presence_penalty" not in payload["options"]
    assert payload["options"]["num_predict"] == 24576
    assert payload["options"]["num_ctx"] == 65536
    assert payload["options"]["seed"] == 2026071301


def test_call_qwen_once_returns_raw_text_and_metadata() -> None:
    def fake(prompt, **_kwargs):
        assert prompt == "print hello"
        return _ok_response("ok-body")

    out = adapter.call_qwen_once("print hello", transport=fake)
    assert out["raw_text"] == "ok-body"
    assert out["metadata"]["inference_config"]["temperature"] == 0.7
    assert out["metadata"]["inference_config"]["top_p"] == 0.8
    assert out["metadata"]["inference_config"]["top_k"] == 20
    assert out["metadata"]["inference_config"]["num_predict"] == 24576
    assert out["metadata"]["inference_config"]["presence_penalty"] == "ollama_default_unset"
    assert out["metadata"]["eval_count"] == 5


def test_empty_response_is_retryable_and_exhausts_to_l0() -> None:
    sleeps: list[float] = []

    def empty_transport(_prompt, **_kwargs):
        return {"raw_text": "   ", "metadata": {"model": adapter.MODEL_ID}}

    with pytest.raises(adapter.InvalidInfrastructureError) as excinfo:
        adapter.call_qwen_with_retries(
            "print hello",
            transport=empty_transport,
            sleep=sleeps.append,
        )
    err = excinfo.value
    assert err.layer == "L0"
    assert err.validity == "INVALID_INFRASTRUCTURE"
    assert len(err.api_attempts) == 3
    assert all(a["status"] == "error" for a in err.api_attempts)
    assert all(a["retryable"] for a in err.api_attempts)
    assert sleeps == [5, 20]


def test_connection_failure_retries_then_succeeds() -> None:
    calls = {"n": 0}
    sleeps: list[float] = []

    def flaky(_prompt, **_kwargs):
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("Ollama unreachable: connection refused")
        return _ok_response("recovered")

    out = adapter.call_qwen_with_retries(
        "print hello",
        transport=flaky,
        sleep=sleeps.append,
    )
    assert out["raw_text"] == "recovered"
    assert out["api_attempts"][0]["status"] == "error"
    assert out["api_attempts"][1]["status"] == "error"
    assert out["api_attempts"][2]["status"] == "success"
    assert out["metadata"]["api_attempt_count"] == 3
    assert out["metadata"]["first_valid_attempt"] == 3
    assert sleeps == [5, 20]


def test_timeout_exhaustion_marks_invalid_infrastructure() -> None:
    sleeps: list[float] = []

    def always_timeout(_prompt, **_kwargs):
        raise TimeoutError("read timed out")

    with pytest.raises(adapter.InvalidInfrastructureError) as excinfo:
        adapter.call_qwen_with_retries(
            "print hello",
            transport=always_timeout,
            sleep=sleeps.append,
        )
    assert len(excinfo.value.api_attempts) == 3
    assert sleeps == [5, 20]
    assert "INVALID_INFRASTRUCTURE" in str(excinfo.value)


def test_non_retryable_error_fails_immediately() -> None:
    sleeps: list[float] = []

    def bad_request(_prompt, **_kwargs):
        raise RuntimeError("Ollama HTTP 400: bad request")

    with pytest.raises(RuntimeError, match="non-retryable") as excinfo:
        adapter.call_qwen_with_retries(
            "print hello",
            transport=bad_request,
            sleep=sleeps.append,
        )
    assert sleeps == []
    assert "HTTP 400" in str(excinfo.value)


def test_build_cell_generation_record_schema() -> None:
    response = adapter.call_qwen_with_retries(
        "print hello",
        transport=lambda _p, **_k: _ok_response("cell-body"),
        sleep=lambda _s: None,
    )
    record = adapter.build_cell_generation_record(response)
    assert record["raw_response"] == "cell-body"
    assert record["model"] == "qwen3.5:4b"
    assert record["token_metadata"]["eval_count"] == 5
    assert record["api_attempt_count"] == 1
    assert record["provenance"]["api_retry_same_cell"] is True
    assert "wall_clock_seconds" in record["duration_metadata"]


def test_is_retryable_error_classification() -> None:
    assert adapter.is_retryable_error(TimeoutError("timed out"))
    assert adapter.is_retryable_error(ConnectionError("unreachable"))
    assert adapter.is_retryable_error(adapter.EmptyResponseError("empty"))
    assert not adapter.is_retryable_error(RuntimeError("Ollama HTTP 400: nope"))
