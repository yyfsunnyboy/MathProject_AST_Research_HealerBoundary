# 《Math16 實驗題目、Prompt 與程式骨架展示附錄 v1》 Build Report

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告類型：** 附錄 C 構建與勘誤報告
**建置時間 UTC：** 2026-07-23

---

> **固定位階聲明 (Mandatory Disclaimer)：**
> 本附錄為Evidence Complete凍結後之Post-hoc展示文件，只供老師與評審理解實驗材料，不修改、取代或重新解釋既有Primary與正式Post-hoc結果。

---

## 1. 勘誤與修訂紀錄 (Errata & Revision Record)

1. **Difficulty 欄位語意釐清與拆分**:
   - 原 `difficulty = Level 1` 經權威核對為程式生成介面 (`generate(level=1)`) 的執行預設參數。
   - 欄位改為 `runtime_level` (固定值 `1`)，並新增 `preregistered_difficulty` (從預註冊 Spec Manifest 填入 `LOW` / `MEDIUM` / `HIGH`)。
   - 明確標示指定四題之預註冊難度：
     - `ce111_q08_polynomial_factor_parameter_recovery`: `HIGH`
     - `ce111_q10_ordered_quadratic_roots_radical`: `HIGH`
     - `ce112_q04_radical_simplification`: `LOW`
     - `ce115_calc_polynomial_division_l1`: `MEDIUM`
2. **附錄 A／B Manifest SHA 標籤修正與分離**:
   - 附錄 A 權威 Manifest SHA256 獨立標示為 `52014b1fbdbb09372953ae39be5965397d1f3813d88d99b95ff9053a25e1d29d` (`docs/experiments/manifests/math16_six_cell_healer_mechanism_validation_appendix_v1_manifest.json`)。
   - 附錄 B 權威 Manifest SHA256 獨立標示為 `ae61249c6dd8bafa422e401b5e6bed5abcd9262b5b6ea0df5bc641b93e9e6d1b` (`docs/experiments/manifests/math16_eligibility_and_unrestricted_stress_test_appendix_v1_manifest.json`)。
   - 上游 Six-Cell 正式結果 Manifest SHA256 保留標示為 `97392be833786bab90bcd5f1cb9eb9b57edaffc681466bdda62650f29dda35de` (`docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json`)。
   - 上游 Stress Test v1.1 正式結果 Manifest SHA256 保留標示為 `7cfc9f8f4de8b1fbf56ef19afdedba5dc43fd3ee70fe35d72c46cfeff33cdcf0` (`docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json`)。

---

## 2. 檔案清單 (File Checklist)

1. `docs/experiments/manifests/math16_tasks_prompts_and_program_skeletons_appendix_v1_manifest.json`
2. `docs/experiments/appendices/math16_tasks_prompts_and_program_skeletons_appendix_v1.md`
3. `docs/experiments/appendices/math16_tasks_prompts_and_program_skeletons_appendix_v1_build_report.md`
4. `artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/task_index.csv`
5. `artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/prompt_index.csv`
6. `artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/representative_case_index.json`
7. `artifacts/math16_tasks_prompts_and_program_skeletons_appendix_v1/evidence_index.json`
8. `scripts/build_math16_appendix_c.py`
9. `tests/test_math16_tasks_prompts_and_program_skeletons_appendix_v1.py`
