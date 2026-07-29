# Math16 Cumulative Healer Layering Protocol v1

> **status:** `naming_and_layering_protocol_v1`
> **HEAD_at_authoring:** `f0eae63fe8c3760e9912589654657510119175ce`
> **origin/main_at_authoring:** `f0eae63fe8c3760e9912589654657510119175ce`

本文件定案 Healer **分層命名修正**與 **C0–C5 累積式實驗架構**。只規範設計／命名／量測；本輪不改 A–C 實作語意、不跑資料。

---

## Scope

本協議為 Cumulative Healer stack 的命名與分層**唯一總控**；現行 Tier 歸屬以本文件 **Legacy Rule ID Mapping Table** 與機器可讀 mapping manifest 為準。

> 程式碼與歷史紀錄中的 rule_id 保留原始命名，以維持 tests、logs 與 provenance 可追溯性；rule_id 字串中的 TIER_A／TIER_B 不代表目前研究分層。所有現行 Tier 歸屬以本文件 Legacy Rule ID Mapping Table 為唯一準據。

機器可讀對照：`docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json`

### Legacy Rule ID Mapping Table

| legacy_rule_id | current_tier | layer_role |
|---|---|---|
| `L1_CLOSE_UNBALANCED_PARENTHESIS` | Tier A | frozen_conservative_base |
| `L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED` | Tier A | frozen_conservative_base |
| `L1_PROSE_RESIDUE_NARROW` | Tier A | frozen_conservative_base |
| `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` | Tier A | frozen_conservative_base |
| `L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM` | Tier A | frozen_conservative_base |
| `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP` | Tier A | frozen_conservative_base |
| `core.normalize_fullwidth_python_punctuation` | Tier B | safe_structural_extension |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | Tier B | safe_structural_extension |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | Tier B | safe_structural_extension |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | Tier B | safe_structural_extension |
| `TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1` | Tier C1 | contract_aware_repair_candidate |
| `TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1` | Tier C2 | contract_aware_repair_candidate |
| `TIER_D_OPS_SHADOW_REMOVAL_V1` | Tier D | failure_gated_risk_accepting_repair |
| `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1` | Tier D | failure_gated_risk_accepting_repair |
| `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1` | Tier D | failure_gated_risk_accepting_repair |
| `TIER_D_UNIQUE_NATIVE_TO_DOMAIN_API_REWRITE_V1` | Tier D | failure_gated_risk_accepting_repair |
| `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1` | Tier D | failure_gated_risk_accepting_repair |
| `TIER_D_FIXED_TEMPLATE_LOCAL_BODY_REPAIR_V1` | Tier D | failure_gated_risk_accepting_repair |

治理條款：

- **Tier A** 固定指上表六條 frozen conservative 規則；不得把含 `TIER_A_` 字串的結構規則誤判為 Tier A
- **不得由 rule_id 字面推斷 Tier**（含 `TIER_A_*` → 實際 Tier B；`TIER_B_*` Domain Binding → 實際 Tier C1／C2）
- 後續 manifest／runner／report **必須同時記錄**：`rule_id`、`current_tier`、`layer_role`（以本表／mapping manifest 填入）
- 未來若 rename `rule_id`，必須升版本協議與 mapping，並保留 **alias mapping**（舊 ID → 新 ID → current_tier）
- **Tier D** 與 Tier A–C **獨立分帳**；不得把 Tier D rescue 混入既有 A–C verified rescue headline

---

## 1. Naming correction

| 舊／易混淆說法 | 正式定案 |
|---|---|
| 「Tier A」= 剛完成的四條安全結構規則 | **錯誤**。該四條為 **Tier B** |
| 「Aggressive Healer v1」= 上述四條 | **錯誤**。不得單獨將 Tier B 命名為 Aggressive Healer v1 |
| 「Tier B」= Domain API Binding（原 B1／B2） | **錯誤**。該兩條為 **Tier C**（C1／C2） |
| 「Tier A」= Pilot-02 已凍結的六條保守規則 | **正確** |
| 「Tier D」= LLM／evaluator-driven repair | **錯誤**。Tier D 為 failure-gated、deterministic、**no-LLM**、**no-evaluator-selection** |

**Rule ID 政策（本輪）：** 暫不批次 rename 歷史字串。Tier 以本協議 **Legacy Rule ID Mapping Table** 與 mapping manifest 為唯一準據。

權威交叉參照：

| Layer | Spec／evidence（路徑保留歷史檔名） |
|---|---|
| Tier A | Pilot-02 frozen allowlist（見 §2）；mapping `current_tier=Tier A` |
| Tier B | `docs/experiments/design/math16_aggressive_healer_tier_a_v1_spec.md`（檔名歷史；內容 = Tier B） |
| Tier C | `docs/experiments/design/math16_aggressive_healer_domain_api_binding_spec_v1.md`（檔名歷史；內容 = Tier C） |
| Tier D | `docs/experiments/design/math16_tier_d_risk_accepting_repair_spec_v1.md` |
| Tier B raw supply census | `docs/experiments/reports/math16_aggressive_healer_tier_a_development_supply_v1.md`（改稱 Tier B supply；**非** residual） |
| Legacy ID ↔ Tier map | `docs/experiments/manifests/math16_healer_rule_id_tier_mapping_v1.json` |

---

## 2. Tier A／B／C／D definition

### 2.1 Tier A — Frozen Conservative Healer

已完成正式 Pilot-02 實驗的**固定基底**（六條）：

| # | Rule ID |
|---|---|
| 1 | `L1_CLOSE_UNBALANCED_PARENTHESIS` |
| 2 | `L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED` |
| 3 | `L1_PROSE_RESIDUE_NARROW` |
| 4 | `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` |
| 5 | `L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM` |
| 6 | `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP` |

正式結果錨點（Qwen 4B，報告層校正後）：

- Baseline → Final：**79/320 → 85/320**
- **Verified rescue = 6**
- 為後續所有累積層的固定基底；**不得**修改這六條

### 2.2 Tier B — Safe Structural Extension

四條安全結構擴充（已實作；**不是**獨立 Aggressive Healer 版本）：

| # | Rule ID（保留既有 ID，不 rename） |
|---|---|
| B1 | `core.normalize_fullwidth_python_punctuation` |
| B2 | `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` |
| B3 | `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` |
| B4 | `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` |

### 2.3 Tier C — Contract-Aware Repair

Domain API contract-aware 候選：

| # | Rule ID（保留既有 ID，不 rename） | Short name |
|---|---|---|
| C1 | `TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1` | Explicit Domain Method Binding Repair |
| C2 | `TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1` | Domain Signature Form Repair |

Tier C **guard 不因 Tier D 而放寬**。

### 2.4 Tier D — Failure-Gated Risk-Accepting Deterministic Repair

規格：`docs/experiments/design/math16_tier_d_risk_accepting_repair_spec_v1.md`

定位（強制）：

| Attribute | Binding |
|---|---|
| Failure-gated | 只接受前層後仍 FAIL 的 cells |
| Risk-accepting | 允許 ranked multi-candidate 與固定模板 body 重建，但可審計／可 abstain |
| Deterministic | 凍結 features／權重／模板；同輸入同輸出 |
| No-LLM | 禁止 LLM 生成或改寫 |
| No-evaluator-selection | 禁止以 evaluator／答案選擇候選；evaluator 僅修後觀測 |
| Separate ledger | 與 Tier A–C 分帳；不混入既有 verified rescue |

六條候選（僅 placeholder／規格；**未**實作）：

| # | Rule ID |
|---|---|
| D1 | `TIER_D_OPS_SHADOW_REMOVAL_V1` |
| D2 | `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1` |
| D3 | `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1` |
| D4 | `TIER_D_UNIQUE_NATIVE_TO_DOMAIN_API_REWRITE_V1` |
| D5 | `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1` |
| D6 | `TIER_D_FIXED_TEMPLATE_LOCAL_BODY_REPAIR_V1` |

LLM repair 必須另立獨立實驗軌道，**不得**混入 Tier D／C5。

---

## 3. C0–C5 cumulative order

固定累積順序（**每層輸入 = 前一層輸出**；禁止各自獨立平行比較）：

```text
C0 = Raw baseline
C1 = Tier A
C2 = Tier A + Tier B
C3 = Tier A + Tier B + Tier C1
C4 = Tier A + Tier B + Tier C1 + Tier C2
C5 = C4 + Tier D
     = Tier A + Tier B + Tier C1 + Tier C2 + Tier D
```

| Condition | Composition | Input |
|---|---|---|
| C0 | 無 Healer | Raw candidate |
| C1 | Tier A only | C0 output |
| C2 | Tier A then Tier B | C1 output |
| C3 | Tier A then Tier B then C1 | C2 output |
| C4 | Tier A then Tier B then C1 then C2 | C3 output |
| C5 | C4 then Tier D | C4 output（仍 FAIL 子集） |

當前 4B 操作錨（C4 final-source closure 已建立）：

- C2 PASS = 86／320；**C4 still-FAIL = 234**（identity 承接 C2 still-FAIL）
- Tier D Development 輸入必須為 **C4 final post-source**（`math16_c4_final_source_closure_v1`）
- **不得**直接使用純 C2 final post-source 作為 Tier D 輸入
- `C5 = C4 + Tier D`

禁止：

- 以「只跑 Tier B／C／D」與 C1 做平行 headline 比較
- 跳層（例如 Raw 直接進 Tier D）
- 在同一 condition 內循環重試超出各層自身 budget
- 將 Tier D ledger 混入 Tier A–C verified rescue

---

## 4. Residual eligibility

| Concept | Definition |
|---|---|
| Raw supply | 對 **C0** 原始 candidate 的靜態 eligibility |
| Residual supply @ Ck | 對 **Ck 輸出** 再做下一層規則的靜態 eligibility |
| Required for Tier B claims | Residual after **C1** |
| Required for Tier C claims | Residual after **C2** |
| Required for Tier D claims | Residual after **C4**；當前 4B = **C4 still-FAIL 234／C4 final post-source**（不得純 C2） |

---

## 5. Marginal metrics

每一累積層（相對前一層）至少量測：

| Metric | Meaning |
|---|---|
| `residual_eligible_supply` | 進入本層前仍靜態 eligible 的格數 |
| `marginal_triggered` | 本層實際觸發 |
| `marginal_modified` | 本層 mutation |
| `marginal_executable_gain` | executable 改善 |
| `marginal_verified_rescue` | 新增 verified rescue |
| `preserved_pass` | 前層 PASS 仍 PASS |
| `regression` | 狀態惡化 |
| `abstention` | abstain |

Tier D 額外強制：`FAIL_STILL_FAIL_BUT_DEGRADED`、`selected_candidate_score`、`runner_up_score`、`edit_distance`（見 Tier D 規格）。

所有邊際量測必須標註：**input_condition** 與 **output_condition**（現含 C5）。

---

## 6. Version naming rule

| Name | When allowed |
|---|---|
| **Tier A** | 已成立：Pilot-02 六條 |
| **Tier B** | 已實作＋tests；**不得**單獨稱 Aggressive Healer v1 |
| **Tier D** | 規格已定；實作前不得寫入正式 C5 結果表；**不是** LLM track |
| **Aggressive Healer v2** | **僅當**同時滿足：至少納入一條 Tier C；完成該 C 規則之 implementation、focused tests、**residual** census、以及 Development evidence 後，方可正式命名 |

Tier D 的存在**不**自動構成 Aggressive Healer v2。

---

## 7. Governance／freeze

1. **Tier A 六條**：凍結。
2. **Tier B 四條**：實作凍結於現況語意。
3. **Tier C**：不因 Tier D 放寬 guard。
4. **Tier D**：規則、ranking 權重、margin、template registry 必須在 replay 前 freeze；變更升版。
5. **累積比較**：新實驗必須宣告 Ck 並以 C(k−1) 輸出為輸入。
6. **分帳**：Tier D 與 A–C 分開報告。
7. Confirmatory 前不得暗改任一已凍結層規則語意。

---

## 8. Explicit non-goals

本協議**不**授權：

1. 修改六條 Tier A 正式規則或重跑 Pilot-02
2. 修改四條 Tier B 實作語意（本輪）
3. 放寬 Tier C guard
4. 本輪實作 Tier D 或跑 234 census／replay
5. LLM／evaluator-driven 候選選擇混入 Tier D
6. 批次 rename 歷史 `rule_id`
7. 將 Tier B 單獨命名為 Aggressive Healer v1
8. 以 Tier D 規格直接命名 Aggressive Healer v2
9. 非累積式平行層間 headline 比較
10. Commit／push（由本授權任務決定）

---

## Document control

| Field | Value |
|---|---|
| Document | `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md` |
| Kind | Naming + cumulative protocol（C0–C5） |
| Tier D spec | `docs/experiments/design/math16_tier_d_risk_accepting_repair_spec_v1.md` |
| Implementation／data this round | Out of scope |
