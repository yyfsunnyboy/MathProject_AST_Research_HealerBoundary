# -*- coding: utf-8 -*-
"""
Targeted tests for Pilot-02 Segment 1 & 2: Ab2d+spec Assets and Prompts
"""
import os
import re
import json
import hashlib
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "docs/experiments/templates/ab2d_spec"
GUARDRAILS_DIR = ROOT / "docs/experiments/prompts/ab2d_spec/task_guardrails/integer"
PROMPTS_DIR = ROOT / "docs/experiments/prompts/ab2d_spec/prompts"
MANIFEST_PATH = ROOT / "docs/experiments/prompts/ab2d_spec/manifest.json"

REF_PATH = TEMPLATES_DIR / "Example_Program_Research_Math16_Ab2d_Spec_Reference.py"
COMPACT_PATH = TEMPLATES_DIR / "integer_domain_scaffold_compact.py"

GUARDRAIL_FILES = [
    "ce111_q03_prime_factor_selection.md",
    "ce112_q01_negative_integer_power.md",
    "ce112_q09_divisor_multiple_intersection.md",
    "ce111_nonchoice_q01_part1_exponential_growth.md",
]

TARGET_TASKS = [
    "ce111_q03_prime_factor_selection",
    "ce112_q01_negative_integer_power",
    "ce112_q09_divisor_multiple_intersection",
    "ce111_nonchoice_q01_part1_exponential_growth"
]

# SEGMENT 1 TESTS
def test_reference_exists_and_marked_no_inject():
    assert REF_PATH.exists()
    content = REF_PATH.read_text(encoding="utf-8")
    assert "Do not inject this file verbatim into model prompts." in content
    assert "Researcher-facing reference only." in content

def test_reference_contains_return_keys():
    content = REF_PATH.read_text(encoding="utf-8")
    assert "question_text" in content
    assert "correct_answer" in content
    assert "oracle_payload" in content
    match = re.search(r'return\s*\{\s*["\']question_text["\']\s*:\s*.*,\s*["\']correct_answer["\']\s*:\s*.*,\s*["\']oracle_payload["\']\s*:\s*.*\}', content, re.DOTALL)
    assert match is not None

def test_compact_has_only_one_generate_and_no_imports_or_banned_terms():
    assert COMPACT_PATH.exists()
    content = COMPACT_PATH.read_text(encoding="utf-8")
    content_no_comments = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
    generate_defs = re.findall(r'def\s+generate\s*\(', content_no_comments)
    assert len(generate_defs) == 1
    assert "import " not in content_no_comments
    assert "IntegerOps" not in content_no_comments
    assert "eval" not in content_no_comments
    assert "exec" not in content_no_comments
    assert "safe_eval" not in content_no_comments

def test_compact_contains_return_keys():
    content = COMPACT_PATH.read_text(encoding="utf-8")
    assert "question_text" in content
    assert "correct_answer" in content
    assert "oracle_payload" in content
    match = re.search(r'return\s*\{\s*["\']question_text["\']\s*:\s*question_text,\s*["\']correct_answer["\']\s*:\s*correct_answer,\s*["\']oracle_payload["\']\s*:\s*oracle_payload,\s*\}', content, re.DOTALL)
    assert match is not None

def test_guardrails_exist():
    for f_name in GUARDRAIL_FILES:
        path = GUARDRAILS_DIR / f_name
        assert path.exists()

def test_task_3_guardrail_spec():
    path = GUARDRAILS_DIR / "ce112_q09_divisor_multiple_intersection.md"
    content = path.read_text(encoding="utf-8")
    assert "x % multiple_of == 0" in content
    assert "divisor_of % x == 0" in content
    assert "x % divisor_of == 0" not in content

def test_task_4_guardrail_spec():
    path = GUARDRAILS_DIR / "ce111_nonchoice_q01_part1_exponential_growth.md"
    content = path.read_text(encoding="utf-8")
    assert "Return k" in content or "return k" in content
    assert "final population" in content

def test_guardrails_do_not_contain_known_fixed_answers():
    for f_name in GUARDRAIL_FILES:
        path = GUARDRAILS_DIR / f_name
        content = path.read_text(encoding="utf-8")
        assert not re.search(r'(?i)answer\s*is\s*\d+', content)
        assert not re.search(r'(?i)correct_answer\s*=\s*\d+', content)

def test_files_do_not_contain_complete_solvers():
    for path in [REF_PATH, COMPACT_PATH]:
        content = path.read_text(encoding="utf-8")
        assert "split_factor" not in content
        assert "divisor_of" not in content
        assert "multiple_of" not in content
        assert "primality" not in content
        assert "base ** exponent" not in content

# SEGMENT 2 TESTS
def test_exactly_four_prompts_generated():
    assert PROMPTS_DIR.exists()
    txt_files = list(PROMPTS_DIR.glob("*.txt"))
    assert len(txt_files) == 4
    filenames = {f.stem for f in txt_files}
    assert filenames == set(TARGET_TASKS)

def test_prompts_contain_correct_task_id_and_frozen_contract():
    for tid in TARGET_TASKS:
        prompt_path = PROMPTS_DIR / f"{tid}.txt"
        content = prompt_path.read_text(encoding="utf-8")
        assert tid in content
        assert "generate() must return a dict with exactly question_text, correct_answer, and oracle_payload." in content

def test_prompts_contain_ab2g_prefix():
    for tid in TARGET_TASKS:
        prompt_path = PROMPTS_DIR / f"{tid}.txt"
        content = prompt_path.read_text(encoding="utf-8")
        assert "## Clean-incremental GENERIC" in content
        assert "Preserve frozen parameters exactly." in content

def test_prompts_contain_compact_scaffold():
    scaffold_content = COMPACT_PATH.read_text(encoding="utf-8").strip()
    for tid in TARGET_TASKS:
        prompt_path = PROMPTS_DIR / f"{tid}.txt"
        content = prompt_path.read_text(encoding="utf-8")
        assert "## Compact Domain Scaffold" in content
        assert scaffold_content in content

def test_prompts_contain_isolated_guardrails():
    for tid in TARGET_TASKS:
        prompt_path = PROMPTS_DIR / f"{tid}.txt"
        content = prompt_path.read_text(encoding="utf-8")

        # Read the matching guardrail content
        guardrail_path = GUARDRAILS_DIR / f"{tid}.md"
        guardrail_content = guardrail_path.read_text(encoding="utf-8").strip()

        assert "## Task Guardrails" in content
        assert guardrail_content in content

        # Ensure other guardrails are not present
        for other_tid in TARGET_TASKS:
            if other_tid == tid:
                continue
            other_guardrail_path = GUARDRAILS_DIR / f"{other_tid}.md"
            other_guardrail_content = other_guardrail_path.read_text(encoding="utf-8").strip()
            assert other_guardrail_content not in content

def test_prompts_do_not_contain_reference_markers():
    for tid in TARGET_TASKS:
        prompt_path = PROMPTS_DIR / f"{tid}.txt"
        content = prompt_path.read_text(encoding="utf-8")
        assert "Do not inject this file verbatim into model prompts." not in content
        assert "Example Program Research" not in content

def test_prompts_do_not_contain_legacy_api_exposure():
    for tid in TARGET_TASKS:
        prompt_path = PROMPTS_DIR / f"{tid}.txt"
        content = prompt_path.read_text(encoding="utf-8")
        assert "## Clean-incremental DOMAIN" not in content
        assert "IntegerOps.is_divisible" not in content

def test_prompts_do_not_contain_integerops_calls_except_final_check():
    for tid in TARGET_TASKS:
        prompt_path = PROMPTS_DIR / f"{tid}.txt"
        content = prompt_path.read_text(encoding="utf-8")
        final_check_marker = "- Do not use IntegerOps or invented APIs."
        content_no_final_check = content.replace(final_check_marker, "")

        scaffold_comment = "# - Do not import, reference, or call IntegerOps."
        content_no_scaffold_comment = content_no_final_check.replace(scaffold_comment, "")

        assert "IntegerOps" not in content_no_scaffold_comment

def test_prompts_do_not_contain_eval_exec_calls():
    for tid in TARGET_TASKS:
        prompt_path = PROMPTS_DIR / f"{tid}.txt"
        content = prompt_path.read_text(encoding="utf-8")

        lines = content.splitlines()
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.startswith("#") or line_stripped.startswith("-"):
                continue
            assert "eval(" not in line_stripped
            assert "exec(" not in line_stripped
            assert "safe_eval" not in line_stripped

def test_task_3_prompt_整除方向():
    prompt_path = PROMPTS_DIR / "ce112_q09_divisor_multiple_intersection.txt"
    content = prompt_path.read_text(encoding="utf-8")
    assert "x % multiple_of == 0" in content
    assert "divisor_of % x == 0" in content
    assert "x % divisor_of == 0" not in content

def test_task_4_prompt_exponent_is_k():
    prompt_path = PROMPTS_DIR / "ce111_nonchoice_q01_part1_exponential_growth.txt"
    content = prompt_path.read_text(encoding="utf-8")
    assert "Return k" in content or "return k" in content
    assert "final population" in content

def test_prompts_do_not_contain_known_answers():
    for tid in TARGET_TASKS:
        prompt_path = PROMPTS_DIR / f"{tid}.txt"
        content = prompt_path.read_text(encoding="utf-8")
        assert "correct_answer = 13" not in content
        assert "correct_answer = -27" not in content
        assert "correct_answer = 6" not in content
        assert "correct_answer = 18" not in content
        assert "correct_answer = {\"count\": 6}" not in content
        assert "correct_answer = {\"k\": 18}" not in content

def test_manifest_matches_actual_files():
    assert MANIFEST_PATH.exists()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert manifest["manifest_id"] == "math16_ab2d_spec_pilot02_freeze_v1"

    tasks = manifest["tasks"]
    assert len(tasks) == 4

    for t in tasks:
        tid = t["task_id"]
        prompt_path = PROMPTS_DIR / f"{tid}.txt"
        assert prompt_path.exists()
        content = prompt_path.read_text(encoding="utf-8")

        prompt_sha = hashlib.sha256(content.encode("utf-8")).hexdigest()
        assert t["exact_prompt_sha256"] == prompt_sha
        assert t["character_count"] == len(content)
        assert t["utf8_byte_count"] == len(content.encode("utf-8"))

        assert t["condition"] == "ab2d_spec"
        assert t["prompt_frozen"] is True
        assert t["historical_error_informed"] is True
        assert t["pilot02_same_run_results_used"] is False
        assert t["model_called"] is False

def test_assembler_idempotence():
    manifest_before = MANIFEST_PATH.read_text(encoding="utf-8")
    prompts_before = {}
    for tid in TARGET_TASKS:
        prompts_before[tid] = (PROMPTS_DIR / f"{tid}.txt").read_text(encoding="utf-8")

    from scripts.build_math16_integer_ab2d_spec_prompts import main as run_assembler
    run_assembler()

    manifest_after = MANIFEST_PATH.read_text(encoding="utf-8")
    assert manifest_before == manifest_after
    for tid in TARGET_TASKS:
        prompt_after = (PROMPTS_DIR / f"{tid}.txt").read_text(encoding="utf-8")
        assert prompts_before[tid] == prompt_after
