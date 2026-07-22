# -*- coding: utf-8 -*-
"""Unit tests for Math16 Pilot-02 Executive One-Pager v1."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ONE_PAGER_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v1"
MANIFEST_PATH = ONE_PAGER_DIR / "one_pager_manifest.json"
REPORT_PATH = ONE_PAGER_DIR / "one_pager_build_report.md"
PNG_PATH = ONE_PAGER_DIR / "math16_pilot02_one_pager_v1.png"
PDF_PATH = ONE_PAGER_DIR / "math16_pilot02_one_pager_v1.pdf"

CLAIMS_PATH = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/frozen_numeric_claims.json"
FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"

PRESERVED_SHA = {
    "figure_01_baseline_overall.png": "5bc0c714769c987710dd124b7f126a53a4c77f96ccd578fbff4a0c82bdb52db2",
    "figure_03_family_breakdown.png": "f164edc807659c45628cbab4711074879af58d3beaa825f59aaf2ebce4c9fb79",
    "figure_04_tier1_paired_analysis.png": "f18bbb774e9a75c51da364f080281172e7c35c4a5b2e30245142de0993565fdf",
    "figure_05_healer_eligibility_boundary.png": "5887f0b829797ab63f30a096ec2e27c80530c1f988dcc16e3bead4bd7feb9885",
}


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# ── File existence ─────────────────────────────────────────────────────────────

def test_one_pager_output_files_exist():
    """PNG, PDF, manifest, and report must all exist and be non-empty."""
    for p in [PNG_PATH, PDF_PATH, MANIFEST_PATH, REPORT_PATH]:
        assert p.exists(), f"Missing output: {p.name}"
        assert p.stat().st_size > 0, f"Empty output: {p.name}"


# ── PDF page count ─────────────────────────────────────────────────────────────

def test_pdf_has_exactly_one_page():
    """PDF /Count must be 1 (strict single page)."""
    data = PDF_PATH.read_bytes()
    count_matches = re.findall(rb'/Count\s+(\d+)', data)
    assert len(count_matches) >= 1, "No /Count found in PDF"
    assert int(count_matches[0]) == 1, f"PDF page count is {count_matches[0]}, expected 1"

    page_type_count = len(re.findall(rb'/Type\s*/Page\b', data))
    assert page_type_count == 1, f"PDF /Type /Page count = {page_type_count}, expected 1"


# ── Manifest structure ────────────────────────────────────────────────────────

def test_manifest_structure():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    assert m["manifest_id"] == "math16_pilot02_one_pager_v1_manifest"
    assert m["page_count"] == 1
    assert m["figure_count"] == 4
    assert m["page_format"] == "A4 landscape (297mm x 210mm)"
    assert m["dpi"] == 300


def test_manifest_exactly_four_figures():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    used = m["figures_used"]
    assert len(used) == 4
    assert "fig1_baseline_overall" in used
    assert "fig3_family_breakdown" in used
    assert "fig4_tier1_paired_analysis" in used
    assert "fig5_healer_eligibility_boundary" in used


def test_manifest_excludes_figure_2_and_6():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    excluded = m["figures_excluded"]
    assert "fig2_prompt_conditions" in excluded
    assert "fig6_healer_concept_zones" in excluded

    # Double-check: figs 2 and 6 not in used list
    used = m["figures_used"]
    assert "fig2_prompt_conditions" not in used
    assert "fig6_healer_concept_zones" not in used


# ── Core numeric claims ────────────────────────────────────────────────────────

def test_manifest_core_numbers_correct():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    pa = m["primary_posthoc_accounting"]
    assert "289/320" in pa["gemini_primary"]
    assert "78/320" in pa["qwen4b_baseline"]
    assert "101/320" in pa["qwen9b_baseline"]
    assert "5 cells" in pa["qwen4b_primary_rescue"]
    assert "83/320" in pa["qwen4b_primary_rescue"]
    assert "6 cells" in pa["qwen4b_posthoc_rescue"]
    assert "84/320" in pa["qwen4b_posthoc_rescue"]
    assert pa["gemini_eligible"] == 0
    assert pa["qwen9b_eligible"] == 0
    assert pa["observed_regression"] == 0


def test_manifest_statistics_correct():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    ks = m["key_statistics"]
    assert ks["nine_b_only"] == 49
    assert ks["four_b_only"] == 26
    assert ks["net_cell_gain"] == 23
    assert ks["paired_risk_diff_pct"] == 7.19
    assert ks["exact_mcnemar_p"] == 0.010582
    assert "-0.94%" in ks["task_clustered_bootstrap_95ci"]
    assert "+14.38%" in ks["task_clustered_bootstrap_95ci"]


# ── Primary / Post-hoc accounting ────────────────────────────────────────────

def test_primary_posthoc_clearly_separated():
    """Primary rescue=5 and Post-hoc rescue=6 must appear as distinct values."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    pa = m["primary_posthoc_accounting"]
    # Primary: 5 cells → 83/320
    assert "5 cells" in pa["qwen4b_primary_rescue"]
    assert "83/320" in pa["qwen4b_primary_rescue"]
    # Post-hoc: 6 cells → 84/320 labeled as Post-hoc
    assert "6 cells" in pa["qwen4b_posthoc_rescue"]
    assert "84/320" in pa["qwen4b_posthoc_rescue"]
    assert "Post-hoc" in pa["qwen4b_posthoc_rescue"]


# ── McNemar & Bootstrap CI ────────────────────────────────────────────────────

def test_mcnemar_and_bootstrap_ci_in_report():
    """Build report must contain McNemar p and Bootstrap CI values."""
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "0.010582" in text, "McNemar p missing from report"
    assert "-0.94%" in text, "Bootstrap CI lower bound missing"
    assert "+14.38%" in text, "Bootstrap CI upper bound missing"


# ── Source figure SHA preservation ───────────────────────────────────────────

def test_source_figures_1_3_4_5_sha_preserved():
    """Source figure PNGs must not have been modified."""
    for fname, expected in PRESERVED_SHA.items():
        p = FIG_DIR / fname
        assert p.exists(), f"Source figure missing: {fname}"
        actual = compute_sha256(p)
        assert actual == expected, (
            f"SHA MISMATCH {fname}: expected {expected[:16]}... got {actual[:16]}..."
        )


def test_manifest_records_correct_source_shas():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    recorded = m["source_figure_shas"]
    for fname, expected in PRESERVED_SHA.items():
        assert recorded.get(fname) == expected, f"Manifest SHA mismatch for {fname}"


# ── No forbidden outputs ──────────────────────────────────────────────────────

def test_no_poster_or_oral_slides_in_output():
    """Output directory must not contain poster or oral slides."""
    forbidden = ["poster", "oral", ".pptx", ".ppt"]
    for p in ONE_PAGER_DIR.iterdir():
        for pat in forbidden:
            assert pat not in p.name.lower(), f"Forbidden output: {p.name}"


def test_evidence_complete_milestone_not_modified():
    """Frozen claims JSON must match the SHA recorded in manifest."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    recorded_sha = m["input_milestone_sha256"]
    actual_sha = compute_sha256(CLAIMS_PATH)
    assert actual_sha == recorded_sha, (
        f"frozen_numeric_claims.json modified! recorded: {recorded_sha[:16]}... actual: {actual_sha[:16]}..."
    )
