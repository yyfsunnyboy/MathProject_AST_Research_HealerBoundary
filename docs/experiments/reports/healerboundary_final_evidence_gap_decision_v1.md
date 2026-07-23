# HealerBoundary 最終證據缺口決策 v1

## 1. Executive Decision

`DECISION 1: NO_ADDITIONAL_EXPERIMENT_REQUIRED_BEFORE_FINAL`

現有證據已足以支持受限於 Math16 cohort 的核心邊界結論與答辯；外部獨立驗證只影響跨資料集、跨模型與公開 benchmark 的泛化主張，不影響既有 Primary/Corrected 分帳或「自然介入窗口狹窄」的結論。

## 2. Evidence Matrix

| 主張 | 判定 | 證據路徑與關鍵數字 | 限制 | 影響核心結論 |
|---|---|---|---|---|
| 1. Prompt 條件影響 baseline | COMPLETE | Final Report §15：4B 15/80、19/80、8/80、36/80；9B 18/80、27/80、16/80、40/80 | Gemini spec 版本不同 | 否；僅限條件性描述 |
| 2. 六條規則事前凍結 | COMPLETE | provenance audit §1、§3：6/6 `PRE_FROZEN_UNCHANGED`，`d9aa264c` | 規則源自先期開發資料 | 是 |
| 3. Primary 5 為 cohort 內前瞻評估 | SUFFICIENT_WITH_LIMITATION | provenance audit §1：`PROSPECTIVE_WITHIN_MATH16_COHORT`；78/320→83/320，eligible=10、rescued=5 | 非外部獨立驗證 | 是 |
| 4. Corrected 第 6 格為 runner 勘誤 | COMPLETE | provenance audit §1；Appendix A §1：false-loop rollback，Corrected=6、84/320 | 僅列 technical account | 是 |
| 5. 231/242 無規則候選 | COMPLETE | Appendix B §2：231 no-rule、10 unique、1 ambiguous | 僅限凍結六條規則與此 cohort | 是 |
| 6. Forced ambiguity 支持 Abstain gate | SUFFICIENT_WITH_LIMITATION | Appendix B §3–4：1 格 forced arm 為 FAILED，`observed_harm_prevented=not_demonstrated` | 單一案例；不證明避免實際傷害 | 是 |
| 7. 9B eligible=0 的範圍 | COMPLETE | Final Report §10–11、§18：9B 101/320、eligible=0、219 FAIL | 不代表 9B 無失敗或永不需要 Healer | 否 |
| 8. 自然介入窗口狹窄 | SUFFICIENT_WITH_LIMITATION | Appendix B：231/242 no-rule，10/242 unique；Primary rescued=5 | 不可外推為所有程式生成工作 | 是 |
| 9. 不適合一般語意修復 | SUFFICIENT_WITH_LIMITATION | Final Report §16、§18；Appendix B forced ambiguity | 是拒絕邊界證據，不是所有語意錯誤的完整測試 | 是 |
| 10. 尚未外部獨立驗證 | OPTIONAL_FUTURE_WORK | provenance audit §1、§6：`INDEPENDENT_EXTERNAL_VALIDATION=0` | 缺口限制泛化，不推翻 Math16 cohort 結論 | 否 |
| 11. PASS 誤觸／regression 風險 | SUFFICIENT_WITH_LIMITATION | Final Report §18：Observed Regression=0；Appendix B §3：new failure=0 | 非零副作用保證，未做長期監測 | 是 |
| 12. 跨模型、題庫、公開 benchmark 泛化 | OPTIONAL_FUTURE_WORK | Final Report §18 明定 16 tasks、3 models、4 prompts、5 seeds 範圍 | 尚無跨資料集或公開 benchmark 證據 | 否 |

**矩陣計數：** COMPLETE=5；SUFFICIENT_WITH_LIMITATION=5；REQUIRED_BEFORE_FINAL=0；OPTIONAL_FUTURE_WORK=2；NOT_SUPPORTED=0。

## 3. Required Before Final

無。現有資料沒有使核心結論失效的證據缺口：規則凍結、Primary/Corrected 分帳、候選分層與限制聲明均可由正式 artifacts、manifests 與 Evidence Complete 追溯。

## 4. Optional Future Work

1. 完全未參與規則開發的獨立資料集驗證。
2. 更多模型、題型與公開 benchmark 的泛化測試，以及長期 regression 監測。

這些工作只擴張外推範圍；不得為增加 rescues 而回寫 Primary 帳目或改動凍結規則。

## 5. Independent Validation Decision

外部獨立驗證是 `OPTIONAL_FUTURE_WORK`，不是正式成果提交前的必要條件。因此不啟動額外驗證實驗；既有 Primary=5 與 Corrected=6 保持凍結分帳。

## 6. 最小驗證方案

不適用於本次 final go/no-go。若日後進行，必須使用未參與六條規則開發的題目，維持規則、Prompt 與 Evaluator 凍結，事前定義樣本與停止條件，並將其獨立標記為 confirmatory，不影響既有 Primary 帳目。

## 7. 可直接放入成果報告的限制文字

> 本研究已證明，在Math16 cohort中，預先凍結的deterministic Healer僅能介入少數具有唯一、局部且離線可驗證結構證據的失敗；多數失敗沒有安全規則候選。此結論描述的是本研究條件下的自然介入邊界，不主張已完成跨資料集、跨模型或公開benchmark的外部泛化驗證。

## 8. Final Go／No-Go Verdict

`GO_FOR_FINAL_SUBMISSION_WITH_SCOPE_LIMITATION`

可答辯的核心結論是「Math16 cohort 中的窄範圍 deterministic repair boundary」，不是一般化修復能力或外部泛化效果。故不需要新增獨立驗證實驗才可形成完整的受限研究結論。
