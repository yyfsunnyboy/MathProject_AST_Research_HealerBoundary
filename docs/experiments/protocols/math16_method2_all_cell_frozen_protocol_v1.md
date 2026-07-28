# Math16 Method 2 全格 Eligibility-First Frozen Protocol v1

狀態：**FROZEN — NOT EXECUTED**

凍結日期：2026-07-28

對應 manifest：[`math16_method2_all_cell_protocol_v1.json`](../manifests/math16_method2_all_cell_protocol_v1.json)

## 1. 目的與範圍

本 Protocol 凍結 Math16／Qwen 3.5 4B 既有 320 格 raw source 的 Method 2 zero-model replay 設計。本次只凍結程序、欄位、程式入口與 SHA-256，不執行正式 Healer replay 或 Evaluator，不重跑模型，也不修改 Method 1 結果。

Method 2 與 Method 1 的唯一程序差異是 Eligibility 的母體與時序：Method 2 不查看任何 Baseline PASS／FAIL，320 格全部先完成 Eligibility 決策；所有 source 決策凍結後，才以相同 Evaluator 分別批改 Raw 與 Final。

## 2. 凍結流程

1. 依既有 320-cell plan 讀取每格 `raw_response.txt`，以凍結 extractor 取得 raw source。
2. 每格無條件進入 Eligibility。Eligibility 僅接收 raw source 與 frozen task parameters。
3. Eligible 才呼叫現有凍結 `MathHealerRunner`；不更動 allowlist、priority、matcher、Eligibility、Guard、transformation 或 max-pass 語意。
4. Noneligible 的 Final source 必須與 Raw source 完全相同，且 SHA-256 相等。
5. Raw source 與 Final source 分開保存；在 320 格 source 決策全部完成前，不得啟動 Evaluator。
6. 使用同一 pinned Evaluator 對 Raw 與 Final 兩路分別評分；評分結果不得回饋 Eligibility、transform 接受或回退。
7. 全部評分完成後，才由 `(raw_status, final_status)` 唯一導出 transition。

本輪停在 Protocol freeze 與 zero-model preflight；第 3 步的 transformation、第 6 步的評分均未執行。

## 3. Blinding 與禁止資料流

Eligibility／Healer 決策允許輸入只有：

- raw source；
- frozen task parameters（Healer 現有 schema/Guard 所需 context）。

在 source 決策完成前，禁止讀取或傳入：

- Baseline `final_status`、`raw_status` 或任何 PASS／FAIL 標籤；
- 正確答案值；
- classifier outcome、evaluation gates、evaluator result；
- 任何以評分結果為依據的觸發、接受或回退訊號。

程式碼中出現的候選程式 `correct_answer` 欄位屬 raw source AST 的原文；現有凍結規則若檢查該欄位的結構存在性或 transformation 前後不變性，不得讀取其答案值來決定是否觸發或接受。

## 4. Eligibility 與 Healer 入口

- Eligibility：依 `RULE_ALLOWLIST` 固定順序，對每格呼叫既有 rule 的 `is_applicable(raw_source, context)`，適用時再呼叫 `is_triggered(raw_source, context)`。
- Eligible：至少一個現有 allowlisted rule triggered；`rule_id` 記錄固定順序的第一個命中規則。
- Noneligible：無可擷取 raw source，或 allowlist 中沒有規則 triggered。
- Healer：`agent_tools/finals_rebuild/ce115_research_healer_runner.py::MathHealerRunner`，正式 replay 時沿用 manifest 凍結的 allowlist 與 `max_passes=3`。

Method 1 的 `scripts/evaluate_math16_pilot02_qwen4b_healer_v4.py` 可重用 corpus/pin/context 組裝概念，但其 Baseline FAIL 節流不可重用於 Method 2。

## 5. Runner 與儲存契約

Runner 必須分兩個不可交錯的 phase：

### Phase A：source decision（全 320 格）

- 逐格保存 raw source 與 `raw_source_sha256`。
- 逐格保存 Eligibility 決策、rule provenance、source 是否改變。
- Eligible 保存 Healer output 為 Final source。
- Noneligible 複製 Raw source 為 Final source；兩者 SHA-256 必須相同。
- Raw 與 Final 必須寫入 manifest 指定的不同目錄。
- 320 格 `eligibility_checked=true` 且 source journal 完整後才可關閉 Phase A。

### Phase B：independent scoring（未於本輪執行）

- 先固定 Phase A journal 的 SHA closure。
- 同一 Evaluator 分別讀取 Raw 與 Final；不得覆寫 source。
- `raw_status` 與 `final_status` 分別落盤。
- 只由兩個 status 導出 transition，不得人工重分類。

## 6. 每格 Journal 欄位

| 欄位 | 型別／允許值 | 時點與不變量 |
|---|---|---|
| `cell_identity` | object | 至少含 `cell_id`, `task_id`, `condition`, `seed` |
| `raw_source_sha256` | 64-char SHA-256 | Phase A 擷取後 |
| `eligibility_checked` | boolean | 320 格必須全為 `true` |
| `eligible` | boolean | 不得由 Baseline status 決定 |
| `rule_id` | string/null | eligible 時為第一個 frozen allowlist hit |
| `rule_triggered` | boolean | 與 rule hit provenance 一致 |
| `source_changed` | boolean | Raw／Final byte comparison |
| `final_source_sha256` | 64-char SHA-256 | Noneligible 時必須等於 raw SHA |
| `raw_status` | `PASSED`/`FAILED`/null | Phase B 前為 null |
| `final_status` | `PASSED`/`FAILED`/null | Phase B 前為 null |
| `transition` | enum/null | Phase B 兩路完成後唯一導出 |

實作可增加 extraction diagnostics、全部 rule hits、per-pass provenance、rolled_back 等欄位，但不得省略上述欄位或改變其語意。

## 7. Transition 凍結定義

| Raw | Final | transition |
|---|---|---|
| FAILED | PASSED | `verified_rescue` |
| PASSED | FAILED | `regression` |
| PASSED | PASSED | `preserved_pass` |
| FAILED | FAILED | `still_failed` |

## 8. Zero-model preflight

`scripts/preflight_math16_method2_all_cell.py` 僅執行：

- manifest 與 frozen SHA 驗證；
- 320-cell plan 完整性與 cell identity 唯一性；
- canonical extraction 與 320 格 Eligibility probe；
- Eligibility context 不含 Baseline status、正確答案值或 evaluator 欄位；
- Noneligible `Final == Raw` 的 hash invariant；
- Raw／Final 儲存路徑分離；
- journal 欄位與四種 transition mapping 完整性。

Preflight 不呼叫 `MathHealerRunner.run()`、任何 rule `apply()`、Evaluator 或模型，且不寫正式結果目錄。

執行：

```powershell
python scripts/preflight_math16_method2_all_cell.py
python -m pytest tests/test_math16_method2_all_cell_protocol_v1.py
```

## 9. 凍結檔案

所有 pinned SHA-256 以 manifest 的 `frozen_sha256` 為唯一機器可讀來源，包含：

- 現有 Healer runner 與 execution protocol；
- 現有 production allowlist 的六個 rule modules；
- canonical extraction 與 Math16 frozen task context；
- 320-cell plan；
- 後續 Raw／Final 共用 Evaluator。

任何 pinned SHA drift、allowlist drift、cell count 非 320、Eligibility coverage 非 320、Raw／Final 路徑相同或 journal contract drift，均為正式 replay blocker，必須停止，不得自動改寫 manifest 或降級執行。
