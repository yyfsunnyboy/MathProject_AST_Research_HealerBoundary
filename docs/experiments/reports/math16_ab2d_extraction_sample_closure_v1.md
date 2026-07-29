# Math16 Ab2d Extraction Sample Closure v1 (draft)

> **status:** `development_candidate_not_frozen`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **sample_seed:** `20260729`

## Verdict

`STRATIFIED_SAMPLE_EXTRACTION_CONCORDANCE_CONFIRMED`

30/30 抽樣格之 compliance label（authoritative reference vs compliance-audit ad-hoc `extract_code()`）一致。

> 20/422 為經 30 格分層抽樣一致性支持的高可信度 supplemental estimate，並非完整 422 格 frozen-candidate closure。

## Authoritative extraction reference

| Priority | Finding |
|---|---|
| 1 frozen `extracted_candidate.py` | Pilot-02 cell dirs：**不存在**；Method2 `raw_sources/*.py` 覆蓋 formal422 中 **160**（Qwen4B ab2d+ab2d_spec_v2） |
| 2 journal execution source | `candidate_hash` 覆蓋 **400/422**（缺 Gemini `ab2d_spec_v2` 22） |
| 3 formal extractor | `agent_tools/finals_rebuild/extraction.py::extract_code`（file SHA `a59da1c0a76fe24e868a51481306a5ea09d8d8977c92aab38a6c0c4dc38feccf`）；對有 `candidate_hash` 者 **400/400** 可重現 |
| 4 Method 2 policy | Protocol／manifest 明訂 raw_source_extraction = 上述 formal extractor |

**本輪 reference policy：** Method2 raw_sources（若有）→ 否則 formal extract 並以 journal `candidate_hash` 驗證 → 否則（Gemini v2 無 hash）僅 formal extract。

Ad-hoc 對照物：compliance audit builder 內嵌之 best-effort `extract_code()`（非 formal module）。

## Sample composition (30)

| Stratum | Quota | Actual |
|---|---:|---:|
| `SYSTEM_CONTRACT_DEFECT` | 6 | 6 |
| `UNRESOLVED_CONTRACT` | 4 | 4 |
| `NONCOMPLIANT_PASS` | 10 | 10 |
| `COMPLIANT_PASS` | 5 | 5 |
| `OTHER_FAIL` | 5 | 5 |

- Defect task-conditions: `[('ce111_q08_polynomial_factor_parameter_recovery', 'ab2d_spec_v2'), ('ce115_calc_exact_rational_expression_l1', 'ab2d_spec_v2')]`
- Unresolved task-condition: `('ce111_q10_ordered_quadratic_roots_radical', 'ab2d_spec_v2')`
- Models: `{'gemini': 5, 'qwen4b': 12, 'qwen9b': 13}`
- Conditions: `{'Ab2d+spec': 20, 'Ab2d+api': 10}`
- PASS/FAIL: 18/12

## Comparison class counts

| Class | Count |
|---|---:|
| `EXACT_SOURCE_MATCH` | 26 |
| `SOURCE_DIFF_LABEL_SAME` | 4 |
| `API_CALLSET_DIFF_LABEL_SAME` | 0 |
| `COMPLIANCE_LABEL_CHANGED` | 0 |
| `UNRESOLVED` | 0 |

- Compliance label agree: **30/30**
- Retain `20/422` high-confidence supplemental estimate: **True**

## Aggressive Healer readiness

可立即回到 Aggressive Healer 主線；本輪不再擴大 422 closure。

## Artifacts

- manifest: `docs/experiments/manifests/math16_ab2d_extraction_sample_v1.json` (SHA `b09f8313a4dd1f9629f0c9c989cf65ab52a89a3a483f38f8d8000880caa7f795`)
- this report: `docs/experiments/reports/math16_ab2d_extraction_sample_closure_v1.md`

## Declarations

- 未執行模型／Healer／candidate／evaluator
- 未修改 frozen Pilot-02 結果
- 未 commit、未 push
- 保留既有 6 個未追蹤稽核草案
