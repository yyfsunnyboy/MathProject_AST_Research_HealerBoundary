# Math16 統整總表:三模型 × 16 題 × 三條件(含 Ab3 結果)

資料來源:`math16_ab3_full_report.md`(凍結基準 `d9aa264c`,Gemini 口徑 = evaluation_revision_003 平反後)

**格內代碼**:
- `PASS` = H0 通過(Ab3 identity reuse,不經 Healer)
- `F-ans` = ANSWER_INCORRECT(語意層,答案錯,非 Healer eligible)
- `F-parse` = PARSE_MINOR(語法錯誤)
- `F-exec` = EXECUTION_FAILURE(執行期錯誤)
- `F-struct` = STRUCTURAL_MISMATCH(回傳結構不符合約)
- `F-schema` = SCHEMA_FAILURE(schema 打包錯誤)
- `F-latex` = LATEX_MISMATCH
- `F-extract` = EXTRACTION_FAILURE / `F-entry` = MISSING_ENTRY_POINT(無程式結構,Ab3 排除)
- `F-parse→EXPOSE` = Ab3 觸發修復,語法修好但重評仍 FAIL(layer_exposure)
- 所有未標 EXPOSE 的 FAIL 格,Ab3 結果均為 no_trigger(6 條規則零觸發)

---

## Gemini 3.5 Flash(40/48 PASS)

| # | 題目 | Ab1 | Ab2g | Ab2d |
|---|---|---|---|---|
| 1 | ce111_q01_exponential_growth | PASS | PASS | PASS |
| 2 | ce111_q02_polynomial_division_remainder | F-ans | F-ans | F-ans |
| 3 | ce111_q03_prime_factor_selection | PASS | PASS | PASS |
| 4 | ce111_q05_exact_fraction_expression | PASS | PASS | PASS |
| 5 | ce111_q08_polynomial_factor_param_recovery | F-ans | F-ans | PASS |
| 6 | ce111_q10_ordered_quadratic_roots_radical | PASS | PASS | PASS |
| 7 | ce112_q01_negative_integer_power | PASS | PASS | PASS |
| 8 | ce112_q04_radical_simplification | PASS | PASS | F-latex |
| 9 | ce112_q09_divisor_multiple_intersection | PASS | PASS | PASS |
| 10 | ce112_q12_independent_probability_fraction | PASS | PASS | PASS |
| 11 | ce113_q01_negative_fraction_subtraction | PASS | PASS | PASS |
| 12 | ce113_q11_rationalize_denominator | F-parse | PASS | PASS |
| 13 | ce115_calc_exact_rational_expression | PASS | PASS | PASS |
| 14 | ce115_calc_polynomial_division | PASS | PASS | PASS |
| 15 | ce115_calc_polynomial_factor_roots | PASS | PASS | F-exec |
| 16 | ce115_calc_radical_simplification | PASS | PASS | PASS |

**統計**:PASS 40|F-ans 5|F-latex 1|F-parse 1|F-exec 1|Ab3 觸發 0

---

## Qwen 3.5 4B(6/48 PASS)

| # | 題目 | Ab1 | Ab2g | Ab2d |
|---|---|---|---|---|
| 1 | ce111_q01_exponential_growth | F-ans | F-ans | F-exec |
| 2 | ce111_q02_polynomial_division_remainder | F-ans | F-ans | F-ans |
| 3 | ce111_q03_prime_factor_selection | F-parse | F-exec | F-exec |
| 4 | ce111_q05_exact_fraction_expression | F-exec | F-parse | F-exec |
| 5 | ce111_q08_polynomial_factor_param_recovery | PASS | F-exec | F-extract |
| 6 | ce111_q10_ordered_quadratic_roots_radical | F-ans | F-parse | F-parse |
| 7 | ce112_q01_negative_integer_power | PASS | PASS | F-ans |
| 8 | ce112_q04_radical_simplification | F-struct | F-exec | F-parse |
| 9 | ce112_q09_divisor_multiple_intersection | F-parse | F-ans | F-parse |
| 10 | ce112_q12_independent_probability_fraction | F-parse | F-parse | F-struct |
| 11 | ce113_q01_negative_fraction_subtraction | PASS | PASS | F-exec |
| 12 | ce113_q11_rationalize_denominator | F-parse | F-exec | F-entry |
| 13 | ce115_calc_exact_rational_expression | F-parse | F-parse | F-parse |
| 14 | ce115_calc_polynomial_division | F-parse | F-parse | PASS |
| 15 | ce115_calc_polynomial_factor_roots | F-exec | **F-parse→EXPOSE** | F-parse |
| 16 | ce115_calc_radical_simplification | F-struct | F-struct | F-parse |

**統計**:PASS 6|F-parse 17(含 1 EXPOSE)|F-exec 10|F-ans 8|F-struct 4|F-extract 1|F-entry 1|Ab3 觸發 1(layer_exposure)

---

## Qwen 3.5 9B(7/48 PASS)

| # | 題目 | Ab1 | Ab2g | Ab2d |
|---|---|---|---|---|
| 1 | ce111_q01_exponential_growth | F-ans | F-ans | F-ans |
| 2 | ce111_q02_polynomial_division_remainder | F-ans | F-ans | F-ans |
| 3 | ce111_q03_prime_factor_selection | F-ans | PASS | F-ans |
| 4 | ce111_q05_exact_fraction_expression | F-schema | F-exec | F-exec |
| 5 | ce111_q08_polynomial_factor_param_recovery | F-ans | F-exec | F-parse |
| 6 | ce111_q10_ordered_quadratic_roots_radical | F-ans | F-parse | F-parse |
| 7 | ce112_q01_negative_integer_power | PASS | PASS | F-entry |
| 8 | ce112_q04_radical_simplification | F-struct | F-exec | F-exec |
| 9 | ce112_q09_divisor_multiple_intersection | F-ans | PASS | PASS |
| 10 | ce112_q12_independent_probability_fraction | F-struct | PASS | F-latex |
| 11 | ce113_q01_negative_fraction_subtraction | PASS | F-parse | F-parse |
| 12 | ce113_q11_rationalize_denominator | F-ans | F-ans | F-ans |
| 13 | ce115_calc_exact_rational_expression | F-struct | F-parse | F-parse |
| 14 | ce115_calc_polynomial_division | F-parse | F-parse | F-parse |
| 15 | ce115_calc_polynomial_factor_roots | F-parse | F-parse | F-parse |
| 16 | ce115_calc_radical_simplification | F-schema | F-ans | **F-parse→EXPOSE** |

**統計**:PASS 7|F-parse 15(含 1 EXPOSE)|F-ans 15|F-exec 6|F-struct 3|F-schema 2|F-latex 1|F-entry 1|Ab3 觸發 1(layer_exposure)

---

## 三模型彙總對照

| | Gemini 3.5 Flash | Qwen 3.5 4B | Qwen 3.5 9B |
|---|---:|---:|---:|
| PASS(通過率) | 40(83.3%) | 6(12.5%) | 7(14.6%) |
| FAIL 總數 | 8 | 42 | 41 |
| — 語意層(F-ans) | 5 | 8 | 15 |
| — 結構/語法層(parse+struct+schema+latex) | 3 | 22 | 21 |
| — 執行層(F-exec) | 1 | 10 | 6 |
| — 無程式結構(extract/entry) | 0 | 2 | 2 |
| Healer eligible | 8* | 34 | 26 |
| Ab3 觸發 | 0 | 1 | 1 |
| layer_exposure | 0 | 1 | 1 |
| rescue_to_pass | 0 | 0 | 0 |
| 預測命中率 | 48/48 | 48/48 | 48/48 |

*Gemini 8 格 FAIL 全數過完整 6 條規則 Healer,零觸發(失敗全在語意層,結構規則無作用對象)。

## 數字對照速查

| 數字 | 定義 |
|---|---|
| 16 | 題數 |
| 48 | 一模型全部格(16 題 × Ab1/Ab2g/Ab2d 三條件) |
| 144 | 三模型全量(Ab3 正式輪範圍) |
| 60 | Qwen Healer eligible(4B 34 + 9B 26,不含 ANSWER_INCORRECT 語意層格) |
| 57 | 60 排除 3 格無程式結構者(qualification 實跑數) |
