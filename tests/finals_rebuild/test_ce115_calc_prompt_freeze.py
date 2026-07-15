"""Milestone 3A/3B — CE115 calc prompt conditions and run-manifest freeze tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.ab2d_local_prompt import MATH_CORE_SCAFFOLD
from agent_tools.finals_rebuild.ce115_calc_golden_generators import FORMAL_L1_TASK_IDS
from agent_tools.finals_rebuild.ce115_calc_prompt_freeze import (
    FORMAL_CONDITIONS,
    FROZEN_PROMPT_HASHES_PRE_QWEN35,
    assert_no_leakage,
    build_all_formal_prompts,
    build_run_manifest,
    prompt_sha256,
    render_calc_task_contract,
    strip_ab2d_primitive_section,
    write_run_manifest,
)
from agent_tools.finals_rebuild.ce115_calc_golden_generators import formal_l1_tasks
from agent_tools.finals_rebuild.math_task_sampler import sample_task_parameters

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "docs" / "experiments" / "manifests" / "ce115_calc_main_experiment_manifest.json"
GIT_COMMIT = "908033d348634b7f0ee65495d4da58820dff6c83"


@pytest.fixture(scope="module")
def prompts():
    return build_all_formal_prompts()


@pytest.fixture(scope="module")
def manifest():
    return build_run_manifest(git_commit=GIT_COMMIT)


def test_twelve_prompts_for_four_tasks_three_conditions(prompts):
    assert list(prompts) == list(FORMAL_L1_TASK_IDS)
    for task_id, conds in prompts.items():
        assert tuple(conds) == FORMAL_CONDITIONS
        assert len(conds) == 3


def test_formal_task_ids_exclude_legacy(prompts):
    assert "ce115_cr01_training_sequence_threshold_l3" not in prompts
    assert all(task_id.startswith("ce115_calc_") and task_id.endswith("_l1") for task_id in prompts)


def test_ab1_has_no_math_core_or_primitive(prompts):
    for task_id in FORMAL_L1_TASK_IDS:
        text = prompts[task_id]["ab1"]
        assert MATH_CORE_SCAFFOLD not in text
        assert "## Task-local domain primitive:" not in text
        assert "## Task contract" in text
        assert "## Frozen parameters" in text


def test_ab2g_has_math_core_without_primitive(prompts):
    for task_id in FORMAL_L1_TASK_IDS:
        text = prompts[task_id]["ab2g"]
        assert text.startswith(MATH_CORE_SCAFFOLD)
        assert "## Task-local domain primitive:" not in text
        assert "## Task contract" in text
        assert "## Frozen parameters" in text


def test_ab2d_has_math_core_and_correct_primitive(prompts):
    tasks = formal_l1_tasks()
    for task_id in FORMAL_L1_TASK_IDS:
        text = prompts[task_id]["ab2d"]
        skill = tasks[task_id]["skill_id"]
        assert text.startswith(MATH_CORE_SCAFFOLD)
        assert f"## Task-local domain primitive: {skill}" in text
        assert "## Task contract" in text
        assert "## Frozen parameters" in text


def test_shared_task_contract_and_frozen_byte_identical_across_conditions(prompts):
    tasks = formal_l1_tasks()
    for task_id in FORMAL_L1_TASK_IDS:
        contract = render_calc_task_contract(tasks[task_id]).strip()
        payload = sample_task_parameters(tasks[task_id], 2026071301)["oracle_payload"]
        frozen_json = json.dumps(payload, ensure_ascii=False, sort_keys=True)
        for condition in FORMAL_CONDITIONS:
            text = prompts[task_id][condition]
            assert contract in text
            assert frozen_json in text
            assert text.count("## Task contract") == 1
            assert text.count("## Frozen parameters") == 1


def test_ab2d_minus_primitive_equals_ab2g(prompts):
    for task_id in FORMAL_L1_TASK_IDS:
        assert strip_ab2d_primitive_section(prompts[task_id]["ab2d"]) == prompts[task_id]["ab2g"]


def test_no_answer_or_oracle_leakage(prompts):
    for task_id in FORMAL_L1_TASK_IDS:
        for condition in FORMAL_CONDITIONS:
            assert_no_leakage(prompts[task_id][condition])


def test_prompt_hashes_deterministic_and_model_agnostic(prompts):
    again = build_all_formal_prompts()
    for task_id in FORMAL_L1_TASK_IDS:
        for condition in FORMAL_CONDITIONS:
            a = prompt_sha256(prompts[task_id][condition])
            b = prompt_sha256(again[task_id][condition])
            assert a == b
            assert "qwen" not in prompts[task_id][condition].lower()
            assert "gemini" not in prompts[task_id][condition].lower()
            assert prompts[task_id][condition] == again[task_id][condition]


def test_single_character_change_alters_hash(prompts):
    text = prompts[FORMAL_L1_TASK_IDS[0]]["ab1"]
    assert prompt_sha256(text) != prompt_sha256(text + "x")


def test_ab1_without_math_core_markers_for_pilot_alignment():
    prompts = build_all_formal_prompts()
    marker = "Make one complete first attempt; do not self-retry."
    for task_id in FORMAL_L1_TASK_IDS:
        assert marker not in prompts[task_id]["ab1"]
        assert marker in prompts[task_id]["ab2g"]
        assert marker in prompts[task_id]["ab2d"]


def test_local_confirmatory_freeze_without_unresolved_local_fields(manifest):
    assert manifest["local_unresolved_fields"] == []
    assert manifest["local_confirmatory_frozen"] is True
    assert "not_explicitly_set" not in json.dumps(manifest["local_unresolved_fields"])


def test_not_explicitly_set_is_legal_not_unresolved(manifest):
    dumped = json.dumps(manifest, ensure_ascii=False)
    assert "not_explicitly_set" in dumped
    for path in manifest["unresolved_fields"]:
        assert "not_explicitly_set" not in path
    sampling = manifest["models"]["qwen35_4b"]["sampling"]
    assert sampling["top_p"] == "not_explicitly_set"
    assert sampling["top_k"] == "not_explicitly_set"
    assert sampling["presence_penalty"] == "not_explicitly_set"
    assert sampling["num_predict"] == "not_explicitly_set"
    assert "UNRESOLVED" not in (sampling["top_p"], sampling["top_k"], sampling["num_predict"])


def test_qwen35_cohort_metadata(manifest):
    m4 = manifest["models"]["qwen35_4b"]
    m9 = manifest["models"]["qwen35_9b"]
    assert m4["model_tag"] == "qwen3.5:4b"
    assert m9["model_tag"] == "qwen3.5:9b"
    assert m4["model_digest"] == "2a654d98e6fb"
    assert m9["model_digest"] == "6488c96fa5fa"
    assert m4["parameter_count_reported"] == "4.7B"
    assert m9["parameter_count_reported"] == "9.7B"
    assert m4["runtime_version"] == "0.32.0"
    assert m9["runtime_version"] == "0.32.0"
    assert m4["quantization"] == m9["quantization"] == "Q4_K_M"
    assert set(manifest["models"]) >= {"qwen35_4b", "qwen35_9b", "historical_cohort", "gemini"}
    hist = manifest["models"]["historical_cohort"]
    assert hist["qwen3_4b_instruct_2507_q4_k_m"]["included_in_new_confirmatory"] is False
    assert hist["qwen3_8b"]["included_in_new_confirmatory"] is False


def test_sampling_layers_separate_defaults_from_request(manifest):
    for key in ("qwen35_4b", "qwen35_9b"):
        sampling = manifest["models"][key]["sampling"]
        assert sampling["request_explicit_settings"]["temperature"] == 0.0
        assert sampling["request_explicit_settings"]["think"] is False
        assert sampling["request_not_explicitly_set"]["top_p"] == "not_explicitly_set"
        assert sampling["observed_model_defaults"]["temperature"] == 1
        assert sampling["observed_model_defaults"]["top_p"] == 0.95
        assert sampling["effective_temperature_source"] == "request_override"


def test_local_cell_count_is_72_and_separated_from_gemini(manifest):
    assert manifest["cell_counts"]["confirmatory_local_cell_count"] == 72
    assert manifest["cell_geometry"]["confirmatory_local_cell_count"] == 72
    assert manifest["cell_geometry"]["expected_primary_local_cells"] == 72
    assert manifest["cell_counts"]["exploratory_cloud_cell_count"] == "UNRESOLVED"
    assert manifest["cell_counts"]["total_planned_cell_count"] == "UNRESOLVED"
    assert manifest["cell_geometry"]["gemini_cells"] == "UNRESOLVED"
    assert manifest["cell_counts"]["confirmatory_local_cell_count"] != manifest["cell_counts"]["exploratory_cloud_cell_count"]


def test_unresolved_gemini_does_not_block_local_freeze(manifest):
    assert any(p.startswith("models.gemini.") for p in manifest["unresolved_fields"])
    assert manifest["local_confirmatory_frozen"] is True
    assert manifest["gemini_exploratory_frozen"] is False
    assert manifest["frozen"] is False
    assert manifest["freeze_verdict"] == "LOCAL CONFIRMATORY FROZEN"


def test_manifest_evidence_paths_exist(manifest):
    assert manifest["evidence_paths"]
    for rel in manifest["evidence_paths"]:
        path = ROOT / rel
        assert path.is_file(), f"missing evidence path: {rel}"


def test_4b_9b_request_settings_schema_identical(manifest):
    s4 = manifest["models"]["qwen35_4b"]["sampling"]
    s9 = manifest["models"]["qwen35_9b"]["sampling"]
    assert set(s4) == set(s9)
    for key in ("temperature", "top_p", "top_k", "presence_penalty", "num_predict", "seed_binding", "api", "think"):
        assert s4[key] == s9[key]
    assert s4["temperature"] == 0.0
    assert s4["think"] is False
    assert s4["seed_binding"] == "per_cell_repeat_seed"


def test_thinking_policy_explicit_think_false(manifest):
    for key in ("qwen35_4b", "qwen35_9b"):
        thinking = manifest["models"][key]["thinking"]
        assert thinking["thinking_capability"] == "supported"
        assert thinking["thinking_requested"] is False
        assert thinking["requested"] is False
        assert thinking["thinking_policy"] == "explicit_think_false"
        assert thinking["qualification_result"] == "THINK_FALSE_CLEAN"
        assert thinking["qualification_scope"] == "external_nonformal_6_call_test"
        assert thinking["qualification_date"] == "2026-07-15"


def test_prompt_hashes_invariant_across_qwen35_cohort(manifest):
    assert manifest["per_task_prompt_hashes"] == FROZEN_PROMPT_HASHES_PRE_QWEN35


def test_no_model_or_api_calls_in_freeze_module():
    source = (ROOT / "agent_tools" / "finals_rebuild" / "ce115_calc_prompt_freeze.py").read_text(encoding="utf-8")
    # Module may document /api/chat as evidence string; forbid live call sites only.
    assert "urllib.request" not in source
    assert "GoogleAIClient(" not in source
    assert "generate_content(" not in source
    assert "requests.post" not in source
    assert "ollama.chat(" not in source
    assert "ollama.generate(" not in source
    assert "http://127.0.0.1:11434" not in source
    assert "generativelanguage.googleapis.com" not in source


def test_manifest_json_serializable_and_checked_in(manifest, tmp_path):
    dumped = json.dumps(manifest, ensure_ascii=False, sort_keys=True)
    restored = json.loads(dumped)
    assert restored["request_count"] == 1
    assert restored["retry_count"] == 0
    assert restored["healer_enabled"] is False
    assert restored["first_attempt_is_ITT"] is True
    assert restored["formal_task_ids"] == list(FORMAL_L1_TASK_IDS)
    assert restored["local_confirmatory_frozen"] is True
    assert restored["gemini_exploratory_frozen"] is False
    assert restored["frozen"] is False
    assert restored["freeze_verdict"] == "LOCAL CONFIRMATORY FROZEN"
    out = tmp_path / "manifest.json"
    write_run_manifest(out, git_commit=GIT_COMMIT)
    assert out.is_file()
    assert MANIFEST_PATH.is_file()
    checked = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert checked["git_commit"] == GIT_COMMIT
    assert checked["local_confirmatory_frozen"] is True
    assert checked["freeze_verdict"] == "LOCAL CONFIRMATORY FROZEN"
    assert checked["cell_counts"]["confirmatory_local_cell_count"] == 72
