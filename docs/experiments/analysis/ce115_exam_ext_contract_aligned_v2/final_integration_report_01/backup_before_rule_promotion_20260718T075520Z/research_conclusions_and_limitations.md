# 研究結論與限制摘要

> 更新含 Qwen4B v2 Ab3；備份：`docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/final_integration_report_01/backup_before_qwen4b_v2_ab3_20260718T052755Z`

## 主要結論

- Contract-aligned v2 在 formal overlap 消除 Gemini v1 兩類失敗（114-02 coefficients 巢狀；114-04 非法 Fraction 路徑）：Gemini v2 formal8 = 8/8 PASS（ITT=valid-response）。
- Qwen4B v2 formal8 = 3/8 ITT PASS；排除 114-04 timeout 後 valid-response = 3/7；殘敗經 forensic 歸為 assembly/routing/bloat，剩餘 prompt/API mismatch = 0。
- Qwen4B v2 Ab3（凍結 L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP，與 v1 Gemini 同版）：4 模型失敗格全數 noneligible；healer_executed=0；rescue-to-pass=0；無 false-positive。
- 殘敗 mechanism 本質上落在 allowlist 設計範圍外（非規則不夠聰明）；不可宣稱 v2 Healer 可救援 Qwen4B 此批失敗。
- qwen3.5:9b 與 Gemini v2 Ab3 仍未執行；不做模型規模趨勢推論。

## 限制

- v1 full18 與 v2 formal8 矩陣不同；僅 overlap8 可做成對 v1→v2 變化。
- L2 eligibility audit 僅涵蓋 v1；v2 失敗另以 forensic taxonomy 審查，未重跑 L2 audit。
- Ab3：v1 Gemini 與 v2 Qwen4B（本輪）已完成；Gemini v2 Ab3 仍 pending。
- Qwen 114-04 v2 timeout 屬 infrastructure；能力比較須用 valid-response 分母。
- 單一 seed（2026071301）；無多 seed 變異。
- v2 formal 跑次 Healer 關閉（healer_calls=0）。

## 待補

- qwen3.5:9b 相同 8-cell v2 執行
- Gemini v2 Ab3 / Healer production eval
- （可選）Qwen v1 Ab3 on existing-L2-eligible cells
- 多 seed 重複驗證

## Qwen4B v2 Ab3 速查

- eligible: 0
- noneligible: 4
- rescue-to-pass: 0
- healer_executed: 0
- false-positive: none

## 分母速查（勿混算）

| Cohort | ITT | Valid-response |
|---|---|---|
| v1_gemini_full18 | 14/18 (0.7778) | 14/18 (0.7778) |
| v1_qwen4b_full18 | 7/18 (0.3889) | 7/18 (0.3889) |
| v2_gemini_formal8 | 8/8 (1.0) | 8/8 (1.0) |
| v2_qwen4b_formal8 | 3/8 (0.375) | 3/7 (0.4286) |
| v2_qwen9b_formal8 | NOT_EXECUTED | NOT_EXECUTED |
