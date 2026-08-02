"""Shared Ab2d+full cell artifact assembly (QFIX-001 null-safe encoding).

Engineering-only helpers for writing evaluation/artifact JSON after
``classify_math16_response``. Does not alter evaluator semantics, outcomes,
classification, prompts, APIs, scaffolds, or model settings.
"""
from __future__ import annotations

import ast
import json
import os
import tempfile
from pathlib import Path
from typing import Any


QFIX_001_ID = "QFIX-001"
QFIX_001_SUMMARY = (
    "Null-safe evaluation artifact encoding when outcome=='passed' and "
    "classify details omit returned_value (avoid sorted(None))."
)


def encode_returned_value_for_artifact(outcome: str, details: dict[str, Any]) -> Any:
    """Encode returned_value for evaluation_result.json.

    QFIX-001: when outcome is ``passed``, classify_math16_response may omit
    ``returned_value`` from assembled success fields. Never call ``sorted`` on
    a missing/None returned_value.
    """
    returned = details.get("returned_value")
    if outcome == "passed":
        return {
            "_note": (
                "full returned_value omitted on pass; "
                "evaluator already validated three-key schema"
            ),
            "detail_keys": sorted(details.keys()),
        }
    return returned


def schema_flags(
    outcome: str,
    details: dict[str, Any],
    *,
    frozen_params: dict[str, Any],
) -> tuple[bool, bool]:
    """Derive three_key_output and oracle_payload equality flags for artifacts."""
    returned = details.get("returned_value")
    if outcome == "passed":
        # Authoritative classify path already validated three-key + payload.
        return True, True
    three_key = isinstance(returned, dict) and set(returned) == {
        "question_text",
        "correct_answer",
        "oracle_payload",
    }
    oracle_eq = isinstance(returned, dict) and returned.get("oracle_payload") == frozen_params
    return three_key, oracle_eq


def domain_api_availability(source: str | None) -> dict[str, Any]:
    if not source:
        return {"checked": False, "import_ok": None, "detail": "no source"}
    needed = [name for name in ("IntegerOps", "FractionOps", "RadicalOps", "PolynomialOps") if name in source]
    try:
        from core.prompts import domain_function_library as dfl

        present = {
            name: hasattr(dfl, name)
            for name in ("IntegerOps", "FractionOps", "RadicalOps", "PolynomialOps")
        }
        return {
            "checked": True,
            "ops_referenced_in_source": needed,
            "ops_importable": present,
            "import_ok": all(present.values()),
        }
    except Exception as exc:  # noqa: BLE001 — record import failure only
        return {"checked": True, "import_ok": False, "error": str(exc)}


def build_evaluation_result(
    *,
    outcome: str,
    source: str | None,
    details: dict[str, Any],
    frozen_params: dict[str, Any],
) -> dict[str, Any]:
    """Build evaluation_result payload without mutating outcome/details semantics."""
    if outcome == "transport_failure":
        return {
            "outcome": "transport_failure",
            "error": details.get("error"),
            "api_attempts": details.get("api_attempts"),
        }

    parse_ok: bool | None = None
    detail_out = dict(details)
    if source:
        try:
            ast.parse(source)
            parse_ok = True
        except SyntaxError as exc:
            parse_ok = False
            detail_out["python_parse_error"] = str(exc)

    three_key, oracle_eq = schema_flags(outcome, detail_out, frozen_params=frozen_params)
    runtime_error = None
    nested = detail_out.get("detail")
    if isinstance(nested, dict):
        runtime_error = nested.get("runtime_error")
    else:
        runtime_error = detail_out.get("runtime_error")

    return {
        "outcome": outcome,
        "python_parse_ok": parse_ok,
        "domain_api_availability": domain_api_availability(source),
        "three_key_output": three_key,
        "oracle_payload_equals_frozen_params": oracle_eq,
        "authoritative_evaluator_outcome": outcome,
        "detail_keys": sorted(detail_out.keys()),
        "returned_value": encode_returned_value_for_artifact(outcome, detail_out),
        "structural_ok": detail_out.get("structural_ok"),
        "latex_ok": detail_out.get("latex_ok"),
        "runtime_error": runtime_error,
    }


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_write_text(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def write_evaluation_artifacts(
    cell_dir: Path,
    *,
    evaluation: dict[str, Any],
    outcome: str,
) -> None:
    """Write evaluation_result.json and execution_result.json."""
    atomic_write_json(cell_dir / "evaluation_result.json", evaluation)
    if outcome != "transport_failure":
        atomic_write_json(
            cell_dir / "execution_result.json",
            {
                "outcome": outcome,
                "returned_value": evaluation.get("returned_value"),
                "runtime_error": evaluation.get("runtime_error"),
            },
        )


def write_artifact_manifest(cell_dir: Path, artifact: dict[str, Any]) -> dict[str, Any]:
    """Write artifact.json with required-file check; returns updated artifact."""
    required = [
        "prompt.txt",
        "raw_response.txt",
        "request_metadata.json",
        "evaluation_result.json",
        "logs.json",
    ]
    missing = [name for name in required if not (cell_dir / name).exists()]
    artifact = dict(artifact)
    artifact["missing_required_before_manifest"] = missing
    artifact["qfix_001_applied"] = True
    atomic_write_json(cell_dir / "artifact.json", artifact)
    artifact["artifact_files"] = sorted(p.name for p in cell_dir.iterdir() if p.is_file())
    atomic_write_json(cell_dir / "artifact.json", artifact)
    return artifact
