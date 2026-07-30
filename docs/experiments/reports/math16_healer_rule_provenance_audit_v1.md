# Math16 Healer 規則 Provenance Audit 報告 v1 (Refined Classification Audit)

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**文件類型：** 規則溯源與雙層分類稽核報告 (Rule Provenance & Dual-Layer Classification Audit Report v1)
**建置時間 UTC：** 2026-07-23

---

> **固定位階聲明 (Mandatory Disclaimer)：**
> 本報告為 Evidence Complete 凍結後之 Post-hoc 規則溯源與雙層學術分類稽核文件。本報告**嚴禁**修改、取代或重寫既有 Primary (Pass=83/320, Rescued=5) 與 Corrected (Pass=84/320, Rescued=6) 帳目，亦不重新執行模型、Healer 或 Evaluator。

---

## 1. Executive Verdict

1. **六條正式 Healer 規則 Freeze 狀態與雙層分類統計**：
   - 六條 Healer 規則均在正式 Math16 320-cell generation (2026-07-21 22:33 UTC `9e948a5f`) 前於 `math16_ab3_freeze_manifest.json` (2026-07-20 18:22 UTC `d9aa264c`) 完成權威清單凍結。
   - 經 `git diff d9aa264c..HEAD` 逐檔比對實作原始碼，**六條規則本體（Detector、Eligibility、Abstain、Transform、Acceptance Criteria）在 Freeze 後 100% 完全未經任何修改 (`git diff` 輸出為空)**。
   - 後續修復 (`d3b5a69c`) 僅發生於 `ce115_research_healer_runner.py` 執行器迴圈邏輯 (`max_passes` false-loop rollback)，屬 **Runner-only Technical Fix**，不得錯算為規則本體修改。
   - **`rule_freeze_status`** 統計：
     - **`PRE_FROZEN_UNCHANGED`**: **6 條** (100%)
     - **`PRE_FROZEN_RULE_MODIFIED_POST_HOC`**: **0 條**
     - **`POST_HOC_RULE_DISCOVERY`**: **0 條**
     - **`UNRESOLVED`**: **0 條**
   - **`validation_status`** 統計：
     - **`PROSPECTIVE_WITHIN_MATH16_COHORT`**: **6 條** (對應 Primary 5 格救援效應)
     - **`INDEPENDENT_EXTERNAL_VALIDATION`**: **0 條** (未宣稱外部獨立驗證)
     - **`EXPLORATORY_REANALYSIS` / `POST_HOC_TECHNICAL_CORRECTION`**: **1 條** (對應 Corrected 第 6 格技術重算)

2. **Primary 5 的正確方法學定位**：
   > 六條 Healer 規則均在正式 Math16 320-cell generation 前完成凍結 (`d9aa264c`)，且 freeze 後未修改 detector、eligibility、transform 或 activation scope。因此 Primary 帳目的 5 格救援屬於預先固定規則在 Math16 cohort 上的前瞻性評估結果 (`PROSPECTIVE_WITHIN_MATH16_COHORT`)。由於規則源自先期 CE115／CE113 開發資料，且尚未在完全獨立資料集驗證，本研究不主張其為外部獨立確認性證據。

3. **Corrected 第 6 格的正確方法學定位**：
   > 第 6 格來自既有規則成功 transform 被 runner false-loop rollback 錯誤撤回後的技術修正。此修正未新增或修改 Healer 規則，因此不改變規則 freeze status (`PRE_FROZEN_UNCHANGED`)；但因屬正式結果揭露後的技術重算，只列入 Corrected technical account (`POST_HOC_TECHNICAL_CORRECTION`)，不回寫 Primary。

4. **`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 結構精確核對**：
   - **真實輸入結構**：模型生成的 `generate()` 函式可正常 Parse，且 `return` 回傳之字典符合標準三欄契約格式：
     ```python
     return {
         "question_text": ...,
         "correct_answer": ...,
         "oracle_payload": {"radicand": 135} # 或 {"expression": ...} 或純純量
     }
     ```
   - **問題本質**：模型於 `oracle_payload` 欄位內部填入單一 Key 包裹值（例如 `{radicand: 135}` 或衍生純量），而非最外層 `return` 字典只有單一 key。
   - **Transform 後結構**：Healer 僅解開 `oracle_payload` 內部多餘包裝，保持 `question_text` 與 `correct_answer` 100% 凍結未變。
   - **`oracle_answer_used = false` 實作證據**：Rule 實作僅檢查 JSON 結構與欄位 key 名稱，完全未讀取 `correct_answer` 之答案內容。

---

## 2. 規則開發與實驗時間線 (Timeline of Provenance Events)

| 時間 (UTC) | Commit Hash | 事件說明與標的 | 證據檔案／ Manifest 路徑與 SHA256 |
|---|---|---|---|
| 2026-07-17 00:28 | `e098dc04` | 首次建立 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 規則原型 | `agent_tools/finals_rebuild/ce115_research_healer_rules_l2.py` |
| 2026-07-18 16:02 | `1f016ef1` | 晉升 `L2_KWARGS_BAG` 與 `L2_JSON_DUMPS` 規則至生產環境 | `agent_tools/finals_rebuild/ce115_research_healer_rules_l2_*.py` |
| 2026-07-20 17:04 | `36126ce4` | 完成 3 L1 + 3 L2 六條 Healer 規則程式碼凍結 | `agent_tools/finals_rebuild/ce115_research_healer_rules_*.py` |
| 2026-07-20 18:22 | `d9aa264c` | 建立 `math16_ab3_freeze_manifest.json` 權威凍結清單 | `docs/experiments/manifests/math16_ab3_freeze_manifest.json` |
| 2026-07-21 22:33 | `9e948a5f` | 4B 320-cell 矩陣預註冊與 Generation 執行 | `docs/experiments/manifests/math16_pilot02_qwen4b_cell_plan.json` |
| 2026-07-22 16:30 | `d3b5a69c` | Six-Cell 救援稽核與 runner false-loop bug 重構 (Corrected=6) | `docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_result_manifest.json` |
| 2026-07-23 14:58 | `9e05050c` | 執行 Unrestricted Stress Test v1.1 正式實驗 (242 格) | `docs/experiments/manifests/math16_pilot02_qwen4b_unrestricted_stress_test_v11_result_manifest.json` |

---

## 3. 六條 Healer 規則雙層分類明細表 (Rule-by-Rule Dual-Layer Audit Table)

| Rule ID | First Commit | Freeze Commit | Git Diff (d9aa264c..HEAD) | Rule Freeze Status | Validation Status | Evidence Basis |
|---|---|---|---|---|---|---|
| `L1_CLOSE_UNBALANCED_PARENTHESIS` | `36126ce4` | `d9aa264c` | Empty (Unchanged) | `PRE_FROZEN_UNCHANGED` | `PROSPECTIVE_WITHIN_MATH16_COHORT` | `ce115_research_healer_rules_l1_paren_close.py` |
| `L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED` | `36126ce4` | `d9aa264c` | Empty (Unchanged) | `PRE_FROZEN_UNCHANGED` | `PROSPECTIVE_WITHIN_MATH16_COHORT` | `ce115_research_healer_rules_l1_delimiter_extended.py` |
| `L1_PROSE_RESIDUE_NARROW` | `36126ce4` | `d9aa264c` | Empty (Unchanged) | `PRE_FROZEN_UNCHANGED` | `PROSPECTIVE_WITHIN_MATH16_COHORT` | `ce115_research_healer_rules_l1_prose_narrow.py` |
| `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | `e098dc04` | `d9aa264c` | Empty (Unchanged) | `PRE_FROZEN_UNCHANGED` | `PROSPECTIVE_WITHIN_MATH16_COHORT` | `ce115_research_healer_rules_l2.py` |
| `L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM` | `1f016ef1` | `d9aa264c` | Empty (Unchanged) | `PRE_FROZEN_UNCHANGED` | `PROSPECTIVE_WITHIN_MATH16_COHORT` | `ce115_research_healer_rules_l2_kwargs_bag_inline.py` |
| `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP` | `1f016ef1` | `d9aa264c` | Empty (Unchanged) | `PRE_FROZEN_UNCHANGED` | `PROSPECTIVE_WITHIN_MATH16_COHORT` | `ce115_research_healer_rules_l2_json_dumps_unwrap.py` |

---

## 4. L2 Payload Wrap 專題結構核對 (L2 Payload Wrap Structural Audit)

1. **觸發前結構 (Before Structure)**：
   ```python
   def generate(level=1, **kwargs):
       return {
           "question_text": r"化簡根式 \sqrt{135}",
           "correct_answer": "3\sqrt{15}",
           "oracle_payload": {"radicand": 135} # 帶有單一內部 Key 包裹
       }
   ```
2. **Transform 後結構 (After Structure)**：
   ```python
   def generate(level=1, **kwargs):
       return {
           "question_text": r"化簡根式 \sqrt{135}",
           "correct_answer": "3\sqrt{15}",
           "oracle_payload": {"radicand": 135} # 保持平鋪標準結構
       }
   ```
3. **`oracle_answer_used = false` 實作證據**：
   - 規則實作於 `ce115_research_healer_rules_l2.py`，僅檢查 `ast.Dict` 結構與 `oracle_payload` 內部 key/value 形態，對 `correct_answer` 僅執行 Fingerprint 變更防護 Guard，**零讀取解答內容**。

---

## 5. 正式結果數字對齊 (Preserved Formal Accounts)

本稽核完全尊重既有正式結果分帳，不進行任何改寫：
- **Qwen 4B Baseline Pass**: `78 / 320`
- **Primary Eligible**: `10` 格
- **Primary Rescued**: `5` 格 (Pass $\rightarrow$ `83 / 320`)
- **Corrected Rescued**: `6` 格 (Pass $\rightarrow$ `84 / 320`，技術修正，不回寫 Primary)
- **Qwen 9B Baseline Pass**: `101 / 320`
- **242 Baseline FAIL 互斥帳目**: `NO_RULE_CANDIDATE=231`, `UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE=10`, `AMBIGUOUS_MULTIPLE_CANDIDATES=1`

---

## 6. 研究限制 (Methodological Limitations)

1. **同批資料規則發現風險 (Discovery Cohort Risk)**：規則原型雖然在 4B 實驗前凍結，但早期開發曾參考同系列開發數據。
2. **獨立驗證尚未執行 (No External Independent Validation)**：本研究尚未於完全獨立之新 Task 數據庫驗證通用效度。
3. **Runner 邏輯對救援結果之敏感性**：Runner 迴圈機制修正可影響極端邊界 cell (如第 6 格)，凸顯執行器規格嚴謹性之重要性。

---

## 7. Healer 世代切割：舊版工程 Healer vs Math16 Conservative Healer

| 世代 | 路徑／定位 | 目標與治理 |
|---|---|---|
| 舊版工程 Healer | `core/healers`（regex／AST／unified cleanup 等歷史庫） | **工程導向**：優先恢復可執行／可解析；含較寬鬆或探索性修復路徑 |
| Math16 正式 Healer | `agent_tools/finals_rebuild/ce115_research_healer_rules_*.py` 等凍結規則＋FAIL-only runner | **研究導向**：deterministic、evaluator-blind、保守拒修（Abstain）、固定 eligibility／journal 證據 |

**強制切割聲明：**

1. 舊版 `core/healers` **只作為歷史來源／盤點對象**，**不參與** Math16 Round 1 正式修補決策。
2. Math16 Conservative／Aggressive cumulative 規則之 **detector／eligibility／abstain／transform／acceptance** 為獨立重寫之修補決策模組；正式決策鏈不以舊版工程 Healer 輸出為準。
3. 若存在共用底層能力（例如 Python 標準庫 `ast.parse`、通用字串／檔案工具），僅屬基礎設施共用；**不得**宣稱「整套 Healer 與舊系統完全不共用任何程式碼」，也**不得**反過來說「舊系統仍在做正式修補」。
4. 可主張範圍：本節界定 **lineage／決策邊界**；不改寫既有 Primary／Corrected／Round 1 數字帳。

---

## 8. Development 40／Evaluation 120 資料分帳與可主張範圍

權威切分數值見 `docs/experiments/reports/math16_method1_40_120_split_results_report_v1.md` 與 Final Report 第 11 節（Contract-Aware 160 子集）。

**矩陣與切分定義（必須明示）：**

1. Round 1 全量：**16題 × 4條件 × 5 seeds = 320**。
2. Contract-Aware 子集**僅含** `ab2d` + `ab2d_spec_v2`：**16題 × 2條件 × 5 seeds = 160**。
3. Development：**4×2×5=40**；Evaluation：**12×2×5=120**；**40+120=160**，只是 320 的子集，非新實驗。
4. `ab1`／`ab2g` **仍在** 320 總體結果中，但因**無 domain API／function contract**，不納入此 Contract-Aware split；**不得**推論為一般 Healer 完全不能作用於 `ab1`／`ab2g`。

| 範圍 | Baseline → Final | verified rescue |
|---|---|---:|
| Development 40 | 11/40 → 11/40 | **0** |
| Evaluation 120 | 33/120 → 37/120 | **4**（該切分內全部 rescue） |

**治理措辭（口試／報告必須遵守）：**

1. Development 40 用於理解失敗模式與規則／Guard 設計討論；**不宣稱**「開發集完全未見」或零資訊外洩。
2. 該切分內 **全部 verified rescue 落在獨立 Evaluation 120**；Development 40 verified rescue＝**0**。
3. 結論只能寫成：**支持非題目客製化**（規則未在 Development 40 刷出 PASS）；**不得**宣稱完全無污染風險。
4. 後續 Aggressive／Tier B–D 規則採通用 AST／結構 pattern；development influence 仍以 **frozen-rule benchmark**（固定規則、FAIL-only、journal）控制，不得把開發觀察直接升格為正式泛化保證。
5. Development 40／Evaluation 120 與三模型 Round 1 全量 320 headline **分帳**，不得加總混報；Method 1 之 Dev rescue＝0／Eval rescue＝4 **不得**與 Round 1 Aggressive overlay（corrected **79→87／rescue 8**；frozen archive 79→88／9）混稱。

---

## 9. Qwen 4B cell-wise fixpoint replay（post-hoc 機制結果）

權威結果：`docs/experiments/results/math16_qwen4b_cellwise_fixpoint_replay_v1/summary.json`
Protocol：`docs/experiments/design/math16_qwen4b_cellwise_fixpoint_replay_protocol_v1.md`

| 項目 | 值 |
|---|---|
| 輸入 | Round 1 final 後仍 FAIL 的 **232** cells |
| 永久排除 | Round 1 final 已 PASS 的 **88** cells（本輪未掃描） |
| `ZERO_CHANGE_CONVERGENCE` | **232**（全部於第一輪 zero-change） |
| `ITERATIVE_RESCUE` | **0**（additional verified rescue＝0） |
| `CYCLE_DETECTED` | **0** |
| `MAX_ROUND_NON_CONVERGENT` | **0** |
| model calls | **0** |

**可主張：**

1. 在現有凍結規則與固定順序 `A→B→C1→C2→D3→D1→D5→D2` 下，Round 1 後殘餘 FAIL 再跑完整一輪 stack，**全部第一輪即無 source 變更** → 現有 Healer 對 4B residual 已達**操作上的 fixpoint**。
2. 此為 **4B-only post-hoc mechanism pilot**，**不得覆寫** Round 1 三模型主表；亦**不是**三模型協定所稱之「Round 2 正式主分析覆寫」。

**不可主張：**

1. **不得**把本輪觀察到的 regression＝0（或 journal 內 regression 欄位）當作**新的安全性證據**：本輪**未掃描** 88 個 PASS cells。
2. 正式 regression 證據仍來自 Round 1／Method 2 等已封存帳（例如 Method 2 measured regression＝0/320；Round 1 三模型 regression＝0）。

---

## 10. Aggressive Healer full 320-cell safety benchmark（尚未執行）

**定義：** `Aggressive Healer full 320-cell safety benchmark`＝對全量 320 cells **同時掃描原始 PASS／FAIL**，量測 verified rescue、preserved pass、PASS→FAIL regression、net PASS change。

**狀態：** **尚未執行**；列為**後續工作**。

**不得混稱：** 本 benchmark **不是** Method 2（已封存之 Raw／Final 雙路評分）、**不是**三模型 Round 2 正式覆寫、**也不是** 4B-only fixpoint（僅掃 232 FAIL、排除 88 PASS）。fixpoint 不得冒充本 benchmark 之 regression 安全證明。
