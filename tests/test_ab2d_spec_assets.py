# -*- coding: utf-8 -*-
"""
Targeted tests for Pilot-02 Segment 1: Ab2d+spec Assets
"""
import os
import re
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = ROOT / "docs/experiments/templates/ab2d_spec"
GUARDRAILS_DIR = ROOT / "docs/experiments/prompts/ab2d_spec/task_guardrails/integer"

REF_PATH = TEMPLATES_DIR / "Example_Program_Research_Math16_Ab2d_Spec_Reference.py"
COMPACT_PATH = TEMPLATES_DIR / "integer_domain_scaffold_compact.py"

GUARDRAIL_FILES = [
    "ce111_q03_prime_factor_selection.md",
    "ce112_q01_negative_integer_power.md",
    "ce112_q09_divisor_multiple_intersection.md",
    "ce111_nonchoice_q01_part1_exponential_growth.md",
]

def test_reference_exists_and_marked_no_inject():
    assert REF_PATH.exists(), f"Reference file not found: {REF_PATH}"
    content = REF_PATH.read_text(encoding="utf-8")
    assert "Do not inject this file verbatim into model prompts." in content
    assert "Researcher-facing reference only." in content

def test_reference_contains_return_keys():
    content = REF_PATH.read_text(encoding="utf-8")
    # Verify the return dictionary structure contains the three contract keys
    assert "question_text" in content
    assert "correct_answer" in content
    assert "oracle_payload" in content

    # Check return dictionary format via regex
    match = re.search(r'return\s*\{\s*["\']question_text["\']\s*:\s*.*,\s*["\']correct_answer["\']\s*:\s*.*,\s*["\']oracle_payload["\']\s*:\s*.*\}', content, re.DOTALL)
    assert match is not None, "Reference generate() does not return a dict with the three expected keys in the standard contract layout"

def test_compact_has_only_one_generate_and_no_imports_or_banned_terms():
    assert COMPACT_PATH.exists(), f"Compact scaffold file not found: {COMPACT_PATH}"
    content = COMPACT_PATH.read_text(encoding="utf-8")

    # Strip comments to check actual code execution path
    content_no_comments = re.sub(r'#.*$', '', content, flags=re.MULTILINE)

    # 1. Only one generate() definition
    generate_defs = re.findall(r'def\s+generate\s*\(', content_no_comments)
    assert len(generate_defs) == 1, f"Expected exactly one generate() definition, found {len(generate_defs)}"

    # 2. No import statements
    assert "import " not in content_no_comments, "Compact scaffold must not contain import statements in code"

    # 3. No IntegerOps, eval, exec, safe_eval
    assert "IntegerOps" not in content_no_comments, "Compact scaffold must not reference IntegerOps in code"
    assert "eval" not in content_no_comments, "Compact scaffold must not contain eval in code"
    assert "exec" not in content_no_comments, "Compact scaffold must not contain exec in code"
    assert "safe_eval" not in content_no_comments, "Compact scaffold must not contain safe_eval in code"

def test_compact_contains_return_keys():
    content = COMPACT_PATH.read_text(encoding="utf-8")
    # Verify the return dictionary structure contains the three contract keys
    assert "question_text" in content
    assert "correct_answer" in content
    assert "oracle_payload" in content

    # Check return dictionary format
    match = re.search(r'return\s*\{\s*["\']question_text["\']\s*:\s*question_text,\s*["\']correct_answer["\']\s*:\s*correct_answer,\s*["\']oracle_payload["\']\s*:\s*oracle_payload,\s*\}', content, re.DOTALL)
    assert match is not None, "Compact scaffold generate() does not return a dict with the three expected keys in the standard contract layout"

def test_guardrails_exist():
    for f_name in GUARDRAIL_FILES:
        path = GUARDRAILS_DIR / f_name
        assert path.exists(), f"Guardrail file not found: {path}"

def test_task_3_guardrail_spec():
    path = GUARDRAILS_DIR / "ce112_q09_divisor_multiple_intersection.md"
    content = path.read_text(encoding="utf-8")

    # Must contain both conditions
    assert "x % multiple_of == 0" in content
    assert "divisor_of % x == 0" in content

    # Must not contain incorrect direction
    assert "x % divisor_of == 0" not in content

def test_task_4_guardrail_spec():
    path = GUARDRAILS_DIR / "ce111_nonchoice_q01_part1_exponential_growth.md"
    content = path.read_text(encoding="utf-8")

    # Must specify returning k instead of final population
    assert "Return k" in content or "return k" in content
    assert "final population" in content

def test_guardrails_do_not_contain_known_fixed_answers():
    # Verify no hardcoded final answers in the guardrails
    for f_name in GUARDRAIL_FILES:
        path = GUARDRAILS_DIR / f_name
        content = path.read_text(encoding="utf-8")
        # Ensure we do not see a line indicating "The answer is 123" or similar
        # Since answers are completely empty in the cards, this should hold.
        # We also check that specific answer values aren't leaked.
        assert not re.search(r'(?i)answer\s*is\s*\d+', content)
        assert not re.search(r'(?i)correct_answer\s*=\s*\d+', content)

def test_files_do_not_contain_complete_solvers():
    # Verify neither reference nor compact files contain complete solver logic for any of the 4 tasks
    for path in [REF_PATH, COMPACT_PATH]:
        content = path.read_text(encoding="utf-8")
        # Verify lack of loops or operations specific to the tasks
        assert "split_factor" not in content
        assert "divisor_of" not in content
        assert "multiple_of" not in content
        assert "primality" not in content
        assert "base ** exponent" not in content
