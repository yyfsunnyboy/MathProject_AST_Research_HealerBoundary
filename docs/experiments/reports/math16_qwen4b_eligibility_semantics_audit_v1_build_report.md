# Math16 Qwen4B Eligibility Semantics Audit v1 Build Report

```text
MATH16_QWEN4B_ELIGIBILITY_SEMANTICS_BUILD_V1_COMPLETED
ZERO_MODEL_EXECUTION_VERIFIED
242_FAIL_CELLS_FIVE_STRATA_CLASSIFIED
STRESS_TEST_INTERVENTION_CONTRAST_CONFIRMED
OFFICIAL_RESULTS_PRESERVED
```

**專案／研究線：** Ivan 旺宏科學展 —— HealerBoundary (`MathProject_AST_Research_HealerBoundary`)
**報告版本：** v1.0 (Eligibility Semantics Build Closeout)
**建置時間 UTC：** 2026-07-23

---

## 1. 執行合規與數據彙總 (Compliance & Metrics Summary)

- **模型呼叫次數 (LLM/VLM Calls)**: `0`
- **Healer 執行次數**: `0`
- **Evaluator 執行/重評次數**: `0`
- **Transform 執行次數**: `0`
- **既有 PASS/FAIL 修改次數**: `0`
- **Final Report v1.3 修改**: `無 (SHA未變)`

---

## 2. 242 格 Baseline FAIL 分層盤點結果 (Strata Summary)

| 分層名稱 (Strata Name) | Cell 數量 | 佔比 (%) | 說明 |
|---|---:|---:|---|
| `NO_RULE_CANDIDATE` | 231 | 95.45% | 無任何凍結規則 Pattern 命中 (含 227 無規則 + 4 無抽取原始碼) |
| `UNIQUE_CANDIDATE_PRIMARY_ELIGIBLE` | 10 | 4.13% | 命中單一規則且通過 Primary 安全 Eligibility 閘門 |
| `UNIQUE_CANDIDATE_PRIMARY_NONELIGIBLE` | 0 | 0.00% | 命中單一規則但被 Primary 安全 Eligibility 閘門擋下 |
| `AMBIGUOUS_MULTIPLE_CANDIDATES` | 1 | 0.41% | 歧義入口點 (`qwen3_5_4b__ce111_q08_...__seed_2026072004`) |
| `DETECTION_UNRESOLVED` | 0 | 0.00% | 未能解析規則候選 |
| **總和 (Total Baseline FAIL)** | **242** | **100.00%** | **五類互斥且完整覆蓋** |

---

## 3. 產出檔案清單 (Generated Files)

- `artifacts/math16_qwen4b_eligibility_semantics_audit_v1/eligibility_semantics_records.jsonl`
- `artifacts/math16_qwen4b_eligibility_semantics_audit_v1/candidate_strata_table.csv`
- `artifacts/math16_qwen4b_eligibility_semantics_audit_v1/rule_candidate_counts.csv`
- `artifacts/math16_qwen4b_eligibility_semantics_audit_v1/eligibility_rejection_reasons.csv`
- `artifacts/math16_qwen4b_eligibility_semantics_audit_v1/evidence_index.json`
- `docs/experiments/manifests/math16_qwen4b_eligibility_semantics_audit_v1_manifest.json`
- `docs/experiments/reports/math16_qwen4b_eligibility_semantics_audit_v1.md`
- `docs/experiments/reports/math16_qwen4b_eligibility_semantics_audit_v1_build_report.md`
- `scripts/build_math16_qwen4b_eligibility_semantics_audit_v1.py`
- `tests/test_math16_qwen4b_eligibility_semantics_audit_v1.py`

---

## 4. 結案 Verdict

```text
MATH16_QWEN4B_ELIGIBILITY_SEMANTICS_AUDIT_V1_COMPLETED
RULE_DETECTION_AND_SAFETY_GATE_DISTINGUISHED
STRESS_TEST_INTERVENTION_CONTRAST_CONFIRMED
UNRESTRICTED_STRESS_TEST_V11_PREREGISTERED
OFFICIAL_RESULTS_PRESERVED
READY_FOR_ZERO_MODEL_V11_DRY_RUN
```
