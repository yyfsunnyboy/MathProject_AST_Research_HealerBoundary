# -*- coding: utf-8 -*-
"""Authoritative Math16 observational PASS/FAIL evaluator binding (v1).

Pins the frozen Round-1 / fail-gated Aggressive scoring chain without rewriting
a new judge:

  classify_math16_response → classify_outcome_to_v3 → PASSED|FAILED
  → protocol-layer PASS|FAIL

This module is observational only: it must not mutate source, sealed artifacts,
or Healer rules. Callers may inject the returned callback into fixpoint / safety
runners; default CLIs must not invoke it unless formal execution is authorized.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Mapping, Optional

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent_tools.finals_rebuild.math16_pool import frozen_for_prompt, tasks_by_id  # noqa: E402
from scripts.evaluate_math16_pilot02_full_v4 import (  # noqa: E402
    _load_family_and_api_policy,
    classify_outcome_to_v3,
)
from scripts.run_math16_latex_v1_gemini_live import classify_math16_response  # noqa: E402

AUTHORITATIVE_BINDING = {
    "binding_id": "math16_observational_evaluator_v1",
    "classifier_module": "scripts.run_math16_latex_v1_gemini_live",
    "classifier_function": "classify_math16_response",
    "mapper_module": "scripts.evaluate_math16_pilot02_full_v4",
    "mapper_function": "classify_outcome_to_v3",
    "wrapper_reference": (
        "scripts.run_math16_c5a_c5c_tier_d_d5_d2_qwen9b_fail_gated_authoritative_v1"
        ".score_source"
    ),
    "method2_protocol_pin": (
        "docs/experiments/manifests/math16_method2_all_cell_protocol_v1.json"
        " → evaluator/classifier/outcome_mapper"
    ),
    "scoring_layer_statuses": ["PASSED", "FAILED"],
    "protocol_layer_statuses": ["PASS", "FAIL"],
    "execution_timeout_seconds": 3.0,
    "mutates_source": False,
    "mutates_artifacts": False,
    "evaluator_blind_for_rule_selection": True,
    "evidence": [
        "scripts/run_math16_c5a_c5c_tier_d_d5_d2_qwen9b_fail_gated_authoritative_v1.py::score_source",
        "docs/experiments/manifests/math16_method2_all_cell_protocol_v1.json",
        "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/scoring_manifest.json",
    ],
}


class ObservationalEvaluatorError(RuntimeError):
    """Raised when the authoritative observational binding cannot be resolved."""


def map_scoring_status_to_protocol(status: str) -> str:
    """Map scoring-layer PASSED|FAILED to protocol-layer PASS|FAIL."""
    if status == "PASSED":
        return "PASS"
    if status == "FAILED":
        return "FAIL"
    raise ObservationalEvaluatorError(f"unexpected scoring status: {status!r}")


def score_source(
    source: str,
    *,
    task: Mapping[str, Any],
    frozen_params: Mapping[str, Any],
    api_policy: str,
) -> dict[str, Any]:
    """Authoritative observational score_source (identical semantics to Round-1).

    Returns scoring-layer fields; does not write files or mutate ``source``.
    """
    outcome, _source, details = classify_math16_response(
        source,
        frozen_params=dict(frozen_params),
        audit_oracle_payload=task["oracle_payload"],
        task=dict(task),
    )
    mapped = classify_outcome_to_v3(outcome, details, api_policy=api_policy)
    status = mapped["final_status"]
    if status not in {"PASSED", "FAILED"}:
        raise ObservationalEvaluatorError(f"UNEXPECTED_STATUS: {status}")
    return {
        "status": status,
        "classifier_outcome": outcome,
        "primary_failure_layer": mapped["primary_failure_layer"],
        "failure_subtype": mapped["failure_subtype"],
    }


def resolve_task_and_api_policy(task_id: str) -> tuple[dict[str, Any], str]:
    tasks = tasks_by_id()
    if task_id not in tasks:
        raise ObservationalEvaluatorError(f"unknown task_id: {task_id}")
    _, api_policy_map = _load_family_and_api_policy()
    if task_id not in api_policy_map:
        raise ObservationalEvaluatorError(f"missing api_policy for {task_id}")
    return tasks[task_id], api_policy_map[task_id]


def make_observational_pass_fail_evaluator(
    *,
    task_id: str,
    task: Optional[Mapping[str, Any]] = None,
    api_policy: Optional[str] = None,
) -> Callable[[str], str]:
    """Build a unique observational callback: source text → PASS|FAIL.

    The callback is evaluator-blind w.r.t. Healer mutation: callers must apply
    the frozen stack first, then observe. It must not accept/rollback source.
    """
    resolved_task, resolved_policy = resolve_task_and_api_policy(task_id)
    task_obj = dict(task) if task is not None else resolved_task
    policy = api_policy if api_policy is not None else resolved_policy
    frozen_params = frozen_for_prompt(task_obj)["oracle_payload"]

    def _evaluate(source: str) -> str:
        scored = score_source(
            source,
            task=task_obj,
            frozen_params=frozen_params,
            api_policy=policy,
        )
        return map_scoring_status_to_protocol(scored["status"])

    _evaluate.__name__ = "math16_observational_pass_fail_evaluator_v1"
    _evaluate.__doc__ = (
        "Authoritative Math16 observational evaluator "
        f"(task_id={task_id}, binding={AUTHORITATIVE_BINDING['binding_id']})"
    )
    return _evaluate


def make_observational_evaluator_for_cell(
    cell: Mapping[str, Any],
) -> Callable[[str], str]:
    """Convenience: build PASS|FAIL callback from a Round-1 cell mapping."""
    task_id = str(cell["task_id"])
    return make_observational_pass_fail_evaluator(task_id=task_id)


def evaluator_binding_report() -> dict[str, Any]:
    """Machine-readable pin used by 9B protocols / preflight (no scoring)."""
    # Importability check only — does not score any cell.
    assert callable(classify_math16_response)
    assert callable(classify_outcome_to_v3)
    assert callable(score_source)
    assert callable(make_observational_pass_fail_evaluator)
    return {
        "ok": True,
        "binding": AUTHORITATIVE_BINDING,
        "injectable_factory": (
            "agent_tools.finals_rebuild.math16_observational_evaluator_v1"
            ".make_observational_pass_fail_evaluator"
        ),
        "cell_factory": (
            "agent_tools.finals_rebuild.math16_observational_evaluator_v1"
            ".make_observational_evaluator_for_cell"
        ),
        "protocol_status_mapping": {"PASSED": "PASS", "FAILED": "FAIL"},
        "formal_invocation_default": False,
    }
