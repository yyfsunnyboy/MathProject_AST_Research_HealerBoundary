# 《Math16 Eligibility 與 Unrestricted Stress Test 驗證附錄 v1》 Build Report

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告類型：** 附錄 B 構建與勘誤報告
**建置時間 UTC：** 2026-07-23

---

> **固定位階聲明 (Mandatory Disclaimer)：**
> 本附錄為Evidence Complete凍結後之Post-hoc補充分析，不修改、取代或重新解釋既有Primary與正式Post-hoc結果。

---

## 1. 勘誤與修正紀錄 (Errata & Corrections Record)

1. **移除 `ambiguity_gate_prevented_harm = True` 誇大主張**:
   - 刪除原始 prevented harm 宣稱。
   - 語意替換為：
     - `ambiguity_gate_prevented_unsafe_intervention = true`
     - `ambiguity_gate_prevented_ineffective_intervention = true`
     - `observed_harm_prevented = not_demonstrated`
   - 正文固定表述更新為：
     > 歧義閘門避免了一次事前無法證明安全、且實際未能救回程式的介入。本案例未觀察到新增失敗或failure chain惡化，因此不能宣稱已證明避免實際傷害。
2. **收斂 Q7 語意表述**:
   - Q7 不寫「證實Eligibility擋下是正確的」，改為：
     > 此案例支持原本Abstain決策具有合理性：強制放寬歧義限制沒有產生額外有效救援。
3. **收斂 Q10 語意表述**:
   - Q10 不寫「覆蓋全部可安全救回的潛在窗口」，改為：
     > 在本次凍結規則集與242格FAIL母體中，Primary Eligibility涵蓋了所有已偵測到的唯一安全候選；沒有發現「唯一候選但遭安全閘門拒絕」的案例。
4. **證據索引 SHA 欄位分離與獨立核對**:
   - 證據索引表欄位調整為 `| Claim | Artifact Path | Artifact SHA256 | Governing Manifest Path | Manifest SHA256 | Supports |`。
   - `disposition_summary.json` (Artifact SHA256: `54fd4a0849137e4bf2f2baf7b0b2ced9ed242ad4503c6a5f7c6feade2cf052e7`) 與 forced ambiguity `.diff` (Artifact SHA256: `d8f0130d0d1d532ddfa78aba1b82eae4d9df1066f1ec09aec09345a82b350c24`) 之 Artifact SHA256 獨立重算並與 Manifest SHA256 (`7cfc9f8f4de8b1fbf56ef19afdedba5dc43fd3ee70fe35d72c46cfeff33cdcf0`) 明確分離。

---

## 2. 檔案清單 (File Checklist)

1. `docs/experiments/manifests/math16_eligibility_and_unrestricted_stress_test_appendix_v1_manifest.json`
2. `docs/experiments/appendices/math16_eligibility_and_unrestricted_stress_test_appendix_v1.md`
3. `docs/experiments/appendices/math16_eligibility_and_unrestricted_stress_test_appendix_v1_build_report.md`
4. `tests/test_math16_eligibility_and_unrestricted_stress_test_appendix_v1.py`
