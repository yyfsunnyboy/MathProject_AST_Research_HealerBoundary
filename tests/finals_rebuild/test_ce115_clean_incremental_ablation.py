"""Clean incremental ablation: Ab1=BASE, Ab2g=BASE+GENERIC, Ab2d=BASE+GENERIC+DOMAIN."""
from __future__ import annotations

import json

import pytest

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    DOMAIN_BUDGET,
    FORBIDDEN_AB2G_DOMAIN_MARKERS,
    FORBIDDEN_BASELINE_MARKERS,
    GENERIC_BUDGET,
    LINEAGE_ID,
    TASK_DOMAIN_APIS,
    assert_clean_ablation_invariants,
    build_condition_prompt,
    domain_section,
    extract_domain_section,
    extract_generic_section,
    generic_section,
    prompt_sha256,
    section_identity,
    strip_domain_section,
    strip_generic_section,
)
from agent_tools.finals_rebuild.math_boundary_pilot import (
    build_ab1_prompt,
    frozen_payloads,
    load_pilot_tasks,
)
from scripts import run_ce115_gemini_three_condition_pilot as gemini_pilot
from scripts import run_ce115_qwen_three_condition_pilot as qwen_pilot

TASK_IDS = (
    "ce115_calc_polynomial_division_l1",
    "ce115_calc_radical_simplification_l1",
    "ce115_calc_exact_rational_expression_l1",
)
SEED = 2026071301
MANIFEST = gemini_pilot.TASK_MANIFEST


def _tasks_and_frozen():
    loaded = {t["task_id"]: t for t in load_pilot_tasks(MANIFEST)}
    tasks = {tid: loaded[tid] for tid in TASK_IDS}
    frozen = {row["task_id"]: row for row in frozen_payloads(tasks.values(), (SEED,))}
    return tasks, frozen


def test_generic_is_shared_constant_within_budget():
    g = generic_section()
    assert GENERIC_BUDGET[0] <= len(g) <= GENERIC_BUDGET[1]
    assert "PolynomialOps" not in g
    assert "FractionOps" not in g
    assert "RadicalOps" not in g
    assert "sqrt" not in g.lower()
    assert "division" not in g.lower()


def test_domain_sections_task_local_and_within_budget():
    for tid, apis in TASK_DOMAIN_APIS.items():
        section = domain_section(tid)
        assert DOMAIN_BUDGET[0] <= len(section) <= DOMAIN_BUDGET[1]
        assert "Ab1 answer-contract wording" not in section
        assert "Available Domain APIs" not in section
        assert "CE115 Ab2d-Assembly" not in section
        for api in apis:
            assert api["name"] in section
            assert api["import"] in section
            assert api["signature"] in section
        # Unrelated families must not appear
        allowed = {a["name"].split(".")[0] for a in apis}
        for family in ("PolynomialOps", "FractionOps", "RadicalOps", "RadicalLogicEngine"):
            if family not in allowed:
                assert family not in section


def test_composition_prefix_and_remove_section_equality():
    tasks, frozen = _tasks_and_frozen()
    generics = set()
    for tid in TASK_IDS:
        prompts = assert_clean_ablation_invariants(tasks[tid], frozen[tid])
        ab1, ab2g, ab2d = prompts["ab1"], prompts["ab2g"], prompts["ab2d"]
        assert ab1 == build_ab1_prompt(tasks[tid], frozen[tid])
        assert strip_generic_section(ab2g) == ab1
        assert strip_domain_section(ab2d) == ab2g
        assert extract_generic_section(ab2g) == extract_generic_section(ab2d)
        generics.add(extract_generic_section(ab2g))
        assert ab2d == ab2g + "\n\n" + extract_domain_section(ab2d)
        # No duplicated frozen / schema dumps in DOMAIN
        frozen_json = json.dumps(frozen[tid]["oracle_payload"], sort_keys=True)
        domain = extract_domain_section(ab2d)
        assert frozen_json not in domain
        assert "Required return schema" not in domain
        assert "## Task contract" not in domain
    assert len(generics) == 1


def test_ab1_has_no_generic_domain_or_algorithm_hints():
    tasks, frozen = _tasks_and_frozen()
    for tid in TASK_IDS:
        ab1 = build_condition_prompt("ab1", tasks[tid], frozen[tid])
        for marker in FORBIDDEN_BASELINE_MARKERS:
            assert marker not in ab1
        assert "step-by-step" not in ab1.lower()
        assert "algorithm" not in ab1.lower()
        assert "example answer" not in ab1.lower()


def test_ab2g_has_no_domain_clues():
    tasks, frozen = _tasks_and_frozen()
    for tid in TASK_IDS:
        ab2g = build_condition_prompt("ab2g", tasks[tid], frozen[tid])
        for marker in FORBIDDEN_AB2G_DOMAIN_MARKERS:
            assert marker not in ab2g


def test_ab2d_not_full_toolbox():
    tasks, frozen = _tasks_and_frozen()
    for tid in TASK_IDS:
        ab2d = build_condition_prompt("ab2d", tasks[tid], frozen[tid])
        # Full legacy toolbox lists many APIs; clean DOMAIN must not.
        assert ab2d.count("PolynomialOps.") + ab2d.count("FractionOps.") + ab2d.count("RadicalOps.") <= 3
        assert "RadicalLogicEngine" not in ab2d
        assert "format_latex" not in ab2d
        assert "format_plain" not in ab2d
        assert "format_expression" not in ab2d
        assert "to_latex" not in ab2d


def test_prompt_hashes_deterministic_and_shared_across_runners(tmp_path):
    tasks, frozen = _tasks_and_frozen()
    for tid in TASK_IDS:
        for cond in ("ab1", "ab2g", "ab2d"):
            a = build_condition_prompt(cond, tasks[tid], frozen[tid])
            b = build_condition_prompt(cond, tasks[tid], frozen[tid])
            assert a == b
            assert prompt_sha256(a) == prompt_sha256(b)

    g_plan = gemini_pilot.build_plan(tmp_path / "g")
    q_plan = qwen_pilot.build_plan(tmp_path / "q")
    g_hashes = {(c["task_id"], c["condition"]): c["prompt_hash"] for c in g_plan["cells"]}
    q_hashes = {(c["task_id"], c["condition"]): c["prompt_hash"] for c in q_plan["cells"]}
    assert g_hashes == q_hashes
    assert g_plan["prompt_lineage"] == q_plan["prompt_lineage"] == LINEAGE_ID


def test_gemini_and_qwen_preflight_zero_model_and_clean_markers(tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    g = gemini_pilot.preflight(tmp_path / "g_new", require_api_key=False)
    assert g["checks"]["real_model_calls"] == 0
    assert g["checks"]["clean_incremental_ab2d"] is True
    assert g["checks"]["clean_incremental_ab2g"] is True
    assert g["checks"]["ab1_uncontaminated"] is True
    assert g["checks"]["passed"] is True

    q = qwen_pilot.preflight(tmp_path / "q_new", require_ollama=False)
    assert q["checks"]["real_model_calls"] == 0
    assert q["checks"]["clean_incremental_ab2d"] is True
    assert q["checks"]["passed"] is True

    # Same prompt hashes across runners
    assert {
        (c["task_id"], c["condition"], c["prompt_hash"]) for c in g["plan"]["cells"]
    } == {
        (c["task_id"], c["condition"], c["prompt_hash"]) for c in q["plan"]["cells"]
    }


def test_section_identity_budget_report():
    tasks, frozen = _tasks_and_frozen()
    for tid in TASK_IDS:
        for cond in ("ab1", "ab2g", "ab2d"):
            prompt = build_condition_prompt(cond, tasks[tid], frozen[tid])
            info = section_identity(prompt, cond)
            assert info["lineage"] == LINEAGE_ID
            if cond == "ab2g":
                assert GENERIC_BUDGET[0] <= info["generic_chars"] <= GENERIC_BUDGET[1]
            if cond == "ab2d":
                assert DOMAIN_BUDGET[0] <= info["domain_chars"] <= DOMAIN_BUDGET[1]


def test_three_conditions_share_base_frozen_and_schema_text():
    tasks, frozen = _tasks_and_frozen()
    for tid in TASK_IDS:
        ab1 = build_condition_prompt("ab1", tasks[tid], frozen[tid])
        ab2g = build_condition_prompt("ab2g", tasks[tid], frozen[tid])
        ab2d = build_condition_prompt("ab2d", tasks[tid], frozen[tid])
        assert ab2g[: len(ab1)] == ab1
        assert ab2d[: len(ab2g)] == ab2g
        # Frozen line identical across conditions (from shared BASE)
        frozen_line = [ln for ln in ab1.splitlines() if ln.startswith("Frozen sampled parameters:")][0]
        assert frozen_line in ab2g and frozen_line in ab2d
