# CE115 Exam Ext — Contract-Aligned Ablation v2 研究里程碑報告

**日期**：2026-07-18
**狀態**：正式封存（本文件不重跑模型、不改 raw artifacts）
**Seed**：2026071301
**Production Healer allowlist（凍結）**：僅 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`

---

## 0. 閱讀規則（硬性分母）

本報告強制遵守：

1. **v1／v2 分開列示，從不混算**。
2. **ITT（intent-to-treat）與 valid-response 分母分開**；infra failure 不併入模型能力率。
3. **Timeout = infrastructure failure**，不歸因模型能力（例：Qwen4B v2 114-04 Ab2d，wall≈1800s，`chat_calls=0`）。
4. **qwen3.5:9b 標未執行**；不做模型規模趨勢推論。
5. Healer 邊界數字（本里程碑 Qwen4B v2 Ab3）：**rescue-to-pass = 0**，**false-positive = 0**。

機器可讀總表：
`docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/final_integration_report_01/final_integration_matrix.json`

---

## 1. 方法

### 1.1 研究問題

在 junior-high 外部驗證題組（113／114）上：

- 對齊 production Domain API＋prompt contract（v2）後，生成通過率如何變化？
- 現行凍結 L2 Healer 能否安全救援殘敗？邊界在哪裡？

### 1.2 設計

| 層級 | 內容 |
|---|---|
| Tasks | 6 題 L1：114-01／114-02／114-04／114-08／113-10／113-11 |
| Conditions | Ab1／Ab2g／Ab2d（v1 全矩陣）；v2 formal 為 114-02×3 + 其餘 Ab2d |
| Models | Gemini 3.5 Flash；qwen3.5:4b；**qwen3.5:9b 未執行** |
| Lineage v1 | `ce115_exam_external_validation_113_114` pilots |
| Lineage v2 | `ce115_contract_aligned_ablation_v2`（human_review_prompts_02） |
| Healer | Production allowlist 僅 L2；本輪不新增／不放寬規則 |
| Healer 關閉於 formal 生成 | v2 formal runs：`healer_calls=0` |

### 1.3 Evidence 路徑索引

| 類型 | 路徑 |
|---|---|
| v1 Gemini results | `docs/experiments/results/ce115_exam_ext_113_114_gemini_pilot_01/` |
| v1 Qwen4B results | `docs/experiments/results/ce115_exam_ext_113_114_qwen_pilot_01/` |
| v2 Gemini formal | `docs/experiments/results/ce115_exam_ext_contract_aligned_v2_gemini_01/` |
| v2 Qwen4B formal | `docs/experiments/results/ce115_exam_ext_contract_aligned_v2_qwen4b_01/` |
| v2 combined 16-cell | `docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/formal_16cell_gemini_qwen4b_combined.json` |
| L2 eligibility（v1） | `docs/experiments/analysis/ce115_exam_ext_113_114_combined_census_01/l2_eligibility_audit.json` |
| Ab3 v1 Gemini | `docs/experiments/analysis/ce115_exam_ext_113_114_ab3_production_eval_01/summary.json` |
| Qwen4B fail-5 forensic | `docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/qwen4b_fail5_reviewed_forensic_ledger.json` |
| Qwen4B v2 Ab3 | `docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/qwen4b_v2_ab3_production_eval_01/summary.json` |
| 整合矩陣 | `docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/final_integration_report_01/` |
| Canonical prompts v2 | `docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/human_review_prompts_02/` |
| Domain API SoT | `core/prompts/domain_function_library.py` |
| Ablation builder | `agent_tools/finals_rebuild/ce115_contract_aligned_ablation_v2.py` |

---

## 2. 結果矩陣（分開分母）

### 2.1 Cohort 總表

| Cohort | ITT pass/n | ITT rate | Infra fails | Valid pass/n | Valid rate |
|---|---|---|---|---|---|
| v1 Gemini full18 | 14/18 | 0.7778 | 0 | 14/18 | 0.7778 |
| v1 Qwen4B full18 | 7/18 | 0.3889 | 0 | 7/18 | 0.3889 |
| v1 Gemini overlap8（對齊 v2 計劃） | 4/8 | 0.50 | 0 | 4/8 | 0.50 |
| v1 Qwen4B overlap8 | 3/8 | 0.375 | 0 | 3/8 | 0.375 |
| **v2 Gemini formal8** | **8/8** | **1.00** | 0 | **8/8** | **1.00** |
| **v2 Qwen4B formal8** | **3/8** | **0.375** | **1** | **3/7** | **0.4286** |
| v2 Qwen9B formal8 | NOT_EXECUTED | — | — | — | — |

> 詳細逐格矩陣見
> `docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/final_integration_report_01/final_integration_matrix.md`

### 2.2 v1 → v2（僅 formal overlap8）

**Gemini**

| 變化 | n | 說明 |
|---|---|---|
| fail_to_pass | 4 | 114-02 Ab1/Ab2g/Ab2d（coefficients 巢狀）；114-04 Ab2d（非法 Fraction 路徑） |
| pass_to_pass | 4 | 其餘 overlap 格維持 PASS |

**Qwen4B**

| 變化 | n | 格 |
|---|---|---|
| pass_to_pass | 2 | 114-02 Ab1；114-01 Ab2d |
| fail_to_pass | 1 | 114-02 Ab2g |
| fail_to_fail | 3 | 114-02 Ab2d；114-08；113-11 |
| fail_to_infra_fail | 1 | 114-04（timeout；**不歸因模型**） |
| pass_to_fail | 1 | 113-10 Ab2d |

### 2.3 Gemini vs Qwen4B（v2，分開）

- Gemini v2：contract-aligned prompts／APIs 下 **8/8 PASS**。
- Qwen4B v2：ITT 3/8；valid-response 3/7（排除 timeout）。
- 殘敗 forensic：**剩餘 prompt/API mismatch = 0**；主因為 assembly／tool-routing／code-bloat（詳見 fail-5 ledger）。
- **不比較、不推論 4B vs 9B 規模因果**（9B 未執行）。

---

## 3. L2 eligibility 與 Ab3／Healer 安全邊界

### 3.1 v1 L2 eligibility audit

來源：`…/ce115_exam_ext_113_114_combined_census_01/l2_eligibility_audit.json`

| 類別 | n |
|---|---|
| eligible_existing_rule | 3 |
| eligible_new_rule_candidate | 5 |

Existing rule：`L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
（new-rule candidates **本里程碑未實作**；correct_answer wrap 禁止）

### 3.2 Ab3 — v1 Gemini（已完成）

來源：`…/ce115_exam_ext_113_114_ab3_production_eval_01/summary.json`

- Allowlist：僅 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
- triggered_any = 0；**rescue-to-pass = 0**
- 4 失敗格全 no_op；14 PASS 無回歸
- `real_model_calls = 0`

### 3.3 Ab3 — Qwen4B v2（本里程碑完成）

來源：`…/qwen4b_v2_ab3_production_eval_01/summary.json`

| 項目 | 值 |
|---|---|
| 輸入格 | 114-02／114-08／113-10／113-11 Ab2d（排除 114-04 infra） |
| Hash integrity | 4/4 OK |
| Eligible | **0** |
| Non-eligible | **4** |
| Healer executed | **0** |
| **rescue-to-pass** | **0** |
| **false-positive** | **0** |
| 磁碟 candidate 修改 | 無 |

Non-eligible 對應 production guard（非「規則不夠聰明」）：

| Cell | analyze.reason | 對應 guard |
|---|---|---|
| 114-02 | `parse_error` | `parse_ok=False` |
| 114-08 | `payload_not_static_scalar` | payload 非裸 scalar |
| 113-10 | `frozen_not_single_key` | frozen 多鍵 |
| 113-11 | `frozen_not_single_key` | frozen 多鍵 |

**邊界結論**：殘敗 mechanism 本質上落在現行 allowlist 設計範圍外；不可宣稱 v2 Healer 可救援此批 Qwen4B 失敗。Gemini v2 Ab3 **仍 pending**。

---

## 4. 主要研究結論

1. **Contract alignment 有效（Gemini）**：v2 消除 v1 Gemini 在 overlap 上的兩類 contract／API 失敗，formal8 = 8/8 PASS（ITT = valid-response）。
2. **同 prompt 下 Qwen4B 殘敗非 signature mismatch**：forensic 判定 assembly／routing／bloat；114-04 為 infrastructure timeout。
3. **凍結 L2 Healer 安全但無救援**：v1 Gemini Ab3 與 Qwen4B v2 Ab3 皆 **rescue=0、false-positive=0**；Qwen4B v2 四格全數 noneligible（guard 正確擋下）。
4. **Healer 價值在邊界清晰**：可修範圍仍是「單鍵 frozen + 裸 scalar `oracle_payload` wrap」；不可修範圍包含 parse／runtime assembly／多鍵 frozen 等。
5. **9B 未執行**：禁止規模趨勢宣稱。

---

## 5. 研究限制

- v1 full18 ≠ v2 formal8；僅 overlap8 可做成對 v1→v2。
- L2 eligibility audit 以 v1 為主；v2 另採 forensic／Ab3 路徑。
- Gemini v2 Ab3 未跑；Qwen v1 Ab3（existing-L2-eligible）未跑。
- 單一 seed；無多 seed 變異估計。
- v2 formal 生成階段 Healer 關閉（`healer_calls=0`）。
- Timeout 必須用 valid-response 分母，不得併入能力結論。

### 待補清單

- qwen3.5:9b 相同 8-cell v2
- Gemini v2 Ab3
- （可選）Qwen v1 Ab3 on existing-L2-eligible
- 多 seed 重複驗證

---

## 6. 封存備註

- 整合報告備份目錄（可回溯、未覆寫）位於
  `docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/final_integration_report_01/`
  底下以 `backup_before_qwen4b_v2_ab3_` 為前綴的子目錄。
- 本里程碑清理：僅移除一次性 scripts 目錄下 `_tmp_` 前綴腳本；**不刪除** results 與 analysis 實驗下任何實驗產物。
- 結論摘要副本：
  `docs/experiments/analysis/ce115_exam_ext_contract_aligned_v2/final_integration_report_01/research_conclusions_and_limitations.md`
