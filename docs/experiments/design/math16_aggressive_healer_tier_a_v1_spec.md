# Math16 Tier B — Safe Structural Extension Spec v1

> **status:** `specification_repositioned_as_tier_b_safe_structural_extension`
> **spec_version:** `v1`
> **risk_tier:** `Tier B`（Safe Structural Extension）
> **product_role:** Cumulative stack layer after Frozen Conservative Healer（Tier A）；**不是**獨立 Aggressive Healer v1
> **layering_protocol:** `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md`
> **HEAD_at_authoring:** `f0eae63fe8c3760e9912589654657510119175ce`
> **origin/main_at_authoring:** `f0eae63fe8c3760e9912589654657510119175ce`

> **Naming correction:** 本檔歷史檔名含 `tier_a`；依累積分層協議，本四條規則正式定位為 **Tier B**。檔名與部分 `rule_id` 字串暫不 rename。  
> 現行 Tier 歸屬以 `math16_cumulative_healer_layering_protocol_v1.md` 與 mapping manifest 為準；rule_id 為歷史識別碼。  
> **Note:** HEAD SHAs are authoring provenance only; they are not eligibility predicates.

**Tier A（對照）：** Pilot-02 已凍結六條保守規則（`L1_*`／`L2_*` allowlist）為累積基底；本文件**不**修改 Tier A。

本規格描述 Tier B 四條安全結構擴充。Tier C（Domain API Binding／原文件 Tier B 候選）見 companion 規格。

---

## 1. Scope

**Tier B（Safe Structural Extension）** 包含以下四條規則（不新增第五條、不混入 Tier C；亦不取代 Tier A 六條）：

| # | Category | Rule ID（保留既有 ID，不 rename） |
|---|---|---|
| B1 | 全形／中文程式符號正規化 | `core.normalize_fullwidth_python_punctuation` |
| B2 | 單一且唯一可判定的缺失 delimiter 修復 | `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` |
| B3 | empty suite 補入 `pass` | `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` |
| B4 | 唯一且可證明的 import／binding 修復 | `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` |

### Status snapshot

- 已實作：`agent_tools/finals_rebuild/aggressive_healer_tier_a/`（目錄名歷史）
- Focused tests：**44 passed**
- Formal 960 **Tier B supply census**（raw）：eligible **0／0／9／0**
- 必須在 **Tier A（C1）輸出之後**量測 residual supply；raw census 不得代替 residual
- **不**單獨命名為 Aggressive Healer v1

### Rule ID provenance

| Rule ID | Provenance decision |
|---|---|
| `core.normalize_fullwidth_python_punctuation` | **沿用**既有 Minimal Core 正式身份（見 `core_adapter.py` 與 safe-historical governance）。禁止另立同義 ID。 |
| `TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1` | 歷史 ID 字串含 `TIER_A_`；**現行 risk tier = Tier B**。不得挪用 Frozen Tier A 的 `L1_CLOSE_*` ID。暫不 rename。 |
| `TIER_A_EMPTY_SUITE_INSERT_PASS_V1` | 同上；現行 **Tier B**。草稿 `L1_COMMENT_ONLY_IF_INSERT_PASS` 不得冒充本規則。 |
| `TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1` | 同上；現行 **Tier B**。歷史 Regex／AST 猜測性 import 注入不是本規則。 |

**明確排除於本文件：** Tier C Domain API Binding（C1／C2）、修改 Tier A 六條、legacy aggressive heuristics。

---

## 2. Shared invariants

四條規則共同遵守：

| Invariant | Requirement |
|---|---|
| Deterministic | 相同 candidate + 相同契約／上下文 → 相同 trigger／edit／abstain |
| Answer-blind | 不得讀取或依賴正確答案 |
| Evaluator-blind | 不得以 PASS／FAIL 或 evaluator 輸出決定觸發、修法或接受修改 |
| Bounded-edit | 僅允許該規則定義的局部、可列舉變更 |
| Single-local-repair | 每次觸發只修單一局部 site（B1 的正規化除外：一次掃描內對所有合規全形符號做同一映射，仍視為單一 normalization pass） |
| Ambiguity → abstain | 非唯一可判定則放棄 |
| No core-algorithm rewrite | 不得改寫解題／演算法本體、控制流語意或運算順序 |
| No answer／score feedback | Audit 可記錄 PASS-FAIL 觀測，但禁止回饋進決策 |

---

## 3. Rule 1–4 specifications

> 節內標題 B1–B4 為 **Tier B** 內部序號；與 Tier C 的 C1／C2 不同。

### 3.1 B1 — Fullwidth／Chinese program-symbol normalization

#### rule_id

`core.normalize_fullwidth_python_punctuation`

#### trigger

Candidate 原始碼中，在 **Python syntax position**（非字串、非註解、非 docstring、非 f-string text segment）出現已核准映射表內的全形標點。

核准映射（與既有 Core 規則一致，不得本輪擴充）：

| Fullwidth | ASCII |
|---|---|
| `，` | `,` |
| `：` | `:` |
| `；` | `;` |
| `（` | `(` |
| `）` | `)` |
| `［` | `[` |
| `］` | `]` |
| `｛` | `{` |
| `｝` | `}` |

#### eligibility

- 輸入為可 tokenize 的 candidate 文字（tokenize失敗 → abstain／no-op，fail-closed 回傳原文）
- 至少一處 unprotected mapped character
- 正規化後 `ast.parse` 成功；否則 fail-closed 回傳原文（視為未套用）

#### transformation

將所有 syntax-position 的核准全形標點替換為對應 ASCII；不碰 protected spans。

#### abstention guards

- tokenize 失敗
- 無 unprotected mapped character
- 正規化後無法 parse
- 企圖映射表外符號（例如全形運算子）→ 不擴充、不猜測；若僅有表外符號則不觸發

#### edit boundary

- 僅字元替換（表內 9 種）；不得改 identifier 語意、不得改字串／註解內容、不得插入／刪除語句

#### preconditions

- Candidate 字串非空（空字串 → no-op）
- 不依賴答案／evaluator

#### postconditions

- 若套用成功：輸出可 `ast.parse`；所有 syntax-position 表內全形已轉 ASCII
- 若未套用：byte-identical 原文

#### idempotence

對已正規化輸出再跑一次 → 零變更。

#### audit fields

見 §7；本規則另記 `mapped_char_count`、`protected_span_policy=tokenize_mask`。

#### focused test requirements

- 語法位置全形 → ASCII
- 字串／註解／docstring 內全形不變
- tokenize／parse fail-closed
- 二次套用 idempotent
- 不得改表外全形運算子

#### explicit non-goals

- 不正規化全形運算子／識別字內非常規字元（超出核准表）
- 不修 delimiter 失衡、empty suite、import（屬 B2–B4）
- 不另立第二個 fullwidth rule_id

---

### 3.2 B2 — Unique missing-delimiter repair

#### rule_id

`TIER_A_UNIQUE_MISSING_DELIMITER_REPAIR_V1`

#### trigger

Candidate **無法** `ast.parse`，且 SyntaxError 形態可歸因為 **單一缺失的閉合 delimiter**（`()`／`[]`／`{}` 之一），並且存在**唯一**可證明的插入位置與插入字元，使得一次插入後 parse 成功。

#### eligibility

- `ast.parse` 失敗且具可用 lineno（或等價唯一錯誤錨點）
- 錯誤可機械歸類為 unbalanced／unclosed delimiter
- 在允許的編輯空間內，**恰好一個** (location, delimiter_char) 使 trial parse 成功
- 對所有其他合理候選位置／字元的 trial **皆**失敗（唯一性證明）
- 不使用答案或 evaluator 結果

#### transformation

在唯一證明的位置插入唯一缺失的閉合 delimiter 字元；不得改其他字元、不得刪行、不得重排運算式。

#### abstention guards

- 已可 parse
- 錯誤非 delimiter 類
- 多個位置／多種字元皆能使 parse 成功
- 需刪除字元、需一次插入多個 delimiter、或需改非 delimiter 內容
- 字串／註解內的「看起來失衡」無法與 code 區分時
- 需依賴答案／PASS-FAIL 才能選擇修法

#### edit boundary

- Edit count：1（單一字元插入）
- Scope：唯一 delimiter site only

#### preconditions

- Parse failure present
- Unique-repair proof completed before mutate

#### postconditions

- 套用後 `ast.parse` 成功
- 除此之外原始碼其餘內容不變（相對該次插入）

#### idempotence

套用後已 parse → 本規則不再觸發；再跑一次零變更。

#### audit fields

見 §7；另記 `delimiter_char`、`insert_location`、`uniqueness_proof=true`。

#### focused test requirements

- 唯一缺失 `)`／`]`／`}` 各至少一例正向
- 兩處皆可修 → 必須 abstain
- 非 delimiter SyntaxError → abstain
- 不刪行、不改運算式本體
- 二次套用 idempotent

#### explicit non-goals

- 不涵蓋「刪除多餘 delimiter」除非未來另開規則（本 v1 **不做**）
- 不涵蓋字串未閉合的任意猜測配對
- 不借用 Active Healer `L1_*` rule_id
- 不做反覆刪 SyntaxError 行

---

### 3.3 B3 — Empty-suite insert `pass`

#### rule_id

`TIER_A_EMPTY_SUITE_INSERT_PASS_V1`

#### trigger

Candidate 因 **empty suite**（例如 `expected an indented block` 類 IndentationError／SyntaxError）無法 parse，且存在**唯一**可判定的 compound 語句頭（`if`／`elif`／`else`／`for`／`while`／`try`／`except`／`finally`／`with`／`def`／`class` 等需 suite 者），其 suite 為空（僅空白與／或僅註解、無執行敘述），插入單一 `pass` 後 parse 成功。

#### eligibility

- Parse failure 可歸因為 empty suite
- 空 suite site **唯一**
- Suite 內無非註解執行碼
- Trial：於正確縮排插入一行 `pass` 後 parse 成功
- 其他 site 的 trial 不得同樣「修好」（唯一性）

#### transformation

在唯一空 suite 內插入一行適當縮排的 `pass`；不刪既有註解，不改 suite 外程式。

#### abstention guards

- 已可 parse
- 多個空 suite
- 空區塊其實含未辨識執行碼
- 插入 `pass` 後仍不可 parse
- 需改縮排結構、刪行、或補非 `pass` 敘述才能 parse
- 與「註解-only if」草稿規則範圍混淆但無法唯一判定時 → abstain

#### edit boundary

- Edit count：1（插入一行 `pass`）
- Scope：單一 empty suite

#### preconditions

- Empty-suite parse failure
- Unique site + successful trial parse

#### postconditions

- 套用後 `ast.parse` 成功
- 僅新增該 `pass` 行

#### idempotence

套用後 suite 非空 → 不再觸發；再跑零變更。

#### audit fields

見 §7；另記 `suite_owner_kind`、`insert_lineno`、`suite_indent`。

#### focused test requirements

- `if`／`for`／`while`／`def` 空 suite 正向（唯一 site）
- 雙空 suite → abstain
- 僅註解的空 suite → 可修且保留註解
- 不刪行、不改條件／迴圈條件表達式
- idempotent

#### explicit non-goals

- 不把 paused `L1_COMMENT_ONLY_IF_INSERT_PASS` 改名為本規則
- 不插入 `return`／預設值／其它猜測敘述
- 不修復一般縮排錯亂（非 empty suite）

---

### 3.4 B4 — Unique import／binding repair

#### rule_id

`TIER_A_UNIQUE_IMPORT_BINDING_REPAIR_V1`

#### trigger

Candidate **可 parse**（或經 B1–B3 後可 parse），存在**靜態可證明**的單一缺失 binding：某一 Name／屬性使用所需的 **唯一** import 或綁定語句缺失，且正確 import／binding 形式由凍結契約或標準庫／已注入 runtime 命名空間的**唯一允許寫法**決定。

#### eligibility

- 缺失符號與所需 binding 之間存在**唯一**可追溯映射（例如標準庫 `from fractions import Fraction`，或 Math16 runtime 已注入、契約允許的唯一 import 形式）
- Candidate 未本地定義該名；亦未已有等價 import
- 僅一個符號缺口對應僅一種合法補法
- **不得**以 NameError 執行結果、PASS／FAIL 或答案作為觸發依據（靜態證明優先；執行錯誤僅可作 audit 觀測）
- 非 Ops class shadowing；非 domain method 猜測；非 Tier C binding repair

#### transformation

在檔案頂部（或契約指定的唯一合法位置）插入**唯一** import／binding 語句；不改其它語句、不改呼叫 arguments、不改 method 名。

#### abstention guards

- 多個可能 import 來源或多種等價寫法無法唯一選定
- 符號可能是本地漏定義的變數／參數（非 import 可證）
- Ops class shadowing
- Domain method／API binding 猜測（屬 Tier C 或排除）
- 需注入猜測性預設值或改參數
- 多符號同時缺失且無法拆成單一唯一修復
- 依賴 evaluator／答案決定補哪一個

#### edit boundary

- Edit count：1（單一 import／binding 語句插入）
- Scope：binding header only

#### preconditions

- 靜態唯一映射成立
- 插入位置唯一且不破壞既有結構

#### postconditions

- 套用後仍可 parse
- 目標名成為合法 binding；其餘程式不變

#### idempotence

已存在等價 binding → 不觸發；再跑零變更。

#### audit fields

見 §7；另記 `missing_name`、`binding_stmt`、`ssot_or_stdlib_evidence_id`。

#### focused test requirements

- 唯一標準庫 import 缺失 → 插入成功
- 兩種合法 import 寫法並列 → abstain
- 本地已定義 → 不插入
- 不觸發 domain method rename（Tier C／C1）
- 不因 PASS／FAIL 而接受／拒絕

#### explicit non-goals

- 不做歷史 RegexHealer 式大量依賴猜測注入
- 不做 `while True` 有限化、刪 SyntaxError 行、LLM 深層修復
- 不做 Tier C domain API method／signature repair
- 不修復 Ops class shadowing

---

## 4. Rule order

定案**唯一**管線順序（單向、禁止循環反覆修補）：

```text
B1 Normalization
  → B2 Delimiter repair
  → B3 Empty-suite repair
  → B4 Unique import／binding repair
  → final parse／idempotence check
```

### Order rationale

| Step | Why this position |
|---|---|
| B1 first | 全形標點會污染 tokenize／SyntaxError 定位；與既有 Core／safe-historical「先正規化」一致。 |
| B2 before B3 | Delimiter 失衡常使 suite 結構無法可靠判定；先唯一閉合再判 empty suite。 |
| B3 before B4 | Import 規則要求（或偏好）可 parse 的靜態結構；empty suite 先解除 parse blocker。 |
| B4 last among repairs | Binding 修復假設語法樹可建立。 |
| Final check | 驗證 parse 與整管線二次套用零變更。 |

### Evidence note on alternate orders

**Frozen Tier A** allowlist 順序（`L1_CLOSE_UNBALANCED_PARENTHESIS` → `L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED` → `L1_PROSE_RESIDUE_NARROW` → L2…）屬累積堆疊之 **C1 基底層**，與本 Tier B 管線不同；**不構成本 Tier B 四條內部改序依據**。  
在累積實驗中，Tier B 僅應作用於 **C1（Tier A）輸出**，不得與 Tier A 平行替代。  
未發現要求「empty suite 先於 delimiter」或「import 先於 normalization」的 Tier B 正式證據；故採上表順序。

### Per-rule firing

- 每條規則對每格**最多觸發一次**（成功套用或明確 abstain／skip 後不得在同格同管線內重入該規則）
- 禁止「修到能 parse 為止」的迴圈式刪行／重試

---

## 5. Global abstention

任一情況成立，該規則 abstain；若導致無法安全繼續且無後續規則可靜態適用，則 cell 層 outcome 為 abstain／unrepaired（不得強改）：

- 觸發條件或唯一性證明失敗
- 需修改核心演算法、運算順序、參數值
- 反覆刪除 SyntaxError 行才能前進
- `while True` 強制有限化
- 注入猜測性預設值
- Domain method 猜測或 Tier C binding repair
- Ops class shadowing
- 多候選 import／binding
- LLM／模型深層修復
- 根據 PASS／FAIL 選擇或接受修改
- Ambiguous delimiter 或多空 suite
- Final idempotence check 失敗（二次管線仍產生 diff）→ 整次 repair **作廢回滾**並標 `NON_IDEMPOTENT_ABORT`

---

## 6. Edit budget

| Budget item | Limit |
|---|---|
| Rules in Tier B package | 4（B1–B4 only） |
| Pipeline passes | **1** 正向 pass + **1** idempotence 驗證 pass（驗證 pass 必須零 diff） |
| Per-rule fires per cell | ≤ 1 |
| Max successful edits per cell | ≤ **4**（每規則至多 1 次成功 mutation） |
| Max chars／lines per edit | 依各規則 edit boundary（B1：表內字元替換；B2：1 char；B3：1 line `pass`；B4：1 import／binding stmt） |
| Retries on failure | **0**（失敗即 abstain，不循環） |
| Cross-rule re-entry loops | **Forbidden** |

超過 budget 或違反單次觸發 → abort／abstain，不得繼續修補。

---

## 7. Audit schema

每格至少記錄：

| Field | Notes |
|---|---|
| `rule_id` | 當步規則；管線摘要可含 `rules_fired[]` |
| `risk_tier` | `Tier B` |
| `sequence_index` | 管線中順序 1..4 |
| `triggered` / `applied` / `abstained` | 布林 |
| `trigger_evidence` | 靜態證據；不得含答案導向理由 |
| `abstention_reason` | abstain 時必填 |
| `pre_source_sha` / `post_source_sha` | |
| `edit_count` / `edit_scope` | |
| `ast_node_location` 或等價定位 | B1 可記 span 列表摘要 |
| `pre_parseable` / `post_parseable` | |
| `pre_executable` / `post_executable` | **觀測 only** |
| `pre_pass_fail` / `post_pass_fail` | **觀測 only；禁回饋決策** |
| `outcome_taxonomy` | repaired／partial_syntax_repair／abstain／non_idempotent_abort 等 |
| `pipeline_idempotent` | final check 結果 |

---

## 8. Development／Validation／Confirmatory governance

本文件只定案治理條件，**本輪不選 cell、不跑實驗**。

### 8.1 Development eligibility

- 僅得使用事先標記的 **Development** 供給池
- 規則觸發與修法必須滿足本規格 eligibility／guards
- Development 觀察**不得**寫入 Validation／Confirmatory 結論

### 8.2 Validation freeze 條件

進入 Validation 前必須同時成立：

1. 本 Tier B 規格已定案且 rule_id／order／budget 未再改動
2. 實作通過 focused tests（§3 各條；已達 44 passed）
3. Development 上的規則行為與規格一致（另輪記錄；且須含 **residual-after-Tier-A**）
4. 宣告 `VALIDATION_FREEZE`：此後至 Confirmatory 結束前**不得修改規則語意、順序、budget、guards**

### 8.3 Confirmatory 前不得修改規則

- Validation 開始後 → Confirmatory 結束前：禁止改 rule 邏輯與本規格
- 若發現缺陷：只能 **abstain／標記失效**，另開版本（v1.1+），不得暗改 v1

### 8.4 資料不得混用

| Split | Rule |
|---|---|
| Development | 只供規則成形與除錯 |
| Validation | 只供凍結後驗證；不得回寫改規則 |
| Confirmatory | 只供最終確認；不得與 Dev／Val 混池或重訓式改規則 |

三池 cell 身份不得重疊使用於會影響規則定義的決策。

---

## 9. Excluded legacy mechanisms

下列機制**明確排除**於 Tier B Safe Structural Extension（歷史可參考，不可啟用）：

| Excluded mechanism | Reason |
|---|---|
| 反覆刪除 SyntaxError 行 | 非唯一局部、非可證語意安全 |
| `while True` 強制有限化 | 改變控制流語意（Core registry 亦標記 deferred／unsafe for this product） |
| 注入猜測性預設值／`input()`→常數等 | 猜測性語意改寫 |
| 參數值／運算順序猜測 | 非 answer-blind 可證 |
| Domain method 猜測；Tier C C1／C2 | 非本層範圍 |
| Ops class shadowing「修復」 | 超出唯一 binding 可證範圍 |
| 多候選 import／binding 任選 | 違反 uniqueness |
| LLM／模型深層修復 | 非 deterministic |
| 依 PASS／FAIL 選擇或接受修改 | evaluator-aware 禁止 |
| 修改或重跑 Frozen Tier A 六條 | 屬累積基底，本層不得更動 |
| 將本層單獨稱為 Aggressive Healer v1 | 違反命名協議 |
| Legacy Regex／AST Healer 全家桶 | 含大量非 Tier B 行為 |

---

## 10. Freeze criteria

Tier B Safe Structural Extension 規格定位凍結當且僅當：

1. **Exactly four** Tier B structural rules，ID 如 §1 表；無第五條、無 Tier C
2. Rule order 如 §4，單一方向，無循環修補
3. Global edit budget 如 §6
4. 每條含完整 trigger／eligibility／transformation／guards／boundary／pre／post／idempotence／audit／tests／non-goals
5. 共用 invariants（§2）與 exclusions（§5／§9）寫入
6. Development／Validation／Confirmatory 不得混用；Confirmatory 前不得改規則
7. B1 沿用 `core.normalize_fullwidth_python_punctuation`，無重複 fullwidth ID
8. 明確從屬於累積堆疊 **C2 = Tier A + Tier B**；不單獨稱 Aggressive Healer v1
9. Residual eligibility 必須在 Tier A 輸出上另測（raw 960 census 不足替代）

凍結後變更必須升版；不得靜默改 v1。

---

## Document control

| Field | Value |
|---|---|
| Document | `docs/experiments/design/math16_aggressive_healer_tier_a_v1_spec.md`（歷史檔名；內容 = Tier B） |
| Kind | Tier B specification |
| Tier A base | Frozen six-rule Pilot-02 allowlist（不在本檔修改） |
| Tier C companion | `docs/experiments/design/math16_aggressive_healer_domain_api_binding_spec_v1.md` |
| Layering protocol | `docs/experiments/design/math16_cumulative_healer_layering_protocol_v1.md` |
| Implementation this round | Out of scope（實作已存在；本輪只改文件定位） |
| Commit／push | Not authorized by this authoring task |
