# Math16 Post-hoc Six-Cell Before-After Evidence Recovery Audit Report v1

```text
MATH16_SIX_CELL_BEFORE_AFTER_RECOVERY_V1_COMPLETED
NO_EXACT_SOURCE_DIFF_RECOVERED
RULE_LEVEL_MECHANISM_ONLY
EVIDENCE_LIMITATION_FORMALLY_RECORDED
OFFICIAL_RESULTS_PRESERVED
```

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告版本：** v1.0 (Evidence Recovery Audit)
**標的數據庫：** Math16 Pilot-02 既有 6 個 Post-hoc rescued cells

---

> **固定聲明 (Mandatory Disclaimer)：**
> 本分析為 Evidence Complete 凍結後之 Post-hoc 補充稽核，不修改、取代或重新解釋既有 Primary 與正式 Post-hoc 結果。

---

## 1. 執行摘要與判定 (Executive Summary & Classification)

本稽核旨在對 **Math16 Pilot-02** 既有 **6 個 Post-hoc rescued cells** 的真實原始程式碼內容（Before Source / After Source）進行全庫只讀搜尋與證明回收。

### 稽核結論與數據：
1. **Before Source 逐字回收率**: `6 / 6` (100%)
   - 6 格之原始 LLM 生成碼均成功於 `docs/experiments/results/math16_pilot02_qwen4b/cells/<cell_id>/artifact.json` 中之 `raw_response` 完整檢索回收，且經基礎 code fence 清理後，其 SHA256 與 `eligible_execution_records.jsonl` 之 `before_source_sha256` 100% 吻合。
2. **After Source 逐字回收率**: `0 / 6` (0%)
   - 所有修復後程式碼受限於 `sha_only_not_committed_py` 之極簡化磁碟儲存策略，未在 repo 內提交獨立 `.py` 檔案。
3. **逐字 Unified Diff 重建能力**: `0 / 6` (0%)
   - 由於無對應之原始 After Source `.py` 檔，**無法進行非猜測性的逐字 Unified Diff 重建**。
4. **成對比較證據等級**: `RULE_LEVEL_ONLY` (規則層級機制說明)
   - 6 格在單側 (Before Source) 達到 `PARTIAL` 逐字回收；成對修復說明則依據事前登錄之修復規則與 SHA 歸類為 `RULE_LEVEL_ONLY`。
5. **Incremental Cell 狀況**:
   - 第 4 格 (`qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301`) 之 Before Source 亦已 100% 逐字回收於 `recovered_sources/`。

---

## 2. 報告七問解答 (Systematic Recovery Answers)

### Q1: 6 格中幾格能回收完整 Before Source？
**6 格 (100%)**。所有 6 格的原始模型生成碼均在獨立 cell 紀錄 (`docs/experiments/results/math16_pilot02_qwen4b/cells/<cell_id>/artifact.json`) 中完整保留，並已複製備份至 `artifacts/math16_posthoc_six_cell_before_after_recovery_v1/recovered_sources/`。

### Q2: 幾格能回收完整 After Source？
**0 格 (0%)**。根據歷史儲存規範 `sha_only_not_committed_py`，修復後的 `.py` 檔案未被 commit 進版本庫。

### Q3: 幾格能重建真實 Unified Diff？
**0 格 (0%)**。在無 After Source 檔案的情況下，嚴格禁止進行猜測性重構以冒充真實逐字 Diff。

### Q4: 幾格只能做 Rule-level 機制說明？
**6 格 (100%)**。所有成對修復分析均採用確定性規則 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 作為機制說明。

### Q5: 是否至少有 1 格可製作給老師看的真實 Before/After Case Card？
**否**。由於無 `EXACT` 級別（即無逐字 After Source），依規範**不得製作真實 Before/After 程式碼對比卡**；僅能製作 Rule-level 示意，且必須強制標註「`機制示意，非逐字還原之原始程式碼。`」。

### Q6: Incremental Post-hoc Cell 的 Before/After 是否可回收？
- **Before Source**: **可 100% 回收**（檔案位於 `recovered_sources/qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301__before.py`）。
- **After Source**: **不可回收**（僅有 `after_source_sha256 = ac6299da36256125e27fc76c71bb76ff1ef1b31939f71e72fc22df1f4b092aaf`）。

### Q7: 若無法回收，正式證據限制應如何表述？
**正式表述措辭：**
> 「受限於實驗數據持久化採用 `sha_only_not_committed_py` 之極簡策略，修復後程式碼未在版本庫中保留獨立原始檔。雖然 Before Source 達到 100% 逐字回收，但成對 Unified Diff 無法進行無猜測性重構。本研究對於 AST Healer 修復細節之說明，嚴格限定於 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 凍結簽章與 SHA256 驗證，不宣稱具備雙側逐字原始碼對比證據。」

---

## 3. 老師展示用 Rule-Level 機制示意 (Teacher-Facing Rule Schema)

> **`機制示意，非逐字還原之原始程式碼。`**

### 代表案例示意 1: JSON Payload 包覆解封 (Single-Key Unwrap)

#### [Before Source (真實回收片段)]
```python
# 檔名: qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004__before.py
def generate(level=1, **kwargs):
    radicand = 135
    coefficient = 3
    simplified_radicand = 15
    question_text = r"\text{Simplify the radical: } \sqrt{135}"
    # 模型將輸出包覆於 JSON 字典中
    return {"result": f"{coefficient} * \\sqrt{{{simplified_radicand}}}"}
```

#### [After Source (Rule-Level 機制示意，非逐字還原)]
```python
# 依據 L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP 確定性規則進行剝離:
# Healer 動作: 偵測單鍵 JSON 字典 Envelope，提取內部表達式字串。
# 為何不改數學邏輯: 不改動 radicand (15) 與 coefficient (3) 數值，僅調整輸出契約型態。
```

---

## 4. 6 格回收明細表 (Recovery Matrix)

| Canonical Cell ID | Condition | Before Recovered | After Recovered | Confidence | Diff Reconstructable |
|---|---|:---:|:---:|:---:|:---:|
| `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004` | Ab2g | TRUE | FALSE | PARTIAL / RULE_LEVEL | FALSE |
| `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002` | Ab2d+spec | TRUE | FALSE | PARTIAL / RULE_LEVEL | FALSE |
| `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003` | Ab2g | TRUE | FALSE | PARTIAL / RULE_LEVEL | FALSE |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` (Incremental) | Ab2d+api | TRUE | FALSE | PARTIAL / RULE_LEVEL | FALSE |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002` | Ab2d+api | TRUE | FALSE | PARTIAL / RULE_LEVEL | FALSE |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301` | Ab2d+spec | TRUE | FALSE | PARTIAL / RULE_LEVEL | FALSE |

---

## 5. SHA 保護與凍結驗證

以下既有成果與基準檔案 SHA256 均經比對 100% 未受影響：

- Final Report v1.3: `dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b` (未修改 ✅)
- Evidence Complete: `de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225` (未修改 ✅)
- Integrated Report: `44018 bytes` (未修改 ✅)

---

## 6. 結案 Verdict

```text
MATH16_SIX_CELL_BEFORE_AFTER_RECOVERY_V1_COMPLETED
NO_EXACT_SOURCE_DIFF_RECOVERED
RULE_LEVEL_MECHANISM_ONLY
EVIDENCE_LIMITATION_FORMALLY_RECORDED
OFFICIAL_RESULTS_PRESERVED
```
