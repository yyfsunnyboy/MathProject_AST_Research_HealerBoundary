"""Production promotion tests for kwargs-bag inline + json.dumps unwrap chain."""

from __future__ import annotations

import json
from pathlib import Path

from agent_tools.finals_rebuild.ce115_research_healer_protocol import provenance_to_dict
from agent_tools.finals_rebuild.ce115_research_healer_rules_l2_json_dumps_unwrap import (
    PRODUCTION_APPROVED as DUMPS_APPROVED,
    RULE_ID as DUMPS_ID,
)
from agent_tools.finals_rebuild.ce115_research_healer_rules_l2_kwargs_bag_inline import (
    PRODUCTION_APPROVED as KWARGS_APPROVED,
    RULE_ID as KWARGS_ID,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    RECOMMENDED_CHAIN_MAX_PASSES,
    RULE_ALLOWLIST,
    MathHealerRunner,
    run_research_healer,
)
from agent_tools.finals_rebuild.math_boundary_pilot import classify_response

ROOT = Path(__file__).resolve().parents[2]
CELL = (
    ROOT
    / "docs/experiments/results/ce115_exam_ext_contract_aligned_v2_qwen4b_01/cells"
    / "qwen3_5_4b__ce115_ext_113_10_factorization_l1__ab2d__seed_2026071301"
)
TASK_MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"


def _load_task(task_id: str) -> dict:
    for line in TASK_MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("task_id") == task_id:
            return row
    raise KeyError(task_id)


def test_promoted_rules_on_production_allowlist():
    assert KWARGS_APPROVED is True
    assert DUMPS_APPROVED is True
    assert KWARGS_ID in RULE_ALLOWLIST
    assert DUMPS_ID in RULE_ALLOWLIST
    assert RECOMMENDED_CHAIN_MAX_PASSES == len(RULE_ALLOWLIST) == 3


def test_113_10_production_chain_rescue_to_pass():
    art = json.loads((CELL / "artifact.json").read_text(encoding="utf-8"))
    source = (CELL / "extracted_candidate.py").read_text(encoding="utf-8").replace(
        "\r\n", "\n"
    )
    frozen = dict(art["frozen_parameters"])
    task = _load_task(art["task_id"])

    before, _, _ = classify_response(source, {"oracle_payload": frozen}, task)
    assert before == "runtime_failure"

    result = MathHealerRunner(max_passes=RECOMMENDED_CHAIN_MAX_PASSES).run(
        source,
        context={"frozen": frozen, "task": task},
    )
    assert result.real_model_calls == 0
    assert result.final_status == "changed"
    assert result.rolled_back is False
    assert result.consumer_may_use_output is True

    changed = [p for p in result.provenance if p.changed]
    assert len(changed) == 2
    assert [p.selected_rule_id for p in changed] == [KWARGS_ID, DUMPS_ID]
    assert [p.chain_position for p in changed] == [1, 2]

    after, _, details = classify_response(
        result.output_source, {"oracle_payload": frozen}, task
    )
    assert after == "passed"
    gates = details["evaluation_gates"]
    assert gates["g2_executability"]["status"] == "PASS"
    assert gates["g4_semantic_correctness"]["status"] == "PASS"

    # Provenance serialization includes chain_position
    assert all("chain_position" in provenance_to_dict(p) for p in result.provenance)


def test_default_max_passes_fail_closed_when_second_layer_remains():
    """DEFAULT_MAX_PASSES=1 must not silently drop remaining chain layers."""
    art = json.loads((CELL / "artifact.json").read_text(encoding="utf-8"))
    source = (CELL / "extracted_candidate.py").read_text(encoding="utf-8").replace(
        "\r\n", "\n"
    )
    frozen = dict(art["frozen_parameters"])
    task = _load_task(art["task_id"])
    result = run_research_healer(
        source,
        context={"frozen": frozen, "task": task},
        max_passes=1,
    )
    assert result.final_status == "max_passes_exceeded"
    assert result.rolled_back is True
    assert result.consumer_may_use_output is False
    assert result.output_source == source
