# Math16 Tier D — Risk-Accepting Deterministic Repair Spec v1

> **status:** `specification_only_not_implemented`
> **spec_version:** `v1`
> **risk_tier:** `Tier D`
> **layer_role:** `failure_gated_risk_accepting_repair`
> **layering_protocol:** `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md`
> **HEAD_at_authoring:** `f0eae63fe8c3760e9912589654657510119175ce`
> **origin/main_at_authoring:** `f0eae63fe8c3760e9912589654657510119175ce`

本文件定案 **Tier D** 的正式設計規格。本輪**不**實作、**不**跑 census／replay、**不**執行 candidate／evaluator、**不**呼叫模型、**不**建立正式 Aggressive Healer v2。

---

## 1. Positioning

### 1.1 Definition

**Tier D** = **failure-gated、risk-accepting、deterministic repair track**。

| Property | Binding |
|---|---|
| Failure-gated | 只接受前層後仍 **FAIL** 的 cells 作為輸入 |
| Risk-accepting | 允許比 Tier A–C 更積極的局部變換（含 ranked multi-candidate 與固定模板 body 重建），但必須可審計、可 abstain、可分帳 |
| Deterministic | 相同 pre-source + 相同 frozen contract／ranking／template → 相同觸發、選元、abstain 與 post-source |
| No-LLM | **禁止** LLM 生成／改寫 body 或參與候選選擇 |
| No-evaluator-selection | **禁止**以 evaluator PASS／FAIL、正確答案或修後結果回饋 ranking |

### 1.2 Relation to Tier A–C

| Layer | Nature | Mixing with Tier D |
|---|---|---|
| Tier A–C | Conservative／structural／contract-aware | **獨立分帳**；Tier D verified rescue **不得**混入既有 A–C headline |
| Tier D | Risk-accepting residual track | 只吃前層 FAIL residual；不回寫改寫 A–C 規則 |

Tier D **不**放寬既有 Tier C guard；Tier C 的 uniqueness／SYSTEM_CONTRACT_CORRECT 等約束維持原規格。

### 1.3 Cumulative slot

```text
C5 = C4 + Tier D
```

輸入必須為 **C4 final post-source**（見 `math16_c4_final_source_closure_v1`）。當前 4B Development residual = **C4 still-FAIL 234 cells／C4 final post-source**。**不得**直接使用純 C2 final post-source 作為 Tier D 輸入（C4 已承接 Tier C1 NO_OP + Tier C2 的 5 格 post-source）。

LLM repair 必須另立**獨立實驗軌道**，**不得**混入 Tier D 或 C5。

---

## 2. Hard mechanism boundaries

### 2.1 Multi-candidate selection（強制）

只能使用**預先凍結**的 deterministic ranking。

**禁止：**

1. 跑多個候選後依 evaluator PASS 選擇
2. 用正確答案決定候選
3. 用修後結果回饋 ranking／權重

**固定流程：**

```text
1. 依 frozen features 對每個候選計分
2. 選唯一最高分
3. 並列（score tie）或分差 < minimum_margin → abstain
4. 只輸出一個正式 post-source
5. evaluator 僅在修復完成後評量（觀測），永不回饋步驟 1–4
```

Diagnostic shadow candidates 可記錄於 audit，**不得**影響正式 post-source。

### 2.2 Local body reconstruction（強制）

只允許**固定模板**（frozen template registry）。

**禁止：**

1. LLM 生成 body
2. 自由重寫演算法
3. evaluator-driven retry
4. 自然語言 semantic repair

---

## 3. Blindness／gating split

| Signal | Allowed use |
|---|---|
| Correct answer value | **禁止**（answer-blind） |
| Evaluator PASS／FAIL／outcome | **禁止**用於 trigger、ranking、template 選擇（repair-selection evaluator-blind） |
| 既有 cell FAIL 狀態（前層 journal） | **允許**僅作 **cell-gating**（是否進入 Tier D 池） |
| Prompt／contract／SSOT／AST／scaffold | **允許**作 eligibility、features、templates |

---

## 4. Input pool and bookkeeping

### 4.1 Current 4B Development residual (authoritative snapshot)

| Quantity | Value |
|---|---:|
| C0 PASS | 79／320 |
| C1 PASS | 85／320 |
| C2 PASS | 86／320 |
| C4 still-FAIL（identity = C2 still-FAIL） | **234** |

- 每格 Tier D 輸入 = **C4 final post-source**（`math16_c4_final_source_closure_v1`）
- Lineage：Tier C1 = 0 eligible → NO_OP；Tier C2 = 5 modified-still-failed → `TIER_C2_POST_SOURCE`；其餘 229 → `C2_PRESERVED`
- **不得**直接使用純 C2 final post-source 作為 Tier D 輸入
- **不得**回退 raw 或 C1-pre-Tier-B source

`C5 = C4 + Tier D`；本 234 格為當前 4B C4 residual 人口錨。

### 4.2 Separate ledger（強制）

Tier D 報告與 Tier A–C **分開**：

- 不得把 Tier D rescue 加進 Pilot-02／Method2 Tier A verified rescue = 6
- 不得把 Tier D 邊際與 Tier B／C Development replay 混成單一 headline

### 4.3 Required ledger fields（每格至少）

| Field | Notes |
|---|---|
| `attempted` | 是否進入 Tier D runner |
| `triggered` | 是否有規則觸發 |
| `modified` | 正式 post-source 是否異於 pre |
| `abstained` | 觸發後放棄 |
| `parse_gain`／`parse_regression` | parseable 狀態相對 pre |
| `executable_gain`／`executable_regression` | executable 狀態相對 pre |
| `verified_rescue` | FAIL→PASS（僅 ledger；不回饋選擇） |
| `still_failed` | 仍 FAIL |
| `FAIL_STILL_FAIL_BUT_DEGRADED` | 仍 FAIL 且 parse／executable／failure-layer 惡化 |
| `edit_distance` | 字元或 AST 節點距離（實作時凍結一種） |
| `selected_candidate_score` | 入選分 |
| `runner_up_score` | 次高分（無則 null） |
| `abstention_reason` | 必填於 abstain |
| `rule_id`／`current_tier`／`layer_role` | 固定 `Tier D`／`failure_gated_risk_accepting_repair` |

---

## 5. Frozen ranking contract（shared）

適用所有「多候選」規則（至少 D2、D5；其他規則若產生 >1 候選亦必須套用）。

### 5.1 Allowed features only

| Feature ID | Description | Similarity? |
|---|---|---|
| `F_prompt_contract_token` | prompt／contract 詞彙命中（任務暴露符號、necessity 卡關鍵詞） | No |
| `F_class_compat` | Ops class 與任務 domain／exposed class 相容 | No |
| `F_method_compat` | method 屬於 exposed／SSOT 集合 | No |
| `F_arity` | 呼叫 arity 與簽名必要參數相容 | No |
| `F_keyword_schema` | keyword 名稱集合與簽名 schema 相容 | No |
| `F_return_shape` | 回傳使用處與 SSOT return shape 粗相容（靜態） | No |
| `F_ast_context` | AST 上下文（賦值目標、回傳、suite 位置等離散特徵） | No |
| `F_scaffold_signature` | scaffold／signature card 對齊 | No |
| `F_method_name_similarity` | method-name 相似度（輔助） | **Yes — 不得單獨決定** |

**禁止**將 evaluator outcome、答案、修後 executable／PASS 納入 features。

### 5.2 Score

\[
S(c) = \sum_i w_i \cdot f_i(c)
\]

**Spec-provisional weights**（本輪不調參；**任何 Development replay 前必須寫入獨立 ranking freeze manifest 並升版**；下列數值僅為規格可審核預設，**不是**依 evaluator 調參結果）：

| Feature | Weight \(w\) | Notes |
|---|---:|---|
| `F_prompt_contract_token` | 5 | |
| `F_class_compat` | 4 | |
| `F_method_compat` | 4 | |
| `F_arity` | 3 | |
| `F_keyword_schema` | 3 | |
| `F_return_shape` | 2 | |
| `F_ast_context` | 2 | |
| `F_scaffold_signature` | 3 | |
| `F_method_name_similarity` | 1 | **不得**為唯一非零貢獻而入選 |

### 5.3 Selection thresholds

| Parameter | Spec-provisional value | Rule |
|---|---:|---|
| `minimum_score` | 8 | \(S(\text{best}) < minimum\_score\) → abstain |
| `minimum_margin` | 2 | \(S(\text{best}) - S(\text{runner-up}) < minimum\_margin\) → abstain |
| Tie | — | \(S(\text{best}) = S(\text{runner-up})\) → abstain |
| Similarity sole-decision ban | — | 若去掉 `F_method_name_similarity` 後排序改變或不再唯一 → abstain |

### 5.4 Output rule

- 只物化**一個**正式 post-source
- Shadow 候選寫入 `diagnostics.shadow_candidates[]`，不進正式結果樹

---

## 6. Candidate rules（exactly six）

本版**只**規格化下列六類；**不得**在本 spec_version 新增其他規則族。

---

### D1 — Ops shadow removal

| Field | Content |
|---|---|
| **rule_id** | `TIER_D_OPS_SHADOW_REMOVAL_V1` |
| **current_tier** | `Tier D` |
| **layer_role** | `failure_gated_risk_accepting_repair` |
| **trigger** | Candidate 內存在對注入 Ops class 名稱（`IntegerOps`／`FractionOps`／`RadicalOps`／`PolynomialOps`）的 `ClassDef`／同名綁定賦值，遮蔽 runtime 注入 |
| **eligibility** | (1) cell 在 Tier D FAIL gate；(2) parseable 或可定位 shadow 節點；(3) **唯一** shadow 錨點；(4) 移除後不需猜測替代實作 |
| **transformation** | 刪除該 shadow 定義／賦值節點，保留其餘程式；不改 call sites 或其他邏輯。移除後同名呼叫應改由 frozen scaffold 注入的正式 Ops 承接（見下方 binding 分類） |
| **ranking／template** | 單候選；無 ranking。若多 shadow 錨點 → abstain（不 ranking 猜哪個） |
| **edit boundary** | 僅 shadow 定義節點；不改 call sites、不改非 Ops 名稱 |
| **abstention threshold** | 多 shadow、shadow 與業務 class 無法機械區分、移除後明顯切斷唯一依賴且無注入可還原證明 |
| **edit budget** | 1 shadow site／cell／pass |
| **audit fields** | §4.3 + `shadow_names[]`、`removed_span` + **`shadow_binding_class`**（`DEAD_SHADOW_REMOVAL`／`ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`／`MIXED_OR_UNRESOLVED`） |
| **outcome taxonomy** | `repaired`／`abstain`／`ineligible`／`rolled_back`；若 `repaired` 且屬 active replacement，ledger **必須**另標 `ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API` |
| **explicit non-goals** | 不重寫被刪 class 的方法體；不引入 LLM；不依 PASS／evaluator 選擇是否刪；**不得**把 active replacement 敘述成死代碼清除 |

#### D1 binding classes（normative）

D1 必須以 AST binding／call-site 證據區分，不得只看名稱：

| Class | Definition | Narrative |
|---|---|---|
| `DEAD_SHADOW_REMOVAL` | Shadow 定義存在，但**未被任何執行路徑**（含 `generate` 及會被呼叫之 helper）上的 Ops call 綁定使用 | 僅在此類可稱「移除未被使用的 shadow 定義」；仍建議避免「死代碼」口語除非已證明 unused |
| `ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API` | 執行路徑上的 Ops call **原先 lexical 綁定**至模型自訂 shadow；移除後同名 call **重新綁定**至 frozen scaffold 注入的正式 Ops implementation | **高風險替換**。正式措辭必須為：以 frozen scaffold 注入的正式 Ops implementation，取代模型自訂的 active shadow implementation。**禁止**稱「移除死代碼／清除未使用 class／刪除無關定義」 |
| `MIXED_OR_UNRESOLVED` | 部分 call 綁定不清、或多路徑不一致 | abstain 或獨立標記；不得冒充 DEAD／ACTIVE |

#### D1 允許 `ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API` 的條件（全部必備）

1. Frozen scaffold **明確注入**同名正式 Ops（`IntegerOps`／`FractionOps`／`RadicalOps`／`PolynomialOps`）
2. Shadow 定義**唯一可定位**（單一名稱、單一錨點；多 shadow → abstain）
3. Call resolution 可**靜態確認**（移除前：執行路徑 call → 本地 shadow；移除後：無本地同名 binding）
4. 移除後 binding **唯一**回到 runtime 注入 Ops（不需猜測替代實作）
5. **不使用** evaluator／PASS／答案決定是否移除
6. Outcome／ledger **必須獨立標記** `ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`（與 `verified_rescue` 分欄；rescue 計數可保留，但機制敘事不得寫成 dead-code removal）

**Development 事實錨（4B C4 residual，見 supplemental closure）：** `ce112_q04` seed `2026071301`／`2026072002` 兩格 verified rescue 均為 `ACTIVE_SHADOW_REPLACED_BY_RUNTIME_API`；`verified rescue = 2` 保留。

---


### D2 — Duplicate definition selection

| Field | Content |
|---|---|
| **rule_id** | `TIER_D_DUPLICATE_DEFINITION_SELECTION_V1` |
| **current_tier** | `Tier D` |
| **layer_role** | `failure_gated_risk_accepting_repair` |
| **trigger** | 同一作用域內重複 `def`／`class` 同名定義（後者覆蓋前者） |
| **eligibility** | FAIL gate；存在可枚舉的重複定義對；可建候選「保留哪一個」集合 |
| **transformation** | 刪除未入選之重複定義，保留恰好一個 |
| **ranking／template** | **Deterministic ranking**（§5）對「保留定義 A／B／…」計分；features 含 AST 完整性、是否被引用、與 scaffold／contract 對齊；**禁止**執行後選 |
| **edit boundary** | 只刪整段重複定義；不合併／不改 body |
| **abstention threshold** | tie／margin 不足／minimum_score 不足／引用圖顯示兩者皆被需要 |
| **edit budget** | 1 組同名衝突／pass |
| **audit fields** | §4.3 + `candidate_defs[]`、`selected_candidate_score`、`runner_up_score` |
| **outcome taxonomy** | `repaired`／`abstain`／`ineligible`／`rolled_back` |
| **explicit non-goals** | 不合成新定義；不用 evaluator 挑選；不 LLM |

---

### D3 — Syntax residue quarantine

| Field | Content |
|---|---|
| **rule_id** | `TIER_D_SYNTAX_RESIDUE_QUARANTINE_V1` |
| **current_tier** | `Tier D` |
| **layer_role** | `failure_gated_risk_accepting_repair` |
| **trigger** | 可定位的非執行殘留（例如 `generate` 之後的散文／殘段、明確無綁定的尾部 syntax residue），且存在**唯一**quarantine 邊界 |
| **eligibility** | FAIL gate；residue 區間可機械證明不影響 `generate` AST（或移除後 `generate` 唯一保留）；與 Tier A prose 規則不重疊時才可動（若 A 已適用且未改，D 不得重複搶修同一 span） |
| **transformation** | 將 residue 註解化或刪除（兩者皆為固定策略；**策略必須在 freeze 時二選一寫死**，預設：**comment-out**） |
| **ranking／template** | 單策略；無多候選 ranking。多邊界 → abstain |
| **edit boundary** | 僅 residue 區間；不改 `generate` body 語義節點 |
| **abstention threshold** | 邊界不唯一；residue 與可執行碼交織無法分離 |
| **edit budget** | 1 contiguous residue span／pass |
| **audit fields** | §4.3 + `residue_span`、`quarantine_mode` |
| **outcome taxonomy** | `repaired`／`abstain`／`ineligible`／`rolled_back` |
| **explicit non-goals** | 不「猜」題意補碼；不 LLM；不把 quarantine 當 body rewrite |

---

### D4 — Unique native-operation → domain-API rewrite

| Field | Content |
|---|---|
| **rule_id** | `TIER_D_UNIQUE_NATIVE_TO_DOMAIN_API_REWRITE_V1` |
| **current_tier** | `Tier D` |
| **layer_role** | `failure_gated_risk_accepting_repair` |
| **trigger** | 單一局部 native 運算型樣（預先凍結的 pattern 表，例如唯一 `a + b` on Fraction-like、唯一整除檢查）可機械對應到**唯一** exposed domain API call |
| **eligibility** | FAIL gate；`SYSTEM_CONTRACT_CORRECT` 或等價可追溯 exposed 集合；**唯一** pattern 命中；**唯一**目標 API；arguments 可原樣包裹 |
| **transformation** | 將該 native 節點改寫為對應 `Ops.method(...)`，保留子表達式 |
| **ranking／template** | 無多候選時不 ranking；若 pattern 映射表出現多 API → 必須 abstain（**不**用 similarity 決勝；若要進 D5 則本規則不觸發） |
| **edit boundary** | 單一 expression／statement 節點；不改周圍控制流 |
| **abstention threshold** | 多 pattern、多 API、Ab2d+spec native-allowed 且無義務改寫、映射不唯一 |
| **edit budget** | 1 rewrite site／pass |
| **audit fields** | §4.3 + `native_pattern_id`、`target_api`、`ssot_entry_id` |
| **outcome taxonomy** | `repaired`／`abstain`／`ineligible`／`rolled_back` |
| **explicit non-goals** | 不整段演算法 API 化；不放寬 Tier C uniqueness 去「硬改」；不 LLM |

---

### D5 — Ranked domain method binding

| Field | Content |
|---|---|
| **rule_id** | `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1` |
| **current_tier** | `Tier D` |
| **layer_role** | `failure_gated_risk_accepting_repair` |
| **trigger** | 已存在 domain API call（或可錨定之 call site），method 與契約不完全一致，且存在 **≥2** 合理 method 候選（此為相對 Tier C1 的 risk-accepting 擴張） |
| **eligibility** | FAIL gate；parseable；單一 call site；候選集合來自 exposed／SSOT／prompt cards（有限閉集）；**非** SYSTEM_CONTRACT_DEFECT／UNRESOLVED 下「修復契約本身」 |
| **transformation** | 只改 method attribute 名稱；**arguments 原樣保留** |
| **ranking／template** | **必須**套用 §5 deterministic ranking；similarity 不得單獨決定；tie／margin／min score → abstain |
| **edit boundary** | 單一 attribute 名稱節點 |
| **abstention threshold** | §5 全部 abstain 條件；候選集為空；改 class／receiver／args |
| **edit budget** | 1 binding site／pass |
| **audit fields** | §4.3 + `candidate_methods[]`、scores、`ssot_entry_id`、`similarity_sole_decision=false` |
| **outcome taxonomy** | `repaired`／`abstain`／`ineligible`／`rolled_back` |
| **explicit non-goals** | 不取代 Tier C1 的「唯一 method」嚴格路徑敘事；不 evaluator-select；不改 args；不 LLM；不放寬 Tier C 的正式 guard 定義（C1 仍維持原規格；D5 是**另帳** risk track） |

---

### D6 — Fixed-template local body repair

| Field | Content |
|---|---|
| **rule_id** | `TIER_D_FIXED_TEMPLATE_LOCAL_BODY_REPAIR_V1` |
| **current_tier** | `Tier D` |
| **layer_role** | `failure_gated_risk_accepting_repair` |
| **trigger** | `generate`（或唯一局部 helper）body 命中凍結 **template precondition**（例如：空 body、唯一 `pass`、唯一 `raise NotImplementedError`、唯一可匹配之 scaffold hole） |
| **eligibility** | FAIL gate；單一可替換 body 區間；恰好一個 template ID 命中；template 參數槽可從 frozen oracle_payload／局部既有綁定**機械填入**（不得讀答案作選擇） |
| **transformation** | 以凍結模板替換該 body 區間；槽位填入僅允許：literal from frozen params、既有 local name、SSOT API call 骨架 |
| **ranking／template** | **Fixed template registry only**。若多 template 同時命中 → abstain（**不**用 evaluator 選模板）。單 template 無 ranking |
| **edit boundary** | 單一函數 body（預設 `generate`）；不改模組級其他定義；禁止跨函數重寫 |
| **abstention threshold** | 多 template；槽位無法機械填；需自由演算法；需 LLM／NL semantic repair |
| **edit budget** | 1 body region／pass |
| **audit fields** | §4.3 + `template_id`、`slot_bindings`、`template_sha256` |
| **outcome taxonomy** | `repaired`／`abstain`／`ineligible`／`rolled_back` |
| **explicit non-goals** | **禁止** LLM body；**禁止**自由演算法重寫；**禁止** evaluator-driven retry；**禁止**自然語言 semantic repair；模板未 freeze 前不得跑 Development replay |

#### D6 template boundary (normative)

允許的模板種類（登記後凍結）：

1. `TMPL_RETURN_FROZEN_PAYLOAD_WRAP` — 以固定 dict 結構包裝已存在局部變數（結構同 L2 wrap 精神，但屬 D 帳）
2. `TMPL_SINGLE_DOMAIN_API_THEN_RETURN` — 單一 SSOT call + return 骨架
3. `TMPL_PASS_TO_SIMPLE_ASSIGN_RETURN` — 將空／`pass` body 換成「賦值 + return」固定骨架

模板必須：

- 有穩定 `template_id` 與 bytes SHA-256
- 參數槽集合封閉
- 不包含「自由語句生成」洞

---

## 7. Pipeline order and budgets（spec-level）

建議固定順序（實作凍結時寫死；本輪不實作）：

```text
D1 → D2 → D3 → D4 → D5 → D6
```

| Budget | Value |
|---|---|
| Max rules fired／cell／Tier D pass | 3 |
| Max mutations／cell／Tier D pass | 3 |
| Max formal post-sources／cell | **1** |
| Idempotence | 修復後再跑同一 allowlist 必須零 diff；否則 rollback |

跨規則：同一 cell 若兩條規則爭同一 span → abstain 該 span（不 cascading 猜測）。

---

## 8. Governance

1. **Answer-blind：** 禁止讀取正確答案作 trigger／ranking／template／slot 選擇。
2. **Repair-selection evaluator-blind：** evaluator 只作修後觀測。
3. **Cell-gating：** 可使用既有 FAIL 狀態決定是否進入池。
4. **Provenance：** 原始 raw、各層 post-source **永久保留**；Tier D 另寫獨立目錄。
5. **Single formal repair version：** 每格最多一個正式 Tier D post-source。
6. **Shadow diagnostics：** 不得影響正式結果。
7. **Freeze-before-replay：** 規則語意、feature 權重、margin、template registry 必須在任何 Development replay **前** freeze；變更必須 **spec／ranking／template 升版**。
8. **No Aggressive Healer v2 auto-naming：** Tier D 規格≠ v2；v2 門檻仍依累積協議（至少一條 Tier C 完成實作＋tests＋residual＋Development evidence 等）。
9. **LLM track isolation：** 任何 LLM repair 實驗必須使用不同 condition 名稱與報告帳本。

---

## 9. Outcome taxonomy（shared）

| Code | Meaning |
|---|---|
| `repaired` | 正式 post-source 已修改且通過 idempotence |
| `abstain` | 觸發審核後放棄 |
| `ineligible` | 未達 eligibility |
| `rolled_back` | 修改後因 idempotence／parse／budget 回滾 |
| `FAIL_STILL_FAIL_BUT_DEGRADED` | ledger 標記（仍 FAIL 且惡化） |
| `verified_rescue` | ledger 觀測 FAIL→PASS |
| `still_failed` | ledger 觀測仍 FAIL |

---

## 10. Explicit non-goals

1. 本輪實作任何 Tier D 規則或 runner
2. 對 234 格跑 census／replay／evaluator
3. 呼叫模型或 LLM body repair
4. 以 evaluator／答案選擇候選或模板
5. 修改 Tier A／B／C 規則語意或放寬 Tier C guard
6. 把 Tier D rescue 併入既有 A–C verified rescue 帳
7. 新增本文件六類以外的規則
8. 調參權重（依 evaluator 迴圈）
9. 命名正式 Aggressive Healer v2
10. Commit／push（非本規格授權）

---

## Document control

| Field | Value |
|---|---|
| Document | `docs/experiments/design/math16_tier_d_risk_accepting_repair_spec_v1.md` |
| Kind | Tier D specification only |
| Implementation | Out of scope this round |
| Ranking numeric freeze | Required in separate manifest before first replay |
| Template registry freeze | Required before D6 Development replay |
