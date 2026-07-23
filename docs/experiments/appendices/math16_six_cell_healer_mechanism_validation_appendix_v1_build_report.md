# 《Math16 六格 Healer 救援機制驗證附錄 v1》 Build Report

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告類型：** 附錄 A 構建與勘誤報告
**建置時間 UTC：** 2026-07-23

---

> **固定位階聲明 (Mandatory Disclaimer)：**
> 本附錄為Evidence Complete凍結後之Post-hoc補充分析，不修改、取代或重新解釋既有Primary與正式Post-hoc結果。

---

## 1. 勘誤與修正紀錄 (Errata & Corrections Record)

1. **移除錯誤 8B 與模型尺寸描述**:
   - `Ab1 (Native 8B Baseline)` 改為 `Ab1（原始契約條件）`。
   - Q8 內文移除 `8B/4B`，改為精確表述：
     > 本實驗顯示，在本次Qwen 3.5 4B Math16資料中，部分失敗來自可由確定性規則處理的契約或介面瑕疵，而不一定是完整數學推理錯誤。
2. **修正 single-key 介面描述**:
   - 修正描述，避免誤傳「整個字典只有一個 key」。
   - 改為精確表述：
     > 在固定三欄回傳結構（`question_text`、`correct_answer`、`oracle_payload`）中，答案本體被額外包裝於唯一的`oracle_payload`欄位；Healer移除的是該payload層級的外包裝。
3. **收斂安全性與判準措辭**:
   - Q6 措辭收斂為：
     > SAFE_REPAIR_CANDIDATE表示修改前具備不看答案、唯一、局部、可離線驗證的安全依據，但不保證一定PASS，也不代表所有未知案例絕無副作用。
4. **證據索引 SHA 欄位分離**:
   - 證據索引表欄位調整為 `| Claim | Artifact Path | Artifact SHA256 | Governing Manifest Path | Manifest SHA256 | Supports |`，獨立重算並分離 Artifact SHA256 與 Governing Manifest SHA256。

---

## 2. 檔案清單 (File Checklist)

1. `docs/experiments/manifests/math16_six_cell_healer_mechanism_validation_appendix_v1_manifest.json`
2. `docs/experiments/appendices/math16_six_cell_healer_mechanism_validation_appendix_v1.md`
3. `docs/experiments/appendices/math16_six_cell_healer_mechanism_validation_appendix_v1_build_report.md`
4. `tests/test_math16_six_cell_healer_mechanism_validation_appendix_v1.py`
