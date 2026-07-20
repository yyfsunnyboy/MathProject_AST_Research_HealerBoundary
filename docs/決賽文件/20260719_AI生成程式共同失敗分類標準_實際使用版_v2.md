# AI 生成程式共同失敗分類標準（實際使用版 v2）

> 適用：CE115（Math16）、MBPP+、HumanEval+ 與後續資料集
> 目的：讓不同研究小組以相同口徑標記失敗，最後能合併分析。
> 原則：只保留已實際使用或已被實戰教訓驗證為必要的分類，不新增尚未驗證的複雜細項。
> v2 變更摘要：新增 outcome_validity 維度（區分模型錯誤與評測方錯誤）、補齊 L3 判定式、
> 明定 canonical form 歸屬與語意等價比對原則、明確區分「症狀分類」與「責任歸因」、
> 補充必填欄位（prompt_hash、evaluator_hash）與評測方錯誤的平反（revision）流程。

---

## 1. 核心判定原則

每個 cell 都記錄三件彼此獨立的事：

1. **最後是否通過**（final_status）
2. **若未通過，最早在哪一層出現可觀察的失敗**（primary_failure_layer，L0–L5）——這是**症狀位置**
3. **這格結果能不能算在模型頭上**（outcome_validity）——這是**責任歸因**

### 1.1 症狀（layer）與責任（validity）是兩個正交的維度

- **L0–L5 回答「失敗最早出現在哪裡」**：語法錯誤先標 L1；能執行但格式錯標 L2；格式正確但答案錯才標 L5。
- **outcome_validity 回答「這是誰的錯」**：同一個 L5 症狀，可能是模型真的算錯（VALID_MODEL_OUTCOME），
  也可能是 evaluator 用字串全等比對冤枉了正確答案（INVALID_EVALUATOR）。
- 兩者**不得混用**：layer 永遠記症狀，validity 永遠記歸因。細部機制另以 mechanism_tags 補充。

> 實戰依據（CE115）：三格「6x + 24」vs「6x+24」的評分冤案，症狀是 G4 FAIL（L5），
> 但責任在評測方；若無 validity 維度，這三格會被灌進模型失敗率，且事後平反無處記錄。

### 1.2 採用「最早可觀察失敗層」

主分類以最早出現的可觀察失敗為準；後續因修復而暴露的更深層問題記入 failure_chain（見第 6 節）。

---

## 2. 正式通過標準 G1–G4（＋G3c 子項）

| Gate | 名稱 | 判定內容 |
|---|---|---|
| G1 | Parse | Python 能否解析並建立 AST |
| G2 | Execution | 程式能否正常執行且不發生例外 |
| G3 | Contract | 函式介面、回傳型別、答案 schema 與 **canonical form** 是否符合契約 |
| G4 | Correctness | 是否通過 oracle、單元測試或 benchmark tests |

只有 G1–G4 全部 PASS 才算 `PASSED`。

### 2.1 G3c：canonical form 檢查的明文規則

- 答案的標準呈現形式（如 canonical LaTeX、正規化字串）屬 **G3 契約範疇**，失敗歸 **L2**，不歸 L5。
- **禁止以字串全等作為 canonical form 的判定方式**。必須先做語意等價正規化
  （空白、等價排版、可交換順序、型別包裝），結構正確者不得因呈現差異被否決；
  結構或數值錯誤者（如 radicand 錯、係數錯）仍判 FAIL，不得因正規化被誤放行。
- 各資料集若無 canonical form 要求（如 HumanEval+ 以測試通過為準），G3c 標 `NOT_APPLICABLE`。

> 實戰依據（CE115）：LaTeX 字串全等比對造成三輪反覆平反；語意等價正規化上線後，
> 「結構對、排版不同」不再誤殺，「\\sqrt{(3,15)}」等真錯誤仍被正確拒絕。

### 2.2 G3a：required API adoption（補齊 L3 的隱形 gate）

- 若任務**事前**標定 required API，未採用即 G3a FAIL，主分類 L3——
  即使 G1、G2、G4 全部 PASS，final_status 仍為 FAILED。
- 未事前標定 required 的 API，其未採用**不得**事後判為失敗。
- G3a 不適用的資料集（無 required API 設計）標 `NOT_APPLICABLE`。

---

## 3. outcome_validity：結果有效性標記（v2 新增，必填）

| 值 | 定義 | 計入模型統計？ |
|---|---|---|
| `VALID_MODEL_OUTCOME` | 失敗（或成功）可歸因於模型自身行為 | ✅ |
| `INVALID_EVALUATOR` | evaluator / oracle 比對邏輯錯誤造成的誤判（含冤案與誤放） | ❌，需平反或重評 |
| `INVALID_CONTRACT` | 評測方的 prompt、API 文件、型別介面或 schema 設計錯誤，誘發或直接造成失敗 | ❌，需修契約後另行驗證 |
| `INVALID_INFRASTRUCTURE` | 執行環境、序列化通道、runner 等系統層問題 | ❌ |
| `PENDING_REVIEW` | 證據不足，待人工裁決 | 暫不計入，須於合併分析前清零 |

### 3.1 平反（revision）流程

evaluator 或契約修正後，對受影響 cells 以**原始 first-attempt raw response 離線重評**
（model_calls = 0），結果寫入新的 `evaluation_revision_NNN`：

- 原始 artifact 與原始判定**永不改寫**；修正僅能「平反誤判」，不得放寬真實錯誤。
- 每次 revision 必附：修正的測試佐證、新舊 evaluator hash、受影響 cell 清單、翻正前後對照。
- 若修正涉及 prompt 內容（契約層），受影響 cells 的驗證需重新呼叫模型，
  以新 run_id 獨立記錄並標 `post_hoc_validation`，**不得自動併入既有 revision**。

> 實戰依據（CE115）：三輪 evaluator 修正（37→40/48）全程遵循此流程；
> 契約修正後的 16 格重跑以 post_hoc 標記獨立保存，未污染 confirmatory 統計。

---

## 4. 共同失敗層級 L0–L5

### L0：Infrastructure Failure

模型生成或評測流程沒有完成，尚不能判斷程式能力。

包含：模型 API／Ollama timeout、模型呼叫失敗、runner 中斷、raw response 不存在、系統資源或寫檔錯誤。

規則：

- 保留在 ITT 分母；可從 valid-response 分母排除。
- 不歸因為模型程式能力；outcome_validity 標 `INVALID_INFRASTRUCTURE`。
- 不送入 Healer。
- API 層可重試（timeout、rate limit、transient 5xx；上限與 backoff 依各專案 runner 政策），
  重試屬同一 cell 而非新 seed，全部 attempt metadata 必須保存；重試耗盡才標 L0。

---

### L1：Parse / Syntax Failure

模型已有輸出，但 Python 無法解析。

包含：`SyntaxError`、`IndentationError`、括號／字串未關閉、非法條件運算式、程式截斷、
Markdown／自然語言污染、`ast.parse()` 失敗。

判定：

```text
G1 FAIL
G2–G4 NOT_ASSESSED
```

專案例：Qwen 114-02 Ab2d 的非法 ternary；CE115 q11@Ab1 的 f-string 多餘「}」。

---

### L2：Schema / Contract / Packaging Failure

程式可以解析並執行，但輸出格式不符合契約。

包含：應回傳 dict 卻回傳 scalar／string、缺少必要 key、多包或少包一層、
`correct_answer` 型別錯誤、nested schema 錯誤、dict 被 `json.dumps()` 包成字串、
函式介面不符、**canonical form 不符（G3c，經語意等價正規化後仍不符者）**。

判定：

```text
G1 PASS
G2 PASS
G3 FAIL
G4 NOT_ASSESSED
```

- 這通常是 deterministic Healer 最適合處理的區域（內容正確、僅包裝錯誤）。
- 注意 validity：若 schema 要求本身在 prompt 中未明確定義或自相矛盾，
  標 `INVALID_CONTRACT` 而非算在模型頭上。

專案例（模型原生 L2 的實證錨點）：CE115 q02——餘式正確算得 4x，
三條件加重跑共 4 次觀測全部交出裸字串而非規定欄位；prompt 已明文要求欄位，
故 validity 為 `VALID_MODEL_OUTCOME`。此類「內容對、包裝錯、穩定重現」
正是 Healer 正當職權的定義性案例。

---

### L3：Domain API / Tool-Use Failure

程式對提供的 Domain API 或工具契約使用錯誤。

包含：漏 import、API 名稱錯誤、arity／型別錯誤、非法 input grammar、
required API 未使用（G3a）、選錯工具、本地重寫同名 API、partial adoption、
**臆測不存在的回傳形狀（return-shape hallucination）**。

判定（v2 補齊，依症狀出現位置分三型）：

```text
型一（誤用致崩潰）：G1 PASS, G2 FAIL, G3–G4 NOT_ASSESSED
  ——與 L4 同為 G2 FAIL，以 mechanism 區分：例外直接源自 API 呼叫點者標 L3。
型二（誤用但可執行）：G1 PASS, G2 PASS, 於 G3／G4 顯現
  ——依最早可觀察 gate 標記，mechanism 註明 API 誤用。
型三（required API 未採用）：G3a FAIL（其餘 gate 可全 PASS）
```

常用 mechanism：

```text
invalid_api_call
missing_import
tool_routing_failure
local_api_shadowing
partial_adoption
return_shape_hallucination
```

**validity 判定原則（v2 新增，實戰教訓）**：

- API 文件描述與 runtime 實際行為不一致而誘發的誤用 → `INVALID_CONTRACT`
  ＋ mechanism `prompt_api_mismatch`。修正文件後另行驗證，原格判定永不改寫。
- 文件正確而模型仍臆測錯誤用法 → `VALID_MODEL_OUTCOME`。
- 判定前**必須**核對該 API 在 prompt 中的實際描述與程式實際簽名，不得僅憑症狀推定。

> 實戰依據（CE115）：factor_quadratic_exact 文件寫「returns: tuple of exact linear
> factors / roots」（模糊），模型幻覺 3-tuple 解包而崩潰——文件精確化後同型錯誤消失，
> 證明原格屬 `INVALID_CONTRACT`。防範機制：API 文件由程式碼單一事實來源（SSOT）
> 自動生成，並於 preflight 以機器驗證 prompt 描述與 runtime 簽名一致。

---

### L4：Runtime / Assembly / Data-Flow Failure

程式可解析，但執行時因變數、資料流、控制流程或組裝錯誤而失敗。

包含：`KeyError`、`NameError`、`TypeError`、`IndexError`、`RecursionError`、
無限迴圈、模型程式執行逾時、`kwargs`／`frozen` 接線錯誤、參數來源錯誤、
變數未定義、錯誤資料結構取值、code bloat 導致 runtime 問題。

判定：

```text
G1 PASS
G2 FAIL
G3–G4 NOT_ASSESSED
```

- 與 L3 型一同為 G2 FAIL：例外源自模型自身資料流／組裝者標 L4，
  源自 API 呼叫點者標 L3，無法區分時標 `needs_human_review`。
- **validity 注意**：例外若源自評測方的序列化通道或型別介面
  （模型輸出合理、系統接不住），標 `INVALID_INFRASTRUCTURE` 或 `INVALID_CONTRACT`。

專案例：113-10 從空 `kwargs` 讀 frozen data 造成 `KeyError`（VALID_MODEL_OUTCOME）；
CE115 q10 模型依文件回傳 Fraction、系統 JSON 通道僅收 int 而崩潰（INVALID_CONTRACT，
修正型別轉接層後以原 first-attempt 離線重評為 PASSED）。

---

### L5：Answer Incorrect / Semantic Failure

程式能解析、能執行、格式也正確，但答案或演算法錯誤。

包含：數學公式錯誤、演算法錯誤、邊界條件漏處理、硬編碼錯誤答案、模式匹配錯誤、
HumanEval+／MBPP+ tests 未通過、oracle 判定不等價、
**目標偏移（正確解出中間結果後自行改答他物）**、**參數語義錯置（如 c、d 互換）**。

判定：

```text
G1 PASS
G2 PASS
G3 PASS
G4 FAIL
```

- **G4 FAIL 前必須先排除**：L2 包裝／schema 問題、以及 evaluator 比對邏輯問題
  （後者標 `INVALID_EVALUATOR`，不入 L5 模型統計）。
- L5 是 deterministic Healer 的**外邊界**：修復需要重新解題或重建模型意圖，
  任何「修復」等同竄改模型真實能力數據——L5 一律不送 Healer。
- 實測特性（CE115）：L5 錯誤呈隨機變異（同題同 prompt 時對時錯），
  且不受格式規範或工具引導等 prompt 層注入影響；
  已知的有效方向是上游任務契約的事前明確化（降低發生率），而非事後修復。

---

## 5. 輔助機制標籤

| 標籤 | 意義 |
|---|---|
| `prompt_api_mismatch` | prompt 中 API 描述與 production API 實際行為不一致 |
| `model_assembly_failure` | 模型無法正確組裝程式 |
| `tool_routing_failure` | 選錯、漏用或重寫工具 |
| `return_shape_hallucination` | 臆測不存在的 API 回傳形狀 |
| `code_bloat` | 程式異常膨脹 |
| `infrastructure_failure` | 系統或模型呼叫問題 |
| `output_packaging` | 答案包裝／格式問題 |
| `semantic_goal_drift` | 目標偏移：解對中間結果後自行改答他物 |
| `parameter_semantics_swap` | 參數語義錯置（變數對應交換） |
| `answer_leak` | 題面或程式直接暴露答案 |
| `needs_human_review` | 證據不足，需人工裁決 |

範例：

```json
{
  "primary_failure_layer": "L3",
  "outcome_validity": "INVALID_CONTRACT",
  "mechanism_tags": ["prompt_api_mismatch", "return_shape_hallucination"]
}
```

---

## 6. 多層錯誤（failure chain）

一個 cell 可能有多層錯誤。例如 113-10：

1. 原始程式先發生 L4 `KeyError`
2. 第一條規則修復後，暴露 L2 `json.dumps` 包裝錯誤
3. 第二條規則修復後 PASS

記錄：

```json
{
  "initial_failure_layer": "L4",
  "failure_chain": ["L4_WRONG_PARAMETER_SOURCE", "L2_JSON_DUMPS_WRAPPER"],
  "final_status": "PASSED"
}
```

- 原始 cell 的主分類仍是最早出現的 L4。
- **系統修正也適用同一原則**（實戰觀察）：消除一層系統缺陷後，同格常暴露更深一層的
  模型原生問題（如：契約崩潰修正後轉為 L2 組裝錯誤）。failure chain 應記錄此型態轉變，
  型態轉變本身即為「修正對其目標層有效」的證據，不因該格仍未 PASS 而否定修正。

---

## 7. Healer 搭配規範

### 7.1 Healer 的職權邊界（v2 明文化）

| 層 | 送 Healer？ | 理由 |
|---|---|---|
| L0 | ❌ | 非模型錯誤 |
| L1 | ⚠️ 限定 | 僅限機械性語法修復（如截斷補全）；重寫邏輯即越權 |
| L2 | ✅ 主戰場 | 內容正確、僅包裝錯誤；deterministic 規則最適區 |
| L3 | ⚠️ 限定 | 僅 validity = VALID_MODEL_OUTCOME 者；INVALID_CONTRACT 一律先修契約，不送 Healer |
| L4 | ⚠️ 限定 | 僅機械性接線錯誤；涉及解題邏輯即越權 |
| L5 | ❌ | 修復＝竄改模型能力數據 |

**核心原則（實戰推導）**：可自動修復的失敗多數源自評測系統自身缺陷；
Healer 的高觸發率是系統成熟度的**反向指標**。Healer 的正確定位是暫時性缺陷偵測器——
每次觸發即標記一個待修的上游問題（文件、契約、schema 說明）——而非常設品質保障層。
凡 outcome_validity ≠ VALID_MODEL_OUTCOME 的 cell，一律先走第 3.1 節平反／修正流程，
不送 Healer。

### 7.2 Healer 結果分類

| 狀態 | 定義 |
|---|---|
| `noneligible` | 不符合任何安全規則 guard |
| `no_trigger` | 沒有規則觸發 |
| `changed_partial_progress` | 往後推進，但仍未 PASS |
| `rescue_to_pass` | 修復後 G1–G4 全 PASS |
| `rejected` | 修復候選未通過安全檢查 |
| `rollback` | 修改後結果變差，回復原程式 |
| `false_positive` | 不該修改的程式被錯誤修改 |
| `abstained` | Healer 因不確定而停止 |

- `changed_partial_progress` 與 `rescue_to_pass` 必須分開。
- Healer 修復結果**只能另行分帳**，不得覆蓋 first-attempt outcome（ITT）。

---

## 8. 每個 cell 最少必填欄位

```json
{
  "dataset": "MBPP+",
  "task_id": "Mbpp/123",
  "model": "qwen3.5:4b",
  "condition": "Ab2g",
  "seed": 2026071301,

  "prompt_hash": "sha256:…",
  "evaluator_hash": "sha256:…",
  "evaluation_revision": "revision_003",

  "infrastructure_valid": true,
  "raw_response_present": true,
  "candidate_present": true,

  "g1_parse": "PASS",
  "g2_execution": "PASS",
  "g3_contract": "FAIL",
  "g3a_required_api": "NOT_APPLICABLE",
  "g3c_canonical_form": "NOT_APPLICABLE",
  "g4_correctness": "NOT_ASSESSED",

  "final_status": "FAILED",
  "primary_failure_layer": "L2",
  "outcome_validity": "VALID_MODEL_OUTCOME",
  "failure_subtype": "OUTPUT_PACKAGING",
  "mechanism_tags": ["output_packaging"],
  "failure_chain": [],

  "exception_type": null,
  "exception_message": null,

  "healer_eligible": true,
  "matched_rule": "L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP",
  "healer_outcome": "rescue_to_pass",

  "review_status": "human_reviewed",
  "notes": ""
}
```

v2 新增必填：`prompt_hash`、`evaluator_hash`、`evaluation_revision`、`outcome_validity`、
`g3a_required_api`、`g3c_canonical_form`、`failure_chain`。
無此設計的資料集，gate 子項以 `NOT_APPLICABLE` 填寫，不得留空。

---

## 9. 共同判定流程

```text
1. 模型呼叫或基礎設施成功嗎？（含 API 重試耗盡）
   否 → L0（validity = INVALID_INFRASTRUCTURE）

2. Python 能解析嗎？
   否 → L1

3. 程式能正常執行嗎？
   否 →
      例外源自 API 呼叫點 → L3（並核對文件：validity 判 VALID 或 INVALID_CONTRACT）
      例外源自變數／資料流／控制流程 → L4
      例外源自評測方序列化／介面 → 症狀層照標，validity = INVALID_CONTRACT/INFRASTRUCTURE
      無法區分 → needs_human_review

4. 輸出符合 contract 嗎？（含 G3c canonical form，語意等價比對）
   否 → L2（先確認 schema 要求在 prompt 中明確；不明確 → INVALID_CONTRACT）

5. required API adoption（G3a）符合嗎？
   否 → L3

6. 答案通過 oracle/tests 嗎？
   否 → 先排除 evaluator 比對邏輯問題（是 → INVALID_EVALUATOR，走平反流程）
        確認後 → L5（VALID_MODEL_OUTCOME）

7. 全部通過 → PASSED（validity 仍須確認非誤放）
```

---

## 10. 三組共同紀律

1. 主分類以最早可觀察失敗層為準；症狀（layer）與責任（validity）分開記錄，不得混用。
2. 不確定時標 `needs_human_review` / `PENDING_REVIEW`，不得推測；合併分析前必須清零。
3. L0 與一切 validity ≠ VALID 的 cell 不可當成模型程式錯誤。
4. G4 fail 前先排除 L2 包裝問題**與 evaluator 比對邏輯問題**。
5. required API 必須事前定義；事後不得補判。
6. 多層錯誤保留 failure chain；系統修正造成的失敗型態轉變亦須記錄。
7. Healer 不可用最終答案反推修法；L5 與 INVALID_* cells 一律不送 Healer。
8. 單題補丁不能算通用規則。
9. 修復後重新跑 G1–G4。
10. production 與 experimental Healer 分開。
11. development、held-out、不同資料集與模型不得混算；
    prompt 開發用的 dev set cells 永久排除於正式統計。
12. machine label 與人工判定不同時，保留兩者，不覆寫原始標籤。
13. 原始 artifact 與 first-attempt 判定永不改寫；evaluator／契約修正一律以
    revision 分版記錄，只平反、不放水。
14. prompt、evaluator、工具箱、任務契約均凍結並記錄 hash；
    任一 hash 變更即構成新版本，跨版本結果不得直接合併。
15. API 工具文件由程式碼單一事實來源（SSOT）生成並於 preflight 機器驗證一致，
    禁止人工手寫維護。

---

## 11. 共同統計項目

### 原始生成

- planned cells / valid responses / PASS
- L0–L5 數量（僅 VALID_MODEL_OUTCOME）
- **validity 分佈：VALID / INVALID_EVALUATOR / INVALID_CONTRACT / INVALID_INFRASTRUCTURE**
- ITT pass rate / valid-response pass rate
- **各 evaluation_revision 的翻正格數與理由**

### Healer

- eligible / triggered / changed / partial progression / rescue-to-pass
- rejected / rollback / false-positive / abstained
- **Healer 觸發率隨系統修正版本的變化**（成熟度反向指標的追蹤）

### 必須分開報告

- MBPP+／HumanEval+／CE115
- development／held-out
- 不同模型
- 不同 prompt condition
- Healer 前／後（first-attempt 為正式；Healer 後另行分帳）
- production／experimental
- infrastructure failure／model failure／**evaluator-contract failure（平反紀錄）**

---

## 12. 共同研究敘述

> 本研究以 L0–L5 統一分類 AI 生成程式的失敗症狀層級，以 outcome_validity 區分模型原生
> 錯誤與評測系統缺陷，並以 G1–G4（含 G3a required-API、G3c canonical-form 子項）判定
> 程式是否正式通過。每個失敗 cell 依最早可觀察失敗層分類，同時保留工具使用機制、多層
> failure chain、評測修正的 revision 紀錄與 Healer 修復結果，使 MBPP+、HumanEval+、
> CE115 與其他資料集能以相同口徑合併分析。Healer 僅於模型原生且機械可修的層級
> （以 L2 為主）行使職權，其觸發率作為評測系統成熟度的反向指標持續追蹤。

---

## 13. 版本說明

**v2（本版）**：

- 新增 outcome_validity 維度與平反（revision）流程——來自 CE115 三輪 evaluator 修正
  與契約修正的實戰教訓；無此維度，評測方錯誤將被灌入模型失敗統計且平反無處記錄。
- 補齊 L3 判定式（三型）與 G3a required-API 子 gate。
- 明定 canonical form 歸 G3c／L2，並強制語意等價比對、禁止字串全等。
- 明文區分症狀（layer）與責任（validity）兩維度。
- 必填欄位新增 prompt_hash、evaluator_hash、evaluation_revision、failure_chain 等。
- 第 7 節新增 Healer 職權邊界表與「觸發率為成熟度反向指標」原則。
- 紀律新增第 13–15 條（不可竄改、hash 凍結、SSOT）。

**v1**：初版，L0–L5、G1–G4 與 Healer 結果分類。

後續若三組出現新的穩定錯誤類型，先共同審核，再更新版本。
