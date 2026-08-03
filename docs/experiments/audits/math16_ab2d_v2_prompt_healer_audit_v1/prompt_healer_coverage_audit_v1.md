# Prompt–Healer Coverage Audit (Prompt-derived contracts)

> **ARCHIVE NOTICE**
> - 資料來源主要為 V1 FAIL（V2 480-cell 正式重跑前）
> - 此批候選不得直接用於設計 V2 Healer 規則
> - 狀態：PENDING_V2_RESIDUAL_EVIDENCE
> - 下一個 gate：V2 480-cell 正式重跑完成後重新 census

Generated: 2026-08-03T05:35:49.959564+00:00
Baseline commit: `f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4`

## Prompt-derived contract coverage matrix

| task_id | condition | contract_id | machine | detection | repair | gap | action |
|---|---|---|---|---|---|---|---|
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce115_calc_polynomial_division_l1 | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce115_calc_polynomial_division_l1 | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce115_calc_polynomial_factor_roots_l1 | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce115_calc_exact_rational_expression_l1 | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce115_calc_exact_rational_expression_l1 | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce115_calc_radical_simplification_l1 | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce115_calc_radical_simplification_l1 | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_q02_polynomial_division_remainder | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce111_q02_polynomial_division_remainder | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce111_q08_polynomial_factor_parameter_recovery | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_q03_prime_factor_selection | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce111_q03_prime_factor_selection | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce112_q01_negative_integer_power | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce112_q01_negative_integer_power | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce112_q09_divisor_multiple_intersection | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce112_q09_divisor_multiple_intersection | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce111_nonchoice_q01_part1_exponential_growth | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_q05_exact_fraction_expression | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce111_q05_exact_fraction_expression | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce113_q01_negative_fraction_subtraction | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce113_q01_negative_fraction_subtraction | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce112_q12_independent_probability_fraction | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce112_q12_independent_probability_fraction | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce112_q04_radical_simplification | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce112_q04_radical_simplification | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce111_q10_ordered_quadratic_roots_radical | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_ALLOWED_DOMAIN_APIS | yes | none | none | not_covered | detection_only |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_FORBIDDEN_CROSS_DOMAIN | yes | none | none | not_covered | abstain_only |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_GENERATE_SIGNATURE | yes | none | none | partial | detection_only |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_ZERO_ARG_RUNTIME | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_PROHIBIT_KWARGS_FROZEN | partial | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_FROZEN_LITERAL_BINDING | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_OUTPUT_DICT_KEYS | yes | partial | none | partial | detection_only |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_ORACLE_PAYLOAD_SOURCE | yes | partial | deterministic | narrow_rule | deterministic_repair_candidate |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_CORRECT_ANSWER_SHAPE | yes | partial | deterministic | partial | detection_only |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_DOMAIN_MENU_NO_REQUIRED_API | yes | none | none | not_applicable_by_design | out_of_scope |
| ce113_q11_rationalize_denominator | ab2d_domain_menu_v2 | PC_FORBID_PRESCRIBED_ORDER | yes | none | none | not_applicable_by_design | out_of_scope |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_FULL_REQUIRED_APIS | yes | none | none | not_covered | detection_only |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_FULL_API_CALL_ORDER | partial | none | none | not_covered | abstain_only |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_FULL_RETURN_BINDING | partial | none | none | not_covered | abstain_only |
| ce113_q11_rationalize_denominator | ab2d_full_v2 | PC_FULL_ANSWER_PROVENANCE | partial | none | none | not_covered | abstain_only |

## Healer coverage summary (Prompt-derived only)

- Fully covered (deterministic): **0** distinct contract types
- Narrow / conditional: **4**
- Detection-only or partial: **1**
- Missing: **7**
- Out of scope / abstain: **2**

## Domain-menu vs full-plan contract diff (per task)

### `ce115_calc_polynomial_division_l1`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce115_calc_polynomial_factor_roots_l1`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce115_calc_exact_rational_expression_l1`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce115_calc_radical_simplification_l1`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce111_q02_polynomial_division_remainder`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce111_q08_polynomial_factor_parameter_recovery`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce111_q03_prime_factor_selection`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce112_q01_negative_integer_power`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce112_q09_divisor_multiple_intersection`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce111_nonchoice_q01_part1_exponential_growth`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce111_q05_exact_fraction_expression`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce113_q01_negative_fraction_subtraction`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce112_q12_independent_probability_fraction`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce112_q04_radical_simplification`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce111_q10_ordered_quadratic_roots_radical`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

### `ce113_q11_rationalize_denominator`
- Shared contracts: **9**
- Full-plan-only: **PC_FULL_ANSWER_PROVENANCE, PC_FULL_API_CALL_ORDER, PC_FULL_REQUIRED_APIS, PC_FULL_RETURN_BINDING**

