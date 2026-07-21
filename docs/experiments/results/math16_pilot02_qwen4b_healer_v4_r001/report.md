# Qwen4B Pilot-02 Frozen Healer v4_r001

```text
QWEN4B_FROZEN_HEALER_EXECUTION_COMPLETED
QWEN4B_HEALER_COMPLETENESS_AUDIT_PASSED
QWEN4B_POST_HEALER_RESULTS_FROZEN
QWEN4B_PRIMARY_HEALER_PIPELINE_COMPLETED
```

- External eligibility pre-filter: **retained** (noneligible never call `run()`)
- Baseline PASS: **78/320**
- Post-Healer PASS: **83/320**
- FAIL eligible / noneligible: **10 / 232**
- Healer ran: **10**
- Rescued: **5**
- Repaired-still-fail: **3**
- Eligible no-op: **2**
- Abstained (noneligible): **232**
- Regression: **0**
- Rule applied: `{'L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP': 6, 'L1_PROSE_RESIDUE_NARROW': 1, 'L1_CLOSE_UNBALANCED_PARENTHESIS': 1}`
- Corpus SHA: `7dd3ba5f7e7a38e7ad20142e8c5c5b2e84c20df1b7f5abcf5701c23d24172a22`
- Evaluator SHA: `2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc`
- Healer runner SHA: `b89e6059ce67efb622aa2e085e365b909d0d4f7df1a6814c1dc83df029ce81e1`
- Healer protocol SHA: `bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39`
- Allowlist: `L1_CLOSE_UNBALANCED_PARENTHESIS, L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED, L1_PROSE_RESIDUE_NARROW, L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP, L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM, L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP`
- LLM calls: **0**

## Condition

| Condition | Baseline | Post-Healer | Eligible | Rescued |
| :--- | ---: | ---: | ---: | ---: |
| Ab1 | 15/80 | 15/80 | 1 | 0 |
| Ab2g | 19/80 | 21/80 | 3 | 2 |
| Ab2d+api | 8/80 | 9/80 | 3 | 1 |
| Ab2d+spec-v2 | 36/80 | 38/80 | 3 | 2 |

## Family

| Family | Baseline | Post-Healer | Eligible | Rescued |
| :--- | ---: | ---: | ---: | ---: |
| Integer | 30/80 | 30/80 | 1 | 0 |
| Polynomial | 16/80 | 16/80 | 1 | 0 |
| Radical | 15/80 | 18/80 | 5 | 3 |
| Fraction | 17/80 | 19/80 | 3 | 2 |
