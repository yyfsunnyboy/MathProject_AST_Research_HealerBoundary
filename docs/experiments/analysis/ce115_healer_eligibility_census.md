# CE115 Taxonomy-Level Healer Eligibility Candidate Census (read-only)

This document reports a **taxonomy-level eligibility candidate census**.
Candidates are **not** confirmed frozen-rule applicable.
Actual repair window remains pending the frozen-rule applicability audit.

- taxonomy: `docs/experiments/success_definition.md` (`success_definition.md#Post-Healer+Failure-taxonomy-mapping`)
- observed_dataset_hash: `8144fa46afa9063bc2c1ac2b546e0c0ebc328b77a347836720c10f23953efbd5`
- script_sha256: `78ad52aa869b6ce20366d4b236ab5c85b53708daf4db509e1809e488e0446df1`
- enabled Core rules: `['core.normalize_fullwidth_python_punctuation']`
- BLOCKED_UNCLASSIFIED: **0** `[]`
- taxonomy candidate prevalence: **18 / 72**
- candidate window width among failures: **18 / 63**
- rule-applicable window: **PENDING_FROZEN_RULE_APPLICABILITY_AUDIT**
- call_counts: model/healer/retry/API = 0/0/0/0

## Overall (taxonomy candidates)

- taxonomy-level eligible candidates: **18 / 72**
- noneligible: **45 / 72**
- already_passed: **9 / 72**

## By model

- qwen3.5:4b: taxonomy candidates **5 / 36**
- qwen3.5:9b: taxonomy candidates **13 / 36**

## By condition

- ab1: taxonomy candidates **9 / 24**
- ab2g: taxonomy candidates **6 / 24**
- ab2d: taxonomy candidates **3 / 24**

## By task

- ce115_calc_exact_rational_expression_l1: taxonomy candidates **3 / 18**
- ce115_calc_polynomial_division_l1: taxonomy candidates **7 / 18**
- ce115_calc_polynomial_factor_roots_l1: taxonomy candidates **4 / 18**
- ce115_calc_radical_simplification_l1: taxonomy candidates **4 / 18**

## By observed outcome

- answer_incorrect: n=16, taxonomy candidates **0 / 16**
- missing_entry_point: n=7, taxonomy candidates **0 / 7**
- parse_minor: n=18, taxonomy candidates **18 / 18**
- passed: n=9, taxonomy candidates **0 / 9**
- runtime_failure: n=14, taxonomy candidates **0 / 14**
- schema_failure: n=8, taxonomy candidates **0 / 8**

## Model × condition (taxonomy candidates / 12)

- qwen3.5:4b|ab1: **4 / 12**
- qwen3.5:4b|ab2g: **1 / 12**
- qwen3.5:4b|ab2d: **0 / 12**
- qwen3.5:9b|ab1: **5 / 12**
- qwen3.5:9b|ab2g: **5 / 12**
- qwen3.5:9b|ab2d: **3 / 12**

## Taxonomy candidate composition

`{'parse_failure': 18}`

## Explicitly noneligible categories

`{'g4_semantic_oracle_mismatch_excluded': 16, 'g2_runtime_no_enabled_runtime_repair': 14, 'g3_contract_no_enabled_non_semantic_schema_repair': 8, 'already_passed': 9, 'g1_missing_entry_point_no_enabled_entry_point_repair': 7}`

## Boundary notes

- Taxonomy candidate window = G1 `parse_failure` / observed `parse_minor` only.
- These candidates are **not** yet confirmed applicable to frozen Core rule.
- All 16 `answer_incorrect` cells are G4 `oracle_mismatch` → excluded.
- G2 runtime / G3 schema / missing_entry_point have no enabled non-semantic repair family → excluded.
- No Healer repair was executed in this census.
