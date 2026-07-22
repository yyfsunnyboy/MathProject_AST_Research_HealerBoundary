# -*- coding: utf-8 -*-
"""Unit tests for Math16 Pilot-02 Executive One-Pager v2."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

V2_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v2"
V1_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v1"
ASSETS_DIR = V2_DIR / "assets"
MANIFEST_PATH = V2_DIR / "one_pager_v2_manifest.json"
REPORT_PATH = V2_DIR / "one_pager_v2_build_report.md"
PNG_PATH = V2_DIR / "math16_pilot02_one_pager_v2.png"
PDF_PATH = V2_DIR / "math16_pilot02_one_pager_v2.pdf"

CLAIMS_PATH = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/frozen_numeric_claims.json"
FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"

ORIG_SHAS = {
    "figure_01_baseline_overall.png": "5bc0c714769c987710dd124b7f126a53a4c77f96ccd578fbff4a0c82bdb52db2",
    "figure_03_family_breakdown.png": "f164edc807659c45628cbab4711074879af58d3beaa825f59aaf2ebce4c9fb79",
    "figure_04_tier1_paired_analysis.png": "f18bbb774e9a75c51da364f080281172e7c35c4a5b2e30245142de0993565fdf",
    "figure_05_healer_eligibility_boundary.png": "5887f0b829797ab63f30a096ec2e27c80530c1f988dcc16e3bead4bd7feb9885",
}
V1_PNG_SHA = "1998988aabcb0b61e37c257e51e35008db56ab51abe0e43540789355cbb8d234"
V1_PDF_SHA = "adc5b870cdcdbd7595dbcaa79efb44b08423196893bd544f3ab10d18d262cd21"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# ── File existence ────────────────────────────────────────────────────────────

def test_v2_all_required_files_exist():
    for p in [PNG_PATH, PDF_PATH, MANIFEST_PATH, REPORT_PATH]:
        assert p.exists(), f"Missing: {p.name}"
        assert p.stat().st_size > 0, f"Empty: {p.name}"

    for fname in ["fig1_compact.png", "fig3_compact.png",
                  "fig4_compact.png", "fig5_compact.png"]:
        p = ASSETS_DIR / fname
        assert p.exists(), f"Missing compact asset: {fname}"
        assert p.stat().st_size > 0, f"Empty compact asset: {fname}"


# ── PDF page count ────────────────────────────────────────────────────────────

def test_v2_pdf_exactly_one_page():
    data = PDF_PATH.read_bytes()
    counts = re.findall(rb'/Count\s+(\d+)', data)
    assert int(counts[0]) == 1, f"PDF /Count = {counts[0]}, expected 1"
    page_types = re.findall(rb'/Type\s*/Page\b', data)
    assert len(page_types) == 1, f"/Type /Page count = {len(page_types)}, expected 1"


# ── Manifest structure ────────────────────────────────────────────────────────

def test_v2_manifest_structure():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    assert m["manifest_id"] == "math16_pilot02_one_pager_v2_manifest"
    assert m["page_count"] == 1
    assert m["figure_count"] == 4
    assert m["page_format"] == "A4 landscape (297mm x 210mm)"
    assert m["dpi"] == 300
    assert m["layout_version"] == "v2_asymmetric"


def test_v2_uses_compact_figures():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    compact = m["compact_figures_used"]
    assert len(compact) == 4
    for expected in ["fig1_compact.png", "fig3_compact.png",
                     "fig4_compact.png", "fig5_compact.png"]:
        assert expected in compact


def test_v2_does_not_directly_embed_originals():
    """Original full-resolution PNGs must appear in excluded list."""
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    excluded = m["original_figures_excluded_from_direct_embed"]
    for fname in ["figure_01_baseline_overall.png", "figure_03_family_breakdown.png",
                  "figure_04_tier1_paired_analysis.png", "figure_05_healer_eligibility_boundary.png"]:
        assert fname in excluded


def test_v2_excludes_figure_2_and_6():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    excl = m["figures_excluded"]
    assert "fig2_prompt_conditions" in excl
    assert "fig6_healer_concept_zones" in excl


# ── Core numbers ─────────────────────────────────────────────────────────────

def test_v2_manifest_core_numbers():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    pa = m["primary_posthoc_accounting"]
    assert "5 cells" in pa["qwen4b_primary_rescue"]
    assert "83/320" in pa["qwen4b_primary_rescue"]
    assert "6 cells" in pa["qwen4b_posthoc_rescue"]
    assert "84/320" in pa["qwen4b_posthoc_rescue"]
    assert "Post-hoc" in pa["qwen4b_posthoc_rescue"]
    assert pa["gemini_eligible"] == 0
    assert pa["qwen9b_eligible"] == 0
    assert pa["observed_regression"] == 0


def test_v2_manifest_statistics():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    ks = m["key_statistics"]
    assert ks["nine_b_only"] == 49
    assert ks["four_b_only"] == 26
    assert ks["exact_mcnemar_p"] == 0.010582
    assert "-0.94%" in ks["task_clustered_bootstrap_95ci"]
    assert "+14.38%" in ks["task_clustered_bootstrap_95ci"]


# ── Primary/Post-hoc separation ──────────────────────────────────────────────

def test_v2_primary_posthoc_separated():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    pa = m["primary_posthoc_accounting"]
    # Primary = 5, Post-hoc = 6, distinct
    assert "5 cells → 83/320" in pa["qwen4b_primary_rescue"]
    assert "6 cells → 84/320" in pa["qwen4b_posthoc_rescue"]


# ── McNemar & CI in report ────────────────────────────────────────────────────

def test_v2_report_has_mcnemar_and_ci():
    text = REPORT_PATH.read_text(encoding="utf-8")
    assert "0.010582" in text
    assert "-0.94%" in text
    assert "+14.38%" in text


# ── Original figure SHA preserved ────────────────────────────────────────────

def test_original_source_figures_sha_preserved():
    for fname, expected in ORIG_SHAS.items():
        p = FIG_DIR / fname
        actual = sha256(p)
        assert actual == expected, f"SHA changed for {fname}"


def test_manifest_records_correct_original_shas():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    recorded = m["source_original_shas"]
    for fname, expected in ORIG_SHAS.items():
        assert recorded.get(fname) == expected, f"Manifest SHA mismatch: {fname}"


# ── v1 files unchanged ────────────────────────────────────────────────────────

def test_v1_files_not_modified():
    """v1 outputs must not be overwritten."""
    v1_png = V1_DIR / "math16_pilot02_one_pager_v1.png"
    v1_pdf = V1_DIR / "math16_pilot02_one_pager_v1.pdf"
    assert v1_png.exists() and v1_png.stat().st_size > 0
    assert v1_pdf.exists() and v1_pdf.stat().st_size > 0
    # SHA must be identical to the original v1 build
    assert sha256(v1_png) == V1_PNG_SHA, "v1 PNG was overwritten!"
    assert sha256(v1_pdf) == V1_PDF_SHA, "v1 PDF was overwritten!"


# ── No forbidden outputs ──────────────────────────────────────────────────────

def test_no_poster_or_oral_slides_in_v2():
    forbidden = ["poster", "oral", ".pptx", ".ppt"]
    for p in V2_DIR.rglob("*"):
        if p.is_file():
            for pat in forbidden:
                assert pat not in p.name.lower(), f"Forbidden: {p.name}"


# ── Evidence Complete not modified ────────────────────────────────────────────

def test_evidence_complete_not_modified():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    recorded = m["input_milestone_sha256"]
    actual = sha256(CLAIMS_PATH)
    assert actual == recorded, "frozen_numeric_claims.json was modified!"


# ── v1 defects listed in manifest ────────────────────────────────────────────

def test_v2_manifest_records_v1_defects_fixed():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    fixes = m["v1_defects_fixed"]
    assert len(fixes) >= 3, "v2 should record at least 3 v1 defects fixed"
    # Must mention top text clipping
    any_clipping = any("clipping" in fix.lower() or "text" in fix.lower() for fix in fixes)
    assert any_clipping, "Must document top text clipping fix"
    # Must mention asymmetric layout
    any_asymmetric = any("asymmetric" in fix.lower() or "fig4" in fix.lower() or "55%" in fix for fix in fixes)
    assert any_asymmetric, "Must document asymmetric layout"
