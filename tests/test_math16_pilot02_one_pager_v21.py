# -*- coding: utf-8 -*-
"""Unit tests for Math16 Pilot-02 Executive One-Pager v2.1."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

V21_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v21"
V2_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v2"
V1_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v1"
ASSETS_DIR = V21_DIR / "assets"
MANIFEST_PATH = V21_DIR / "one_pager_v21_manifest.json"
REPORT_PATH = V21_DIR / "one_pager_v21_build_report.md"
PNG_PATH = V21_DIR / "math16_pilot02_one_pager_v21.png"
PDF_PATH = V21_DIR / "math16_pilot02_one_pager_v21.pdf"

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
V2_PNG_SHA = "7e582554e2a1c2e27aa86199ec759f583fcd498e6fd6a1bd9ef9da50467fbefc"
V2_PDF_SHA = "4fb1443d8e10b3abe74fc06d99e04356e940be38b57ed9de20b0fb65e46ae2d7"


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


# ── File existence ────────────────────────────────────────────────────────────

def test_v21_all_required_files_exist():
    for p in [PNG_PATH, PDF_PATH, MANIFEST_PATH, REPORT_PATH]:
        assert p.exists(), f"Missing: {p.name}"
        assert p.stat().st_size > 0, f"Empty: {p.name}"

    for fname in ["fig1_compact_v21.png", "fig3_compact_table_v21.png",
                  "fig4_compact_v21.png", "fig5_compact_v21.png"]:
        p = ASSETS_DIR / fname
        assert p.exists(), f"Missing compact asset: {fname}"
        assert p.stat().st_size > 0, f"Empty compact asset: {fname}"


# ── PDF page count ────────────────────────────────────────────────────────────

def test_v21_pdf_exactly_one_page():
    data = PDF_PATH.read_bytes()
    counts = re.findall(rb'/Count\s+(\d+)', data)
    assert int(counts[0]) == 1, f"PDF /Count = {counts[0]}, expected 1"
    page_types = re.findall(rb'/Type\s*/Page\b', data)
    assert len(page_types) == 1, f"/Type /Page count = {len(page_types)}, expected 1"


# ── Manifest structure ────────────────────────────────────────────────────────

def test_v21_manifest_structure():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    assert m["manifest_id"] == "math16_pilot02_one_pager_v21_manifest"
    assert m["page_count"] == 1
    assert m["layout_version"] == "v2.1_visual_hotfix"
    assert m["header_height_pct"] == 19
    assert m["fig3_style"] == "horizontal_mini_bars_table"


def test_v21_right_column_order():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    order = m["right_column_order"]
    assert "Fig1" in order[0]
    assert "Fig5" in order[1]
    assert "Fig3" in order[2]


# ── Core numbers ─────────────────────────────────────────────────────────────

def test_v21_manifest_core_numbers():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    pa = m["primary_posthoc_accounting"]
    assert "5 cells" in pa["qwen4b_primary_rescue"]
    assert "83/320" in pa["qwen4b_primary_rescue"]
    assert "6 cells" in pa["qwen4b_posthoc_rescue"]
    assert "84/320" in pa["qwen4b_posthoc_rescue"]
    assert pa["gemini_eligible"] == 0
    assert pa["qwen9b_eligible"] == 0
    assert pa["observed_regression"] == 0


def test_v21_manifest_statistics():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    ks = m["key_statistics"]
    assert ks["nine_b_only"] == 49
    assert ks["four_b_only"] == 26
    assert ks["exact_mcnemar_p"] == 0.010582
    assert "-0.94%" in ks["task_clustered_bootstrap_95ci"]
    assert "+14.38%" in ks["task_clustered_bootstrap_95ci"]


# ── SHA preservation guards ───────────────────────────────────────────────────

def test_original_source_figures_sha_preserved():
    for fname, expected in ORIG_SHAS.items():
        p = FIG_DIR / fname
        assert sha256(p) == expected, f"Original figure SHA changed: {fname}"


def test_v1_and_v2_files_not_modified():
    assert sha256(V1_DIR / "math16_pilot02_one_pager_v1.png") == V1_PNG_SHA
    assert sha256(V1_DIR / "math16_pilot02_one_pager_v1.pdf") == V1_PDF_SHA
    assert sha256(V2_DIR / "math16_pilot02_one_pager_v2.png") == V2_PNG_SHA
    assert sha256(V2_DIR / "math16_pilot02_one_pager_v2.pdf") == V2_PDF_SHA


# ── No forbidden outputs ──────────────────────────────────────────────────────

def test_no_poster_or_oral_slides_in_v21():
    forbidden = ["poster", "oral", ".pptx", ".ppt"]
    for p in V21_DIR.rglob("*"):
        if p.is_file():
            for pat in forbidden:
                assert pat not in p.name.lower(), f"Forbidden: {p.name}"


def test_evidence_complete_not_modified():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)
    recorded = m["input_milestone_sha256"]
    assert sha256(CLAIMS_PATH) == recorded, "frozen_numeric_claims.json modified!"
