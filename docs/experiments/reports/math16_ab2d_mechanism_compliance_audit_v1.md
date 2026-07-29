# Math16 Ab2d Mechanism Compliance Audit v1 (draft)

> **status:** `development_candidate_not_frozen`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> Depends on Step -1 registry (not modified): `docs/experiments/manifests/math16_domain_api_contract_registry_v1.json`

## Executive Conclusion

系統契約大致成立：32 個 task-condition 中 **29** 正確；另有 **2** 處 prompt 內部矛盾與 **1** 處 method 未明確指定，均已標記，並排除於後續契約型 Healer eligibility。模型並非百分之百依約：formal **422** 格中 **COMPLIANT_PASS = 169**，**NONCOMPLIANT_PASS = 20/422（4.7%）**（答對但未完全依約使用指定工具），故不把所有 PASS 都解釋成 API 使用成功。分層抽樣 **30** 格（涵蓋兩處系統契約缺陷、一處未指定 method，以及 compliant／noncompliant／其他失敗類別）顯示兩種抽取路徑之 compliance 標籤 **30/30** 一致（`EXACT_SOURCE_MATCH` 26、`SOURCE_DIFF_LABEL_SAME` 4、label changed 0）。**20/422** 為經 30 格分層抽樣一致性支持的高可信度 supplemental estimate，並非完整 422 格 frozen-candidate closure。本補充稽核**不改變**既有 Baseline、Healer rescue 與 Tier 1 統計。Ab2d+api／Ab2d+spec 比較應解讀為**系統工具選擇與 prompt 暴露設計**之比較；Gemini 現行 Ab2d+spec 僅有限 post-hoc evidence，早期不完整 spec 不作現行結論。

## Verdict

機制判斷：**系統供給面大致可追溯；模型全量遵守未成立**。

- **Ab2d+api**：16/16 system contract 可由 SSOT／TASK_DOMAIN_APIS 組裝；模型側存在不可忽略的 noncompliant（含 PASS）。
- **Ab2d+spec（現行 v2）**：多數 selector 可追溯；保留 2 defect、1 unresolved；Gemini 現行可比 spec 僅 post-hoc 部分 `ab2d_spec_v2`。

## Provenance & extraction concordance（brief）

- Raw responses 與既有 PASS／FAIL 錨定 Pilot-02 frozen artifacts／evaluator journals（422/422 identity／SHA 可追溯）。
- Compliance AST 輸入曾以 ad-hoc `extract_code()` 自 frozen raw 重建；後經 30 格分層抽樣與 authoritative reference（Method2 `raw_sources`／formal `extraction.py::extract_code` + journal `candidate_hash`）比對，**compliance label 30/30 一致**（`STRATIFIED_SAMPLE_EXTRACTION_CONCORDANCE_CONFIRMED`）。詳見 `math16_ab2d_extraction_sample_closure_v1.md`。
- 因此：**不得**宣稱完整 422 格 frozen-candidate closure；亦**不得**將本補充誤讀為「Pilot-02 整體做錯」。核心正式分數與 Healer 統計不變。

## Scope

| Condition | Current formal evidence |
|---|---|
| Ab2d+api | Gemini + Qwen4B + Qwen9B `ab2d` cells |
| Ab2d+spec | Qwen4B/Qwen9B `ab2d_spec_v2`; Gemini `ab2d_spec_v2` post-hoc partial |
| Excluded from current-mechanism conclusion | Gemini primary `ab2d_spec` (v1) |

## Layer 1 — 32 task-condition system contracts

| Status | Count |
|---|---:|
| SYSTEM_CONTRACT_CORRECT | 29 |
| SYSTEM_CONTRACT_DEFECT | 2 |
| UNRESOLVED | 1 |

### SYSTEM_CONTRACT_DEFECT

- `Ab2d+spec` / `ce111_q08_polynomial_factor_parameter_recovery`: native-only task still embeds API Signature Card for PolynomialOps.format_latex (prohibition card for to_latex)
- `Ab2d+spec` / `ce115_calc_exact_rational_expression_l1`: Prompt internal conflict: guardrail names FractionOps.sub; scaffold example shows FractionOps.add; Ab2d+api exposes FractionOps.add

### UNRESOLVED contracts

- `Ab2d+spec` / `ce111_q10_ordered_quadratic_roots_radical`: Selector mixed / class-level Use Ops without method-level cards; method requirements UNRESOLVED (evaluation api_policy='mixed'; scaffold/guardrail methods=['RadicalOps.simplify_term'])

### Ab2d+api vs evaluation `api_policy` label

Evaluation baseline 對 `condition=ab2d` 的 `api_policy` 標籤（native-only／API-only／mixed）**不可直接當成 Ab2d+api prompt 契約**：多個 Integer／部分 Radical／Polynomial 任務在 Ab2d+api prompt 暴露 Domain API，但 baseline 標成 native-only。本稽核以 `TASK_DOMAIN_APIS` + SSOT 為 Ab2d+api 真相。

建議（不修改舊檔）：後續若校正 evaluation 標籤，另開 revision；本輪只記錄缺陷建議。

## Layer 2 — Model compliance census

- Total rows (incl. historical Gemini v1): **502**
- Formal scored rows: **422**
- Historical excluded Gemini v1 rows: **80**

### Formal compliance class totals

| Class | Count |
|---|---:|
| `COMPLIANT_PASS` | 169 |
| `COMPLIANT_FAIL` | 92 |
| `NONCOMPLIANT_PASS` | 20 |
| `NONCOMPLIANT_FAIL` | 106 |
| `SYSTEM_CONTRACT_DEFECT` | 25 |
| `UNRESOLVED` | 10 |

### By model (formal)

- **gemini**: COMPLIANT_FAIL=2, COMPLIANT_PASS=95, SYSTEM_CONTRACT_DEFECT=5
- **qwen4b**: COMPLIANT_FAIL=62, COMPLIANT_PASS=33, NONCOMPLIANT_FAIL=43, NONCOMPLIANT_PASS=7, SYSTEM_CONTRACT_DEFECT=10, UNRESOLVED=5
- **qwen9b**: COMPLIANT_FAIL=28, COMPLIANT_PASS=41, NONCOMPLIANT_FAIL=63, NONCOMPLIANT_PASS=13, SYSTEM_CONTRACT_DEFECT=10, UNRESOLVED=5

### By prompt condition (formal)

- **Ab2d+api**: COMPLIANT_FAIL=52, COMPLIANT_PASS=88, NONCOMPLIANT_FAIL=86, NONCOMPLIANT_PASS=14
- **Ab2d+spec**: COMPLIANT_FAIL=40, COMPLIANT_PASS=81, NONCOMPLIANT_FAIL=20, NONCOMPLIANT_PASS=6, SYSTEM_CONTRACT_DEFECT=25, UNRESOLVED=10

## Required suspicion checks

### ce115_calc_exact_rational_expression_l1 add／sub／example

- **System:** SYSTEM_CONTRACT_DEFECT under Ab2d+spec（guardrail=`sub`，scaffold example=`add`，Ab2d+api=`add`）。
- Cell-level rows for this task under Ab2d+spec are classified `SYSTEM_CONTRACT_DEFECT` (not auto-PASS).

### PolynomialOps.to_latex

- Spec cards **負向提及**「There is NO `PolynomialOps.to_latex`」。未列為正向暴露 symbol。

### Spec class-only / mixed

- `ce111_q10_ordered_quadratic_roots_radical`：evaluation `api_policy=mixed`；prompt 寫 Use RadicalOps 但無 method card → contract `UNRESOLVED`；cells → `UNRESOLVED`。

### Runtime 全注入四 Ops

- 確認：未暴露 method 仍可能被呼叫。Census 以「是否呼叫未暴露 Ops method」計入 noncompliance（domain_api）或 native-only 違規。

### 模型自行重定義 Ops

- Formal cells with redefines: **58**

### Gemini 現行可比較 spec 範圍

- Primary Gemini `ab2d_spec` v1：**歷史排除**（80 cells → UNRESOLVED / not scored for current success）。
- Gemini `ab2d_spec_v2` post-hoc formal rows: **22**（非整份 80 格；不足以外推 Gemini 全量 spec-v2）。

## Does evidence support mechanism success?

### Ab2d+api

- System contracts CORRECT: **16/16**
- Formal COMPLIANT_PASS: **88** / formal api cells **240**
- Formal NONCOMPLIANT_PASS: **14**
- **Judgment:** 供給／寫入機制可支持「成功」敘事；但 NONCOMPLIANT_PASS>0 代表「模型使用需要的工具、忽略不需要的工具」**未在全量成立**。整體：**條件式支持（supply-side yes；compliance-side partial）**。

### Ab2d+spec（現行 v2）

- System CORRECT/DEFECT/UNRESOLVED: 13/2/1
- Formal COMPLIANT_PASS: **81** / formal spec cells **182**
- Formal NONCOMPLIANT_PASS: **6**
- **Judgment:** 不能宣稱全面成功。Selector 機制大致可追溯，但 defect／mixed UNRESOLVED／Gemini 可比範圍不完整 → **部分支持，附重大保留**。

## Suggested fixes (do not apply in this round)

1. 修正 `ce115_calc_exact_rational_expression_l1` Ab2d+spec guardrail／scaffold 的 add vs sub 一致性。
2. native-only 任務移除或隔離僅作禁止別名的 signature card，避免與 forbid Domain API 訊息衝突。
3. 為 mixed／class-only 任務補 method-level card，或明確允許 native。
4. 校正 evaluation `api_policy` 在 `condition=ab2d` 的標籤，使其對齊 TASK_DOMAIN_APIS（另開 revision）。
5. 若要對 Gemini 下現行 Ab2d+spec 全量結論，需完整 ab2d_spec_v2 生成／評分矩陣（本輪不做）。

## Artifact digests

- matrix: `c4dd105a915a0dafbc1a192ce1aa480f03de77b345507859041d906107acbbe6`
- census: `f7d1e53fc1364e3efeaef43e78261c78e163405e79b06d00dbcb315639c15cf6`
- this report (after provenance supplement): see working-tree file hash via sha256 (self-hash omitted)

## Declarations

- 本輪僅整理說明文字；未重新分析、未擴大 422 closure
- Did not modify healers / frozen Pilot-02 results / figures 數值
- Did not execute models, Healer replay, candidate, or evaluator
- Did not commit or push
- 既有 8 份稽核草案均保留（本檔為其中之一，僅更新文字）
