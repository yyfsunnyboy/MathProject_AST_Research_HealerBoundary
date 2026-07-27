# Smoke Pipeline Known Issues v1 — K1 / K2 / K3

- **狀態**：唯讀稽核產物；不修改任何既有程式或smoke/正式產物。
- **範圍**：僅涵蓋 `agent_tools/finals_rebuild/math_boundary_pilot.py::classify_response()` 所代表的 **smoke 評分管線**（供本 session 新增的4支 smoke script 使用：`run_math16_qwen25coder7b_four_condition_smoke_20260725.py`、`run_math16_qwen35_2b_four_condition_smoke_20260725.py`、`run_math16_qwen35_2b_smoke_20260725.py`、`run_math16_qwen35_2b_timeout_rerun_240s_20260725.py`）。
- **不涵蓋**：正式 v4 管線（`scripts/run_math16_latex_v1_gemini_live.py::classify_math16_response()` + `scripts/evaluate_math16_pilot02_{qwen4b,qwen9b,full}_v4.py`）。兩套管線程式碼互相獨立，見第6節。
- **本輪不實作任何修正**，僅記錄缺陷、影響範圍與未來警語。

---

## K1 — WRONG_ORACLE_PAYLOAD_SOURCE

| 項目 | 內容 |
|---|---|
| **程式檔／函數位置** | `agent_tools/finals_rebuild/math_boundary_pilot.py`，`classify_response()`，[第419行](agent_tools/finals_rebuild/math_boundary_pilot.py:419)：`verdict = evaluate_math_task_oracle(task["oracle_type"], frozen["oracle_payload"], value["correct_answer"])` |
| **觸發條件** | `frozen["oracle_payload"]` 是 `sample_task_parameters()` 依 task 定義的 `frozen_params` 取樣所得（見 [math_task_sampler.py:89-91](agent_tools/finals_rebuild/math_task_sampler.py:89)），並非 task 定義中完整的 `oracle_payload`（`audit oracle payload`，見 [math16_pool.py](agent_tools/finals_rebuild/math16_pool.py) 各 `_task(...)` 呼叫）。當某 task 的 `frozen_params` 缺少對應 oracle 函數所需的鍵（例如 `integer_exact` 需要 `selected`／`value`／`a`+`b`，但 `frozen_params` 只有 `candidates`／`n`），此行把不完整的 payload 直接送入 oracle。 |
| **後果** | oracle 函數依情況回傳 `error="...payload incomplete"`（有 try/except 或 else 分支的 oracle，如 `evaluate_integer_exact`）或直接 `KeyError` 崩潰（無 try/except 的 oracle，如 `evaluate_polynomial_factor_parameter_recovery`、`evaluate_integer_exact_k`、`evaluate_compound_radical_result`）。**與模型提交答案的對錯完全無關**——即使模型答對，oracle 仍無法判分。 |
| **已確認受影響run／cell** | `docs/experiments/results/qwen25coder7b_math16_four_condition_smoke_20260725_001/` 中 `ce111_q03_prime_factor_selection` 的3格：`ab2g`、`ab2d`、`ab2d_spec_v2`。三格皆confirmed：oracle_payload恆為`{"candidates":[11,12,13,14],"n":156}`，缺`selected`/`value`/`a`+`b`，`evaluate_integer_exact()`（[math16_oracles.py:490-500](agent_tools/finals_rebuild/math16_oracles.py:490)）無條件回傳 `error="integer_exact payload incomplete"`；`ab2d_spec_v2`格模型提交的答案（13）客觀正確，仍被判 `intrinsic_safety`，是最強反證。這3格屬 `INVALID_CONTRACT`，**不得算模型PASS或FAIL**。 |
| **已確認未受影響** | 正式v4管線：`scripts/run_math16_latex_v1_gemini_live.py::classify_math16_response()` 對 schema 檢查用 `frozen_params`、對 oracle 評分改用完整的 `audit_oracle_payload = task["oracle_payload"]`（[evaluate_math16_pilot02_qwen4b_v4.py:225-230](scripts/evaluate_math16_pilot02_qwen4b_v4.py:225)）。三份正式320-cell語料（Gemini/Qwen4B/Qwen9B）各自的 `outcome_validity_distribution` 均顯示 `INVALID_CONTRACT: 0`／`VALID_MODEL_OUTCOME: 320`，見第8節。 |

---

## K2 — ORACLE_ERROR_OVERMAPPED_TO_INTRINSIC_SAFETY

| 項目 | 內容 |
|---|---|
| **程式檔／函數位置** | `agent_tools/finals_rebuild/math_boundary_pilot.py`，`classify_response()`，[第420-424行](agent_tools/finals_rebuild/math_boundary_pilot.py:420)：`if verdict.get("error"): return "intrinsic_safety", ...` |
| **觸發條件** | `math16_oracles.py` 中多個 oracle 函數（`evaluate_math16_radical_simplification`、`evaluate_exact_fraction_canonical`、`evaluate_math16_polynomial_division_general`、`evaluate_math16_polynomial_factor_roots`、`evaluate_math16_exact_rational_expression`、`evaluate_radical_simplification_canonical`、`evaluate_compound_radical_result`、`evaluate_polynomial_division_remainder_only`、`evaluate_polynomial_factor_parameter_recovery`、`evaluate_integer_count`、`evaluate_integer_exact_k` 等）把「答案錯誤」的說明也寫進同一個 `error` 欄位（例如 `error="structural_mismatch"`／`"fraction_mismatch"`），而不是只在oracle**真正執行失敗**時才填 `error`。`classify_response()` 只要見到 `verdict["error"]` 非空字串，一律映射成 `intrinsic_safety`，未區分「oracle算不出來」與「oracle算出來但答案不對」。 |
| **後果** | 一般 answer mismatch／structural mismatch 被錯誤貼上 `intrinsic_safety` 標籤，讓人誤以為是安全過濾攔截；但oracle contract本身完好、payload完整、比對邏輯正確，模型是**真實答錯**。 |
| **已確認受影響run／cell** | `qwen25coder7b_math16_four_condition_smoke_20260725_001/` 中3格：`ce111_q05_exact_fraction_expression/ab1`（模型提交40/99，正解4/11，`error="fraction_mismatch"`）、`ce115_calc_radical_simplification_l1/ab1`與`/ab2g`（模型提交radicand=27未化簡，正解radicand=3，`error="structural_mismatch"`）。這3格是**有效模型FAIL**，只是outcome label錯誤，**不得排除於有效分母或Healer eligibility母體**。 |
| **已確認未受影響** | 正式v4管線改用 `classify_math16_oracle_failure()`（[math16_oracles.py:684-718](agent_tools/finals_rebuild/math16_oracles.py:684)），只有 error 字串含 `safety`/`policy_denied`/`intrinsic_safety`/`blocked_by_safety` 才判 `intrinsic_safety`，一般mismatch正確映射為 `structural_mismatch`/`answer_incorrect`。三份正式320-cell語料的 `INVALID_EVALUATOR`／相應欄位皆為0，見第8節。 |

---

## K3 — ODD_CODE_FENCE_FALSE_TRUNCATION

| 項目 | 內容 |
|---|---|
| **程式檔／函數位置** | `agent_tools/finals_rebuild/math_boundary_pilot.py`，[`_looks_truncated()`，第319-321行](agent_tools/finals_rebuild/math_boundary_pilot.py:319)：`return stripped.count("```") % 2 == 1` |
| **觸發條件** | 此函數只計算 raw response 中 ```` ``` ```` 出現次數的奇偶性，完全不檢查內容本身是否完整。當模型輸出**完整、可執行的程式**，但只是忘記在結尾補上收尾的 ```` ``` ```` fence時，fence計數為奇數，此函數仍回傳 `True`，`classify_response()` 在 extraction／schema／oracle 之前就提早判為 `catastrophic_truncation`，永遠不會走到後續判分。 |
| **後果** | 內容完整的回應被誤標為「災難性截斷」，其真實下游結果（能否parse／通過schema／oracle judge）因評分提早退出而**未知**，不能沿用舊label。 |
| **已確認受影響run／cell** | `docs/experiments/results/qwen35_2b_math16_four_condition_smoke_20260725_001/qwen35_2b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301/`。直接證據：`raw_response.txt` 全文以 `return {...}` 正常收尾，後接 `assert hasattr(generate, '__call__')` 與 `print("Function generate() verified.")`，內容無缺失；fence計數確認為1（僅開頭```python，無收尾）。該格最終 **PASS／FAIL未決**（UNRESOLVED），因評分管線從未真正執行extraction/schema/oracle判斷。 |
| **已確認未受影響** | 正式v4管線的 `classify_math16_response()`（`scripts/run_math16_latex_v1_gemini_live.py`）沿用同一 `_looks_truncated`-等價邏輯（[第272-275行](scripts/run_math16_latex_v1_gemini_live.py:272)），**理論上具有相同的fence計數盲點**，尚未在正式320-cell語料中找到實際受影響的cell（本輪未逐cell查證正式語料是否存在同類假陽性；此為未驗證項目，見警語）。 |

---

## 未來使用smoke管線前的警語

1. **禁止**直接把 `math_boundary_pilot.classify_response()` 的 `intrinsic_safety` outcome 當作安全過濾或倫理攔截的證據——多數情況下它只是K1（合約缺鍵）或K2（error欄位誤標）的產物。
2. **禁止**把 `catastrophic_truncation` outcome 直接當作內容確實缺失的證據，需先核對raw_response.txt尾端是否有完整收尾語意（K3）。
3. 若未來要用此smoke管線評分 Math16 新12題（`ce111_*`／`ce112_*`／`ce113_*`）中任一使用 `integer_exact`／`integer_count`／`integer_exact_k`／`polynomial_factor_parameter_recovery`／`compound_radical_result`／`exact_fraction_canonical` 等 oracle_type 的task，**必須先確認`frozen_params`是否包含該oracle所需全部鍵**，否則K1可能重現。
4. 若必須用此smoke管線做「PASS/FAIL計數」或「能力比較」，**必須先扣除K1格（不計入分母）並將K2/K3格重新分類**，不得直接沿用原始summary.json的outcome標籤做統計。
5. 本文件所列3個缺陷是**彼此獨立**的機制（K1：payload來源錯誤；K2：error欄位語意衝突；K3：截斷偵測啟發式過於粗糙），修正其中一個不會自動修正另外兩個。

---

## 修正原則（本輪不實作）

- **K1**：oracle評分應改用task定義中完整的 `oracle_payload`（audit payload），schema檢查繼續用 `frozen_params`，比照正式v4管線 `classify_math16_response()` 的雙payload設計（[run_math16_latex_v1_gemini_live.py:260-330](scripts/run_math16_latex_v1_gemini_live.py:260)）。
- **K2**：`classify_response()` 不應把 `verdict.get("error")` 直接等同於 `intrinsic_safety`；應改用如正式管線的 `classify_math16_oracle_failure()`，只在error字串含真正安全/政策攔截標記時才判 `intrinsic_safety`，其餘映射為 `structural_mismatch`/`answer_incorrect`/對應mismatch類別。
- **K3**：`_looks_truncated()` 應在fence數量為奇數時，額外檢查內容是否已達成語意上完整的收尾（例如：能否被extraction後的parser成功`ast.parse()`），而非只憑fence奇偶性下定論。

---

## 正式v4 baseline目前不受影響（本輪引用，未重新計算）

| 語料 | pass_fraction | 來源 |
|---|---|---|
| Gemini | 289/320 | `docs/experiments/results/math16_pilot02_full_evaluation_v4_r001/baseline_summary.json` |
| Qwen3.5:4B | 78/320 | `docs/experiments/results/math16_pilot02_qwen4b_evaluation_v4_r001/baseline_summary.json` |
| Qwen3.5:9B | 101/320 | `docs/experiments/results/math16_pilot02_qwen9b_evaluation_v4_r001/baseline_summary.json` |

三份摘要之 `outcome_validity_distribution`／`INVALID_CONTRACT`／`INVALID_EVALUATOR` 欄位均顯示 0 受影響 cell（Gemini明確列出 `INVALID_EVALUATOR:0, INVALID_CONTRACT:0`；Qwen4B/Qwen9B為 `VALID_MODEL_OUTCOME:320`，無其餘分類出現）。

**Formal amendment：NO**（K1/K2/K3三者皆未在正式v4語料中找到實際受影響cell；判定條件不成立，見既往稽核報告的四項必要條件）。
