"""Deterministic, dependency-free observability for generator success gates."""
from __future__ import annotations

import json
import re
from typing import Any

PASS = "PASS"
FAIL = "FAIL"
NOT_ASSESSED = "NOT_ASSESSED"
NOT_OBSERVED = "NOT_OBSERVED"

LEDGER_STAGES = frozenset({"observed", "pipeline_corrected", "post_healer"})
REQUIRED_RETURN_KEYS = frozenset({"question_text", "correct_answer", "oracle_payload"})
G1_FAIL_OUTCOMES = frozenset({
    "empty_response",
    "catastrophic_truncation",
    "extraction_failure",
    "parse_minor",
    "missing_entry_point",
})
OBSERVED_SUCCESS_FIELD_KEYS = (
    "ledger_stage",
    "actual_question_text",
    "evaluation_gates",
    "composite_outcomes",
)
THREE_LEDGER_FIELD_KEYS = (
    "record_id",
    "source_record_id",
    "correction_actions",
    "healer",
    "observation_status",
)
GATE_STATUSES = frozenset({PASS, FAIL, NOT_ASSESSED, NOT_OBSERVED})
EXPERIMENT_NOT_RUN = "experiment_not_run"
GENERATOR_FAILURE = "generator_failure"


def _gate(status: str, reason: str, **evidence: Any) -> dict[str, Any]:
    return {"status": status, "reason": reason, **evidence}


def extract_actual_question_text(returned_value: Any) -> str | None:
    """Persist only the entry-point return object's question_text (or null)."""
    if not isinstance(returned_value, dict) or "question_text" not in returned_value:
        return None
    text = returned_value["question_text"]
    return text if isinstance(text, str) else None


def evaluate_problem_presentation(question_text: Any, frozen_parameters: Any = None,
                                  correct_answer: Any = None) -> dict[str, Any]:
    if not isinstance(question_text, str) or not question_text.strip():
        return _gate(NOT_OBSERVED, "actual_question_text_unavailable", question_present=False)
    text = question_text.strip()
    placeholder = bool(re.search(r"\{\{.*?\}\}|<PLACEHOLDER>|\bTODO\b|\bFIXME\b|\[INSERT[^\]]*\]", text, re.I))
    prompt_leak = any(token.lower() in text.lower() for token in
                      ("you are chatgpt", "return only python", "task contract", "frozen parameters"))
    code_leak = bool(re.search(r"\bdef\s+generate\s*\(|\bimport\s+[A-Za-z_] |\breturn\s*\{", text))
    answer_leak = isinstance(correct_answer, (str, int, float)) and bool(str(correct_answer).strip()) and str(correct_answer) in text
    truncation = text.endswith(("...", "…", "\\"))
    reasons = [name for name, present in (("placeholder_leak", placeholder), ("prompt_leak", prompt_leak), ("code_leak", code_leak), ("answer_leak", answer_leak), ("truncation_signal", truncation)) if present]
    return _gate(FAIL if reasons else PASS, ",".join(reasons) if reasons else "presentation_checks_passed",
                 question_present=True, placeholder_leak=placeholder, prompt_leak=prompt_leak,
                 code_leak=code_leak, answer_leak=answer_leak, truncation_signal=truncation,
                 frozen_parameters_available=frozen_parameters is not None)


def evaluate_math_notation(question_text: Any) -> dict[str, Any]:
    if not isinstance(question_text, str) or not question_text.strip():
        return _gate(NOT_OBSERVED, "actual_question_text_unavailable", uses_latex=False)
    text = question_text
    uses_latex = any(token in text for token in ("$", r"\(", r"\)", r"\[", r"\]", "\\"))
    dollar_count = len(re.findall(r"(?<!\\)\$", text))
    delimiter_balance = dollar_count % 2 == 0 and text.count(r"\(") == text.count(r"\)") and text.count(r"\[") == text.count(r"\]")
    regions = re.findall(r"\$\$.*?\$\$|(?<!\$)\$[^$]*\$|\\\(.*?\\\)|\\\[.*?\\\]", text, re.S)
    brace_balance = all(region.count("{") == region.count("}") for region in regions)
    malformed = text.rstrip().endswith("\\") or bool(re.search(r"\\[A-Za-z]+\{[^}]*$", text))
    reasons = [name for name, present in (("latex_delimiter_failure", not delimiter_balance), ("latex_brace_failure", not brace_balance), ("latex_malformed_command", malformed)) if present]
    return _gate(FAIL if reasons else PASS, ",".join(reasons) if reasons else "notation_checks_passed",
                 uses_latex=uses_latex, delimiter_balance=delimiter_balance, brace_balance=brace_balance,
                 malformed_command=malformed, unclosed_math_region=not delimiter_balance)


def composite_outcomes(gates: dict[str, dict[str, Any]]) -> dict[str, str]:
    def combine(names: tuple[str, ...]) -> str:
        values = [gates[name]["status"] for name in names]
        if FAIL in values:
            return FAIL
        if NOT_OBSERVED in values or NOT_ASSESSED in values:
            return NOT_OBSERVED
        return PASS
    return {
        "technical_pass": combine(("g1_evaluability", "g2_executability", "g3_contract_compliance", "g4_semantic_correctness")),
        "presentation_pass": combine(("g5_problem_presentation", "g6_math_notation")),
        "full_pass": combine(("g1_evaluability", "g2_executability", "g3_contract_compliance", "g4_semantic_correctness", "g5_problem_presentation", "g6_math_notation")),
    }


def _not_assessed(reason: str) -> dict[str, Any]:
    return _gate(NOT_ASSESSED, reason)


def _exception_fields(error: str | None) -> tuple[str | None, str | None, bool]:
    if not error:
        return None, None, False
    timeout = "execution_timeout" in error or error.startswith("TimeoutExpired")
    if timeout:
        return "TimeoutExpired", error, True
    if ": " in error:
        head, tail = error.split(": ", 1)
        if head and head.replace("_", "").isalnum() and head[:1].isupper():
            return head, tail, False
    return None, error, False


def _contract_evidence(returned_value: Any, frozen_payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(returned_value, dict):
        return {
            "schema_valid": False,
            "missing_keys": sorted(REQUIRED_RETURN_KEYS),
            "unexpected_keys": [],
            "field_types_valid": False,
            "frozen_parameters_valid": None,
            "entry_point_signature_valid": None,
        }
    keys = set(returned_value)
    missing = sorted(REQUIRED_RETURN_KEYS - keys)
    unexpected = sorted(keys - REQUIRED_RETURN_KEYS)
    question_ok = isinstance(returned_value.get("question_text"), str)
    answer_ok = "correct_answer" in returned_value and returned_value.get("correct_answer") is not None
    field_types_valid = question_ok and answer_ok and "oracle_payload" in returned_value
    frozen_ok = None
    if frozen_payload is not None and "oracle_payload" in returned_value:
        frozen_ok = returned_value.get("oracle_payload") == frozen_payload
    schema_valid = not missing and not unexpected and field_types_valid and (frozen_ok is not False)
    return {
        "schema_valid": schema_valid,
        "missing_keys": missing,
        "unexpected_keys": unexpected,
        "field_types_valid": field_types_valid,
        "frozen_parameters_valid": frozen_ok,
        "entry_point_signature_valid": None,
    }


def build_evaluation_gates_from_outcome(
    *,
    outcome: str,
    raw_response_available: bool,
    candidate_extracted: str | None,
    returned_value: Any,
    frozen_payload: dict[str, Any] | None = None,
    detail: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    """Map existing classify_response outcomes onto G1–G6 gate evidence."""
    detail = detail or {}
    actual_question_text = extract_actual_question_text(returned_value)
    correct_answer = returned_value.get("correct_answer") if isinstance(returned_value, dict) else None

    if outcome in {EXPERIMENT_NOT_RUN, "not_run"}:
        absent = _gate(
            NOT_OBSERVED, EXPERIMENT_NOT_RUN,
            raw_output_present=False,
            extraction_succeeded=None,
            candidate_nonempty=False,
            parse_succeeded=None,
            required_entry_point_present=None,
        )
        return {
            "g1_evaluability": absent,
            "g2_executability": _gate(NOT_OBSERVED, EXPERIMENT_NOT_RUN),
            "g3_contract_compliance": _gate(NOT_OBSERVED, EXPERIMENT_NOT_RUN),
            "g4_semantic_correctness": _gate(NOT_OBSERVED, EXPERIMENT_NOT_RUN),
            "g5_problem_presentation": evaluate_problem_presentation(None),
            "g6_math_notation": evaluate_math_notation(None),
        }

    extraction_succeeded = outcome not in {
        "empty_response", "catastrophic_truncation", "extraction_failure",
    } and bool(candidate_extracted)
    # missing_entry_point means parse succeeded but entry point failed
    if outcome in {"empty_response", "catastrophic_truncation", "extraction_failure"}:
        parse_succeeded = False
    elif outcome in {"parse_minor", "parse_failure"}:
        parse_succeeded = False
    else:
        parse_succeeded = True
    entry_present = outcome not in G1_FAIL_OUTCOMES and outcome != "parse_failure"
    if outcome == "missing_entry_point":
        entry_present = False
        parse_succeeded = True
        extraction_succeeded = bool(candidate_extracted)

    g1_fail_outcomes = G1_FAIL_OUTCOMES | {"parse_failure"}
    if outcome in g1_fail_outcomes:
        g1 = _gate(
            FAIL, outcome or "evaluability_failure",
            raw_output_present=raw_response_available,
            extraction_succeeded=extraction_succeeded,
            candidate_nonempty=bool(candidate_extracted),
            parse_succeeded=parse_succeeded,
            required_entry_point_present=entry_present,
        )
        g2 = g3 = g4 = _not_assessed("g1_not_passed")
    else:
        g1 = _gate(
            PASS, "evaluability_passed",
            raw_output_present=raw_response_available,
            extraction_succeeded=True,
            candidate_nonempty=bool(candidate_extracted),
            parse_succeeded=True,
            required_entry_point_present=True,
        )
        exception_type = detail.get("exception_type")
        exception_message = detail.get("exception_message") or detail.get("runtime_error")
        if exception_type is None and exception_message:
            exception_type, exception_message, _ = _exception_fields(exception_message)
        timeout = bool(detail.get("timeout")) or (
            isinstance(exception_message, str) and "execution_timeout" in exception_message
        ) or exception_type == "TimeoutExpired"

        if outcome in {"runtime_failure", "infrastructure_failure", "execution_failure"} or timeout:
            g2 = _gate(
                FAIL, outcome if outcome != "passed" else "execution_failure",
                load_succeeded=outcome != "infrastructure_failure",
                entry_point_called=outcome in {"runtime_failure", "execution_failure"} or timeout,
                timeout=timeout,
                exception_type=exception_type,
                exception_message=exception_message,
                return_value_produced=returned_value is not None,
            )
            g3 = g4 = _not_assessed("g2_not_passed")
        else:
            g2 = _gate(
                PASS, "execution_passed",
                load_succeeded=True,
                entry_point_called=True,
                timeout=False,
                exception_type=None,
                exception_message=None,
                return_value_produced=returned_value is not None,
            )
            contract = _contract_evidence(returned_value, frozen_payload)
            if outcome in {"schema_failure", "contract_schema_failure"} or not contract["schema_valid"]:
                g3 = _gate(FAIL, "contract_schema_failure", **contract)
                g4 = _not_assessed("g3_not_passed")
            else:
                g3 = _gate(PASS, "contract_observed", **contract)
                if outcome in {"answer_incorrect", "oracle_mismatch"}:
                    g4 = _gate(
                        FAIL, detail.get("mismatch_reason") or "oracle_mismatch",
                        oracle_executed=True,
                        oracle_match=False,
                        invariant_checks=None,
                        mismatch_reason=detail.get("mismatch_reason") or "oracle_mismatch",
                    )
                elif outcome == "intrinsic_safety":
                    g4 = _gate(
                        FAIL, detail.get("oracle_error") or "semantic_invariant_failure",
                        oracle_executed=True,
                        oracle_match=False,
                        invariant_checks=None,
                        mismatch_reason=detail.get("oracle_error") or "semantic_invariant_failure",
                    )
                elif outcome == "passed":
                    g4 = _gate(
                        PASS, "oracle_match",
                        oracle_executed=True,
                        oracle_match=True,
                        invariant_checks=None,
                        mismatch_reason=None,
                    )
                else:
                    g4 = _gate(
                        NOT_OBSERVED, "unmapped_outcome",
                        oracle_executed=None,
                        oracle_match=None,
                        invariant_checks=None,
                        mismatch_reason=None,
                    )

    if actual_question_text is None:
        g5 = evaluate_problem_presentation(None)
        g6 = evaluate_math_notation(None)
    else:
        g5 = evaluate_problem_presentation(
            actual_question_text,
            frozen_parameters=frozen_payload,
            correct_answer=correct_answer if isinstance(correct_answer, (str, int, float)) else None,
        )
        g6 = evaluate_math_notation(actual_question_text)

    return {
        "g1_evaluability": g1,
        "g2_executability": g2,
        "g3_contract_compliance": g3,
        "g4_semantic_correctness": g4,
        "g5_problem_presentation": g5,
        "g6_math_notation": g6,
    }


def build_evaluation_gates(*, raw_response_available: bool, extraction_status: str, extracted_code: str | None,
                           parse_status: str, entry_point_count: int | None, execution_status: str,
                           returned_value: Any, validation: Any, error_code: str | None,
                           actual_question_text: Any) -> dict[str, dict[str, Any]]:
    """Legacy MathEvaluationResult-shaped mapper retained for reuse."""
    g1_ok = (
        raw_response_available
        and extraction_status in {"success", "not_applicable"}
        and bool(extracted_code)
        and parse_status == "success"
        and entry_point_count == 1
    )
    g1 = _gate(
        PASS if g1_ok else FAIL,
        "evaluability_passed" if g1_ok else "evaluability_failure",
        raw_output_present=raw_response_available,
        extraction_succeeded=extraction_status in {"success", "not_applicable"},
        candidate_nonempty=bool(extracted_code),
        parse_succeeded=parse_status == "success",
        required_entry_point_present=entry_point_count == 1,
    )
    if not g1_ok:
        g2 = g3 = g4 = _not_assessed("g1_not_passed")
    else:
        g2_ok = execution_status == "success"
        g2 = _gate(
            PASS if g2_ok else FAIL,
            "execution_passed" if g2_ok else "execution_failure",
            load_succeeded=g2_ok,
            entry_point_called=g2_ok,
            timeout=execution_status == "timeout",
            exception_type=error_code if not g2_ok else None,
            exception_message=error_code if not g2_ok else None,
            return_value_produced=returned_value is not None,
        )
        if not g2_ok:
            g3 = g4 = _not_assessed("g2_not_passed")
        else:
            contract = _contract_evidence(returned_value, None)
            # Prefer validator field-level signals when available; otherwise schema evidence only.
            if validation is None:
                g3 = _gate(FAIL, "contract_not_observed", **contract)
                g4 = _not_assessed("g3_not_passed")
            else:
                missing = list(getattr(validation, "details", {}).get("missing_fields", []) or [])
                if validation.error_code in {"missing_field", "extra_field", "wrong_field", "invalid_type"}:
                    g3 = _gate(
                        FAIL, validation.error_code or "contract_schema_failure",
                        schema_valid=False,
                        missing_keys=missing,
                        unexpected_keys=list(getattr(validation, "details", {}).get("extra_fields", []) or []),
                        field_types_valid=validation.error_code != "invalid_type",
                        frozen_parameters_valid=None,
                        entry_point_signature_valid=None,
                    )
                    g4 = _not_assessed("g3_not_passed")
                else:
                    g3 = _gate(PASS, "contract_observed", **{**contract, "schema_valid": True})
                    g4 = _gate(
                        PASS if bool(validation.is_correct) else FAIL,
                        "oracle_match" if validation.is_correct else (validation.error_code or "oracle_mismatch"),
                        oracle_executed=True,
                        oracle_match=bool(validation.is_correct),
                        invariant_checks=None,
                        mismatch_reason=None if validation.is_correct else (validation.error_code or "oracle_mismatch"),
                    )
    question = actual_question_text if actual_question_text is not None else extract_actual_question_text(returned_value)
    correct_answer = returned_value.get("correct_answer") if isinstance(returned_value, dict) else None
    return {
        "g1_evaluability": g1,
        "g2_executability": g2,
        "g3_contract_compliance": g3,
        "g4_semantic_correctness": g4,
        "g5_problem_presentation": evaluate_problem_presentation(question, correct_answer=correct_answer if isinstance(correct_answer, (str, int, float)) else None),
        "g6_math_notation": evaluate_math_notation(question),
    }


def assemble_observed_success_fields(
    *,
    outcome: str,
    raw_response_available: bool,
    candidate_extracted: str | None,
    returned_value: Any = None,
    frozen_payload: dict[str, Any] | None = None,
    detail: dict[str, Any] | None = None,
    ledger_stage: str = "observed",
) -> dict[str, Any]:
    """Additive success-chain fields for a new observed generation artifact."""
    if ledger_stage not in LEDGER_STAGES:
        raise ValueError(f"unsupported ledger_stage: {ledger_stage!r}")
    gates = build_evaluation_gates_from_outcome(
        outcome=outcome,
        raw_response_available=raw_response_available,
        candidate_extracted=candidate_extracted,
        returned_value=returned_value,
        frozen_payload=frozen_payload,
        detail=detail,
    )
    return {
        "ledger_stage": ledger_stage,
        "actual_question_text": extract_actual_question_text(returned_value),
        "evaluation_gates": gates,
        "composite_outcomes": composite_outcomes(gates),
    }


def merge_success_fields(row: dict[str, Any], fields: dict[str, Any]) -> dict[str, Any]:
    """Additive merge; never deletes existing keys."""
    for key in OBSERVED_SUCCESS_FIELD_KEYS:
        if key in fields:
            row[key] = fields[key]
    for key in THREE_LEDGER_FIELD_KEYS:
        if key in fields:
            row[key] = fields[key]
    return row


def read_success_fields(record: dict[str, Any]) -> dict[str, Any]:
    """Old records missing new fields must not crash readers."""
    return {
        "ledger_stage": record.get("ledger_stage"),
        "actual_question_text": record.get("actual_question_text"),
        "evaluation_gates": record.get("evaluation_gates"),
        "composite_outcomes": record.get("composite_outcomes"),
        "record_id": record.get("record_id"),
        "source_record_id": record.get("source_record_id"),
        "correction_actions": record.get("correction_actions"),
        "healer": record.get("healer"),
        "observation_status": record.get("observation_status"),
    }


def build_healer_fields(
    *,
    eligible: bool | None = None,
    attempted: bool = False,
    rescued: bool = False,
    regression: bool = False,
    reason: str | None = None,
    actions: list[Any] | None = None,
) -> dict[str, Any]:
    """Pure healer ledger metadata. Ineligible must never count as attempted."""
    if eligible is False:
        attempted = False
        rescued = False
        if reason is None:
            reason = "ineligible"
    if not attempted:
        rescued = False
        # Regression still allowed as an explicit post-attempt observation, but
        # require attempted=True for regression=True below when constructing post_healer.
    return {
        "eligible": eligible,
        "attempted": bool(attempted),
        "rescued": bool(rescued) if attempted else False,
        "regression": bool(regression) if attempted else False,
        "reason": reason,
        "actions": list(actions or []),
    }


def observation_kind(outcome: str | None) -> str:
    """Distinguish missing runs from observed generator failures."""
    if outcome in {EXPERIMENT_NOT_RUN, "not_run", None}:
        return EXPERIMENT_NOT_RUN
    return GENERATOR_FAILURE if outcome != "passed" else "observed_success"


def serialize_artifact(record: dict[str, Any]) -> str:
    """JSON-serialize an artifact; reject non-JSON values (e.g. raw exception objects)."""
    return json.dumps(record, sort_keys=True, ensure_ascii=False, allow_nan=False)


def validate_gate_statuses(gates: dict[str, dict[str, Any]]) -> None:
    for name, gate in gates.items():
        status = gate.get("status")
        if status not in GATE_STATUSES:
            raise ValueError(f"invalid gate status for {name}: {status!r}")


def build_generator_artifact(
    *,
    record_id: str,
    outcome: str,
    raw_response_available: bool,
    candidate_extracted: str | None,
    returned_value: Any = None,
    frozen_payload: dict[str, Any] | None = None,
    detail: dict[str, Any] | None = None,
    ledger_stage: str = "observed",
    source_record_id: str | None = None,
    correction_actions: list[Any] | None = None,
    healer: dict[str, Any] | None = None,
    base: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an additive, JSON-safe generator artifact for any ledger stage."""
    if ledger_stage not in LEDGER_STAGES:
        raise ValueError(f"unsupported ledger_stage: {ledger_stage!r}")
    if ledger_stage != "observed" and not source_record_id:
        raise ValueError(f"{ledger_stage} requires source_record_id")
    success = assemble_observed_success_fields(
        outcome=outcome,
        raw_response_available=raw_response_available,
        candidate_extracted=candidate_extracted,
        returned_value=returned_value,
        frozen_payload=frozen_payload,
        detail=detail,
        ledger_stage=ledger_stage,
    )
    validate_gate_statuses(success["evaluation_gates"])
    row = dict(base or {})
    merge_success_fields(row, success)
    row["record_id"] = record_id
    row["source_record_id"] = source_record_id
    row["correction_actions"] = list(correction_actions or [])
    row["observation_status"] = observation_kind(outcome if raw_response_available or outcome == EXPERIMENT_NOT_RUN else EXPERIMENT_NOT_RUN)
    if outcome == EXPERIMENT_NOT_RUN:
        row["observation_status"] = EXPERIMENT_NOT_RUN
    default_healer = build_healer_fields(eligible=None, attempted=False, rescued=False, regression=False)
    if ledger_stage == "observed":
        row["healer"] = healer if healer is not None else default_healer
    elif ledger_stage == "pipeline_corrected":
        row["healer"] = healer if healer is not None else default_healer
    else:
        if healer is None:
            raise ValueError("post_healer requires an explicit healer block")
        row["healer"] = healer
    if "raw_first_attempt_output" not in row:
        row["raw_first_attempt_output"] = None
    # Builder arg is authoritative so pipeline/post_healer can replace observed candidate.
    row["candidate_extracted"] = candidate_extracted
    if "actual_question_text" in row and row["actual_question_text"] is not None:
        if not isinstance(row["actual_question_text"], str):
            raise TypeError("actual_question_text must be str or null")
    serialize_artifact(row)  # fail closed on non-serializable content
    return row


def derive_pipeline_corrected_record(
    observed: dict[str, Any],
    *,
    record_id: str,
    correction_actions: list[Any],
    outcome: str,
    candidate_extracted: str | None,
    returned_value: Any = None,
    frozen_payload: dict[str, Any] | None = None,
    detail: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Independent pipeline-corrected ledger row; never mutates observed."""
    if not correction_actions:
        raise ValueError("pipeline_corrected requires deterministic correction_actions")
    # Preserve raw bytes/text from observed; pipeline must not rewrite first attempt raw.
    base = {
        key: value for key, value in observed.items()
        if key not in {*OBSERVED_SUCCESS_FIELD_KEYS, *THREE_LEDGER_FIELD_KEYS}
    }
    base["raw_first_attempt_output"] = observed.get("raw_first_attempt_output")
    return build_generator_artifact(
        record_id=record_id,
        outcome=outcome,
        raw_response_available=bool(observed.get("raw_first_attempt_output")),
        candidate_extracted=candidate_extracted,
        returned_value=returned_value,
        frozen_payload=frozen_payload,
        detail=detail,
        ledger_stage="pipeline_corrected",
        source_record_id=observed.get("record_id") or observed.get("source_record_id"),
        correction_actions=correction_actions,
        healer=build_healer_fields(eligible=None, attempted=False),
        base=base,
    )


def derive_post_healer_record(
    observed: dict[str, Any],
    *,
    record_id: str,
    healer: dict[str, Any],
    outcome: str,
    candidate_extracted: str | None = None,
    returned_value: Any = None,
    frozen_payload: dict[str, Any] | None = None,
    detail: dict[str, Any] | None = None,
    correction_actions: list[Any] | None = None,
) -> dict[str, Any]:
    """Independent post-Healer ledger row; never mutates observed or pipeline rows."""
    if healer.get("eligible") is False and healer.get("attempted"):
        raise ValueError("ineligible healer must not set attempted=true")
    if healer.get("regression") and not healer.get("attempted"):
        raise ValueError("regression requires attempted=true")
    if healer.get("rescued") and not healer.get("attempted"):
        raise ValueError("rescued requires attempted=true")
    if healer.get("eligible") is False:
        # Document ineligibility only: no repaired candidate, no fabricated pass.
        base = {
            key: value for key, value in observed.items()
            if key not in THREE_LEDGER_FIELD_KEYS
        }
        row = dict(base)
        row["ledger_stage"] = "post_healer"
        row["record_id"] = record_id
        row["source_record_id"] = observed.get("record_id")
        row["correction_actions"] = list(correction_actions or [])
        row["healer"] = healer
        row["candidate_extracted"] = observed.get("candidate_extracted")
        row["raw_first_attempt_output"] = observed.get("raw_first_attempt_output")
        if "observation_status" not in row:
            row["observation_status"] = observed.get("observation_status")
        serialize_artifact(row)
        return row
    base = {
        key: value for key, value in observed.items()
        if key not in {*OBSERVED_SUCCESS_FIELD_KEYS, *THREE_LEDGER_FIELD_KEYS}
    }
    base["raw_first_attempt_output"] = observed.get("raw_first_attempt_output")
    return build_generator_artifact(
        record_id=record_id,
        outcome=outcome,
        raw_response_available=bool(observed.get("raw_first_attempt_output")),
        candidate_extracted=candidate_extracted,
        returned_value=returned_value,
        frozen_payload=frozen_payload,
        detail=detail,
        ledger_stage="post_healer",
        source_record_id=observed.get("record_id"),
        correction_actions=list(correction_actions or []),
        healer=healer,
        base=base,
    )
