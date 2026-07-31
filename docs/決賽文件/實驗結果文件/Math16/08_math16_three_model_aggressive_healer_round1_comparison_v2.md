# Math16 Historical Round 1：三模型 Healer 完整機制與逐格診斷 v2

> **文件定位：** 對齊 HumanEval+／MBPP+ H1–H4 報告深度的 Math16 技術版結果報告
> **證據封存：** `main@e44213d2d07d585b96ecb61b416223f7ed83be6a`
> **正式口徑：** Baseline `469/960` → Final `478/960`；verified rescue `9`（4B／9B／Gemini＝`8／1／0`）
> **限制：** 本文件只整理既有 ledger、journal、evaluator 輸出與規則原始碼；未執行模型、Healer、candidate、replay 或 evaluator。

---

## 1. 實驗身分與正式結果

Math16 Historical Round 1 比較三個模型、四種 Prompt 條件與八個累積狀態。每個模型均有 320 cells，總母體為 960 cells。

| 模型 | Baseline PASS | Final PASS | verified rescue | Baseline FAIL | 修復率 |
|---|---:|---:|---:|---:|---:|
| Qwen 3.5 4B | 79 | 87 | 8 | 241 | 3.32% |
| Qwen 3.5 9B | 101 | 102 | 1 | 219 | 0.46% |
| Gemini 3.5 Flash | 289 | 289 | 0 | 31 | 0.00% |
| **合計** | **469** | **478** | **9** | **491** | **1.83%** |

正式結果只使用 corrected formal account；歷史更正過程留在 Correction Note 與 provenance audit，不放入本報告主敘事。

**資料來源：** `docs/experiments/results/math16_three_model_historical_round1_unified_cell_ledger_v1/unified_cell_ledger.jsonl`；`docs/experiments/results/math16_historical_round1_final_overlay_audit_v1/validation_summary.json`。

---

## 2. C0–C5c 與 Healer 層級對應

| 狀態轉移 | 實際層級 | 角色 |
|---|---|---|
| C0→C1 | Tier A | 六條 frozen conservative rules |
| C1→C2 | Tier B | 四條 safe structural extension rules |
| C2→C3 | Tier C1 | explicit domain-method binding candidate |
| C3→C4 | Tier C2 | domain signature form cleanup |
| C4→C5a | Tier D3→D1 | syntax residue quarantine，再做 Ops shadow removal |
| C5a→C5b | Tier D5 | ranked domain-method binding |
| C5b→C5c | Tier D2 | duplicate-definition selection |

後文的「modified」一律指相鄰狀態的 `source_sha256` 改變；「rescue」一律指正式配對的 `FAIL→PASS`。

**資料來源：** `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md`；`docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json`；`unified_cell_ledger.jsonl`。

---

## 3. 各層 Healer 的實際機制

### 3.1 Tier A：凍結的保守語法與輸出包裝修復

Tier A 處理的是「可由唯一局部結構判定、且不需要猜測演算法的語法或輸出包裝錯誤」。六條規則依序涵蓋未閉合括號、延伸 delimiter、窄範圍 prose residue、`oracle_payload` 單鍵包裝、空 kwargs bag 與 `correct_answer` 的 `json.dumps` 包裝。

觸發條件：

1. cell 進入既定 eligibility，且只能命中 frozen allowlist 中可唯一決定的規則。
2. 變換不得讀取正確答案內容；結構規則只讀 AST、欄位形狀或局部 token。
3. 修改後必須通過規則自己的保護條件；無法唯一判定時 abstain。

實際案例：Qwen 4B／`ce115_calc_radical_simplification_l1`／Ab2d+api／seed `2026071301`，規則 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`。

```python
# 修改前
"oracle_payload": radicand_input

# 修改後
"oracle_payload": {"radicand": 27}
```

演算法是否被更動：**否**。只改輸出 payload 的契約形狀。
本層修改格數：**11**；rescue：**6**。
其餘 5 格沒有 rescue，因為第一個 blocker 被移除後仍有其他問題：1 格仍不可解析、2 格停在 runtime exception、1 格停在 schema mismatch、1 格前進到 correctness／structural mismatch。

**資料來源：** `agent_tools/finals_rebuild/ce115_research_healer_rules_*.py`；`docs/experiments/results/math16_method2_all_cell_replay_v1/phase_b_source_changed_11_results.jsonl`；`docs/experiments/results/math16_c0_c1_tier_a_reproducibility_v1/transition_journal.jsonl`；上述 cell 的 C0/C1 source files。

### 3.2 Tier B：安全結構補洞，使程式先恢復可解析

Tier B 處理的是「全形 Python 標點、唯一缺失 delimiter、空 suite、唯一 import binding」等安全結構問題。Round 1 真正修改的 8 格全部由 `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` 觸發；其他三條規則本輪 modified=0。

觸發條件：

1. 只接受前一層仍 FAIL 的 cell。
2. 必須找到唯一空 suite；插入位置由 suite header 唯一決定。
3. 只插入一行 `pass`；不得改條件、運算式、回傳值或答案。
4. 修改後需可解析、可重跑且具 rollback／idempotence guard。

實際案例：Qwen 9B／`ce115_calc_polynomial_factor_roots_l1`／Ab1／seed `2026072004`。

```python
# 修改前
if discriminant % 4 != 0:
    # 只有註解，沒有可執行 statement

# 修改後
if discriminant % 4 != 0:
    pass
    # 原註解保留
```

演算法是否被更動：**否**。`pass` 只補足 Python suite，不新增數學運算。
本層修改格數：**8**；rescue：**1**。
其餘 7 格中，4B 的 4 格與 9B 的 3 格雖取得 parse gain，但多數仍停在 runtime failure 或 missing entry point；只有 2/8 取得 execution gain。

**資料來源：** `agent_tools/finals_rebuild/aggressive_healer_tier_a/rule_a1_fullwidth.py`、`rule_a2_delimiter.py`、`rule_a3_empty_suite.py`、`rule_a4_import_binding.py`；4B `math16_c1_c2_tier_b_development_replay_v1/cell_results.jsonl`；9B `math16_c1_c2_tier_b_reproducibility_qwen9b_fail_gated_authoritative_v1/transition_journal.jsonl`。

### 3.3 Tier C1：明確且唯一的 domain method 名稱修復

Tier C1 處理的是「Prompt／SSOT 已明示唯一 domain method，但 source 呼叫了另一個 method 名稱」的窄型契約錯誤。

觸發條件：cell 必須是 Ab2d 類條件、source 可解析、只有一個錯誤呼叫點、SSOT 能給出唯一 expected method，且不存在 Ops shadow、multiple wrong sites 或 system-contract defect。Round 1 只有 Qwen 9B 1 格 modified，仍為 FAIL，rescue=0；因此改正 method 名稱仍不足以修復該格的其他失敗。

治理但書：mapping manifest 把此規則標成 `spec_only_not_implemented`，但 9B Round 1 runner 內確實保存同名 `RULE_ID`、eligibility 與 transform，並產生 1 格 source change。故本報告把它列為「**runner-inline development candidate**」，SHA 釘在實際 runner，不捏造不存在的獨立 rule module。

**資料來源：** `scripts/run_math16_c2_c3_tier_c1_qwen9b_v1.py`；`docs/experiments/results/math16_c2_c3_tier_c1_reproducibility_qwen9b_fail_gated_authoritative_v1/transition_journal.jsonl`；`math16_healer_rule_id_tier_mapping_v1.json`。

### 3.4 Tier C2：只清理 domain signature 的 optional pure form

Tier C2 處理的是 `default_optional_pure_form_cleanup`：當 domain API 的 optional argument 以不必要但可安全移除的形式出現時，只清理呼叫形狀，不改 argument value 與主要演算法。

觸發條件：source 可解析、SSOT signature 可解析、只有一個允許的 call site、待移除參數具有已知 default，且變換前後參數語意等價。Round 1 modified=11（4B 5、9B 6），rescue=0；4B 的 4 格仍為 answer incorrect、1 格仍為 runtime failure，顯示 signature 形式不是主要答案錯誤來源。

**資料來源：** `agent_tools/finals_rebuild/aggressive_healer_tier_c2/rule_default_optional_cleanup.py`；4B `math16_c2_c4_tier_c2_development_replay_v1/cell_results.jsonl`；9B `math16_c3_c4_tier_c2_reproducibility_qwen9b_fail_gated_authoritative_v1/transition_journal.jsonl`。

#### C2 的 9B 六格完整去向

| journal row | Cell identity | 實際形式清理 | 最終狀態／卡點分類 |
|---:|---|---|---|
| 19 | `qwen3_5_9b__ce111_q02_polynomial_division_remainder__ab2d_spec_v2__seed_2026071301` | `PolynomialOps.format_latex` 的 `var="x"` default optional pure form | `FAILED→FAILED`；**證據不足**：journal 保存 `still_failed`，未保存 post-failure subtype |
| 54 | `qwen3_5_9b__ce112_q12_independent_probability_fraction__ab2d__seed_2026071301` | `FractionOps.to_latex` 的 `mixed=false` default optional pure form | `FAILED→FAILED`；**證據不足**：未保存 post subtype |
| 147 | `qwen3_5_9b__ce111_q02_polynomial_division_remainder__ab2d_spec_v2__seed_2026072002` | `PolynomialOps.format_latex`／`var="x"` | `FAILED→FAILED`；**證據不足**：未保存 post subtype |
| 182 | `qwen3_5_9b__ce112_q12_independent_probability_fraction__ab2d__seed_2026072002` | `FractionOps.to_latex`／`mixed=false` | `FAILED→FAILED`；**證據不足**：未保存 post subtype |
| 186 | `qwen3_5_9b__ce113_q01_negative_fraction_subtraction__ab2d__seed_2026072002` | `FractionOps.to_latex`／`mixed=false` | `FAILED→FAILED`；**證據不足**：未保存 post subtype |
| 275 | `qwen3_5_9b__ce111_q02_polynomial_division_remainder__ab2d_spec_v2__seed_2026072004` | `PolynomialOps.format_latex`／`var="x"` | `FAILED→FAILED`；**證據不足**：未保存 post subtype |

六格皆有 `modified=true`、`rule_triggered_ids=[TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1]`、`pre_status=post_status=FAILED`，且 `parse_gain=false`、`execution_gain=false`；因此不可把 4B 的 answer/runtime 類別外推給這六格。穩定鍵為上述 journal row（0-based）＋`cell_id`。

### 3.5 Tier D3：隔離 generate 後方唯一 trailing residue

Tier D3 處理的是「唯一 `generate()` 已結束，但其後殘留一段可界定的非定義 statement」。它以 comment-out quarantine 隔離該連續區段。

觸發條件：唯一 `generate`、唯一 trailing residue span、依賴關係允許隔離；若 residue 仍被 `generate` 依賴或範圍不唯一則 abstain。Round 1 D3 modified=4、rescue=0。兩格取得 execution gain，但分別停在 structural mismatch 與 answer incorrect；移除尾端殘留並不會重建數學演算法。

**資料來源：** `agent_tools/finals_rebuild/aggressive_healer_tier_d/rule_d3_syntax_residue_quarantine.py`；`docs/experiments/results/math16_c4_c5_tier_d_d3_d1_development_replay_v1/cell_results.jsonl`；9B authoritative D3/D1 journal。

#### D3 四格完整去向

| `cell_results.jsonl` row | Cell identity | D3 後最終狀態／卡點 | modified-still-failed |
|---:|---|---|---|
| 0 | `qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d__seed_2026072002` | `FAILED`／`runtime_failure`；同格後續亦執行 D1 | 是 |
| 1 | `qwen3_5_4b__ce111_q02_polynomial_division_remainder__ab2d__seed_2026072004` | `FAILED`／`runtime_failure` | 是 |
| 3 | `qwen3_5_4b__ce111_q10_ordered_quadratic_roots_radical__ab2d__seed_2026072002` | `FAILED`／`structural_mismatch`；`executable_gain=true` | 是 |
| 4 | `qwen3_5_4b__ce111_q10_ordered_quadratic_roots_radical__ab2d__seed_2026072003` | `FAILED`／`answer_incorrect`；`executable_gain=true` | 是 |

四格均由 `per_rule.TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1.modified=true` 證實；row 0/1 是原文未交代的兩格，並非 execution gain。

### 3.6 Tier D1（active-shadow）：讓呼叫重新綁定正式 runtime Ops

Tier D1 處理的是「模型自訂的 `IntegerOps`／`FractionOps`／`RadicalOps`／`PolynomialOps` 遮蔽 runtime 注入的正式同名 Ops」。這不是清除死代碼，而是把 active binding 換回 frozen runtime API。

觸發條件：

1. source 中存在唯一 Ops shadow 定義或 binding。
2. scaffold 確定會注入同名正式 Ops。
3. 移除 shadow 後現有呼叫會解析到 runtime API。
4. 多個 shadow、名稱不唯一或移除後不可解析時 abstain。

實際案例：Qwen 4B／`ce112_q04_radical_simplification`／Ab2d+api／seed `2026071301`。

```python
# 修改前：模型自訂 active shadow
class RadicalOps:
    @staticmethod
    def simplify_term(...):
        ...

def generate(...):
    simplified_coeff, final_radicand = RadicalOps.simplify_term(...)

# 修改後：移除整個自訂 RadicalOps；generate 的呼叫保留
def generate(...):
    simplified_coeff, final_radicand = RadicalOps.simplify_term(...)
    # 此名稱改由 frozen scaffold 注入的 RadicalOps 綁定
```

演算法是否被更動：**是（implementation binding 改變）**，但沒有由 Healer 新寫演算法；它改用既有 frozen runtime implementation。
D1 modified=**16**（4B 4、9B 12），rescue=**2**；兩格 rescue 均為 4B radical task。多數未 rescue 的原因是 shadow 不是唯一 blocker：4B 有 1 格移除 shadow 後仍 answer incorrect；9B 的 12 格全數仍 FAIL，其中 3 格取得 execution gain，但 journal 沒有保存可供本報告逐格引用的完整 post-failure subtype。

**資料來源：** `agent_tools/finals_rebuild/aggressive_healer_tier_d/rule_d1_ops_shadow_removal.py`；4B `math16_c4_c5_tier_d_d3_d1_development_replay_v1/cell_results.jsonl`；9B `math16_c4_c5a_tier_d_d3_d1_reproducibility_qwen9b_fail_gated_authoritative_v1/transition_journal.jsonl`；上述 cell 的 pre/post sources。

### 3.7 Tier D5：凍結排名下的 domain method binding

Tier D5 只在唯一 wrong Ops attribute 存在時，依 frozen contract/ranking 選定 method 名稱；所有 argument 原樣保留，tie 或 margin 不足即 abstain。Round 1 modified=1、rescue=0；該格修改前後皆可解析、可執行，但仍 answer incorrect，表示 method 名稱並非唯一語意錯誤。

**資料來源：** `agent_tools/finals_rebuild/aggressive_healer_tier_d/rule_d5_ranked_domain_method_binding.py`；`docs/experiments/results/math16_c5a_tier_d_d5_development_replay_v1/cell_results.jsonl`。

### 3.8 Tier D2：兩個同名定義中的唯一勝者選擇

Tier D2 在同一 scope 出現兩個同名 definition 時，依 frozen features、minimum score 與 margin 選唯一勝者；不合併 body，也不使用 evaluator 選候選。Round 1 modified=1、rescue=0；該格由 missing entry point 前進為可執行，但最後仍 answer incorrect。

**資料來源：** `agent_tools/finals_rebuild/aggressive_healer_tier_d/rule_d2_duplicate_definition_selection.py`；`docs/experiments/results/math16_c5a_tier_d_d2_development_replay_v1/cell_results.jsonl`。

---

## 4. Transform class × 模型 × Prompt

本表以相鄰 stage 的 source SHA 是否改變建立「source-change transform class」。它能回答哪個 Prompt 最常被實際改寫。4B unified ledger 的 triggered／abstained event coverage 並不完整，因此本表**不把未修改的 trigger/abstain 猜成 transform**。

| Source-change class | 4B・Ab1 | 4B・Ab2g | 4B・Ab2d+api | 4B・Ab2d+spec | 9B・Ab1 | 9B・Ab2g | 9B・Ab2d+api | 9B・Ab2d+spec | Gemini・Ab1 | Gemini・Ab2g | Gemini・Ab2d+api | Gemini・Ab2d+spec |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tier A only | 1 | 3 | 4 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Tier B only | 0 | 2 | 2 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| Tier C2 only | 0 | 0 | 1 | 4 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 |
| D3+D1 only | 0 | 0 | 7 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 |
| Tier C1 + D3+D1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| Tier B + D3+D1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| Tier C2 + D3+D1 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| D5 only | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| D2 only | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 未修改 | 79 | 75 | 64 | 73 | 79 | 78 | 68 | 77 | 80 | 80 | 80 | 80 |
| **欄合計** | **80** | **80** | **80** | **80** | **80** | **80** | **80** | **80** | **80** | **80** | **80** | **80** |

實際 source change 高度集中於 Ab2d+api：4B 有 16/80 格、9B 有 12/80 格被修改；Gemini 四條件均為 0/80。這支持「Healer 活躍度取決於 residual failure 與契約型 Prompt 的互動」，不能單獨歸因於模型大小。

**資料來源：** `unified_cell_ledger.jsonl` 的 C0–C5c `source_sha256`；stage mapping 見第 2 節。

---

## 5. 九格 verified rescue 的證據等級

| 證據口徑 | 不可解析→PASS | 結構／執行 blocker→PASS | 可執行但答案錯→PASS | 證據不足 |
|---|---:|---:|---:|---:|
| Evaluator-only（raw/final classifier 欄位直接保存） | 0 | 6 | 0 | 0 |
| Pipeline-assisted（journal／runner 結果保存） | 1 | 2 | 0 | 0 |

分類依據：

- Tier A 6 格：`phase_b_source_changed_11_results.jsonl` 直接保存 `raw_classifier_outcome=schema_failure`、`raw_status=FAILED`、`final_classifier_outcome=passed`、`final_status=PASSED`。
- Tier B 1 格及 D1 2 格：現存檔案是 pipeline／runner journal；雖保存前後狀態或 classifier outcome，但不是獨立 evaluator 原始產物，故只能列 Pipeline-assisted。

#### 九格逐格 evidence-level 重核

| Cell identity | model／task／seed／condition | rescue stage/rule | 保存的 pre → post 欄位和值 | 證據等級與檔案／穩定鍵 |
|---|---|---|---|---|
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` | 4B／`ce115_calc_radical_simplification_l1`／2026071301／ab2d | Tier A／`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | `raw_classifier_outcome=schema_failure`, `raw_status=FAILED` → `final_classifier_outcome=passed`, `final_status=PASSED` | **Evaluator-only**；`math16_method2_all_cell_replay_v1/phase_b_source_changed_11_results.jsonl` row 0 |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301` | 4B／同 task／2026071301／ab2d_spec_v2 | Tier A／同 rule | 同上 | **Evaluator-only**；同檔 row 1 |
| `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002` | 4B／同 task／2026072002／ab2d | Tier A／同 rule | 同上 | **Evaluator-only**；同檔 row 5 |
| `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002` | 4B／`ce113_q01_negative_fraction_subtraction`／2026072002／ab2d_spec_v2 | Tier A／同 rule | 同上 | **Evaluator-only**；同檔 row 6 |
| `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003` | 4B／同 task／2026072003／ab2g | Tier A／同 rule | 同上 | **Evaluator-only**；同檔 row 8 |
| `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004` | 4B／`ce112_q04_radical_simplification`／2026072004／ab2g | Tier A／同 rule | 同上 | **Evaluator-only**；同檔 row 9 |
| `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026072004` | 9B／`ce115_calc_polynomial_factor_roots_l1`／2026072004／ab1 | Tier B／`TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | journal `pre_status=FAILED` → `post_status=PASSED`; classifier `parse_minor→passed` 只在非-authoritative replay 保存 | **Pipeline-assisted**；`math16_c1_c2_tier_b_reproducibility_qwen9b_fail_gated_authoritative_v1/transition_journal.jsonl` row 284；pre-failure subtype 無 evaluator-direct 證據 |
| `qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026071301` | 4B／`ce112_q04_radical_simplification`／2026071301／ab2d | D1／`TIER_D_OPS_SHADOW_REMOVAL_V1` | `pre_classifier_outcome=runtime_failure`, `pre_pass_fail=FAILED` → `post_classifier_outcome=passed`, `post_pass_fail=PASSED` | **Pipeline-assisted**；`math16_c4_c5_tier_d_d3_d1_development_replay_v1/cell_results.jsonl` row 5 |
| `qwen3_5_4b__ce112_q04_radical_simplification__ab2d__seed_2026072002` | 4B／同 task／2026072002／ab2d | D1／同 rule | 同上 | **Pipeline-assisted**；同檔 row 6 |

因此不得維持「9/9 evaluator-direct」主張：現存可直接作 raw/final classifier 配對的為 6/9；另 3/9 的 PASS 與 transform 可由 pipeline 保存的前後欄位追溯，但沒有獨立 evaluator 原始產物可作 evaluator-direct 判定。

**資料來源：** `phase_b_source_changed_11_results.jsonl`；9B Tier B authoritative `transition_journal.jsonl`；4B D3/D1 `cell_results.jsonl`；`unified_cell_ledger.jsonl`。

---

## 6. Modified-still-failed 的逐格診斷

### 6.1 依修改層與模型的 cross table

同一 cell 可能在多層被修改，因此下表是 **stage-event** 計數，不是互斥 cell 數。

| 修改層 | Qwen 4B | Qwen 9B | Gemini | Stage-events 合計 |
|---|---:|---:|---:|---:|
| Tier A | 5 | 0 | 0 | 5 |
| Tier B | 4 | 3 | 0 | 7 |
| Tier C1 | 0 | 1 | 0 | 1 |
| Tier C2 | 5 | 6 | 0 | 11 |
| D3+D1（union） | 5 | 12 | 0 | 17 |
| D5 | 1 | 0 | 0 | 1 |
| D2 | 1 | 0 | 0 | 1 |
| **合計** | **21** | **22** | **0** | **43** |

去除跨層重複後，共 **38 個不重複 modified-still-failed cells**：4B 21、9B 17、Gemini 0。9B 有 5 格先在 Tier B/C1/C2 修改，後又在 D1 修改，故 22 events 對應 17 cells。

**資料來源：** `unified_cell_ledger.jsonl` 的相鄰 stage source SHA 與 `formal_final_status`。

### 6.2 修改前後可解析性與執行進展

| 模型 | 不重複 modified-still-failed | 修改前可解析 | 修改前不可解析 | 修改後可解析 | 修改後不可解析 | 曾取得 execution gain |
|---|---:|---:|---:|---:|---:|---:|
| Qwen 4B | 21 | 14 | 7 | 20 | 1 | 4 |
| Qwen 9B | 17 | 14 | 3 | 17 | 0 | 4 |
| **合計** | **38** | **28** | **10** | **37** | **1** | **8** |

唯一修改後仍不可解析的是 4B `ce112_q09_divisor_multiple_intersection`／Ab2d+api／seed `2026072003`；其原始 failure 為 catastrophic truncation，Tier A 的窄修復不足以補回被截斷的主要內容。

**資料來源：** 4B `phase_b_source_changed_11_results.jsonl`、Tier B/C2/D3-D1/D5/D2 `cell_results.jsonl`；9B 各 fail-gated authoritative `transition_journal.jsonl`。

### 6.3 Tier A 的具體失敗模式

| Cell | 實際變換 | 修改後卡點 |
|---|---|---|
| 4B・`ce115_calc_exact_rational_expression_l1`・Ab1・`2026072004` | 補上唯一缺失 `)` | L1 parse error 被移除，但停在 L2 `OUTPUT_SCHEMA_MISMATCH` |
| 4B・`ce112_q09_divisor_multiple_intersection`・Ab2d+api・`2026072001` | `json.dumps(correct_answer_dict)` → `correct_answer_dict` | 仍為 L4 runtime exception；`safe_eval` 未定義 |
| 4B・`ce112_q04_radical_simplification`・Ab2g・`2026072002` | scalar payload → `{"radicand": 135}` | schema blocker 被移除，但停在 L5 correctness／structural mismatch |

第一格的實際 source diff：

```python
# 修改前
return ... + "}{1} \\cdot ..."

# 修改後
return ... + "}{1} \\cdot ..." )
```

第二格的實際 source diff：

```python
# 修改前
"correct_answer": json.dumps(correct_answer_dict)

# 修改後
"correct_answer": correct_answer_dict
```

這些案例說明 Tier A 只修其命中的局部 blocker；不會因「仍 FAIL」而繼續猜測另一個修法。

**資料來源：** `phase_b_source_changed_11_results.jsonl`；`math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl`；三格的 C0/C1 source paths（均列於 unified ledger）。

### 6.4 Tier B 的具體失敗模式

| Cell | 進展 | 修改後卡點 |
|---|---|---|
| 4B・`ce115_calc_polynomial_division_l1`・Ab2g・`2026072001` | 插入 `pass`；不可解析→可解析 | runtime failure |
| 4B・`ce111_q08_polynomial_factor_parameter_recovery`・Ab2d+api・`2026072002` | 插入 `pass`；不可解析→可解析 | runtime failure |
| 9B・`ce112_q04_radical_simplification`・Ab2d+api・`2026072002` | 插入 `pass`；parse gain + execution gain | journal 只保存 `still_failed`，未保存足以引用的 post-failure subtype |

共同 source diff：

```python
if <condition>:
    pass       # Healer 唯一新增內容
    # 原註解保留
```

證據但書：9B authoritative journal 能直接證明 parse gain、execution gain 與 `FAILED→FAILED`，但沒有保存與 4B `cell_results.jsonl` 同等細度的 post classifier outcome；因此不能替它補寫一個推測的 runtime／schema／answer 類別。

**資料來源：** 4B Tier B `cell_results.jsonl`；9B Tier B authoritative `transition_journal.jsonl`；各格 pre/post source paths。

### 6.5 D1 active-shadow 的具體失敗模式

| Cell | 實際變換 | 修改後卡點 |
|---|---|---|
| 4B・`ce111_q05_exact_fraction_expression`・Ab2d+api・`2026072003` | 移除模型自訂 `FractionOps`，改綁 runtime API | 修改前後皆可執行；仍 answer incorrect |
| 4B・`ce111_q02_polynomial_division_remainder`・Ab2d・`2026072002` | 移除 `PolynomialOps` shadow，改綁 runtime API（同格亦有 D3 quarantine） | `FAILED`／`runtime_failure`；非 rescue |
| 9B・`ce112_q04_radical_simplification`・Ab2d+api・`2026071301` | 移除唯一 `RadicalOps` shadow | execution gain，但仍 FAIL；post subtype 未完整保存 |
| 9B・`ce115_calc_radical_simplification_l1`・Ab2d+api・`2026071301` | 移除唯一 `RadicalOps` shadow | execution gain，但仍 FAIL；post subtype 未完整保存 |

4B 實際 source 片段：

```python
# 修改前
class FractionOps:
    @staticmethod
    def create(...): ...
    @staticmethod
    def add(...): ...
    @staticmethod
    def sub(...): ...

# 修改後
# 上述自訂 FractionOps 整段移除；原本的 FractionOps 呼叫保留，
# 因而改綁 frozen scaffold 注入的正式實作。
```

證據但書：4B D1 journal 保存完整 classifier outcome；9B D1 journal 保存 source lineage、shadow binding、execution gain 與 `FAILED→FAILED`，但缺少完整 post-failure subtype。因此本報告能列出實際 cell 與變換，不能把 4B 的 `answer_incorrect` 類別外推給 9B。

**資料來源：** 4B D3/D1 `cell_results.jsonl`；9B D3/D1 authoritative `transition_journal.jsonl`；相關 pre/post sources。

---

## 7. 三層次框架的定量結論

本輪 38 個不重複 modified-still-failed cells 中：

- 修改前：28 格可解析、10 格不可解析。
- 修改後：37 格可解析、1 格仍不可解析。
- 8 格取得 execution gain，前進到可執行／可診斷層。
- **0 格**達到完整 PASS，因本節母體刻意限定為 modified-still-failed。

可直接引用的總結句：

> Math16 Round 1 的 38 個 modified-still-failed cells 中，修改後 37 格可解析，8 格取得 execution gain，但 0 格達到完整 PASS；這證明「移除 blocker」與「修成完整正確答案」是不同研究層次。

**資料來源：** 第 6.2 節所列 stage journals；`unified_cell_ledger.jsonl`。

---

## 8. Rule ID、實作 SHA-256 與治理狀態

SHA-256 以封存 commit 中實際 UTF-8 原始碼 bytes 計算。Tier C1 沒有獨立 rule module，因此釘選實際執行 transform 的 runner，避免捏造不存在的檔案。

| Tier | 原始碼中的 rule_id | SHA-256 | 狀態 | 實作路徑 |
|---|---|---|---|---|
| A | `L1_CLOSE_UNBALANCED_PARENTHESIS` | `4e68a0b488b87d26865c94c6271def373f5bf6ba257298947586f99c01d4de1d` | frozen | `agent_tools/finals_rebuild/ce115_research_healer_rules_l1_paren_close.py` |
| A | `L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED` | `ddad91f867fc9bed2cd5eb6549631f0e83fa6f84f464490e8b5e22c860a6826d` | frozen | `...rules_l1_delimiter_extended.py` |
| A | `L1_PROSE_RESIDUE_NARROW` | `a8ea5f1198c073d0c5e9971ea541e48ae5c4072f9a7315850726f0ba6ea2d1eb` | frozen | `...rules_l1_prose_narrow.py` |
| A | `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | `b3385a3f1c0da0032ac895d44367e09a66b9817e121920b9a499d92f18387f29` | frozen | `...ce115_research_healer_rules_l2.py` |
| A | `L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM` | `8a89c099e2a491ca45826e5fb7a6c9ff7b53ce6bda2eaa3f29c138c1035a1896` | frozen | `...rules_l2_kwargs_bag_inline.py` |
| A | `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP` | `7aeecce7e86468c08f872e09c03fcf067de3077eac4eaf4cdcca7c0fe5539046` | frozen | `...rules_l2_json_dumps_unwrap.py` |
| B | `core.normalize_fullwidth_python_punctuation` | `be1b15545ceebc50dd099bd16af041f8886aeb693a52227db69bd91e2b40ed2d` | development candidate（implemented） | `aggressive_healer_tier_a/rule_a1_fullwidth.py` |
| B | `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | `70631d33c74f45cdb4668abd4151584b32f5dd9a862aa564c14822075213621f` | development candidate（implemented） | `.../rule_a2_delimiter.py` |
| B | `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | `94afce503bc739888d59e4e656869b6a51a4368d642a09eceb81d15244d8319e` | development candidate（implemented） | `.../rule_a3_empty_suite.py` |
| B | `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | `834d79f017379c461f51d95fbe8036000e3fc9fe4a274fa19300e323dd13db73` | development candidate（implemented） | `.../rule_a4_import_binding.py` |
| C1 | `TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1` | `f9c5b029b88c6ae89bc6e03285e1358cd4737586e6b7620adb351eb69dc52813` | development candidate（runner-inline；mapping 尚標 spec-only） | `scripts/run_math16_c2_c3_tier_c1_qwen9b_v1.py` |
| C2 | `TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1` | `7cfb9c2f469b99820addc657fe43a04f1d84e9c96c2ee1294e15219e0af1fc35` | development candidate（dev-only） | `aggressive_healer_tier_c2/rule_default_optional_cleanup.py` |
| D3 | `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1` | `757fe5ceebdac3d9f107436def572bfbc193b06f0e3634d64faa879eed6adaca` | development candidate | `aggressive_healer_tier_d/rule_d3_syntax_residue_quarantine.py` |
| D1 | `TIER_D_OPS_SHADOW_REMOVAL_V1` | `a9e6af1dd23a89bb0bb7f1955fb2320c50746362eb91436efa26a5c57522c1f0` | development candidate | `aggressive_healer_tier_d/rule_d1_ops_shadow_removal.py` |
| D5 | `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1` | `c86ac468673ae77fdd90a09d5ce978054dfacbedee737c7d453300debc7de93c` | development candidate | `aggressive_healer_tier_d/rule_d5_ranked_domain_method_binding.py` |
| D2 | `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1` | `6e36b1218102f8436665af7748c994255f109b4c86804ed7a5d703b0b5721d92` | development candidate | `aggressive_healer_tier_d/rule_d2_duplicate_definition_selection.py` |

表中的 `TIER_A_*`／`TIER_B_*` 是歷史 legacy ID，不代表 current tier；正式層級以 mapping manifest 為準。

**資料來源：** 上表各實作檔；`math16_healer_rule_id_tier_mapping_v1.json`；`math16_cumulative_healer_layering_protocol_v1.md`。

---

## 9. 證據限制與不可主張事項

1. 4B unified ledger 的 `ever_triggered`／`ever_modified` 部分欄位為 NULL／`DIAGNOSTIC_PENDING`；因此第 4 節只列可機械核對的 source-change class，不捏造完整 trigger-abstain class。
2. 9B Tier B/C1/C2/D1 authoritative journals保存 status、source SHA、parse/execution gain 與 rule IDs，但部分 stage 沒有保存完整 post classifier subtype；缺失處已逐格標明，沒有用 4B 案例代替。
3. Tier C1 mapping 狀態與實際 runner evidence 不一致：mapping 寫 `spec_only_not_implemented`，但 runner 與 journal 證明有 1 格實際修改。本文件保留此差異，不回寫舊 mapping。
4. 本報告不主張模型規模與修復率的普遍因果關係；它只說明本次 residual failure 是否落入既有 deterministic rules 的修復窗口。
5. `modified`、`parse gain`、`execution gain` 與 `verified rescue` 是四種不同結果，不能互相替代。

---

## 10. 本次新增內容 vs 原 `08` 文件

| 缺口 | 本次新增 |
|---|---|
| 1. 每層機制 | 新增 Tier A、B、C1、C2、D3、D1、D5、D2 的處理對象、gate、結果與實際案例 |
| 2. modified-still-failed | 新增 43 stage-events／38 unique cells、模型×層 cross table、parseability、execution gain 與逐格診斷 |
| 3. rule_id + SHA | 新增 16 條實際執行規則／runner 的語意化 ID、SHA-256、狀態與路徑 |
| 4. rescue 證據等級 | 逐格重核：6/9 evaluator-only；3/9 pipeline-assisted（1 格不可解析、2 格 runtime blocker） |
| 5. Transform class | 新增 12 個模型×Prompt 欄位的 source-change class 交叉表 |
| 6. 三層定量分佈 | 新增 38 格中 37 格 post-parseable、8 格 execution gain、0 格 full PASS 的引用句 |

本次沒有修改 `469→478`、rescue=9、4B/9B/Gemini=`8/1/0` 等正式主表數字。

---

## 11. 主要證據索引

- `docs/experiments/results/math16_three_model_historical_round1_unified_cell_ledger_v1/unified_cell_ledger.jsonl`
- `docs/experiments/results/math16_three_model_historical_round1_unified_cell_ledger_v1/validation_summary.json`
- `docs/experiments/results/math16_method2_all_cell_replay_v1/phase_b_source_changed_11_results.jsonl`
- `docs/experiments/results/math16_c1_c2_tier_b_development_replay_v1/cell_results.jsonl`
- `docs/experiments/results/math16_c2_c4_tier_c2_development_replay_v1/cell_results.jsonl`
- `docs/experiments/results/math16_c4_c5_tier_d_d3_d1_development_replay_v1/cell_results.jsonl`
- `docs/experiments/results/math16_c5a_tier_d_d5_development_replay_v1/cell_results.jsonl`
- `docs/experiments/results/math16_c5a_tier_d_d2_development_replay_v1/cell_results.jsonl`
- `docs/experiments/results/math16_c1_c2_tier_b_reproducibility_qwen9b_fail_gated_authoritative_v1/transition_journal.jsonl`
- `docs/experiments/results/math16_c2_c3_tier_c1_reproducibility_qwen9b_fail_gated_authoritative_v1/transition_journal.jsonl`
- `docs/experiments/results/math16_c3_c4_tier_c2_reproducibility_qwen9b_fail_gated_authoritative_v1/transition_journal.jsonl`
- `docs/experiments/results/math16_c4_c5a_tier_d_d3_d1_reproducibility_qwen9b_fail_gated_authoritative_v1/transition_journal.jsonl`
- `docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json`
- `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md`
- `docs/experiments/design/math16_tier_d_risk_accepting_repair_spec_v1.md`
