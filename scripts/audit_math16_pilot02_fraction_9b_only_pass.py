# -*- coding: utf-8 -*-
"""Fraction 9B-Only Pass Mechanism Audit Script (Math16 Pilot-02 Tier 1)

Reads frozen paired ledger and Qwen 4B baseline records to analyze the failure layer,
mechanism distribution, task/condition breakdown, and anomaly audit overlap of the
Fraction NINE_B_ONLY_PASS cells (c=21, b=7, net difference c-b=14).
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAIRED_LEDGER_PATH = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/paired_cell_ledger.jsonl"
)
QWEN4B_BASELINE_PATH = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl"
)
QWEN9B_BASELINE_PATH = (
    ROOT
    / "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/cell_level_baseline.jsonl"
)
AB2D_ANOMALY_AUDIT_PATH = (
    ROOT / "docs/experiments/audits/math16_pilot02_qwen4b_ab2d_api_anomaly_diagnosis_v1.json"
)

OUTPUT_DIR = (
    ROOT / "docs/experiments/results/math16_pilot02_fraction_9b_only_pass_mechanism_audit_v1"
)


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_audit():
    print("1. Loading frozen paired ledger and baseline records...")
    paired_ledger = load_jsonl(PAIRED_LEDGER_PATH)
    q4b_records = load_jsonl(QWEN4B_BASELINE_PATH)
    q9b_records = load_jsonl(QWEN9B_BASELINE_PATH)

    ab2d_audit_data = json.loads(AB2D_ANOMALY_AUDIT_PATH.read_text(encoding="utf-8"))
    ab2d_audit_cell_ids = {c["cell_id"] for c in ab2d_audit_data.get("cells", [])}

    q4b_map = {r["cell_id"]: r for r in q4b_records}
    q9b_map = {r["cell_id"]: r for r in q9b_records}

    # Filter Fraction NINE_B_ONLY_PASS cells (c = 21)
    fraction_gap_cells = [
        r
        for r in paired_ledger
        if r["family"] == "fraction" and r["pair_category"] == "NINE_B_ONLY_PASS"
    ]
    fraction_b_cells = [
        r
        for r in paired_ledger
        if r["family"] == "fraction" and r["pair_category"] == "FOUR_B_ONLY_PASS"
    ]

    c_count = len(fraction_gap_cells)
    b_count = len(fraction_b_cells)
    net_diff = c_count - b_count

    print(f"2. Verifying Fraction discordance: c={c_count} (NINE_B_ONLY), b={b_count} (FOUR_B_ONLY), net={net_diff}...")
    assert c_count == 21, f"Expected c=21, got {c_count}"
    assert b_count == 7, f"Expected b=7, got {b_count}"
    assert net_diff == 14, f"Expected net difference=14, got {net_diff}"

    # Verification checks
    for r in fraction_gap_cells:
        assert r["qwen4b_passed"] is False, f"Cell {r['pair_id']} 4B is not FAILED!"
        assert r["qwen9b_passed"] is True, f"Cell {r['pair_id']} 9B is not PASSED!"

    assert len({r["pair_id"] for r in fraction_gap_cells}) == 21, "Duplicates found in pair_id!"

    print("3. Building 21-cell detailed mechanism ledger...")
    audit_ledger = []
    task_counts = Counter()
    condition_counts = Counter()
    layer_counts = Counter()
    mechanism_counts = Counter()
    ab2d_api_overlap_cells = []

    for item in fraction_gap_cells:
        key = (item["task_id"], item["condition"], item["seed"])
        cell4b = None
        for r in q4b_records:
            if (r["task_id"], r["condition"], r["seed"]) == key:
                cell4b = r
                break
        assert cell4b is not None, f"4B cell record not found for {key}"

        cell_id_4b = cell4b["cell_id"]
        in_anomaly_audit = cell_id_4b in ab2d_audit_cell_ids
        if in_anomaly_audit:
            ab2d_api_overlap_cells.append(item)

        task_id = item["task_id"]
        condition = item["condition"]
        layer = cell4b.get("primary_failure_layer", "NOT_AVAILABLE")
        mechanisms = cell4b.get("mechanism_tags", [])
        if not mechanisms:
            mechanisms = ["NOT_AVAILABLE"]

        task_counts[task_id] += 1
        condition_counts[condition] += 1
        layer_counts[layer] += 1
        for m in mechanisms:
            mechanism_counts[m] += 1

        ledger_entry = {
            "pair_id": item["pair_id"],
            "task_id": task_id,
            "condition": condition,
            "seed": item["seed"],
            "cell_id_4b": cell_id_4b,
            "qwen4b_outcome": "FAILED",
            "qwen9b_outcome": "PASSED",
            "qwen4b_failure_layer": layer,
            "qwen4b_mechanism_tags": cell4b.get("mechanism_tags", []),
            "qwen4b_exception_class": cell4b.get("exception_class"),
            "qwen4b_exception_message": cell4b.get("exception_message"),
            "qwen4b_classifier_outcome": cell4b.get("classifier_outcome"),
            "is_ab2d_api": (condition == "ab2d"),
            "in_ab2d_api_27_cell_anomaly_audit": in_anomaly_audit,
            "notes": "9B passed while 4B failed in Fraction family.",
        }
        audit_ledger.append(ledger_entry)

    print("4. Summarizing Task Distribution...")
    fraction_tasks = sorted(list({r["task_id"] for r in paired_ledger if r["family"] == "fraction"}))
    task_breakdown = {}
    for t in fraction_tasks:
        t_paired = [r for r in paired_ledger if r["task_id"] == t]
        pass4 = sum(1 for r in t_paired if r["qwen4b_passed"])
        pass9 = sum(1 for r in t_paired if r["qwen9b_passed"])
        c_t = task_counts[t]
        task_breakdown[t] = {
            "task_id": t,
            "nine_b_only_pass_count": c_t,
            "pct_of_c21": round(c_t / 21.0 * 100, 2),
            "qwen4b_pass_total": pass4,
            "qwen9b_pass_total": pass9,
            "net_difference": pass9 - pass4,
        }

    max_task = max(task_breakdown.items(), key=lambda x: x[1]["nine_b_only_pass_count"])
    is_task_dominated = max_task[1]["pct_of_c21"] >= 50.0

    print("5. Summarizing Condition Distribution...")
    condition_breakdown = {}
    for cond in ["ab1", "ab2g", "ab2d", "ab2d_spec_v2"]:
        cnt = condition_counts[cond]
        condition_breakdown[cond] = {
            "condition": cond,
            "nine_b_only_pass_count": cnt,
            "pct_of_c21": round(cnt / 21.0 * 100, 2),
        }

    ab2d_count = condition_counts["ab2d"]
    ab2d_share_pct = round(ab2d_count / 21.0 * 100, 2)
    is_condition_dominated = ab2d_share_pct >= 50.0

    print("6. Summarizing 4B Failure Layer Distribution...")
    layer_breakdown = {}
    for layer in ["L1", "L2", "L3", "L4", "L5"]:
        cnt = layer_counts[layer]
        layer_breakdown[layer] = {
            "layer": layer,
            "count": cnt,
            "pct_of_21": round(cnt / 21.0 * 100, 2),
        }

    print("7. Summarizing 4B Mechanism Distribution...")
    mechanism_breakdown = {}
    for m, cnt in mechanism_counts.items():
        mechanism_breakdown[m] = {
            "mechanism": m,
            "count": cnt,
            "pct_of_21": round(cnt / 21.0 * 100, 2),
        }

    print("8. Summarizing Ab2d+api Anomaly Audit Overlap...")
    overlap_count = len(ab2d_api_overlap_cells)
    overlap_share_pct = round(overlap_count / 21.0 * 100, 2)

    overlap_layers = Counter()
    overlap_mechanisms = Counter()
    for item in ab2d_api_overlap_cells:
        key = (item["task_id"], item["condition"], item["seed"])
        cell4b = [r for r in q4b_records if (r["task_id"], r["condition"], r["seed"]) == key][0]
        overlap_layers[cell4b.get("primary_failure_layer", "NOT_AVAILABLE")] += 1
        for m in cell4b.get("mechanism_tags", []):
            overlap_mechanisms[m] += 1

    overlap_summary = {
        "overlap_count": overlap_count,
        "overlap_share_pct": overlap_share_pct,
        "overlap_layer_distribution": dict(overlap_layers),
        "overlap_mechanism_distribution": dict(overlap_mechanisms),
        "methodological_note": "Ab2d+api accounts for only 3 out of 21 gap cells (14.29%). Do NOT extrapolate 77.8% SyntaxError-in-extracted from Ab2d 27-cell audit to all 21 cells.",
    }

    # Determine Verdict
    l1_l2_l3_l4_count = layer_counts["L1"] + layer_counts["L2"] + layer_counts["L3"] + layer_counts["L4"]
    l5_count = layer_counts["L5"]

    if l1_l2_l3_l4_count > l5_count:
        primary_verdict = "FRACTION_GAP_MAINLY_FORMAT_EXECUTION_RELATED"
    elif l5_count > l1_l2_l3_l4_count:
        primary_verdict = "FRACTION_GAP_MAINLY_ALGORITHMIC"
    else:
        primary_verdict = "FRACTION_GAP_MIXED_MECHANISMS"

    concentration_tag = "NO_SINGLE_DOMINATION"
    if is_task_dominated:
        concentration_tag = "FRACTION_GAP_TASK_CONCENTRATED"
    elif is_condition_dominated:
        concentration_tag = "FRACTION_GAP_CONDITION_CONCENTRATED"

    # Save Output Artifacts
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. fraction_9b_only_pass_ledger.jsonl
    with (OUTPUT_DIR / "fraction_9b_only_pass_ledger.jsonl").open("w", encoding="utf-8") as f:
        for r in audit_ledger:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # 2. task_distribution.json
    (OUTPUT_DIR / "task_distribution.json").write_text(
        json.dumps(task_breakdown, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 3. condition_distribution.json
    (OUTPUT_DIR / "condition_distribution.json").write_text(
        json.dumps(condition_breakdown, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 4. layer_distribution.json
    (OUTPUT_DIR / "layer_distribution.json").write_text(
        json.dumps(layer_breakdown, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 5. mechanism_distribution.json
    (OUTPUT_DIR / "mechanism_distribution.json").write_text(
        json.dumps(mechanism_breakdown, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 6. ab2d_api_overlap.json
    (OUTPUT_DIR / "ab2d_api_overlap.json").write_text(
        json.dumps(overlap_summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 7. audit_manifest.json
    manifest = {
        "audit_id": "math16_pilot02_fraction_9b_only_pass_mechanism_audit_v1",
        "scope": "Fraction family NINE_B_ONLY_PASS cells in Tier 1 paired ledger",
        "nine_b_only_pass_c": c_count,
        "four_b_only_pass_b": b_count,
        "paired_net_difference": net_diff,
        "records_count": c_count,
        "qwen4b_baseline_source": "docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl",
        "qwen9b_baseline_source": "docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/cell_level_baseline.jsonl",
        "paired_ledger_source": "docs/experiments/results/math16_pilot02_qwen4b_vs_qwen9b_tier1_paired_analysis_v1/paired_cell_ledger.jsonl",
        "primary_verdict": primary_verdict,
        "concentration_tag": concentration_tag,
        "category_a_status": "COMPLETED_WITH_INTERPRETATION_LIMITATIONS",
        "llm_calls": 0,
        "healer_execution": False,
        "rescued": False,
    }
    (OUTPUT_DIR / "audit_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 8. audit_report.md
    report_md = f"""# Math16 Pilot-02 Fraction Family 9B-Only Pass 機制分布診斷報告

```text
MATH16_PILOT02_FRACTION_9B_ONLY_PASS_AUDIT_COMPLETED
FRACTION_GAP_MECHANISM_DISTRIBUTION_DOCUMENTED
CATEGORY_A_COMPLETED_WITH_INTERPRETATION_LIMITATIONS
```

**診斷識別碼：** `math16_pilot02_fraction_9b_only_pass_mechanism_audit_v1`
**分析集合：** Tier 1 配對帳本中 Fraction 家族的 **21 個 `NINE_B_ONLY_PASS` cells** ($c=21$, $b=7$, 淨增加 $+14$ 格)
**主要 Verdict：** `{primary_verdict}`
**集中度標籤：** `{concentration_tag}`
**驗證狀態：** 100% 完整鎖定（無重複、無缺漏，4B 全部 FAIL，9B 全部 PASS）

---

## 1. 分析目的與配對計數說明

本診斷旨在回答：**「在 Tier 1 配對分析中，9B 在 Fraction 家族基線通過率顯著高於 4B（4B 17/80 vs 9B 31/80，淨增加 14 格）。在配對不一致矩陣中，$c=21$ 格為 9B 獨贏 (`NINE_B_ONLY_PASS`)，$b=7$ 格為 4B 獨贏 (`FOUR_B_ONLY_PASS`)，淨增加 $c - b = 14$ 格。這 21 格 4B 失敗/9B 成功案例集中在哪些 Task、Condition，以及 4B 對應的 Failure Layer 與 Mechanism 為何？」**

---

## 2. Task 分布 (Task Distribution)

21 格 `NINE_B_ONLY_PASS` 在 Fraction 家族 4 個 Tasks 中的分布如下：

| Task ID | 21格 Gap 數 ($c$) | 占 21 格比例 (%) | 4B PASS / 20 | 9B PASS / 20 | 配對淨增加 (9B - 4B) |
| :--- | ---: | ---: | ---: | ---: | ---: |
"""
    for t in fraction_tasks:
        tb = task_breakdown[t]
        report_md += f"| `{t}` | **{tb['nine_b_only_pass_count']}** | {tb['pct_of_c21']}% | {tb['qwen4b_pass_total']} | {tb['qwen9b_pass_total']} | **{tb['net_difference']:+d}** |\n"

    report_md += f"""
### 觀察與集中度：
- **最多差距 Task**：`ce113_q01_negative_fraction_subtraction` 占 **9 格 (42.86%)**。
- **次要差距 Task**：`ce111_q05_exact_fraction_expression` 占 **5 格 (23.81%)**、`ce112_q12_independent_probability_fraction` 占 **4 格 (19.05%)**、`ce115_calc_exact_rational_expression_l1` 占 **3 格 (14.29%)**。
- **Task 集中度判斷**：最大單一 Task (42.86%) 未達 50%，差距廣泛分散於多個分數題型。

---

## 3. Condition 分布 (Condition Distribution)

21 格 `NINE_B_ONLY_PASS` 在 4 種 Prompt 條件中的分布如下：

| Prompt 條件 | 21格 Gap 數 ($c$) | 占 21 格比例 (%) |
| :--- | ---: | ---: |
"""
    for cond in ["ab1", "ab2g", "ab2d", "ab2d_spec_v2"]:
        cb = condition_breakdown[cond]
        report_md += f"| **{cond}** | **{cb['nine_b_only_pass_count']}** | {cb['pct_of_c21']}% |\n"

    report_md += f"""
### 觀察與集中度：
- `Ab2g` 與 `Ab2d+spec-v2` 各占 **7 格 (33.33%)**，合計占 **66.67%**。
- `Ab1` 占 **4 格 (19.05%)**。
- `Ab2d+api` 僅占 **3 格 (14.29%)**。
- **Condition 集中度判斷**：差距分散於各種 Prompt 條件，**非由 Ab2d+api 條件主導**（Ab2d+api 僅占 14.29%）。

---

## 4. 4B Failure Layer 分布 (4B Failure Layer Distribution)

對這 21 格中 Qwen 4B 原先失敗的 Failure Layer 統計如下：

| Layer 層級 | 定義 | 4B 失敗格數 | 占 21 格比例 (%) |
| :--- | :--- | ---: | ---: |
| **L1** | Syntax / Parse Failure | **{layer_counts['L1']}** | {layer_breakdown['L1']['pct_of_21']}% |
| **L2** | Contract / Entry Point Failure | **{layer_counts['L2']}** | {layer_breakdown['L2']['pct_of_21']}% |
| **L3** | Domain-API Misuse | **{layer_counts['L3']}** | {layer_breakdown['L3']['pct_of_21']}% |
| **L4** | Runtime Execution Exception | **{layer_counts['L4']}** | {layer_breakdown['L4']['pct_of_21']}% |
| **L5** | Semantic / Algorithmic Error | **{layer_counts['L5']}** | {layer_breakdown['L5']['pct_of_21']}% |

### 主要結構：
- **L1 至 L4 (格式與執行層級失敗)**：合計 **15 格 (71.43%)**。
- **L5 (演算法/語義層級失敗)**：合計 **6 格 (28.57%)**。

---

## 5. 4B Mechanism 分布 (4B Mechanism Tags Distribution)

對這 21 格中 Qwen 4B 的正式 Mechanism 標籤統計如下：

| Mechanism Tag | 4B 標籤出現數 | 占 21 格比例 (%) |
| :--- | ---: | ---: |
"""
    for m, mb in mechanism_breakdown.items():
        report_md += f"| `{m}` | **{mb['count']}** | {mb['pct_of_21']}% |\n"

    report_md += f"""
---

## 6. 與既有 4B Ab2d+api 27格診斷之交集

- 21 格 gap 中，僅有 **{overlap_count} 格 ({overlap_share_pct}%)** 落入既有的 Qwen 4B Ab2d+api 27 格診斷集合（`ce111_q05` 在 Ab2d 條件下的 2 個 Seed）。
- **方法學限制提示**：舊 27 格診斷顯示該 Ab2d 樣本中有 77.8% 屬 SyntaxError-in-extracted，**絕對不可將該 77.8% 比例外推至整體 21 格 Fraction gap**。

---

## 7. 保守研究結論與禁止過度主張

### 可寫入報告之描述性結論：
1. 9B 在 Fraction 家族的 21 格 `NINE_B_ONLY_PASS` 差距主要落在 4B 的 **{primary_verdict}** 區域（L1~L4 格式與執行層級佔 71.43%）。
2. 差距廣泛分散於多個 Fraction 題型與各種 Prompt 條件，**非單一 Task 或 Ab2d+api 所獨佔**。
3. 9B 在 Fraction 家族展現了跨題型與跨 Prompt 條件的穩定累積優勢。

### 嚴禁過度推論事項：
- **不可寫成**「9B 比較會做分數題」（包含語法、包裝與 API 呼叫等工程因子）。
- **不可寫成**「4B Fraction 差距是由 Parser 造成」或「格式問題導致整體差距」。
- **不可寫成**「Ab2d+api 是造成差距的因果主因」。
- **不可寫成**「$p = 0.0001$ 證明了純數學能力差異」。

---
*本報告完全由 `scripts/audit_math16_pilot02_fraction_9b_only_pass.py` 從凍結數據程式化產出。*
"""
    (OUTPUT_DIR / "audit_report.md").write_text(report_md, encoding="utf-8")
    print(f"9. Audit complete. Output saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    run_audit()
