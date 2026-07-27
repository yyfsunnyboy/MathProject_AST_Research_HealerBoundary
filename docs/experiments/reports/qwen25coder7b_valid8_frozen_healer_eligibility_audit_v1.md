# Qwen2.5-Coder:7B Valid-Failure Frozen Healer Eligibility Audit v1

- **狀態**：唯讀稽核產物。不修改原始7B artifacts、`qwen25coder7b_smoke_corrected_accounting_v1.md`、`smoke_pipeline_known_issues_v1.md`、正式v4結果、Healer程式碼。
- **母體**：僅審查 `qwen25coder7b_smoke_corrected_accounting_v1.md` 已確認的8個有效FAIL cell（K1的3格INVALID_CONTRACT不在此次審查範圍）。
- **不執行**：模型呼叫、repair套用、oracle重評、Healer runner。
- **判定方式**：`EXECUTED_DIAGNOSTIC`（見下）。

---

## 步驟A：定位唯一權威frozen規則

| 項目 | 內容 |
|---|---|
| **規則名稱** | `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` |
| **實作檔案** | `agent_tools/finals_rebuild/ce115_research_healer_rules_l2.py` |
| **matcher函數** | `analyze_l2_payload_wrap(source, frozen)`（核心分析函數；`is_applicable()`／`is_triggered()`為其包裝，`apply()`為實際transform，本輪僅呼叫前者，不呼叫`apply()`） |
| **guards（依檢查順序）** | `single_frozen_key`（frozen context必須恰為單一key）→ `parse_ok` → `return_has_oracle_payload` → `payload_static_scalar`（`oracle_payload`欄位須能靜態解析為純量）→ `scalar_equals_frozen_value` → `correct_answer_present` → `already_wrapped`（若已是`{frozen_key:scalar}`形式則視為no-op，非triggered） |
| **freeze文件／manifest** | `docs/experiments/manifests/math16_ab3_freeze_manifest.json`（`manifest_id: math16_ab3_freeze_v1`），`frozen_rule_allowlist`第4條列出`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`（layer L2, priority 100） |
| **freeze版本／hash／commit證據** | 首次原型commit `e098dc04`（2026-07-17 00:28 UTC）；規則本體凍結commit `d9aa264c`（2026-07-20 18:22 UTC，即`math16_ab3_freeze_manifest.json`建立時點）；`docs/experiments/reports/math16_healer_rule_provenance_audit_v1.md`確認`git diff d9aa264c..HEAD`對此規則實作檔為空（`PRE_FROZEN_UNCHANGED`），即規則自凍結後**逐字未改動**，早於4B 320-cell正式generation（commit`9e948a5f`，2026-07-21 22:33 UTC） |
| **原始Math16 verified rescue案例數** | 規則本身docstring聲明其**發源證據**僅限單一預先核准fixture`fail_radical_ab1_l2`（schema_failure→passed，屬Math16之前的CE115開發資料，非Math16 cohort）。在**Math16 pilot02 cohort內**，依`docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_manifest.json`與`docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/overall_summary.json`（`rule_applied_counts.L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP: 6`），此規則在Qwen3.5:4B正式320-cell語料中共應用於**6格**（5格primary rescued + 1格post-hoc incremental pass），全部條件為`Ab2g`／`Ab2d+api`／`Ab2d+spec`，**無`Ab1`案例**；task涵蓋`ce115_calc_radical_simplification_l1`、`ce113_q01_negative_fraction_subtraction`、`ce112_q04_radical_simplification`。**此6格均屬Qwen3.5:4B，與本輪審查的Qwen2.5-Coder:7B完全是不同模型的產物**，僅作為規則本身有效性佐證，不得直接套用於7B。 |

---

## 步驟B/C：逐格matcher／guard判定

**判定方式**：`EXECUTED_DIAGNOSTIC`。`analyze_l2_payload_wrap()`是既有、已凍結、純AST靜態分析函數（無副作用、不寫檔、不呼叫模型），本輪直接import並以每格的`extracted_candidate.py`原始碼與該task的`frozen_params`（= `sample_task_parameters()`實際採樣輸出，與 [qwen25coder7b_valid8...] 各格對照確認）作為輸入呼叫之，**只呼叫`analyze_l2_payload_wrap()`，未呼叫`apply()`**，未套用transform，未寫回任何artifact。診斷腳本位置（scratch，唯讀呼叫用，不屬正式程式碼庫）：`C:\Users\yehiv\AppData\Local\Temp\claude\...\scratchpad\run_l2_matcher_diagnostic.py`（僅本次session暫存，不在repo內，不影響git狀態）。

| # | task/condition | corrected failure type | candidate中的直接問題 | matcher（applicable）各predicate | guard各predicate結果 | 最終eligibility | 判定方式 | direct evidence path |
|---|---|---|---|---|---|---|---|---|
| 1 | ce115_calc_polynomial_division_l1/ab1 | VALID_MODEL_OUTCOME (runtime_failure) | frozen={2 keys}；oracle_payload欄位= `{dividend_coefficients, divisor_coefficients}`（inline dict，2 keys） | parse_ok=True; return_has_oracle_payload=True → **applicable=True** | single_frozen_key=**False**（frozen有2 key）→ guard鏈在第一關即失敗，reason=`frozen_not_single_key` | **MATCHER_HIT_GUARDS_FAIL** | EXECUTED_DIAGNOSTIC | `.../qwen25coder7b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301/extracted_candidate.py` |
| 2 | ce115_calc_polynomial_division_l1/ab2g | VALID_MODEL_OUTCOME (runtime_failure) | 同上，frozen 2 key，oracle_payload為inline 2-key dict | applicable=True | single_frozen_key=**False**，reason=`frozen_not_single_key` | **MATCHER_HIT_GUARDS_FAIL** | EXECUTED_DIAGNOSTIC | `.../qwen25coder7b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301/extracted_candidate.py` |
| 3 | ce111_q03_prime_factor_selection/ab1 | VALID_MODEL_OUTCOME (schema_failure) | frozen={candidates,n}（2 key）；oracle_payload= `{"candidates":candidates,"n":n}`（inline 2-key dict） | applicable=True | single_frozen_key=**False**，reason=`frozen_not_single_key` | **MATCHER_HIT_GUARDS_FAIL** | EXECUTED_DIAGNOSTIC | `.../qwen25coder7b__ce111_q03_prime_factor_selection__ab1__seed_2026071301/extracted_candidate.py` |
| 4 | ce111_q05_exact_fraction_expression/ab1 | K2有效FAIL（label錯誤，真實答錯40/99 vs 4/11） | frozen={expression}（1 key，通過single_frozen_key）；但oracle_payload= `{"expression": expression}`（return中直接是Dict字面值，非可解析純量） | applicable=True | single_frozen_key=**True**；`_already_wrapped()`檢查：payload本身即為`{key:value}`形式，但**key是變數expression的值而非常數字面**——實際上該Dict在AST上key="expression"(常數字串)、value=Name("expression")，並非scalar；guard鏈於`payload_static_scalar`失敗（`_resolve_scalar`對Dict節點無法解析出純量），reason=`payload_not_static_scalar` | **MATCHER_HIT_GUARDS_FAIL** | EXECUTED_DIAGNOSTIC | `.../qwen25coder7b__ce111_q05_exact_fraction_expression__ab1__seed_2026071301/extracted_candidate.py` |
| 5 | ce111_q05_exact_fraction_expression/ab2d | VALID_MODEL_OUTCOME (runtime_failure) | frozen={expression}（1 key）；return中`oracle_payload`是對變數`oracle_payload`（先前賦值為`{"expression": expression}`）的Name參照 | applicable=True | single_frozen_key=**True**；`_resolve_scalar`沿Name→賦值鏈找到該Dict節點，Dict本身非scalar，guard於`payload_static_scalar`失敗，reason=`payload_not_static_scalar` | **MATCHER_HIT_GUARDS_FAIL** | EXECUTED_DIAGNOSTIC | `.../qwen25coder7b__ce111_q05_exact_fraction_expression__ab2d__seed_2026071301/extracted_candidate.py` |
| 6 | ce115_calc_radical_simplification_l1/ab1 | K2有效FAIL（label錯誤，真實答錯：radicand未化簡） | frozen={radicand:27}（1 key）；return中`oracle_payload`為Name參照，先前賦值`oracle_payload = {"radicand": radicand}`（Dict，value為Name("radicand")非常數） | applicable=True | single_frozen_key=**True**；`_resolve_scalar`解析到Dict節點，非scalar，guard於`payload_static_scalar`失敗，reason=`payload_not_static_scalar` | **MATCHER_HIT_GUARDS_FAIL** | EXECUTED_DIAGNOSTIC | `.../qwen25coder7b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301/extracted_candidate.py` |
| 7 | ce115_calc_radical_simplification_l1/ab2g | K2有效FAIL（label錯誤，同上真實答錯機制） | 同#6結構（oracle_payload為Name→Dict賦值鏈） | applicable=True | single_frozen_key=**True**，guard於`payload_static_scalar`失敗，reason=`payload_not_static_scalar` | **MATCHER_HIT_GUARDS_FAIL** | EXECUTED_DIAGNOSTIC | `.../qwen25coder7b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301/extracted_candidate.py` |
| 8 | ce115_calc_radical_simplification_l1/ab2d_spec_v2 | VALID_MODEL_OUTCOME (answer_incorrect) | frozen={radicand:27}（1 key）；`oracle_payload = {"radicand": 27}`為inline dict，value是常數27（非Name），但仍是Dict節點本身，非scalar | applicable=True | single_frozen_key=**True**；payload_value本身即為Dict（`{"radicand": 27}`），`_resolve_scalar`對Dict節點直接回`_MISSING`（該函式只解析`ast.Constant`/`ast.Name`/`kwargs.get(...)`/`kwargs[...]`四種可解析為scalar的形態，Dict字面值本身不在其列），guard於`payload_static_scalar`失敗，reason=`payload_not_static_scalar` | **MATCHER_HIT_GUARDS_FAIL** | EXECUTED_DIAGNOSTIC | `.../qwen25coder7b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301/extracted_candidate.py` |

（路徑前綴皆為 `docs/experiments/results/qwen25coder7b_math16_four_condition_smoke_20260725_001/`）

verified 8/8（每格皆以`analyze_l2_payload_wrap()`實際執行，非人工比對規則名稱或語意相似度）。

**abstention／no-match原因彙整**：本規則的設計目標是修復「模型把`oracle_payload`寫成裸純量（例如`oracle_payload: 135`），而非依規格包成`{frozen_key: 135}`字典」這一種特定結構缺陷（見規則docstring與`math16_healer_rule_provenance_audit_v1.md`第4節之「觸發前結構」範例）。**Qwen2.5-Coder:7B在全部8格中，`oracle_payload`欄位從未出現裸純量**——它要嘛回傳多鍵字典（#1,2,3；且這些task本身frozen就是多鍵，guard`single_frozen_key`直接排除），要嘛回傳單鍵字典或對單鍵字典變數的參照（#4,5,6,7,8；guard`payload_static_scalar`排除，因為Dict字面值/Dict型別的變數參照都不算「純量」）。也就是說，**這8格的失敗成因，全部落在此規則designed覆蓋範圍之外**：#1,2,3,5,6,7,8屬於runtime_failure/schema_failure/K2答案內容錯誤，與`oracle_payload`結構完全無關；#4的「40/99 vs 4/11」是答案內容錯誤，同樣不是`oracle_payload`結構問題。此規則`oracle_answer_used=false`（只檢查結構，不讀答案內容），因此天生不可能修復K2這種「答案內容錯誤」的cell——這點在matcher/guard層級即可確認，不需重跑oracle。

---

## 統計

1. `MATCHER_HIT_GUARDS_PASS`：**0**
2. `MATCHER_HIT_GUARDS_FAIL`：**8**
3. `NO_MATCH`：**0**
4. `UNRESOLVED`：**0**

## confirmed eligible cell清單

**無**。8格中沒有任何一格達成`MATCHER_HIT_GUARDS_PASS`，因此沒有cell可稱為frozen-rule eligible或natural matcher hit。

## 是否存在Coder 7B自然命中

**NO**。依據：8/8格皆為`EXECUTED_DIAGNOSTIC`（非靜態人工猜測），guard鏈在`single_frozen_key`或`payload_static_scalar`階段確定性失敗，無一格達到`triggered=True`。此結論具體、可重現（純AST靜態分析，非機率性），非UNRESOLVED。

---

## 舊eligibility結論撤回

沿用`qwen25coder7b_smoke_corrected_accounting_v1.md`已撤回之`1/11 eligible`（該文件已標記為「撤回或改為未驗證」）。**本輪據此正式補完**：8個有效FAIL母體中，`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`規則之eligible數為**0（非1，非任何非零值）**。任何先前暗示「Coder 7B有cell可套用既有Healer規則修復」的表述（包含但不限於`1/11`此類分母/分子）**必須撤回**：無論分母取11、13或8，經本輪實際matcher/guard執行，分子皆應為0（就`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`而言）。本輪未審查其餘5條frozen規則（`L1_CLOSE_UNBALANCED_PARENTHESIS`／`L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED`／`L1_PROSE_RESIDUE_NARROW`／`L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM`／`L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP`），故不對這8格是否符合其餘5條規則做任何判定——若先前結論涉及這5條規則對7B的eligibility，狀態應為**未驗證**，非本輪確認範圍。

---

## 起始／結束Git狀態

- 起始：`main` @ `c5bddac8`，origin/main同步，2個既存modified正式檔案未變動，untracked清單與任務起始時一致。
- 結束：與起始相同，僅新增本文件；原始7B artifacts、corrected accounting文件、known-issues文件、正式v4結果、Healer程式碼**全部未修改**；未stage、未commit、未push。scratch診斷腳本存於session暫存目錄，不在repo內，不影響git狀態。

## 新增檔案清單

- `docs/experiments/reports/qwen25coder7b_valid8_frozen_healer_eligibility_audit_v1.md`（repo內，本次唯一新增）
- `C:\Users\yehiv\AppData\Local\Temp\claude\...\scratchpad\run_l2_matcher_diagnostic.py`（session暫存，非repo檔案，僅用於唯讀呼叫既有matcher函數）
