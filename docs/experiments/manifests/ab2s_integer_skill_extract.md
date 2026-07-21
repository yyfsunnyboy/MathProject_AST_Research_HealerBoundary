# Ab2s Integer Skill Specification & Extraction

This document outlines the extraction of the legacy Integer `SKILL.md` rules into the formalized **Ab2s (Skill-style Precise Specification)** format, detailing what is preserved, what is excluded, and the lineage tracing for each rule.

---

## A. 保留並改寫為Ab2s規格 (Ab2s Specification Rules)

### 1. 完整 Dotted-Path 規則 (Full Dotted-Path Namespace Enforcement)
* **規格內容**：調用領域 API 時，模型必須使用完整的命名空間限定名稱 `IntegerOps.method(...)`，絕對禁止使用未限定的裸名函數（如 `fmt_num(...)` 或 `safe_eval(...)`），以防在模組載入或執行環境中產生 NameError 錯誤。

### 2. 依賴注入規則 (Dependency Injection Rule)
* **規格內容**：`IntegerOps` 類別已經由執行沙盒環境預先注入。在生成的 Python 程式碼中，禁止寫入任何 `import IntegerOps` 或 `from ... import IntegerOps` 的語句，直接調用 `IntegerOps.xxx` 即可。

### 3. 安全求值規則 (Safe Evaluation Rule)
* **規格內容**：嚴禁在程式碼中使用 Python 原生 `eval()` 執行不受信任的輸入。`IntegerOps.safe_eval(expr)` 的使用範圍僅限於對已生成的靜態算術算式字串（如 `"(-3)**3"`）進行安全求值，不得將其作為一般的 Python 代碼執行捷徑或代替常規的 Python 計算變數。

### 4. 原生 Python 優先 (Native Python First)
* **規格內容**：對於基本的整數運算（加、減、乘、整除）、整數冪次（`**`）、整除餘數判斷（`%`）、比較（`<`, `>`, `==`）以及循環控制結構，模型應優先使用原生 Python 語法。禁止調用未在 Task-local allowlist 中的 API（如 `IntegerOps.add` 或 `IntegerOps.sub`），以避免由於 API 模板缺失導致的運行時崩潰。

### 5. Task-Local Allowlist 限制 (Task-Local Allowlist Constraint)
* **規格內容**：模型只能調用在該 Task 提示詞中明列的 API。縱使 `IntegerOps` 類別在運行時可能定義了其他方法，只要未被本題 Allowlist 明確列出，模型一律禁止調用。
  模型可見 Prompt 中不得包含任何 module import path（如 `core.prompts.domain_function_library`）。
  Allowlist API 格式統一為：
  ```text
  - IntegerOps.is_divisible(a, b) -> bool
    Availability: already injected into runtime scope.
    Call exactly as IntegerOps.is_divisible(a, b).
    Do not import IntegerOps.
  ```

### 6. 未定義 Helper 禁止規則 (No Fabricated Helpers Rule)
* **規格內容**：模型在生成程式碼時，不得引用、假設或捏造任何未列在 Allowlist 或 Python 標準庫中的 adapter、converter、helper 或 solver 函數（例如 `to_exact`、`RationalSolver` 等）。

### 7. Family 結構分類 (Family Structural Taxonomy)
* **規格內容**：舊的 `I1–I8` 分類概念僅作為後端與提示詞的設計來源，並不與本次實驗的四個 Task 形成一對一的硬編碼映射。在實際 Prompt 中，只加入對應的一般結構標籤：
  * `ce111_q03_prime_factor_selection`: `divisibility-and-prime-factor selection`
  * `ce112_q01_negative_integer_power`: `signed integer exponentiation`
  * `ce112_q09_divisor_multiple_intersection`: `divisor-multiple intersection`
  * `ce111_nonchoice_q01_part1_exponential_growth`: `discrete exponential growth`
  結構標籤中絕不包含具體的解題步驟、答案或固定程式碼。

### 8. 結構化狀態 (Structured State Preservation)
* **規格內容**：程式碼中的精確數學值應保存在標準 Python 數據結構（如 `int`, `bool`, `list`, `dict`）中，不得將格式化後的 LaTeX 或 presentation 顯示字串（如 `"(-5)"`）作為計算的中間狀態或權威數據源。

### 9. 計算與渲染解耦 (Decoupling Computation and Rendering)
* **規格內容**：在 `generate()` 中必須將精確的數值計算與 LaTeX 字串渲染進行物理分離。先計算出正確的數值答案（`correct_answer`），再根據顯示格式要求建構題面（`question_text`），避免兩者邏輯混淆。

### 10. JSON-Safe 輸出契約 (JSON-Safe Output Contract)
* **規格內容**：`generate()` 函數回傳的 dictionary 中，`question_text`, `correct_answer`, `oracle_payload` 的值必須完全符合該 Task 的 JSON 格式契約，且所有的 leaves 必須為標準的 JSON-safe 類型（如 `str`, `int`, `float`, `bool`），不可包含 Fraction 物件或 custom class 實例。

### 11. 自動化 Quality Gate 自檢自查 (Quality Gate Self-Check)
* **規格內容**：模型生成的代碼必須包含自檢自查 Quality Gate 邏輯，確認：
  * `generate(level=1, **kwargs)` 存在。
  * 回傳值恰好包含 `question_text`、`correct_answer`、`oracle_payload` 三個頂層 key。
  * 隨機輸入參數 `frozen_params` 未被篡改，且 `oracle_payload` 欄位、值、型別符合 contract。
  * `correct_answer` 型別符合該題 contract。
  * 所有變數與函數名稱在使用前已正確定義與導入。
  * API 必須使用完整 dotted path，且不得使用 allowlist 以外的 API。
  * 不得使用 `IntegerOps.add`、`IntegerOps.sub` 與原生 `eval`。
  * 不得捏造 helper、adapter、converter。
  * 所有輸出均為 JSON-serializable。
  * 先完成精確計算，再建立字串與 LaTeX。
  * 無 Markdown fences（如 ```python 標籤）與額外的解釋性文字 (explanatory prose)。

### 12. 輕量型自檢限制 (Lightweight Verification Constraint)
* **規格內容**：如果程式碼中包含自檢或檢查邏輯，其設計必須是通用的結構與型別驗證，嚴禁包含答案求解邏輯、逆向推理或對 evaluator oracle 的直接呼叫。

---

## B. 明確排除 (Explicit Exclusions)

為防止模型硬套模板、偷渡答案或繞過實際計算，以下內容在 Ab2s 中被**明確排除**，禁止寫入提示詞：
1. **硬編碼與特判補丁**：任何題型 ID 到具體程式碼/答案常數的硬編碼映射（如 `if task_id == "ce112_q01": return -27`）。
2. **Evaluator 與 Healer 內部邏輯**：判分器的具體測試用例、逆運算流程、以及運行時 Healer 的 auto-correct 規則。
3. **無效 API 方法**：`IntegerOps.add` 與 `IntegerOps.sub`（經 Pilot-00 盤點證實可能在部分 stubs 中缺失，易引發 AttributeError），以及 fraction 專用的 `to_exact` adapter。
4. **非 Task-Local 工具**：非本題所需的其他 domain helpers。
5. **模組導入路徑**：模型可見 Prompt 中完全不出現 `import: core.prompts.domain_function_library` 等 module import path，以避開 import 歧義。

---

## C. 逐項來源追蹤 (Lineage Tracing & Rule Mapping)

我們定義 **Ab2s 五大工程原則** 作為對照依據：
* **P-1**：依賴注入原則 (Dependency Injection Principle)
* **P-2**：完整命名空間路徑 (Full Namespace Enforcement)
* **P-3**：原生語法優先 (Native-First Rule)
* **P-4**：計算與渲染解耦 (Decoupled Computation & Rendering)
* **P-5**：結構化數據輸出契約 (Complete Structured JSON Contract)

| 序號 | 規則名稱 | SKILL.md 原始區段 | 表述方式 | 對應五原則 | 涉及 Pilot-00 修正？ | 是否改變任務能力？ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | 完整 Dotted-Path | `【Engineering Constraints】` 2 | 重新表述 | **P-2** | 否 | 否 (純規格約束) |
| **2** | 依賴注入規則 | `【Engineering Constraints】` 2 | 重新表述 | **P-1** | 否 | 否 (純規格約束) |
| **3** | 安全求值規則 | `【Engineering Constraints】` 3 | 重新表述 | **P-4** | 否 | 否 (防止 eval 濫用) |
| **4** | 原生 Python 優先 | `【Engineering Constraints】` 1 | 重新表述 | **P-3** | **是** (排除 `add`/`sub`) | 否 (提高代碼健壯性) |
| **5** | Task-Local Allowlist | `【Injected APIs】` | 重新表述 | **P-2** | **是** (篩除無效 API/移除 import) | 否 (收緊 API 邊界) |
| **6** | 未定義 Helper 禁止 | `【Engineering Constraints】` | 重新表述 | **P-2** | 否 | 否 (防幻覺規約) |
| **7** | Family 結構分類 | `【Family Catalogue】` | 重新表述 | **P-5** | **是** (以結構標籤取代硬編碼映射) | 否 (保留題型結構分類) |
| **8** | 結構化狀態 | `【Structural Schema】` | 重新表述 | **P-5** | 否 | 否 (提高變數維護精度) |
| **9** | 計算與渲染解耦 | `【Verification Logic】` | 重新表述 | **P-4** | 否 | 否 (優化生成代碼邏輯) |
| **10** | JSON-Safe 輸出契約 | `【Output Contract】` | 重新表述 | **P-5** | 否 | 否 (防 Fraction 洩漏) |
| **11** | 自動化 Quality Gate | `【Verification Logic】` | 重新表述 | **P-5** | **是** (擴充為完整的 Quality Gate 自檢標準) | 否 (提升編譯通過率) |
| **12** | 輕量型自檢邏輯 | `【Minimum check() Contract】` | 重新表述 | **P-5** | 否 | 否 (防逆向偷渡) |
