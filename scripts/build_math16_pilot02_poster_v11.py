"""Render the readability-focused Math16 Pilot-02 Poster v1.1."""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
PRESENTATION = ROOT / "docs/experiments/presentation"
OUT_DIR = PRESENTATION / "math16_pilot02_poster_v11"
ASSETS_DIR = OUT_DIR / "assets"
PNG = OUT_DIR / "math16_pilot02_poster_v11.png"
PDF = OUT_DIR / "math16_pilot02_poster_v11.pdf"
MANIFEST = OUT_DIR / "poster_v11_manifest.json"
REPORT = OUT_DIR / "poster_v11_build_report.md"
BBOX_JSON = OUT_DIR / "poster_v11_element_bboxes.json"

SPEC = PRESENTATION / "math16_pilot02_poster_v1_spec.md"
CONTENT_MAP = PRESENTATION / "math16_pilot02_poster_v1_content_map.json"
FINAL_REPORT = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
FINAL_REPORT_MANIFEST = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13_manifest.json"
EVIDENCE = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json"
INTEGRATED = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"
QA = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
ONE_PAGER = PRESENTATION / "math16_pilot02_one_pager_v23/math16_pilot02_one_pager_v23.png"
POSTER_V1_PNG = PRESENTATION / "math16_pilot02_poster_v1/math16_pilot02_poster_v1.png"
POSTER_V1_PDF = PRESENTATION / "math16_pilot02_poster_v1/math16_pilot02_poster_v1.pdf"
CORE_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
FIGS = {
    "fig1": CORE_DIR / "figure_01_baseline_overall.png",
    "fig2": CORE_DIR / "figure_02_prompt_conditions.png",
    "fig3": CORE_DIR / "figure_03_family_breakdown.png",
    "fig4": CORE_DIR / "figure_04_tier1_paired_analysis.png",
    "fig5": CORE_DIR / "figure_05_healer_eligibility_boundary.png",
    "fig6": CORE_DIR / "figure_06_healer_concept_zones.png",
}

STARTING_HEAD = "dd15220e85ec61a67fce490ee77bc6f4ab4f7863"
POSTER_IN = (36, 24)
DPI = 150
FONT = "Microsoft JhengHei"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def protected_sources() -> dict[str, Path]:
    return {
        "poster_v1_spec": SPEC,
        "poster_v1_content_map": CONTENT_MAP,
        "final_report_v13": FINAL_REPORT,
        "final_report_v13_manifest": FINAL_REPORT_MANIFEST,
        "evidence_complete": EVIDENCE,
        "integrated_report": INTEGRATED,
        "jury_qa": QA,
        "one_pager_v23": ONE_PAGER,
        "poster_v1_png": POSTER_V1_PNG,
        "poster_v1_pdf": POSTER_V1_PDF,
        **FIGS,
    }


def source_shas() -> dict[str, str]:
    return {name: sha(path) for name, path in protected_sources().items()}


def panel(
    fig: plt.Figure,
    name: str,
    rect: tuple[float, float, float, float],
    title: str,
    body: str,
    *,
    fill: str = "#F8FBFE",
    title_color: str = "#113B62",
    body_color: str = "#14283D",
    title_size: float = 15,
    body_size: float = 12,
) -> tuple[str, object]:
    ax = fig.add_axes(rect)
    ax.set_axis_off()
    ax.add_patch(
        FancyBboxPatch(
            (0, 0), 1, 1, boxstyle="round,pad=0.012,rounding_size=0.02",
            transform=ax.transAxes, facecolor=fill, edgecolor="#AFC2D4", linewidth=1.3,
        )
    )
    ax.text(0.035, 0.93, title, ha="left", va="top", fontsize=title_size,
            fontweight="bold", color=title_color, fontfamily=FONT, transform=ax.transAxes)
    ax.text(0.035, 0.76, body, ha="left", va="top", fontsize=body_size,
            color=body_color, fontfamily=FONT, linespacing=1.34, transform=ax.transAxes)
    return name, ax


def card(
    fig: plt.Figure, name: str, rect: tuple[float, float, float, float],
    label: str, number: str, detail: str, fill: str, accent: str,
) -> tuple[str, object]:
    ax = fig.add_axes(rect)
    ax.set_axis_off()
    ax.add_patch(
        FancyBboxPatch(
            (0, 0), 1, 1, boxstyle="round,pad=0.012,rounding_size=0.025",
            transform=ax.transAxes, facecolor=fill, edgecolor=accent, linewidth=2.1,
        )
    )
    ax.text(0.05, 0.86, label, ha="left", va="top", fontsize=13, fontweight="bold",
            color="#163752", fontfamily=FONT, transform=ax.transAxes)
    ax.text(0.05, 0.51, number, ha="left", va="center", fontsize=36, fontweight="bold",
            color=accent, fontfamily=FONT, transform=ax.transAxes)
    ax.text(0.05, 0.13, detail, ha="left", va="bottom", fontsize=16, fontweight="bold",
            color=accent, fontfamily=FONT, transform=ax.transAxes)
    return name, ax


def image_panel(
    fig: plt.Figure, name: str, rect: tuple[float, float, float, float],
    image: Path, title: str,
) -> tuple[str, object]:
    ax = fig.add_axes(rect)
    ax.imshow(mpimg.imread(image), aspect="auto")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#AFC2D4")
        spine.set_linewidth(1.4)
    ax.set_title(title, loc="left", fontsize=14, fontweight="bold", color="#113B62",
                 pad=8, fontfamily=FONT)
    return name, ax


def area(bbox: object) -> float:
    return max(0.0, bbox.width) * max(0.0, bbox.height)


def overlap(a: object, b: object) -> float:
    return max(0.0, min(a.x1, b.x1) - max(a.x0, b.x0)) * max(
        0.0, min(a.y1, b.y1) - max(a.y0, b.y0)
    )


def main() -> None:
    before = source_shas()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    # New v1.1-only assets: exact copies, leaving frozen core figures untouched.
    for key, path in FIGS.items():
        shutil.copy2(path, ASSETS_DIR / f"{key}_compact_v11.png")

    fig = plt.figure(figsize=POSTER_IN, dpi=DPI, facecolor="#EAF1F7")
    elements: list[tuple[str, object]] = []

    # High-contrast header: uses its height for title, scope, question and 960 cells.
    elements.append(panel(
        fig, "header", (0.02, 0.825, 0.96, 0.155),
        "Small but Precise: Outperforming Large Models through Engineered Self-Healing",
        "Math16 Pilot-02 子實驗  •  AI生成程式失敗時，哪些錯誤可由 Deterministic AST Healer 安全修復？哪些必須 Abstain？\n"
        "16題 × 3模型 × 4條件 × 5 seeds = 960 cells",
        fill="#123A63", title_color="#FFFFFF", body_color="#F5F9FD", title_size=35, body_size=18,
    ))
    elements += [
        card(fig, "card_gemini", (0.06, 0.720, 0.27, 0.083),
             "Gemini 3.5 Flash", "289/320", "PRIMARY", "#DDF1FA", "#16779A"),
        card(fig, "card_qwen4b", (0.365, 0.720, 0.27, 0.083),
             "Qwen 4B  PRIMARY", "83/320", "救回 5 格", "#FFF0C8", "#D47600"),
        card(fig, "card_qwen9b", (0.67, 0.720, 0.27, 0.083),
             "Qwen 9B", "101/320", "BASELINE / FINAL", "#E4F0D8", "#4D7D2A"),
    ]

    # Left: concise study design, all body text 14pt or larger.
    elements.append(panel(
        fig, "left_study", (0.02, 0.535, 0.270, 0.165),
        "研究設計", "16題／四 family：Integer、Polynomial、Radical、Fraction\n"
        "三模型：Qwen 4B、Qwen 9B、Gemini 3.5 Flash\n"
        "四條件：Ab1、Ab2g、Ab2d+api、Ab2d+spec",
        body_size=14,
    ))
    elements.append(panel(
        fig, "left_window", (0.02, 0.390, 0.270, 0.125),
        "Healer 只修窄小且可驗證的窗口",
        "不是第二個解題模型，不重寫解題邏輯。\n"
        "修法唯一、局部、可驗證才介入；否則 Abstain。",
        fill="#E3F0FA", body_size=14, title_size=17,
    ))
    elements.append(panel(
        fig, "left_flow", (0.02, 0.285, 0.270, 0.090),
        "Baseline → Eligibility → Healer／Abstain",
        "生成 → Evaluator → 靜態審查 → 修復或放棄盲猜",
        fill="#EEF6E4", body_size=13, title_size=15,
    ))
    elements.append(panel(
        fig, "left_accounting", (0.02, 0.115, 0.270, 0.150),
        "Primary／Post-hoc 分帳",
        "4B Baseline 78/320\n"
        "Primary 83/320，rescue=5\n"
        "Post-hoc 84/320，total rescue=6（僅多1 PASS）\n"
        "Gemini Primary 289/320；Post-hoc 306/320",
        fill="#FFF8E9", body_size=13, title_size=16,
    ))

    # Middle: figure 4 remains the largest named figure; Figure 1/5 are enlarged.
    elements.append(image_panel(
        fig, "figure_04", (0.310, 0.405, 0.400, 0.290), FIGS["fig4"],
        "Figure 4  Tier 1 配對分析（最大主視覺）",
    ))
    elements.append(panel(
        fig, "hero_messages", (0.310, 0.310, 0.400, 0.073),
        "49 vs 26：9B-only vs 4B-only",
        "BOTH_PASS 52  •  BOTH_FAIL 193  •  McNemar p=0.010582  •  Cluster CI=[-0.94%, +14.38%]",
        fill="#DCEBFA", body_size=14, title_size=19,
    ))
    elements.append(image_panel(
        fig, "figure_01", (0.310, 0.130, 0.190, 0.155), FIGS["fig1"],
        "Figure 1  Baseline",
    ))
    elements.append(image_panel(
        fig, "figure_05", (0.520, 0.130, 0.190, 0.155), FIGS["fig5"],
        "Figure 5  Eligibility／Rescue",
    ))
    elements.append(panel(
        fig, "middle_boundary", (0.310, 0.055, 0.400, 0.053),
        "4B Eligible=10，Primary rescue=5；Gemini／9B Eligible=0",
        "無唯一安全修法時，Healer Abstain，不盲目修改。",
        fill="#EEF6E4", body_size=13, title_size=16,
    ))

    # Right: support figures plus readable four-line warning and one-line findings.
    elements.append(image_panel(
        fig, "figure_03", (0.735, 0.555, 0.245, 0.145), FIGS["fig3"],
        "Figure 3  Family 差異",
    ))
    elements.append(image_panel(
        fig, "figure_02", (0.735, 0.390, 0.245, 0.132), FIGS["fig2"],
        "Figure 2  Prompt 條件",
    ))
    elements.append(panel(
        fig, "figure_02_warning", (0.735, 0.290, 0.245, 0.083),
        "Figure 2 分帳警語",
        "1. Gemini 80/80 = Post-hoc\n"
        "2. Primary spec-v1 = 63/80\n"
        "3. Qwen = spec-v2\n"
        "4. 不作完全同條件因果推論",
        fill="#FFF0C8", body_size=12, title_size=15,
    ))
    elements.append(image_panel(
        fig, "figure_06", (0.735, 0.130, 0.245, 0.135), FIGS["fig6"],
        "Figure 6  安全概念圖",
    ))
    elements.append(panel(
        fig, "right_findings", (0.735, 0.055, 0.245, 0.055),
        "五項主要發現",
        "1. Baseline與修復窗口不同  2. 4B有窄小 repair window  3. 9B family非單調\n"
        "4. Prompt效果依模型／版本而異  5. Abstain是重要安全能力",
        body_size=11.5, title_size=14,
    ))

    # Bottom: limitations are one line each; conclusion is enlarged and separated.
    elements.append(panel(
        fig, "bottom_limitations", (0.02, 0.005, 0.690, 0.035),
        "三項限制",
        "1. Cluster CI 跨0，外推有限  •  2. Fraction為探索性，非純數學能力差異  •  3. Regression=0／Eligible=0僅限本次",
        fill="#FCECE9", body_size=13, title_size=14,
    ))
    elements.append(panel(
        fig, "bottom_conclusion", (0.735, 0.005, 0.245, 0.035),
        "結論",
        "Healer 只修窄小且可驗證的窗口。",
        fill="#DCEBFA", body_size=16, title_size=14,
    ))

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    by_name = dict(elements)
    data: dict[str, object] = {}
    for name, artist in elements:
        bbox = artist.get_window_extent(renderer=renderer)
        position = artist.get_position()
        data[name] = {
            "bbox_pixels": {
                "x0": round(float(bbox.x0), 3), "y0": round(float(bbox.y0), 3),
                "x1": round(float(bbox.x1), 3), "y1": round(float(bbox.y1), 3),
                "width": round(float(bbox.width), 3), "height": round(float(bbox.height), 3),
                "area": round(area(bbox), 3),
            },
            "position_figure_fraction": {
                "x0": round(float(position.x0), 6), "y0": round(float(position.y0), 6),
                "width": round(float(position.width), 6), "height": round(float(position.height), 6),
            },
        }

    pairs: list[dict[str, object]] = []
    collisions: list[dict[str, object]] = []
    for left, right in combinations(by_name, 2):
        value = overlap(
            by_name[left].get_window_extent(renderer=renderer),
            by_name[right].get_window_extent(renderer=renderer),
        )
        item = {"left": left, "right": right, "intersection_area_pixels": round(value, 6)}
        pairs.append(item)
        if value > 0:
            collisions.append(item)
    if collisions:
        raise RuntimeError(f"BBox collisions: {collisions}")

    fig.savefig(PNG, dpi=DPI, facecolor=fig.get_facecolor())
    fig.savefig(PDF, dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    after = source_shas()
    if after != before:
        raise RuntimeError("a protected frozen source SHA changed during v1.1 rendering")
    final_manifest = json.loads(FINAL_REPORT_MANIFEST.read_text(encoding="utf-8"))
    if sha(FINAL_REPORT) != final_manifest["v13_sha256"]:
        raise RuntimeError("Final Report v1.3 SHA mismatch")

    bbox = {
        "methodology": {
            "bbox_measurement": "get_window_extent(renderer=renderer)",
            "position_measurement": "get_position()",
            "pairwise_policy": "any intersection area > 0 fails the build",
        },
        "element_count": len(data), "pair_count": len(pairs),
        "passing_pair_count": len(pairs) - len(collisions), "collision_count": len(collisions),
        "elements": data, "pairs": pairs,
    }
    BBOX_JSON.write_text(json.dumps(bbox, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    outputs = {
        "png_sha256": sha(PNG), "pdf_sha256": sha(PDF), "bbox_sha256": sha(BBOX_JSON),
        "assets": {p.name: sha(p) for p in sorted(ASSETS_DIR.glob("*.png"))},
    }
    manifest = {
        "manifest_id": "math16_pilot02_poster_v11_render_manifest",
        "version": "1.1", "starting_head": STARTING_HEAD,
        "poster_dimensions_inches": list(POSTER_IN), "orientation": "landscape", "columns": 3,
        "readability_hotfixes": [
            "high-contrast Header with explicit Math16 Pilot-02 子實驗 scope and 960 cells",
            "50%+ larger card numbers with independent 救回5格 highlight",
            "Figure 4 retained as largest figure; enlarged Figure 1/5 panels",
            "four-line Figure 2 warning; compact one-line findings and bottom limitations",
        ],
        "source_shas_before_and_after_match": True, "source_shas": before, "outputs": outputs,
        "bbox": {k: bbox[k] for k in ("element_count", "pair_count", "passing_pair_count", "collision_count")},
        "model_calls": 0, "rescoring": False, "healer_execution": False,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "# Math16 Pilot-02 Poster v1.1 Readability Hotfix Report\n\n"
        "## Scope\n"
        "- Pure visual hotfix: layout, font size, contrast, and information density only.\n"
        "- No official number, conclusion, core figure, Final Report, Poster v1, spec, or One-Pager change.\n\n"
        "## Improvements\n"
        "- Header adds high-contrast `Math16 Pilot-02 子實驗` and a large standalone `960 cells` statement.\n"
        "- Cards use enlarged 30pt core numbers; Qwen 4B `救回 5 格` is independently highlighted.\n"
        "- Figure 4 remains the largest figure; Figure 1/5 panels enlarged; right-column prose is compressed.\n"
        "- Figure 2 uses four readable accounting lines; limitations use one line each; conclusion is isolated.\n\n"
        "## Three-second messages\n"
        "- Math16 Pilot-02 子實驗 • 960 cells • 救回 5 格 • 49 vs 26 • Healer只修窄小且可驗證的窗口。\n\n"
        "## Frozen accounting retained\n"
        "- 4B Baseline 78/320; Primary 83/320 (rescue=5); Post-hoc 84/320 (total rescue=6; +1 PASS).\n"
        "- Gemini Primary 289/320; Gemini Post-hoc 306/320.\n\n"
        "## Figure 2 warning\n"
        "- Gemini 80/80 is Post-hoc.\n"
        "- Primary spec-v1=63/80.\n"
        "- Qwen uses spec-v2.\n"
        "- No fully matched-condition causal inference.\n\n"
        "## BBox verification\n"
        f"- Named elements: {bbox['element_count']}; pairs: {bbox['pair_count']}; "
        f"passing: {bbox['passing_pair_count']}; collisions: {bbox['collision_count']}.\n"
        "- Renderer get_window_extent() and get_position() measurements were used; any overlap fails the build.\n\n"
        "## Output SHA-256\n"
        f"- PNG: `{outputs['png_sha256']}`\n- PDF: `{outputs['pdf_sha256']}`\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "POSTER_V11_RENDERED", "bbox": manifest["bbox"], "outputs": outputs}, ensure_ascii=False))


if __name__ == "__main__":
    main()
