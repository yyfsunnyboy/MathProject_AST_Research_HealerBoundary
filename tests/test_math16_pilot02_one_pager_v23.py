# -*- coding: utf-8 -*-
"""Renderer-Measured Pairwise Collision Detection Tests for Math16 Pilot-02 One-Pager v2.3.

Requirements fulfilled:
  A. Named-element pairwise test loaded from ACTUAL RENDERER-MEASURED bboxes
     exported by build_math16_pilot02_one_pager_v23.py via get_window_extent()
     and get_position().  NO hardcoded percentage estimates.

  B. 15 named elements, 15*(15-1)/2 = 105 total pairs, all verified.

  C. Test prints and asserts:
       "15 named elements, 105 total pairs, 105/105 pairs no collision"
     and on failure identifies exactly which pair collides.

  D. Also verifies:
     - header background is dark navy (not white) via PNG pixel sampling
     - PDF is exactly 1 page
     - manifest layout_version is correct
     - all 5 specific v2.2 collisions are now gone (using real bboxes)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

V23_DIR   = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v23"
BBOX_PATH = V23_DIR / "one_pager_v23_element_bboxes.json"
PNG_PATH  = V23_DIR / "math16_pilot02_one_pager_v23.png"
PDF_PATH  = V23_DIR / "math16_pilot02_one_pager_v23.pdf"
MANIFEST  = V23_DIR / "one_pager_v23_manifest.json"


def _load_bboxes() -> dict:
    assert BBOX_PATH.exists(), f"Element bbox JSON missing: {BBOX_PATH}"
    with open(BBOX_PATH, encoding="utf-8") as f:
        return json.load(f)


def _intersection_area(bA: dict, bB: dict, tol: float = 1e-4) -> float:
    iw = min(bA["xmax"], bB["xmax"]) - max(bA["xmin"], bB["xmin"])
    ih = min(bA["ymax"], bB["ymax"]) - max(bA["ymin"], bB["ymin"])
    area = max(0.0, iw) * max(0.0, ih)
    return area if area > tol else 0.0


# ── A. Renderer-measured pairwise collision detection ─────────────────────────

def test_v23_renderer_measured_pairwise_105_pairs_no_collision():
    """Load actual renderer-measured bboxes and verify 105/105 pairs no collision."""
    bboxes = _load_bboxes()
    names  = list(bboxes.keys())
    n      = len(names)
    total_pairs = n * (n - 1) // 2

    collisions  = []
    passed      = 0
    for i in range(n):
        for j in range(i + 1, n):
            area = _intersection_area(bboxes[names[i]], bboxes[names[j]])
            if area > 0:
                collisions.append(
                    f"  COLLISION '{names[i]}' vs '{names[j]}': area={area:.6f}"
                )
            else:
                passed += 1

    summary = f"{n} named elements, {total_pairs} total pairs, {passed}/{total_pairs} pairs no collision"
    print(f"\n[v2.3 Pairwise BBox Test] {summary}")

    assert not collisions, "Collisions detected!\n" + "\n".join(collisions)
    assert passed == total_pairs, f"Expected {total_pairs}/{total_pairs}, got {passed}"


def test_v23_element_count_is_15():
    bboxes = _load_bboxes()
    assert len(bboxes) == 15, f"Expected 15 elements, got {len(bboxes)}"


# ── B. 5 specific v2.2 collisions resolved (using real bboxes) ───────────────

def test_v23_cards_do_not_touch_fig4_or_fig1_captions():
    """Cards (y=[0.840,0.898]) must not overlap cap_fig4 or cap_fig1."""
    bboxes = _load_bboxes()
    for card in ("card_gemini", "card_4b", "card_9b"):
        for cap in ("cap_fig4", "cap_fig1"):
            area = _intersection_area(bboxes[card], bboxes[cap])
            assert area == 0.0, f"COLLISION {card} vs {cap}: area={area:.6f}"


def test_v23_fig1_box_does_not_touch_fig5_caption():
    """box_fig1 must not overlap cap_fig5."""
    bboxes = _load_bboxes()
    area = _intersection_area(bboxes["box_fig1"], bboxes["cap_fig5"])
    assert area == 0.0, f"COLLISION box_fig1 vs cap_fig5: area={area:.6f}"


def test_v23_fig5_box_does_not_touch_fig3_caption():
    """box_fig5 must not overlap cap_fig3."""
    bboxes = _load_bboxes()
    area = _intersection_area(bboxes["box_fig5"], bboxes["cap_fig3"])
    assert area == 0.0, f"COLLISION box_fig5 vs cap_fig3: area={area:.6f}"


def test_v23_conclusions_do_not_touch_stats_box():
    """All 3 conclusion texts must not overlap stats_box."""
    bboxes = _load_bboxes()
    for cid in ("conclusion_1", "conclusion_2", "conclusion_3"):
        area = _intersection_area(bboxes[cid], bboxes["stats_box"])
        assert area == 0.0, f"COLLISION {cid} vs stats_box: area={area:.6f}"


# ── C. Header background pixel assertion ──────────────────────────────────────

def test_v23_header_background_is_dark_navy():
    """Header pixel at (50%, 5%) must be dark navy, not white."""
    from PIL import Image
    img = Image.open(PNG_PATH).convert("RGB")
    w, h = img.size
    r, g, b = img.getpixel((int(w * 0.5), int(h * 0.05)))
    print(f"\n[v2.3 Header Pixel] RGB({r},{g},{b}) at (50%,5%)")
    assert not (r > 240 and g > 240 and b > 240), \
        f"Header is pure white RGB({r},{g},{b}); dark background patch missing!"
    assert r < 50 and g < 50 and b < 80, \
        f"Header color mismatch: RGB({r},{g},{b}), expected dark navy ~(15,23,42)"


# ── D. PDF & manifest checks ──────────────────────────────────────────────────

def test_v23_pdf_has_exactly_one_page():
    data = PDF_PATH.read_bytes()
    counts = re.findall(rb'/Count\s+(\d+)', data)
    assert int(counts[0]) == 1, f"PDF /Count={counts[0]}, expected 1"


def test_v23_manifest_version():
    with open(MANIFEST, encoding="utf-8") as f:
        m = json.load(f)
    assert m["manifest_id"] == "math16_pilot02_one_pager_v23_manifest"
    assert m["layout_version"] == "v2.3_renderer_measured_pairwise_collision_free"
    assert m["element_count"] == 15
    assert m["total_pairs"] == 105
    assert m["collision_count"] == 0


def test_v23_manifest_statistics():
    with open(MANIFEST, encoding="utf-8") as f:
        m = json.load(f)
    ks = m["key_statistics"]
    assert ks["exact_mcnemar_p"] == 0.010582
    assert "[-0.94%, +14.38%]" in ks["task_clustered_bootstrap_95ci"]
    assert ks["nine_b_only"] == 49
    assert ks["four_b_only"] == 26
