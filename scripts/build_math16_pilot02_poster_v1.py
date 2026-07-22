"""Render the frozen Math16 Pilot-02 Poster v1 as a PNG and one-page PDF."""
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
OUT_DIR = PRESENTATION / "math16_pilot02_poster_v1"
ASSETS_DIR = OUT_DIR / "assets"
PNG_PATH = OUT_DIR / "math16_pilot02_poster_v1.png"
PDF_PATH = OUT_DIR / "math16_pilot02_poster_v1.pdf"
MANIFEST_PATH = OUT_DIR / "poster_v1_manifest.json"
REPORT_PATH = OUT_DIR / "poster_v1_build_report.md"
BBOX_PATH = OUT_DIR / "poster_v1_element_bboxes.json"

SPEC_PATH = PRESENTATION / "math16_pilot02_poster_v1_spec.md"
CONTENT_MAP_PATH = PRESENTATION / "math16_pilot02_poster_v1_content_map.json"
FINAL_REPORT = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13.md"
FINAL_REPORT_MANIFEST = ROOT / "docs/experiments/reports/math16_pilot02_final_report_v13_manifest.json"
EVIDENCE_DIR = ROOT / "docs/experiments/milestones/math16_pilot02_evidence_complete_v1"
EVIDENCE_MANIFEST = EVIDENCE_DIR / "evidence_complete_manifest.json"
INTEGRATED_REPORT = ROOT / "docs/experiments/reports/math16_pilot02_integrated_results_report_v1.md"
JURY_QA = ROOT / "docs/experiments/reports/math16_pilot02_jury_qa_final_v1.md"
CORE_FIG_DIR = ROOT / "docs/experiments/visualization/math16_pilot02_core_figures_v1"
ONE_PAGER = PRESENTATION / "math16_pilot02_one_pager_v23/math16_pilot02_one_pager_v23.png"

FIGURES = {
    "figure_01_baseline_overall": CORE_FIG_DIR / "figure_01_baseline_overall.png",
    "figure_02_prompt_conditions": CORE_FIG_DIR / "figure_02_prompt_conditions.png",
    "figure_03_family_breakdown": CORE_FIG_DIR / "figure_03_family_breakdown.png",
    "figure_04_tier1_paired_analysis": CORE_FIG_DIR / "figure_04_tier1_paired_analysis.png",
    "figure_05_healer_eligibility_boundary": CORE_FIG_DIR / "figure_05_healer_eligibility_boundary.png",
    "figure_06_healer_concept_zones": CORE_FIG_DIR / "figure_06_healer_concept_zones.png",
}

STARTING_HEAD = "3a8c52934ec7ead2a3ee9de44f0bb0ada07b6306"
POSTER_SIZE_IN = (36, 24)
DPI = 150
FONT = "Microsoft JhengHei"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_paths() -> dict[str, Path]:
    return {
        "poster_spec": SPEC_PATH,
        "poster_content_map": CONTENT_MAP_PATH,
        "final_report_v13": FINAL_REPORT,
        "final_report_v13_manifest": FINAL_REPORT_MANIFEST,
        "evidence_complete_manifest": EVIDENCE_MANIFEST,
        "integrated_report": INTEGRATED_REPORT,
        "jury_qa": JURY_QA,
        "one_pager_v23": ONE_PAGER,
        **FIGURES,
    }


def source_shas() -> dict[str, str]:
    return {name: sha256(path) for name, path in source_paths().items()}


def verify_frozen_sources(before: dict[str, str]) -> None:
    if source_shas() != before:
        raise RuntimeError("a frozen source SHA changed during poster rendering")
    final_manifest = json.loads(FINAL_REPORT_MANIFEST.read_text(encoding="utf-8"))
    if sha256(FINAL_REPORT) != final_manifest["v13_sha256"]:
        raise RuntimeError("Final Report v1.3 SHA mismatch against its manifest")


def add_panel(
    fig: plt.Figure,
    name: str,
    rect: tuple[float, float, float, float],
    title: str,
    body: str,
    *,
    facecolor: str = "#F7FAFC",
    title_color: str = "#12355B",
    body_size: float = 11,
    title_size: float = 15,
) -> tuple[str, object]:
    ax = fig.add_axes(rect)
    ax.set_axis_off()
    ax.add_patch(
        FancyBboxPatch(
            (0, 0),
            1,
            1,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            linewidth=1.2,
            edgecolor="#B8C7D9",
            facecolor=facecolor,
            transform=ax.transAxes,
            clip_on=False,
        )
    )
    ax.text(
        0.035,
        0.94,
        title,
        va="top",
        ha="left",
        fontsize=title_size,
        fontweight="bold",
        color=title_color,
        fontfamily=FONT,
        transform=ax.transAxes,
    )
    ax.text(
        0.035,
        0.84,
        body,
        va="top",
        ha="left",
        fontsize=body_size,
        color="#14283D",
        fontfamily=FONT,
        linespacing=1.35,
        transform=ax.transAxes,
        wrap=True,
    )
    return name, ax


def add_image(
    fig: plt.Figure,
    name: str,
    rect: tuple[float, float, float, float],
    image_path: Path,
    title: str,
) -> tuple[str, object]:
    ax = fig.add_axes(rect)
    ax.set_facecolor("white")
    ax.imshow(mpimg.imread(image_path), aspect="auto")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#B8C7D9")
        spine.set_linewidth(1.2)
    ax.set_title(
        title,
        fontsize=12,
        fontweight="bold",
        color="#12355B",
        loc="left",
        pad=7,
        fontfamily=FONT,
    )
    return name, ax


def rect_area(bbox: object) -> float:
    return max(0.0, bbox.width) * max(0.0, bbox.height)


def intersection_area(a: object, b: object) -> float:
    left = max(a.x0, b.x0)
    right = min(a.x1, b.x1)
    bottom = max(a.y0, b.y0)
    top = min(a.y1, b.y1)
    return max(0.0, right - left) * max(0.0, top - bottom)


def render() -> dict[str, object]:
    before = source_shas()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    for path in FIGURES.values():
        shutil.copy2(path, ASSETS_DIR / path.name)

    fig = plt.figure(figsize=POSTER_SIZE_IN, dpi=DPI, facecolor="#EEF3F8")
    elements: list[tuple[str, object]] = []

    # Header and hierarchy level 2 number cards.
    elements.append(
        add_panel(
            fig,
            "header_title",
            (0.025, 0.875, 0.95, 0.10),
            "Small but Precise: Outperforming Large Models through Engineered Self-Healing",
            "研究問題：AI生成程式失敗時，哪些錯誤可由 Deterministic AST Healer 安全修復？哪些必須 Abstain？\n"
            "16題 × 3模型 × 4條件 × 5 seeds = 960 cells",
            facecolor="#12355B",
            title_color="white",
            body_size=15,
            title_size=25,
        )
    )
    elements.append(
        add_panel(
            fig, "header_card_gemini", (0.08, 0.815, 0.25, 0.045),
            "Gemini 3.5 Flash", "289/320  PASS\n雲端強模型參照",
            facecolor="#D8ECF3", body_size=12, title_size=13,
        )
    )
    elements.append(
        add_panel(
            fig, "header_card_qwen4b", (0.375, 0.815, 0.25, 0.045),
            "Qwen 3.5 4B  Primary", "83/320  PASS\nBaseline 78 + 救回5格",
            facecolor="#FFE9BE", body_size=12, title_size=13,
        )
    )
    elements.append(
        add_panel(
            fig, "header_card_qwen9b", (0.67, 0.815, 0.25, 0.045),
            "Qwen 3.5 9B", "101/320  PASS\nBaseline / Final",
            facecolor="#E2EBD6", body_size=12, title_size=13,
        )
    )

    # Left column: study design.
    elements.append(
        add_panel(
            fig, "left_motivation", (0.025, 0.666, 0.285, 0.130),
            "研究動機", "小模型部署常遇語法、契約、API、執行與語意層失敗。\n"
            "目標：劃定硬性 AST 修復可安全介入的邊界。",
            body_size=12,
        )
    )
    elements.append(
        add_panel(
            fig, "left_healer_role", (0.025, 0.542, 0.285, 0.112),
            "Healer 定位：只修窄小窗口",
            "不是第二個解題模型，不重寫解題邏輯。\n"
            "僅在修法唯一、局部、可驗證時介入；否則 Abstain。",
            facecolor="#E6F0FA", body_size=12,
        )
    )
    elements.append(
        add_panel(
            fig, "left_design", (0.025, 0.398, 0.285, 0.132),
            "研究設計", "16題／四 family：Integer、Polynomial、Radical、Fraction\n"
            "三模型：Qwen 4B、Qwen 9B、Gemini 3.5 Flash\n"
            "四條件：Ab1、Ab2g、Ab2d+api、Ab2d+spec",
            body_size=11,
        )
    )
    elements.append(
        add_panel(
            fig, "left_flow", (0.025, 0.270, 0.285, 0.110),
            "Baseline → Eligibility → Healer／Abstain",
            "LLM 程式生成 → Evaluator Baseline → Eligibility 靜態審查\n"
            "→ Active Healer（唯一、局部、可驗證）或 Abstain",
            facecolor="#F1F6E8", body_size=11,
        )
    )
    elements.append(
        add_panel(
            fig, "left_accounting", (0.025, 0.065, 0.285, 0.185),
            "Primary／Post-hoc 分帳",
            "4B Baseline = 78/320\n"
            "Primary：83/320，rescue=5（唯一正式預註冊結論）\n"
            "Post-hoc：84/320，total rescue=6\n"
            "相較 Primary 僅多 1 PASS\n"
            "Gemini：Primary 289/320；Post-hoc 306/320",
            facecolor="#FFF8E9", body_size=11,
        )
    )

    # Middle column: Figure 4 is deliberately the largest image.
    elements.append(
        add_image(
            fig, "figure_04_tier1_paired_analysis", (0.335, 0.465, 0.375, 0.330),
            FIGURES["figure_04_tier1_paired_analysis"], "Figure 4  Tier 1 配對分析（主視覺）",
        )
    )
    elements.append(
        add_panel(
            fig, "middle_hero_statistics", (0.335, 0.350, 0.375, 0.097),
            "配對核心訊息",
            "BOTH_PASS 52   |   FOUR_B_ONLY 26   |   NINE_B_ONLY 49   |   BOTH_FAIL 193\n"
            "McNemar p=0.010582    •    Cluster CI=[-0.94%, +14.38%]\n"
            "9B-only 49 vs 4B-only 26；外推至未知題型仍具不確定性。",
            facecolor="#DCEAF7", body_size=11, title_size=14,
        )
    )
    elements.append(
        add_image(
            fig, "figure_01_baseline_overall", (0.335, 0.170, 0.178, 0.160),
            FIGURES["figure_01_baseline_overall"], "Figure 1  Baseline",
        )
    )
    elements.append(
        add_image(
            fig, "figure_05_healer_eligibility_boundary", (0.532, 0.170, 0.178, 0.160),
            FIGURES["figure_05_healer_eligibility_boundary"], "Figure 5  Eligibility／Rescue",
        )
    )
    elements.append(
        add_panel(
            fig, "middle_eligibility_summary", (0.335, 0.065, 0.375, 0.085),
            "Healer 邊界",
            "4B Eligible=10、Primary rescue=5；Gemini／9B Eligible=0。\n"
            "無唯一安全修法時，系統 Abstain，不盲目修改。",
            facecolor="#EFF6E7", body_size=11, title_size=14,
        )
    )

    # Right column: supporting images, warning, interpretation, limits, conclusion.
    elements.append(
        add_image(
            fig, "figure_03_family_breakdown", (0.735, 0.630, 0.240, 0.166),
            FIGURES["figure_03_family_breakdown"], "Figure 3  Family 差異",
        )
    )
    elements.append(
        add_image(
            fig, "figure_02_prompt_conditions", (0.735, 0.455, 0.240, 0.145),
            FIGURES["figure_02_prompt_conditions"], "Figure 2  Prompt 條件",
        )
    )
    elements.append(
        add_panel(
            fig, "figure_02_warning", (0.735, 0.375, 0.240, 0.060),
            "Figure 2 分帳警語",
            "Gemini 80/80 為 Post-hoc 機制驗證；Primary spec-v1=63/80。\n"
            "Qwen 採 spec-v2；不作完全同條件 Primary 因果推論。",
            facecolor="#FFF1CC", body_size=9, title_size=11,
        )
    )
    elements.append(
        add_image(
            fig, "figure_06_healer_concept_zones", (0.735, 0.205, 0.240, 0.145),
            FIGURES["figure_06_healer_concept_zones"], "Figure 6  安全概念圖",
        )
    )
    elements.append(
        add_panel(
            fig, "right_discoveries", (0.735, 0.065, 0.240, 0.122),
            "五項主要發現",
            "1. Baseline能力與可修復窗口不同。\n"
            "2. 4B 有窄小、可驗證 repair window。\n"
            "3. 9B 整體較高，但 family 非單調。\n"
            "4. Prompt 效果依模型、版本與部署條件而異。\n"
            "5. Abstain 是重要安全能力。",
            body_size=8.6, title_size=11,
        )
    )
    elements.append(
        add_panel(
            fig, "right_limitations", (0.735, 0.005, 0.115, 0.045),
            "三項限制",
            "McNemar 顯著但 Cluster CI 跨0；Fraction 為探索性；\n"
            "Regression=0／Eligible=0 僅限本次凍結測試。",
            facecolor="#FBE9E7", body_size=7.2, title_size=9,
        )
    )
    elements.append(
        add_panel(
            fig, "right_conclusion", (0.860, 0.005, 0.115, 0.045),
            "一句結論",
            "Healer 只修窄小窗口；無確定解即 Abstain。",
            facecolor="#DDEBF7", body_size=7.2, title_size=9,
        )
    )

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    element_data: dict[str, dict[str, object]] = {}
    for name, artist in elements:
        bbox = artist.get_window_extent(renderer=renderer)
        position = artist.get_position()
        element_data[name] = {
            "bbox_pixels": {
                "x0": round(float(bbox.x0), 3),
                "y0": round(float(bbox.y0), 3),
                "x1": round(float(bbox.x1), 3),
                "y1": round(float(bbox.y1), 3),
                "width": round(float(bbox.width), 3),
                "height": round(float(bbox.height), 3),
                "area": round(rect_area(bbox), 3),
            },
            "position_figure_fraction": {
                "x0": round(float(position.x0), 6),
                "y0": round(float(position.y0), 6),
                "width": round(float(position.width), 6),
                "height": round(float(position.height), 6),
            },
        }

    pairs: list[dict[str, object]] = []
    collisions: list[dict[str, object]] = []
    axes_by_name = dict(elements)
    for left_name, right_name in combinations(axes_by_name, 2):
        left_bbox = axes_by_name[left_name].get_window_extent(renderer=renderer)
        right_bbox = axes_by_name[right_name].get_window_extent(renderer=renderer)
        area = intersection_area(left_bbox, right_bbox)
        record = {"left": left_name, "right": right_name, "intersection_area_pixels": round(area, 6)}
        pairs.append(record)
        if area > 0:
            collisions.append(record)
    if collisions:
        raise RuntimeError(f"BBox collision detected: {collisions}")

    fig.savefig(PNG_PATH, dpi=DPI, facecolor=fig.get_facecolor())
    fig.savefig(PDF_PATH, dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)

    verify_frozen_sources(before)
    bbox_payload = {
        "methodology": {
            "renderer": "matplotlib Agg",
            "bbox_measurement": "get_window_extent(renderer=renderer)",
            "position_measurement": "get_position()",
            "pairwise_policy": "any intersection area > 0 fails the build",
        },
        "element_count": len(element_data),
        "pair_count": len(pairs),
        "passing_pair_count": len(pairs) - len(collisions),
        "collision_count": len(collisions),
        "elements": element_data,
        "pairs": pairs,
    }
    BBOX_PATH.write_text(json.dumps(bbox_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    output_shas = {
        "poster_png_sha256": sha256(PNG_PATH),
        "poster_pdf_sha256": sha256(PDF_PATH),
        "bbox_json_sha256": sha256(BBOX_PATH),
        "asset_shas": {path.name: sha256(path) for path in sorted(ASSETS_DIR.glob("*.png"))},
    }
    manifest = {
        "manifest_id": "math16_pilot02_poster_v1_render_manifest",
        "version": "1.0.0",
        "starting_head": STARTING_HEAD,
        "poster_dimensions_inches": list(POSTER_SIZE_IN),
        "orientation": "landscape",
        "columns": 3,
        "visual_hierarchy": {
            "hero": "figure_04_tier1_paired_analysis",
            "level_2": "header_core_cards",
            "level_3": ["figure_01_baseline_overall", "figure_05_healer_eligibility_boundary"],
            "level_4": ["figure_02_prompt_conditions", "figure_03_family_breakdown", "figure_06_healer_concept_zones"],
        },
        "source_shas_before_and_after_match": True,
        "source_shas": before,
        "outputs": output_shas,
        "bbox": {
            "element_count": len(element_data),
            "pair_count": len(pairs),
            "passing_pair_count": len(pairs) - len(collisions),
            "collision_count": len(collisions),
        },
        "pdf_page_count_validation": "single Matplotlib figure saved once to PDF; tests validate one /Type /Page token",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model_calls": 0,
        "rescoring": False,
        "healer_execution": False,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(
        "# Math16 Pilot-02 Poster v1 Render Build Report\n\n"
        "## Layout\n"
        f"- Landscape {POSTER_SIZE_IN[0]} × {POSTER_SIZE_IN[1]} inches; three columns.\n"
        "- Figure 4 is the largest named figure; header cards are level 2; Figures 1/5 level 3; Figures 2/3/6 level 4.\n\n"
        "## Frozen accounting\n"
        "- 4B: Baseline 78/320; Primary 83/320 (rescue=5); Post-hoc 84/320 (total rescue=6; +1 PASS vs Primary).\n"
        "- Gemini: Primary 289/320; Post-hoc 306/320.\n"
        "- Figure 2 warning: Gemini 80/80 is Post-hoc; Primary spec-v1=63/80; Qwen uses spec-v2; no direct Primary causal inference.\n\n"
        "## Renderer BBox verification\n"
        f"- Named elements: {len(element_data)}\n"
        f"- Pairwise comparisons: {len(pairs)}\n"
        f"- Passing pairs: {len(pairs) - len(collisions)}\n"
        f"- Collisions: {len(collisions)}\n"
        "- Measured with get_window_extent(renderer=renderer) and get_position(); any positive intersection fails the build.\n\n"
        "## Integrity\n"
        "- Frozen source SHA values matched before and after rendering.\n"
        f"- PNG SHA-256: `{output_shas['poster_png_sha256']}`\n"
        f"- PDF SHA-256: `{output_shas['poster_pdf_sha256']}`\n"
        "- Model calls=0; rescoring=false; Healer execution=false.\n",
        encoding="utf-8",
    )
    return manifest


if __name__ == "__main__":
    result = render()
    print(json.dumps({"status": "POSTER_RENDERED", "bbox": result["bbox"], "outputs": result["outputs"]}, ensure_ascii=False))
