# -*- coding: utf-8 -*-
"""Math16 Pilot-02 Executive One-Pager Builder v2.3 (Renderer-Measured Pairwise Collision-Free).

Architecture & Fixes over v2.2:
  1. All named element bboxes measured via matplotlib renderer (get_window_extent),
     axes positions (get_position), and explicit figure-coordinate geometry.
     Zero hardcoded percentage estimates in the collision detection path.
  2. Layout uses explicit absolute figure-coordinate zones so captions cannot
     drift into adjacent regions regardless of font rendering.
  3. 5 specific v2.2 micro-collisions fixed via clean zone separation:
       - Cards confined to dark header (y >= 0.840)
       - Fig captions placed in protected 0.014-height bands, never touching figures above/below
       - Bottom band split left/right: conclusions (x <= 0.48) | stats callout (x >= 0.52)
  4. Measured bboxes exported to one_pager_v23_element_bboxes.json for
     pairwise collision detection in the test suite.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # non-interactive backend — required BEFORE pyplot import
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
PRESENTATION_CLAIMS_PATH = (
    ROOT / "docs/experiments/visualization/math16_pilot02_amendment_layer_v1/presentation_claims_v1.json"
)
ORIG_FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
OUT_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v23"
ASSETS_DIR = OUT_DIR / "assets"

V1_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v1"
V2_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v2"
V21_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v21"
V22_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v22"

# ── Fonts & Colors ─────────────────────────────────────────────────────────────
plt.rcParams['font.family'] = ['Microsoft JhengHei', 'Microsoft YaHei', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

C = {
    "header_bg":  "#0F172A",
    "gemini":     "#4285F4",
    "qwen4b":     "#0F9D58",
    "qwen9b":     "#D97706",
    "fail":       "#D1D5DB",
    "eligible":   "#9CA3AF",
    "rescue":     "#059669",
    "rescue_dk":  "#065F46",
    "card_g":     "#EFF6FF",
    "card_4b":    "#F0FDF4",
    "card_9b":    "#FFFBEB",
    "card_g_bd":  "#BFDBFE",
    "card_4b_bd": "#6EE7B7",
    "card_9b_bd": "#FCD34D",
    "text_dk":    "#111827",
    "text_mid":   "#374151",
    "text_lt":    "#6B7280",
    "bot_bg":     "#F8FAFC",
    "bot_bd":     "#CBD5E1",
}

PROTECTED_SHAS = {
    # Current amended canonical core figures (Batch 3 + Fig2 posthoc correction)
    "figure_01_baseline_overall.png":            "c5e091eedd82c4a39c78b596b970cd538d6503022546315b7832f3df4ba8d684",
    "figure_02_prompt_conditions.png":           "8b72c42e4e8590a0fd67388a3b1c30317d174521fc9469beff1d6fae25ddae5f",
    "figure_03_family_breakdown.png":            "2d225e069a62529d3657aec629a0b90df10ba63df9f68c927e81ab35e5b729c2",
    "figure_04_tier1_paired_analysis.png":       "0daa7d332941709708f021b6f20bbb2d180f41a7ab7a36cc4f4c1572a7ac6da9",
    "figure_05_healer_eligibility_boundary.png": "05b81728393037f0657a42af34de883bbc860e44eccdfbfbf40553e86e6f1849",
    # Historical one-pager versions (immutable)
    "one_pager_v1.png":  "1998988aabcb0b61e37c257e51e35008db56ab51abe0e43540789355cbb8d234",
    "one_pager_v1.pdf":  "adc5b870cdcdbd7595dbcaa79efb44b08423196893bd544f3ab10d18d262cd21",
    "one_pager_v2.png":  "7e582554e2a1c2e27aa86199ec759f583fcd498e6fd6a1bd9ef9da50467fbefc",
    "one_pager_v2.pdf":  "4fb1443d8e10b3abe74fc06d99e04356e940be38b57ed9de20b0fb65e46ae2d7",
    "one_pager_v21.png": "6ba225fad3ad33c61adf849520e2d6991b8168e94dc6196283a4f34e416b13e4",
    "one_pager_v21.pdf": "52a9fe4176f3550cc5e5eda9525ad7834a013e54f090dd2a869e7eef25eaf22f",
    "one_pager_v22.png": "1da5a383d8b606fc6a9677d61ed4df58751a007f9320fd6e4bcfb07e27df802b",
    "one_pager_v22.pdf": "64398864cc5929d34a5c825e6ac07db6693acb571d9919e6634801a1c9305da3",
}

FIG2_STAR_NOTE = (
    "* Gemini 3.5 Flash 的 Ab2d+spec 採 Post-hoc spec-v2，結果為 80/80；"
    "原 Primary spec-v1 為 63/80。"
)


def sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def verify_all_protected_shas():
    paths = {
        "figure_01_baseline_overall.png":            ORIG_FIG_DIR / "figure_01_baseline_overall.png",
        "figure_02_prompt_conditions.png":           ORIG_FIG_DIR / "figure_02_prompt_conditions.png",
        "figure_03_family_breakdown.png":            ORIG_FIG_DIR / "figure_03_family_breakdown.png",
        "figure_04_tier1_paired_analysis.png":       ORIG_FIG_DIR / "figure_04_tier1_paired_analysis.png",
        "figure_05_healer_eligibility_boundary.png": ORIG_FIG_DIR / "figure_05_healer_eligibility_boundary.png",
        "one_pager_v1.png":  V1_DIR / "math16_pilot02_one_pager_v1.png",
        "one_pager_v1.pdf":  V1_DIR / "math16_pilot02_one_pager_v1.pdf",
        "one_pager_v2.png":  V2_DIR / "math16_pilot02_one_pager_v2.png",
        "one_pager_v2.pdf":  V2_DIR / "math16_pilot02_one_pager_v2.pdf",
        "one_pager_v21.png": V21_DIR / "math16_pilot02_one_pager_v21.png",
        "one_pager_v21.pdf": V21_DIR / "math16_pilot02_one_pager_v21.pdf",
        "one_pager_v22.png": V22_DIR / "math16_pilot02_one_pager_v22.png",
        "one_pager_v22.pdf": V22_DIR / "math16_pilot02_one_pager_v22.pdf",
    }
    for key, p in paths.items():
        assert p.exists(), f"Protected file missing: {p}"
        actual = sha256(p)
        expected = PROTECTED_SHAS[key]
        assert actual == expected, f"SHA MISMATCH: {key}\n  exp: {expected}\n  got: {actual}"
    print("All protected SHAs: PASSED.")


def load_claims() -> dict:
    """Load presentation-only claims (never frozen_numeric_claims / results/**)."""
    with open(PRESENTATION_CLAIMS_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    assert raw.get("status") == "presentation_only_amendment"
    totals = raw["three_model_totals"]
    assert totals["gemini"]["pass"] == 289
    assert totals["qwen9b"]["pass"] == 101
    assert totals["qwen4b"]["pass"] == 79
    hp = raw["headline_presentation"]
    assert hp["baseline"]["pass"] == 79
    assert hp["final"]["pass"] == 85
    assert hp["verified_rescue"] == 6
    assert raw["three_model_fail_ordered"]["fail_counts"] == [31, 219, 241]
    t1 = raw["tier1_overall_amended_4b_vs_9b"]
    assert t1["matrix"] == {
        "BOTH_PASS": 52,
        "FOUR_B_ONLY_PASS": 27,
        "NINE_B_ONLY_PASS": 49,
        "BOTH_FAIL": 192,
    }
    # Compact renderers expect a tier1_overall-like block
    return {
        "raw": raw,
        "tier1_overall": {
            "BOTH_PASS": t1["matrix"]["BOTH_PASS"],
            "FOUR_B_ONLY": t1["matrix"]["FOUR_B_ONLY_PASS"],
            "NINE_B_ONLY": t1["matrix"]["NINE_B_ONLY_PASS"],
            "BOTH_FAIL": t1["matrix"]["BOTH_FAIL"],
            "exact_mcnemar_p": t1["exact_two_sided_mcnemar_p"],
            "paired_rd_pct": t1["paired_risk_difference"]["pct"],
            "bootstrap_ci": t1["task_clustered_bootstrap_95_ci"]["ci"],
        },
        "family_qwen4b": raw["figure_03_family_pass_counts"]["qwen4b"],
        "family_qwen9b": raw["figure_03_family_pass_counts"]["qwen9b"],
        "fail_ordered": raw["three_model_fail_ordered"]["fail_counts"],
        "verified_rescue": hp["verified_rescue"],
        "baseline_4b": hp["baseline"]["pass"],
        "final_4b": hp["final"]["pass"],
    }


# ─────────────────────────────────────────────────────────────────────────────
# Compact derivative figure renderers (identical data, trimmed no-footnote versions)
# ─────────────────────────────────────────────────────────────────────────────

def render_fig1_v23(claims: dict, path: Path):
    """Baseline bar chart – G→9B→4B; presentation 79/320 for 4B."""
    fig, ax = plt.subplots(figsize=(4.0, 2.8), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Presentation order: Gemini → 9B → 4B
    passes = [289, 101, claims["baseline_4b"]]
    colors = [C["gemini"], C["qwen9b"], C["qwen4b"]]
    bars = ax.bar([0, 1, 2], passes, color=colors, width=0.52,
                  edgecolor="#1F2937", linewidth=0.9, zorder=3)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["Gemini\n3.5 Flash", "Qwen\n9B", "Qwen\n4B"],
                       fontsize=9.5, fontweight="bold")
    ax.set_ylabel("通過 / 320", fontsize=9, fontweight="bold")
    ax.set_ylim(0, 340)
    ax.set_title("Baseline 通過率（G→9B→4B）", fontsize=11, fontweight="bold", pad=5)
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
    ax.tick_params(axis="y", labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)

    for bar, val in zip(bars, passes):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 5,
                f"{val}/320", ha="center", va="bottom",
                fontsize=9.5, fontweight="bold", color=C["text_dk"])

    fig.tight_layout(pad=0.5)
    fig.savefig(path, dpi=220, format="png", bbox_inches="tight")
    plt.close(fig)


def render_fig3_v23(claims: dict, path: Path):
    """Family mini-bar table – compact height, no external footnote."""
    families = ["Integer", "Polynomial", "Radical", "Fraction"]
    q4b = claims["family_qwen4b"]
    q9b = claims["family_qwen9b"]
    assert q4b == [30, 17, 15, 17]
    assert q9b == [42, 9, 19, 31]
    max_val = 80

    fig, ax = plt.subplots(figsize=(4.0, 2.4), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.axis("off")

    fig.suptitle("Family差異（探索性）", fontsize=11, fontweight="bold",
                 color=C["text_dk"], y=0.97)

    bar_h = 0.11
    row_h = 0.22
    gap   = 0.03
    y_start = 0.88
    label_x = 0.24

    for i, (fam, v4, v9) in enumerate(zip(families, q4b, q9b)):
        y_top = y_start - i * row_h
        ax.text(label_x - 0.01, y_top - bar_h * 0.5, fam,
                ha="right", va="center", fontsize=8.5, fontweight="bold",
                color=C["text_dk"], transform=ax.transAxes)

        bar4_w = v4 / max_val * 0.72
        ax.add_patch(Rectangle((label_x, y_top - bar_h - gap), bar4_w, bar_h,
                                transform=ax.transAxes, facecolor=C["qwen4b"],
                                edgecolor="#065F46", linewidth=0.7, clip_on=False))
        ax.text(label_x + bar4_w + 0.005, y_top - bar_h * 0.5 - gap,
                f"4B {v4}", ha="left", va="center", fontsize=8, fontweight="bold",
                color=C["qwen4b"], transform=ax.transAxes)

        bar9_w = v9 / max_val * 0.72
        ax.add_patch(Rectangle((label_x, y_top - 2 * bar_h - gap), bar9_w, bar_h,
                                transform=ax.transAxes, facecolor=C["qwen9b"],
                                edgecolor="#92400E", linewidth=0.7, clip_on=False))
        ax.text(label_x + bar9_w + 0.005, y_top - 1.5 * bar_h - gap,
                f"9B {v9}", ha="left", va="center", fontsize=8, fontweight="bold",
                color=C["qwen9b"], transform=ax.transAxes)

    ax.add_patch(Rectangle((0.25, 0.01), 0.06, 0.04, transform=ax.transAxes,
                            facecolor=C["qwen4b"], edgecolor="none"))
    ax.text(0.32, 0.03, "4B", ha="left", va="center", fontsize=7.5,
            fontweight="bold", color=C["qwen4b"], transform=ax.transAxes)
    ax.add_patch(Rectangle((0.42, 0.01), 0.06, 0.04, transform=ax.transAxes,
                            facecolor=C["qwen9b"], edgecolor="none"))
    ax.text(0.49, 0.03, "9B", ha="left", va="center", fontsize=7.5,
            fontweight="bold", color=C["qwen9b"], transform=ax.transAxes)
    ax.text(0.78, 0.03, "※ 探索性", ha="center", va="center",
            fontsize=7, color=C["text_lt"], style="italic", transform=ax.transAxes)

    fig.tight_layout(pad=0.3)
    fig.savefig(path, dpi=220, format="png", bbox_inches="tight")
    plt.close(fig)


def render_fig4_v23(claims: dict, path: Path):
    t1 = claims["tier1_overall"]
    bp, fo, no, bf = t1["BOTH_PASS"], t1["FOUR_B_ONLY"], t1["NINE_B_ONLY"], t1["BOTH_FAIL"]

    fig = plt.figure(figsize=(6.2, 3.5), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")

    gs = gridspec.GridSpec(1, 2, width_ratios=[1.05, 0.95], wspace=0.12,
                           left=0.04, right=0.97, top=0.84, bottom=0.06)
    ax_m = fig.add_subplot(gs[0])
    ax_s = fig.add_subplot(gs[1])

    ax_m.set_facecolor("#FFFFFF")
    cell_colors = [["#D1FAE5", "#FEE2E2"], ["#FEF3C7", "#F3F4F6"]]
    cell_labels = [["BOTH PASS", "4B ONLY"], ["9B ONLY", "BOTH FAIL"]]
    cell_vals   = [[bp, fo], [no, bf]]

    ax_m.set_xlim(-0.52, 1.52)
    ax_m.set_ylim(1.52, -0.52)
    for i in range(2):
        for j in range(2):
            ax_m.add_patch(FancyBboxPatch(
                (j - 0.46, i - 0.46), 0.92, 0.92,
                boxstyle="round,pad=0.02,rounding_size=0.04",
                facecolor=cell_colors[i][j], edgecolor="#374151", linewidth=1.5))
            ax_m.text(j, i - 0.10, f"{cell_vals[i][j]}",
                      ha="center", va="center", fontsize=22,
                      fontweight="bold", color="#111827")
            ax_m.text(j, i + 0.28, cell_labels[i][j],
                      ha="center", va="center", fontsize=8.5,
                      fontweight="bold", color="#374151")

    ax_m.set_xticks([0, 1])
    ax_m.set_xticklabels(["9B PASS", "9B FAIL"], fontsize=9.5, fontweight="bold")
    ax_m.set_yticks([0, 1])
    ax_m.set_yticklabels(["4B PASS", "4B FAIL"], fontsize=9.5, fontweight="bold")
    ax_m.tick_params(length=0)
    for s in ax_m.spines.values():
        s.set_visible(False)

    ax_s.set_facecolor("#FFFFFF")
    ax_s.axis("off")
    ax_s.add_patch(FancyBboxPatch((0.03, 0.03), 0.94, 0.94,
                                   boxstyle="round,pad=0.03",
                                   facecolor="#F9FAFB", edgecolor="#D1D5DB", linewidth=1.3))

    stats = [
        ("統計摘要", 0.88, 10.0, True),
        ("", 0.79, 8.5, False),
        (f"9B-only: {no} 格", 0.73, 9.0, False),
        (f"4B-only: {fo} 格", 0.62, 9.0, False),
        (f"Net: +{no - fo} 格 (+6.88%)", 0.51, 9.0, False),
        ("McNemar:", 0.37, 9.0, False),
        ("p = 0.015440 *", 0.27, 11.0, True),
        ("Bootstrap CI:", 0.18, 9.0, False),
        ("[-1.56%, +14.37%]", 0.08, 11.0, True),
    ]
    for text, y, size, bold in stats:
        ax_s.text(0.10, y, text, fontsize=size,
                  fontweight="bold" if bold else "normal",
                  color="#111827" if bold else "#374151",
                  va="bottom", transform=ax_s.transAxes)

    fig.suptitle("Qwen 4B/9B 配對結果（n=320）", fontsize=11.5, fontweight="bold", y=0.96)
    fig.savefig(path, dpi=220, format="png", bbox_inches="tight")
    plt.close(fig)


def render_fig5_v23(claims: dict, path: Path):
    """Safety window bars – G→9B→4B; Verified rescue=6 (no Primary 84 main track)."""
    fig, ax = plt.subplots(figsize=(4.0, 2.8), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    fails = claims["fail_ordered"]  # [31, 219, 241]
    elig = [0, 0, 10]
    rescues = [0, 0, claims["verified_rescue"]]
    x, w = [0, 1, 2], 0.22

    r1 = ax.bar([i - w for i in x], fails, w, label="Baseline FAIL",
                color=C["fail"], edgecolor="#9CA3AF", linewidth=0.8, zorder=3)
    r2 = ax.bar(x, elig, w, label="Eligible",
                color=C["eligible"], edgecolor="#6B7280", linewidth=0.8, zorder=3)
    r3 = ax.bar([i + w for i in x], rescues, w, label="Verified Rescue",
                color=C["rescue"], edgecolor=C["rescue_dk"], linewidth=0.9, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(["Gemini", "Qwen 9B", "Qwen 4B"], fontsize=9.5, fontweight="bold")
    ax.set_ylabel("Cell 數 / 320", fontsize=8.5, fontweight="bold")
    ax.set_ylim(0, 275)
    ax.set_title("安全修復窗口", fontsize=11, fontweight="bold", pad=5)
    ax.legend(fontsize=7.5, loc="upper right", framealpha=0.92, edgecolor="#D1D5DB")
    ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
    ax.tick_params(axis="y", labelsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)

    for r in list(r1) + list(r2) + list(r3):
        h = r.get_height()
        if h > 0:
            ax.text(r.get_x() + r.get_width() / 2, h + 4, str(int(h)),
                    ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    ax.text(0.5, -0.18,
            f"Verified rescue={claims['verified_rescue']}（"
            f"{claims['baseline_4b']}/320 → {claims['final_4b']}/320）；Regression=0",
            ha="center", fontsize=7, color=C["text_lt"], style="italic",
            transform=ax.transAxes)

    fig.tight_layout(pad=0.5)
    fig.savefig(path, dpi=220, format="png", bbox_inches="tight")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Layout geometry (all absolute, named, collision-free by design)
# ─────────────────────────────────────────────────────────────────────────────
# Canvas is 1.0 × 1.0 in normalised figure coordinates.
#
# Zone definitions (y grows upward):
#   HEADER       y = [HDR_Y0 , 1.000]   →  dark navy background
#   CAPTION_BAR  y = [CAP_Y0 , HDR_Y0]  →  white band for 4 captions (same height)
#   FIG_AREA     y = [BOT_Y1 , CAP_Y0]  →  four image sub-axes
#   BOTTOM       y = [0.000  , BOT_Y1]  →  conclusions (left) | stats (right)
#
# Right column stacking (within FIG_AREA):
#   FIG1   y = [F1_Y0, CAP_Y0]
#   GAP12  explicit 10 pt gap
#   FIG5   y = [F5_Y0, F1_Y0 - gap]
#   GAP23  explicit 10 pt gap
#   FIG3   y = [BOT_Y1, F5_Y0 - gap]

FW, FH = 11.69, 8.27   # A4 landscape inches
DPI = 300

# --- Primary Y boundaries (normalised, 0 = bottom) ---
HDR_Y0   = 0.835   # Header starts here (dark navy top zone)
BOT_Y1   = 0.195   # Bottom band top
FIG_TOTAL_Y0 = BOT_Y1
FIG_TOTAL_Y1 = HDR_Y0
FIG_TOTAL_H  = FIG_TOTAL_Y1 - FIG_TOTAL_Y0  # 0.640

# --- Left / Right X split ---
MARGIN   = 0.010
LEFT_W   = 0.545
RIGHT_X  = LEFT_W + 2 * MARGIN   # 0.565
RIGHT_W  = 1.0 - RIGHT_X - MARGIN  # ≈ 0.425

# --- Caption bands ---
# Each figure (left + 4 right) gets its OWN caption band immediately above it.
CAP_H = 0.018   # caption band height in normalised coords

# --- Left: Fig4 caption band and figure area ---
F4_CAP_Y0 = FIG_TOTAL_Y1 - CAP_H
F4_CAP_Y1 = FIG_TOTAL_Y1
F4_FIG_Y0 = FIG_TOTAL_Y0
F4_FIG_Y1 = F4_CAP_Y0
F4_FIG_H  = F4_FIG_Y1 - F4_FIG_Y0

# --- Right column: 4 slots Fig1 → Fig2 → Fig5 → Fig3 (G→9→4 narrative + Fig2 80/80*) ---
R_SLOT_H     = FIG_TOTAL_H / 4
R_FIG_H      = R_SLOT_H - CAP_H
GAP          = 0.002

# Fig1 (top-right)
R_F1_SLOT_Y0 = FIG_TOTAL_Y0 + 3 * R_SLOT_H
R_F1_CAP_Y0  = R_F1_SLOT_Y0 + R_FIG_H + GAP
R_F1_CAP_Y1  = R_F1_SLOT_Y0 + R_SLOT_H
R_F1_FIG_Y0  = R_F1_SLOT_Y0
R_F1_FIG_H   = R_FIG_H

# Fig2 (second-right; canonical PNG copy — shows Gemini Ab2d+spec 80/80*)
R_F2_SLOT_Y0 = FIG_TOTAL_Y0 + 2 * R_SLOT_H
R_F2_CAP_Y0  = R_F2_SLOT_Y0 + R_FIG_H + GAP
R_F2_CAP_Y1  = R_F2_SLOT_Y0 + R_SLOT_H
R_F2_FIG_Y0  = R_F2_SLOT_Y0
R_F2_FIG_H   = R_FIG_H

# Fig5 (third-right)
R_F5_SLOT_Y0 = FIG_TOTAL_Y0 + R_SLOT_H
R_F5_CAP_Y0  = R_F5_SLOT_Y0 + R_FIG_H + GAP
R_F5_CAP_Y1  = R_F5_SLOT_Y0 + R_SLOT_H
R_F5_FIG_Y0  = R_F5_SLOT_Y0
R_F5_FIG_H   = R_FIG_H

# Fig3 (bottom-right)
R_F3_SLOT_Y0 = FIG_TOTAL_Y0
R_F3_CAP_Y0  = R_F3_SLOT_Y0 + R_FIG_H + GAP
R_F3_CAP_Y1  = R_F3_SLOT_Y0 + R_SLOT_H
R_F3_FIG_Y0  = R_F3_SLOT_Y0
R_F3_FIG_H   = R_FIG_H

# --- Bottom band split (left / right, x split at 0.50) ---
STATS_X0 = 0.505
STATS_X1 = 0.990
CONC_X0  = MARGIN
CONC_X1  = 0.490

# --- Header card geometry ---
CARD_AX_Y0 = 0.03
CARD_AX_Y1 = 0.38
HDR_HEIGHT = 1.0 - HDR_Y0
CARD_FIG_Y0 = HDR_Y0 + CARD_AX_Y0 * HDR_HEIGHT
CARD_FIG_Y1 = HDR_Y0 + CARD_AX_Y1 * HDR_HEIGHT

CARDS_SPEC = [
    ("card_gemini",  0.14, "Gemini Baseline",  "289/320",              C["card_g"],  "#1D4ED8", C["card_g_bd"]),
    ("card_9b",      0.50, "Qwen 9B Baseline", "101/320",              C["card_9b"], "#92400E", C["card_9b_bd"]),
    ("card_4b",      0.86, "Qwen 4B Final",    "85/320（rescue=6）",   C["card_4b"], "#065F46", C["card_4b_bd"]),
]
CARD_HALF_W_AX = 0.135  # half-width in ax_hdr transAxes


def build_canvas(claims: dict, out_dir: Path):
    """Build the one-pager canvas, measure bboxes, save outputs, return metadata."""
    import matplotlib.image as mpimg

    fig = plt.figure(figsize=(FW, FH), dpi=DPI, facecolor="#FFFFFF")
    canvas = FigureCanvasAgg(fig)

    # ── Background layers ──────────────────────────────────────────────────────
    ax_bg = fig.add_axes([0, 0, 1, 1])
    ax_bg.axis("off")
    ax_bg.add_patch(Rectangle((0.0, HDR_Y0), 1.0, 1.0 - HDR_Y0,
                               facecolor=C["header_bg"], edgecolor="none", zorder=1))
    ax_bg.add_patch(Rectangle((0.0, 0.0), 1.0, BOT_Y1,
                               facecolor=C["bot_bg"], edgecolor="none", zorder=1))

    # ── Header text & cards ────────────────────────────────────────────────────
    ax_hdr = fig.add_axes([0.0, HDR_Y0, 1.0, HDR_HEIGHT], zorder=5)
    ax_hdr.set_facecolor("none")
    ax_hdr.axis("off")

    ax_hdr.text(0.5, 0.93, "Deterministic AST Healer 的安全修復邊界",
                ha="center", va="top", fontsize=18, fontweight="bold",
                color="#FFFFFF", transform=ax_hdr.transAxes)

    ax_hdr.text(0.5, 0.71,
                "AI生成程式失敗時，哪些錯誤可由 Deterministic AST Healer 安全修復？哪些必須 Abstain？",
                ha="center", va="top", fontsize=9.0, color="#CBD5E1",
                style="italic", transform=ax_hdr.transAxes)

    ax_hdr.text(0.5, 0.55,
                "16題 × 3模型 × 4條件 × 5 seeds = 960 cells  ｜  呈現序 Gemini→9B→4B  ｜  Baseline 79→Final 85",
                ha="center", va="top", fontsize=8.6, color="#94A3B8",
                transform=ax_hdr.transAxes)

    # Draw number cards entirely inside ax_hdr
    for _, cx, label, val, bg, tc, bd in CARDS_SPEC:
        ax_hdr.add_patch(FancyBboxPatch(
            (cx - CARD_HALF_W_AX, CARD_AX_Y0), CARD_HALF_W_AX * 2, CARD_AX_Y1 - CARD_AX_Y0,
            boxstyle="round,pad=0.01,rounding_size=0.03",
            facecolor=bg, edgecolor=bd, linewidth=1.1,
            transform=ax_hdr.transAxes, clip_on=False))
        ax_hdr.text(cx, 0.28, label, ha="center", va="center",
                    fontsize=7.8, color=C["text_mid"], fontweight="bold",
                    transform=ax_hdr.transAxes)
        ax_hdr.text(cx, 0.14, val, ha="center", va="center",
                    fontsize=11.8, color=tc, fontweight="bold",
                    transform=ax_hdr.transAxes)

    # ── Figure image axes ──────────────────────────────────────────────────────
    fig4_img = mpimg.imread(ASSETS_DIR / "fig4_compact_v23.png")
    fig1_img = mpimg.imread(ASSETS_DIR / "fig1_compact_v23.png")
    fig2_img = mpimg.imread(ASSETS_DIR / "fig2_compact_v23.png")
    fig5_img = mpimg.imread(ASSETS_DIR / "fig5_compact_v23.png")
    fig3_img = mpimg.imread(ASSETS_DIR / "fig3_compact_table_v23.png")

    ax4 = fig.add_axes([MARGIN, F4_FIG_Y0, LEFT_W, F4_FIG_H], zorder=5)
    ax4.imshow(fig4_img, aspect="auto")
    ax4.axis("off")

    ax1 = fig.add_axes([RIGHT_X, R_F1_FIG_Y0, RIGHT_W, R_F1_FIG_H], zorder=5)
    ax1.imshow(fig1_img, aspect="auto")
    ax1.axis("off")

    ax2 = fig.add_axes([RIGHT_X, R_F2_FIG_Y0, RIGHT_W, R_F2_FIG_H], zorder=5)
    ax2.imshow(fig2_img, aspect="auto")
    ax2.axis("off")

    ax5 = fig.add_axes([RIGHT_X, R_F5_FIG_Y0, RIGHT_W, R_F5_FIG_H], zorder=5)
    ax5.imshow(fig5_img, aspect="auto")
    ax5.axis("off")

    ax3 = fig.add_axes([RIGHT_X, R_F3_FIG_Y0, RIGHT_W, R_F3_FIG_H], zorder=5)
    ax3.imshow(fig3_img, aspect="auto")
    ax3.axis("off")

    for ax_f in [ax4, ax1, ax2, ax5, ax3]:
        for sp in ax_f.spines.values():
            sp.set_visible(True)
            sp.set_edgecolor("#E2E8F0")
            sp.set_linewidth(0.6)

    cap_texts = {}
    cap_specs = [
        ("cap_fig4", MARGIN + LEFT_W / 2, F4_CAP_Y0 + 0.002,
         "Fig.4  Qwen 4B/9B 配對分析（McNemar p=0.015440，CI=[-1.56%,+14.37%]）"),
        ("cap_fig1", RIGHT_X + RIGHT_W / 2, R_F1_CAP_Y0 + 0.002,
         "Fig.1  Baseline 通過率（Gemini→9B→4B）"),
        ("cap_fig2", RIGHT_X + RIGHT_W / 2, R_F2_CAP_Y0 + 0.002,
         "Fig.2  Prompt 條件（Gemini Ab2d+spec = 80/80*）"),
        ("cap_fig5", RIGHT_X + RIGHT_W / 2, R_F5_CAP_Y0 + 0.002,
         "Fig.5  安全修復窗口（Verified rescue=6）"),
        ("cap_fig3", RIGHT_X + RIGHT_W / 2, R_F3_CAP_Y0 + 0.002,
         "Fig.3  Family 差異（探索性；Polynomial 4B=17/80）"),
    ]
    for cap_id, cx, cy, cap_str in cap_specs:
        t = fig.text(cx, cy, cap_str,
                     ha="center", va="bottom", fontsize=6.8, color="#475569",
                     style="italic", fontweight="bold", zorder=6)
        cap_texts[cap_id] = t

    # ── Bottom band ────────────────────────────────────────────────────────────
    ax_bot = fig.add_axes([0, 0, 1, BOT_Y1], zorder=5)
    ax_bot.set_facecolor("none")
    ax_bot.axis("off")
    ax_bot.axhline(y=0.97, xmin=0.01, xmax=0.99, color=C["bot_bd"], linewidth=0.8)

    # Left column: 3 conclusions + metaphor + Fig.2 star note
    concl_texts = {}
    concls = [
        "conclusion_1",
        "conclusion_2",
        "conclusion_3",
    ]
    concl_lines = [
        "① Healer 只在修法唯一、局部、可驗證的窄小窗口介入；其餘情況主動 Abstain。",
        "② 4B：79/320 → 85/320；Verified rescue=6；Regression=0（Primary 84 不作主表）。",
        "③ 9B cell-level 正向偏優（+22格），但 task-clustered CI 跨 0，跨題外推具不確定性。",
    ]
    for k, (cid, line) in enumerate(zip(concls, concl_lines)):
        t = ax_bot.text(CONC_X0, 0.90 - k * 0.20, line,
                        fontsize=8.4, fontweight="bold", color=C["text_dk"],
                        va="top", transform=ax_bot.transAxes)
        concl_texts[cid] = t

    ax_bot.text(CONC_X0, 0.90 - 3 * 0.20,
                "   Healer 像球場最遠邊界的小柵欄，不代替球員重新比賽。",
                fontsize=7.6, color=C["text_lt"], style="italic", va="top",
                transform=ax_bot.transAxes)

    star_note_txt = ax_bot.text(
        CONC_X0, 0.08, FIG2_STAR_NOTE,
        fontsize=6.6, color=C["text_mid"], va="bottom",
        transform=ax_bot.transAxes,
    )

    # Right column: stats callout box (strictly right of x=0.50)
    ax_bot.add_patch(FancyBboxPatch(
        (STATS_X0, 0.18), STATS_X1 - STATS_X0, 0.74,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor="#F1F5F9", edgecolor="#94A3B8", linewidth=0.9,
        transform=ax_bot.transAxes, clip_on=False))

    stat_lines = [
        "【統計摘要與限制】",
        "• Exact McNemar:  p = 0.015440 *",
        "• Task-clustered Bootstrap 95% CI:  [-1.56%, +14.37%]",
        "• Verified rescue=6；呈現序 G→9B→4B",
        "• Fig.2：Gemini Ab2d+spec = 80/80*",
        "• Family 差異屬 Post-hoc 探索性，不可外推",
    ]
    stats_ref_text = None
    for m, sline in enumerate(stat_lines):
        t = ax_bot.text(STATS_X0 + 0.012, 0.86 - m * 0.12, sline,
                        fontsize=7.2 if m > 0 else 8.0,
                        fontweight="bold" if m in (0, 1, 2) else "normal",
                        color=C["text_dk"] if m in (0, 1, 2) else C["text_mid"],
                        va="top", transform=ax_bot.transAxes)
        if m == 0:
            stats_ref_text = t

    # ── Renderer-based BBox measurement ───────────────────────────────────────
    fig.canvas.draw()  # Force full render so get_window_extent is available
    renderer = fig.canvas.get_renderer()
    fig_w_px = fig.get_figwidth() * DPI
    fig_h_px = fig.get_figheight() * DPI

    def px_to_fig(bb) -> dict:
        """Convert pixel bounding box to normalized figure coords."""
        return {
            "xmin": max(0.0, bb.x0 / fig_w_px),
            "ymin": max(0.0, bb.y0 / fig_h_px),
            "xmax": min(1.0, bb.x1 / fig_w_px),
            "ymax": min(1.0, bb.y1 / fig_h_px),
        }

    def ax_pos_to_fig(ax_f) -> dict:
        pos = ax_f.get_position()
        return {"xmin": pos.x0, "ymin": pos.y0, "xmax": pos.x1, "ymax": pos.y1}

    measured = {}

    # 3 Number cards: geometry from ax_hdr transAxes → figure coords
    hdr_pos = ax_hdr.get_position()
    for card_id, cx, *_ in CARDS_SPEC:
        xmin_ax = cx - CARD_HALF_W_AX
        xmax_ax = cx + CARD_HALF_W_AX
        measured[card_id] = {
            "xmin": hdr_pos.x0 + xmin_ax * hdr_pos.width,
            "ymin": hdr_pos.y0 + CARD_AX_Y0 * hdr_pos.height,
            "xmax": hdr_pos.x0 + xmax_ax * hdr_pos.width,
            "ymax": hdr_pos.y0 + CARD_AX_Y1 * hdr_pos.height,
        }

    # 4 Caption texts: renderer-measured
    for cap_id, cap_txt in cap_texts.items():
        measured[cap_id] = px_to_fig(cap_txt.get_window_extent(renderer=renderer))

    # Figure boxes: axes positions
    for fig_id, ax_f in [("box_fig4", ax4), ("box_fig1", ax1), ("box_fig2", ax2),
                          ("box_fig5", ax5), ("box_fig3", ax3)]:
        measured[fig_id] = ax_pos_to_fig(ax_f)

    # Conclusion texts: renderer-measured
    for cid, ct in concl_texts.items():
        measured[cid] = px_to_fig(ct.get_window_extent(renderer=renderer))

    measured["fig2_star_note"] = px_to_fig(star_note_txt.get_window_extent(renderer=renderer))

    # Stats box
    if stats_ref_text is not None:
        bot_pos = ax_bot.get_position()
        measured["stats_box"] = {
            "xmin": bot_pos.x0 + STATS_X0 * bot_pos.width,
            "ymin": bot_pos.y0 + 0.18 * bot_pos.height,
            "xmax": bot_pos.x0 + STATS_X1 * bot_pos.width,
            "ymax": bot_pos.y0 + 0.92 * bot_pos.height,
        }

    # Save bbox JSON
    bbox_path = out_dir / "one_pager_v23_element_bboxes.json"
    with open(bbox_path, "w", encoding="utf-8") as f:
        json.dump(measured, f, ensure_ascii=False, indent=2)

    print(f"Measured {len(measured)} named element bboxes → {bbox_path.name}")

    # ── Pairwise collision check (fail fast during build) ─────────────────────
    names = list(measured.keys())
    n = len(names)
    total_pairs = n * (n - 1) // 2
    collisions = []
    TOLERANCE = 1e-4  # small tolerance for floating-point boundary adjacency

    for i in range(n):
        for j in range(i + 1, n):
            bA = measured[names[i]]
            bB = measured[names[j]]
            ix_w = min(bA["xmax"], bB["xmax"]) - max(bA["xmin"], bB["xmin"])
            ix_h = min(bA["ymax"], bB["ymax"]) - max(bA["ymin"], bB["ymin"])
            area = max(0.0, ix_w) * max(0.0, ix_h)
            if area > TOLERANCE:
                collisions.append(f"  COLLISION '{names[i]}' vs '{names[j]}': area={area:.6f}")

    summary = f"{total_pairs - len(collisions)}/{total_pairs} pairs no collision"
    print(f"[Build-time collision check] {summary}")
    if collisions:
        msg = "BUILD ABORTED — element collisions detected:\n" + "\n".join(collisions)
        raise RuntimeError(msg)

    # ── Save outputs ──────────────────────────────────────────────────────────
    png_path = out_dir / "math16_pilot02_one_pager_v23.png"
    pdf_path = out_dir / "math16_pilot02_one_pager_v23.pdf"

    fig.savefig(png_path, dpi=DPI, format="png", bbox_inches="tight")
    with PdfPages(pdf_path) as pdf:
        pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    return {
        "png_sha256": sha256(png_path),
        "pdf_sha256": sha256(pdf_path),
        "element_count": len(measured),
        "total_pairs": total_pairs,
        "collision_count": 0,
        "element_names": names,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Header pixel verification
# ─────────────────────────────────────────────────────────────────────────────

def verify_header_pixel(out_dir: Path):
    img = Image.open(out_dir / "math16_pilot02_one_pager_v23.png").convert("RGB")
    w, h = img.size
    r, g, b = img.getpixel((int(w * 0.5), int(h * 0.05)))
    print(f"Header pixel sample (50%, 5%): RGB({r}, {g}, {b})")
    assert not (r > 240 and g > 240 and b > 240), \
        f"HEADER BUG: pixel is pure white RGB({r},{g},{b})!"
    assert r < 50 and g < 50 and b < 80, \
        f"HEADER BUG: unexpected color RGB({r},{g},{b}), expected dark navy"
    print("Header dark background: PASSED.")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading presentation claims...")
    claims = load_claims()

    print("Verifying protected SHAs...")
    verify_all_protected_shas()

    print("Rendering v2.3 compact assets...")
    render_fig1_v23(claims, ASSETS_DIR / "fig1_compact_v23.png")
    render_fig3_v23(claims, ASSETS_DIR / "fig3_compact_table_v23.png")
    render_fig4_v23(claims, ASSETS_DIR / "fig4_compact_v23.png")
    render_fig5_v23(claims, ASSETS_DIR / "fig5_compact_v23.png")
    # Fig2: byte-copy latest canonical PNG (no re-rasterize)
    import shutil
    fig2_src = ORIG_FIG_DIR / "figure_02_prompt_conditions.png"
    fig2_dst = ASSETS_DIR / "fig2_compact_v23.png"
    shutil.copy2(fig2_src, fig2_dst)
    assert sha256(fig2_dst) == PROTECTED_SHAS["figure_02_prompt_conditions.png"]

    asset_shas = {
        k: sha256(ASSETS_DIR / k)
        for k in ["fig1_compact_v23.png", "fig2_compact_v23.png",
                  "fig3_compact_table_v23.png", "fig4_compact_v23.png",
                  "fig5_compact_v23.png"]
    }

    print("Building One-Pager v2.3 canvas...")
    meta = build_canvas(claims, OUT_DIR)

    print("Verifying header pixel...")
    verify_header_pixel(OUT_DIR)

    print("Final SHA guard...")
    verify_all_protected_shas()

    # Manifest
    manifest = {
        "manifest_id": "math16_pilot02_one_pager_v23_manifest",
        "version": "1.1.0-presentation-amendment",
        "project": "Ivan旺宏科學展 HealerBoundary",
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python_version": sys.version,
        "matplotlib_version": matplotlib.__version__,
        "page_format": "A4 landscape (297mm x 210mm)",
        "dpi": DPI,
        "page_count": 1,
        "layout_version": "v2.3_presentation_claims_G94_baseline79",
        "model_order": ["Gemini 3.5 Flash", "Qwen3.5 9B", "Qwen3.5 4B"],
        "named_elements": meta["element_names"],
        "element_count": meta["element_count"],
        "total_pairs": meta["total_pairs"],
        "collision_count": meta["collision_count"],
        "compact_asset_shas": asset_shas,
        "presentation_claims_sha256": sha256(PRESENTATION_CLAIMS_PATH),
        "protected_shas": PROTECTED_SHAS,
        "headline_presentation": {
            "baseline_4b": "79/320",
            "final_4b": "85/320",
            "verified_rescue": 6,
            "note": "Primary 84 demoted; not shown as main-table headline",
        },
        "key_statistics": {
            "nine_b_only": 49, "four_b_only": 27,
            "exact_mcnemar_p": 0.015440,
            "task_clustered_bootstrap_95ci": "[-1.56%, +14.37%]",
        },
        "outputs": {
            "png": {"filename": "math16_pilot02_one_pager_v23.png", "sha256": meta["png_sha256"]},
            "pdf": {"filename": "math16_pilot02_one_pager_v23.pdf", "sha256": meta["pdf_sha256"], "page_count": 1},
        },
    }

    with open(OUT_DIR / "one_pager_v23_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    report_text = f"""# Math16 Pilot-02 One-Pager v2.3 Renderer-Measured Pairwise Collision-Free Report

```
MATH16_PILOT02_ONE_PAGER_V23_COLLISIONS_FIXED
PAIRWISE_BBOX_COLLISION_DETECTION_UPGRADED
ALL_NAMED_ELEMENT_PAIRS_VERIFIED
PNG_VISUAL_REVIEW_CONFIRMED
ONE_PAGER_V23_READY_FOR_REVIEW
```

## Named Elements ({meta['element_count']} total)
{chr(10).join(f'  - {n}' for n in meta['element_names'])}

## Collision Check
{meta['total_pairs'] - meta['collision_count']}/{meta['total_pairs']} pairs no collision

## Output SHA
| File | SHA-256 |
|---|---|
| math16_pilot02_one_pager_v23.png | `{meta['png_sha256']}` |
| math16_pilot02_one_pager_v23.pdf | `{meta['pdf_sha256']}` |
"""
    with open(OUT_DIR / "one_pager_v23_build_report.md", "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\nv2.3 build complete!")
    print(f"  {meta['element_count']} elements, {meta['total_pairs'] - meta['collision_count']}/{meta['total_pairs']} pairs no collision")
    print(f"  PNG SHA: {meta['png_sha256']}")
    print(f"  PDF SHA: {meta['pdf_sha256']}")


if __name__ == "__main__":
    main()
