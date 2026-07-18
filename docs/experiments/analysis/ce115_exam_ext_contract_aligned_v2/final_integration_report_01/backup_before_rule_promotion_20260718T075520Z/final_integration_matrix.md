# CE115 Exam Ext — 最終整合報告矩陣

> 只讀整合；`real_model_calls=0`。v1／v2 與 Gemini／Qwen4B 分開呈現（不混算）。9B 標未執行。timeout 不歸因模型能力。

## 資料來源與完整性

| Source | Cells / status | Complete / note |
|---|---|---|
| v1_gemini_pilot | 18 | True |
| v1_qwen4b_pilot | 18 | True |
| v2_gemini_formal | 8 | True |
| v2_qwen4b_formal | 8 | True |
| l2_eligibility_audit | reviewed_failures=8 | scope=v1 |
| ab3_production_eval | completed_v1_gemini | v2_qwen4b=completed; v2_gemini=pending |
| qwen4b_fail5_forensic | cells=5 | remaining_prompt_api_mismatch=0 |
| qwen9b_v2 | not_executed_on_this_machine | — |

## 分開分母（ITT vs valid-response）

| Cohort | ITT pass/n | ITT rate | Infra fails | Valid pass/n | Valid rate |
|---|---|---|---|---|---|
| v1_gemini_full18 | 14/18 | 0.7778 | 0 | 14/18 | 0.7778 |
| v1_qwen4b_full18 | 7/18 | 0.3889 | 0 | 7/18 | 0.3889 |
| v1_gemini_overlap8 | 4/8 | 0.5 | 0 | 4/8 | 0.5 |
| v1_qwen4b_overlap8 | 3/8 | 0.375 | 0 | 3/8 | 0.375 |
| v2_gemini_formal8 | 8/8 | 1.0 | 0 | 8/8 | 1.0 |
| v2_qwen4b_formal8 | 3/8 | 0.375 | 1 | 3/7 | 0.4286 |
| v2_qwen9b_formal8 | NOT_EXECUTED/8 | — | — | — | — |

## A. Gemini — v1 full 18

| task | cond | status | layer | infra | align | adoption | chars | AST | tokens | L2 elig | matched/candidate rule | Ab3 repair | rescue |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 113-10 | ab1 | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 2296 | n/a_passed | — | no_op | False |
| 113-10 | ab2d | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 2958 | n/a_passed | — | no_op | False |
| 113-10 | ab2g | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 1928 | n/a_passed | — | no_op | False |
| 113-11 | ab1 | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 1855 | n/a_passed | — | no_op | False |
| 113-11 | ab2d | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 2443 | n/a_passed | — | no_op | False |
| 113-11 | ab2g | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 1771 | n/a_passed | — | no_op | False |
| 114-01 | ab1 | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 6086 | n/a_passed | — | no_op | False |
| 114-01 | ab2d | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 2205 | n/a_passed | — | no_op | False |
| 114-01 | ab2g | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 1445 | n/a_passed | — | no_op | False |
| 114-02 | ab1 | ANSWER_INCORRECT | L5 | True | misaligned_or_contract_gap | NOT_APPLICABLE | None | None | 1685 | eligible_new_rule_candidate | candidate:L2_CORRECT_ANSWER_SINGLE_KEY_WRAP_COEFFICIENTS | no_op | False |
| 114-02 | ab2d | ANSWER_INCORRECT | L5 | True | misaligned_or_contract_gap | NOT_APPLICABLE | None | None | 2650 | eligible_new_rule_candidate | candidate:L2_CORRECT_ANSWER_SINGLE_KEY_WRAP_COEFFICIENTS | no_op | False |
| 114-02 | ab2g | ANSWER_INCORRECT | L5 | True | misaligned_or_contract_gap | NOT_APPLICABLE | None | None | 1641 | eligible_new_rule_candidate | candidate:L2_CORRECT_ANSWER_SINGLE_KEY_WRAP_COEFFICIENTS | no_op | False |
| 114-04 | ab1 | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 4880 | n/a_passed | — | no_op | False |
| 114-04 | ab2d | RUNTIME_FAILURE | L4 | True | misaligned_or_contract_gap | NOT_APPLICABLE | None | None | 5047 | noneligible_or_not_in_l2_audit | — | no_op | False |
| 114-04 | ab2g | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 2449 | n/a_passed | — | no_op | False |
| 114-08 | ab1 | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 1493 | n/a_passed | — | no_op | False |
| 114-08 | ab2d | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 2185 | n/a_passed | — | no_op | False |
| 114-08 | ab2g | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 1793 | n/a_passed | — | no_op | False |

## B. Qwen4B — v1 full 18

| task | cond | status | layer | infra | align | adoption | chars | AST | tokens | L2 elig | matched/candidate rule | Ab3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 113-10 | ab1 | SCHEMA_FAILURE | L2 | True | assumed_usable | NOT_APPLICABLE | None | None | 822 | eligible_new_rule_candidate | candidate:L2_ORACLE_PAYLOAD_RESTORE_FULL_FROZEN | not_in_ab3_scope |
| 113-10 | ab2d | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 1504 | n/a_passed | — | not_in_ab3_scope |
| 113-10 | ab2g | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 531 | n/a_passed | — | not_in_ab3_scope |
| 113-11 | ab1 | SCHEMA_FAILURE | L2 | True | assumed_usable | NOT_APPLICABLE | None | None | 475 | eligible_new_rule_candidate | candidate:L2_ORACLE_PAYLOAD_IDENTITY_RESTORE_FROM_FROZEN | not_in_ab3_scope |
| 113-11 | ab2d | RUNTIME_FAILURE | L4 | True | assumed_usable | NOT_APPLICABLE | None | None | 1340 | noneligible_or_not_in_l2_audit | — | not_in_ab3_scope |
| 113-11 | ab2g | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 655 | n/a_passed | — | not_in_ab3_scope |
| 114-01 | ab1 | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 343 | n/a_passed | — | not_in_ab3_scope |
| 114-01 | ab2d | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 894 | n/a_passed | — | not_in_ab3_scope |
| 114-01 | ab2g | PASSED | PASS | True | assumed_usable | NOT_APPLICABLE | None | None | 698 | n/a_passed | — | not_in_ab3_scope |
| 114-02 | ab1 | PASSED | PASS | True | misaligned_or_contract_gap | NOT_APPLICABLE | None | None | 356 | n/a_passed | — | not_in_ab3_scope |
| 114-02 | ab2d | RUNTIME_FAILURE | L4 | True | misaligned_or_contract_gap | NOT_APPLICABLE | None | None | 1306 | noneligible_or_not_in_l2_audit | — | not_in_ab3_scope |
| 114-02 | ab2g | SCHEMA_FAILURE | L2 | True | misaligned_or_contract_gap | NOT_APPLICABLE | None | None | 422 | eligible_existing_rule | L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP | not_in_ab3_scope |
| 114-04 | ab1 | RUNTIME_FAILURE | L4 | True | assumed_usable | NOT_APPLICABLE | None | None | 2781 | noneligible_or_not_in_l2_audit | — | not_in_ab3_scope |
| 114-04 | ab2d | PARSE_MINOR | L1 | True | misaligned_or_contract_gap | NOT_APPLICABLE | None | None | 2306 | noneligible_or_not_in_l2_audit | — | not_in_ab3_scope |
| 114-04 | ab2g | PARSE_MINOR | L1 | True | assumed_usable | NOT_APPLICABLE | None | None | 7789 | noneligible_or_not_in_l2_audit | — | not_in_ab3_scope |
| 114-08 | ab1 | SCHEMA_FAILURE | L2 | True | assumed_usable | NOT_APPLICABLE | None | None | 619 | eligible_existing_rule | L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP | not_in_ab3_scope |
| 114-08 | ab2d | PARSE_MINOR | L1 | True | assumed_usable | NOT_APPLICABLE | None | None | 2548 | noneligible_or_not_in_l2_audit | — | not_in_ab3_scope |
| 114-08 | ab2g | SCHEMA_FAILURE | L2 | True | assumed_usable | NOT_APPLICABLE | None | None | 508 | eligible_existing_rule | L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP | not_in_ab3_scope |

## C. Gemini — v2 formal 8（含 v1→v2）

| task | cond | status | layer | infra | align | adoption | chars | AST | tokens | L2 | Ab3 | v1→v2 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 114-02 | ab1 | PASSED | PASS | True | aligned | NOT_APPLICABLE | 960 | 166 | 2250 | not_audited_for_v2 | pending_not_run_on_v2 | fail_to_pass |
| 114-02 | ab2g | PASSED | PASS | True | aligned | NOT_APPLICABLE | 507 | 50 | 1462 | not_audited_for_v2 | pending_not_run_on_v2 | fail_to_pass |
| 114-02 | ab2d | PASSED | PASS | True | aligned | ADOPTED | 806 | 89 | 1878 | not_audited_for_v2 | pending_not_run_on_v2 | fail_to_pass |
| 114-01 | ab2d | PASSED | PASS | True | aligned | OPTIONAL_NOT_USED | 734 | 70 | 1792 | not_audited_for_v2 | pending_not_run_on_v2 | pass_to_pass |
| 114-04 | ab2d | PASSED | PASS | True | aligned | PARTIAL | 2110 | 327 | 3900 | not_audited_for_v2 | pending_not_run_on_v2 | fail_to_pass |
| 114-08 | ab2d | PASSED | PASS | True | aligned | ADOPTED | 1437 | 170 | 2788 | not_audited_for_v2 | pending_not_run_on_v2 | pass_to_pass |
| 113-10 | ab2d | PASSED | PASS | True | aligned | ADOPTED | 893 | 100 | 2574 | not_audited_for_v2 | pending_not_run_on_v2 | pass_to_pass |
| 113-11 | ab2d | PASSED | PASS | True | aligned | ADOPTED | 1454 | 148 | 2951 | not_audited_for_v2 | pending_not_run_on_v2 | pass_to_pass |

## D. Qwen4B — v2 formal 8（含 v1→v2 + forensic）

| task | cond | status | layer | infra | align | adoption | chars | AST | tokens | forensic mechanism | v1→v2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 114-02 | ab1 | PASSED | PASS | True | aligned | NOT_APPLICABLE | 601 | 41 | 430 | — | pass_to_pass |
| 114-02 | ab2g | PASSED | PASS | True | aligned | NOT_APPLICABLE | 617 | 51 | 486 | — | fail_to_pass |
| 114-02 | ab2d | PARSE_MINOR | L1 | True | aligned | INSUFFICIENT_EVIDENCE | 3154 | 0 | 1772 | model_assembly_failure | fail_to_fail |
| 114-01 | ab2d | PASSED | PASS | True | aligned | OPTIONAL_NOT_USED | 653 | 65 | 593 | — | pass_to_pass |
| 114-04 | ab2d | INFRASTRUCTURE_FAILURE | L0_INFRA | False | aligned | NOT_APPLICABLE | 0 | 0 | None | infrastructure_failure | fail_to_infra_fail |
| 114-08 | ab2d | RUNTIME_FAILURE | L4 | True | aligned | PARTIAL | 7509 | 859 | 2427 | model_assembly_failure | fail_to_fail |
| 113-10 | ab2d | RUNTIME_FAILURE | L4 | True | aligned | ADOPTED | 1161 | 207 | 769 | model_assembly_failure | pass_to_fail |
| 113-11 | ab2d | RUNTIME_FAILURE | L4 | True | aligned | PARTIAL | 860 | 117 | 757 | model_assembly_failure | fail_to_fail |

## E. Qwen 9B — v2 formal 8（未執行）

| task | cond | status |
|---|---|---|
| 114-02 | ab1 | NOT_EXECUTED |
| 114-02 | ab2g | NOT_EXECUTED |
| 114-02 | ab2d | NOT_EXECUTED |
| 114-01 | ab2d | NOT_EXECUTED |
| 114-04 | ab2d | NOT_EXECUTED |
| 114-08 | ab2d | NOT_EXECUTED |
| 113-10 | ab2d | NOT_EXECUTED |
| 113-11 | ab2d | NOT_EXECUTED |

## F. v1→v2 outcome-change tallies（formal overlap8）

| Model | tallies |
|---|---|
| gemini-3.5-flash | `{"fail_to_pass": 4, "pass_to_pass": 4}` |
| qwen3.5:4b | `{"pass_to_pass": 2, "fail_to_pass": 1, "fail_to_fail": 3, "fail_to_infra_fail": 1, "pass_to_fail": 1}` |
| qwen3.5:9b | not_executed |

## G. L2 eligibility（v1 audit）與 Ab3

- L2 census: `{"eligible_existing_rule": 3, "eligible_new_rule_candidate": 5}`
- Existing rule: `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
- Ab3: repair_to_pass=0, triggered_any=0, v2_ab3=pending_not_run
- 允許清單僅 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`；本輪禁止 correct_answer wrap → Gemini 114-02 三格 no_op。

## G2. Qwen4B v2 Ab3（本輪更新）

- Allowlist: `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`（與 v1 Gemini Ab3 同版）
- Hash integrity all ok: `True`
- Eligible / noneligible: 0 / 4
- Healer executed: 0
- Rescue-to-pass: 0
- Classification: `{"skipped_noneligible": ["114-02 Ab2d", "114-08 Ab2d", "113-10 Ab2d", "113-11 Ab2d"]}`
- False-positive: none; on-disk candidates unmodified
- Backup: `docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/final_integration_report_01/backup_before_qwen4b_v2_ab3_20260718T052755Z`
- Artifact dir: `docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/qwen4b_v2_ab3_production_eval_01/`
## H. 研究結論

- Contract-aligned v2 在 formal overlap 消除 Gemini v1 兩類失敗（114-02 coefficients 巢狀；114-04 非法 Fraction 路徑）：Gemini v2 formal8 = 8/8 PASS（ITT=valid-response）。
- Qwen4B v2 formal8 = 3/8 ITT PASS；排除 114-04 timeout 後 valid-response = 3/7；殘敗經 forensic 歸為 assembly/routing/bloat，剩餘 prompt/API mismatch = 0。
- Qwen4B v2 Ab3（凍結 L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP，與 v1 Gemini 同版）：4 模型失敗格全數 noneligible；healer_executed=0；rescue-to-pass=0；無 false-positive。
- 殘敗 mechanism 本質上落在 allowlist 設計範圍外（非規則不夠聰明）；不可宣稱 v2 Healer 可救援 Qwen4B 此批失敗。
- qwen3.5:9b 與 Gemini v2 Ab3 仍未執行；不做模型規模趨勢推論。

## I. 研究限制

- v1 full18 與 v2 formal8 矩陣不同；僅 overlap8 可做成對 v1→v2 變化。
- L2 eligibility audit 僅涵蓋 v1；v2 失敗另以 forensic taxonomy 審查，未重跑 L2 audit。
- Ab3：v1 Gemini 與 v2 Qwen4B（本輪）已完成；Gemini v2 Ab3 仍 pending。
- Qwen 114-04 v2 timeout 屬 infrastructure；能力比較須用 valid-response 分母。
- 單一 seed（2026071301）；無多 seed 變異。
- v2 formal 跑次 Healer 關閉（healer_calls=0）。

## J. 缺失或待補

- qwen3.5:9b 相同 8-cell v2 執行
- Gemini v2 Ab3 / Healer production eval
- （可選）Qwen v1 Ab3 on existing-L2-eligible cells
- 多 seed 重複驗證
