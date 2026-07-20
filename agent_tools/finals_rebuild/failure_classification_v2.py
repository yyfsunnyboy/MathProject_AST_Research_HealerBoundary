"""Failure classification standard v2 — shared L0–L5 / outcome_validity taxonomy.

Implements docs/standards/failure_classification_standard_v2.md:
- §3 outcome_validity
- §4 L0–L5
- §5 mechanism_tags (+ degenerate_repetition, complexity_induced_derailment)
- §7.2 Healer outcomes
- §8 cell-record schema validation
- §9 classify_cell decision flow

Does not call models, mutate artifacts, or re-score historical runs.
"""
from __future__ import annotations

from typing import Any, Mapping

# ---------------------------------------------------------------------------
# §4 Layers
# ---------------------------------------------------------------------------

FAILURE_LAYERS: tuple[str, ...] = ("L0", "L1", "L2", "L3", "L4", "L5")
PRIMARY_FAILURE_LAYER_VALUES: tuple[str, ...] = FAILURE_LAYERS + ("PASSED",)

# ---------------------------------------------------------------------------
# §3 outcome_validity (five values)
# ---------------------------------------------------------------------------

OUTCOME_VALIDITY_VALUES: tuple[str, ...] = (
    "VALID_MODEL_OUTCOME",
    "INVALID_EVALUATOR",
    "INVALID_CONTRACT",
    "INVALID_INFRASTRUCTURE",
    "PENDING_REVIEW",
)

# ---------------------------------------------------------------------------
# Gate statuses (G1–G4 + G3a/G3c)
# ---------------------------------------------------------------------------

GATE_STATUS_VALUES: tuple[str, ...] = (
    "PASS",
    "FAIL",
    "NOT_ASSESSED",
    "NOT_APPLICABLE",
    "NOT_OBSERVED",
)

GATE_KEYS: tuple[str, ...] = (
    "g1_parse",
    "g2_execution",
    "g3_contract",
    "g3a_required_api",
    "g3c_canonical_form",
    "g4_correctness",
)

# ---------------------------------------------------------------------------
# §5 mechanism_tags (+ extras required by task brief)
# ---------------------------------------------------------------------------

MECHANISM_TAGS: tuple[str, ...] = (
    "prompt_api_mismatch",
    "model_assembly_failure",
    "tool_routing_failure",
    "return_shape_hallucination",
    "code_bloat",
    "infrastructure_failure",
    "output_packaging",
    "semantic_goal_drift",
    "parameter_semantics_swap",
    "answer_leak",
    "needs_human_review",
    # Task brief extras (beyond §5 table)
    "degenerate_repetition",
    "complexity_induced_derailment",
    # Documented L3 mechanisms (§4 L3)
    "invalid_api_call",
    "missing_import",
    "local_api_shadowing",
    "partial_adoption",
)

# ---------------------------------------------------------------------------
# §7.2 Healer outcomes (eight)
# ---------------------------------------------------------------------------

HEALER_OUTCOME_VALUES: tuple[str, ...] = (
    "noneligible",
    "no_trigger",
    "changed_partial_progress",
    "rescue_to_pass",
    "rejected",
    "rollback",
    "false_positive",
    "abstained",
)

# ---------------------------------------------------------------------------
# §8 required cell-record fields
# ---------------------------------------------------------------------------

REQUIRED_CELL_RECORD_FIELDS: tuple[str, ...] = (
    "dataset",
    "task_id",
    "model",
    "condition",
    "seed",
    "prompt_hash",
    "evaluator_hash",
    "evaluation_revision",
    "infrastructure_valid",
    "raw_response_present",
    "candidate_present",
    "g1_parse",
    "g2_execution",
    "g3_contract",
    "g3a_required_api",
    "g3c_canonical_form",
    "g4_correctness",
    "final_status",
    "primary_failure_layer",
    "outcome_validity",
    "failure_subtype",
    "mechanism_tags",
    "failure_chain",
    "exception_type",
    "exception_message",
    "healer_eligible",
    "matched_rule",
    "healer_outcome",
    "review_status",
    "notes",
)

FINAL_STATUS_VALUES: tuple[str, ...] = ("PASSED", "FAILED")

NEEDS_HUMAN_REVIEW = "needs_human_review"


class CellRecordSchemaError(ValueError):
    """Raised when a v2 cell record fails schema validation."""


def _norm_gate(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip().upper()
    aliases = {
        "PASSED": "PASS",
        "FAILED": "FAIL",
        "NA": "NOT_APPLICABLE",
        "N/A": "NOT_APPLICABLE",
        "NOTAPPLICABLE": "NOT_APPLICABLE",
        "NOTASSESSED": "NOT_ASSESSED",
        "NOTOBSERVED": "NOT_OBSERVED",
    }
    text = aliases.get(text, text)
    return text


def _gate(gate_results: Mapping[str, Any], *keys: str) -> str | None:
    for key in keys:
        if key in gate_results and gate_results[key] is not None:
            return _norm_gate(gate_results[key])
    return None


def classify_cell(
    gate_results: Mapping[str, Any],
    evidence: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Classify a cell per standard §9.

    Parameters
    ----------
    gate_results:
        Must include G1–G4 (+ optional G3a/G3c) statuses under either short
        keys (g1_parse, …) or legacy Math16 keys (g1_evaluability, …).
    evidence:
        Optional adjudication hints. Missing evidence that the flow needs
        yields ``needs_human_review`` — never guessed.

    Returns a dict with at least:
      primary_failure_layer, outcome_validity, mechanism_tags,
      needs_human_review, final_status.
    """
    evidence = dict(evidence or {})
    g1 = _gate(gate_results, "g1_parse", "g1_evaluability", "g1")
    g2 = _gate(gate_results, "g2_execution", "g2_executability", "g2")
    g3 = _gate(gate_results, "g3_contract", "g3_contract_compliance", "g3")
    g3a = _gate(gate_results, "g3a_required_api", "g3a")
    g3c = _gate(gate_results, "g3c_canonical_form", "g3c")
    g4 = _gate(gate_results, "g4_correctness", "g4_semantic_correctness", "g4")

    tags: list[str] = []
    for tag in evidence.get("mechanism_tags") or []:
        if tag not in tags:
            tags.append(str(tag))

    def _result(
        layer: str | None,
        validity: str,
        *,
        final_status: str,
        extra_tags: list[str] | None = None,
        needs_review: bool = False,
        note: str = "",
    ) -> dict[str, Any]:
        out_tags = list(tags)
        for t in extra_tags or []:
            if t not in out_tags:
                out_tags.append(t)
        if needs_review and NEEDS_HUMAN_REVIEW not in out_tags:
            out_tags.append(NEEDS_HUMAN_REVIEW)
        return {
            "primary_failure_layer": layer,
            "outcome_validity": validity,
            "mechanism_tags": out_tags,
            "needs_human_review": needs_review,
            "final_status": final_status,
            "note": note,
            "gates_normalized": {
                "g1_parse": g1,
                "g2_execution": g2,
                "g3_contract": g3,
                "g3a_required_api": g3a,
                "g3c_canonical_form": g3c,
                "g4_correctness": g4,
            },
        }

    # §9.1 Infrastructure
    infra_ok = evidence.get("infrastructure_valid")
    if infra_ok is None and "infrastructure_ok" in evidence:
        infra_ok = evidence.get("infrastructure_ok")
    if infra_ok is False or evidence.get("raw_response_present") is False:
        return _result(
            "L0",
            "INVALID_INFRASTRUCTURE",
            final_status="FAILED",
            extra_tags=["infrastructure_failure"],
            note="infrastructure or missing raw response",
        )

    # Explicit validity overrides from forensic (do not invent; caller supplies)
    forced_validity = evidence.get("outcome_validity")
    if forced_validity is not None and forced_validity not in OUTCOME_VALIDITY_VALUES:
        return _result(
            None,
            "PENDING_REVIEW",
            final_status="FAILED",
            needs_review=True,
            note=f"illegal outcome_validity override: {forced_validity}",
        )

    # §9.2 Parse
    if g1 == "FAIL":
        validity = forced_validity or "VALID_MODEL_OUTCOME"
        return _result("L1", validity, final_status="FAILED", note="G1 FAIL")

    if g1 not in {"PASS", None}:
        # Unknown / missing G1 when infra claimed valid → review
        if g1 is None and evidence.get("assume_gates_complete"):
            return _result(
                None,
                "PENDING_REVIEW",
                final_status="FAILED",
                needs_review=True,
                note="G1 status missing",
            )

    # §9.3 Execution
    if g2 == "FAIL":
        source = evidence.get("exception_source")
        # exception_source: api_call | dataflow | serialization | unknown | None
        if source is None or source == "unknown":
            return _result(
                None,
                forced_validity or "PENDING_REVIEW",
                final_status="FAILED",
                needs_review=True,
                note="G2 FAIL but exception_source undistinguished",
            )
        if source == "api_call":
            if forced_validity:
                validity = forced_validity
            else:
                api_doc_ok = evidence.get("api_documentation_consistent")
                if api_doc_ok is None:
                    return _result(
                        "L3",
                        "PENDING_REVIEW",
                        final_status="FAILED",
                        needs_review=True,
                        extra_tags=["invalid_api_call"],
                        note="G2 FAIL at API call; api_documentation_consistent unknown",
                    )
                validity = (
                    "VALID_MODEL_OUTCOME"
                    if api_doc_ok
                    else "INVALID_CONTRACT"
                )
                if not api_doc_ok and "prompt_api_mismatch" not in tags:
                    tags.append("prompt_api_mismatch")
            return _result(
                "L3",
                validity,
                final_status="FAILED",
                extra_tags=["invalid_api_call"],
                note="G2 FAIL at API call point",
            )
        if source == "serialization":
            validity = forced_validity or "INVALID_CONTRACT"
            return _result(
                "L4",
                validity,
                final_status="FAILED",
                note="G2 FAIL from evaluator serialization/interface",
            )
        if source == "dataflow":
            validity = forced_validity or "VALID_MODEL_OUTCOME"
            return _result(
                "L4",
                validity,
                final_status="FAILED",
                extra_tags=["model_assembly_failure"],
                note="G2 FAIL from model dataflow/assembly",
            )
        return _result(
            None,
            "PENDING_REVIEW",
            final_status="FAILED",
            needs_review=True,
            note=f"unrecognized exception_source={source}",
        )

    # Treat G3c FAIL as contract fail (canonical form → L2)
    contract_fail = g3 == "FAIL" or g3c == "FAIL"

    # §9.4 Contract / packaging / canonical form
    if contract_fail:
        schema_explicit = evidence.get("schema_explicit_in_prompt")
        if forced_validity:
            validity = forced_validity
        elif schema_explicit is False:
            validity = "INVALID_CONTRACT"
        elif schema_explicit is True:
            validity = "VALID_MODEL_OUTCOME"
        else:
            return _result(
                "L2",
                "PENDING_REVIEW",
                final_status="FAILED",
                needs_review=True,
                extra_tags=["output_packaging"],
                note="G3/G3c FAIL; schema_explicit_in_prompt unknown",
            )
        return _result(
            "L2",
            validity,
            final_status="FAILED",
            extra_tags=["output_packaging"],
            note="G3 or G3c FAIL",
        )

    # §9.5 required API (G3a)
    if g3a == "FAIL":
        validity = forced_validity or "VALID_MODEL_OUTCOME"
        return _result(
            "L3",
            validity,
            final_status="FAILED",
            extra_tags=["partial_adoption"],
            note="G3a required API not adopted",
        )

    # §9.6 Correctness
    if g4 == "FAIL":
        evaluator_fault = evidence.get("evaluator_logic_fault")
        if evaluator_fault is True:
            return _result(
                "L5",
                forced_validity or "INVALID_EVALUATOR",
                final_status="FAILED",
                note="G4 FAIL attributed to evaluator logic",
            )
        if evaluator_fault is False:
            return _result(
                "L5",
                forced_validity or "VALID_MODEL_OUTCOME",
                final_status="FAILED",
                note="G4 FAIL confirmed model-semantic",
            )
        if forced_validity == "INVALID_EVALUATOR":
            return _result(
                "L5",
                "INVALID_EVALUATOR",
                final_status="FAILED",
                note="G4 FAIL with forced INVALID_EVALUATOR",
            )
        return _result(
            "L5",
            forced_validity or "PENDING_REVIEW",
            final_status="FAILED",
            needs_review=forced_validity is None,
            note="G4 FAIL; evaluator_logic_fault unknown",
        )

    # §9.7 All pass
    all_core_pass = g1 == "PASS" and g2 == "PASS" and (
        g3 in {"PASS", "NOT_APPLICABLE", "NOT_ASSESSED", None} or g3 == "PASS"
    )
    # Require g3 PASS when assessed
    if g3 == "FAIL" or g3c == "FAIL" or g3a == "FAIL" or g4 == "FAIL":
        # Should have been handled above; defensive
        return _result(
            None,
            "PENDING_REVIEW",
            final_status="FAILED",
            needs_review=True,
            note="unexpected residual gate FAIL",
        )

    if g1 == "PASS" and g2 == "PASS" and g4 == "PASS" and g3 in {
        "PASS",
        "NOT_APPLICABLE",
        None,
    }:
        false_pass = evidence.get("evaluator_false_pass")
        if false_pass is True:
            return _result(
                "PASSED",
                "INVALID_EVALUATOR",
                final_status="PASSED",
                needs_review=True,
                note="gates PASS but evaluator_false_pass flagged",
            )
        validity = forced_validity or "VALID_MODEL_OUTCOME"
        return _result(
            "PASSED",
            validity,
            final_status="PASSED",
            note="G1–G4 pass",
        )

    # Incomplete gate vector
    return _result(
        None,
        forced_validity or "PENDING_REVIEW",
        final_status="FAILED",
        needs_review=True,
        note="insufficient gate evidence for §9 flow",
    )


_NULLABLE_FIELDS = frozenset(
    {
        "exception_type",
        "exception_message",
        "matched_rule",
        "failure_subtype",
        "notes",
    }
)


def validate_cell_record(record: Mapping[str, Any]) -> list[str]:
    """Validate §8 required fields. Returns a list of error strings (empty = ok)."""
    errors: list[str] = []
    for field in REQUIRED_CELL_RECORD_FIELDS:
        if field not in record:
            errors.append(f"missing_field:{field}")
            continue
        value = record[field]
        if value is None and field not in _NULLABLE_FIELDS:
            if field in GATE_KEYS:
                errors.append(f"null_not_allowed:{field}_use_NOT_APPLICABLE")
            else:
                errors.append(f"null_not_allowed:{field}")

    for gate in GATE_KEYS:
        if gate not in record:
            continue
        status = _norm_gate(record[gate])
        if status is None:
            errors.append(f"null_not_allowed:{gate}_use_NOT_APPLICABLE")
        elif status not in GATE_STATUS_VALUES:
            errors.append(f"illegal_gate_status:{gate}={record[gate]}")

    layer = record.get("primary_failure_layer")
    if "primary_failure_layer" in record and layer is not None:
        if layer not in PRIMARY_FAILURE_LAYER_VALUES:
            errors.append(f"illegal_primary_failure_layer:{layer}")

    validity = record.get("outcome_validity")
    if "outcome_validity" in record and validity is not None:
        if validity not in OUTCOME_VALIDITY_VALUES:
            errors.append(f"illegal_outcome_validity:{validity}")

    final_status = record.get("final_status")
    if "final_status" in record and final_status is not None:
        if final_status not in FINAL_STATUS_VALUES:
            errors.append(f"illegal_final_status:{final_status}")

    tags = record.get("mechanism_tags")
    if "mechanism_tags" in record:
        if not isinstance(tags, list):
            errors.append("illegal_mechanism_tags:not_a_list")
        else:
            for tag in tags:
                if tag not in MECHANISM_TAGS:
                    errors.append(f"illegal_mechanism_tag:{tag}")

    chain = record.get("failure_chain")
    if "failure_chain" in record and not isinstance(chain, list):
        errors.append("illegal_failure_chain:not_a_list")

    healer = record.get("healer_outcome")
    if "healer_outcome" in record:
        if healer is None:
            errors.append("null_not_allowed:healer_outcome")
        elif healer not in HEALER_OUTCOME_VALUES:
            errors.append(f"illegal_healer_outcome:{healer}")

    for hash_field in ("prompt_hash", "evaluator_hash"):
        value = record.get(hash_field)
        if value is not None and (not isinstance(value, str) or not value.strip()):
            errors.append(f"empty_{hash_field}")

    return errors


def assert_valid_cell_record(record: Mapping[str, Any]) -> None:
    """Raise CellRecordSchemaError if record is invalid."""
    errors = validate_cell_record(record)
    if errors:
        raise CellRecordSchemaError("; ".join(errors))


def build_v2_fields_from_classification(
    classification: Mapping[str, Any],
    *,
    dataset: str,
    task_id: str,
    model: str,
    condition: str,
    seed: int,
    prompt_hash: str,
    evaluator_hash: str,
    evaluation_revision: str,
    infrastructure_valid: bool,
    raw_response_present: bool,
    candidate_present: bool,
    failure_subtype: str | None = None,
    failure_chain: list[str] | None = None,
    exception_type: str | None = None,
    exception_message: str | None = None,
    healer_eligible: bool = False,
    matched_rule: str | None = None,
    healer_outcome: str = "noneligible",
    review_status: str = "machine_labeled",
    notes: str = "",
) -> dict[str, Any]:
    """Assemble a §8 cell-record fragment for future runners (additive)."""
    gates = classification.get("gates_normalized") or {}
    record = {
        "dataset": dataset,
        "task_id": task_id,
        "model": model,
        "condition": condition,
        "seed": seed,
        "prompt_hash": prompt_hash,
        "evaluator_hash": evaluator_hash,
        "evaluation_revision": evaluation_revision,
        "infrastructure_valid": infrastructure_valid,
        "raw_response_present": raw_response_present,
        "candidate_present": candidate_present,
        "g1_parse": gates.get("g1_parse") or "NOT_ASSESSED",
        "g2_execution": gates.get("g2_execution") or "NOT_ASSESSED",
        "g3_contract": gates.get("g3_contract") or "NOT_ASSESSED",
        "g3a_required_api": gates.get("g3a_required_api") or "NOT_APPLICABLE",
        "g3c_canonical_form": gates.get("g3c_canonical_form") or "NOT_APPLICABLE",
        "g4_correctness": gates.get("g4_correctness") or "NOT_ASSESSED",
        "final_status": classification.get("final_status") or "FAILED",
        "primary_failure_layer": classification.get("primary_failure_layer"),
        "outcome_validity": classification.get("outcome_validity"),
        "failure_subtype": failure_subtype,
        "mechanism_tags": list(classification.get("mechanism_tags") or []),
        "failure_chain": list(failure_chain or []),
        "exception_type": exception_type,
        "exception_message": exception_message,
        "healer_eligible": healer_eligible,
        "matched_rule": matched_rule,
        "healer_outcome": healer_outcome,
        "review_status": review_status,
        "notes": notes,
        "needs_human_review": bool(classification.get("needs_human_review")),
    }
    return record


def math16_gates_from_evaluation_gates(evaluation_gates: Mapping[str, Any] | None) -> dict[str, str]:
    """Map Math16 evaluation_gates dict into v2 G1–G4 (+G3a/G3c) statuses."""
    gates = evaluation_gates or {}

    def _status(key_primary: str, key_alt: str | None = None) -> str:
        node = gates.get(key_primary)
        if node is None and key_alt:
            node = gates.get(key_alt)
        if not isinstance(node, dict):
            return "NOT_ASSESSED"
        status = _norm_gate(node.get("status"))
        return status or "NOT_ASSESSED"

    return {
        "g1_parse": _status("g1_evaluability", "g1_parse"),
        "g2_execution": _status("g2_executability", "g2_execution"),
        "g3_contract": _status("g3_contract_compliance", "g3_contract"),
        "g3a_required_api": "NOT_APPLICABLE",
        "g3c_canonical_form": "NOT_APPLICABLE",
        "g4_correctness": _status("g4_semantic_correctness", "g4_correctness"),
    }


def classify_math16_cell_for_future_runner(
    *,
    evaluation_gates: Mapping[str, Any] | None,
    evaluator_status: str | None,
    validity: str | None = None,
    infrastructure_valid: bool = True,
    raw_response_present: bool = True,
    exception_source: str | None = None,
    schema_explicit_in_prompt: bool | None = None,
    evaluator_logic_fault: bool | None = None,
    api_documentation_consistent: bool | None = None,
    mechanism_tags: list[str] | None = None,
) -> dict[str, Any]:
    """Future-run helper: classify Math16 cell with v2 §9 (no artifact mutation)."""
    gate_results = math16_gates_from_evaluation_gates(evaluation_gates)
    # If gates incomplete but status is PASSED, synthesize PASS vector.
    if (evaluator_status or "").upper() == "PASSED":
        for key in ("g1_parse", "g2_execution", "g3_contract", "g4_correctness"):
            if gate_results.get(key) in {None, "NOT_ASSESSED", "NOT_OBSERVED"}:
                gate_results[key] = "PASS"

    evidence: dict[str, Any] = {
        "infrastructure_valid": infrastructure_valid,
        "raw_response_present": raw_response_present,
        "mechanism_tags": list(mechanism_tags or []),
    }
    if validity in OUTCOME_VALIDITY_VALUES:
        evidence["outcome_validity"] = validity
    if exception_source is not None:
        evidence["exception_source"] = exception_source
    if schema_explicit_in_prompt is not None:
        evidence["schema_explicit_in_prompt"] = schema_explicit_in_prompt
    if evaluator_logic_fault is not None:
        evidence["evaluator_logic_fault"] = evaluator_logic_fault
    if api_documentation_consistent is not None:
        evidence["api_documentation_consistent"] = api_documentation_consistent

    # Infer minimal evidence from status when caller did not supply it (still
    # refuses to invent exception_source for ambiguous G2 FAIL).
    status = (evaluator_status or "").upper()
    if status in {"SCHEMA_FAILURE", "STRUCTURAL_MISMATCH", "LATEX_MISMATCH"}:
        evidence.setdefault("schema_explicit_in_prompt", True)
    if status in {"ANSWER_INCORRECT", "INTRINSIC_SAFETY"}:
        evidence.setdefault("evaluator_logic_fault", False)
    if status in {"EXECUTION_FAILURE", "RUNTIME_FAILURE"} and exception_source is None:
        # Leave undistinguished → needs_human_review per §9.3
        pass

    return classify_cell(gate_results, evidence)


__all__ = [
    "CellRecordSchemaError",
    "FAILURE_LAYERS",
    "FINAL_STATUS_VALUES",
    "GATE_KEYS",
    "GATE_STATUS_VALUES",
    "HEALER_OUTCOME_VALUES",
    "MECHANISM_TAGS",
    "NEEDS_HUMAN_REVIEW",
    "OUTCOME_VALIDITY_VALUES",
    "PRIMARY_FAILURE_LAYER_VALUES",
    "REQUIRED_CELL_RECORD_FIELDS",
    "assert_valid_cell_record",
    "build_v2_fields_from_classification",
    "classify_cell",
    "classify_math16_cell_for_future_runner",
    "math16_gates_from_evaluation_gates",
    "validate_cell_record",
]
