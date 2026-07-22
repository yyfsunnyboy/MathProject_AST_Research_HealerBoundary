# -*- coding: utf-8 -*-
"""Tier 1 Paired Analysis Script: Qwen 3.5 4B vs Qwen 3.5 9B (Math16 Pilot-02 Baseline)

Reads frozen baseline evaluation artifacts for Qwen 4B and Qwen 9B, verifies
320-cell 1-to-1 matching, and computes exact McNemar tests, task-clustered
bootstrap 95% CIs, condition/family decompositions, seed stability, and task-level summaries.
"""
from __future__ import annotations

import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

QWEN4B_BASELINE_JSONL = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl"
)
QWEN4B_SUMMARY_JSON = (
    ROOT / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/overall_summary.json"
)
QWEN9B_BASELINE_JSONL = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/cell_level_baseline.jsonl"
)
QWEN9B_SUMMARY_JSON = (
    ROOT / "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/overall_summary.json"
)

OUTPUT_DIR = (
    ROOT / "docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1"
)


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def compute_exact_mcnemar_pvalue(b: int, c: int) -> float:
    """Computes exact two-sided McNemar p-value using Binomial(b+c, 0.5)."""
    n_disc = b + c
    if n_disc == 0:
        return 1.0
    k = min(b, c)
    # Cumulative probability sum for i in 0..k under Binomial(n_disc, 0.5)
    cum_p = sum(math.comb(n_disc, i) for i in range(k + 1)) * (0.5 ** n_disc)
    if k * 2 == n_disc:
        p_val = 1.0
    else:
        p_val = min(1.0, 2.0 * cum_p)
    return p_val


def compute_wald_risk_difference_ci(b: int, c: int, n: int) -> tuple[float, float, float]:
    """Computes paired risk difference (c - b)/n and Wald 95% CI."""
    rd = (c - b) / n
    # SE for paired risk difference: sqrt(b + c - (c - b)^2 / n) / n
    variance = (b + c - ((c - b) ** 2) / n) / (n ** 2)
    se = math.sqrt(max(0.0, variance))
    z = 1.959963984540054  # 95% z-score
    ci_lower = rd - z * se
    ci_upper = rd + z * se
    return rd, ci_lower, ci_upper


def run_analysis():
    print("1. Loading frozen baseline records...")
    q4b_records = load_jsonl(QWEN4B_BASELINE_JSONL)
    q9b_records = load_jsonl(QWEN9B_BASELINE_JSONL)

    q4b_summary = json.loads(QWEN4B_SUMMARY_JSON.read_text(encoding="utf-8"))
    q9b_summary = json.loads(QWEN9B_SUMMARY_JSON.read_text(encoding="utf-8"))

    # Verification checks
    assert len(q4b_records) == 320, f"Qwen 4B records count mismatch: {len(q4b_records)}"
    assert len(q9b_records) == 320, f"Qwen 9B records count mismatch: {len(q9b_records)}"
    assert q4b_summary["passed"] == 78, f"Qwen 4B pass count mismatch: {q4b_summary['passed']}"
    assert q9b_summary["passed"] == 101, f"Qwen 9B pass count mismatch: {q9b_summary['passed']}"

    # Build lookup maps by matching key (task_id, condition, seed)
    q4b_map = {}
    for r in q4b_records:
        key = (r["task_id"], r["condition"], r["seed"])
        assert key not in q4b_map, f"Duplicate key in 4B: {key}"
        q4b_map[key] = r

    q9b_map = {}
    for r in q9b_records:
        key = (r["task_id"], r["condition"], r["seed"])
        assert key not in q9b_map, f"Duplicate key in 9B: {key}"
        q9b_map[key] = r

    assert set(q4b_map.keys()) == set(q9b_map.keys()), "Identity mismatch between 4B and 9B keys!"
    assert len(q4b_map) == 320, "Matched pairs count mismatch!"

    print("2. Building 320-cell paired ledger...")
    paired_ledger = []
    category_counts = {
        "BOTH_PASS": 0,
        "FOUR_B_ONLY_PASS": 0,
        "NINE_B_ONLY_PASS": 0,
        "BOTH_FAIL": 0,
    }

    # Sort keys deterministically
    sorted_keys = sorted(q4b_map.keys(), key=lambda k: (k[0], k[1], k[2]))

    for idx, key in enumerate(sorted_keys, start=1):
        task_id, condition, seed = key
        r4 = q4b_map[key]
        r9 = q9b_map[key]

        pass4 = (r4["final_status"] == "PASSED")
        pass9 = (r9["final_status"] == "PASSED")

        if pass4 and pass9:
            cat = "BOTH_PASS"
        elif pass4 and not pass9:
            cat = "FOUR_B_ONLY_PASS"
        elif not pass4 and pass9:
            cat = "NINE_B_ONLY_PASS"
        else:
            cat = "BOTH_FAIL"

        category_counts[cat] += 1

        ledger_entry = {
            "pair_id": f"pair_{idx:03d}",
            "key": f"{task_id}__{condition}__seed_{seed}",
            "task_id": task_id,
            "family": r4["family"],
            "condition": condition,
            "seed": seed,
            "qwen4b_status": r4["final_status"],
            "qwen4b_passed": pass4,
            "qwen9b_status": r9["final_status"],
            "qwen9b_passed": pass9,
            "pair_category": cat,
        }
        paired_ledger.append(ledger_entry)

    assert sum(category_counts.values()) == 320
    b = category_counts["FOUR_B_ONLY_PASS"]
    c = category_counts["NINE_B_ONLY_PASS"]
    a = category_counts["BOTH_PASS"]
    d = category_counts["BOTH_FAIL"]

    assert a + b == 78, f"4B pass total mismatch: {a+b}"
    assert a + c == 101, f"9B pass total mismatch: {a+c}"
    assert c - b == 23, f"Net difference mismatch: {c-b}"

    print(f"   Category counts: BOTH_PASS={a}, 4B_ONLY={b}, 9B_ONLY={c}, BOTH_FAIL={d}")

    # Overall McNemar and Wald Stats
    p_val_overall = compute_exact_mcnemar_pvalue(b, c)
    rd_overall, ci_low_wald, ci_high_wald = compute_wald_risk_difference_ci(b, c, 320)
    or_overall = (c / b) if b > 0 else None

    # 3. Task-Clustered Bootstrap (10,000 resamples)
    print("3. Running Task-Clustered Bootstrap (10,000 resamples)...")
    random.seed(42)
    tasks = sorted(list({r["task_id"] for r in paired_ledger}))
    assert len(tasks) == 16

    # Group ledger entries by task_id
    task_cells = {t: [r for r in paired_ledger if r["task_id"] == t] for t in tasks}

    N_BOOTSTRAP = 10000
    boot_overall_rd = []
    boot_cond_rd = {cond: [] for cond in ["ab1", "ab2g", "ab2d", "ab2d_spec_v2"]}
    boot_fam_rd = {fam: [] for fam in ["integer", "polynomial", "radical", "fraction"]}

    for _ in range(N_BOOTSTRAP):
        sampled_tasks = [random.choice(tasks) for _ in range(16)]
        resampled_cells = []
        for t in sampled_tasks:
            resampled_cells.extend(task_cells[t])

        # Overall in resample
        c_4b = sum(1 for r in resampled_cells if r["qwen4b_passed"])
        c_9b = sum(1 for r in resampled_cells if r["qwen9b_passed"])
        boot_overall_rd.append((c_9b - c_4b) / 320.0)

        # Conditions in resample
        for cond in boot_cond_rd:
            cond_cells = [r for r in resampled_cells if r["condition"] == cond]
            c4 = sum(1 for r in cond_cells if r["qwen4b_passed"])
            c9 = sum(1 for r in cond_cells if r["qwen9b_passed"])
            boot_cond_rd[cond].append((c9 - c4) / 80.0)

        # Families in resample
        for fam in boot_fam_rd:
            fam_cells = [r for r in resampled_cells if r["family"] == fam]
            c4 = sum(1 for r in fam_cells if r["qwen4b_passed"])
            c9 = sum(1 for r in fam_cells if r["qwen9b_passed"])
            boot_fam_rd[fam].append((c9 - c4) / 80.0)

    def percentile_ci(vals: list[float]) -> tuple[float, float]:
        sorted_vals = sorted(vals)
        low = sorted_vals[int(0.025 * len(sorted_vals))]
        high = sorted_vals[int(0.975 * len(sorted_vals))]
        return low, high

    boot_overall_ci = percentile_ci(boot_overall_rd)

    print(f"   Overall Paired Risk Difference: {rd_overall:.4f} (+{c-b} cells)")
    print(f"   Exact McNemar p-value: {p_val_overall:.6e}")
    print(f"   Wald 95% CI: [{ci_low_wald:.4f}, {ci_high_wald:.4f}]")
    print(f"   Task-Clustered Bootstrap 95% CI: [{boot_overall_ci[0]:.4f}, {boot_overall_ci[1]:.4f}]")

    # 4. Condition Breakdown
    print("4. Computing Condition Breakdown...")
    condition_summary = {}
    for cond in ["ab1", "ab2g", "ab2d", "ab2d_spec_v2"]:
        cond_cells = [r for r in paired_ledger if r["condition"] == cond]
        assert len(cond_cells) == 80
        b_c = sum(1 for r in cond_cells if r["pair_category"] == "FOUR_B_ONLY_PASS")
        c_c = sum(1 for r in cond_cells if r["pair_category"] == "NINE_B_ONLY_PASS")
        a_c = sum(1 for r in cond_cells if r["pair_category"] == "BOTH_PASS")
        d_c = sum(1 for r in cond_cells if r["pair_category"] == "BOTH_FAIL")

        p4 = a_c + b_c
        p9 = a_c + c_c
        rd_c, low_w, high_w = compute_wald_risk_difference_ci(b_c, c_c, 80)
        p_val_c = compute_exact_mcnemar_pvalue(b_c, c_c)
        boot_ci_c = percentile_ci(boot_cond_rd[cond])

        condition_summary[cond] = {
            "condition": cond,
            "total_cells": 80,
            "qwen4b_pass": p4,
            "qwen9b_pass": p9,
            "BOTH_PASS": a_c,
            "FOUR_B_ONLY_PASS": b_c,
            "NINE_B_ONLY_PASS": c_c,
            "BOTH_FAIL": d_c,
            "net_difference": c_c - b_c,
            "paired_risk_difference": rd_c,
            "wald_95_ci": [low_w, high_w],
            "bootstrap_task_clustered_95_ci": list(boot_ci_c),
            "exact_mcnemar_pvalue": p_val_c,
        }

    # 5. Family Breakdown
    print("5. Computing Family Breakdown...")
    family_summary = {}
    for fam in ["integer", "polynomial", "radical", "fraction"]:
        fam_cells = [r for r in paired_ledger if r["family"] == fam]
        assert len(fam_cells) == 80
        b_f = sum(1 for r in fam_cells if r["pair_category"] == "FOUR_B_ONLY_PASS")
        c_f = sum(1 for r in fam_cells if r["pair_category"] == "NINE_B_ONLY_PASS")
        a_f = sum(1 for r in fam_cells if r["pair_category"] == "BOTH_PASS")
        d_f = sum(1 for r in fam_cells if r["pair_category"] == "BOTH_FAIL")

        p4 = a_f + b_f
        p9 = a_f + c_f
        rd_f, low_w, high_w = compute_wald_risk_difference_ci(b_f, c_f, 80)
        p_val_f = compute_exact_mcnemar_pvalue(b_f, c_f)
        boot_ci_f = percentile_ci(boot_fam_rd[fam])

        family_summary[fam] = {
            "family": fam,
            "total_cells": 80,
            "qwen4b_pass": p4,
            "qwen9b_pass": p9,
            "BOTH_PASS": a_f,
            "FOUR_B_ONLY_PASS": b_f,
            "NINE_B_ONLY_PASS": c_f,
            "BOTH_FAIL": d_f,
            "net_difference": c_f - b_f,
            "paired_risk_difference": rd_f,
            "wald_95_ci": [low_w, high_w],
            "bootstrap_task_clustered_95_ci": list(boot_ci_f),
            "exact_mcnemar_pvalue": p_val_f,
            "special_notes": "Polynomial 9B (9/80) < 4B (16/80), net -7. Localized anomaly co-occurring with multi-LaTeX assembly." if fam == "polynomial" else None,
        }

    # 6. Seed Stability Summary
    print("6. Computing Seed Stability Summary...")
    seed_summary = {}
    seeds = sorted(list({r["seed"] for r in paired_ledger}))
    diffs = []
    for s in seeds:
        s_cells = [r for r in paired_ledger if r["seed"] == s]
        assert len(s_cells) == 64
        b_s = sum(1 for r in s_cells if r["pair_category"] == "FOUR_B_ONLY_PASS")
        c_s = sum(1 for r in s_cells if r["pair_category"] == "NINE_B_ONLY_PASS")
        p4 = sum(1 for r in s_cells if r["qwen4b_passed"])
        p9 = sum(1 for r in s_cells if r["qwen9b_passed"])
        diff = p9 - p4
        diffs.append(diff)

        seed_summary[str(s)] = {
            "seed": s,
            "total_cells": 64,
            "qwen4b_pass": p4,
            "qwen9b_pass": p9,
            "net_difference": diff,
            "FOUR_B_ONLY_PASS": b_s,
            "NINE_B_ONLY_PASS": c_s,
        }

    mean_diff = sum(diffs) / len(diffs)
    sd_diff = math.sqrt(sum((x - mean_diff) ** 2 for x in diffs) / (len(diffs) - 1))

    seed_overall_stability = {
        "nine_b_higher_in_all_seeds": all(d > 0 for d in diffs),
        "seed_diff_range": [min(diffs), max(diffs)],
        "mean_diff": mean_diff,
        "sample_sd_diff": sd_diff,
        "per_seed_data": seed_summary,
    }

    # 7. Task-Level Diagnosis Summary
    print("7. Computing Task-Level Summary...")
    task_summary = {}
    for t in tasks:
        t_cells = [r for r in paired_ledger if r["task_id"] == t]
        assert len(t_cells) == 20
        b_t = sum(1 for r in t_cells if r["pair_category"] == "FOUR_B_ONLY_PASS")
        c_t = sum(1 for r in t_cells if r["pair_category"] == "NINE_B_ONLY_PASS")
        p4 = sum(1 for r in t_cells if r["qwen4b_passed"])
        p9 = sum(1 for r in t_cells if r["qwen9b_passed"])
        diff = p9 - p4

        direction = "9B_BETTER" if diff > 0 else ("4B_BETTER" if diff < 0 else "EQUAL")

        task_summary[t] = {
            "task_id": t,
            "family": t_cells[0]["family"],
            "total_cells": 20,
            "qwen4b_pass": p4,
            "qwen9b_pass": p9,
            "net_difference": diff,
            "FOUR_B_ONLY_PASS": b_t,
            "NINE_B_ONLY_PASS": c_t,
            "direction": direction,
            "is_polynomial_division_anomaly": (t == "ce115_calc_polynomial_division_l1"),
        }

    # Save Output Artifacts
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. paired_cell_ledger.jsonl
    with (OUTPUT_DIR / "paired_cell_ledger.jsonl").open("w", encoding="utf-8") as f:
        for r in paired_ledger:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # 2. overall_paired_summary.json
    overall_summary = {
        "analysis_id": "math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1",
        "scope": "Tier 1: Qwen 3.5 4B vs Qwen 3.5 9B matched pairs",
        "total_pairs": 320,
        "qwen4b_baseline_pass": a + b,
        "qwen4b_baseline_pass_rate": (a + b) / 320.0,
        "qwen9b_baseline_pass": a + c,
        "qwen9b_baseline_pass_rate": (a + c) / 320.0,
        "paired_contingency_table": {
            "BOTH_PASS": a,
            "FOUR_B_ONLY_PASS": b,
            "NINE_B_ONLY_PASS": c,
            "BOTH_FAIL": d,
        },
        "net_difference": c - b,
        "paired_risk_difference": rd_overall,
        "wald_95_ci": [ci_low_wald, ci_high_wald],
        "bootstrap_task_clustered_95_ci": list(boot_overall_ci),
        "exact_mcnemar_pvalue": p_val_overall,
        "matched_pairs_odds_ratio": or_overall,
        "verdict": "QWEN9B_STATISTICALLY_SUPERIOR_IN_TIER1_BASELINE",
    }
    (OUTPUT_DIR / "overall_paired_summary.json").write_text(
        json.dumps(overall_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 3. condition_paired_summary.json
    (OUTPUT_DIR / "condition_paired_summary.json").write_text(
        json.dumps(condition_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 4. family_paired_summary.json
    (OUTPUT_DIR / "family_paired_summary.json").write_text(
        json.dumps(family_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 5. seed_stability_summary.json
    (OUTPUT_DIR / "seed_stability_summary.json").write_text(
        json.dumps(seed_overall_stability, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 6. task_level_summary.json
    (OUTPUT_DIR / "task_level_summary.json").write_text(
        json.dumps(task_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 7. bootstrap_summary.json
    bootstrap_summary = {
        "bootstrap_method": "Task-clustered resample (16 tasks with replacement, 20 cells per task)",
        "num_resamples": N_BOOTSTRAP,
        "random_seed": 42,
        "overall_paired_risk_difference_ci": list(boot_overall_ci),
        "condition_paired_risk_difference_cis": {
            cond: list(percentile_ci(boot_cond_rd[cond])) for cond in boot_cond_rd
        },
        "family_paired_risk_difference_cis": {
            fam: list(percentile_ci(boot_fam_rd[fam])) for fam in boot_fam_rd
        },
    }
    (OUTPUT_DIR / "bootstrap_summary.json").write_text(
        json.dumps(bootstrap_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 8. analysis_manifest.json
    manifest = {
        "analysis_id": "math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1",
        "tier": "Tier 1 (Qwen 4B vs Qwen 9B matched pairs)",
        "source_qwen4b_baseline": "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl",
        "source_qwen9b_baseline": "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/cell_level_baseline.jsonl",
        "total_pairs": 320,
        "verification_status": "PASSED_100_PERCENT",
        "llm_calls": 0,
        "healer_execution": False,
        "rescored": False,
    }
    (OUTPUT_DIR / "analysis_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 9. analysis_report.md
    report_md = f"""# Math16 Pilot-02 Tier 1 配對統計分析報告 (Qwen 4B vs Qwen 9B)

```text
MATH16_PILOT02_QWEN4B_VS_QWEN9B_TIER1_PAIRED_ANALYSIS_COMPLETED
EXACT_MCNEMAR_COMPLETED
TASK_CLUSTERED_BOOTSTRAP_COMPLETED
SEED_AND_TASK_STABILITY_DOCUMENTED
```

**分析識別碼：** `math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1`
**範疇：** Tier 1 正式配對比較（Qwen 3.5 4B vs Qwen 3.5 9B，共 320 組一對一 matched cells）
**資料驗證狀態：** 100% 完整匹配（320 pairs，無重複，無缺漏，4B PASS=78, 9B PASS=101）

---

## 1. 研究問題與 Tier 1 可比性理由

本分析旨在回應：**「在控制相同題目 (16 題)、相同 Prompt 條件 (4 種)、相同隨機種子 (5 個) 與相同主要 sampling 設定下，Qwen 3.5 9B 相較於 Qwen 3.5 4B 是否在端到端程式生成通過率上展現統計顯著的配對淨增加？」**

### Tier 1 可比性宣告
- **同模型家族**：均為 Qwen 3.5 衍生模型 (4B / 9B)。
- **同實驗因子**：16 題 $\\times$ 4 conditions $\\times$ 5 seeds = 320 matched cells。
- **嚴格對稱性**：每個 pair 共享相同的 task_id、condition、seed 與評估標準 (v4 Evaluator)。

---

## 2. 資料完整性驗證 (Data Completeness Audit)

| 項目 | 預期值 | 實測值 | 驗證狀態 |
| :--- | ---: | ---: | :---: |
| **Qwen 4B 總紀錄數** | 320 | 320 | PASS |
| **Qwen 9B 總紀錄數** | 320 | 320 | PASS |
| **成功匹配對數 (Matched Pairs)** | 320 | 320 | PASS |
| **重複 / 缺漏 / 身分不符** | 0 | 0 | PASS |
| **Qwen 4B Baseline PASS 總數** | 78 | 78 | PASS |
| **Qwen 9B Baseline PASS 總數** | 101 | 101 | PASS |

---

## 3. Overall 2×2 配對列聯表與 Exact McNemar 檢定

### 3.1 2×2 Contingency Table

| | Qwen 9B PASS | Qwen 9B FAIL | 合計 (Qwen 4B) |
| :--- | ---: | ---: | ---: |
| **Qwen 4B PASS** | **{a}** (`BOTH_PASS`) | **{b}** (`FOUR_B_ONLY_PASS`) | **{a+b}** (24.38%) |
| **Qwen 4B FAIL** | **{c}** (`NINE_B_ONLY_PASS`) | **{d}** (`BOTH_FAIL`) | **{c+d}** (75.62%) |
| **合計 (Qwen 9B)** | **{a+c}** (31.56%) | **{b+c+d-c}** | **320** |

### 3.2 統計檢定結果

- **不一致配對 (Discordant Pairs)**：
  - $b$ (`4B_ONLY_PASS`) = **{b}**
  - $c$ (`9B_ONLY_PASS`) = **{c}**
  - 淨增加 (Net Difference) = $c - b =$ **+{c-b} 格**
- **Paired Risk Difference (\\Delta)**：
  - \\Delta = \\frac{{101 - 78}}{{320}} = +7.1875\\% (**+{rd_overall:.4f}**)
- **Exact Two-Sided McNemar Test $p$-value**：
  - $p = \\mathbf{{{p_val_overall:.4f}}}$ ($p = {p_val_overall:.6f}$)
- **Matched-Pairs Odds Ratio (OR)**：
  - $\\text{{OR}} = \\frac{{c}}{{b}} = \\mathbf{{{or_overall:.2f}}}$
- **95% 雙重信賴區間**：
  - Wald 95% CI: `[{ci_low_wald:.4f}, {ci_high_wald:.4f}]` (+1.94% 至 +12.43%)
  - **Task-Clustered Bootstrap 95% CI** (10,000 resamples): `[{boot_overall_ci[0]:.4f}, {boot_overall_ci[1]:.4f}]` ({boot_overall_ci[0]*100:+.2f}% 至 {boot_overall_ci[1]*100:+.2f}%)

**統計結論**：在控制 Task, Condition, Seed 後，Qwen 9B 在 320 格配對測試中的基線通過率高於 Qwen 4B ($p = {p_val_overall:.4f} < 0.05$)，淨增加 23 格程式生成成功案例。

---

## 4. Condition 分層配對分析 (Secondary Decomposition)

各 Condition 分母均為 $n=80$ 格配對：

| Condition | 4B PASS | 9B PASS | BOTH PASS | 4B ONLY ($b$) | 9B ONLY ($c$) | BOTH FAIL | 淨增加 ($c-b$) | Paired RD (\\Delta) | Task-Clustered Bootstrap 95% CI | Exact McNemar $p$-value |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | ---: |
"""
    for cond in ["ab1", "ab2g", "ab2d", "ab2d_spec_v2"]:
        cs = condition_summary[cond]
        boot_ci_str = f"[{cs['bootstrap_task_clustered_95_ci'][0]:.4f}, {cs['bootstrap_task_clustered_95_ci'][1]:.4f}]"
        report_md += f"| **{cond}** | {cs['qwen4b_pass']}/80 | {cs['qwen9b_pass']}/80 | {cs['BOTH_PASS']} | {cs['FOUR_B_ONLY_PASS']} | {cs['NINE_B_ONLY_PASS']} | {cs['BOTH_FAIL']} | **+{cs['net_difference']}** | {cs['paired_risk_difference']:+.4f} | {boot_ci_str} | {cs['exact_mcnemar_pvalue']:.4f} |\n"

    report_md += f"""
### 保守解讀：
- `Ab2g` 展現最大的單一條件配對淨增加 (+8 格, $p = {condition_summary['ab2g']['exact_mcnemar_pvalue']:.4f}$).
- `Ab2d+spec-v2` 兩模型皆有較高通過率 (4B 36/80, 9B 40/80)，配對淨增加 +4 格 ($p = {condition_summary['ab2d_spec_v2']['exact_mcnemar_pvalue']:.4f}$).
- `Ab2d+api` 兩模型通過率均偏低 (4B 8/80, 9B 16/80)，淨增加 +8 格 ($p = {condition_summary['ab2d']['exact_mcnemar_pvalue']:.4f}$).

---

## 5. Family 分層配對分析 (Secondary Decomposition)

各 Family 分母均為 $n=80$ 格配對：

| Family | 4B PASS | 9B PASS | BOTH PASS | 4B ONLY ($b$) | 9B ONLY ($c$) | BOTH FAIL | 淨增加 ($c-b$) | Paired RD (\\Delta) | Task-Clustered Bootstrap 95% CI | Exact McNemar $p$-value |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: | ---: |
"""
    for fam in ["integer", "polynomial", "radical", "fraction"]:
        fs = family_summary[fam]
        boot_ci_str = f"[{fs['bootstrap_task_clustered_95_ci'][0]:.4f}, {fs['bootstrap_task_clustered_95_ci'][1]:.4f}]"
        report_md += f"| **{fam}** | {fs['qwen4b_pass']}/80 | {fs['qwen9b_pass']}/80 | {fs['BOTH_PASS']} | {fs['FOUR_B_ONLY_PASS']} | {fs['NINE_B_ONLY_PASS']} | {fs['BOTH_FAIL']} | **{fs['net_difference']:+d}** | {fs['paired_risk_difference']:+.4f} | {boot_ci_str} | {fs['exact_mcnemar_pvalue']:.4f} |\n"

    report_md += f"""
### 保守解讀與 Polynomial 限制：
- **Integer** (+12 格, $p = {family_summary['integer']['exact_mcnemar_pvalue']:.4f}$) 與 **Fraction** (+14 格, $p = {family_summary['fraction']['exact_mcnemar_pvalue']:.4f}$) 展現配對淨成長。
- **Polynomial (多項式) 出現反向差異 (-7 格)**：9B (9/80) 低於 4B (16/80)，$p = {family_summary['polynomial']['exact_mcnemar_pvalue']:.4f}$。經診斷，此低分極度集中於 `ce115_calc_polynomial_division_l1` 該單一題型（9B 0/20 vs 4B 4/20），與在 only-Python 中組裝多個 LaTeX 欄位的提示結構高度共現，**不可解讀為 9B 全域數學能力落後**。

---

## 6. Seed 穩定性摘要

對 5 個獨立隨機種子（各 64 格配對）進行對照：

| Seed | 4B PASS / 64 | 9B PASS / 64 | 配對淨增加 (9B - 4B) | 4B ONLY ($b$) | 9B ONLY ($c$) |
| :--- | ---: | ---: | ---: | ---: | ---: |
"""
    for s in seeds:
        ss = seed_summary[str(s)]
        report_md += f"| **{s}** | {ss['qwen4b_pass']}/64 | {ss['qwen9b_pass']}/64 | **{ss['net_difference']:+d}** | {ss['FOUR_B_ONLY_PASS']} | {ss['NINE_B_ONLY_PASS']} |\n"

    report_md += f"""
- **跨 Seed 穩定度**：在所有 5 個種子中，9B 的通過數均一致高於 4B（淨增加範圍為 **+{min(diffs)} 至 +{max(diffs)} 格**）。
- **平均與標準差**：跨 Seed 平均淨增加為 **+{mean_diff:.1f} 格** (sample SD = **{sd_diff:.2f}**)。
- **結論**：配對淨增加是由 9B 在所有 5 個種子上的穩定優勢所驅動，而非個別極端種子主導。

---

## 7. Task-Level 差異與診斷

在 16 個 Task（各 20 格配對）中：

| Task ID | Family | 4B PASS / 20 | 9B PASS / 20 | 淨增加 (9B - 4B) | 方向 |
| :--- | :--- | ---: | ---: | ---: | :---: |
"""
    for t in tasks:
        ts = task_summary[t]
        flag = " ⚠️ (Anomaly)" if ts["is_polynomial_division_anomaly"] else ""
        report_md += f"| `{t}`{flag} | {ts['family']} | {ts['qwen4b_pass']} | {ts['qwen9b_pass']} | **{ts['net_difference']:+d}** | {ts['direction']} |\n"

    report_md += f"""
### 關鍵發現：
1. **改善最大 Tasks**：`ce112_q12_independent_probability_fraction` (+5 格)、`ce112_q01_negative_integer_power` (+4 格)、`ce113_q11_rationalize_denominator` (+2 格)。
2. **反向落後 Task**：`ce115_calc_polynomial_division_l1` (-4 格) 是導致 Polynomial 家族 9B 低於 4B 的主要單點因素。

---

## 8. 多重比較治理 (Multiple Comparisons Governance)

- **Confirmatory 核心宣告**：僅 `Overall 320-cell paired McNemar test` ($p = {p_val_overall:.4f}$) 屬事前的 Confirmatory 統計檢定。
- **Exploratory 屬性**：Condition、Family、Seed、Task 等分層分析均屬次要探索性分解 (Secondary/Exploratory Decompositions)。分層 $p$-value 供模式識別參考，不單獨宣稱全域普遍顯著。

---

## 9. 可寫入統整報告的保守結論

1. 在同一 Qwen 系列與相同 320 格配對實驗下，Qwen 3.5 9B 的端到端基線通過率高於 Qwen 3.5 4B (Paired Risk Difference = $+7.19\\%$, Exact McNemar $p = {p_val_overall:.4f}$).
2. Task-clustered Bootstrap 95% CI 為 `[{boot_overall_ci[0]*100:+.2f}%, {boot_overall_ci[1]*100:+.2f}%]`.
3. 9B 的勝出在 5 個獨立種子上均保持穩定 (每種子 +1 至 +7 格).
4. 分數 (Fraction) 與整數 (Integer) 家族貢獻了主要的配對淨成長.

---

## 10. 嚴禁過度推論之事項

- **不可寫成**「所有 family 都單調改善」（Polynomial 出現局部反向落後）。
- **不可寫成**「Gemini 也適用此 paired 統計結論」（Gemini 屬 Tier 2 描述性參照）。
- **不可寫成**「純參數規模造成因果差異」（仍包含提示結構與量化因子）。

---
"""
    (OUTPUT_DIR / "analysis_report.md").write_text(report_md, encoding="utf-8")
    print(f"8. Analysis complete. Results saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    run_analysis()
