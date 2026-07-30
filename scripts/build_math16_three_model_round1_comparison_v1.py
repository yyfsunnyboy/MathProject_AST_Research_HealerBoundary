# -*- coding: utf-8 -*-
"""Build Math16 three-model Round 1 comparison archive (no Round 2)."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs/決賽文件/實驗結果文件/Math16"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Frozen Round-1 headline numbers (must match authoritative summaries / handoff).
MODELS = {
    "qwen4b": {
        "label": "Qwen 4B",
        "display_order": 3,
        "baseline_pass": 79,
        "baseline_fail": 241,
        "final_pass": 88,
        "final_fail": 232,
        "verified_rescue": 9,
        "regression": 0,
        "pass_pass_modified": 0,
        "pass_curve": {
            "C0": 79,
            "C1": 85,
            "C2": 86,
            "C3": 86,
            "C4": 86,
            "C5a": 88,
            "C5b": 88,
            "C5c": 88,
        },
        "authority_note": "4B cumulative FAIL-only Round 1 (Method2／Development closures under _v1); headline from sealed handoff",
        "sources": [
            "docs/決賽文件/實驗結果文件/Math16/06_math16_aggressive_healer_current_handoff_v1.md",
            "docs/experiments/manifests/math16_c5a_final_source_closure_v1.json",
        ],
    },
    "qwen9b": {
        "label": "Qwen 9B",
        "display_order": 2,
        "baseline_pass": 101,
        "baseline_fail": 219,
        "final_pass": 102,
        "final_fail": 218,
        "verified_rescue": 1,
        "regression": 0,
        "pass_pass_modified": 0,
        "pass_curve": {
            "C0": 101,
            "C1": 101,
            "C2": 102,
            "C3": 102,
            "C4": 102,
            "C5a": 102,
            "C5b": 102,
            "C5c": 102,
        },
        "authority_note": "qwen9b_fail_gated_authoritative_v1 FAIL-only C0→C5c",
        "sources": [
            "docs/experiments/manifests/math16_c0_c4_fail_gated_authoritative_chain_qwen9b_fail_gated_authoritative_v1.json",
            "docs/experiments/manifests/math16_c5a_c5c_tier_d_d5_d2_chain_qwen9b_fail_gated_authoritative_v1.json",
            "docs/決賽文件/實驗結果文件/Math16/07_math16_qwen9b_aggressive_healer_round1_handoff_v1.md",
        ],
    },
    "gemini": {
        "label": "Gemini 3.5 Flash",
        "display_order": 1,
        "baseline_pass": 289,
        "baseline_fail": 31,
        "final_pass": 289,
        "final_fail": 31,
        "verified_rescue": 0,
        "regression": 0,
        "pass_pass_modified": 0,
        "pass_curve": {
            "C0": 289,
            "C1": 289,
            "C2": 289,
            "C3": 289,
            "C4": 289,
            "C5a": 289,
            "C5b": 289,
            "C5c": 289,
        },
        "authority_note": "gemini_fail_gated_authoritative_v1 FAIL-only C0→C5c",
        "sources": [
            "docs/experiments/manifests/math16_cumulative_summary_gemini_fail_gated_authoritative_v1.json",
            "docs/experiments/manifests/math16_c5a_c5c_tier_d_d5_d2_chain_gemini_fail_gated_authoritative_v1.json",
        ],
    },
}

FORMAL_CONCLUSION = (
    "在同一套凍結、FAIL-only、單輪 Deterministic Healer 下，Qwen 4B、Qwen 9B 與 Gemini "
    "分別獲得 9、1、0 格 verified rescue；以 Baseline FAIL 為分母，修復率分別為 3.73%、"
    "0.46% 與 0%。在本次三模型與 16 題實驗範圍內，Baseline 表現較高的模型，其殘餘失敗"
    "較少命中現有 frozen rules 的安全修復窗口。此結果顯示 Healer 效益與 residual failure "
    "type 及規則適配程度密切相關，但不宣稱模型規模與修復率存在普遍因果關係。"
    "三模型 regression 均為 0。"
)

COLORS = {
    "gemini": "#2A6F97",
    "qwen9b": "#BC4749",
    "qwen4b": "#6A994E",
}


def head_sha() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, cwd=str(ROOT)
    ).strip()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pct(n: int, d: int) -> float:
    return round(100.0 * n / d, 2) if d else 0.0


def verify_against_sources() -> list[str]:
    errors: list[str] = []
    # 9B
    c0c4 = json.loads(
        (
            ROOT
            / "docs/experiments/manifests/math16_c0_c4_fail_gated_authoritative_chain_qwen9b_fail_gated_authoritative_v1.json"
        ).read_text(encoding="utf-8")
    )
    c5 = json.loads(
        (
            ROOT
            / "docs/experiments/manifests/math16_c5a_c5c_tier_d_d5_d2_chain_qwen9b_fail_gated_authoritative_v1.json"
        ).read_text(encoding="utf-8")
    )
    if c0c4["pass_curve"]["C0"] != 101 or c5["pass_curve_c0_c5c"]["C5c"] != 102:
        errors.append("9B_PASS_CURVE_MISMATCH")
    rescue_9b = (
        c0c4["layers"]["C1"]["transitions"]["verified_rescue"]
        + c0c4["layers"]["C2"]["transitions"]["verified_rescue"]
        + c0c4["layers"]["C3"]["transitions"]["verified_rescue"]
        + c0c4["layers"]["C4"]["transitions"]["verified_rescue"]
        + c5["d5"]["rescue"]
        + c5["d2"]["rescue"]
    )
    if rescue_9b != 1:
        errors.append(f"9B_RESCUE_MISMATCH:{rescue_9b}")

    # Gemini
    g = json.loads(
        (
            ROOT
            / "docs/experiments/manifests/math16_cumulative_summary_gemini_fail_gated_authoritative_v1.json"
        ).read_text(encoding="utf-8")
    )
    if g["baseline"]["pass"] != 289 or g["final"]["pass"] != 289:
        errors.append("GEMINI_PASS_MISMATCH")
    if g["totals"]["verified_rescue"] != 0 or g["totals"]["regression"] != 0:
        errors.append("GEMINI_TOTALS_MISMATCH")

    # 4B C5a closure final pass
    c5a4 = json.loads(
        (ROOT / "docs/experiments/manifests/math16_c5a_final_source_closure_v1.json").read_text(
            encoding="utf-8"
        )
    )
    if c5a4["validation"]["pass_n"] != 88:
        errors.append(f"4B_C5A_PASS_MISMATCH:{c5a4['validation']['pass_n']}")

    # rate checks
    for key, m in MODELS.items():
        rate = pct(m["verified_rescue"], m["baseline_fail"])
        expected = {"qwen4b": 3.73, "qwen9b": 0.46, "gemini": 0.0}[key]
        if rate != expected:
            errors.append(f"RATE_MISMATCH:{key}:{rate}!={expected}")
    return errors


def build_summary(head: str) -> dict:
    ordered = sorted(MODELS.items(), key=lambda kv: kv[1]["display_order"])
    models_out = {}
    for key, m in MODELS.items():
        rate = pct(m["verified_rescue"], m["baseline_fail"])
        models_out[key] = {
            **m,
            "rescue_rate_pct_of_baseline_fail": rate,
            "rescue_over_baseline_fail": f"{m['verified_rescue']}/{m['baseline_fail']}",
            "total_cells": 320,
        }
    return {
        "status": "math16_three_model_round1_summary_v1",
        "verdict": "THREE_MODEL_ROUND1_COMPARISON_ARCHIVED",
        "round": 1,
        "round_role": "PRIMARY_FORMAL_ANALYSIS",
        "round2_status": "NOT_EXECUTED",
        "round2_policy": {
            "if_executed": "post_hoc_iterative_replay_only",
            "must_not_overwrite_round1_primary_tables": True,
        },
        "protocol": {
            "gating": "FAIL_ONLY_CUMULATIVE",
            "rounds": 1,
            "deterministic": True,
            "frozen_rules": True,
            "model_calls": 0,
        },
        "head_at_archive": head,
        "display_order": [k for k, _ in ordered],
        "models": models_out,
        "headline_table": [
            {
                "model": m["label"],
                "baseline_pass": m["baseline_pass"],
                "final_pass": m["final_pass"],
                "verified_rescue": m["verified_rescue"],
                "baseline_fail": m["baseline_fail"],
                "rescue_rate_pct": pct(m["verified_rescue"], m["baseline_fail"]),
                "regression": m["regression"],
            }
            for _, m in ordered
        ],
        "formal_conclusion_zh": FORMAL_CONCLUSION,
        "figures": {
            "baseline_vs_final": "docs/決賽文件/實驗結果文件/Math16/figures/figure_07_round1_baseline_vs_final.svg",
            "verified_rescue": "docs/決賽文件/實驗結果文件/Math16/figures/figure_08_round1_verified_rescue.svg",
            "pass_curves": "docs/決賽文件/實驗結果文件/Math16/figures/figure_09_round1_pass_curves.svg",
            "rescue_rate": "docs/決賽文件/實驗結果文件/Math16/figures/figure_10_round1_rescue_rate.svg",
            "chart_data": "docs/決賽文件/實驗結果文件/Math16/figures/round1_chart_data_v1.json",
        },
        "declarations": [
            "round1_is_primary_formal_analysis",
            "round2_not_executed",
            "no_causal_claim_model_scale_vs_rescue_rate",
            "no_modification_of_prior_model_artifacts",
            "no_model_calls",
        ],
    }


def setup_font() -> None:
    candidates = [
        "Microsoft JhengHei",
        "Microsoft YaHei",
        "Noto Sans CJK TC",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False


def save_fig(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight")
    plt.close(fig)


def render_figures(chart_data: dict) -> None:
    setup_font()
    order = chart_data["display_order"]
    labels = [MODELS[k]["label"] for k in order]
    colors = [COLORS[k] for k in order]

    # Fig 07 Baseline vs Final
    fig, ax = plt.subplots(figsize=(8.0, 4.8))
    x = range(len(order))
    w = 0.36
    base = [MODELS[k]["baseline_pass"] for k in order]
    final = [MODELS[k]["final_pass"] for k in order]
    ax.bar([i - w / 2 for i in x], base, width=w, label="Baseline PASS", color="#8D99AE")
    ax.bar([i + w / 2 for i in x], final, width=w, label="Final PASS", color="#2B2D42")
    for i, (b, f) in enumerate(zip(base, final)):
        ax.text(i - w / 2, b + 3, str(b), ha="center", va="bottom", fontsize=9)
        ax.text(i + w / 2, f + 3, str(f), ha="center", va="bottom", fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("PASS / 320")
    ax.set_ylim(0, 340)
    ax.set_title("Math16 Round 1 — Baseline vs Final PASS")
    ax.legend(frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    save_fig(fig, FIG_DIR / "figure_07_round1_baseline_vs_final.svg")

    # Fig 08 verified rescue
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    rescues = [MODELS[k]["verified_rescue"] for k in order]
    bars = ax.bar(labels, rescues, color=colors)
    for bar, v in zip(bars, rescues):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.15, str(v), ha="center", va="bottom")
    ax.set_ylabel("Verified rescue (cells)")
    ax.set_ylim(0, max(rescues) + 2)
    ax.set_title("Math16 Round 1 — Verified Rescue (4B=9, 9B=1, Gemini=0)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    save_fig(fig, FIG_DIR / "figure_08_round1_verified_rescue.svg")

    # Fig 09 pass curves
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    layers = ["C0", "C1", "C2", "C3", "C4", "C5a", "C5b", "C5c"]
    for k in order:
        ys = [MODELS[k]["pass_curve"][L] for L in layers]
        ax.plot(layers, ys, marker="o", linewidth=2.2, label=MODELS[k]["label"], color=COLORS[k])
    ax.set_ylabel("PASS / 320")
    ax.set_title("Math16 Round 1 — Cumulative PASS Curves")
    ax.set_ylim(0, 340)
    ax.legend(frameon=False)
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    save_fig(fig, FIG_DIR / "figure_09_round1_pass_curves.svg")

    # Fig 10 rescue rate
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    rates = [pct(MODELS[k]["verified_rescue"], MODELS[k]["baseline_fail"]) for k in order]
    dens = [f"{MODELS[k]['verified_rescue']}/{MODELS[k]['baseline_fail']}" for k in order]
    bars = ax.bar(labels, rates, color=colors)
    for bar, r, dens_s in zip(bars, rates, dens):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            r + 0.08,
            f"{r:.2f}%\n({dens_s})",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_ylabel("Rescue / Baseline FAIL (%)")
    ax.set_ylim(0, max(rates) + 1.2)
    ax.set_title("Math16 Round 1 — Rescue Rate of Baseline FAIL")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    save_fig(fig, FIG_DIR / "figure_10_round1_rescue_rate.svg")


def write_comparison_md(summary: dict) -> Path:
    path = OUT_DIR / "08_math16_three_model_aggressive_healer_round1_comparison_v1.md"
    rows = summary["headline_table"]
    lines = [
        "# Math16 三模型 Aggressive Healer Round 1 正式比較 v1",
        "",
        "> **Round 角色：** Round 1 = **正式主分析（Primary formal analysis）**",
        "> **Round 2：** **尚未執行**；若未來執行，僅作 post-hoc iterative replay，**不得覆寫 Round 1 主表**",
        f"> **Archive HEAD：** `{summary['head_at_archive']}`",
        "> **Protocol：** 凍結規則 × FAIL-only × 單輪 Deterministic Healer（不呼叫模型）",
        "",
        "---",
        "",
        "## 1. 核心統計",
        "",
        "| 模型 | Baseline PASS | Final PASS | verified rescue | Baseline FAIL | 修復率 | regression |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['model']} | {r['baseline_pass']}/320 | {r['final_pass']}/320 | "
            f"{r['verified_rescue']} | {r['baseline_fail']} | {r['rescue_rate_pct']:.2f}% | {r['regression']} |"
        )
    lines += [
        "",
        "修復率分母 = Baseline FAIL：",
        "",
        "- Qwen 4B：`9/241 = 3.73%`",
        "- Qwen 9B：`1/219 = 0.46%`",
        "- Gemini：`0/31 = 0%`",
        "",
        "## 2. Cumulative PASS 曲線",
        "",
        "| 模型 | C0 | C1 | C2 | C3 | C4 | C5a | C5b | C5c |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for key in summary["display_order"]:
        m = summary["models"][key]
        c = m["pass_curve"]
        lines.append(
            f"| {m['label']} | {c['C0']} | {c['C1']} | {c['C2']} | {c['C3']} | "
            f"{c['C4']} | {c['C5a']} | {c['C5b']} | {c['C5c']} |"
        )
    lines += [
        "",
        "## 3. 正式主結論",
        "",
        FORMAL_CONCLUSION,
        "",
        "## 4. Round 邊界",
        "",
        "| 項目 | 狀態 |",
        "|---|---|",
        "| Round 1 | **正式主分析**（本文件） |",
        "| Round 2 | **尚未執行** |",
        "| 未來 Round 2（若執行） | 僅 post-hoc iterative replay |",
        "| Round 2 可否覆寫 Round 1 主表 | **否** |",
        "",
        "## 5. 圖表",
        "",
        "| 圖 | 路徑 |",
        "|---|---|",
        f"| Baseline vs Final | `{summary['figures']['baseline_vs_final']}` |",
        f"| Verified rescue | `{summary['figures']['verified_rescue']}` |",
        f"| PASS 曲線 | `{summary['figures']['pass_curves']}` |",
        f"| Rescue rate | `{summary['figures']['rescue_rate']}` |",
        f"| 圖表資料 | `{summary['figures']['chart_data']}` |",
        "",
        "![Baseline vs Final](figures/figure_07_round1_baseline_vs_final.svg)",
        "",
        "![Verified rescue](figures/figure_08_round1_verified_rescue.svg)",
        "",
        "![PASS curves](figures/figure_09_round1_pass_curves.svg)",
        "",
        "![Rescue rate](figures/figure_10_round1_rescue_rate.svg)",
        "",
        "## 6. 來源追溯",
        "",
    ]
    for key in summary["display_order"]:
        m = summary["models"][key]
        lines.append(f"### {m['label']}")
        lines.append("")
        lines.append(f"- Authority note：{m['authority_note']}")
        for s in m["sources"]:
            lines.append(f"- `{s}`")
        lines.append("")
    lines += [
        "## 7. 聲明",
        "",
        "- 未執行 Round 2",
        "- 未呼叫模型",
        "- 未修改 frozen rules／guard／threshold／order",
        "- 未修改既有 4B／9B／Gemini 原始 artifacts（本輪僅新增比較封存產物與既有 Gemini Round 1 untracked 產物入庫）",
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


def write_teacher_brief(summary: dict) -> Path:
    path = OUT_DIR / "09_math16_three_model_round1_teacher_brief_v1.md"
    rows = summary["headline_table"]
    lines = [
        "# Math16 三模型 Round 1 — 老師展示摘要 v1",
        "",
        "> **一句話：** 同一套凍結 FAIL-only 單輪 Healer 下，4B／9B／Gemini 的 verified rescue 為 **9／1／0**；regression 皆為 **0**。",
        "",
        "## 核心數字",
        "",
        "| 模型 | Baseline → Final | rescue | 修復率（／Baseline FAIL） |",
        "|---|---|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['model']} | {r['baseline_pass']} → {r['final_pass']} | "
            f"{r['verified_rescue']} | {r['verified_rescue']}/{r['baseline_fail']} = {r['rescue_rate_pct']:.2f}% |"
        )
    lines += [
        "",
        "## 正式主結論（可直接引用）",
        "",
        FORMAL_CONCLUSION,
        "",
        "## 展示提醒",
        "",
        "- Round 1 是正式主分析；**Round 2 尚未執行**。",
        "- 不把「模型越大／Baseline 越高 → 修復率越高」講成普遍因果。",
        "- 重點講：**Healer 效益取決於 residual failure 是否落入 frozen safe-repair window**。",
        "",
        "## 建議展示圖",
        "",
        "1. `figures/figure_07_round1_baseline_vs_final.svg`",
        "2. `figures/figure_08_round1_verified_rescue.svg`",
        "3. `figures/figure_10_round1_rescue_rate.svg`",
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


def main() -> int:
    head = head_sha()
    errors = verify_against_sources()
    if errors:
        raise SystemExit("VERIFY_FAIL: " + "; ".join(errors))

    summary = build_summary(head)
    chart_data = {
        "status": "math16_three_model_round1_chart_data_v1",
        "derived_from": "docs/experiments/manifests/math16_three_model_round1_summary_v1.json",
        "display_order": summary["display_order"],
        "series": {
            key: {
                "label": MODELS[key]["label"],
                "baseline_pass": MODELS[key]["baseline_pass"],
                "final_pass": MODELS[key]["final_pass"],
                "verified_rescue": MODELS[key]["verified_rescue"],
                "baseline_fail": MODELS[key]["baseline_fail"],
                "rescue_rate_pct": pct(
                    MODELS[key]["verified_rescue"], MODELS[key]["baseline_fail"]
                ),
                "pass_curve": MODELS[key]["pass_curve"],
            }
            for key in summary["display_order"]
        },
        "notes": [
            "Rates use Baseline FAIL denominator",
            "Round 1 primary; Round 2 not executed",
        ],
    }

    render_figures(chart_data)

    summary_path = ROOT / "docs/experiments/manifests/math16_three_model_round1_summary_v1.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    chart_path = FIG_DIR / "round1_chart_data_v1.json"
    chart_path.write_text(
        json.dumps(chart_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    comp = write_comparison_md(summary)
    brief = write_teacher_brief(summary)

    # attach figure hashes for traceability
    fig_hashes = {
        rel: sha256_path(ROOT / rel)
        for rel in summary["figures"].values()
    }
    summary["figure_sha256"] = fig_hashes
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print("OK")
    print(json.dumps({"summary": str(summary_path), "comparison": str(comp), "brief": str(brief), "figures": list(summary["figures"].values())}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
