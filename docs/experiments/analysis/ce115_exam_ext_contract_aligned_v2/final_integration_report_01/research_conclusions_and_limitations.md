# 研究結論與限制摘要

> 更新含規則轉正與鏈式修復；備份：`docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/final_integration_report_01/backup_before_rule_promotion_20260718T075520Z`

## 主要結論

- Contract-aligned v2 在 formal overlap 消除 Gemini v1 兩類失敗（114-02 coefficients 巢狀；114-04 非法 Fraction 路徑）：Gemini v2 formal8 = 8/8 PASS（ITT=valid-response）。
- Qwen4B v2 formal8 = 3/8 ITT PASS；排除 114-04 timeout 後 valid-response = 3/7；殘敗經 forensic 歸為 assembly/routing/bloat，剩餘 prompt/API mismatch = 0。
- **Production allowlist（轉正後）**：
  1. `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
  2. `L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM`
  3. `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP`
- **Production 鏈式修復案例**：Qwen4B v2 113-10 Ab2d — RUNTIME KeyError → kwargs-bag inline（chain_position=1）→ json.dumps unwrap（chain_position=2）→ **PASS**（`rescue_to_pass=true`；見 `qwen4b_v2_113_10_production_chain_01/`）。
- **Production 修復數（勿與 experimental 混算）**：production rescue-to-pass = **1**（113-10 Ab2d 鏈式）；historical Ab3（僅舊 allowlist、max_passes=1）rescue = 0 仍為有效對照，不回溯改寫。
- **外邊界（deterministic 不可修）**：114-08 Ab2d（shadow API／自創邏輯）；114-02 Ab2d（parse 崩壞，同撤回 L1 先例）。
- **113-11 診斷**：NameError 缺 import；arity 正確；僅補 import 不足（缺 `to_exact` 等）；**不**進 allowlist。
- qwen3.5:9b 與 Gemini v2 Ab3 仍未執行；不做模型規模趨勢推論。

## 限制

- v1 full18 與 v2 formal8 矩陣不同；僅 overlap8 可做成對 v1→v2 變化。
- L2 eligibility audit 僅涵蓋 v1；v2 失敗另以 forensic／promotion audit 審查。
- 鏈式修復需顯式 `max_passes=RECOMMENDED_CHAIN_MAX_PASSES`；預設 `DEFAULT_MAX_PASSES=1` 在仍有待改規則時 fail-closed。
- Qwen 114-04 v2 timeout 屬 infrastructure；能力比較須用 valid-response 分母。
- 單一 seed（2026071301）；無多 seed 變異。
- v2 formal 跑次原始 Healer 關閉（healer_calls=0）；本輪 production 鏈式為事後重跑、不改 raw artifacts。

## 待補

- qwen3.5:9b 相同 8-cell v2 執行
- Gemini v2 Ab3 / 全矩陣 Healer production eval（新 allowlist + chain budget）
- （可選）Qwen v1 Ab3 on existing-L2-eligible cells
- 多 seed 重複驗證

## Production／Experimental 分開列示

| 類別 | 內容 | 計數 |
|---|---|---|
| production allowlist | 3 條 L2（見上） | 3 rules |
| production rescue-to-pass（本輪鏈式） | 113-10 Ab2d | 1 |
| experimental（歷史草案證據） | kwargs-bag／dumps-unwrap 實驗目錄 | 證據保留；已轉正後不再另計 experimental 修復 |
| essentially unrepairable | 114-08、114-02 Ab2d | 2 |
| diagnostic-only | 113-11 Ab2d | 1 |

## 分母速查（勿混算）

| Cohort | ITT | Valid-response |
|---|---|---|
| v1_gemini_full18 | 14/18 (0.7778) | 14/18 (0.7778) |
| v1_qwen4b_full18 | 7/18 (0.3889) | 7/18 (0.3889) |
| v2_gemini_formal8 | 8/8 (1.0) | 8/8 (1.0) |
| v2_qwen4b_formal8 | 3/8 (0.375) | 3/7 (0.4286) |
| v2_qwen9b_formal8 | NOT_EXECUTED | NOT_EXECUTED |
