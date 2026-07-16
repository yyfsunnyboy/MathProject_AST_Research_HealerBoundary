"""Audit closeout tests: taxonomy, ledgers, hashes, max_passes, L2 evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from agent_tools.finals_rebuild.ce115_clean_incremental_ablation import (
    CANONICALIZATION_DEFINITION,
    LINEAGE_ID,
    canonical_file_text_hash,
    canonical_prompt_hash,
    file_byte_hash,
    prompt_file_byte_hash,
    prompt_sha256,
)
from agent_tools.finals_rebuild.ce115_research_healer_protocol import (
    ALLOWED_LAYERS,
    FROZEN_EXECUTION_POLICY,
    TASK_DIFFICULTY_VS_FAILURE_LAYER_NOTE,
)
from agent_tools.finals_rebuild.ce115_research_healer_runner import (
    EXPERIMENTAL_RULE_REGISTRY,
    RULE_ALLOWLIST,
    RULE_REGISTRY,
    MathHealerRunner,
    iter_exploratory_cases,
    iter_manifest_cases,
    load_regression_manifest,
    run_research_healer,
)
from agent_tools.finals_rebuild.ce115_research_healer_rules_l2 import RULE_ID as L2_ID
from agent_tools.finals_rebuild.math_boundary_pilot import (
    classify_response,
    load_pilot_tasks,
)
from scripts import run_ce115_gemini_three_condition_pilot as gemini_pilot
from scripts import run_ce115_qwen_three_condition_pilot as qwen_pilot

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "tests/finals_rebuild/fixtures/ce115_research_healer"
MANIFEST_PATH = FIX / "regression_manifest.json"
LEDGER_PATH = (
    ROOT
    / "docs/experiments/analysis/ce115_qwen_clean_incremental_seven_cell_forensic_ledger.json"
)
COMPANION_PATH = (
    ROOT
    / "docs/experiments/analysis/ce115_clean_incremental_prompt_hash_companion_ledger.json"
)
SPEC_PATH = ROOT / "docs/experiments/analysis/ce115_research_healer_frozen_spec_v1.md"
TASK_MANIFEST = ROOT / "tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl"
FORMAL_PILOTS = (
    "ce115_gemini_clean_incremental_pilot_01",
    "ce115_qwen_clean_incremental_pilot_01",
)

LEDGER_REQUIRED_FIELDS = (
    "cell_id",
    "artifact_path",
    "candidate_path",
    "source_file_byte_hash",
    "canonical_source_hash",
    "artifact_declared_candidate_hash",
    "task_id",
    "condition",
    "seed",
    "observed_evaluator_status",
    "primary_layer",
    "latent_layers",
    "eligibility",
    "evidence",
    "adjudication_rationale",
    "confidence",
    "labelled_by",
    "first_audit_reviewed_by",
    "second_audit_reviewed_by",
    "review_dates",
    "review_status",
)

COMPANION_REQUIRED_FIELDS = (
    "cell_id",
    "artifact_path",
    "canonical_prompt_hash",
    "prompt_file_byte_hash",
    "canonicalization_definition",
    "legacy_prompt_hash",
    "legacy_prompt_hash_is_alias_of",
)


def test_production_allowlist_only_approved_l2():
    assert RULE_ALLOWLIST == (L2_ID,)
    assert set(RULE_REGISTRY) == {L2_ID}
    assert "L1_COMMENT_ONLY_IF_INSERT_PASS" in EXPERIMENTAL_RULE_REGISTRY
    assert "L1_COMMENT_ONLY_IF_INSERT_PASS" not in RULE_ALLOWLIST
    manifest = load_regression_manifest(MANIFEST_PATH)
    assert manifest["allowlist_expected"] == [L2_ID]
    assert "fail_exact_ab2d_l1" not in {
        c["case_id"] for c in iter_manifest_cases(manifest)
    }
    exploratory = iter_exploratory_cases(manifest)
    assert any(c["case_id"] == "fail_exact_ab2d_l1" for c in exploratory)
    assert all(c.get("production_approved") is False for c in exploratory)


def test_taxonomy_completeness_and_difficulty_separation():
    assert ALLOWED_LAYERS == frozenset(
        {"L0", "L1", "L2", "L3", "L4", "L5", "L6", "META"}
    )
    assert "_l1" in TASK_DIFFICULTY_VS_FAILURE_LAYER_NOTE or "'_l1'" in TASK_DIFFICULTY_VS_FAILURE_LAYER_NOTE
    assert "_l1" not in ALLOWED_LAYERS
    assert "l1" not in ALLOWED_LAYERS


def test_companion_prompt_hash_ledger_schema_and_18_cells():
    companion = json.loads(COMPANION_PATH.read_text(encoding="utf-8"))
    assert companion["cell_count"] == 18
    assert len(companion["cells"]) == 18
    assert companion["pilots"] == list(FORMAL_PILOTS)
    assert companion["legacy_prompt_hash_is_alias_of"] == "canonical_prompt_hash"
    assert "universal-newline" in companion["canonicalization_definition"].lower()

    by_pair: dict[tuple[str, str], dict[str, str]] = {}
    for cell in companion["cells"]:
        for field in COMPANION_REQUIRED_FIELDS:
            assert field in cell, f"missing {field} in {cell.get('cell_id')}"
        assert cell["legacy_prompt_hash_is_alias_of"] == "canonical_prompt_hash"
        assert cell["legacy_prompt_hash"] == cell["canonical_prompt_hash"]
        assert cell["canonicalization_definition"] == companion["canonicalization_definition"]

        prompt_path = ROOT / cell["prompt_path"]
        art_path = ROOT / cell["artifact_path"]
        assert prompt_path.is_file()
        assert art_path.is_file()
        assert file_byte_hash(prompt_path) == cell["prompt_file_byte_hash"]
        assert canonical_file_text_hash(prompt_path) == cell["canonical_prompt_hash"]

        art = json.loads(art_path.read_text(encoding="utf-8"))
        declared = art.get("prompt_hash") or art["hashes"]["prompt"]
        assert declared == cell["legacy_prompt_hash"]
        assert declared == cell["canonical_prompt_hash"]

        key = (cell["task_id"], cell["condition"])
        by_pair.setdefault(key, {})[cell["model_family"]] = cell["canonical_prompt_hash"]

    assert len(by_pair) == 9
    for key, models in by_pair.items():
        assert models["gemini"] == models["qwen"], key


def test_seven_cell_three_source_hashes_reconcile():
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    assert ledger["cell_count"] == 7
    assert len(ledger["cells"]) == 7
    assert ledger["ledger_kind"] == "manually-labelled forensic ledger"
    assert set(ledger["taxonomy_layers_allowed"]) == set(ALLOWED_LAYERS)
    prohibited = " ".join(ledger["prohibited"]).lower()
    assert "failure_class" in prohibited
    assert "independently human-verified" in prohibited

    for cell in ledger["cells"]:
        for field in LEDGER_REQUIRED_FIELDS:
            assert field in cell, f"missing {field} in {cell.get('cell_id')}"
        assert "source_sha256" not in cell
        assert cell["adjudication_kind"] == "manually-labelled forensic ledger"
        assert cell["primary_layer"] in ALLOWED_LAYERS
        for layer in cell["latent_layers"]:
            assert layer in ALLOWED_LAYERS
        assert cell.get("layer_not_derived_from_failure_class") is True

        cand = ROOT / cell["candidate_path"]
        art_path = ROOT / cell["artifact_path"]
        assert cand.is_file()
        assert art_path.is_file()

        byte_h = file_byte_hash(cand)
        canon_h = canonical_file_text_hash(cand)
        art = json.loads(art_path.read_text(encoding="utf-8"))
        declared = art["hashes"]["extracted_candidate"]

        assert byte_h == cell["source_file_byte_hash"]
        assert canon_h == cell["canonical_source_hash"]
        assert declared == cell["artifact_declared_candidate_hash"]
        assert declared == canon_h


def test_formal_pilot_artifacts_unmodified_in_git_and_hashes():
    """Formal clean pilots must remain untouched (no working-tree edits)."""
    proc = subprocess.run(
        ["git", "status", "--short", "--", *[f"docs/experiments/results/{p}" for p in FORMAL_PILOTS]],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert proc.stdout.strip() == "", proc.stdout

    companion = json.loads(COMPANION_PATH.read_text(encoding="utf-8"))
    for cell in companion["cells"]:
        art_path = ROOT / cell["artifact_path"]
        prompt_path = ROOT / cell["prompt_path"]
        # Re-check declared hashes still match companion (artifacts not rewritten).
        art = json.loads(art_path.read_text(encoding="utf-8"))
        assert art["hashes"]["prompt"] == cell["canonical_prompt_hash"]
        assert prompt_file_byte_hash(prompt_path) == cell["prompt_file_byte_hash"]


def test_adjudication_provenance_and_safe_wording():
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    prov = ledger["review_provenance"]
    for key in (
        "labelled_by",
        "first_audit_reviewed_by",
        "second_audit_reviewed_by",
        "review_dates",
        "review_status",
    ):
        assert key in prov
        assert prov[key]
    assert prov["ledger_kind"] == "manually-labelled forensic ledger"
    assert "independently human-verified" in [c.lower() for c in prov["prohibited_claims"]]

    text = SPEC_PATH.read_text(encoding="utf-8")
    assert "manually-labelled forensic ledger" in text
    assert "independently human-verified" in text
    assert "frozen-oracle-assisted deterministic structural repair" in text
    assert "canonical_prompt_hash" in text
    assert "source_file_byte_hash" in text
    assert "canonical_source_hash" in text


def test_canonical_prompt_hashes_gemini_qwen_builder_consistent(tmp_path):
    g_plan = gemini_pilot.build_plan(tmp_path / "g")
    q_plan = qwen_pilot.build_plan(tmp_path / "q")
    assert g_plan["prompt_lineage"] == q_plan["prompt_lineage"] == LINEAGE_ID
    g_canon = {
        (c["task_id"], c["condition"]): c["canonical_prompt_hash"] for c in g_plan["cells"]
    }
    q_canon = {
        (c["task_id"], c["condition"]): c["canonical_prompt_hash"] for c in q_plan["cells"]
    }
    assert g_canon == q_canon
    for plan in (g_plan, q_plan):
        for cell in plan["cells"]:
            assert cell["prompt_hash"] == cell["canonical_prompt_hash"]
            assert cell["canonical_prompt_hash"] == canonical_prompt_hash(cell["prompt"])
            assert cell["canonical_prompt_hash"] == prompt_sha256(cell["prompt"])


def test_max_passes_transactional_rollback():
    source = "x = 1\n"
    from agent_tools.finals_rebuild.ce115_research_healer_runner import _RegisteredRule

    def _reg(rule_id: str, priority: int, marker: str) -> _RegisteredRule:
        def is_applicable(s, ctx):
            return True, {}, "ok"

        def is_triggered(s, ctx):
            return marker not in s, "trig"

        def apply(s, ctx):
            return s + marker, {}, "mut"

        return _RegisteredRule(
            rule_id=rule_id,
            layer="META",
            priority=priority,
            is_applicable=is_applicable,
            is_triggered=is_triggered,
            apply=apply,
        )

    registry = {
        "a": _reg("a", 1, "#A\n"),
        "b": _reg("b", 2, "#B\n"),
    }
    result = run_research_healer(
        source,
        allowlist=("a", "b"),
        registry=registry,
        max_passes=1,
    )
    assert result.final_status == "max_passes_exceeded"
    assert result.rolled_back is True
    assert result.consumer_may_use_output is False
    assert result.output_source == source
    assert result.real_model_calls == 0
    assert FROZEN_EXECUTION_POLICY["max_passes_semantics"] == "transactional_rollback"


def test_h3_single_l2_repair_to_pass_not_regressed():
    case = next(
        c
        for c in iter_manifest_cases(load_regression_manifest(MANIFEST_PATH))
        if c["case_id"] == "fail_radical_ab1_l2"
    )
    source = (FIX / case["source_artifact"]).read_text(encoding="utf-8")
    frozen = json.loads((FIX / case["frozen_artifact"]).read_text(encoding="utf-8"))
    task = {
        t["task_id"]: t for t in load_pilot_tasks(TASK_MANIFEST)
    }["ce115_calc_radical_simplification_l1"]
    before = classify_response(source, {"oracle_payload": frozen}, task)[0]
    assert before == "schema_failure"
    result = MathHealerRunner().run(source, context={"frozen": frozen, "task": task})
    assert result.final_status == "changed"
    assert result.real_model_calls == 0
    assert result.consumer_may_use_output is True
    assert result.rolled_back is False
    changed = next(o for o in result.rule_outcomes if o.changed)
    assert changed.rule_id == L2_ID
    assert changed.validation.get("oracle_assisted") is True
    assert changed.validation.get("oracle_free_claimed") is False
    assert "frozen-oracle-assisted" in changed.validation.get("research_positioning", "")
    assert "radicand" in changed.validation.get("frozen_oracle_fields_read", {}).get(
        "keys", []
    )
    after = classify_response(result.output_source, {"oracle_payload": frozen}, task)[0]
    assert after == "passed"


def test_real_model_calls_zero_on_all_manifest_cases():
    for case in iter_manifest_cases(load_regression_manifest(MANIFEST_PATH)):
        source = (FIX / case["source_artifact"]).read_text(encoding="utf-8")
        frozen = json.loads((FIX / case["frozen_artifact"]).read_text(encoding="utf-8"))
        result = MathHealerRunner().run(source, context={"frozen": frozen})
        assert result.real_model_calls == 0


def test_canonicalization_definition_exported():
    assert "universal-newline" in CANONICALIZATION_DEFINITION.lower()


def test_git_diff_check_clean():
    proc = subprocess.run(
        ["git", "diff", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
