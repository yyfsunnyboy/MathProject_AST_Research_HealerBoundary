# Math16 最終評審論述風險審查 v1

## 1. 六條規則是否在看完正式 320 格後才寫？
**建議回答：** 不是；六條規則在正式 320-cell generation 前於 `d9aa264c` 凍結，之後未修改 detector、eligibility、transform 或 activation scope。
**支持證據：** provenance audit 記錄 6/6 為 `PRE_FROZEN_UNCHANGED`。
**限制：** 規則來自先期開發資料，尚無獨立外部驗證。
**禁止說法：** 「已完成外部確認性驗證」。

## 2. Primary 5 為何可以算前瞻性結果？
**建議回答：** Primary 的 5 格是凍結規則在 Math16 cohort 內的前瞻性評估，分類為 `PROSPECTIVE_WITHIN_MATH16_COHORT`。
**支持證據：** 4B baseline 78/320、eligible 10、Primary rescued 5、Primary final 83/320。
**限制：** cohort 內前瞻性不等於外部獨立驗證。
**禁止說法：** 「Primary 5 是外部獨立確認證據」。

## 3. Corrected 第 6 格是否為事後灌水？
**建議回答：** 不是新增救援規則；它是既有成功 transform 被 runner false-loop rollback 錯誤撤回後的技術勘誤。
**支持證據：** Corrected rescued 6、final 84/320；規則仍為 `PRE_FROZEN_UNCHANGED`。
**限制：** 這是正式結果揭露後的 `POST_HOC_TECHNICAL_CORRECTION`。
**禁止說法：** 「Corrected 6 等同 Primary 6」。

## 4. 為何不只強化 Prompt，而需要 Healer？
**建議回答：** Prompt 降低生成錯誤；Healer 處理生成後仍存在、可由唯一局部離線結構證據判定的窄型契約錯誤，兩者功能不同。
**支持證據：** 4B 四種 Prompt 條件下仍有 242 個 baseline FAIL，其中 10 格符合唯一候選條件。
**限制：** Healer 不是 Prompt 替代品，也不能修正一般語意或邏輯錯誤。
**禁止說法：** 「Healer 優於 Prompt」。

## 5. 231/242 沒有規則候選，是否代表 Healer 失敗？
**建議回答：** 不是資料缺失；這是核心負面結果，表示多數失敗沒有唯一、安全、離線可驗證的 deterministic repair candidate。
**支持證據：** 242 個 4B baseline FAIL 中，`NO_RULE_CANDIDATE=231`、unique primary eligible=10、ambiguous=1。
**限制：** 這只描述此規則庫與 Math16 cohort，不代表所有程式失敗。
**禁止說法：** 「231 格代表 Healer 無效」。

## 6. PASS 案例若 detector 誤觸，會不會造成 regression？
**建議回答：** Healer 不應對已通過案例任意改寫；detector、eligibility 與 abstain gate 必須分離。
**支持證據：** 本次結果的 Observed Regression=0，且 repair candidate 必須唯一、局部、可離線驗證。
**限制：** Observed Regression=0 不代表零副作用或一般語意安全保證。
**禁止說法：** 「Healer 保證安全」。

## 7. 9B eligible=0，是模型太強還是規則沒用？
**建議回答：** 只能說 9B 在此 cohort 沒有出現六條規則可捕捉的失敗型態。
**支持證據：** 9B baseline/final 為 101/320，eligible=0；其餘 219 格 FAIL 未命中現有凍結規則。
**限制：** 不能推論 9B 永遠不需 Healer，也不能推論規則涵蓋所有錯誤。
**禁止說法：** 「9B 完全不需要 Healer」。

## 8. 只有 6 格成功，樣本是否太少、能否泛化？
**建議回答：** Six-Cell 結果是機制驗證與自然窗口描述，不是大樣本外部泛化證據。
**支持證據：** Primary rescued=5，Corrected technical account=6；231/242 沒有安全候選。
**限制：** 仍需未參與規則開發的獨立資料驗證。
**禁止說法：** 「六格證明可泛化」。

## 最後 30 秒結論

本研究最重要的發現不是 Healer 修了很多，而是證明它只在極窄、可唯一判定的結構錯誤中有價值。Primary 帳目中 5 格被預先凍結規則救回，但 231/242 失敗沒有安全候選，顯示 deterministic repair 的邊界遠比一般想像更窄。這讓 Healer 從「萬用修復器」重新定位成只在明確邊界內介入的小柵欄。
