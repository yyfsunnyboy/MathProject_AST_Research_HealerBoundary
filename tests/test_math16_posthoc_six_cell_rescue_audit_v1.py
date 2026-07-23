"""
tests/test_math16_posthoc_six_cell_rescue_audit_v1.py
=====================================================
Test suite for the Math16 Post-hoc Six-Cell Rescue Mechanism Audit v1.

Validates:
1. Taxonomy three-layer domain completeness
2. Spec contains all required fields
3. Expected rescue accounting: 5 / 6 / +1
4. Corrected-chain: 10 / 8 / 2 / 1
5. Builder contains no model calls
6. Builder does not execute Healer or Evaluator
7. Six cells locatable from frozen artifacts only
8. No self-invented cell IDs
9. Final Report and Evidence Complete SHA unchanged
10. No Stress Test execution
11. No official analysis result report produced
12. No Poster/PPT/Slides output from Builder
"""

import ast
import hashlib
import json
import re
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Repo root
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent.resolve()

# ---------------------------------------------------------------------------
# Frozen SHA constants (must match spec)
# ---------------------------------------------------------------------------
FROZEN_SHA_FINAL_REPORT_V13 = "dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b"
FROZEN_SHA_EVIDENCE_COMPLETE = "de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225"

FINAL_REPORT_V13_PATH = REPO_ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
EVIDENCE_COMPLETE_PATH = REPO_ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"

TAXONOMY_JSON_PATH = REPO_ROOT / "docs/experiments/manifests/math16_posthoc_shared_taxonomy_v1.json"
TAXONOMY_MD_PATH = REPO_ROOT / "docs/experiments/design/math16_posthoc_shared_taxonomy_v1.md"
AUDIT_SPEC_PATH = REPO_ROOT / "docs/experiments/design/math16_posthoc_six_cell_rescue_audit_v1_spec.md"
AUDIT_MANIFEST_PATH = REPO_ROOT / "docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_manifest.json"
BUILDER_SCRIPT_PATH = REPO_ROOT / "scripts/build_math16_posthoc_six_cell_rescue_audit_v1.py"
PREFLIGHT_SCRIPT_PATH = REPO_ROOT / "scripts/preflight_math16_posthoc_six_cell_rescue_audit_v1.py"

COMPARISON_PATH = REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json"
FREEZE_PATH = REPO_ROOT / "docs/experiments/audits/math16_pilot02_qwen4b_posthoc_corrected_chain_freeze_v1.json"
PRIMARY_ELIGIBLE_PATH = REPO_ROOT / "docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: Path) -> list:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_builder_source() -> str:
    with open(BUILDER_SCRIPT_PATH, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# 1. Taxonomy three-layer domain completeness
# ---------------------------------------------------------------------------

class TestTaxonomyDomain:
    @pytest.fixture(scope="class")
    def taxonomy(self):
        assert TAXONOMY_JSON_PATH.exists(), f"Taxonomy JSON not found: {TAXONOMY_JSON_PATH}"
        return load_json(TAXONOMY_JSON_PATH)

    def test_layer_a_has_exactly_5_codes(self, taxonomy):
        """Layer A must have exactly 5 failure layer codes."""
        values = taxonomy["layer_A_original_failure_layer"]["values"]
        codes = [v["code"] for v in values]
        assert len(codes) == 5, f"Expected 5 Layer A codes, got {len(codes)}: {codes}"

    def test_layer_a_required_codes(self, taxonomy):
        """Layer A must contain all 5 required codes."""
        expected = {
            "L1_PARSE_SYNTAX",
            "L2_CONTRACT_SCHEMA_ENTRYPOINT",
            "L3_DOMAIN_API",
            "L4_RUNTIME_EXECUTION",
            "L5_SEMANTIC_ANSWER",
        }
        values = taxonomy["layer_A_original_failure_layer"]["values"]
        actual = {v["code"] for v in values}
        assert actual == expected, f"Layer A codes mismatch. Expected: {expected}, Got: {actual}"

    def test_layer_b_has_exactly_7_codes(self, taxonomy):
        """Layer B must have exactly 7 disposition codes."""
        values = taxonomy["layer_B_healer_disposition_result"]["values"]
        codes = [v["code"] for v in values]
        assert len(codes) == 7, f"Expected 7 Layer B codes, got {len(codes)}: {codes}"

    def test_layer_b_required_codes(self, taxonomy):
        """Layer B must contain all 7 required codes."""
        expected = {
            "NO_OP", "ABSTAIN_NO_RULE", "ABSTAIN_AMBIGUOUS",
            "MODIFIED_RESCUED", "MODIFIED_STILL_FAIL",
            "MODIFIED_NEW_FAILURE", "MODIFIED_UNEVALUABLE",
        }
        values = taxonomy["layer_B_healer_disposition_result"]["values"]
        actual = {v["code"] for v in values}
        assert actual == expected, f"Layer B codes mismatch. Expected: {expected}, Got: {actual}"

    def test_layer_c_has_exactly_3_codes(self, taxonomy):
        """Layer C must have exactly 3 repair signature codes."""
        values = taxonomy["layer_C_repair_signature_match"]["values"]
        codes = [v["code"] for v in values]
        assert len(codes) == 3, f"Expected 3 Layer C codes, got {len(codes)}: {codes}"

    def test_layer_c_required_codes(self, taxonomy):
        """Layer C must contain all 3 required codes."""
        expected = {
            "WITHIN_FROZEN_REPAIR_SIGNATURE",
            "OUTSIDE_FROZEN_REPAIR_SIGNATURE",
            "AMBIGUOUS_SIGNATURE_MATCH",
        }
        values = taxonomy["layer_C_repair_signature_match"]["values"]
        actual = {v["code"] for v in values}
        assert actual == expected, f"Layer C codes mismatch. Expected: {expected}, Got: {actual}"

    def test_mutation_policy_is_immutable(self, taxonomy):
        """Taxonomy mutation policy must state IMMUTABLE."""
        policy = taxonomy.get("mutation_policy", "")
        assert "IMMUTABLE" in policy.upper(), f"Mutation policy must contain IMMUTABLE, got: {policy}"

    def test_valid_conditions_present(self, taxonomy):
        """Taxonomy must list all 4 valid conditions."""
        conditions = taxonomy.get("valid_conditions", {})
        required = {"Ab1", "Ab2g", "Ab2d+api", "Ab2d+spec"}
        assert set(conditions.keys()) == required, f"Valid conditions mismatch: {conditions.keys()}"

    def test_valid_families_present(self, taxonomy):
        """Taxonomy must list all 4 valid families."""
        families = taxonomy.get("valid_families", {})
        required = {"integer", "polynomial", "radical", "fraction"}
        assert set(families.keys()) == required, f"Valid families mismatch: {families.keys()}"


# ---------------------------------------------------------------------------
# 2. Spec contains all required fields
# ---------------------------------------------------------------------------

class TestSpecRequiredFields:
    @pytest.fixture(scope="class")
    def spec_content(self):
        assert AUDIT_SPEC_PATH.exists(), f"Spec not found: {AUDIT_SPEC_PATH}"
        with open(AUDIT_SPEC_PATH, encoding="utf-8") as f:
            return f.read()

    def test_spec_has_cell_id_field(self, spec_content):
        assert "cell_id" in spec_content

    def test_spec_has_model_field(self, spec_content):
        assert "model" in spec_content

    def test_spec_has_task_id_field(self, spec_content):
        assert "task_id" in spec_content

    def test_spec_has_family_field(self, spec_content):
        assert "family" in spec_content

    def test_spec_has_condition_field(self, spec_content):
        assert "condition" in spec_content

    def test_spec_has_seed_field(self, spec_content):
        assert "seed" in spec_content

    def test_spec_has_baseline_failure_layer(self, spec_content):
        assert "baseline_failure_layer" in spec_content

    def test_spec_has_healer_rule_id(self, spec_content):
        assert "healer_rule_id" in spec_content

    def test_spec_has_before_snippet_hash(self, spec_content):
        assert "before_snippet_hash" in spec_content

    def test_spec_has_after_snippet_hash(self, spec_content):
        assert "after_snippet_hash" in spec_content

    def test_spec_has_oracle_answer_used(self, spec_content):
        assert "oracle_answer_used" in spec_content

    def test_spec_has_repair_signature_match(self, spec_content):
        assert "repair_signature_match" in spec_content

    def test_spec_has_changed_line_count(self, spec_content):
        assert "changed_line_count" in spec_content

    def test_spec_has_changed_ast_node_count(self, spec_content):
        assert "changed_ast_node_count" in spec_content

    def test_spec_has_unique_field(self, spec_content):
        assert "unique" in spec_content

    def test_spec_has_local_field(self, spec_content):
        assert "local" in spec_content

    def test_spec_has_offline_verifiable_field(self, spec_content):
        assert "offline_verifiable" in spec_content

    def test_spec_has_analyst_notes(self, spec_content):
        assert "analyst_notes" in spec_content

    def test_spec_has_post_hoc_supplementary_type(self, spec_content):
        assert "POST_HOC_SUPPLEMENTARY" in spec_content

    def test_spec_has_no_model_calls_guarantee(self, spec_content):
        assert "no_model_calls" in spec_content.lower() or "no model call" in spec_content.lower()

    def test_spec_has_no_healer_execution_guarantee(self, spec_content):
        assert "no_healer_execution" in spec_content.lower() or "no healer execution" in spec_content.lower()


# ---------------------------------------------------------------------------
# 3. Expected rescue accounting: 5 / 6 / +1
# ---------------------------------------------------------------------------

class TestRescueAccounting:
    @pytest.fixture(scope="class")
    def comparison(self):
        assert COMPARISON_PATH.exists()
        return load_json(COMPARISON_PATH)

    @pytest.fixture(scope="class")
    def freeze(self):
        assert FREEZE_PATH.exists()
        return load_json(FREEZE_PATH)

    def test_primary_rescued_is_5(self, comparison):
        assert comparison["primary_rescued"] == 5, f"primary_rescued = {comparison['primary_rescued']}, expected 5"

    def test_posthoc_rescued_is_6(self, comparison):
        assert comparison["corrected_rescued"] == 6, f"corrected_rescued = {comparison['corrected_rescued']}, expected 6"

    def test_incremental_pass_is_1(self, comparison):
        delta = comparison["corrected_rescued"] - comparison["primary_rescued"]
        assert delta == 1, f"Incremental PASS = {delta}, expected 1"

    def test_six_cells_with_posthoc_pass(self, comparison):
        rescued = [c for c in comparison["per_cell"] if c.get("new_post_healer_status") == "PASSED"]
        assert len(rescued) == 6, f"Found {len(rescued)} Post-hoc PASSED cells, expected 6"

    def test_five_cells_with_primary_pass(self, comparison):
        rescued = [c for c in comparison["per_cell"] if c.get("primary_post_healer_status") == "PASSED"]
        assert len(rescued) == 5, f"Found {len(rescued)} Primary PASSED cells, expected 5"

    def test_one_noop_to_rescue(self, comparison):
        noop_to_rescue = [c for c in comparison["per_cell"] if c.get("noop_to_rescue")]
        assert len(noop_to_rescue) == 1, f"Found {len(noop_to_rescue)} noop_to_rescue cells, expected 1"

    def test_regression_is_zero(self, freeze):
        assert freeze.get("corrected_regression") == 0, \
            f"corrected_regression = {freeze.get('corrected_regression')}, expected 0"

    def test_no_op_is_zero(self, freeze):
        assert freeze.get("corrected_no_op") == 0, \
            f"corrected_no_op = {freeze.get('corrected_no_op')}, expected 0"


# ---------------------------------------------------------------------------
# 4. Corrected-chain: 10 / 8 / 2 / 1
# ---------------------------------------------------------------------------

class TestCorrectedChain:
    @pytest.fixture(scope="class")
    def comparison(self):
        assert COMPARISON_PATH.exists()
        return load_json(COMPARISON_PATH)

    def test_replayed_is_10(self, comparison):
        assert comparison.get("replayed") == 10, f"replayed = {comparison.get('replayed')}, expected 10"

    def test_same_as_primary_is_8(self, comparison):
        assert comparison.get("same_as_primary") == 8, \
            f"same_as_primary = {comparison.get('same_as_primary')}, expected 8"

    def test_changed_vs_primary_is_2(self, comparison):
        assert comparison.get("changed_vs_primary") == 2, \
            f"changed_vs_primary = {comparison.get('changed_vs_primary')}, expected 2"

    def test_per_cell_count_is_10(self, comparison):
        assert len(comparison.get("per_cell", [])) == 10, \
            f"per_cell count = {len(comparison.get('per_cell', []))}, expected 10"

    def test_primary_pass_fraction(self, comparison):
        assert comparison.get("primary_post_healer_pass_fraction") == "83/320"

    def test_corrected_pass_fraction(self, comparison):
        assert comparison.get("corrected_post_healer_pass_fraction") == "84/320"


# ---------------------------------------------------------------------------
# 5. Builder contains no model calls
# ---------------------------------------------------------------------------

class TestBuilderNoModelCalls:
    @pytest.fixture(scope="class")
    def builder_source(self):
        assert BUILDER_SCRIPT_PATH.exists(), f"Builder not found: {BUILDER_SCRIPT_PATH}"
        return load_builder_source()

    def test_no_openai_import(self, builder_source):
        assert "import openai" not in builder_source
        assert "from openai" not in builder_source

    def test_no_anthropic_import(self, builder_source):
        assert "import anthropic" not in builder_source
        assert "from anthropic" not in builder_source

    def test_no_google_generativeai(self, builder_source):
        # Check for actual import statements (not the prohibition sentinel list)
        assert "import google.generativeai" not in builder_source
        assert "from google.generativeai" not in builder_source
        assert "import google.generativeai as genai" not in builder_source
        assert "genai.generate" not in builder_source

    def test_no_transformers_import(self, builder_source):
        assert "from transformers" not in builder_source
        assert "import transformers" not in builder_source

    def test_no_ollama_import(self, builder_source):
        assert "import ollama" not in builder_source
        assert "from ollama" not in builder_source

    def test_no_requests_post_to_model(self, builder_source):
        """No HTTP POST to known model endpoints."""
        assert "api.openai.com" not in builder_source
        assert "api.anthropic.com" not in builder_source

    def test_prohibited_imports_sentinel_present(self, builder_source):
        """Builder must have a prohibited-imports safety check."""
        assert "_PROHIBITED_IMPORTS" in builder_source or "prohibited" in builder_source.lower()


# ---------------------------------------------------------------------------
# 6. Builder does not execute Healer or Evaluator
# ---------------------------------------------------------------------------

class TestBuilderNoHealerOrEvaluator:
    @pytest.fixture(scope="class")
    def builder_source(self):
        assert BUILDER_SCRIPT_PATH.exists()
        return load_builder_source()

    def test_no_healer_run_call(self, builder_source):
        """Builder must not call Healer run/apply functions."""
        forbidden_patterns = [
            r"healer\.run\(",
            r"healer\.apply\(",
            r"run_healer\(",
            r"apply_healer\(",
            r"Healer\(\)\.run",
        ]
        for pattern in forbidden_patterns:
            assert not re.search(pattern, builder_source), f"Forbidden pattern found: {pattern}"

    def test_no_evaluator_call(self, builder_source):
        """Builder must not call Evaluator score/run functions."""
        forbidden_patterns = [
            r"evaluator\.score\(",
            r"evaluator\.run\(",
            r"run_evaluator\(",
            r"score_cell\(",
            r"Evaluator\(\)\.score",
        ]
        for pattern in forbidden_patterns:
            assert not re.search(pattern, builder_source), f"Forbidden pattern found: {pattern}"

    def test_no_subprocess_model_calls(self, builder_source):
        """Builder must not use subprocess to invoke model scripts."""
        # Check that any subprocess call doesn't invoke generation or healer scripts
        if "subprocess" in builder_source:
            assert "generate" not in builder_source.lower() or "subprocess" not in builder_source.lower()

    def test_healer_calls_count_zero_in_constraints(self, builder_source):
        """Builder must declare healer_calls=0 in output."""
        assert "healer_calls" in builder_source


# ---------------------------------------------------------------------------
# 7. Six cells only from frozen artifacts
# ---------------------------------------------------------------------------

class TestSixCellsFromFrozenArtifacts:
    @pytest.fixture(scope="class")
    def manifest(self):
        assert AUDIT_MANIFEST_PATH.exists()
        return load_json(AUDIT_MANIFEST_PATH)

    @pytest.fixture(scope="class")
    def comparison(self):
        assert COMPARISON_PATH.exists()
        return load_json(COMPARISON_PATH)

    def test_manifest_six_cells_count(self, manifest):
        cells = manifest.get("six_posthoc_rescued_cells", [])
        assert len(cells) == 6, f"Manifest has {len(cells)} cells, expected 6"

    def test_manifest_cells_match_frozen_comparison(self, manifest, comparison):
        """All manifest cell_ids must appear in frozen comparison artifact."""
        frozen_ids = {c["cell_id"] for c in comparison.get("per_cell", [])}
        manifest_ids = {c["cell_id"] for c in manifest.get("six_posthoc_rescued_cells", [])}
        unknown = manifest_ids - frozen_ids
        assert not unknown, f"Manifest cell_ids not in frozen comparison: {unknown}"

    def test_manifest_cells_all_posthoc_pass(self, manifest, comparison):
        """All 6 manifest cells must be Post-hoc PASSED in frozen comparison."""
        posthoc_passed = {
            c["cell_id"] for c in comparison.get("per_cell", [])
            if c.get("new_post_healer_status") == "PASSED"
        }
        for cell in manifest.get("six_posthoc_rescued_cells", []):
            assert cell["cell_id"] in posthoc_passed, \
                f"Cell {cell['cell_id']} is in manifest but not Post-hoc PASSED"

    def test_manifest_before_hashes_match_frozen(self, manifest, comparison):
        """Before hashes in manifest must match frozen comparison artifact."""
        frozen_hashes = {
            c["cell_id"]: c.get("before_source_sha256", "")
            for c in comparison.get("per_cell", [])
        }
        for cell in manifest.get("six_posthoc_rescued_cells", []):
            cid = cell["cell_id"]
            manifest_hash = cell.get("before_snippet_hash", "")
            frozen_hash = frozen_hashes.get(cid, "")
            if frozen_hash:
                assert manifest_hash == frozen_hash, \
                    f"Before hash mismatch for {cid}: manifest={manifest_hash}, frozen={frozen_hash}"

    def test_manifest_has_no_invented_cell_ids(self, manifest, comparison):
        """No manifest cell should have a cell_id not in the frozen comparison."""
        frozen_ids = {c["cell_id"] for c in comparison.get("per_cell", [])}
        for cell in manifest.get("six_posthoc_rescued_cells", []):
            assert cell["cell_id"] in frozen_ids, \
                f"INVENTED cell_id detected: {cell['cell_id']}"


# ---------------------------------------------------------------------------
# 8. No self-invented cell IDs
# ---------------------------------------------------------------------------

class TestNoInventedCellIds:
    @pytest.fixture(scope="class")
    def all_known_cell_ids(self):
        records = load_jsonl(PRIMARY_ELIGIBLE_PATH)
        return {r["cell_id"] for r in records}

    def test_manifest_cell_ids_all_known(self, all_known_cell_ids):
        """All manifest cell_ids must appear in the primary eligible execution records."""
        manifest = load_json(AUDIT_MANIFEST_PATH)
        for cell in manifest.get("six_posthoc_rescued_cells", []):
            assert cell["cell_id"] in all_known_cell_ids, \
                f"cell_id not found in primary eligible records: {cell['cell_id']}"


# ---------------------------------------------------------------------------
# 9. Final Report and Evidence Complete SHA unchanged
# ---------------------------------------------------------------------------

class TestFrozenSHAs:
    def test_final_report_v13_sha_unchanged(self):
        """Final Report v1.3 SHA must match frozen value."""
        assert FINAL_REPORT_V13_PATH.exists(), f"Final Report not found: {FINAL_REPORT_V13_PATH}"
        actual = sha256_file(FINAL_REPORT_V13_PATH)
        assert actual == FROZEN_SHA_FINAL_REPORT_V13, (
            f"Final Report v1.3 SHA MISMATCH!\n"
            f"  expected: {FROZEN_SHA_FINAL_REPORT_V13}\n"
            f"  actual:   {actual}\n"
            "The Final Report has been modified — STOP."
        )

    def test_evidence_complete_sha_unchanged(self):
        """Evidence Complete manifest SHA must match frozen value."""
        assert EVIDENCE_COMPLETE_PATH.exists(), f"Evidence Complete not found: {EVIDENCE_COMPLETE_PATH}"
        actual = sha256_file(EVIDENCE_COMPLETE_PATH)
        assert actual == FROZEN_SHA_EVIDENCE_COMPLETE, (
            f"Evidence Complete SHA MISMATCH!\n"
            f"  expected: {FROZEN_SHA_EVIDENCE_COMPLETE}\n"
            f"  actual:   {actual}\n"
            "The Evidence Complete has been modified — STOP."
        )


# ---------------------------------------------------------------------------
# 10. No Stress Test execution
# ---------------------------------------------------------------------------

class TestNoStressTest:
    def test_no_stress_test_artifacts(self):
        """No formal Stress Test result artifact directories should exist."""
        artifacts_root = REPO_ROOT / "artifacts"
        if not artifacts_root.exists():
            return  # No artifacts dir at all — fine
        formal_stress_dirs = [
            d for d in artifacts_root.glob("**/formal")
            if "stress_test" in str(d)
        ]
        assert not formal_stress_dirs, (
            f"Formal Stress Test execution artifacts found: {formal_stress_dirs}"
        )

    def test_no_stress_test_scripts_executed(self):
        """No stress test execution runner scripts should be present in scripts dir."""
        scripts_dir = REPO_ROOT / "scripts"
        stress_scripts = [
            p for p in scripts_dir.glob("*stress_test*")
            if p.is_file() and not p.name.startswith(("build_", "preflight_"))
        ]
        assert not stress_scripts, f"Stress test execution scripts found: {stress_scripts}"


# ---------------------------------------------------------------------------
# 11. No official analysis result report produced
# ---------------------------------------------------------------------------

class TestNoOfficialResultReport:
    def test_no_official_analysis_result_in_output(self):
        """Output directory must not contain an official result report."""
        output_dir = REPO_ROOT / "artifacts/math16_posthoc_six_cell_rescue_audit_v1"
        if not output_dir.exists():
            return  # No output yet — fine
        # Official result reports would be named e.g. "final_report_*" or "official_result_*"
        forbidden_patterns = [
            "final_report_*.md",
            "official_result_*.md",
            "analysis_result_*.md",
        ]
        for pattern in forbidden_patterns:
            found = list(output_dir.rglob(pattern))
            assert not found, f"Official result report found in output: {found}"


# ---------------------------------------------------------------------------
# 12. No Poster/PPT/Slides output from Builder/Preflight
# ---------------------------------------------------------------------------

class TestNoPosterOrSlides:
    def test_builder_does_not_produce_poster(self):
        """Builder must not produce Poster or PPT files."""
        source = load_builder_source()
        forbidden = [".pptx", ".ppt", "poster", "slides", "presentation"]
        # Check none of these appear in write/output paths
        for term in forbidden:
            # Allow references in comments/docs as long as not in write paths
            # Check if it appears in a write operation context
            write_lines = [
                ln for ln in source.split("\n")
                if "write_text" in ln or "open(" in ln
            ]
            for line in write_lines:
                assert term not in line.lower(), \
                    f"Builder appears to write {term} file: {line.strip()}"

    def test_preflight_does_not_produce_poster(self):
        """Preflight must not produce Poster or PPT files."""
        with open(PREFLIGHT_SCRIPT_PATH, encoding="utf-8") as f:
            source = f.read()
        forbidden = [".pptx", ".ppt", "poster", "slides"]
        for term in forbidden:
            write_lines = [ln for ln in source.split("\n") if "write_text" in ln or "open(" in ln]
            for line in write_lines:
                assert term not in line.lower(), \
                    f"Preflight appears to write {term} file: {line.strip()}"


# ---------------------------------------------------------------------------
# Integration: Run preflight import (no side effects)
# ---------------------------------------------------------------------------

class TestBuilderAndPrefightCanImport:
    def test_builder_is_valid_python(self):
        """Builder script must be valid Python (parseable)."""
        with open(BUILDER_SCRIPT_PATH, encoding="utf-8") as f:
            source = f.read()
        try:
            ast.parse(source)
        except SyntaxError as e:
            pytest.fail(f"Builder script has a syntax error: {e}")

    def test_preflight_is_valid_python(self):
        """Preflight script must be valid Python (parseable)."""
        with open(PREFLIGHT_SCRIPT_PATH, encoding="utf-8") as f:
            source = f.read()
        try:
            ast.parse(source)
        except SyntaxError as e:
            pytest.fail(f"Preflight script has a syntax error: {e}")

    def test_manifest_is_valid_json(self):
        """Audit manifest must be valid JSON."""
        assert AUDIT_MANIFEST_PATH.exists()
        try:
            load_json(AUDIT_MANIFEST_PATH)
        except json.JSONDecodeError as e:
            pytest.fail(f"Audit manifest is not valid JSON: {e}")

    def test_taxonomy_json_is_valid_json(self):
        """Taxonomy JSON must be valid JSON."""
        assert TAXONOMY_JSON_PATH.exists()
        try:
            load_json(TAXONOMY_JSON_PATH)
        except json.JSONDecodeError as e:
            pytest.fail(f"Taxonomy JSON is not valid JSON: {e}")
