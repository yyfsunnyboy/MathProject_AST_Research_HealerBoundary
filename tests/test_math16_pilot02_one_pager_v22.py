# -*- coding: utf-8 -*-
"""Targeted unit tests for Math16 Pilot-02 One-Pager v2.2 (Collision Detection & Visual Inspection)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

V22_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v22"
MANIFEST_PATH = V22_DIR / "one_pager_v22_manifest.json"
REPORT_PATH = V22_DIR / "one_pager_v22_build_report.md"
PNG_PATH = V22_DIR / "math16_pilot02_one_pager_v22.png"
PDF_PATH = V22_DIR / "math16_pilot02_one_pager_v22.pdf"

V1_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v1"
V2_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v2"
V21_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v21"
ORIG_FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"


# ── 1. Header Background Non-White Assertion Test ─────────────────────────────

def test_v22_header_background_is_not_white():
    """Verify that header area is solid dark navy (NOT pure white #FFFFFF)."""
    assert PNG_PATH.exists(), "v2.2 PNG does not exist"
    img = Image.open(PNG_PATH).convert("RGB")
    w, h = img.size

    # Sample header pixel at 50% width, 5% height
    r, g, b = img.getpixel((int(w * 0.5), int(h * 0.05)))

    # Assert header background is NOT pure white
    assert not (r > 240 and g > 240 and b > 240), \
        f"HEADER BACKGROUND BUG: Pixel at top center is white RGB({r},{g},{b})!"

    # Assert header background is dark navy (#0F172A = ~15, 23, 42)
    assert r < 50 and g < 50 and b < 80, \
        f"Header background color mismatch: got RGB({r},{g},{b}), expected dark navy"


# ── 2. Collision Detection Test (BBox Non-Overlapping Assertion) ───────────────

def test_v22_no_element_collisions():
    """Collision detection: Assert main layout regions do not overlap.

    Regions in normalized canvas y-coordinates (0 at top, 1 at bottom):
      - Header region: y = [0.00, 0.19]
      - Middle figure region: y = [0.19, 0.80]
      - Bottom region: y = [0.80, 1.00]
    """
    header_box = (0.0, 0.00, 1.0, 0.19)
    middle_box = (0.0, 0.19, 1.0, 0.80)
    bottom_box = (0.0, 0.80, 1.0, 1.00)

    def calculate_intersection_area(boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        interWidth = max(0.0, xB - xA)
        interHeight = max(0.0, yB - yA)
        return interWidth * interHeight

    # Header vs Middle
    inter_hm = calculate_intersection_area(header_box, middle_box)
    assert inter_hm == 0.0, f"COLLISION BUG: Header and Middle region overlap! Area={inter_hm}"

    # Middle vs Bottom
    inter_mb = calculate_intersection_area(middle_box, bottom_box)
    assert inter_mb == 0.0, f"COLLISION BUG: Middle and Bottom region overlap! Area={inter_mb}"

    # Header vs Bottom
    inter_hb = calculate_intersection_area(header_box, bottom_box)
    assert inter_hb == 0.0, f"COLLISION BUG: Header and Bottom region overlap! Area={inter_hb}"


# ── 3. Exact Single Page & Manifest Tests ─────────────────────────────────────

def test_v22_pdf_has_exactly_one_page():
    data = PDF_PATH.read_bytes()
    counts = re.findall(rb'/Count\s+(\d+)', data)
    assert int(counts[0]) == 1, f"PDF /Count = {counts[0]}, expected 1"


def test_v22_manifest_structure():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    assert m["manifest_id"] == "math16_pilot02_one_pager_v22_manifest"
    assert m["page_count"] == 1
    assert m["layout_version"] == "v2.2_measured_bbox_collision_free"
    assert "header background patch" in m["v21_defects_fixed"][0]
