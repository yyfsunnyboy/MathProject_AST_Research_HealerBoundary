# Healer Triage 依據查證 — Schema-Only vs Answer-Value Leakage v1

- **性質**：唯讀稽核。未修改任何程式、規則、評分邏輯、正式結果；未執行模型呼叫、規則修改或重評；僅追蹤既有原始碼與既有凍結artifact。
- **範圍**：Qwen3.5:4B math16_pilot02正式v4管線，`classify_math16_response()` → `evaluate_math_task_oracle()` → `math16_oracles.py` → healer eligibility gate（`decide_healer_eligibility()`/`probe_healer_hits()`）→ `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`的matcher（`analyze_l2_payload_wrap()`）之完整判斷鏈，聚焦於`eligible_execution_records.jsonl`中10格`fail_eligible`紀錄。
- **母體確認**：`docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl`確為10筆，其中7筆`matched_rule_probe = L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`（其餘3筆為`L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP`×1、`L1_PROSE_RESIDUE_NARROW`×1、`L1_CLOSE_UNBALANCED_PARENTHESIS`×1）。本報告聚焦L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP的triage依據，但Q1/Q2/Q4的管線追蹤適用於全部10格（因eligibility gate與schema判定邏輯對六規則共用）。

---

## Q1：「這格是L2 schema_failure」這個判定，具體是哪一段程式碼產生的？

**函式**：`classify_math16_response()`，[scripts/run_math16_latex_v1_gemini_live.py:260-328](scripts/run_math16_latex_v1_gemini_live.py:260)

**確認：本函式由qwen4b正式v4管線實際import使用**（並非僅Gemini專用）：
- [scripts/evaluate_math16_pilot02_qwen4b_v4.py:181](scripts/evaluate_math16_pilot02_qwen4b_v4.py:181) `from scripts.run_math16_latex_v1_gemini_live import classify_math16_response, extract_code`（產出`cell_level_baseline.jsonl`，即320格baseline評分）
- [scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py:38](scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py:38) 同一import（healer執行時對同一raw_response重新呼叫一次，見Q4）

**具體產生schema_failure的判定式**（[scripts/run_math16_latex_v1_gemini_live.py:316-328](scripts/run_math16_latex_v1_gemini_live.py:316)）：

```python
if (
    not isinstance(value, dict)
    or set(value) != {"question_text", "correct_answer", "oracle_payload"}
    or not isinstance(value.get("question_text"), str)
    or value.get("oracle_payload") != frozen_params
):
    return "schema_failure", source, _success_details(...)
```

**讀取的變數**：
- `value`：candidate的`generate()`實際執行後的回傳dict（來自`_execute_generate_all_ops()`，[scripts/run_math16_latex_v1_gemini_live.py:185](scripts/run_math16_latex_v1_gemini_live.py:185)，純執行層產物）
- `frozen_params`：task的凍結參數（`frozen_for_prompt(task)["oracle_payload"]`），**與模型答案無關的task定義本身**，不是「正確答案數值」
- 檢查項目：`value`是否為dict、keys是否恰為三個固定字串、`question_text`型別、`oracle_payload`是否等於`frozen_params`

**是否包含`correct_answer`或任何正確數值**：**否**。此判定式的四個條件**完全不引用`value["correct_answer"]`**，也不引用task的標準答案。`value["correct_answer"]`要到第330行（`schema_failure`分支之後）才第一次被讀取。

**下游標籤產生**：`classify_outcome_to_v3()`（[scripts/evaluate_math16_pilot02_full_v4.py:136](scripts/evaluate_math16_pilot02_full_v4.py:136)）在`outcome == "schema_failure"`分支（[scripts/evaluate_math16_pilot02_full_v4.py:253-259](scripts/evaluate_math16_pilot02_full_v4.py:253)）機械式設定`primary_failure_layer = "L2"`、`gates["g4_correctness"] = "NOT_ASSESSED"`——純字串映射，同樣不讀取任何答案數值。

**結論**：Q1判定鏈 = `classify_math16_response()`的schema判定式（答案盲）→ `classify_outcome_to_v3()`的字串映射（答案盲）。**CONFIRMED，不涉及`correct_answer`**。

---

## Q2：`evaluate_math_task_oracle()`與schema檢查的執行順序——是否為「schema先攔截，數值比對是獨立後續分支」？

**逐行確認`classify_math16_response()`內部順序**（[scripts/run_math16_latex_v1_gemini_live.py:292-345](scripts/run_math16_latex_v1_gemini_live.py:292)）：

```
293: tree = ast.parse(source)                          # (a) parse檢查
298: entries = [... generate ...]                       # (b) entry point檢查
306: status, value, error = _execute_generate_all_ops(...)  # (c) 執行candidate
307: if status != "passed": return status, ...          # (d) runtime failure提早return
316: if (schema條件不符): return "schema_failure", ...   # (e) ← schema檢查，提早return
329: verdict = evaluate_math_task_oracle(               # (f) ← 數值比對，schema通過後才執行
         task["oracle_type"], audit_oracle_payload, value["correct_answer"]
     )
332: outcome = classify_math16_oracle_failure(verdict)
```

**這是兩個明確分開的if分支，非同一段程式碼糾纏**：
- 第316-328行（schema_failure分支）以`return`語句**提早終止函式**，第329行的`evaluate_math_task_oracle()`呼叫**永遠不會被執行到**。
- 只有(e)的schema條件**全部為False**（即通過schema檢查）時，控制流才會落到(f)呼叫`evaluate_math_task_oracle()`。

**Python執行語意的直接證明**：Python的`return`是無條件跳出函式，第322行`return "schema_failure", ...`執行後，函式立即返回，第329-358行（含`evaluate_math_task_oracle`呼叫與其後的`classify_math16_oracle_failure`/"passed"/其他數值比對結果分支）在該次呼叫中**完全不會被執行**（非邏輯推論，是Python `return`語句的確定性行為）。

**結論**：schema檢查在數值比對**之前**執行，且schema_failure的產生**不需要**執行到`evaluate_math_task_oracle()`那一步。**非ENTANGLED**——兩者是同一函式內先後兩個可清楚拆分的`if`分支，schema_failure分支對數值比對分支具有阻斷性（一旦schema_failure，數值比對分支的程式碼在該次呼叫中永不執行）。**CONFIRMED CLEAN**。

---

## Q3：`analyze_l2_payload_wrap()`的guard輸入與`correct_answer_present`的實際檢查內容

**函式位置**：[agent_tools/finals_rebuild/ce115_research_healer_rules_l2.py:181-336](agent_tools/finals_rebuild/ce115_research_healer_rules_l2.py:181)

**輸入參數**（第181-184行）：`source: str`（candidate的原始碼文字）、`frozen: Mapping[str, Any] | None`（task的凍結參數，`context.get("frozen")`）。**不接受`correct_answer`或任何評分結果作為參數**。

**Guard鏈逐一檢查（依matcher內實際執行順序）**：

| Guard | 程式碼（逐字） | 讀取數值比對？ |
|---|---|---|
| `single_frozen_key` | `len(frozen.keys()) == 1`（第209行） | 否——只數frozen dict的key數量 |
| `parse_ok` | `ast.parse(source)`成功（第214-216行） | 否——純語法解析 |
| `return_has_oracle_payload` | `_dict_entry(ret, "oracle_payload")`非None（第243-244行） | 否——只檢查key是否存在於AST return dict中 |
| `payload_static_scalar` | `_resolve_scalar()`能靜態解析出純量（第289-305行） | 否——純AST靜態解析（Constant/Name鏈/`kwargs.get`） |
| `scalar_equals_frozen_value` | `resolved == frozen_value`（第307行） | **是，但比對對象是`frozen_value`（task定義的凍結參數），不是`correct_answer`**——這是「candidate回傳的oracle_payload純量是否等於task的frozen參數」，屬於契約/schema一致性比對，不是「模型答案是否等於標準答案」的評分比對 |
| `correct_answer_present` | `_dict_entry(ret, "correct_answer")`非None（第245-246、319行） | **否**——`_dict_entry()`（第133-137行）只用`isinstance(k, ast.Constant) and k.value == key_name`比對**key名稱字串**，回傳的`value`（第246行`correct_answer`對應的AST節點）**只被判斷"是否為None"（即該key是否存在），其AST節點的實際內容（數值/表達式）從未在此guard中被讀取或比較** |
| `already_wrapped` | `payload_value`本身即為`ast.Dict`且恰為`{frozen_key: scalar}`（第140-149、275-287行） | 否——純AST結構比對 |

**明確回答「`correct_answer_present`是否連帶檢查數值」**：**否**。原始碼第245-246行：
```python
_ck, correct_value, _ci = _dict_entry(ret, "correct_answer")
guards["correct_answer_present"] = correct_value is not None
```
`correct_value`是`correct_answer`這個key所對應的**AST節點物件**（不是Python執行後的實際數值），且**唯一的用途是`is not None`存在性判斷**。此guard從頭到尾不對`correct_value`的AST節點做`ast.dump`比對、不做`_resolve_scalar()`解析、也不與task的標準答案做任何相等比較。（`apply()`函式內另有獨立的`_correct_answer_fingerprint()`AST dump比對，但那是transform前後**不變性**驗證，用途是確保修改沒有動到答案欄位，同樣不是「這格算不算schema_failure」的判定依據，且發生在eligibility判定之後的repair階段。）

**結論**：全部7個guard中，僅`scalar_equals_frozen_value`涉及「相等比對」，但比對對象是task的凍結參數（`frozen_value`，非模型答案，非評分標準答案），其餘guard皆為AST結構/存在性檢查。**CONFIRMED，guard鏈不涉及`correct_answer`的具體數值**。

---

## Q4：Eligibility gate的觸發時機

**追蹤呼叫鏈**：[scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py:266-324](scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py:266)

```
286: outcome, source, details = classify_math16_response(raw, ...)   # 重新對raw_response跑一次分類
292: mapped = classify_outcome_to_v3(outcome, details, ...)
306: is_pass = base["final_status"] == "PASSED"    # ← 讀取「已計算完的baseline」欄位，非本次重跑結果
313: context = {"task": task, "frozen": frozen_params}
314: eligibility = decide_healer_eligibility(
315:     baseline_passed=is_pass,                    # ← 來自precomputed baseline
316:     source=source,                              # ← 來自本次重跑的classify_math16_response
317:     context=context,
318:     mechanism_tags=list(base.get("mechanism_tags") or mapped["mechanism_tags"] or []),
...
```

**兩個判定式必須分開回答，不得含糊**：

1. **`baseline_passed`（是否進入eligibility候選）**：讀取`base["final_status"]`——這是`load_baseline()`（[scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py:181](scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py:181)）從`cell_level_baseline.jsonl`載入的**precomputed欄位**，即先前一次獨立的`evaluate_math16_pilot02_qwen4b_v4.py`跑批已產出的最終分類結果。**這一步確實依賴「評分管線已經跑完之後的中間輸出」**——但要注意：`final_status != "PASSED"`（即FAIL）對schema_failure格而言，其FAIL狀態本身也是由Q1的答案盲schema判定式產生（`classify_outcome_to_v3`對`schema_failure`機械映射`final_status="FAILED"`，見[scripts/evaluate_math16_pilot02_full_v4.py:257](scripts/evaluate_math16_pilot02_full_v4.py:257)），並非由數值比對產生。（對其他FAIL原因如`content_mismatch`——即模型答案數值錯誤——而言，其FAIL狀態才是由`evaluate_math_task_oracle()`數值比對產生；但這是"是否FAIL"的原因分類，不是"是否L2 schema_failure eligible"本身的依據。）
2. **`source`與matcher比對（是否matched L2規則）**：`probe_healer_hits(source, context)`（[scripts/evaluate_math16_pilot02_full_v4.py:307-324](scripts/evaluate_math16_pilot02_full_v4.py:307)）直接呼叫`rule.is_applicable(source, context)`/`rule.is_triggered(source, context)`，其中`source`是**本次（healer腳本內）重新呼叫`classify_math16_response(raw, ...)`**（第286行）所得的候選程式碼字串，非直接複用baseline的預存欄位。此路徑**只執行AST解析與結構比對**（見Q2/Q3），全程未呼叫`evaluate_math_task_oracle()`。

**明確標示**：
- **是否「評分函式已經跑完、產生schema_failure這個outcome之後」才被呼叫**：**是**，就`baseline_passed`（FAIL/PASS gate）而言——eligibility gate依賴`cell_level_baseline.jsonl`這個先前跑批的中間輸出決定「這格是否進入候選」。
- **是否可以獨立於評分管線之外、只靠執行candidate並檢查AST/型別結構就能判定**：**就L2規則本身的matcher/guard邏輯而言，是**——`analyze_l2_payload_wrap()`只需要`source`與`frozen`兩個參數，不需要`base["final_status"]`或任何評分結果即可獨立求值（第314-318行的`probe_healer_hits`呼叫在程式碼結構上本可脫離`base`直接執行，只是目前的腳本把FAIL-gate與matcher呼叫寫在同一個迴圈裡、由precomputed baseline決定「值不值得跑matcher」這一節流步驟）。

**結論（不得含糊）**：eligibility gate分成兩層——(1) FAIL/PASS節流層讀取precomputed baseline的`final_status`（架構上耦合於評分管線的先前輸出，但對schema_failure格而言該欄位本身答案盲）；(2) L2規則matcher層（`probe_healer_hits`→`analyze_l2_payload_wrap`）是純AST/結構判定，不讀取`base`的任何欄位、不呼叫`evaluate_math_task_oracle()`、可獨立於評分管線之外運作。**兩層都不涉及`correct_answer`數值，但第(1)層在目前實作中確實是「讀取評分管線中間輸出」而非「原始執行層獨立判定」——此為誠實揭露的架構耦合，非答案洩漏。**

---

## Q5：概念驗證——完全繞過評分管線的替代triage版本

**若要做到「純執行層triage」，具體步驟**：
1. 執行candidate的`generate()`（沿用現有`_execute_generate_all_ops()`，純執行層，[scripts/run_math16_latex_v1_gemini_live.py:185](scripts/run_math16_latex_v1_gemini_live.py:185)）
2. 捕捉回傳值的型別/結構（`isinstance(value, dict)`、`set(value.keys())`、`value.get("oracle_payload") != frozen_params`——即`classify_math16_response()`第316-321行的schema條件本身，不需要往下走到第329行）
3. 若schema條件不符 → 直接標記為schema_failure候選，接著對candidate的原始碼字串呼叫`analyze_l2_payload_wrap(source, frozen)`（不需要`base["final_status"]`、不需要`evaluate_math_task_oracle()`）
4. 全程不呼叫`evaluate_math_task_oracle()`、不讀取`cell_level_baseline.jsonl`

**架構限制（誠實記錄）**：
- **schema判定邏輯本身**（步驟2）與**評分判定邏輯**（`evaluate_math_task_oracle`呼叫）目前寫在**同一個函式**`classify_math16_response()`內，只是用`return`提早分開（見Q2）。若要"完全繞過評分管線"，需要把第260-328行（schema判定，答案盲）抽成獨立函式，與第329行以後（數值比對）物理分離成兩個檔案/兩個callable——**目前程式碼並未做此物理拆分**，兩者共用同一個函式定義與同一次呼叫入口。這是**函式邊界層面的架構限制**，但不影響Q1/Q2已確認的「schema判定不讀取correct_answer數值」這一事實。
- **eligibility gate的FAIL/PASS節流層**（Q4第(1)層）目前綁定讀取`cell_level_baseline.jsonl`這個先前跑批產物，若要讓eligibility完全獨立於評分管線之外運作，需要把「FAIL/PASS」判定也改為即時重新執行schema檢查（步驟2-3）而非讀取precomputed欄位——**目前腳本（[scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py:306](scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py:306)）選擇讀取precomputed `base["final_status"]`而非即時重算**，這是現有腳本的實作選擇，不是`analyze_l2_payload_wrap()`本身的限制。

---

## 交付結論

| 判定 | **`CLEAN_SCHEMA_ONLY`** |
|---|---|
| 依據 | Q1-Q4逐行追蹤證明：(a) schema_failure判定式（`classify_math16_response()`第316-321行）完全不引用`value["correct_answer"]`或任何標準答案數值；(b) `evaluate_math_task_oracle()`的呼叫（第329行）在schema_failure的`return`路徑上**永遠不會被執行到**（Python `return`語意保證，非推論）；(c) `analyze_l2_payload_wrap()`的7個guard中，僅`correct_answer_present`涉及`correct_answer`，且該guard**只檢查AST key存在性、不讀取其值**；(d) `scalar_equals_frozen_value`guard比對的是task的凍結參數，非模型答案 |

**誠實揭露的架構耦合（不影響上述判定，但必須記錄）**：目前的healer腳本（[scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py](scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py)）將「這格是否FAIL」的節流判斷讀取自`cell_level_baseline.jsonl`這個先前評分管線的precomputed輸出（Q4第(1)層），而非在eligibility階段即時重新執行schema檢查——這是**程序上依賴評分管線的既有輸出**，但因為該輸出本身（對schema_failure格）也是答案盲產生（見Q1/Q2），所以**不構成oracle/答案數值洩漏**，只是尚未做到"完全物理獨立於評分管線之外"的triage實作（見Q5架構限制）。

**可在報告正面主張**：「`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`的triage依據（schema_failure判定與matcher/guard鏈）為執行層可觀察訊號（AST結構、契約schema、回傳值型別），不構成oracle/答案數值洩漏。」

**不得主張**：「eligibility gate完全獨立於評分管線之外運作」——因FAIL/PASS節流層在現行程式碼中確實讀取評分管線的precomputed中間輸出（見Q4）。

---

## UNRESOLVED項目

無。Q1-Q5全部追蹤至具體行號並附direct evidence path，未發現需要標註UNRESOLVED的模糊環節。

---

## Direct Evidence Paths

- [scripts/run_math16_latex_v1_gemini_live.py:260-358](scripts/run_math16_latex_v1_gemini_live.py:260) — `classify_math16_response()`
- [scripts/evaluate_math16_pilot02_full_v4.py:136-330](scripts/evaluate_math16_pilot02_full_v4.py:136) — `classify_outcome_to_v3()`、`probe_healer_hits()`、`decide_healer_eligibility()`
- [scripts/evaluate_math16_pilot02_qwen4b_v4.py:179-246](scripts/evaluate_math16_pilot02_qwen4b_v4.py:179) — qwen4b baseline評分呼叫`classify_math16_response()`
- [scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py:266-338](scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py:266) — eligibility gate呼叫鏈
- [agent_tools/finals_rebuild/ce115_research_healer_rules_l2.py:181-336](agent_tools/finals_rebuild/ce115_research_healer_rules_l2.py:181) — `analyze_l2_payload_wrap()`
- `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl` — 10格母體確認（唯讀讀取，本輪未修改）

---

## Git狀態

- 起始 HEAD：`9d864d126b386d2238f6f68b99bdb7c655e70d68`（branch `main`）
- 本輪操作：唯讀（`Read`/`Grep`/`Bash`讀取既有jsonl），**未**修改、stage、commit、push、stash或restore任何既有檔案
- 本輪唯一新增：本報告本身（`docs/experiments/reports/qwen4b_l2_payload_wrap_eligibility_answer_leakage_audit_v1.md`）
- 結束時HEAD與branch與起始相同；既有的modified/untracked檔案清單（見session開始時`git status`）未受本輪任何操作影響
