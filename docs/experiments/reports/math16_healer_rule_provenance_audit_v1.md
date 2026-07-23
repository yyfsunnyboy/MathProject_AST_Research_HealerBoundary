# Math16 Healer 規則 Provenance Audit 報告 v1

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**文件類型：** 規則溯源稽核報告 (Rule Provenance Audit Report v1)
**建置時間 UTC：** 2026-07-23

---

> **固定位階聲明 (Mandatory Disclaimer)：**
> 本報告為 Evidence Complete 凍結後之 Post-hoc 規則溯源與學術宣告稽核文件。本報告**不得**修改、取代或重寫既有 Primary (Pass=83/320, Rescued=5) 與 Corrected (Pass=84/320, Rescued=6) 帳目，亦不重新執行模型、Healer 或 Evaluator。

---

## 1. Executive Verdict

1. **六條正式 Healer 規則分類統計**：
   - **`PRE_FROZEN_CONFIRMATORY` (分類 A)**: **0 條**。
   - **`PRE_EXISTING_BUT_MODIFIED_POST_HOC` (分類 B)**: **6 條**。
   - **`EXPLORATORY_POST_HOC_DISCOVERY` (分類 C)**: **0 條**（6 條規則之原型與邏輯均在 2026-07-20 18:22 UTC `d9aa264c` 之前完成實作與凍結，無任何 1 條係在 2026-07-21 22:33 UTC 接觸 4B 320-cell 結果後新增）。
   - **`PROVENANCE_UNRESOLVED` (分類 D)**: **0 條**。

2. **`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` 最終分類與定位**：
   - 分態判定：**`PRE_EXISTING_BUT_MODIFIED_POST_HOC` (分類 B)**。
   - 溯源證據：原型於 2026-07-17 00:28 UTC (`e098dc04`) 於早期 CE115 試驗中建立；於 2026-07-20 18:22 UTC (`d9aa264c`) 寫入 `math16_ab3_freeze_manifest.json` 正式凍結；於 2026-07-23 04:36 UTC (`d3b5a69c`) 進行可歸因之 runner false-loop rollback 防護修復 (Fix-count 分帳)。

3. **Primary Rescued = 5 的學術定位**：
   - **不可稱為 Confirmatory (驗證性效應)**。
   - 原因：六條 Healer 規則雖然在 4B 320-cell 實驗前完成凍結，但規則本身係於早期 CE115/CE113 開發資料集中事後歸納，且在 320-cell 救援實驗中僅於同批資料集 (Discovery Cohort) 上量測，尚未經未參與規則發現的獨立資料集驗證。

4. **Corrected 第 6 格的學術定位**：
   - 標的 Cell: `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301`
   - **定位：Technical Correction (技術勘誤說明/執行器 Bug 修復)**。
   - 說明：第 6 格之修復並非導因於 Healer 規則本體改動，而是 Evaluator runner false-loop rollback 機制之邏輯修復。依據雙軌維護規範，Primary 帳目固定為 5 (83/320)，Corrected 帳目標示為 6 (84/320)，兩者並存不回寫。

5. **是否需要獨立 Confirmatory Validation**：
   - **需要**。若欲宣稱 Healer 之通用外在效度 (External Validity)，必須在未參與規則設計與調整之新題目／新種子獨立資料集上進行 Confirmatory 驗證。

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

## 3. 六條 Healer 規則明細清單與 Audit 表格 (Rule-by-Rule Audit Table)

| Rule ID | First Commit | Discovery Source | Freeze Commit | Formal 320 Data Seen Before Freeze | Post-Freeze Change | Provenance Class | Independently Validated | Evidence Basis |
|---|---|---|---|---|---|---|---|---|
| `L1_CLOSE_UNBALANCED_PARENTHESIS` | `36126ce4` | CE115 syntax errors | `d9aa264c` | False | runner false-loop fix | `PRE_EXISTING_BUT_MODIFIED_POST_HOC` | False | `ce115_research_healer_rules_l1_paren_close.py` |
| `L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED` | `36126ce4` | CE115 syntax errors | `d9aa264c` | False | runner false-loop fix | `PRE_EXISTING_BUT_MODIFIED_POST_HOC` | False | `ce115_research_healer_rules_l1_delimiter_extended.py` |
| `L1_PROSE_RESIDUE_NARROW` | `36126ce4` | CE115 prose residue | `d9aa264c` | False | runner false-loop fix | `PRE_EXISTING_BUT_MODIFIED_POST_HOC` | False | `ce115_research_healer_rules_l1_prose_narrow.py` |
| `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | `e098dc04` | CE115 L2 wrap | `d9aa264c` | False | runner false-loop fix | `PRE_EXISTING_BUT_MODIFIED_POST_HOC` | False | `ce115_research_healer_rules_l2.py` |
| `L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM` | `1f016ef1` | CE113 kwargs bag | `d9aa264c` | False | runner false-loop fix | `PRE_EXISTING_BUT_MODIFIED_POST_HOC` | False | `ce115_research_healer_rules_l2_kwargs_bag_inline.py` |
| `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP` | `1f016ef1` | CE113 json dumps | `d9aa264c` | False | runner false-loop fix | `PRE_EXISTING_BUT_MODIFIED_POST_HOC` | False | `ce115_research_healer_rules_l2_json_dumps_unwrap.py` |

---

## 4. L2 Payload Wrap 專題深度稽核 (L2 Payload Wrap Deep Audit)

1. **規則首次出現時間**：2026-07-17 00:28 UTC (`e098dc04`)。
2. **是否早於六個正式案例存在**：**是**。六個正式 4B 案例生成於 2026-07-21 22:33 UTC，規則早於案例 4 天前即已實作與單元測試完成。
3. **Eligibility 條件**：
   - `oracle_answer_used = false` (100% 證明：只對字典結構作解包，不讀取答案內容)。
   - `unique = true` (僅允許單一最外層 key 且內含必要 payload 欄位)。
   - `local = true` (僅改寫 return 敘述句之字典結構)。
   - `offline_verifiable = true` (不依賴 LLM 或網路 API，純 AST/JSON 解析)。
4. **第 6 格修復性質**：第 6 格係導因於 Runner disposition-chain 中 `max_passes` 判定之迴圈誤判 Bug 修復，屬於 **Technical Correction**，不改變 Primary 5 (83/320) 的正式記錄。

---

## 5. 建議成果報告標準引用文字 (Required Reporting Language)

> **規則屬性與效用宣告標準表述：**
> 本研究使用的六條 Healer 規則均於正式 320-cell 實驗前完成實作與權威清單凍結 (`d9aa264c`)，且救援過程嚴格遵守 `oracle_answer_used = false` 之安全隔離。然而，鑑於規則原型係於前期開發資料集歸納，且本次救援量測均發生於同批實驗資料中，本修復結果屬事後探索性自然可修復窗口描述，不視為獨立確認性效應；未來仍需於未參與規則發現的獨立資料集上進行 Confirmatory 驗證。

---

## 6. 研究限制 (Methodological Limitations)

1. **同批資料規則發現風險 (Discovery Cohort Risk)**：規則雖然事前凍結，但規則優先順序與語意邊界曾參考早期開發數據。
2. **PASS 案例誤觸風險 (False Positive Risk)**：Healer 僅於 Baseline FAIL 格生效；若無 Eligibility 閘門防禦，可能於原本 PASS 格造成語意扭曲。
3. **9B Eligible = 0 的限制**：Qwen 9B 之 219 格 FAIL 多屬能力與模型本體輸出結構異常，未落入既有 6 條輕量級語法/結構 Healer 規則的修復窗口。
4. **Prompt 強化與 Healer 定位**：Healer 定位為零算力邊緣防禦層，無法取代 Prompt 規格補齊 (如 Spec-v2 +17) 或模型基礎能力提升。
5. **Six-Cell 小樣本限制**：正式 4B 救援樣本數為 5 格 (Corrected 6 格)，統計功率有限，結果應謹慎解讀。
6. **Deterministic Safety 不等於零副作用**：確定性規則僅保障語法與結構之轉換可重現，不代表對所有任意輸入均無副作用。
