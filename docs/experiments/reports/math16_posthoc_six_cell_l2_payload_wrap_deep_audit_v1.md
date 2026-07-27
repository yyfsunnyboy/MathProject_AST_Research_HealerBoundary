# Math16 Post-hoc Six-Cell L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP Verified Rescue — 深度稽核 v2

- **性質**：唯讀 post-hoc evidence audit。未修改任何既有程式、artifact、正式v4結果、Healer規則、freeze manifest或既有正式文件；未呼叫模型；未新增或放寬規則；未覆寫評分；未改寫歷史帳目。
- **允許並使用之操作**：(1) 純讀取 artifact／manifest／jsonl；(2) 匯入既有凍結 matcher/guard 函數 `analyze_l2_payload_wrap()` 做唯讀分析；(3) 對既有 before/after artifact 做**不寫回**的 deterministic replay（呼叫既有 `apply()`，只在記憶體中比對雜湊，不落地任何檔案）；(4) 讀取既有測試/fixture 檔案。
- **結論範圍限制**：本報告結論僅適用於——本正式 cohort（Qwen3.5:4B math16_pilot02）、此凍結規則版本（`d9aa264c`後未變動）、此6格 verified rescue、本次可重現的 matcher/guard/transform 證據。**不外推**跨模型、跨task或一般 APR 通用性。**本輪不納入 Qwen2.5-Coder 7B 對照**。

---

## 一、研究母體確認（Set A ∩ B ∩ C）— **SCOPE_MISMATCH**

依規格定義三個集合，逐一從凍結證據重建：

**Set A**（規則`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`實際套用＝`applied_rules`非空、`healer_decision="transformed"`，取自primary `eligible_execution_records.jsonl`）：
1. `ce115_calc_radical_simplification_l1/ab2d_spec_v2/2026071301` — outcome=rescue_to_pass
2. `ce112_q04_radical_simplification/ab2g/2026072002` — outcome=**changed_partial_progress（仍FAIL）**
3. `ce115_calc_radical_simplification_l1/ab2d/2026072002` — outcome=rescue_to_pass
4. `ce113_q01_negative_fraction_subtraction/ab2d_spec_v2/2026072002` — outcome=rescue_to_pass
5. `ce113_q01_negative_fraction_subtraction/ab2g/2026072003` — outcome=rescue_to_pass
6. `ce112_q04_radical_simplification/ab2g/2026072004` — outcome=rescue_to_pass

（共6格，直接證據：`docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl`）

**Set B**（baseline非PASS、healed後通過完整G1–G4＝primary `rescued:true`）：
上列1、3、4、5、6（**5格**，排除#2，因其`post_healer_status="FAILED"`）。

**Set C**（正式標記為verified rescue＝`math16_posthoc_six_cell_rescue_audit_v1_manifest.json`之`six_posthoc_rescued_cells`）：
Set B的5格 **加上** `ce115_calc_radical_simplification_l1/ab2d/2026071301`（is_primary_rescued=**false**，primary_disposition=**NO_OP**；is_posthoc_rescued=true，透過`math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001`重新執行後才變為PASSED）。

**A ∩ B ∩ C = 5格**（非6格）：

| cell_id | 在A | 在B | 在C |
|---|---|---|---|
| ce115_radical/ab2d_spec_v2/2026071301 | ✓ | ✓ | ✓ |
| ce115_radical/ab2d/2026072002 | ✓ | ✓ | ✓ |
| ce113_q01/ab2d_spec_v2/2026072002 | ✓ | ✓ | ✓ |
| ce113_q01/ab2g/2026072003 | ✓ | ✓ | ✓ |
| ce112_q04_radical/ab2g/2026072004 | ✓ | ✓ | ✓ |
| ce112_q04_radical/ab2g/2026072002 | ✓ | ✗ | ✗ |
| ce115_radical/ab2d/2026071301 | ✗ | ✗ | ✓ |

**差集**：
- `A \ C = {ce112_q04_radical_simplification/ab2g/seed_2026072002}`：規則在primary run中確實matcher hit且guards全過（見第三節逐格表），transform確實套用，但healed後仍`schema_failure`（**MATCHER_HIT_GUARDS_PASS 但 non-rescue**——因為它同一份`generate()`還有其他與oracle_payload結構無關的獨立schema缺陷，wrap本身正確但不足以使整體通過G3）。**此格不得算入verified rescue，也不是「rule applied ⇒ verified rescue」的反例，而是regression=0之外的第三種結果：repaired_still_fail。**
- `C \ A = {ce115_calc_radical_simplification_l1/ab2d/seed_2026071301}`：在**primary執行環境**下，這個cell的healer因runner層級的`fallback_loop_detected_evaluator_loop_with_verdict_runtime_failure`而回退為`no_op`（`applied_rules: []`），**未被primary記為「規則實際套用」**；其verified rescue狀態完全來自**另一次獨立的posthoc corrected chain執行**（`math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001`），該次執行修正了runner的false-loop rollback bug後，才讓同一條規則的transform被保留並產生PASS。

**結論（依規格強制聲明）**：三集合**不一致**，正式回報 **SCOPE_MISMATCH**。後續不得將「rule applied」直接等同「verified rescue」——本報告後續逐格表對此7格（A∪C的並集）全部逐一列出並清楚標示其集合歸屬，其中深度審查聚焦於**Set C的6格**（因這是"六格verified rescue"標的本身），並對Set A獨有的第7格（`ce112_q04_radical/ab2g/2026072002`）在第三節末附記，以完整呈現SCOPE_MISMATCH全貌，但**不將其計入verified rescue統計**。

---

## 二、Set C 六格：因果鏈總覽

| # | cell_id | model | task | domain | condition | seed |
|---|---|---|---|---|---|---|
| 1 | qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301 | qwen3.5:4b | ce115_calc_radical_simplification_l1 | radicals | ab2d_spec_v2 (Ab2d+spec) | 2026071301 |
| 2 | qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002 | qwen3.5:4b | ce115_calc_radical_simplification_l1 | radicals | ab2d (Ab2d+api) | 2026072002 |
| 3 | qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002 | qwen3.5:4b | ce113_q01_negative_fraction_subtraction | rational_arithmetic (fraction) | ab2d_spec_v2 (Ab2d+spec) | 2026072002 |
| 4 | qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003 | qwen3.5:4b | ce113_q01_negative_fraction_subtraction | rational_arithmetic (fraction) | ab2g (Ab2g) | 2026072003 |
| 5 | qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004 | qwen3.5:4b | ce112_q04_radical_simplification | radicals | ab2g (Ab2g) | 2026072004 |
| 6 | qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301 | qwen3.5:4b | ce115_calc_radical_simplification_l1 | radicals | ab2d (Ab2d+api) | 2026071301 |

---

## 三、逐格完整因果鏈（每格獨立成表）

matcher/guard欄位名稱與順序全部直接取自 `agent_tools/finals_rebuild/ce115_research_healer_rules_l2.py::analyze_l2_payload_wrap()`：`single_frozen_key → parse_ok → return_has_oracle_payload → payload_static_scalar → scalar_equals_frozen_value → correct_answer_present → already_wrapped`，未杜撰任何欄位。

判定方式：對全部6格執行 **deterministic replay**（讀取原始 `raw_response.txt` → `extract_code()` → `_candidate_generate_source()` → `analyze_l2_payload_wrap()` → `apply()`，全部使用既有凍結函數，僅在記憶體比對，未寫回）。

### Cell 1 — ce115_calc_radical_simplification_l1 / Ab2d+spec / seed 2026071301

1. cell_id / model / task / domain / condition / seed：見上表#1。
2. 原始response path：`docs/experiments/results/math16_pilot02_qwen4b/cells/qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301/raw_response.txt`；原文片段（return語句）：`"oracle_payload": frozen_radicand`（`frozen_radicand = 27`，模組內先賦值後以Name參照）。
3. extracted candidate path：同cell目錄下無獨立`extracted_candidate.py`（此語料集不單獨存檔），實際執行candidate＝`extract_code(raw)`後再經`_candidate_generate_source()`去除前導散文所得之字串（本cell無前導散文，去markdown fence後即為完整模組）。
4. frozen baseline outcome：`schema_failure`（`docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl`）。
5. existing failure classification：`gates: g1_parse=PASS, g2_execution=PASS, g3_contract=FAIL(g3s_output_schema=FAIL), g4_correctness=NOT_ASSESSED`；`primary_failure_layer=L2`；`failure_subtype=OUTPUT_SCHEMA_MISMATCH`；`outcome_validity=VALID_MODEL_OUTCOME`。
6. audit-derived v3 L0–L5 classification：**不需要**——既有v4分類（L2/OUTPUT_SCHEMA_MISMATCH）已充分且與本輪matcher trace完全一致，本輪未補標新分類。
7. `analyze_l2_payload_wrap()`實際trace（deterministic replay輸出）：`applicable=True, triggered=True, reason="all_transform_guards_ready"`；guards＝`{single_frozen_key: True, parse_ok: True, return_has_oracle_payload: True, payload_static_scalar: True, scalar_equals_frozen_value: True, correct_answer_present: True, already_wrapped: False, frozen_key:'radicand', frozen_value:27, resolved_scalar:27, payload_value_kind:'Name'}`。
8. transform前後最小diff（replay產出，`apply_reason="wrapped_oracle_payload_scalar"`）：
   ```diff
   -        "oracle_payload": frozen_radicand
   +        "oracle_payload": {'radicand': 27}
   ```
9. 被保留不變：`correct_answer`（`{"coefficient": coeff, "radicand": simplified_radicand, "canonical_latex": correct_answer_str}`，AST fingerprint與逐字文字replay前後皆完全相同，`correct_answer_guard=True`）、`question_text`、全部其餘程式邏輯（`RadicalOps.simplify_term`呼叫、函式簽名）；運算結果（`coeff=3, simplified_radicand=3`）不受影響，healer未讀取或使用答案內容（`oracle_answer_used=False`，見規則docstring）。
10. healed candidate path：無獨立落地檔案（`artifact_storage: sha_only_not_committed_py`）；replay產生之`new_source`SHA256與官方紀錄之`after_snippet_hash`**完全一致**（見下）。
11. frozen healed outcome：`post_healer_scoring.jsonl` → `post_healer_final_status="PASSED"`，`gates`全部PASS（含`g4_correctness=PASS`），`healer_outcome="rescue_to_pass"`，`rescued=true`，`regressed=false`。
12. deterministic replay結果：computed before sha256 = `b2006e37...`＝官方`before_snippet_hash`（**MATCH**）；computed after sha256 = `a03ab5c3...`＝官方`after_snippet_hash`（**MATCH**）。
13. **verified rescue判定：CONFIRMED**（A∩B∩C成員；matcher/guard/transform/雜湊全部可重現且一致）。
14. direct evidence path：`docs/experiments/results/math16_pilot02_qwen4b/cells/qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301/{raw_response.txt,artifact.json}`；`docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl`；`docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/{eligible_execution_records.jsonl,post_healer_scoring.jsonl}`；`docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_manifest.json`。

### Cell 2 — ce115_calc_radical_simplification_l1 / Ab2d+api / seed 2026072002

1–6：task/domain/condition/seed見總表#2；raw path＝`.../qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002/raw_response.txt`；原文片段：`"oracle_payload": radicand_input`（`radicand_input = kwargs.get("radicand", 27)`）；baseline outcome=`schema_failure`；gates同Cell 1模式（g3s_output_schema=FAIL其餘PASS，g4 NOT_ASSESSED）；v3分類充分，未補標。
7. matcher trace：`applicable=True, triggered=True, reason="all_transform_guards_ready"`；guards同型態，`frozen_key='radicand', frozen_value=27, resolved_scalar=27, payload_value_kind='Name'`（此處`_resolve_scalar`沿`kwargs.get("radicand", 27)`分支解析：預設值27與frozen_value相等，成立）。
8. diff：
   ```diff
   -        "oracle_payload": radicand_input
   +        "oracle_payload": {'radicand': 27}
   ```
9. 保留：`correct_answer_dict`（含`coefficient/radicand/canonical_latex`，來自`RadicalOps.simplify_term`）、`try/except ImportError`備援邏輯、`question_text`；`correct_answer_guard=True`。
10. healed path：無獨立落地檔案（sha-only）。
11. healed outcome：`post_healer_final_status="PASSED"`，全gates PASS，`rescued=true`。
12. replay：before sha `d9af6acf...`＝官方**MATCH**；after sha `0ddd4fb7...`＝官方**MATCH**。
13. **verified rescue判定：CONFIRMED**。
14. evidence同Cell 1格式，路徑替換為本cell_id。

### Cell 3 — ce113_q01_negative_fraction_subtraction / Ab2d+spec / seed 2026072002

原文片段：`oracle_payload = frozen_expression`（`frozen_expression = "3/7 - (-1/4)"`）。baseline=`schema_failure`，gates同型態。
7. matcher：`applicable=True, triggered=True`；`frozen_key='expression', frozen_value='3/7 - (-1/4)', resolved_scalar='3/7 - (-1/4)', payload_value_kind='Name'`。
8. diff：
   ```diff
   -        "oracle_payload": oracle_payload
   +        "oracle_payload": {'expression': '3/7 - (-1/4)'}
   ```
9. 保留：`correct_answer_dict`（含手算之`numerator/denominator/canonical_latex`，一段冗長但內容不被讀取的推理註解全部保留）；`correct_answer_guard=True`。
10–11：healed outcome=`PASSED`，全gates PASS，`rescued=true`。
12. replay：before `61c5bbe6...`**MATCH**；after `5c009612...`**MATCH**。
13. **verified rescue判定：CONFIRMED**。
14. evidence同上格式。

### Cell 4 — ce113_q01_negative_fraction_subtraction / Ab2g / seed 2026072003

原文片段：`"oracle_payload": expression`（`expression = "3/7 - (-1/4)"`）。baseline=`schema_failure`。
7. matcher：`applicable=True, triggered=True`；`frozen_key='expression', resolved_scalar='3/7 - (-1/4)', payload_value_kind='Name'`。
8. diff：
   ```diff
   -        "oracle_payload": expression
   +        "oracle_payload": {'expression': '3/7 - (-1/4)'}
   ```
9. 保留：`correct_answer`（用`fractions.Fraction`精確計算，`numerator/denominator/canonical_latex`）；`correct_answer_guard=True`。
10–11：healed outcome=`PASSED`，全gates PASS，`rescued=true`。
12. replay：before `8699b3c1...`**MATCH**；after `f5d06416...`**MATCH**。
13. **verified rescue判定：CONFIRMED**。
14. evidence同上格式。

### Cell 5 — ce112_q04_radical_simplification / Ab2g / seed 2026072004

原文片段：`"oracle_payload": radicand`（`radicand = 135`，此task的frozen為`{"radicand":135}`，非ce115的27）。baseline=`schema_failure`。
7. matcher：`applicable=True, triggered=True`；`frozen_key='radicand', frozen_value=135, resolved_scalar=135, payload_value_kind='Name'`。
8. diff：
   ```diff
   -        "oracle_payload": radicand
   +        "oracle_payload": {'radicand': 135}
   ```
9. 保留：`correct_answer`（`coefficient=3, radicand=15, canonical_latex`）；`correct_answer_guard=True`。
10–11：healed outcome=`PASSED`，全gates PASS，`rescued=true`。
12. replay：before `c8e83cec...`**MATCH**；after `2e77e663...`**MATCH**。
13. **verified rescue判定：CONFIRMED**。
14. evidence同上格式。

### Cell 6 — ce115_calc_radical_simplification_l1 / Ab2d+api / seed 2026071301（**posthoc-only incremental，SCOPE_MISMATCH標的**）

原文片段：`"oracle_payload": radicand_input`（`radicand_input = kwargs.get("radicand", 27)`）——**與Cell 2結構高度相似**（同task、同條件家族Ab2d、同一`kwargs.get`模式），但seed不同（2026071301 vs 2026072002）。baseline=`schema_failure`（gates同型態）。
7. matcher trace（本輪replay直接對此cell的**before**原始碼執行）：`applicable=True, triggered=True, reason="all_transform_guards_ready"`；`frozen_key='radicand', frozen_value=27, resolved_scalar=27, payload_value_kind='Name'`——**規則本身在這格上完全能matcher hit且guards全過，與Cell 1–5同等级**。
8. diff（replay產出）：
   ```diff
   -        "oracle_payload": radicand_input
   +        "oracle_payload": {'radicand': 27}
   ```
9. 保留：`correct_answer_dict`；`correct_answer_guard=True`。
10. healed candidate path：無獨立落地檔案。**關鍵**：此cell在**primary執行**中，healer runner回報`stop_reasons: ["fallback_loop_detected_evaluator_loop_with_verdict_runtime_failure"]`，最終`healer_decision="no_op"`、`applied_rules=[]`——**即使matcher/guard本身觸發，runner仍因偵測到"假循環"而回退，未套用transform**。
11. frozen healed outcome（**primary**）：`post_healer_scoring.jsonl`→ `post_healer_final_status="FAILED"`，`gates.g3_contract=FAIL`，`healer_outcome="no_op"`，`rescued=false`。**此cell在primary healer產物中確定性地是FAIL，非verified rescue。**
    frozen healed outcome（**posthoc corrected chain**，`docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json`）：`new_post_healer_status="PASSED"`，`new_applied_rules=["L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP"]`，`noop_to_rescue=true`，`explanation="Math16 revalidation false-loop fix: false-loop rollback removed; L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP retained; formal PASS achieved in Post-hoc replay."`——**此PASS是runner bug修正後、獨立於primary的另一次執行結果**。
12. deterministic replay結果（本輪對該cell的**before**原始碼獨立執行）：before sha `c74c0315...`＝官方`before_snippet_hash`**MATCH**；after sha `ac6299da...`＝官方（posthoc）`after_snippet_hash`**MATCH**。**本輪replay證實：若不考慮runner的false-loop回退機制，規則本身的matcher/guard/transform在這格上與其餘5格完全同構、確定性一致**——換言之，這格的"verified rescue"地位完全成立於**規則本身**，唯一的特殊之處是**runner執行歷史**（primary因bug回退成no_op，posthoc修正bug後才實際套用並保留）。
13. **verified rescue判定：CONFIRMED，但需標註SCOPE_MISMATCH**——此格屬Set C（正式六格verified rescue名單）但不屬Set A（primary「規則實際套用」），其verified rescue證據鏈依賴**posthoc corrected chain**（一次獨立於primary healer run的重新執行）而非primary healer run本身。**不得將此格的primary healer記錄（no_op/FAILED）與其posthoc-corrected記錄（transformed/PASSED）混為一談引用。**
14. direct evidence path：`docs/experiments/results/math16_pilot02_qwen4b/cells/qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301/{raw_response.txt,artifact.json}`；primary：`docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/{eligible_execution_records.jsonl,post_healer_scoring.jsonl}`；posthoc：`docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json`；`docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_manifest.json`。

### 附記：Set A獨有第7格（不計入verified rescue，僅為完整揭露SCOPE_MISMATCH全貌）

`ce112_q04_radical_simplification/ab2g/seed_2026072002`：matcher applicable=True/triggered=True（同構觸發），transform確實套用（`applied_rules:["L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP"]`），但`post_healer_final_status="FAILED"`（`healer_outcome="changed_partial_progress"`，`repaired_still_fail=true`）。**此格未進入六格verified rescue清單，是`regression=0`統計之外「repaired但未rescue」的示例，本輪未展開其獨立逐格因果鏈（超出Set C範圍），僅在此記錄以完整呈現SCOPE_MISMATCH的差集**。Evidence: `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/{eligible_execution_records.jsonl,post_healer_scoring.jsonl}`。

---

## 四、分布分析

### 4.1 Set C六格分布（task／domain／condition／seed）

| task | domain | condition | seed | 計數 |
|---|---|---|---|---|
| ce115_calc_radical_simplification_l1 | radicals | ab2d_spec_v2 | 2026071301 | 1 |
| ce115_calc_radical_simplification_l1 | radicals | ab2d | 2026072002 | 1 |
| ce115_calc_radical_simplification_l1 | radicals | ab2d | 2026071301 | 1（posthoc-only，見Cell 6註記） |
| ce113_q01_negative_fraction_subtraction | rational_arithmetic | ab2d_spec_v2 | 2026072002 | 1 |
| ce113_q01_negative_fraction_subtraction | rational_arithmetic | ab2g | 2026072003 | 1 |
| ce112_q04_radical_simplification | radicals | ab2g | 2026072004 | 1 |

task分布：`ce115_calc_radical_simplification_l1`=3、`ce113_q01_negative_fraction_subtraction`=2、`ce112_q04_radical_simplification`=1。domain分布：radicals=4、rational_arithmetic(fraction)=2。

### 4.2 各condition分母與此規則之hit/transform/rescue數

| condition | 該condition總cell數（baseline） | 該condition baseline FAIL數 | 該condition中L2層(schema_failure)FAIL數 | 此規則matcher hit數（Set A內） | transform applied數（Set A內） | verified rescue數（Set C內，本condition） |
|---|---|---|---|---|---|---|
| ab1 | 80 | 65 | 6 | 0 | 0 | **0** |
| ab2g | 80 | 61 | 6 | 2 | 2 | 2 |
| ab2d (Ab2d+api) | 80 | 72 | 4 | 3（含Cell 6之posthoc-only） | 2（primary），+1（posthoc） | 3（含Cell 6） |
| ab2d_spec_v2 (Ab2d+spec) | 80 | 44 | 2 | 2 | 2 | 2 |

**確認：Set C六格全部非Ab1（0/6屬Ab1）**，但必須連同分母陳述：Ab1本身在baseline的L2層FAIL數也有6格（與ab2g、ab2d_spec_v2的L2 FAIL數相同量級），**Ab1的L2 FAIL cell並非不存在，而是這6格中沒有一格被本規則matcher hit**（本輪未逐一檢查Ab1那6格L2 FAIL的candidate原始碼是否符合本規則的bare-scalar pattern，此為未驗證項目，見4.4節）。

### 4.3 Ab2d_spec_v2內部分母細節（依4.2表）

`ab2d_spec_v2`該condition的L2層FAIL總數＝2，本規則的verified rescue數也是2——**即該condition全部L2 FAIL cell都被本規則命中並rescue**（分子=分母=2）。`ab2g`condition L2 FAIL總數=6，本規則rescue 2格（2/6，其餘4格屬其他失敗機制或未觸發此規則，本輪未逐一核對）。`ab2d`condition L2 FAIL總數=4，本規則涉及3格（2 primary + 1 posthoc-only，2/4為primary transform，另1/4即Cell6屬posthoc-only incremental）。

### 4.4 四種prompt之直接可觀察結構差異

比對對象：`ce115_calc_radical_simplification_l1`（radicand=27）在四個condition下的**實際prompt.txt**（直接讀取，未杜撰）：

| condition | schema描述（oracle_payload相關文字） | 輸出範例（含oracle_payload的具體skeleton） | API提示 | 格式限制 | wrapper/payload示例 |
|---|---|---|---|---|---|
| **Ab1** | 有（"oracle_payload must exactly equal the frozen sampled parameters"，僅此一句） | **無** | 無 | 有（"Exact integers only; no floats"） | **無** |
| **Ab2g** | 同Ab1一句，另加GENERIC reinforcement："Verify... that oracle_payload equals the frozen parameters" | **無** | 無 | 同上 | **無** |
| **Ab2d** | 同Ab1一句 + 同Ab2g的GENERIC reinforcement | **無**（僅有API signature表：`RadicalOps.simplify_term(coeff, radicand)` → `tuple[...]`） | **有**（DOMAIN API簽章區塊） | 同上 | **無** |
| **Ab2d+spec (ab2d_spec_v2)** | 同上兩句 + "Compact Domain Scaffold"骨架 | **有**——骨架明確示範：`oracle_payload = "oracle_payload"` 後於`return {...,"oracle_payload": oracle_payload,}`中以**變數Name參照**回傳 | 有（骨架含`# from core.prompts.domain_function_library import RadicalOps`註解提示） | 同上＋"Task Guardrails"／"Final Check"逐項checklist | **有**——骨架本身即示範"先賦值純量占位字串、再以Name回傳"這一結構形態 |

**觀察**（僅描述，非因果宣稱）：唯一在文本上明確示範「`oracle_payload`先賦值為一個純量佔位符、再於return字典中以純Name參照回傳」這一具體結構的條件是`Ab2d+spec`；其餘三個condition的prompt皆不含任何oracle_payload的skeleton範例。

**與分布交叉檢驗**：若「骨架示範裸純量+Name參照」是此缺陷的窄化development hypothesis，則預期本規則命中應集中於`Ab2d+spec`。但4.2表顯示：`ab2g`（無骨架、僅有文字checklist）與`ab2d`（無骨架、僅有API簽章）合計貢獻4/6格（含posthoc-only的Cell 6），與`ab2d_spec_v2`（有骨架）貢獻2/6格相當甚至更多。且`ab2g`與`ab2d`彼此的prompt具體追加內容（純文字checklist vs. API簽章表）並不相同，卻都出現同一種"先賦值純量、後Name參照"的candidate結構。**Prompt文本內容與分布並未在同一具體元素上收斂一致**——唯一跨三個非Ab1 condition共通、且與Ab1（0格）形成對比的特徵，只是「prompt在base contract之外是否存在任何額外scaffold/reinforcement文字」這一極寬泛的二元差異，不足以窄化到某個具體prompt元素（如wrapper示例）的因果宣稱。

**結論：`NO_SUPPORTED_SCAFFOLD_HYPOTHESIS`。** 不宣稱因果；僅記錄上述可直接觀察的文本差異與其與分布不完全收斂的事實。

---

## 五、Guard安全性稽核

| Guard（依matcher內實際順序） | 程式判定條件（逐字取自原始碼） | 排除的風險 | 對應正式測試 | do-not-repair案例 | TEST_COVERAGE_GAP |
|---|---|---|---|---|---|
| `parse_ok` | `ast.parse(source)`成功 | 對不可parse的原始碼誤套transform | **無**專屬fixture／parametrize case直接餵入不可parse原始碼給`analyze_l2_payload_wrap()`測試其`reason=parse_error:...`分支（runner層級由phase gating保證L2只在source已可parse時才被評估，但該保證是runner的職責，非規則本身有獨立單元測試） | 無正式測試佐證 | **是**——標記TEST_COVERAGE_GAP |
| `single_frozen_key` | `len(frozen.keys()) == 1` | 對多鍵frozen context誤解析出「哪個鍵」而錯誤包裝 | `test_case_guard_semantics[noop_multikey_frozen]`（`tests/finals_rebuild/fixtures/ce115_research_healer/cases/noop_multikey_frozen`） | `noop_multikey_frozen`：applicable=True, triggered=False | 否 |
| `return_has_oracle_payload` | `_dict_entry(ret, "oracle_payload")`非None | 對缺少`oracle_payload`鍵的return dict誤判為applicable | **無**專屬fixture測試「return dict完全沒有oracle_payload鍵」場景 | 無正式測試佐證 | **是**——標記TEST_COVERAGE_GAP |
| `payload_static_scalar` | `_resolve_scalar()`能靜態解析出純量（Constant／Name鏈／`kwargs.get(key[,default])`／`kwargs[key]`四種形態之一） | 對無法靜態確定的動態表達式（如函式呼叫結果、複雜運算式）誤套transform，避免破壞不可預測的邏輯 | 間接由`test_pass_cells_not_harmed_still_evaluate_passed`（`pass_radical_ab2d`/`pass_polydiv_ab2d`）與`test_case_guard_semantics`覆蓋，但無專屬case明確斷言「payload是不可解析的動態表達式」這一具體guard分支 | `pass_radical_ab2d`／`pass_polydiv_ab2d`：applicable=True, triggered=False（未逐一斷言是此guard還是`already_wrapped`guard導致no_op） | **是**——guard分支本身覆蓋不完整，標記TEST_COVERAGE_GAP |
| `scalar_equals_frozen_value` | `resolved == frozen_value` | 對純量值與frozen值不符的candidate（代表模型算錯或用了錯誤的frozen值）誤套transform，避免把錯誤答案「包裝成看似正確」 | `test_case_guard_semantics[noop_value_mismatch]`（`cases/noop_value_mismatch`） | `noop_value_mismatch`：applicable=True, triggered=False | 否 |
| `correct_answer_present` | `_dict_entry(ret, "correct_answer")`非None | 對缺少`correct_answer`鍵的return dict誤套transform（此guard確保"oracle_answer_used=false"聲明不因為answer缺失而被繞過驗證） | **無**專屬fixture測試「return dict缺少correct_answer鍵」場景 | 無正式測試佐證 | **是**——標記TEST_COVERAGE_GAP |
| `already_wrapped` | `payload_value`本身即為`ast.Dict`且恰為`{frozen_key: scalar}`單鍵字面值 | 對已經正確包裝的candidate重複套用transform（idempotency防護） | `test_idempotent_second_pass_noop`（對`fail_radical_ab1_l2`跑兩次，第二次確認`triggered`鏈中無changed rule） | 間接覆蓋（透過idempotency測試），無獨立fixture直接構造「一開始就是`{radicand:27}`」的candidate並斷言`already_wrapped=True` | **是**——特定guard旗標值本身未被獨立斷言，標記TEST_COVERAGE_GAP |
| （`apply()`內部）`correct_answer_guard`（transform後`correct_answer`的AST dump與原始碼片段皆須與transform前相同） | `before_ca == after_ca and before_ca[0] is not None` | 對transform意外改動答案內容（`oracle_answer_used`必須為false的核心保障） | `test_correct_answer_and_non_payload_ast_unchanged`（明確逐項斷言AST dump相同、片段相同） | 若guard失敗，`apply()`回傳原始source並標記`correct_answer_changed_or_missing_abort`（未見獨立測試主動觸發此abort分支並斷言其行為） | **是**（局部）——正常路徑（guard通過）已充分測試，但**abort路徑本身**（guard主動失敗時的回退行為）無專屬fixture觸發，標記TEST_COVERAGE_GAP |

**概念性風險示例（與正式測試證據分欄，不得視為已測試）**：
- 若`generate()`內對`oracle_payload`的賦值被包在`ast.If`分支內（例如`if condition: oracle_payload = {...} else: oracle_payload = other`），`_return_dict()`明確以註解"ignore complex control flow for H3"略過`ast.If`節點——概念上這代表此規則對條件式return採取保守策略（傾向`return_dict_missing` → not applicable，即fail-closed而非fail-open），但**此行為本身未見正式回歸測試直接構造此類candidate並斷言其為NO_MATCH**。這是一個概念性推論，非已驗證事實。
- 若`oracle_payload`的Name鏈跨越超過1層間接賦值（例如`a=27; b=a; oracle_payload=b`），`_resolve_scalar()`具備遞迴解析能力（`_seen`集合防止循環），概念上應能正確解析，但本輪6格實際candidate皆為單層賦值鏈，**多層鏈的解析能力未在本次6格中被實際驗證，也未見對應正式測試**。

**本規則所主張的semantic invariant**（取自規則docstring與`apply()`內`validation`欄位／測試斷言）：
> Transform只允許改動`oracle_payload`欄位的值表達式（從裸純量/Name參照改為`{frozen_key: scalar}`字面值），**`correct_answer`欄位的AST結構與原始文字片段必須逐字不變**（`correct_answer_guard`），且**規則實作不讀取`correct_answer`的實際內容做任何判斷**（`oracle_answer_used=false`）。

**逐格核對（transform前後是否保持此invariant）**：Set C全部6格，本輪deterministic replay皆確認`correct_answer_guard=True`且diff僅涉及`oracle_payload`那一行（見第三節each cell之diff區塊）。**invariant在全部6格上均成立，CONFIRMED**（verified 6/6，direct evidence：本輪replay腳本輸出，逐格diff僅一行變更）。

---

## 六、Regression 及全量作用範圍

從正式凍結證據（`docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/overall_summary.json`）：

| 項目 | 數值 |
|---|---|
| 完整評估母體 | 320 |
| baseline PASS | 78 |
| baseline FAIL | 242 |
| matcher hit數（fail_eligible，六規則合計） | 10 |
| guard pass數／transform applied（repaired，六規則合計） | 8 |
| **本規則**matcher hit＋transform applied數（primary，即Set A） | 6 |
| verified rescue數（rescued，六規則合計，primary） | 5 |
| **本規則**verified rescue數（primary Set B） | 5（全部5個primary rescue皆用此規則） |
| baseline PASS被修改數 | 0（`preserved_pass=78`＝`baseline_pass=78`） |
| PASS→非PASS數（regression） | **0** |
| 其他退化數 | 0 |
| repaired_still_fail（transform套用但未rescue） | 3（六規則合計，含本規則1格：`ce112_q04_radical/ab2g/2026072002`） |
| no_op（matcher hit但未transform，或runner回退） | 2（六規則合計，含本規則1格：`ce115_radical/ab2d/2026071301`即primary態） |
| unchanged（baseline FAIL但non-eligible，未進入healer） | 232（`fail_noneligible`） |
| abstain | 232（`abstained`，與unchanged同一群） |

**`regression=0`之證據性質判定**：查`eligible_execution_records.jsonl`僅含**10筆**紀錄，且逐筆核對其`cell_id`後確認**無一筆**對應baseline PASS的78格中的任何一格——healer runner的架構設計即為「僅對`fail_eligible`（baseline FAIL且matcher hit）的cell觸發規則評估」（`healer_ran: 10`＝`fail_eligible: 10`，兩者恆等），baseline PASS的78格從未進入healer流程、從未被任何規則的matcher/guard/apply觸碰。

**結論：`regression=0`是由「pipeline架構本身僅對baseline failure啟動規則」所結構性保證**（CONFIRMED，非UNVERIFIED——證據：`eligible_execution_records.jsonl`筆數與cell_id集合、`overall_summary.json`之`healer_ran=10=fail_eligible`恆等關係），**而非**透過對全部320格（含78格baseline PASS）逐一做獨立before/after G1–G4全量重放驗證所得。若需要「78格baseline PASS在healer執行後仍維持原candidate位元不變」這一更強的逐格複驗，本輪**未**對全部78格逐一重放比對（僅信任`preserved_pass=78`此一彙總欄位與架構设计保證），此為未驗證項目，狀態應標記為**部分UNVERIFIED**（架構保證層面CONFIRMED，逐格78格獨立複驗層面UNVERIFIED_REGRESSION_CHECK，不得假設後者已完成）。

---

## 七、結論限制（重申）

本報告全部結論僅限於：Qwen3.5:4B math16_pilot02正式cohort、`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`規則於commit`d9aa264c`凍結後的版本、本文Set C定義之6格verified rescue（含其SCOPE_MISMATCH說明）、本輪可重現之matcher/guard/transform證據（6/6 byte-exact雜湊重現）。**不得**外推至跨模型（含Qwen2.5-Coder 7B，本輪未納入對照）、跨task（僅radical/fraction兩domain、三個task_id）、或一般APR（自動程式修復）技術之通用有效性宣稱。

---

## 八、Git與交付

**起始**：
- branch: `main`
- HEAD: `8cf0e8535c7742880d7ed32e01cb030dcd45b2ee`
- origin/main: `8cf0e8535c7742880d7ed32e01cb030dcd45b2ee`（同步）
- git status --short：2個既存modified正式檔案（`04_math16_pilot02_jury_qa_final_v1.md`、`05_math16_pilot02_appendices_v1.md`）+ 前幾輪session累積之untracked manifests/reports/results/scripts（詳見下方完整清單）

**結束**：
- branch: `main`（未變動）
- HEAD: `8cf0e8535c7742880d7ed32e01cb030dcd45b2ee`（未變動）
- origin/main: `8cf0e8535c7742880d7ed32e01cb030dcd45b2ee`（未變動，同步）
- git status --short：與起始**完全相同**，僅新增本報告一個untracked檔案：`docs/experiments/reports/math16_posthoc_six_cell_l2_payload_wrap_deep_audit_v1.md`
- 2個既存modified正式檔案內容與狀態**未變動**（全程未讀取以外的任何操作，未stage、未commit、未push、未stash、未restore）
- 唯一新增之repo內檔案：本報告本身
- Session暫存（非repo檔案，不影響git狀態）：`.../scratchpad/run_l2_matcher_diagnostic.py`（前一任務遺留）、`.../scratchpad/replay_six_cell_l2_wrap.py`、`.../scratchpad/replay_six_cell_l2_wrap_v2.py`（本輪deterministic replay腳本，僅呼叫既有凍結函數做記憶體比對，未寫入repo任何檔案）
