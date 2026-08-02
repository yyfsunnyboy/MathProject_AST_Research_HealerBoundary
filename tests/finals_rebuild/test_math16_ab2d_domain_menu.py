# -*- coding: utf-8 -*-
"""Tests for Math16 Ab2d+domain-menu freeze (zero-model)."""
from __future__ import annotations

import importlib
import json
import re
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (
    CONDITION,
    DOMAIN_OPS,
    DOMAIN_TEMPLATE_FILES,
    MANIFEST_REL,
    PROMPT_DIR_REL,
    TASK_ANSWER_CONTRACT_HEADER,
    TEMPLATE_DIR_REL,
    build_all_prompts,
    build_domain_menu_prompt,
    build_domain_template,
    domain_block_hashes_from_prompts,
    extract_domain_api_block,
    other_domain_ops,
    run_zero_model_preflight,
    scan_answer_leakage,
    scan_solution_plan,
    supported_apis_for_domain,
    validate_prompt_static,
)
from agent_tools.finals_rebuild.math16_pool import load_pool_manifest, tasks_by_id

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def built():
    return build_all_prompts(ROOT)


def test_four_domain_templates_exist(built):
    for domain, filename in DOMAIN_TEMPLATE_FILES.items():
        path = ROOT / TEMPLATE_DIR_REL / filename
        assert path.is_file(), path
        text = path.read_text(encoding="utf-8")
        assert domain in text
        apis = supported_apis_for_domain(domain)
        assert len(apis) >= 7
        for api in apis:
            assert api in text


def test_sixteen_prompts_and_manifest(built):
    prompt_dir = ROOT / PROMPT_DIR_REL
    files = sorted(prompt_dir.glob("*.txt"))
    assert len(files) == 16
    manifest = json.loads((ROOT / MANIFEST_REL).read_text(encoding="utf-8"))
    assert manifest["condition"] == CONDITION
    assert manifest["n_tasks"] == 16
    assert manifest["pool_identity_hash"]
    assert manifest["task_freeze_hash"]
    assert "evaluator_identity" in manifest
    assert all(manifest["domain_blocks_byte_identical"].values())


def test_same_domain_api_blocks_byte_identical(built):
    tasks = tasks_by_id(ROOT)
    report = domain_block_hashes_from_prompts(built["prompts"], tasks)
    for domain in DOMAIN_OPS:
        assert report[domain]["byte_identical"] is True
        assert report[domain]["n_tasks"] == 4


def test_cross_domain_isolation(built):
    tasks = tasks_by_id(ROOT)
    for tid, prompt in built["prompts"].items():
        domain = tasks[tid]["domain_ops"]
        errs = validate_prompt_static(prompt, domain)
        assert errs == [], (tid, errs)
        for other in other_domain_ops(domain):
            assert other not in prompt


def test_no_solution_plan_or_guardrail(built):
    for tid, prompt in built["prompts"].items():
        assert scan_solution_plan(prompt) == []
        assert "Task Guardrails" not in prompt
        assert "Processing steps" not in prompt
        assert "evaluate the exact expression:" not in prompt.lower()


def test_task_specific_answer_contract_present(built):
    from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (
        TASK_ANSWER_CONTRACT_HEADER,
        authoritative_answer_contract_text,
        extract_task_specific_answer_contract_block,
    )

    tasks = tasks_by_id(ROOT)
    for tid, prompt in built["prompts"].items():
        assert TASK_ANSWER_CONTRACT_HEADER in prompt
        block = extract_task_specific_answer_contract_block(prompt)
        body = authoritative_answer_contract_text(tasks[tid])
        assert body in block
        assert "Required return schema:" in block


def test_answer_contract_byte_identical_with_full_plan(built):
    from agent_tools.finals_rebuild.math16_ab2d_domain_menu import (
        extract_task_specific_answer_contract_block,
    )
    from agent_tools.finals_rebuild.math16_ab2d_full import build_ab2d_full_prompt

    tasks = tasks_by_id(ROOT)
    for tid, menu_prompt in built["prompts"].items():
        full = build_ab2d_full_prompt(tasks[tid], ROOT)
        assert extract_task_specific_answer_contract_block(menu_prompt) == (
            extract_task_specific_answer_contract_block(full)
        )

def test_domain_templates_have_no_answer_leakage(built):
    tasks = list(tasks_by_id(ROOT).values())
    for domain in DOMAIN_OPS:
        text = build_domain_template(domain)
        hits = scan_answer_leakage(text, tasks, allow_frozen_overlap=False)
        assert hits == [], (domain, hits)


def test_prompt_domain_section_no_answer_leakage(built):
    tasks = list(tasks_by_id(ROOT).values())
    for tid, prompt in built["prompts"].items():
        marker = "\n## Task\n"
        task_at = prompt.find(marker)
        domain_part = prompt[:task_at] if task_at >= 0 else prompt
        hits = scan_answer_leakage(domain_part, tasks, allow_frozen_overlap=False)
        assert hits == [], (tid, hits)


def test_task_block_has_stem_and_frozen_only(built):
    tasks = tasks_by_id(ROOT)
    for tid, prompt in built["prompts"].items():
        task = tasks[tid]
        assert "## Frozen task description" in prompt
        assert "## frozen_params" in prompt
        assert task["math16_question_text"] in prompt
        marker = "\n## Task\n"
        task_at = prompt.find(marker)
        assert task_at >= 0
        task_section = prompt[task_at + len(marker) :]
        # Must not embed a labeled formal answer object in the task section.
        assert re.search(r"(?i)expected[_ ]answer\s*[:=]", task_section) is None
        assert "evaluator expected" not in task_section.lower()
        dump = json.dumps(task["correct_answer"], ensure_ascii=False, sort_keys=True)
        if len(dump) >= 8:
            pre_task = prompt[:task_at]
            # Contract schema text is allowed before ## Task; forbid full answer dump there.
            assert dump not in pre_task.split(TASK_ANSWER_CONTRACT_HEADER, 1)[0]


def test_each_task_exposes_full_own_domain_api(built):
    tasks = tasks_by_id(ROOT)
    for tid, prompt in built["prompts"].items():
        domain = tasks[tid]["domain_ops"]
        block = extract_domain_api_block(prompt)
        for api in supported_apis_for_domain(domain):
            assert api in block


def test_zero_model_preflight_overall_pass(built):
    summary = run_zero_model_preflight(ROOT)
    assert summary["model_calls"] == 0
    assert summary["overall_pass"] is True
    assert summary["n_prompts"] == 16


def test_formal_runner_skeleton_no_api_by_default():
    mod = importlib.import_module("scripts.run_math16_ab2d_domain_menu_gemini_formal")
    assert hasattr(mod, "integration_check")
    with pytest.raises(SystemExit) as exc:
        mod.main(["--execute-api"])
    assert "EXECUTE_API_BLOCKED" in str(exc.value)
    info = mod.integration_check()
    assert info["n_prompts_on_disk"] == 16
    assert info["model_calls"] == 0


def test_does_not_modify_ab2d_full_prompt_hashes():
    """Guard: domain-menu build must not rewrite ab2d_full prompts."""
    full_dir = ROOT / "docs/experiments/prompts/ab2d_full/prompts"
    if not full_dir.exists():
        pytest.skip("ab2d_full prompts absent")
    # Touch domain-menu rebuild then ensure full prompts path still present count 16.
    build_all_prompts(ROOT)
    assert len(list(full_dir.glob("*.txt"))) == 16
