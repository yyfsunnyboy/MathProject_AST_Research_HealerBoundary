# Math16 Tier B — Safe Structural Extension Supply Census v1

> **status:** `tier_b_supply_census_v1`（raw／overall inventory；**非** residual-after-Tier-A）
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **manifest:** `docs/experiments/manifests/math16_aggressive_healer_tier_a_development_supply_v1.json`（歷史檔名；內容為 Tier B raw supply）
> **layering_protocol:** `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md`
> **rule_id_tier_mapping:** `docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json`

## 1. Scope

唯讀 eligibility census for **Tier B（Safe Structural Extension）** 四條規則。不執行 Healer mutation、不跑 evaluator、不改 candidate、不進 Validation／Confirmatory。

> 現行 Tier 歸屬以 `math16_cumulative_healer_layering_protocol_v1.md` 與 mapping manifest 為準；rule_id 為歷史識別碼。

**Naming correction：** 本報告原稱「Aggressive Healer Tier A Development Supply」；依累積分層協議，該四條為 **Tier B**。本 census 為對 **C0 raw** 的 **Tier B supply**，**不是** residual-after-Tier-A，亦不得單獨稱為 Aggressive Healer v1 供給。

**Split：** Cumulative／Aggressive stack 之 Development／Validation／Confirmatory 切分**尚未定義**；本文件只輸出 **overall supply inventory**，不自行發明切分。既有 Method1 Contract-Aware 40/120 屬不同產品契約，**未**作為本 census 的 Development 切刀。

**Tier A 對照：** Frozen Conservative Healer 六條為累積基底（Pilot-02；4B 79/320 → 85/320；verified rescue = 6）。後續 C2 邊際結論必須另測 **residual eligible supply after C1（Tier A）**。

## 2. Evidence source

| Item | Value |
|---|---|
| Universe | Formal Pilot-02 `cell_level_baseline.jsonl` × 3 models = **960** cells |
| Qwen4B baseline | `math16_pilot02_qwen4b_evaluation_v4_r001/cell_level_baseline.jsonl` |
| Qwen9B baseline | `math16_pilot02_qwen9b_evaluation_v4_r001/cell_level_baseline.jsonl` |
| Gemini baseline | `math16_pilot02_full_evaluation_v4_r001/cell_level_baseline.jsonl` |
| Candidate policy | Method2 `raw_sources` → else formal `extract_code` (+ journal `candidate_hash` verify when present) |
| Spec | `docs/experiments/design/math16_aggressive_healer_tier_a_v1_spec.md`（歷史檔名；**Tier B** 規格） |
| Implementation | `agent_tools/finals_rebuild/aggressive_healer_tier_a/`（目錄名歷史；**Tier B** 實作） |

Source kind counts:

- `formal_extract_code_verified_vs_journal_candidate_hash`: 640
- `method2_raw_sources`: 320

Missing candidate sources: **0**

## 3. Eligibility method

對每格 **C0 raw** candidate，**分別**對四條 Tier B 規則呼叫既有 `apply_once` 做靜態判定；**丟棄** `source_out`，不做管線串接、不寫 post-source、不執行 candidate、不跑 evaluator。Eligibility **不**讀取 PASS／FAIL（PASS 僅作事後 safety check）。

Statuses: `ELIGIBLE` / `ALREADY_CORRECT` / `AMBIGUOUS_ABSTAIN` / `INELIGIBLE` / `MULTI_RULE_OVERLAP`.

> 本方法量測的是 **raw Tier B supply**。Cumulative protocol 要求 C2 宣稱使用 **residual supply on C1 output**；該 residual census **尚未**執行。

## 4. Aggregate counts

| Metric | Count |
|---|---:|
| Cells | 960 |
| Unique eligible cells（raw Tier B） | 9 |
| Multi-rule overlap cells | 0 |
| Total eligible rule-slots | 9 |
| FAIL cells with no raw Tier B supply | 483 |
| PASS cells marked eligible | 0 |

Eligible by rule (includes MULTI_RULE_OVERLAP slots；raw)：

| Rule ID | Eligible slots |
|---|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 9 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 |

## 5. Counts by model／condition／rule

### By model

**qwen4b** (n=320): unique_eligible=5, overlap=0

| Rule | ELIGIBLE | ALREADY_CORRECT | AMBIGUOUS_ABSTAIN | INELIGIBLE | MULTI_RULE_OVERLAP |
|---|---:|---:|---:|---:|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 | 240 | 0 | 80 | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 | 240 | 1 | 79 | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 5 | 240 | 0 | 75 | 0 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 | 218 | 0 | 102 | 0 |

**qwen9b** (n=320): unique_eligible=4, overlap=0

| Rule | ELIGIBLE | ALREADY_CORRECT | AMBIGUOUS_ABSTAIN | INELIGIBLE | MULTI_RULE_OVERLAP |
|---|---:|---:|---:|---:|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 | 249 | 0 | 71 | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 | 249 | 0 | 71 | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 4 | 249 | 1 | 66 | 0 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 | 209 | 0 | 111 | 0 |

**gemini** (n=320): unique_eligible=0, overlap=0

| Rule | ELIGIBLE | ALREADY_CORRECT | AMBIGUOUS_ABSTAIN | INELIGIBLE | MULTI_RULE_OVERLAP |
|---|---:|---:|---:|---:|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 | 317 | 0 | 3 | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 | 317 | 0 | 3 | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 0 | 317 | 0 | 3 | 0 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 | 307 | 0 | 13 | 0 |

### By condition

**ab1** (n=240): unique_eligible=1, overlap=0

| Rule | ELIGIBLE | ALREADY_CORRECT | AMBIGUOUS | INELIGIBLE | OVERLAP |
|---|---:|---:|---:|---:|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 | 218 | 0 | 22 | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 | 218 | 1 | 21 | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 1 | 218 | 0 | 21 | 0 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 | 215 | 0 | 25 | 0 |

**ab2d** (n=240): unique_eligible=4, overlap=0

| Rule | ELIGIBLE | ALREADY_CORRECT | AMBIGUOUS | INELIGIBLE | OVERLAP |
|---|---:|---:|---:|---:|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 | 173 | 0 | 67 | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 | 173 | 0 | 67 | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 4 | 173 | 1 | 62 | 0 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 | 130 | 0 | 110 | 0 |

**ab2d_spec** (n=80): unique_eligible=0, overlap=0

| Rule | ELIGIBLE | ALREADY_CORRECT | AMBIGUOUS | INELIGIBLE | OVERLAP |
|---|---:|---:|---:|---:|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 | 80 | 0 | 0 | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 | 80 | 0 | 0 | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 0 | 80 | 0 | 0 | 0 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 | 75 | 0 | 5 | 0 |

**ab2d_spec_v2** (n=160): unique_eligible=0, overlap=0

| Rule | ELIGIBLE | ALREADY_CORRECT | AMBIGUOUS | INELIGIBLE | OVERLAP |
|---|---:|---:|---:|---:|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 | 134 | 0 | 26 | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 | 134 | 0 | 26 | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 0 | 134 | 0 | 26 | 0 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 | 125 | 0 | 35 | 0 |

**ab2g** (n=240): unique_eligible=4, overlap=0

| Rule | ELIGIBLE | ALREADY_CORRECT | AMBIGUOUS | INELIGIBLE | OVERLAP |
|---|---:|---:|---:|---:|---:|
| `core.normalize_fullwidth_python_punctuation` | 0 | 201 | 0 | 39 | 0 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 0 | 201 | 0 | 39 | 0 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 4 | 201 | 0 | 35 | 0 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 0 | 189 | 0 | 51 | 0 |

## 6. Overlap

Multi-rule overlap cells: **0**

No multi-rule overlap cells.

## 7. Abstention reasons

Top abstention／noop reasons (rule::reason → count):

- `core.normalize_fullwidth_python_punctuation::no_unprotected_mapped_or_fail_closed`: 960
- `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1::source_already_parses`: 806
- `TIER_A_EMPTY_SUITE_INSERT_PASS_V1::source_already_parses`: 806
- `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1::no_unique_stdlib_binding_gap`: 734
- `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1::source_not_parseable`: 154
- `TIER_A_EMPTY_SUITE_INSERT_PASS_V1::no_empty_suite_site`: 138
- `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1::syntax_error_not_delimiter`: 126
- `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1::missing_names_not_uniquely_mappable`: 34
- `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1::ops_class_shadowing`: 34
- `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1::no_unique_closing_insert`: 27
- `TIER_A_EMPTY_SUITE_INSERT_PASS_V1::empty_suite_insert_pass_still_unparseable`: 6
- `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1::domain_ops_or_excluded_binding`: 4
- `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1::ambiguous_closing_inserts_count_26`: 1
- `TIER_A_EMPTY_SUITE_INSERT_PASS_V1::ambiguous_empty_suites_count_2`: 1

## 8. PASS-cell safety check

Formal PASS cells marked Tier B eligible（raw）: **0** (required: 0).

PASS-cell false eligibility = 0.

Note: PASS／FAIL were **not** used to decide eligibility; this section is a post-hoc audit only.

## 9. Development readiness

Unique eligible cells（raw Tier B）= **9**; overlap = **0**; FAIL without raw Tier B supply = **483**.

**Readiness:** Raw Tier B 供給極窄（僅 empty-suite 9 格），可作結構規則除錯參考；**不足以**支持把 Tier B 單獨稱為 Aggressive Healer v1，也**不能**替代 residual-after-Tier-A。進入 C2 邊際實驗前必須：先跑 C1（Tier A），再測 residual Tier B supply，並正式定義 Dev／Val／Conf 切分後方可消耗 holdout。

## 10. Limitations

- Cumulative stack Dev／Val／Conf split 未定義；本 census 為 **raw Tier B overall supply**。
- Eligibility 以單規則、**C0 raw** source 獨立判定；非正式 C1→C2 累積管線後的 residual 集合。
- Gemini Primary 使用 `ab2d_spec`（v1）；Qwen 使用 `ab2d_spec_v2`。
- Method2 raw_sources 主要覆蓋 Qwen4B；其餘多依賴 formal extract_code。
- 未執行 mutation／evaluator／candidate；無 post-source 產物。
- Manifest／路徑檔名仍含歷史 `tier_a` 字樣；tier 定位以本報告與 layering protocol 為準。

