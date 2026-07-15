# CE115 Frozen-Rule Applicability Audit

- rule: `core.normalize_fullwidth_python_punctuation`
- taxonomy candidates audited: **18**
- RULE_APPLICABLE: **0 / 18**
- RULE_NOT_APPLICABLE: **18 / 18**
- PIPELINE_SUSPECT: **0 / 18**
- INSUFFICIENT_EVIDENCE: **0 / 18**
- frozen-rule applicable window among failures: **0 / 63**
- frozen-rule applicable window among total: **0 / 72**
- verified rescue pool: **0**
- Healer replay: **not executed** (no RULE_APPLICABLE cells)

## Distinction (do not conflate)

- **taxonomy-level candidate window:** **18 / 63** among failures (and **18 / 72** among total). This is a morphology/taxonomy filter only — **not** a repairable or intervention window.
- **frozen-rule applicable window:** **0 / 63** among failures (and **0 / 72** among total).
- The count **18** must **not** be described as a healable/repairable/intervention set under the currently frozen single Core rule.

## Formal conclusion

Currently frozen single Core rule `core.normalize_fullwidth_python_punctuation` matched no formal Qwen3.5 confirmatory failures; this is Healer **rule-coverage mismatch** vs failure morphology, **not** invalid taxonomy/formal run.

目前凍結的單一 Core 規則 `core.normalize_fullwidth_python_punctuation` 未匹配任何正式 Qwen3.5 confirmatory 失敗；此為 Healer **規則覆蓋與失敗型態不符**，而非 taxonomy／正式 run 無效。

## Rule gaps (exploratory only)

Gap tag counts (tags may **overlap** on the same cell and **must not** be summed as unique cells):

- `halfwidth_or_other_syntax_error`: 11
- `indentation_error`: 10
- `truncated_trailer_token`: 5

These gap tags are **exploratory future-work signals only**, not a confirmatory gate and not evidence for unfreezing or adding repair rules in this closeout.

## Downgraded cells

- `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071301`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301`: **RULE_NOT_APPLICABLE** — no_supported_fullwidth_and_indentation_error gaps=['indentation_error', 'indentation_error']
- `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071302`: **RULE_NOT_APPLICABLE** — no_supported_fullwidth_and_indentation_error gaps=['indentation_error', 'indentation_error']
- `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303`: **RULE_NOT_APPLICABLE** — no_supported_fullwidth_and_indentation_error gaps=['indentation_error', 'indentation_error']
- `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301`: **RULE_NOT_APPLICABLE** — no_supported_fullwidth_and_indentation_error gaps=['truncated_trailer_token', 'indentation_error', 'indentation_error']
- `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026071302`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2g__seed_2026071302`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071301`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071302`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab1__seed_2026071303`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302`: **RULE_NOT_APPLICABLE** — no_supported_fullwidth_and_truncated_trailer_token gaps=['truncated_trailer_token', 'truncated_trailer_token']
- `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071301`: **RULE_NOT_APPLICABLE** — no_supported_fullwidth_and_truncated_trailer_token gaps=['truncated_trailer_token', 'truncated_trailer_token']
- `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071302`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2g__seed_2026071303`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab1__seed_2026071301`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071302`: **RULE_NOT_APPLICABLE** — parse_fail_without_supported_fullwidth gaps=['halfwidth_or_other_syntax_error']
- `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301`: **RULE_NOT_APPLICABLE** — no_supported_fullwidth_and_indentation_error gaps=['indentation_error', 'indentation_error']

## Representative diffs (applicable only)

- (none)
