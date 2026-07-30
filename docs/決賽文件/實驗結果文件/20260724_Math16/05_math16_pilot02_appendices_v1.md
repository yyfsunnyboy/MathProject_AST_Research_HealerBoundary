# 《Math16 Pilot-02 實驗附錄總冊 v1》

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**文件類型：** 正式審查附錄總冊 (Official Appendices Collection v1)
**建置時間 UTC：** 2026-07-23

---

> **固定位階聲明 (Mandatory Disclaimer)：**
> 本附錄總冊為 Evidence Complete 凍結後之 Post-hoc 展示文件，只供老師與評審整合理解實驗材料，不修改、取代或重新解釋既有 Primary 與正式 Post-hoc 結果。

---

## 1. 附錄總冊架構與目錄導覽 (Overview & Table of Contents)

本總冊收錄 Math16 HealerBoundary 實驗之三份獨立驗證與展示附錄：

1. **第一部分：附錄 A** —— 《Math16 六格 Healer 救援機制驗證附錄 v1》
2. **第二部分：附錄 B** —— 《Math16 Eligibility 與 Unrestricted Stress Test 驗證附錄 v1》
3. **第三部分：附錄 C** —— 《Math16 實驗題目、Prompt 與程式骨架展示附錄 v1》

---

## 2. 第一部分：附錄 A（六格 Healer 救援機制驗證）

> **原始檔案**：`docs/experiments/appendices/math16_six_cell_healer_mechanism_validation_appendix_v1.md`
> **原始 Manifest**：`docs/experiments/manifests/math16_six_cell_healer_mechanism_validation_appendix_v1_manifest.json`
> **SHA256 (Doc)**：`e638271638556ba8ad672cafc00379a314c9fdf7e0109de3396acfe3c4381d3b`
> **SHA256 (Manifest)**：`52014b1fbdbb09372953ae39be5965397d1f3813d88d99b95ff9053a25e1d29d`

### 2.1 六格救援摘要
- **Primary Rescued Count**: `5` 格 (既有 Primary 報告呈現)
- **Corrected Technical Rescued Count**: `6` 格 (修正 false-loop rollback bug 後呈現)
- **差集唯一案例**: `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301`
- **Hit Rule**: 100% 命中 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`

### 2.2 評審關切 Q&A
- **Q1 救援數字**: Primary 5 格與 Corrected 6 格皆為真實紀錄，差別在於評估器執行器 false-loop bug 之修正。
- **Q4 Healer 偷看答案**: 完全沒有 (`oracle_answer_used = false`)。Healer 僅解解外層字典 key。

---

## 3. 第二部分：附錄 B（Eligibility 與 Unrestricted Stress Test 驗證）

> **原始檔案**：`docs/experiments/appendices/math16_eligibility_and_unrestricted_stress_test_appendix_v1.md`
> **原始 Manifest**：`docs/experiments/manifests/math16_eligibility_and_unrestricted_stress_test_appendix_v1_manifest.json`
> **SHA256 (Doc)**：`01df02153e19e166ec0facd99bf9df1b95c958281f0f0e7f8c6db867d35baab8`
> **SHA256 (Manifest)**：`ae61249c6dd8bafa422e401b5e6bed5abcd9262b5b6ea0df5bc641b93e9e6d1b`

### 3.1 242 格 Baseline FAIL 互斥分層帳目
- **`NO_RULE_CANDIDATE`**: `231` (95.45%)
- **`UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE`**: `10` (4.13%)
- **`UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE`**: `0` (0.00%)
- **`AMBIGUOUS_MULTIPLE_CANDIDATES`**: `1` (0.41%)
- **`DETECTION_UNRESOLVED`**: `0` (0.00%)

### 3.2 Forced Ambiguity 探索結果
- **標的 Cell**: `qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004`
- **Evaluator 評估結果**: **`FAILED`** (`missing_entry_point`)
- **Safety 預分類**: `UNSAFE_MODIFICATION`
- **防護語意**: 歧義閘門避免了一次事前無法證明安全、且實際未能救回程式的介入。

---

## 4. 第三部分：附錄 C（實驗題目、Prompt 與程式骨架展示）

> **原始檔案**：`docs/experiments/appendices/math16_tasks_prompts_and_program_skeletons_appendix_v1.md`
> **原始 Manifest**：`docs/experiments/manifests/math16_tasks_prompts_and_program_skeletons_appendix_v1_manifest.json`
> **SHA256 (Doc)**：`b646269385287fdbf73034031cb869a4c49d2413c653b972b13689ea91b95e06`
> **SHA256 (Manifest)**：`7f03b01e16ceff2f05872dc8f82e731edc1843c3688f73b8df8d9c64da7c6672`

### 4.1 16 題題目與 Prompt 矩陣
- **16 題任務權威索引**：完整記錄於 `artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/task_index.csv`。
- **64 份 Prompt 權威索引**：完整記錄於 `artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/prompt_index.csv`。
- **難度與執行參數澄清**：`runtime_level=1` 是程式生成介面的執行參數；預註冊難度另依據Spec Manifest列為 `preregistered_difficulty` (`LOW` / `MEDIUM` / `HIGH`)。

### 4.2 正確答案程序與視覺隔離聲明
> 正確答案僅供老師與評審對照理解，不是模型生成Prompt的一部分，也不是Healer執行時可讀取的輸入。Healer僅依生成程式的語法、AST結構與凍結契約規則進行修改，`oracle_answer_used = false`。

---

## 5. 權威證據索引表 (Combined Evidence Index)

| Claim | Original Appendix Path & SHA256 | Original Appendix Manifest Path & SHA256 | Upstream Artifact Path & SHA256 | Governing Result Manifest Path & SHA256 |
|---|---|---|---|---|
| **附錄 A 救援機制** | `docs/experiments/appendices/..._appendix_v1.md`<br>`e638271638556ba8ad67...` | `docs/experiments/manifests/..._appendix_v1_manifest.json`<br>`52014b1fbdbb09372953...` | `artifacts/.../before_signature_table.csv`<br>`293646ebca0a3e8b2c4f...` | `docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json`<br>`97392be833786bab90bc...` |
| **附錄 B 處置摘要** | `docs/experiments/appendices/..._appendix_v1.md`<br>`01df02153e19e166ec0f...` | `docs/experiments/manifests/..._appendix_v1_manifest.json`<br>`ae61249c6dd8bafa422e...` | `artifacts/.../disposition_summary.json`<br>`54fd4a0849137e4bf2f2...` | `docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json`<br>`7cfc9f8f4de8b1fbf56e...` |
| **Forced 歧義 Diff** | `docs/experiments/appendices/..._appendix_v1.md`<br>`01df02153e19e166ec0f...` | `docs/experiments/manifests/..._appendix_v1_manifest.json`<br>`ae61249c6dd8bafa422e...` | `artifacts/.../qwen3_5_4b...forced.diff`<br>`d8f0130d0d1d532ddfa7...` | `docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json`<br>`7cfc9f8f4de8b1fbf56e...` |
| **附錄 C 題目與骨架** | `docs/experiments/appendices/..._appendix_v1.md`<br>`b646269385287fdbf730...` | `docs/experiments/manifests/..._appendix_v1_manifest.json`<br>`7f03b01e16ceff2f0587...` | `artifacts/.../prompt_index.csv`<br>`daef61342d9f0e7cbf9b...` | `docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json`<br>`d83451176a51d7d9bdda...` |
| **Provenance Audit** | docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md<br>05a1ef08836e7f957cd0d4e87be9090d863b0c290474ae8b80bfd9ed4347bb4a | docs/experiments/reports/math16_healer_rule_provenance_audit_v1_manifest.json<br>b882b4d31a61dbca8ab60622c75ecf82290223cdab3a816de7116e4bb515ecd5 | agent_tools/finals_rebuild/ce115_research_healer_rules_*.py<br>d9aa264c | docs/experiments/reports/math16_healer_rule_provenance_audit_v1_manifest.json<br>b882b4d31a61dbca8ab60622c75ecf82290223cdab3a816de7116e4bb515ecd5 |
| **正式研究報告** | `docs/experiments/reports/math16_pilot02_final_report_v13.md`<br>`d77eb8c4e1d7ccae03e2...` | `docs/experiments/milestones/.../evidence_complete_manifest.json`<br>`de11b9bd5038171689ee...` | `docs/experiments/reports/math16_pilot02_final_report_v13.md`<br>`d77eb8c4e1d7ccae03e2...` | `docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json`<br>`de11b9bd5038171689ee...` |



## 6. Healer 規則 Provenance Audit 與雙層學術定位 (Provenance Audit Alignment)

1. **規則凍結狀態 (`rule_freeze_status = PRE_FROZEN_UNCHANGED`)**：六條 Healer 規則及其適用條件均於正式 Math16 320-cell generation 前完成凍結 (d9aa264c)，且後續未修改 detector、eligibility、transform 或 activation scope。
2. **Primary 5 定位 (`validation_status = PROSPECTIVE_WITHIN_MATH16_COHORT`)**：Primary 帳目的 5 格救援屬於預先固定規則在 Math16 cohort 上的前瞻性評估結果；但因規則源自先期開發資料，且尚未在完全獨立資料集驗證 (independent_external_validation = false)，本研究不主張其為外部獨立確認性證據。
3. **Corrected 第 6 格定位 (POST_HOC_TECHNICAL_CORRECTION)**：第 6 格來自既有規則成功 transform 被 runner false-loop rollback 錯誤撤回後的技術修正。此修正未新增或修改 Healer 規則，不改變 PRE_FROZEN_UNCHANGED 狀態；但因屬正式結果揭露後的技術重算，只列入 Corrected technical account，不回寫 Primary。
4. **Payload Wrap 結構 (oracle_payload 內部包裝)**：single-key 指固定三欄回傳結構中 oracle_payload 欄位內部的唯一包裝鍵，不是最外層 return dict 只有一個鍵。Healer 不讀取 correct_answer，oracle_answer_used = false。此結果支持窄範圍、唯一、局部且離線可驗證的 deterministic repair candidate，不代表零副作用或一般語意安全保證。

- 權威 Provenance Audit 報告：docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md (SHA256: 05a1ef08836e7f957cd0d4e87be9090d863b0c290474ae8b80bfd9ed4347bb4a)
- 權威 Provenance Audit Manifest：docs/experiments/reports/math16_healer_rule_provenance_audit_v1_manifest.json (SHA256: b882b4d31a61dbca8ab60622c75ecf82290223cdab3a816de7116e4bb515ecd5)
- 規則凍結 Commit：d9aa264c | 分類修正 Commit：97c4e985
