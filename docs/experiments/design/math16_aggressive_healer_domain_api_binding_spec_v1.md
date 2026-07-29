# Math16 Tier C — Domain API Binding Repair Spec v1

> **status:** `specification_repositioned_as_tier_c_contract_aware_candidates`
> **spec_version:** `v1`
> **risk_tier:** `Tier C`（Contract-Aware Repair candidates）
> **layering_protocol:** `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md`
> **HEAD_at_authoring:** `f0eae63fe8c3760e9912589654657510119175ce`
> **origin/main_at_authoring:** `f0eae63fe8c3760e9912589654657510119175ce`

> **Naming correction:** 本檔歷史敘述曾稱「Tier B」；依累積分層協議，本兩條正式定位為 **Tier C（C1／C2）**。`rule_id` 字串仍含 `TIER_B_`，**暫不 rename**。  
> 現行 Tier 歸屬以 `math16_cumulative_healer_layering_protocol_v1.md` 與 mapping manifest 為準；rule_id 為歷史識別碼。  
> **Note:** The HEAD SHAs above are git provenance at authoring time. They are **not** eligibility predicates and are not permanent gate conditions for these rules.

---

## 1. Scope

本文件定案 **Domain API Binding Repair** 的正式規格，並拆成兩條互不混用的 **Tier C** 候選規則：

| Rule | Rule ID（保留既有 ID） | Short name |
|---|---|---|
| C1 | `TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1` | Explicit Domain Method Binding Repair |
| C2 | `TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1` | Domain Signature Form Repair |

本輪只定規格定位修正：

- 不實作程式、runner、測試或 cell 篩選器
- 不執行模型／Healer／candidate／evaluator
- 不修改 frozen 結果
- 不設計其他規則族
- 不改 `rule_id`

**定位原則（強制）：**

- C1／C2 屬於 **Tier C**；在累積堆疊中僅能作為 **C3／C4** 增量（輸入必須為前一層輸出）
- **不進入** Frozen Tier A 六條；**不併入** Tier B 四條結構擴充
- Tier A = Pilot-02 已完成正式實驗基底（4B：79/320 → 85/320；verified rescue = 6）
- Tier B = 安全結構擴充（已實作；不得單獨稱 Aggressive Healer v1）
- 至少完成一條 Tier C 之 implementation／tests／residual census／Development evidence 後，才可命名 **Aggressive Healer v2**
- 初版 Active／Conservative Healer 只提供架構靈感，**不是**本 Tier C 規格來源
- 規則必須 **deterministic**、**answer-blind**、**evaluator-blind**、**bounded-edit**、**可 abstain**

C1 與 C2 必須分開 adjudicate：同一格不得同時套用兩條；若兩者皆看似可觸發，因「非單一規則唯一映射」而 abstain，不得混用或串接。

---

## 2. C1 specification — Explicit Domain Method Binding Repair

### 2.1 Rule ID

`TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1`

### 2.2 Allowed repair (only)

僅在下列條件全部成立時，允許一次 bounded edit：

1. **Frozen contract 明確指定唯一 Ops class／method**  
   可自 frozen prompt／system contract／API SSOT 追溯到唯一 `(OpsClass, method_name)`。
2. **Candidate 已存在局部 domain API call**  
   AST 上已有對某一 Ops class 的 method call（attribute access + call）；不得「從無到有」新增 call。
3. **錯誤 method 不符合 contract**  
   現有 attribute／method name 與 contract 指定之唯一 method 不一致。
4. **正確 method 唯一**  
   契約指定的正確 method 只有一個；不存在第二個同等合理的 method 候選。
5. **Arguments 完全原樣保留**  
   所有 positional／keyword argument expressions、分隔與順序在 AST 等價意義下不變。
6. **只修改 attribute／method name**  
   允許的唯一語法變更是將錯誤的 method attribute 名稱改為契約指定名稱；不得改 class、不得改 receiver expression（除名稱節點本身）、不得改 call 結構。

### 2.3 Prohibited (C1)

- 以**名稱相似度**單獨作為觸發或修法依據
- 新增 API call
- 重寫原生演算法或非 binding 局部之外的程式
- 修改、替換或重排 arguments
- 多候選 method（含「看起來都合理」的並列候選）
- `SYSTEM_CONTRACT_DEFECT`／`UNRESOLVED`（或同等 system contract defect／unresolved）下的任何修復

### 2.4 Edit bound

- Edit count：1（單一 attribute／method name 節點）
- Edit scope：該單一 binding site 的 method name only

---

## 3. C2 specification — Domain Signature Form Repair

### 3.1 Rule ID

`TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1`

### 3.2 Allowed repair (only)

只允許可**機械證明等價**的簽名形式修正。允許的子類型僅限：

1. **Keyword 名稱修正**  
   keyword argument 的參數名與契約簽名不符，且存在唯一正確參數名；對應 value expression 原樣保留。
2. **Positional／keyword 等價轉換**  
   在契約簽名下，同一組 argument expressions 在 positional 與 keyword 形式之間可機械證明等價；不得改變 expression 本體，亦不得藉轉換引入新值。
3. **唯一 wrapper 移除**  
   僅當 wrapper 為可機械證明的多餘包裝（例如單一多餘呼叫層且去除後簽名形式與契約等價），且去除後不改變內層 expression 語意時允許；若 wrapper 是否多餘不唯一可判定，abstain。
4. **Default／optional argument 的純形式整理**  
   僅限不改變呼叫語意的 default／optional 形式整理（例如顯式寫出與省略在契約下等價的 optional 形式，或去除與預設值機械等價的冗餘寫法）；不得插入新語意值，不得刪除必要參數。

### 3.3 Prohibited (C2)

- Argument reorder 導致語意改變（含任何依位置語意不同而改變對應關係的 reorder）
- 替換 argument expression
- 插入新值
- 刪除必要參數
- 依題意猜測變數配對
- 以名稱相似度單獨作為依據
- 新增 API call 或重寫演算法本體
- `SYSTEM_CONTRACT_DEFECT`／`UNRESOLVED` 下的任何修復

### 3.4 Edit bound

- 僅限單一局部 binding site 的簽名形式節點
- 變更必須可列舉為有限、可審計的形式變換步驟；無法機械證明等價則 abstain

---

## 4. Eligibility

規則本身**不得綁死 formal 422**。Formal 422 僅為 development supply source（見 §7），不是永久 eligibility predicate。

一格要進入 C1 或 C2 的修復候選，必須**同時**滿足下列條件；任一不滿足即 **abstain**：

| # | Requirement |
|---|---|
| E1 | Frozen prompt／system contract／API SSOT **可追溯**到本格所用契約 |
| E2 | Contract status = `SYSTEM_CONTRACT_CORRECT` |
| E3 | Expected class／method／signature **唯一** |
| E4 | Candidate 可重現且 **parseable** |
| E5 | 存在**單一**局部 binding site（唯一可識別的修法錨點） |
| E6 | **不使用**正確答案、PASS／FAIL 或 evaluator 結果決定觸發與修法（answer-blind、evaluator-blind） |
| E7 | 不存在第二個同等合理候選（含第二 method、第二簽名解釋、第二修法） |

補充：

- Eligibility 判定為**規則專屬、唯讀 AST adjudication**；不得把 compliance census 標籤直接當成「已完成唯一映射」。
- C1 與 C2 各自獨立檢查 E1–E7；通過 C1 不蘊涵通過 C2，反之亦然。
- PASS／FAIL 與 evaluator 結果僅可作為 **audit 觀測欄位**（見 §8），不得回饋進 trigger／edit 決策。

---

## 5. Exclusions

下列情形**必須排除**（abstain），不得以 C1 或 C2 修復：

| Exclusion | Rule |
|---|---|
| 完全未使用 API，但需要整段重構才能接上契約 | abstain |
| Ab2d+spec 允許 native／mixed，且 candidate 沒有 API call | abstain |
| Ops class shadowing（candidate 覆寫／遮蔽注入之 Ops class／name） | abstain |
| `AVAILABLE_NOT_EXPOSED` method | 見下方固定表述 |
| 多候選 method | abstain |
| System contract defect（`SYSTEM_CONTRACT_DEFECT`） | abstain |
| Unresolved contract（`UNRESOLVED`） | abstain |
| 核心演算法重寫 | abstain |
| Answer-aware／evaluator-aware 修復 | abstain（絕對禁止） |

### 5.1 `AVAILABLE_NOT_EXPOSED` 固定表述

> 不屬於本規則可證明的 exposed-contract binding error，因此 abstain；其 compliance 定性由獨立稽核處理。

---

## 6. Abstention

Abstention 是預設安全行為，不是失敗。

**必須 abstain 的充分條件（非穷舉，與 §4–§5 一致）：**

- 任一 eligibility 條件（E1–E7）不成立
- 命中任一 exclusion（§5）
- C1／C2 邊界不清或兩者皆可解釋
- 無法機械證明等價（C2）或無法證明唯一正確 method（C1）
- 需要答案、PASS／FAIL、evaluator 訊號才能決定是否修或怎麼修
- 修法會超出 bounded edit（新增 call、改 arguments 語意、重寫演算法等）

Abstention 時仍須寫入 audit 欄位，並填 `abstention_reason`；不得靜默跳過。

---

## 7. Development cohort

### 7.1 Role of formal 422

Formal 422 **只作 development supply source**：

- 用於規則開發期的供給池與後續（另輪）adjudication 材料
- **不是**規則永久 eligibility 條件
- **不得**寫成「僅 formal 422 可觸發」或同等永久 gate

### 7.2 Screening then adjudication

開發期篩選流程：

1. **先用 compliance census 粗篩**（供給過濾，非唯一映射判定），優先保留同時符合或明確指向下列者：
   - `SYSTEM_CONTRACT_CORRECT`
   - `NONCOMPLIANT_FAIL`
   - 或明確 API call／signature mismatch 候選
2. **再做唯讀、規則專屬 AST eligibility adjudication**（套用本文件 C1 或 C2 與 §4–§6）

### 7.3 Explicit non-claim

**不得宣稱** compliance census 已完成唯一映射判定。  
Census 只提供 development supply／粗分類；唯一 method／唯一簽名／唯一 binding site 必須由規則專屬 AST adjudication 另行證明。

---

## 8. Audit fields

每一格（cell）至少記錄下列欄位：

| Field | Requirement |
|---|---|
| `rule_id` | `TIER_B_EXPLICIT_DOMAIN_METHOD_BINDING_REPAIR_V1` 或 `TIER_B_DOMAIN_SIGNATURE_FORM_REPAIR_V1`；abstain 時仍標示嘗試之規則 |
| `risk_tier` | 固定 `Tier C` |
| `ssot_entry_id` | API SSOT／contract registry 可追溯 entry ID |
| `trigger_evidence` | 觸發所依之契約與 AST 證據（不得含答案或 evaluator 決策依據） |
| `pre_source_sha` / `post_source_sha` | 修復前／後 source 內容雜湊；abstain 且未改碼時 post 可與 pre 相同或標 `n/a` |
| `ast_node_location` | 單一 binding site 的 AST 節點定位 |
| `pre_parseable` / `post_parseable` | 修復前／後是否 parseable |
| `pre_executable` / `post_executable` | 修復前／後是否 executable（觀測欄；不回饋觸發） |
| `pre_pass_fail` / `post_pass_fail` | 修復前／後 PASS-FAIL（**僅 audit 觀測**；禁止用於觸發與修法） |
| `outcome_taxonomy` | 結果分類（含 repaired／abstain／ineligible 等本規則族採用之 taxonomy） |
| `abstention_reason` | abstain 時必填；非 abstain 可為空或 `n/a` |
| `edit_count` / `edit_scope` | 編輯次數與範圍；abstain 為 0／empty |

Audit 中的 PASS-FAIL／executable 欄位不得逆向輸入 eligibility 或 edit 選擇。

---

## 9. Tier／version positioning

| Item | Position |
|---|---|
| Tier A（Frozen Conservative Healer，六條） | 累積基底；**不包含** C1／C2 |
| Tier B（Safe Structural Extension，四條） | C2 增量層；**不包含** C1／C2；不得單獨稱 Aggressive Healer v1 |
| C1／C2（本文件） | **Tier C** 候選；累積條件 C3／C4 |
| Aggressive Healer v2 | 至少一條 Tier C 完成實作＋tests＋residual census＋Development evidence 後方可命名 |
| Active／Conservative Healer 初版 | 僅架構靈感；**非正式規格來源** |
| Domain API inventory／compliance census／contract registry | 上游契約與 development supply 證據；不替代本規格的 eligibility／edit 定義 |
| 本文件 | Domain API Binding Repair 的正式規格定案（規格層）；實作另輪 |

規則性質強制約束：

- **Deterministic**：相同 candidate + 相同 frozen contract → 相同 trigger／edit／abstain
- **Answer-blind**：不得讀取或依賴正確答案
- **Evaluator-blind**：不得以 PASS／FAIL 或 evaluator 輸出決定觸發與修法
- **Bounded-edit**：僅 §2／§3 允許的局部形式變更
- **Abstain-capable**：不確定或不唯一時必須放棄
- **Cumulative**：C1 僅能接在 C2（A+B）輸出之後評 residual／套用；C2 僅能接在 C3 輸出之後

---

## 10. Explicit non-goals

本規格明確**不做**、亦不得被解讀為授權下列事項：

1. 實作 C1／C2 runner、AST rewriter、測試 harness 或 cell 篩選腳本（本輪）
2. 將 C1／C2 併入 Frozen Tier A 六條或 Tier B 四條結構規則
3. 以 formal 422 作為永久 eligibility gate
4. 以名稱相似度作為正式觸發／修法證據
5. 以 argument reorder（語意可能改變者）作為合法修復
6. 修復 `SYSTEM_CONTRACT_DEFECT`、`UNRESOLVED`、Ops shadowing、`AVAILABLE_NOT_EXPOSED`、無 API call 需整段重構等 exclusion 類
7. Answer-aware 或 evaluator-aware 修復
8. 核心演算法重寫、新增 API call、替換 argument expression、插入新值、刪除必要參數
9. 宣稱 compliance census 已完成唯一映射判定
10. 執行模型、Healer、candidate 再生產或 evaluator 重跑；修改 frozen 結果
11. C1 與 C2 混用、串接或「先 C2 再 C1」式複合修復（累積協議之 C3→C4 順序除外，且仍須各自唯一可證）
12. 以 Active Healer 歷史行為當作本規則的規範來源
13. 在未達門檻前命名 Aggressive Healer v2
14. 批次 rename `rule_id`

---

## Document control

| Field | Value |
|---|---|
| Document | `docs/experiments/design/math16_aggressive_healer_domain_api_binding_spec_v1.md`（歷史檔名；內容 = Tier C） |
| Kind | Tier C specification only |
| Layering protocol | `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md` |
| Implementation | Out of scope this round |
| Commit／push | Not authorized by this authoring task |
