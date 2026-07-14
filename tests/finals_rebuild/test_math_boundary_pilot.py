import json
import tempfile
from pathlib import Path

import pytest

from agent_tools.finals_rebuild.math_boundary_pilot import (
    CONDITIONS,
    CORRECTED_FAMILY_IDS,
    TASK_IDS,
    _execute_generate,
    build_ab1_prompt,
    build_ab2g_prompt,
    classify_response,
    frozen_payloads,
    load_pilot_tasks,
    main,
    run_pilot,
)

MANIFEST = Path(__file__).parent / "fixtures" / "math_generation_tasks_ce115_pilot.jsonl"
LEGACY_EXCLUDED = "ce115_cr01_training_sequence_threshold_l3"


def test_frozen_pilot_is_four_corrected_l1_tasks_by_three_repeats():
    tasks = load_pilot_tasks(MANIFEST)
    assert tuple(task["task_id"] for task in tasks) == TASK_IDS
    assert TASK_IDS == tuple(f"{family}_l1" for family in CORRECTED_FAMILY_IDS)
    assert len(frozen_payloads(tasks)) == 12


def test_formal_set_excludes_legacy_training_sequence_task():
    tasks = load_pilot_tasks(MANIFEST)
    ids = {task["task_id"] for task in tasks}
    assert ids == set(TASK_IDS)
    assert LEGACY_EXCLUDED not in ids
    assert all(task_id.startswith("ce115_calc_") and task_id.endswith("_l1") for task_id in ids)
    # Shared fixture still retains historical non-calc rows; formal loader must ignore them.
    all_ids = {
        json.loads(line)["task_id"]
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    assert any(not task_id.startswith("ce115_calc_") for task_id in all_ids)
    assert ids.isdisjoint({task_id for task_id in all_ids if not task_id.startswith("ce115_calc_")})


def test_load_pilot_tasks_fails_when_formal_task_missing(tmp_path):
    rows = [
        json.loads(line)
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip() and json.loads(line)["task_id"] != TASK_IDS[0]
    ]
    path = tmp_path / "missing.jsonl"
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing tasks"):
        load_pilot_tasks(path)


def test_load_pilot_tasks_fails_on_duplicate_task_id(tmp_path):
    line = next(
        line
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip() and json.loads(line)["task_id"] == TASK_IDS[0]
    )
    path = tmp_path / "dup.jsonl"
    path.write_text(line + "\n" + line + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate task_id"):
        load_pilot_tasks(path)


def test_extra_legacy_rows_do_not_enter_formal_set(tmp_path):
    formal = [
        json.loads(line)
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.strip() and json.loads(line)["task_id"] in TASK_IDS
    ]
    legacy = {
        "task_id": LEGACY_EXCLUDED,
        "domain": "legacy",
        "skill_id": "alternating_training_progression_threshold",
        "difficulty_level": 3,
        "oracle_type": "alternating_sequence_threshold",
        "parameter_ranges": {},
        "seed": 1,
        "required_entry_point": "generate",
        "required_output_keys": ["question_text", "correct_answer", "oracle_payload"],
    }
    path = tmp_path / "mixed.jsonl"
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in [*formal, legacy]) + "\n",
        encoding="utf-8",
    )
    tasks = load_pilot_tasks(path)
    assert tuple(task["task_id"] for task in tasks) == TASK_IDS
    assert LEGACY_EXCLUDED not in {task["task_id"] for task in tasks}


def test_classification_passes_and_detects_schema_failure():
    task = next(t for t in load_pilot_tasks(MANIFEST) if t["oracle_type"] == "polynomial_division_general")
    frozen = frozen_payloads((task,), (2026071301,))[0]
    payload = json.dumps(frozen["oracle_payload"], sort_keys=True)
    source = (
        "def generate(level=1, **kwargs):\n"
        " return {'question_text':'q',"
        "'correct_answer':{'quotient_coefficients':[1, 1],'remainder_coefficients':[0]},"
        f"'oracle_payload':{payload}}}\n"
    )
    assert classify_response(source, frozen, task)[0] in {"passed", "answer_incorrect"}
    assert classify_response("def generate(): pass", frozen, task)[0] == "schema_failure"


def test_polynomial_ab1_prompt_includes_frozen_payload():
    task = next(t for t in load_pilot_tasks(MANIFEST) if t["oracle_type"] == "polynomial_division_general")
    frozen = frozen_payloads((task,), (2026071301,))[0]
    prompt = build_ab1_prompt(task, frozen)
    assert task["task_id"] in prompt
    assert json.dumps(frozen["oracle_payload"], sort_keys=True) in prompt
    assert "question_text" in prompt and "correct_answer" in prompt and "oracle_payload" in prompt


def test_corrected_ab1_prompts_include_frozen_payload_for_each_family():
    for task in load_pilot_tasks(MANIFEST):
        frozen = frozen_payloads((task,), (2026071301,))[0]
        prompt = build_ab1_prompt(task, frozen)
        assert task["skill_id"] in prompt
        assert json.dumps(frozen["oracle_payload"], sort_keys=True) in prompt
        assert "def generate(level=1, **kwargs)" in prompt


def test_mock_run_writes_required_artifacts():
    tasks = load_pilot_tasks(MANIFEST)

    def client(url, payload, timeout):
        return {"message": {"content": "def generate(level=1, **kwargs):\n return {}"}, "prompt_eval_count": 1, "eval_count": 2}

    with tempfile.TemporaryDirectory(dir=Path.cwd()) as directory:
        summary = run_pilot(tasks, output_root=directory, run_id="pilot", repeat_seeds=(1, 2, 3), client=client)
        assert summary["total_cells"] == 24  # 4 tasks × 3 seeds × 2 models
        assert {path.name for path in (Path(directory) / "pilot").iterdir()} >= {
            "manifest.json", "frozen_payloads.jsonl", "cell_results.jsonl", "summary.json", "failure_examples.jsonl"
        }
        manifest = json.loads((Path(directory) / "pilot" / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["task_ids"] == list(TASK_IDS)


def test_ab2g_prompt_preserves_ab1_prompt_unchanged_as_a_prefix():
    task = load_pilot_tasks(MANIFEST)[0]
    frozen = frozen_payloads((task,), (2026071301,))[0]
    ab1_prompt = build_ab1_prompt(task, frozen)
    ab2g_prompt = build_ab2g_prompt(task, frozen)
    assert ab2g_prompt.startswith(ab1_prompt)
    assert json.dumps(frozen["oracle_payload"], sort_keys=True) in ab2g_prompt


def test_ab2g_prompt_adds_generic_scaffold_without_task_specific_hints():
    task = load_pilot_tasks(MANIFEST)[0]
    frozen = frozen_payloads((task,), (2026071301,))[0]
    ab2g_prompt = build_ab2g_prompt(task, frozen)
    assert "Generic Safety-and-Format Scaffold" in ab2g_prompt
    for forbidden in ("retry", "Healer", "expected_answer", "self-correct", "chain-of-thought"):
        assert forbidden.lower() not in ab2g_prompt.lower()


def test_cli_condition_defaults_to_ab1(monkeypatch):
    captured = {}

    def fake_run_pilot(tasks, **kwargs):
        captured.update(kwargs)
        return {}

    monkeypatch.setattr("agent_tools.finals_rebuild.math_boundary_pilot.run_pilot", fake_run_pilot)
    main(["--task-manifest", str(MANIFEST), "--output-root", "unused"])
    assert captured["condition"] == "ab1"


def test_run_pilot_condition_ab2g_selects_build_ab2g_prompt():
    tasks = load_pilot_tasks(MANIFEST)

    def client(url, payload, timeout):
        return {"message": {"content": "def generate(level=1, **kwargs):\n return {}"}, "prompt_eval_count": 1, "eval_count": 2}

    with tempfile.TemporaryDirectory(dir=Path.cwd()) as directory:
        run_pilot(tasks, output_root=directory, run_id="pilot_ab2g", repeat_seeds=(1,), client=client, condition="ab2g")
        rows = [
            json.loads(line)
            for line in (Path(directory) / "pilot_ab2g" / "cell_results.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        assert all("Generic Safety-and-Format Scaffold" in row["prompt_text"] for row in rows)
        assert all(row["treatment"] == "Ab2g" for row in rows)
        manifest = json.loads((Path(directory) / "pilot_ab2g" / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["condition"] == "ab2g"
        assert manifest["treatment"] == "Ab2g"
        assert manifest["task_ids"] == list(TASK_IDS)


def test_condition_registry_maps_ab1_and_ab2g_builders():
    assert CONDITIONS["ab1"][1] is build_ab1_prompt
    assert CONDITIONS["ab2g"][1] is build_ab2g_prompt


def test_unicode_source_and_question_text_use_utf8_subprocess_io():
    source = "def generate(level=1, **kwargs):\n return {'question_text': '\\u6c42 \\u00b2 \\u7684\\u503c', 'correct_answer': 1, 'oracle_payload': {}}\n"
    status, value, error = _execute_generate(source)
    assert status == "passed", error
    assert error is None and value["question_text"] == chr(0x6C42) + " " + chr(0x00B2) + " " + chr(0x7684) + chr(0x503C)


def test_ab2d_polynomial_candidate_receives_documented_domain_api():
    source = "def generate(level=1, **kwargs):\n q, r = PolynomialOps.div_qr([4, -3, -5], [1, 2])\n return {'question_text':'q','correct_answer':{},'oracle_payload':{}}\n"
    status, value, error = _execute_generate(source, skill_id="polynomial_division_general")
    assert status == "passed", error
    assert value["question_text"] == "q"
