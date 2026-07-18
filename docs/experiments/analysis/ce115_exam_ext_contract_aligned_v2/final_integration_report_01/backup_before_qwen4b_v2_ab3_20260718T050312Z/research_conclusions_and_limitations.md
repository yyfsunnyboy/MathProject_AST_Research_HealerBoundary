# 研究結論與限制摘要

## 主要結論

- Contract-aligned v2 在 formal overlap 消除 Gemini v1 兩類失敗（114-02 coefficients 巢狀；114-04 非法 Fraction 路徑）：Gemini v2 formal8 = 8/8 PASS（ITT=valid-response）。
- Qwen4B v2 formal8 = 3/8 ITT PASS；排除 114-04 timeout 後 valid-response = 3/7；殘敗經 forensic 歸為 assembly/routing/bloat，剩餘 prompt/API mismatch = 0。
- v1 L2 eligibility：3 格 existing-rule、5 格 new-rule-candidate。Ab3 凍結 L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP → triggered=0、rescue-to-pass=0（本輪禁止 correct_answer wrap）。
- v2 Ab3 與 Qwen Healer rescue 仍為 pending；不可宣稱 v2 Healer 邊界已閉合。
- qwen3.5:9b 未執行；不做模型規模趨勢推論。

## 限制

- v1 full18 與 v2 formal8 矩陣不同；僅 overlap8 可做成對 v1→v2 變化。
- L2 eligibility audit 僅涵蓋 v1；v2 失敗另以 forensic taxonomy 審查，未重跑 L2 audit。
- Ab3 僅涵蓋 Gemini v1；其他 cohort 的 repair/rescue 欄位為 pending 或 out of scope。
- Qwen 114-04 v2 timeout 屬 infrastructure；能力比較須用 valid-response 分母。
- 單一 seed（2026071301）；無多 seed 變異。
- v2 formal 跑次 Healer 關閉（healer_calls=0）。

## 待補

- qwen3.5:9b 相同 8-cell v2 執行
- v2 Ab3 / Healer production eval（殘敗格）
- 若需 Qwen rescue-to-pass 宣稱：Qwen v1 Ab3（existing-L2-eligible 格）
- 多 seed 重複驗證

## 分母速查（勿混算）

| Cohort | ITT | Valid-response |
|---|---|---|
| v1_gemini_full18 | 14/18 (0.7778) | 14/18 (0.7778) |
| v1_qwen4b_full18 | 7/18 (0.3889) | 7/18 (0.3889) |
| v2_gemini_formal8 | 8/8 (1.0) | 8/8 (1.0) |
| v2_qwen4b_formal8 | 3/8 (0.375) | 3/7 (0.4286) |
| v2_qwen9b_formal8 | NOT_EXECUTED | NOT_EXECUTED |
