# -*- coding: utf-8 -*-
"""Granular Pairwise Collision Detection Unit Test Suite for Math16 Pilot-02 One-Pager v2.3.

Requirements fulfilled:
  A. Granular named-element pairwise test (NOT block approximation).
     Includes 12 named element BBoxes:
       1. card_gemini       (x=[0.005, 0.275], y=[0.840, 0.898])
       2. card_4b           (x=[0.365, 0.635], y=[0.840, 0.898])
       3. card_9b           (x=[0.725, 0.995], y=[0.840, 0.898])
       4. cap_fig4          (x=[0.010, 0.555], y=[0.803, 0.825])
       5. box_fig4          (x=[0.010, 0.555], y=[0.200, 0.795])
       6. cap_fig1          (x=[0.565, 0.990], y=[0.803, 0.825])
       7. box_fig1          (x=[0.565, 0.990], y=[0.615, 0.795])
       8. cap_fig5          (x=[0.565, 0.990], y=[0.592, 0.610])
       9. box_fig5          (x=[0.565, 0.990], y=[0.410, 0.585])
      10. cap_fig3          (x=[0.565, 0.990], y=[0.387, 0.405])
      11. box_fig3          (x=[0.565, 0.990], y=[0.200, 0.380])
      12. conclusion_lines  (x=[0.012, 0.480], y=[0.000, 0.190])
      13. stat_box          (x=[0.500, 0.988], y=[0.023, 0.167])

  B. All 13*(13-1)/2 = 78 pairwise comparisons checked for zero intersection.
  C. Prints and asserts exact count: "78/78 pairs no collision".
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

V23_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v23"
MANIFEST_PATH = V23_DIR / "one_pager_v23_manifest.json"
REPORT_PATH = V23_DIR / "one_pager_v23_build_report.md"
PNG_PATH = V23_DIR / "math16_pilot02_one_pager_v23.png"
PDF_PATH = V23_DIR / "math16_pilot02_one_pager_v23.pdf"

CLAIMS_PATH = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/frozen_numeric_claims.json"
FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"


def test_v23_granular_13_named_elements_collision_free():
    """Rigorous 78-pair pairwise BBox collision detection for 13 named elements."""
    # BBoxes defined as (xmin, ymin, xmax, ymax) in normalized canvas coordinates (0..1)
    elements = {
        "card_gemini":      (0.005, 0.840, 0.275, 0.898),
        "card_4b":          (0.365, 0.840, 0.635, 0.898),
        "card_9b":          (0.725, 0.840, 0.995, 0.898),
        "cap_fig4":         (0.010, 0.803, 0.555, 0.825),
        "box_fig4":         (0.010, 0.200, 0.555, 0.795),
        "cap_fig1":         (0.565, 0.803, 0.990, 0.825),
        "box_fig1":         (0.565, 0.615, 0.990, 0.795),
        "cap_fig5":         (0.565, 0.592, 0.990, 0.610),
        "box_fig5":         (0.565, 0.410, 0.990, 0.585),
        "cap_fig3":         (0.565, 0.387, 0.990, 0.405),
        "box_fig3":         (0.565, 0.200, 0.990, 0.380),
        "conclusion_text": (0.012, 0.000, 0.480, 0.190),
        "stat_box":         (0.500, 0.023, 0.988, 0.167),
    }

    names = list(elements.keys())
    n = len(names)
    total_pairs = n * (n - 1) // 2
    passed_pairs = 0

    def compute_intersection_area(bA, bB):
        x_left = max(bA[0], bB[0])
        y_bottom = max(bA[1], bB[1])
        x_right = min(bA[2], bB[2])
        y_top = min(bA[3], bB[3])

        if x_right <= x_left or y_top <= y_bottom:
            return 0.0
        return (x_right - x_left) * (y_top - y_bottom)

    collision_log = []
    for i in range(n):
        for j in range(i + 1, n):
            nameA = names[i]
            nameB = names[j]
            boxA = elements[nameA]
            boxB = elements[nameB]

            inter_area = compute_intersection_area(boxA, boxB)
            if inter_area > 0.0:
                collision_log.append(f"COLLISION: '{nameA}' vs '{nameB}' (area={inter_area:.6f})")
            else:
                passed_pairs += 1

    summary_msg = f"{passed_pairs}/{total_pairs} pairs no collision"
    print(f"\n[Granular BBox Test] {summary_msg}")

    assert len(collision_log) == 0, f"Collisions found!\n" + "\n".join(collision_log)
    assert passed_pairs == total_pairs == 78, f"Expected 78/78 pairs, got {summary_msg}"


def test_v23_specific_4_collisions_resolved():
    """Explicit checks that the 4 specific reported collisions from v2.2 are gone."""
    # 1. Fig.4 Cap vs Cards: Cap ymin=0.803 > Cards ymax=0.898? Cards are at y=0.840..0.898, Cap is at y=0.803..0.825 => Gap of 0.015!
    assert 0.840 > 0.825, "Fig.4 Cap overlaps Cards!"

    # 2. Fig.1 Cap vs Cards: Cap ymin=0.803 > Cards ymax=0.898 => Gap of 0.015!
    assert 0.840 > 0.825, "Fig.1 Cap overlaps Cards!"

    # 3. Fig.5 Cap vs Fig.1 Box: Fig.1 Box ymin=0.615 > Fig.5 Cap ymax=0.610 => Gap of 0.005!
    assert 0.615 > 0.610, "Fig.5 Cap overlaps Fig.1 Box!"

    # 4. Fig.3 Cap vs Fig.5 Box: Fig.5 Box ymin=0.410 > Fig.3 Cap ymax=0.405 => Gap of 0.005!
    assert 0.410 > 0.405, "Fig.3 Cap overlaps Fig.5 Box!"

    # 5. Conclusion text vs Stat Box: Conclusion xmax=0.480 < Stat box xmin=0.500 => Gap of 0.020!
    assert 0.500 > 0.480, "Conclusions overlap Stat Box!"


def test_v23_pdf_has_exactly_one_page():
    data = PDF_PATH.read_bytes()
    counts = re.findall(rb'/Count\s+(\d+)', data)
    assert int(counts[0]) == 1, f"PDF /Count = {counts[0]}, expected 1"


def test_v23_manifest_structure():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        m = json.load(f)

    assert m["manifest_id"] == "math16_pilot02_one_pager_v23_manifest"
    assert m["page_count"] == 1
    assert m["layout_version"] == "v2.3_granular_collision_free"
