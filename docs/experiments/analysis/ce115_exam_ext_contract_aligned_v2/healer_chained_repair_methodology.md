# CE115 Research Healer — 鏈式修復方法論

> 正式化文件。`real_model_calls=0`。不放寬 guard；不混算 experimental／production。

## 1. 定義

**鏈式修復（chained repair）**：對同一 candidate，在 production allowlist 上以固定 priority 依序套用多條規則；**每一 pass 最多一條規則改動原始碼**；改動後立即 re-parse／re-validate／（若有 task）re-evaluate；再進入下一 pass，直到穩定或耗盡 `max_passes`。

## 2. 套用順序

1. **固定 priority（升序）**：與 runner `select_allowlisted_rules` 一致。
2. **閘門對齊（由外而內）**：優先處理更外層可執行／契約接線失敗，再處理答案形狀包裝。
   - priority 100：`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`（payload 形狀）
   - priority 110：`L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM`（G2 空 kwargs 袋接線）
   - priority 120：`L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP`（G3/G4 `correct_answer` 字串包裝）
3. **一次一條**：`one_change_per_pass`；首個 `changed=True` 即結束該 pass。
4. **每條後重新驗證**：reparse；validation；有 task 時呼叫既有 evaluator（僅報告／止損，不反推修法）。

## 3. `max_passes` 契約

| 模式 | `max_passes` | 語意 |
|---|---|---|
| 單 pass／歷史 Ab3 預設 | `DEFAULT_MAX_PASSES=1` | 若仍有規則要改 → **fail-closed rollback** |
| 鏈式 production 評估 | `RECOMMENDED_CHAIN_MAX_PASSES = len(RULE_ALLOWLIST)` | 允許多層剝離；耗盡仍有待改 → rollback |

預設不自動升為鏈式；呼叫端必須顯式傳入 chain budget。

## 4. Provenance：`chain_position`

每個 pass provenance 含：

- `pass_index`：0-based 執行輪次
- `chain_position`：本 run 中**實際改動**的 1-based 序位；未改動之 pass 為 `null`

其餘既有欄位（selected_rule_id、hashes、guards、validation…）不變。

## 5. 安全不變式

- Guard 僅描述結構特徵；禁止 task_id／題目數值／單題 snippet
- 禁止用 oracle／evaluator 結果決定是否接受修改
- 禁止猜測變數值或演算法意圖
- 任一規則 validation 失敗 → 該規則不落地；max_passes 超限 → 整段 rollback

## 6. 計數分離

| 類別 | 計入 |
|---|---|
| production 修復 | 僅 production allowlist 規則在 production 流程下的 changed／rescue |
| experimental | 標記 experimental 的草案／診斷；**不得**與 production 修復數混算 |

## 7. 參考案例

Qwen4B v2 `113-10 Ab2d`：RUNTIME KeyError → kwargs-bag inline（chain_position=1）→ json.dumps unwrap（chain_position=2）→ PASS。
