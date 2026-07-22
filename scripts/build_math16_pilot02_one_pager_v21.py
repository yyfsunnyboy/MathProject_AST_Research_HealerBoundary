# -*- coding: utf-8 -*-
"""Math16 Pilot-02 Executive One-Pager Builder v2.1 (Visual Hotfix).

v2.1 fixes over v2:
  1. Title: solid dark header bar, white bold title, high contrast.
  2. Whitespace: header height reduced to ~19%, all content shifted up.
  3. Right column: Fig1 top, Fig5 middle, Fig3-compact-table bottom.
     Fig1 and Fig5 taller bands with larger fonts.
  4. Fig3: replaced squashed bar chart with horizontal mini-bars (4-row table).
  5. Bottom: conclusions in dark color, larger font, stat line clear from edge.

CONTENT/NUMBERS: identical to v2 (no text changes).
Does NOT overwrite v1 or v2 files.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
MILESTONE_DIR = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1"
FROZEN_CLAIMS_PATH = MILESTONE_DIR / "frozen_numeric_claims.json"
ORIG_FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
OUT_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v21"
ASSETS_DIR = OUT_DIR / "assets"

# Protect v1 and v2
V1_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v1"
V2_DIR = ROOT / "docs/experiments/presentation/math16_pilot02_one_pager_v2"

# ── Fonts ─────────────────────────────────────────────────────────────────────
plt.rcParams['font.family'] = ['Microsoft JhengHei', 'Microsoft YaHei',
                               'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# ── Color palette ─────────────────────────────────────────────────────────────
C = {
    "header_bg":  "#0F172A",   # Dark navy — high contrast for white title
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

# ── SHA protection constants ──────────────────────────────────────────────────
PROTECTED_SHAS = {
    # Original figures
    "figure_01_baseline_overall.png":    "5bc0c714769c987710dd124b7f126a53a4c77f96ccd578fbff4a0c82bdb52db2",
    "figure_03_family_breakdown.png":    "f164edc807659c45628cbab4711074879af58d3beaa825f59aaf2ebce4c9fb79",
    "figure_04_tier1_paired_analysis.png": "f18bbb774e9a75c51da364f080281172e7c35c4a5b2e30245142de0993565fdf",
    "figure_05_healer_eligibility_boundary.png": "5887f0b829797ab63f30a096ec2e27c80530c1f988dcc16e3bead4bd7feb9885",
    # v1
    "one_pager_v1.png": "1998988aabcb0b61e37c257e51e35008db56ab51abe0e43540789355cbb8d234",
    "one_pager_v1.pdf": "adc5b870cdcdbd7595dbcaa79efb44b08423196893bd544f3ab10d18d262cd21",
    # v2
    "one_pager_v2.png": "7e582554e2a1c2e27aa86199ec759f583fcd498e6fd6a1bd9ef9da50467fbefc",
    "one_pager_v2.pdf": "4fb1443d8e10b3abe74fc06d99e04356e940be38b57ed9de20b0fb65e46ae2d7",
}


def sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def verify_all_protected_shas():
    """Stop immediately if any protected file has changed."""
    paths = {
        "figure_01_baseline_overall.png":    ORIG_FIG_DIR / "figure_01_baseline_overall.png",
        "figure_03_family_breakdown.png":    ORIG_FIG_DIR / "figure_03_family_breakdown.png",
        "figure_04_tier1_paired_analysis.png": ORIG_FIG_DIR / "figure_04_tier1_paired_analysis.png",
        "figure_05_healer_eligibility_boundary.png": ORIG_FIG_DIR / "figure_05_healer_eligibility_boundary.png",
        "one_pager_v1.png": V1_DIR / "math16_pilot02_one_pager_v1.png",
        "one_pager_v1.pdf": V1_DIR / "math16_pilot02_one_pager_v1.pdf",
        "one_pager_v2.png": V2_DIR / "math16_pilot02_one_pager_v2.png",
        "one_pager_v2.pdf": V2_DIR / "math16_pilot02_one_pager_v2.pdf",
    }
    for key, p in paths.items():
        assert p.exists(), f"Protected file missing: {p}"
        actual = sha256(p)
        expected = PROTECTED_SHAS[key]
        assert actual == expected, (
            f"SHA MISMATCH (STOP): {key}\n  expected: {expected}\n  actual:   {actual}"
        )
    print("All protected SHAs: PASSED.")


def load_claims() -> dict:
    with open(FROZEN_CLAIMS_PATH, encoding="utf-8") as f:
        c = json.load(f)
    assert c["gemini_primary"]["baseline_pass"] == 289
    assert c["qwen_4b"]["baseline_pass"] == 78
    assert c["qwen_4b"]["primary_rescue"] == 5
    assert c["qwen_4b"]["posthoc_rescue"] == 6
    assert c["qwen_9b"]["baseline_pass"] == 101
    assert c["tier1_overall"]["exact_mcnemar_p"] == 0.010582
    return c


# ─────────────────────────────────────────────────────────────────────────────
# Compact v2.1 derivative figure renderers
# ─────────────────────────────────────────────────────────────────────────────

def render_fig1_compact_v21(claims: dict, path: Path):
    """Fig1 v2.1: larger fonts, clear 289/78/101 bars."""
    fig, ax = plt.subplots(figsize=(4.0, 3.0), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    models = ["Gemini\n3.5 Flash", "Qwen\n3.5 4B", "Qwen\n3.5 9B"]
    passes = [289, 78, 101]
    colors = [C["gemini"], C["qwen4b"], C["qwen9b"]]

    bars = ax.bar([0, 1, 2], passes, color=colors, width=0.52,
                  edgecolor="#1F2937", linewidth=0.9, zorder=3)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(models, fontsize=10, fontweight="bold")
    ax.set_ylabel("通過格數 / 320", fontsize=9, fontweight="bold")
    ax.set_ylim(0, 340)
    ax.set_title("Baseline 通過率", fontsize=12, fontweight="bold", pad=7, color=C["text_dk"])
    ax.grid(axis="y", linestyle="--", alpha=0.4, zorder=0)
    ax.tick_params(axis="y", labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)

    for bar, val in zip(bars, passes):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 5,
                f"{val}/320", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=C["text_dk"])

    fig.tight_layout(pad=0.6)
    fig.savefig(path, dpi=220, format="png", bbox_inches="tight")
    plt.close(fig)


def render_fig3_compact_table_v21(claims: dict, path: Path):
    """Fig3 v2.1: horizontal mini-bar table — 4 rows, clear labels, no squash."""
    families = ["Integer", "Polynomial", "Radical", "Fraction"]
    q4b =      [30,        16,           15,         17]
    q9b =      [42,        9,            19,         31]
    max_val = 80

    fig, ax = plt.subplots(figsize=(4.0, 3.0), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.axis("off")

    # Title
    fig.suptitle("Family差異（探索性）", fontsize=12, fontweight="bold",
                 color=C["text_dk"], y=0.97)

    bar_h = 0.10            # bar height in data units (axis 0-1)
    row_h = 0.21            # row pitch
    gap   = 0.03            # gap between 4B and 9B bar within a row
    y_start = 0.87          # top of first row
    label_x = 0.24          # right edge of family labels

    for i, (fam, v4, v9) in enumerate(zip(families, q4b, q9b)):
        y_top = y_start - i * row_h

        # Family label
        ax.text(label_x - 0.01, y_top - bar_h * 0.5,
                fam, ha="right", va="center",
                fontsize=9, fontweight="bold", color=C["text_dk"],
                transform=ax.transAxes)

        # 4B bar
        bar4_w = v4 / max_val * 0.72
        r4 = Rectangle((label_x, y_top - bar_h - gap), bar4_w, bar_h,
                        transform=ax.transAxes,
                        facecolor=C["qwen4b"], edgecolor="#065F46",
                        linewidth=0.7, clip_on=False)
        ax.add_patch(r4)
        ax.text(label_x + bar4_w + 0.005, y_top - bar_h * 0.5 - gap,
                f"4B {v4}", ha="left", va="center",
                fontsize=8.5, fontweight="bold", color=C["qwen4b"],
                transform=ax.transAxes)

        # 9B bar
        bar9_w = v9 / max_val * 0.72
        r9 = Rectangle((label_x, y_top - 2 * bar_h - gap), bar9_w, bar_h,
                        transform=ax.transAxes,
                        facecolor=C["qwen9b"], edgecolor="#92400E",
                        linewidth=0.7, clip_on=False)
        ax.add_patch(r9)
        ax.text(label_x + bar9_w + 0.005, y_top - 1.5 * bar_h - gap,
                f"9B {v9}", ha="left", va="center",
                fontsize=8.5, fontweight="bold", color=C["qwen9b"],
                transform=ax.transAxes)

    # Legend row
    ax.add_patch(Rectangle((0.25, 0.02), 0.06, 0.03,
                            transform=ax.transAxes,
                            facecolor=C["qwen4b"], edgecolor="none"))
    ax.text(0.32, 0.035, "4B", ha="left", va="center",
            fontsize=8, fontweight="bold", color=C["qwen4b"],
            transform=ax.transAxes)
    ax.add_patch(Rectangle((0.42, 0.02), 0.06, 0.03,
                            transform=ax.transAxes,
                            facecolor=C["qwen9b"], edgecolor="none"))
    ax.text(0.49, 0.035, "9B", ha="left", va="center",
            fontsize=8, fontweight="bold", color=C["qwen9b"],
            transform=ax.transAxes)
    ax.text(0.5, -0.02, "※ 探索性，不可外推", ha="center", va="center",
            fontsize=7, color=C["text_lt"], style="italic",
            transform=ax.transAxes)

    fig.tight_layout(pad=0.3)
    fig.savefig(path, dpi=220, format="png", bbox_inches="tight")
    plt.close(fig)


def render_fig4_compact_v21(claims: dict, path: Path):
    """Fig4 v2.1: larger matrix numbers, cleaner stat panel, single title."""
    t1 = claims["tier1_overall"]
    bp  = t1["BOTH_PASS"]    # 52
    fo  = t1["FOUR_B_ONLY"]  # 26
    no  = t1["NINE_B_ONLY"]  # 49
    bf  = t1["BOTH_FAIL"]    # 193

    fig = plt.figure(figsize=(6.2, 3.6), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")

    gs = gridspec.GridSpec(1, 2, width_ratios=[1.05, 0.95], wspace=0.12,
                           left=0.04, right=0.97, top=0.84, bottom=0.06)
    ax_m = fig.add_subplot(gs[0])
    ax_s = fig.add_subplot(gs[1])

    # ── Matrix ────────────────────────────────────────────────────────────────
    ax_m.set_facecolor("#FFFFFF")
    cell_colors = [["#D1FAE5", "#FEE2E2"], ["#FEF3C7", "#F3F4F6"]]
    cell_labels = [["BOTH PASS", "4B ONLY"], ["9B ONLY", "BOTH FAIL"]]
    cell_vals   = [[bp, fo], [no, bf]]

    ax_m.set_xlim(-0.52, 1.52)
    ax_m.set_ylim(1.52, -0.52)

    for i in range(2):
        for j in range(2):
            rect = FancyBboxPatch((j - 0.46, i - 0.46), 0.92, 0.92,
                                  boxstyle="round,pad=0.02,rounding_size=0.04",
                                  facecolor=cell_colors[i][j],
                                  edgecolor="#374151", linewidth=1.5)
            ax_m.add_patch(rect)
            # Main number — large
            ax_m.text(j, i - 0.10, f"{cell_vals[i][j]}",
                      ha="center", va="center",
                      fontsize=22, fontweight="bold", color="#111827")
            # Label below number
            ax_m.text(j, i + 0.28, cell_labels[i][j],
                      ha="center", va="center",
                      fontsize=8.5, fontweight="bold", color="#374151")

    ax_m.set_xticks([0, 1])
    ax_m.set_xticklabels(["9B PASS", "9B FAIL"],
                          fontsize=9.5, fontweight="bold")
    ax_m.set_yticks([0, 1])
    ax_m.set_yticklabels(["4B PASS", "4B FAIL"],
                          fontsize=9.5, fontweight="bold")
    ax_m.tick_params(length=0)
    for s in ax_m.spines.values():
        s.set_visible(False)

    # ── Stats panel ───────────────────────────────────────────────────────────
    ax_s.set_facecolor("#FFFFFF")
    ax_s.axis("off")

    box = FancyBboxPatch((0.03, 0.03), 0.94, 0.94,
                          boxstyle="round,pad=0.03",
                          facecolor="#F9FAFB",
                          edgecolor="#D1D5DB", linewidth=1.3)
    ax_s.add_patch(box)

    stats = [
        ("統計摘要", 0.88, 10.0, True),
        ("", 0.79, 8.5, False),
        (f"9B-only PASS:   {no} 格", 0.73, 9.0, False),
        (f"4B-only PASS:   {fo} 格", 0.62, 9.0, False),
        (f"Net Gain:  +{no - fo} 格 (+7.19%)", 0.51, 9.0, False),
        ("", 0.43, 8.5, False),
        ("Exact McNemar:", 0.37, 9.0, False),
        ("p = 0.010582 *", 0.27, 11.0, True),
        ("Cluster Bootstrap CI:", 0.18, 9.0, False),
        ("[-0.94%, +14.38%]", 0.08, 11.0, True),
    ]
    for text, y, size, bold in stats:
        ax_s.text(0.10, y, text,
                  fontsize=size,
                  fontweight="bold" if bold else "normal",
                  color="#111827" if bold else "#374151",
                  va="bottom", transform=ax_s.transAxes)

    fig.suptitle("Qwen 4B/9B 配對結果（n=320）",
                 fontsize=12, fontweight="bold", y=0.96)

    fig.savefig(path, dpi=220, format="png", bbox_inches="tight")
    plt.close(fig)


def render_fig5_compact_v21(claims: dict, path: Path):
    """Fig5 v2.1: larger bars, larger labels, clear Primary/Post-hoc footnote."""
    fig, ax = plt.subplots(figsize=(4.0, 3.0), dpi=220)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    models   = ["Gemini", "Qwen 4B", "Qwen 9B"]
    fails    = [31,  242, 219]
    elig     = [0,   10,  0]
    rescues  = [0,   5,   0]

    x = [0, 1, 2]
    w = 0.22

    r1 = ax.bar([i - w for i in x], fails, w, label="Baseline FAIL",
                color=C["fail"], edgecolor="#9CA3AF", linewidth=0.8, zorder=3)
    r2 = ax.bar(x, elig, w, label="Eligible",
                color=C["eligible"], edgecolor="#6B7280", linewidth=0.8, zorder=3)
    r3 = ax.bar([i + w for i in x], rescues, w, label="Primary Rescue",
                color=C["rescue"], edgecolor=C["rescue_dk"], linewidth=0.9, zorder=3)

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10, fontweight="bold")
    ax.set_ylabel("Cell 數量 / 320", fontsize=9, fontweight="bold")
    ax.set_ylim(0, 272)
    ax.set_title("安全修復窗口", fontsize=12, fontweight="bold",
                 pad=7, color=C["text_dk"])
    ax.legend(fontsize=8, loc="upper right", framealpha=0.92,
              edgecolor="#D1D5DB")
    ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
    ax.tick_params(axis="y", labelsize=9)
    ax.spines[["top", "right"]].set_visible(False)

    for r in r1:
        h = r.get_height()
        if h > 0:
            ax.text(r.get_x() + r.get_width() / 2, h + 4, str(int(h)),
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    for r in r2:
        h = r.get_height()
        if h > 0:
            ax.text(r.get_x() + r.get_width() / 2, h + 4, str(int(h)),
                    ha="center", va="bottom", fontsize=9, fontweight="bold")
    for r in r3:
        h = r.get_height()
        if h > 0:
            ax.text(r.get_x() + r.get_width() / 2, h + 4, str(int(h)),
                    ha="center", va="bottom", fontsize=9.5,
                    fontweight="bold", color=C["rescue_dk"])

    ax.text(0.5, -0.20,
            "Primary rescue=5格(83/320)；Post-hoc驗證=6格(84/320)；Regression=0",
            ha="center", fontsize=7.5, color=C["text_lt"],
            style="italic", transform=ax.transAxes)

    fig.tight_layout(pad=0.6)
    fig.savefig(path, dpi=220, format="png", bbox_inches="tight")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# Main one-pager canvas v2.1
# ─────────────────────────────────────────────────────────────────────────────

def build_one_pager_v21(claims: dict, asset_shas: dict, out_dir: Path) -> dict:
    import matplotlib.image as mpimg

    # A4 landscape: 11.69 × 8.27 in
    FW, FH = 11.69, 8.27
    DPI = 300

    fig = plt.figure(figsize=(FW, FH), dpi=DPI)
    fig.patch.set_facecolor("#FFFFFF")

    # ── HEADER (top 19%) — solid dark bar ────────────────────────────────────
    HDR_TOP = 1.0
    HDR_BOT = 0.81       # 19% of page height
    HDR_H = HDR_TOP - HDR_BOT

    ax_hdr = fig.add_axes([0.0, HDR_BOT, 1.0, HDR_H])
    ax_hdr.set_facecolor(C["header_bg"])
    ax_hdr.axis("off")

    # Main title — white, bold, large
    ax_hdr.text(0.5, 0.94,
                "Deterministic AST Healer 的安全修復邊界",
                ha="center", va="top", fontsize=19, fontweight="bold",
                color="#FFFFFF", transform=ax_hdr.transAxes)

    # Research question (italic, lighter white)
    ax_hdr.text(0.5, 0.70,
                "AI生成程式失敗時，哪些錯誤可由Deterministic AST Healer安全修復？哪些必須Abstain？",
                ha="center", va="top", fontsize=9.5, color="#CBD5E1",
                style="italic", transform=ax_hdr.transAxes)

    # Design line
    ax_hdr.text(0.5, 0.54,
                "16題 × 3模型 × 4條件 × 5 seeds = 960 cells  ｜  Primary 與 Post-hoc 嚴格分帳",
                ha="center", va="top", fontsize=9.0, color="#94A3B8",
                transform=ax_hdr.transAxes)

    # Three number cards
    cards = [
        (0.14, "Gemini Baseline",      "289/320",        C["card_g"],  "#1D4ED8", C["card_g_bd"]),
        (0.50, "Qwen 4B Primary",      "83/320（+5格）", C["card_4b"], "#065F46", C["card_4b_bd"]),
        (0.86, "Qwen 9B Baseline",     "101/320",        C["card_9b"], "#92400E", C["card_9b_bd"]),
    ]
    for cx, label, val, bg, tc, bd in cards:
        card = FancyBboxPatch((cx - 0.135, 0.01), 0.27, 0.35,
                               boxstyle="round,pad=0.01,rounding_size=0.03",
                               facecolor=bg, edgecolor=bd, linewidth=1.2,
                               transform=ax_hdr.transAxes, clip_on=False)
        ax_hdr.add_patch(card)
        ax_hdr.text(cx, 0.295, label,
                    ha="center", va="center", fontsize=8.0,
                    color=C["text_mid"], fontweight="bold",
                    transform=ax_hdr.transAxes)
        ax_hdr.text(cx, 0.155, val,
                    ha="center", va="center", fontsize=12.5,
                    color=tc, fontweight="bold",
                    transform=ax_hdr.transAxes)

    # ── FIGURE AREA (middle 62%) ─────────────────────────────────────────────
    # Layout: left 55% = Fig4 (large); right 45% = Fig1 / Fig5 / Fig3 stacked
    MID_TOP = HDR_BOT - 0.005   # 0.805
    MID_BOT = 0.195              # leaves 19.5% for bottom band
    MID_H = MID_TOP - MID_BOT   # ≈ 0.610

    MARGIN = 0.010
    LEFT_W = 0.545               # Fig4 width
    RIGHT_X = LEFT_W + MARGIN * 2
    RIGHT_W = 1.0 - RIGHT_X - MARGIN

    # Stack heights for right column (Fig1 / Fig5 / Fig3)
    # Fig1 and Fig5 get 36% each, Fig3-table gets 28%
    RH_F1 = 0.36
    RH_F5 = 0.36
    RH_F3 = 1.0 - RH_F1 - RH_F5   # 0.28

    fig4_img = mpimg.imread(ASSETS_DIR / "fig4_compact_v21.png")
    fig1_img = mpimg.imread(ASSETS_DIR / "fig1_compact_v21.png")
    fig5_img = mpimg.imread(ASSETS_DIR / "fig5_compact_v21.png")
    fig3_img = mpimg.imread(ASSETS_DIR / "fig3_compact_table_v21.png")

    # Fig4: left large panel
    ax4 = fig.add_axes([MARGIN, MID_BOT, LEFT_W, MID_H])
    ax4.imshow(fig4_img, aspect="auto")
    ax4.axis("off")

    # Fig1: top-right
    f1_bot = MID_BOT + (RH_F5 + RH_F3) * MID_H
    ax1 = fig.add_axes([RIGHT_X, f1_bot, RIGHT_W, RH_F1 * MID_H - 0.003])
    ax1.imshow(fig1_img, aspect="auto")
    ax1.axis("off")

    # Fig5: middle-right
    f5_bot = MID_BOT + RH_F3 * MID_H
    ax5 = fig.add_axes([RIGHT_X, f5_bot, RIGHT_W, RH_F5 * MID_H - 0.003])
    ax5.imshow(fig5_img, aspect="auto")
    ax5.axis("off")

    # Fig3 table: bottom-right
    ax3 = fig.add_axes([RIGHT_X, MID_BOT, RIGHT_W, RH_F3 * MID_H - 0.002])
    ax3.imshow(fig3_img, aspect="auto")
    ax3.axis("off")

    # Thin borders
    for ax_f in [ax4, ax1, ax5, ax3]:
        for sp in ax_f.spines.values():
            sp.set_visible(True)
            sp.set_edgecolor("#E2E8F0")
            sp.set_linewidth(0.6)

    # Caption labels
    captions = [
        (ax4, "Fig.4  Qwen 4B/9B 配對分析（McNemar p=0.011，CI=[-0.94%,+14.38%]）"),
        (ax1, "Fig.1  Baseline 通過率"),
        (ax5, "Fig.5  安全修復窗口（Primary 救回5格）"),
        (ax3, "Fig.3  Family 差異（探索性）"),
    ]
    for ax_f, cap in captions:
        bb = ax_f.get_position()
        fig.text(bb.x0 + bb.width / 2, bb.y1 + 0.003,
                 cap, ha="center", va="bottom",
                 fontsize=7.5, color="#475569",
                 style="italic", fontweight="bold")

    # ── BOTTOM BAND (bottom 19.5%) ────────────────────────────────────────────
    ax_bot = fig.add_axes([0.0, 0.0, 1.0, MID_BOT])
    ax_bot.set_facecolor(C["bot_bg"])
    ax_bot.axis("off")

    # Top divider
    ax_bot.axhline(y=0.97, xmin=0.01, xmax=0.99,
                   color=C["bot_bd"], linewidth=0.8)

    conclusions = [
        "① Healer 只在修法唯一、局部、可驗證的窄小窗口介入；其餘情況主動 Abstain。",
        "② 4B Primary 救回 5格（83/320）；Post-hoc 機制驗證額外 6格（84/320）；本次觀察到 Regression=0。",
        "③ 9B cell-level 方向偏優（+23格），但 task-clustered CI 跨 0，跨題目外推仍具不確定性。",
    ]
    for k, line in enumerate(conclusions):
        ax_bot.text(0.012, 0.85 - k * 0.22, line,
                    fontsize=9.5, fontweight="bold",
                    color=C["text_dk"], va="top",
                    transform=ax_bot.transAxes)

    # Italic metaphor
    ax_bot.text(0.012, 0.85 - 3 * 0.22,
                "   Healer 像球場最遠邊界的小柵欄，不代替球員重新比賽。",
                fontsize=8.5, color=C["text_lt"], style="italic", va="top",
                transform=ax_bot.transAxes)

    # Stat line — boxed, safe from edge
    stat_text = (
        "【統計】Exact McNemar p = 0.010582  ｜  Task-clustered Bootstrap 95% CI = [-0.94%, +14.38%]  "
        "｜  Primary/Post-hoc 嚴格分帳，Gemini & 9B Eligible=0  ｜  Family差異屬Post-hoc探索性"
    )
    ax_bot.text(0.5, 0.10, stat_text,
                ha="center", va="bottom", fontsize=7.8,
                color=C["text_mid"], style="italic",
                transform=ax_bot.transAxes,
                bbox=dict(boxstyle="round,pad=0.28",
                           facecolor="#F1F5F9",
                           edgecolor="#94A3B8", lw=0.8))

    # ── Save outputs ──────────────────────────────────────────────────────────
    png_path = out_dir / "math16_pilot02_one_pager_v21.png"
    pdf_path = out_dir / "math16_pilot02_one_pager_v21.pdf"

    fig.savefig(png_path, dpi=DPI, format="png", bbox_inches="tight")
    with PdfPages(pdf_path) as pdf:
        pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)

    return {
        "png_sha256": sha256(png_path),
        "pdf_sha256": sha256(pdf_path),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading frozen claims...")
    claims = load_claims()

    print("Verifying protected SHAs (original figs, v1, v2)...")
    verify_all_protected_shas()

    # Render compact v2.1 assets
    print("Rendering compact assets v2.1...")
    render_fig1_compact_v21(claims, ASSETS_DIR / "fig1_compact_v21.png")
    render_fig3_compact_table_v21(claims, ASSETS_DIR / "fig3_compact_table_v21.png")
    render_fig4_compact_v21(claims, ASSETS_DIR / "fig4_compact_v21.png")
    render_fig5_compact_v21(claims, ASSETS_DIR / "fig5_compact_v21.png")

    asset_shas = {
        k: sha256(ASSETS_DIR / k)
        for k in ["fig1_compact_v21.png", "fig3_compact_table_v21.png",
                  "fig4_compact_v21.png", "fig5_compact_v21.png"]
    }

    print("Building One-Pager v2.1...")
    out_meta = build_one_pager_v21(claims, asset_shas, OUT_DIR)

    # Final SHA guard
    print("Final SHA guard...")
    verify_all_protected_shas()

    # ── Manifest ──────────────────────────────────────────────────────────────
    manifest = {
        "manifest_id": "math16_pilot02_one_pager_v21_manifest",
        "version": "1.0.0",
        "project": "Ivan旺宏科學展 HealerBoundary",
        "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python_version": sys.version,
        "matplotlib_version": matplotlib.__version__,
        "page_format": "A4 landscape (297mm x 210mm)",
        "dpi": 300,
        "page_count": 1,
        "layout_version": "v2.1_visual_hotfix",
        "header_height_pct": 19,
        "bottom_height_pct": 19.5,
        "v2_defects_fixed": [
            "title: solid dark header bar (#0F172A), white bold title 19pt, high contrast",
            "whitespace: header height reduced to 19%, cards shifted up, no unused top area",
            "right column: Fig1(top,36%) + Fig5(mid,36%) + Fig3-table(bot,28%), taller Fig1/5",
            "Fig3: replaced squashed bar chart with horizontal mini-bar table (4 rows, clear labels)",
            "bottom: dark text #111827, 9.5pt bold conclusions, stat line safely away from edge",
        ],
        "compact_figures": {
            "fig1_compact_v21.png":       "Baseline 通過率 — larger fonts",
            "fig3_compact_table_v21.png": "Family差異 — horizontal mini-bar table (4 rows)",
            "fig4_compact_v21.png":       "配對結果 — larger matrix 22pt numbers + stat panel",
            "fig5_compact_v21.png":       "安全修復窗口 — larger labels, footnote Primary/Post-hoc",
        },
        "right_column_order": ["Fig1 (top, 36%)", "Fig5 (mid, 36%)", "Fig3-table (bot, 28%)"],
        "fig3_style": "horizontal_mini_bars_table",
        "protected_shas": PROTECTED_SHAS,
        "compact_asset_shas": asset_shas,
        "input_milestone_sha256": sha256(FROZEN_CLAIMS_PATH),
        "primary_posthoc_accounting": {
            "qwen4b_primary_rescue": "5 cells → 83/320 (Primary)",
            "qwen4b_posthoc_rescue": "6 cells → 84/320 [Post-hoc mechanism validation]",
            "gemini_eligible": 0, "qwen9b_eligible": 0, "observed_regression": 0,
        },
        "key_statistics": {
            "nine_b_only": 49, "four_b_only": 26,
            "exact_mcnemar_p": 0.010582,
            "task_clustered_bootstrap_95ci": "[-0.94%, +14.38%]",
        },
        "outputs": {
            "png": {"filename": "math16_pilot02_one_pager_v21.png",
                    "sha256": out_meta["png_sha256"]},
            "pdf": {"filename": "math16_pilot02_one_pager_v21.pdf",
                    "sha256": out_meta["pdf_sha256"], "page_count": 1},
        },
    }

    with open(OUT_DIR / "one_pager_v21_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # ── Build report ──────────────────────────────────────────────────────────
    report = f"""# Math16 Pilot-02 One-Pager v2.1 Visual Hotfix 報告

```text
MATH16_PILOT02_ONE_PAGER_V21_VISUAL_HOTFIX_COMPLETED
TITLE_AND_WHITESPACE_FIXED
RIGHT_COLUMN_READABILITY_IMPROVED
BOTTOM_TEXT_READABILITY_IMPROVED
ORIGINAL_AND_PRIOR_VERSION_SHAS_PRESERVED
ONE_PAGER_V21_READY_FOR_FINAL_REVIEW
```

## v2 缺陷 → v2.1 修正

| v2 缺陷 | v2.1 修正 |
|---|---|
| 主標題對比低（淡藍字）| 深色帶(#0F172A) + 白字加粗 19pt |
| 頂部空白過多 | Header 縮至 19%，卡片上移 |
| 右側 Fig 太扁 | Fig1/5 各佔 36% 帶高，Fig3 佔 28% |
| Fig3 squashed bar chart | 改為 horizontal mini-bar table（4行）|
| 底部結論字淡 | 深灰 #111827 + 9.5pt bold |
| 統計行貼頁邊 | 上移，安全底部邊界 |

## v2.1 版面

| 區域 | 高度 | 內容 |
|---|---|---|
| Header | 19% | 深色帶 + 白字主標題 + 問題/設計 + 3 數字卡 |
| Fig4 (左 54.5%) | 61.5% | 2×2 矩陣大字 + 統計面板 |
| Fig1 (右上 36%) | 22% | Baseline 三柱 |
| Fig5 (右中 36%) | 22% | 安全修復窗口 |
| Fig3-table (右下 28%) | 17.5% | 水平 mini-bar 四行表 |
| Bottom | 19.5% | 3點結論 + 統計框 |

## SHA 驗證

| 項目 | 狀態 |
|---|---|
| 原始 Figure 1/3/4/5 PNG | ✅ 不變 |
| v1 PNG/PDF | ✅ 不變 |
| v2 PNG/PDF | ✅ 不變 |

## 輸出 SHA

| 檔案 | SHA-256 |
|---|---|
| one_pager_v21.png | `{out_meta['png_sha256']}` |
| one_pager_v21.pdf | `{out_meta['pdf_sha256']}` |
"""

    with open(OUT_DIR / "one_pager_v21_build_report.md", "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nv2.1 build complete!")
    print(f"  PNG SHA: {out_meta['png_sha256']}")
    print(f"  PDF SHA: {out_meta['pdf_sha256']}")


if __name__ == "__main__":
    main()
