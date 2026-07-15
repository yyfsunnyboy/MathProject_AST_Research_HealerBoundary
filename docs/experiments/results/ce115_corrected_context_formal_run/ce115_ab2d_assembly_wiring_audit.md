# CE115 Ab2d Assembly Wiring Audit

## Verdict

`ABD2_ASSEMBLY_PARTIALLY_WIRED`. Existing cohort only; no model/healer/repair/replay/retry calls.

## Pipeline

- task/skill_id -> get_required_domains/domain routing
- prompt_builder/scaler -> get_domain_helpers_code(..., stub_mode=True)
- model output -> extracted generated code
- formal runner -> evaluator execution without recorded full library injection/import

## Results

- Cells: 24
- Classification counts: {'API_EXPOSED_BUT_IGNORED': 6, 'ASSEMBLY_COVERAGE_GAP': 6, 'DOMAIN_LOGIC_REIMPLEMENTED': 6, 'INSUFFICIENT_EVIDENCE': 1, 'LIBRARY_RUNTIME_UNAVAILABLE': 5}
- Required API exposure: 12/66
- Required API calls: 0/66
- Domain logic reimplementation: 7/24
- Runtime library availability: 0/24
- Polynomial factor/roots: `ASSEMBLY_COVERAGE_GAP`

- New 24-cell Ab2d-Assembly cohort required: yes.
- Ab1/Ab2g rerun required: no.

## Per-cell evidence

| Cell | Classification | Exposed | Called | Artifact hash |
| --- | --- | --- | --- | --- |
| qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301 | LIBRARY_RUNTIME_UNAVAILABLE | - | - | `cf314eacc08cdafd1fbf3ab222a406f17aeedf769aba2febc8ae14dc46711996` |
| qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071302 | INSUFFICIENT_EVIDENCE | - | - | `39f903b041ad2a397ca85a20014fed815f7cf8ccc3d052d03d489341c7c45ad1` |
| qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071303 | LIBRARY_RUNTIME_UNAVAILABLE | - | - | `6da0a37fa12b3ef3b7a3ce3b8244645349be051b3d7230ae33b3ae098097dede` |
| qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301 | DOMAIN_LOGIC_REIMPLEMENTED | PolynomialOps.div_qr | - | `9eed239033b16db25efb45c115af5fa37381a79910a6fec6fbc44f7ba4040909` |
| qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302 | DOMAIN_LOGIC_REIMPLEMENTED | PolynomialOps.div_qr | - | `c155c51f1685843308b54e96031bbe0934796a36dd2db2b317aaed57136081d5` |
| qwen3_5_4b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071303 | DOMAIN_LOGIC_REIMPLEMENTED | PolynomialOps.div_qr | - | `b1e65f0af665eef91b3857cb335fbb63547e255ce7ea100102158c289a2d3d18` |
| qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301 | ASSEMBLY_COVERAGE_GAP | - | - | `518f6b0d4648fadf59f230322c9ce57c0e7eb455eca3e027bb7a06106c8d50a1` |
| qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071302 | ASSEMBLY_COVERAGE_GAP | - | - | `ce09403f7f4797c04a62aad8750aed8e287933b4cd271b7c491dafaf5f16c57d` |
| qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071303 | ASSEMBLY_COVERAGE_GAP | - | - | `6c1388a413e10d38d3962ebc9208f7147b07915a0fb1ebb5bb150e9aa523527c` |
| qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301 | API_EXPOSED_BUT_IGNORED | RadicalOps | - | `81297cd72bd3ab697ff41718181f63d5ac03bce92a224c623d4f1ad4ca176a56` |
| qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071302 | API_EXPOSED_BUT_IGNORED | RadicalOps | - | `71c9b4f1d46d9efc2f34a21121e0c90453850d32d6037f65a187ce2bd57474f1` |
| qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071303 | API_EXPOSED_BUT_IGNORED | RadicalOps | - | `168d021477550a1d145a168f7ea5b28ef721cb9b1ef0210864ebdc46bfff1c05` |
| qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071301 | LIBRARY_RUNTIME_UNAVAILABLE | - | - | `5733037338777ad4027beafb975958a5377efda2c80736ddf28e695ab4a0f218` |
| qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071302 | LIBRARY_RUNTIME_UNAVAILABLE | - | - | `551682c253f07c7219ddf1085bb3bb3d061c39165d31729b0670e859386105b8` |
| qwen3_5_9b__ce115_calc_exact_rational_expression_l1__ab2d__seed_2026071303 | LIBRARY_RUNTIME_UNAVAILABLE | - | - | `3b3da7672dfa95b53147c7707ab5349aefb1b605edeb42224dc828ff56d39513` |
| qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071301 | DOMAIN_LOGIC_REIMPLEMENTED | PolynomialOps.div_qr | - | `453a303cfdaa2559e9388e6c4e67a9403041b7258bc0db7bda32208fd0ecb5ce` |
| qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071302 | DOMAIN_LOGIC_REIMPLEMENTED | PolynomialOps.div_qr | - | `900e2543515f6b07027b7e7f20b12064cd4d141565e719ac0c8961ecd4e2147b` |
| qwen3_5_9b__ce115_calc_polynomial_division_l1__ab2d__seed_2026071303 | DOMAIN_LOGIC_REIMPLEMENTED | PolynomialOps.div_qr | - | `e5a37295f6827cd8b13c4e6ca7b11ad10eb8a5050af834ad824d3ac559bc6281` |
| qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071301 | ASSEMBLY_COVERAGE_GAP | - | - | `a758e8cebea0001bad3a9279dbb55ef338dfa1952d2b81cc2ec06fb19c8817ee` |
| qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071302 | ASSEMBLY_COVERAGE_GAP | - | - | `d64a428330d151774efba4c3e0ce7a3a1293205c7b1f54f047180da0866a37aa` |
| qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2d__seed_2026071303 | ASSEMBLY_COVERAGE_GAP | - | - | `9a0599b2e806ae28e3326146aa2c29b1e26a50e74cc5d324546400dd52a1bbdd` |
| qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301 | API_EXPOSED_BUT_IGNORED | RadicalOps | - | `cbdf48b94840877281f66478e14d2e37951ebee64ad6b046ea5763ebdd9c8925` |
| qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071302 | API_EXPOSED_BUT_IGNORED | RadicalOps | - | `205ef918ab94023e48ec183d372a1e348a071d707b6571b7f46df0a371f6f9b5` |
| qwen3_5_9b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071303 | API_EXPOSED_BUT_IGNORED | RadicalOps | - | `3fb1499ba24e060e1c623896187aa29f0e50195cc9ad8d730abd6d08d0bdc573` |
