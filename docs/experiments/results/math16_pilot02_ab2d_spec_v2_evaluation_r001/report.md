# Ab2d+spec-v2 Evaluation r001

Offline re-score of 20 newly generated cells with schema-normalize (v4) oracles.

- LLM calls: `0`
- API cost: `$0.00`
- Pass: `20/20`

## Task v1 vs v2
| task | v1(ab2d_spec) pass | v2(ab2d_spec_v2) pass | delta |
| :--- | ---: | ---: | ---: |
| `ce111_q05_exact_fraction_expression` | 0/5 | 5/5 | +5 |
| `ce112_q12_independent_probability_fraction` | 0/5 | 5/5 | +5 |
| `ce113_q01_negative_fraction_subtraction` | 0/5 | 5/5 | +5 |
| `ce111_q08_polynomial_factor_parameter_recovery` | 5/5 | 5/5 | +0 |

## Global recompute (replace these 4 tasks' ab2d_spec cells)
- Ab2d+spec v1: `63/80`
- Ab2d+spec hybrid (v2 replace): `78/80`
- Ab2d+api: `78/80`
- Gap vs api (v1): `-15`
- Gap vs api (hybrid): `0`
- Overall v4: `289/320` → hybrid `304/320`

AB2D_SPEC_V1_V2_COMPARISON_READY
