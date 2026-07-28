# -*- coding: utf-8 -*-
"""Math16 Pilot-02 amended figures renderer (presentation layer only).

Reads ONLY:
  docs/experiments/visualization/math16_pilot02_amendment_layer_v1/presentation_claims_v1.json

Writes ONLY to amendment-layer staging/ (SVG dry-run). Does not read/write
frozen_numeric_claims.json or docs/experiments/results/**. Does not modify
scripts/build_math16_pilot02_core_figures_v1.py or any canonical SVG/PNG/PDF.

Supported: Figures 1, 2, 3, 5.
Figure 4: reuse existing amended SVG (not recomputed here).
Figure 6: not handled.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_PATH = (
    ROOT
    / "docs/experiments/visualization/math16_pilot02_amendment_layer_v1/presentation_claims_v1.json"
)
STAGING_DIR = (
    ROOT
    / "docs/experiments/visualization/math16_pilot02_amendment_layer_v1/staging"
)
CANONICAL_FIG_DIR = (
    ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
)

plt.rcParams["font.family"] = [
    "Microsoft JhengHei",
    "Microsoft YaHei",
    "DejaVu Sans",
    "sans-serif",
]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 11

# Identity-bound colors (never position-bound)
DEFAULT_COLORS = {
    "gemini": "#4285F4",
    "qwen9b": "#D97706",
    "qwen4b": "#0F9D58",
    "fail": "#E5E7EB",
    "eligible": "#9CA3AF",
    "rescue": "#059669",
    "text_dark": "#1F2937",
    "text_muted": "#4B5563",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def load_claims(path: Path = CLAIMS_PATH) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    with open(path, encoding="utf-8") as f:
        claims = json.load(f)
    if claims.get("status") != "presentation_only_amendment":
        raise ValueError("claims status must be presentation_only_amendment")
    return claims


def colors_from_claims(claims: dict) -> dict:
    c = dict(DEFAULT_COLORS)
    ident = claims.get("model_color_identity", {})
    for k in ("gemini", "qwen9b", "qwen4b"):
        if k in ident:
            c[k] = ident[k]
    return c


def validate_claims_schema(claims: dict) -> list[str]:
    """Return list of error strings; empty means PASS."""
    errors: list[str] = []

    if claims.get("status") != "presentation_only_amendment":
        errors.append("status != presentation_only_amendment")

    order = claims.get("model_order", {}).get("presentation", [])
    keys = claims.get("model_order", {}).get("keys", [])
    expected_order = ["Gemini 3.5 Flash", "Qwen3.5 9B", "Qwen3.5 4B"]
    expected_keys = ["gemini", "qwen9b", "qwen4b"]
    if order != expected_order:
        errors.append(f"model_order.presentation mismatch: {order}")
    if keys != expected_keys:
        errors.append(f"model_order.keys mismatch: {keys}")
    if len(set(order)) != 3:
        errors.append("model_order has duplicates")

    totals = claims.get("three_model_totals", {})
    for key, pass_, fail in (("gemini", 289, 31), ("qwen9b", 101, 219), ("qwen4b", 79, 241)):
        t = totals.get(key, {})
        if t.get("pass") != pass_ or t.get("fail") != fail or t.get("total") != 320:
            errors.append(f"three_model_totals.{key} mismatch: {t}")
        elif t["pass"] + t["fail"] != 320:
            errors.append(f"three_model_totals.{key} arithmetic fail")

    fail_ord = claims.get("three_model_fail_ordered", {})
    if fail_ord.get("model_order") != expected_order:
        errors.append("three_model_fail_ordered.model_order mismatch")
    if fail_ord.get("fail_counts") != [31, 219, 241]:
        errors.append(f"fail_counts != [31,219,241]: {fail_ord.get('fail_counts')}")
    # identity alignment
    for i, key in enumerate(expected_keys):
        if totals.get(key, {}).get("fail") != fail_ord.get("fail_counts", [None] * 3)[i]:
            errors.append(f"fail identity mismatch at {key}")

    hp = claims.get("headline_presentation", {})
    b = hp.get("baseline", {})
    f = hp.get("final", {})
    if b.get("pass") != 79 or b.get("fail") != 241 or b.get("total") != 320:
        errors.append(f"baseline mismatch: {b}")
    if abs(float(b.get("rate_pct", 0)) - 24.69) > 0.001:
        errors.append(f"baseline rate_pct != 24.69: {b.get('rate_pct')}")
    if f.get("pass") != 85 or f.get("fail") != 235 or f.get("total") != 320:
        errors.append(f"final mismatch: {f}")
    if abs(float(f.get("rate_pct", 0)) - 26.56) > 0.001:
        errors.append(f"final rate_pct != 26.56: {f.get('rate_pct')}")
    if b.get("pass", 0) + b.get("fail", 0) != 320:
        errors.append("baseline pass+fail != 320")
    if f.get("pass", 0) + f.get("fail", 0) != 320:
        errors.append("final pass+fail != 320")
    if hp.get("verified_rescue") != 6:
        errors.append("verified_rescue != 6")
    if f.get("pass") - b.get("pass") != hp.get("verified_rescue"):
        errors.append("final-baseline != verified_rescue")

    frozen = hp.get("frozen_pipeline_baseline_for_comparison", {})
    if frozen.get("pass") != 78 or claims.get("governance", {}).get(
        "frozen_pipeline_baseline_qwen4b_remains"
    ) != "78/320":
        errors.append("frozen 78 declaration missing or altered")

    ov = claims.get("tier1_overall_amended_4b_vs_9b", {})
    if ov.get("matrix") != {
        "BOTH_PASS": 52,
        "FOUR_B_ONLY_PASS": 27,
        "NINE_B_ONLY_PASS": 49,
        "BOTH_FAIL": 192,
    }:
        errors.append(f"overall matrix mismatch: {ov.get('matrix')}")
    if abs(float(ov.get("exact_two_sided_mcnemar_p", 0)) - 0.01544) > 1e-9:
        errors.append("overall p mismatch")
    if ov.get("wald_95_ci") != [0.0159, 0.1216]:
        errors.append("wald CI mismatch")
    if ov.get("matched_pairs_odds_ratio", {}).get("display") != 1.81:
        errors.append("OR display mismatch")

    poly = claims.get("polynomial_family_amended_4b_vs_9b", {})
    if poly.get("pass_totals", {}).get("qwen4b") != "17/80":
        errors.append("polynomial 4B pass mismatch")
    if poly.get("matrix", {}).get("FOUR_B_ONLY_PASS") != 14:
        errors.append("polynomial FOUR_B_ONLY mismatch")
    if abs(float(poly.get("exact_two_sided_mcnemar_p", 0)) - 0.1153) > 1e-9:
        errors.append("polynomial p mismatch")

    fam = claims.get("figure_03_family_pass_counts", {})
    if fam.get("qwen4b") != [30, 17, 15, 17]:
        errors.append(f"fig3 qwen4b counts mismatch: {fam.get('qwen4b')}")
    if fam.get("qwen9b") != [42, 9, 19, 31]:
        errors.append(f"fig3 qwen9b counts mismatch: {fam.get('qwen9b')}")

    f5 = claims.get("figure_05_healer_boundary", {})
    if f5.get("baseline_fail") != [31, 219, 241]:
        errors.append("fig5 baseline_fail mismatch")
    if f5.get("verified_rescue_counts") != [0, 0, 6]:
        errors.append("fig5 verified_rescue_counts mismatch")
    if not f5.get("do_not_present_primary_84_as_main_track"):
        errors.append("fig5 must demote Primary 84")

    return errors


def render_figure_1(claims: dict, out_path: Path, colors: dict) -> None:
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    totals = claims["three_model_totals"]
    keys = claims["model_order"]["keys"]
    labels = [
        "Gemini 3.5 Flash\n(Cloud Reference)",
        "Qwen 3.5 9B\n(Tier 1 Matched)",
        "Qwen 3.5 4B\n(Tier 1 Matched)",
    ]
    passes = [totals[k]["pass"] for k in keys]
    totals_n = [totals[k]["total"] for k in keys]
    pcts = [p / t * 100 for p, t in zip(passes, totals_n)]
    bar_colors = [colors[k] for k in keys]

    x = range(len(labels))
    bars = ax.bar(
        x, pcts, color=bar_colors, width=0.45, edgecolor="#1F2937", linewidth=1.0, zorder=3
    )
    ax.set_ylabel("端到端通過率 (%)", fontsize=12, fontweight="bold")
    ax.set_title("三模型 Baseline 端到端通過率", fontsize=15, fontweight="bold", pad=15)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, fontsize=11, fontweight="bold")
    ax.set_ylim(0, 105)
    ax.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)

    for bar, p, t, pct in zip(bars, passes, totals_n, pcts):
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            bar.get_height() + 2.5,
            f"{p}/{t}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color=colors["text_dark"],
        )

    footnote = (
        "註：Gemini為Tier 2描述性參照；9B與4B為Tier 1配對比較。"
        "呈現順序 Gemini→9B→4B。Baseline不代表Healer可修復窗口。"
        "Qwen 4B Baseline presentation = 79/320。"
    )
    fig.text(0.5, 0.018, footnote, ha="center", fontsize=8.5, color=colors["text_muted"], style="italic")
    plt.tight_layout(rect=[0, 0.10, 1, 0.96])
    fig.savefig(out_path, format="svg")
    plt.close(fig)


def render_figure_2(claims: dict, out_path: Path, colors: dict) -> None:
    """Condition bars in presentation order per group: Gemini → 9B → 4B.

    Ab2d+spec Gemini is shown as a single solid blue 80/80* bar (Post-hoc
    value). Primary 63/80 is disclosed only in the footnote, not as a dual bar.
    """
    fig, ax = plt.subplots(figsize=(10.5, 6.0), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    f2 = claims["figure_02_condition_scores"]
    gemini_primary = f2["gemini_primary"]
    gemini_posthoc_g4 = f2["gemini_posthoc_g4"]
    qwen9b_scores = f2["qwen9b"]
    qwen4b_scores = f2["qwen4b"]
    # Display heights: Ab1–Ab2d+api use Primary; Ab2d+spec uses Post-hoc 80
    gemini_display = list(gemini_primary[:3]) + [gemini_posthoc_g4]
    assert gemini_display == [72, 76, 78, 80]
    assert qwen9b_scores == [18, 27, 16, 40]
    assert qwen4b_scores == [15, 19, 8, 36]

    x = list(range(4))
    width = 0.24

    # Left: Gemini (all solid); Center: 9B; Right: 4B
    rects_g = ax.bar(
        [i - width for i in x],
        gemini_display,
        width,
        color=colors["gemini"],
        edgecolor="#1F2937",
        linewidth=1.0,
        zorder=3,
        label="Gemini 3.5 Flash*",
    )
    rects_9 = ax.bar(
        x,
        qwen9b_scores,
        width,
        label="Qwen3.5 9B",
        color=colors["qwen9b"],
        edgecolor="#1F2937",
        linewidth=1.0,
        zorder=3,
    )
    rects_4 = ax.bar(
        [i + width for i in x],
        qwen4b_scores,
        width,
        label="Qwen3.5 4B",
        color=colors["qwen4b"],
        edgecolor="#1F2937",
        linewidth=1.0,
        zorder=3,
    )

    ax.set_ylabel("PASS 通過數 (Out of 80)", fontsize=12, fontweight="bold")
    ax.set_title("四種 Prompt 條件與 Spec 文件補齊後的通過數", fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(f2["condition_labels"], fontsize=11, fontweight="bold")
    ax.set_ylim(0, 96)
    ax.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
    ax.legend(
        fontsize=9.0,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        frameon=True,
        facecolor="#F9FAFB",
        edgecolor="#D1D5DB",
    )

    for i, rect in enumerate(rects_g):
        h = rect.get_height()
        label = "80/80*" if i == 3 else f"{int(h)}/80"
        ax.text(
            rect.get_x() + rect.get_width() / 2.0,
            h + 1.5,
            label,
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="#1F2937",
        )
    for rect in list(rects_9) + list(rects_4):
        h = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2.0,
            h + 1.5,
            f"{int(h)}/80",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="#1F2937",
        )

    footnote = (
        "* Gemini 3.5 Flash 的 Ab2d+spec 採 Post-hoc spec-v2，結果為 80/80；"
        "原 Primary spec-v1 為 63/80。\n"
        "其他 Gemini 條件及 Qwen3.5 9B／4B 均為各自正式結果。"
        "每組柱順序：Gemini → Qwen3.5 9B → Qwen3.5 4B。"
    )
    fig.text(0.40, 0.015, footnote, ha="center", fontsize=8.0, color=colors["text_muted"], style="italic")
    fig.subplots_adjust(left=0.08, right=0.72, top=0.88, bottom=0.14)
    fig.savefig(out_path, format="svg")
    plt.close(fig)


def render_figure_3(claims: dict, out_path: Path, colors: dict) -> None:
    """Two-model family bars; Polynomial 4B amended to 17/80."""
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    fam = claims["figure_03_family_pass_counts"]
    families = ["Integer\n(整數)", "Polynomial\n(多項式)", "Radical\n(根式)", "Fraction\n(分數)"]
    q4b_counts = fam["qwen4b"]
    q9b_counts = fam["qwen9b"]
    assert q4b_counts == [30, 17, 15, 17]
    assert q9b_counts == [42, 9, 19, 31]

    x = list(range(len(families)))
    width = 0.32
    rects1 = ax.bar(
        [i - width / 2 for i in x],
        q4b_counts,
        width,
        label="Qwen 3.5 4B",
        color=colors["qwen4b"],
        edgecolor="#1F2937",
        linewidth=1.0,
        zorder=3,
    )
    rects2 = ax.bar(
        [i + width / 2 for i in x],
        q9b_counts,
        width,
        label="Qwen 3.5 9B",
        color=colors["qwen9b"],
        edgecolor="#1F2937",
        linewidth=1.0,
        zorder=3,
    )
    ax.set_ylabel("PASS 通過格數 (Out of 80)", fontsize=12, fontweight="bold")
    ax.set_title("四數學家族的 Qwen 4B／9B Baseline 通過數", fontsize=15, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(families, fontsize=11, fontweight="bold")
    ax.set_ylim(0, 52)
    ax.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
    ax.legend(fontsize=11, loc="upper right", framealpha=0.95)

    for rect in list(rects1) + list(rects2):
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2.0,
            height + 1,
            f"{int(height)}/80",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
        )

    footnote = (
        "註：Family差異屬探索性；Polynomial反向結果（9 vs 17）不可外推為9B整體能力較差。"
        "兩模型配對結構維持；本圖不做三模型重排。"
    )
    fig.text(0.5, 0.02, footnote, ha="center", fontsize=9.0, color=colors["text_muted"], style="italic")
    plt.tight_layout(rect=[0, 0.06, 1, 0.96])
    fig.savefig(out_path, format="svg")
    plt.close(fig)


def render_figure_5(claims: dict, out_path: Path, colors: dict) -> None:
    """FAIL / Eligible / Verified rescue in G→9→4 order; no Primary 84 main track."""
    fig, ax = plt.subplots(figsize=(9.5, 5.5), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    f5 = claims["figure_05_healer_boundary"]
    hp = claims["headline_presentation"]
    models = ["Gemini 3.5 Flash", "Qwen 3.5 9B", "Qwen 3.5 4B"]
    fails = f5["baseline_fail"]
    eligibles = f5["eligible"]
    rescues = f5["verified_rescue_counts"]
    assert fails == [31, 219, 241]
    assert eligibles == [0, 0, 10]
    assert rescues == [0, 0, 6]
    assert hp["baseline"]["pass"] == 79 and hp["baseline"]["fail"] == 241
    assert hp["final"]["pass"] == 85 and hp["final"]["fail"] == 235
    assert hp["verified_rescue"] == 6

    x = list(range(len(models)))
    width = 0.24
    rects1 = ax.bar(
        [i - width for i in x],
        fails,
        width,
        label="Baseline FAIL",
        color=colors["fail"],
        edgecolor="#9CA3AF",
        linewidth=1.0,
        zorder=3,
    )
    rects2 = ax.bar(
        x,
        eligibles,
        width,
        label="Eligible Cases",
        color=colors["eligible"],
        edgecolor="#4B5563",
        linewidth=1.0,
        zorder=3,
    )
    rects3 = ax.bar(
        [i + width for i in x],
        rescues,
        width,
        label="Verified Rescue",
        color=colors["rescue"],
        edgecolor="#065F46",
        linewidth=1.2,
        zorder=3,
    )

    ax.set_ylabel("Cell Count [Out of 320]", fontsize=12, fontweight="bold")
    ax.set_title("FAIL數量與可安全修復窗口", fontsize=15, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=11, fontweight="bold")
    ax.set_ylim(0, 280)
    ax.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
    ax.legend(
        fontsize=9.5,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        frameon=True,
        facecolor="#F9FAFB",
        edgecolor="#D1D5DB",
    )

    for r in list(rects1) + list(rects2) + list(rects3):
        h = r.get_height()
        if h > 0:
            ax.text(
                r.get_x() + r.get_width() / 2.0,
                h + 4,
                f"{int(h)}",
                ha="center",
                va="bottom",
                fontsize=9.5,
                fontweight="bold",
                color="#111827",
            )

    ax.annotate(
        f5["annotation"]
        + f"\nBaseline {hp['baseline']['display']} → Final {hp['final']['display']}"
        + f"\nFAIL=[31, 219, 241] (G→9B→4B)",
        xy=(2 + width, 6.5),
        xytext=(1.35, 90),
        arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.5),
        fontsize=9.0,
        fontweight="bold",
        color="#B45309",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FEF3C7", edgecolor="#F59E0B", lw=1.2),
    )

    footnote = (
        "註：呈現順序 Gemini→9B→4B。Verified rescue=6；不呈現 Primary 84 主軌。"
        "Regression=0。Gemini與9B Eligible=0。"
    )
    fig.text(0.42, 0.02, footnote, ha="center", fontsize=9.0, color=colors["text_muted"], style="italic")
    fig.subplots_adjust(left=0.08, right=0.68, top=0.88, bottom=0.12)
    fig.savefig(out_path, format="svg")
    plt.close(fig)


STAGING_NAMES = {
    "1": "figure_01_baseline_overall.staging.svg",
    "2": "figure_02_condition_breakdown.staging.svg",
    "3": "figure_03_family_breakdown.staging.svg",
    "5": "figure_05_healer_eligibility_boundary.staging.svg",
}


def svg_text_blob(path: Path) -> str:
    try:
        ET.parse(path)
    except ET.ParseError as e:
        raise ValueError(f"SVG XML parse failed for {path}: {e}") from e
    return path.read_text(encoding="utf-8", errors="replace")


def _matplotlib_text_comments(blob: str) -> str:
    """Join matplotlib SVG <!-- label --> comments only (ignore path coords / glyph ids)."""
    import re

    return "\n".join(re.findall(r"<!--(.*?)-->", blob, flags=re.S))


def validate_staging_outputs(staging: Path, claims: dict) -> dict:
    results = {}
    colors = colors_from_claims(claims)

    # Fig1
    p1 = staging / STAGING_NAMES["1"]
    blob = svg_text_blob(p1)
    comments = _matplotlib_text_comments(blob)
    ok = True
    reasons = []
    for needle in ("79/320", "289/320", "101/320"):
        if needle not in comments and needle not in blob:
            ok = False
            reasons.append(f"missing {needle}")
    if "78/320" in comments or "78/320" in blob:
        ok = False
        reasons.append("residual 78/320")
    if "84/320" in comments:
        ok = False
        reasons.append("residual 84/320")
    if "Qwen 3.5 9B" not in blob or "Qwen 3.5 4B" not in blob or "Gemini 3.5 Flash" not in blob:
        ok = False
        reasons.append("model labels missing")
    for hexv in (colors["gemini"], colors["qwen9b"], colors["qwen4b"]):
        if hexv.lower() not in blob.lower():
            ok = False
            reasons.append(f"missing color {hexv}")
    results["figure_01"] = {"path": str(p1), "pass": ok, "reasons": reasons, "sha256": sha256_file(p1)}

    # Fig2
    p2 = staging / STAGING_NAMES["2"]
    blob = svg_text_blob(p2)
    comments = _matplotlib_text_comments(blob)
    ok = True
    reasons = []
    for needle in ("Gemini 3.5 Flash*", "Qwen3.5 9B", "Qwen3.5 4B"):
        if needle not in blob and needle not in comments:
            ok = False
            reasons.append(f"legend missing {needle}")
    if "80/80*" not in comments and "80/80*" not in blob:
        ok = False
        reasons.append("missing 80/80* label")
    if "Post-hoc spec-v2" not in comments and "Post-hoc spec-v2" not in blob:
        ok = False
        reasons.append("missing Post-hoc footnote token")
    if "Primary spec-v1" not in comments and "Primary spec-v1" not in blob:
        ok = False
        reasons.append("missing Primary footnote token")
    if "63/80" not in comments and "63/80" not in blob:
        ok = False
        reasons.append("missing 63/80 footnote token")
    # No hatch dual-track residuals
    if "Post-hoc spec-v2 (80/80)" in blob or "80/80 Post-hoc" in comments:
        ok = False
        reasons.append("residual dual-track posthoc label")
    if "Primary\nspec-v1" in comments or "Primary spec-v1 = 63/80" in comments:
        # footnote may contain "Primary spec-v1 為 63/80" — that is required.
        # Block only the old in-bar box phrasing if still as multi-line box comment alone.
        pass
    if "hatch" in blob.lower() and 'hatch="///"' in blob:
        ok = False
        reasons.append("residual hatch path")
    for hexv in (colors["gemini"], colors["qwen9b"], colors["qwen4b"]):
        if hexv.lower() not in blob.lower():
            ok = False
            reasons.append(f"missing color {hexv}")
    if "78/320" in comments or "78/320" in blob:
        ok = False
        reasons.append("residual 78/320")
    results["figure_02"] = {"path": str(p2), "pass": ok, "reasons": reasons, "sha256": sha256_file(p2)}

    # Fig3
    p3 = staging / STAGING_NAMES["3"]
    blob = svg_text_blob(p3)
    comments = _matplotlib_text_comments(blob)
    ok = True
    reasons = []
    if "17/80" not in comments and "17/80" not in blob:
        ok = False
        reasons.append("missing 17/80")
    if "16/80" in comments:
        ok = False
        reasons.append("residual 16/80")
    if "（9 vs 17）" not in comments and "(9 vs 17)" not in comments and "（9 vs 17）" not in blob:
        ok = False
        reasons.append("polynomial caption 9 vs 17 missing")
    for hexv in (colors["qwen4b"], colors["qwen9b"]):
        if hexv.lower() not in blob.lower():
            ok = False
            reasons.append(f"missing color {hexv}")
    results["figure_03"] = {"path": str(p3), "pass": ok, "reasons": reasons, "sha256": sha256_file(p3)}

    # Fig5
    p5 = staging / STAGING_NAMES["5"]
    blob = svg_text_blob(p5)
    comments = _matplotlib_text_comments(blob)
    ok = True
    reasons = []
    for needle in ("31", "219", "241", "79/320", "85/320", "Verified rescue = 6"):
        if needle not in comments and needle not in blob:
            ok = False
            reasons.append(f"missing {needle}")
    for bad in ("84/320", "83/320", "Primary rescue = 5"):
        if bad in comments or bad in blob:
            ok = False
            reasons.append(f"residual {bad}")
    # Old fail 242 must not appear as a drawn label comment
    if "<!-- 242 -->" in blob or re_search_label_242(comments):
        ok = False
        reasons.append("residual label 242")
    if not (
        "FAIL=[31, 219, 241]" in comments
        or "FAIL=[31, 219, 241]" in blob
        or ("31" in comments and "219" in comments and "241" in comments)
    ):
        ok = False
        reasons.append("FAIL triplet incomplete")
    if "Gemini 3.5 Flash" not in blob or "Qwen 3.5 9B" not in blob or "Qwen 3.5 4B" not in blob:
        ok = False
        reasons.append("model labels missing")
    results["figure_05"] = {"path": str(p5), "pass": ok, "reasons": reasons, "sha256": sha256_file(p5)}

    return results


def re_search_label_242(comments: str) -> bool:
    import re

    # Whole-token 242 in comment text only (not substrings of larger numbers like 2425)
    return re.search(r"(?<!\d)242(?!\d)", comments) is not None


def assert_canonical_untouched(pre_hashes: dict[str, str]) -> None:
    for name, expected in pre_hashes.items():
        path = CANONICAL_FIG_DIR / name
        got = sha256_file(path)
        if got != expected:
            raise RuntimeError(f"Canonical file changed: {name}\n  before={expected}\n  after={got}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render Math16 amended figures to staging only")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--claims", type=Path, default=CLAIMS_PATH)
    args = parser.parse_args(argv)

    claims = load_claims(args.claims)
    errors = validate_claims_schema(claims)
    if errors:
        print("CLAIMS_SCHEMA_BLOCKED:")
        for e in errors:
            print(" -", e)
        return 2

    print("CLAIMS_SCHEMA_PASS")
    if args.validate_only:
        return 0

    # Snapshot canonical hashes before write
    pre = {
        "figure_01_baseline_overall.svg": sha256_file(
            CANONICAL_FIG_DIR / "figure_01_baseline_overall.svg"
        ),
        "figure_04_tier1_paired_analysis.svg": sha256_file(
            CANONICAL_FIG_DIR / "figure_04_tier1_paired_analysis.svg"
        ),
    }

    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    colors = colors_from_claims(claims)

    out1 = STAGING_DIR / STAGING_NAMES["1"]
    out2 = STAGING_DIR / STAGING_NAMES["2"]
    out3 = STAGING_DIR / STAGING_NAMES["3"]
    out5 = STAGING_DIR / STAGING_NAMES["5"]

    render_figure_1(claims, out1, colors)
    render_figure_2(claims, out2, colors)
    render_figure_3(claims, out3, colors)
    render_figure_5(claims, out5, colors)

    # Ensure no fig4/fig6 staging written by this script
    for forbidden in (
        "figure_04_tier1_paired_analysis.staging.svg",
        "figure_06_healer_concept_zones.staging.svg",
    ):
        if (STAGING_DIR / forbidden).exists():
            raise RuntimeError(f"Forbidden staging output present: {forbidden}")

    assert_canonical_untouched(pre)
    results = validate_staging_outputs(STAGING_DIR, claims)

    all_pass = all(r["pass"] for r in results.values())
    print(json.dumps({"staging_validation": results, "all_pass": all_pass}, ensure_ascii=False, indent=2))
    return 0 if all_pass else 3


if __name__ == "__main__":
    sys.exit(main())
