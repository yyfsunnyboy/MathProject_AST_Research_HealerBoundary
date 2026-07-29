# Math16 C5a Tier D D5/D2 Residual Supply Census v1

> **verdict / Go-NoGo:** `GO_IMPLEMENTATION` (nonzero_cross_task_or_condition_supply)
> **residual pool:** C5a still-FAIL **232** / C5a final post-source
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`

## Aggregate

- D5: eligible **1** / ambiguous **3** / ineligible **228**
- D2: eligible **1** / ambiguous **1** / ineligible **230**
- Unique eligible cells: **2**; overlap D5∩D2: **0**
- Priority rule: `TIER_D_RANKED_DOMAIN_METHOD_BINDING_V1`

### Distributions (eligible only)

- D5 by task: `{'ce113_q11_rationalize_denominator': 1}`
- D5 by condition: `{'ab2d': 1}`
- D5 by model: `{'qwen4b': 1}`
- D2 by task: `{'ce111_q08_polynomial_factor_parameter_recovery': 1}`
- D2 by condition: `{'ab2d': 1}`
- D2 by model: `{'qwen4b': 1}`

### vs old C4 census (D5=4, D2=1)

- New D5/D2 eligible: **1** / **1**
- D5 lost: `['qwen3_5_4b__ce111_q05_exact_fraction_expression__ab2d_spec_v2__seed_2026072001', 'qwen3_5_4b__ce111_q05_exact_fraction_expression__ab2d_spec_v2__seed_2026072002', 'qwen3_5_4b__ce111_q05_exact_fraction_expression__ab2d_spec_v2__seed_2026072004']`
- D5 gained: `[]`
- D2 lost: `[]`
- D2 gained: `[]`
- Note: Old C4 census marked D5 RANKED_ELIGIBLE without applying §5 score/margin/similarity gates; this census applies frozen ranking strictly on C5a sources.

## Ranking contract (frozen)

- Weights: `{'F_prompt_contract_token': 5, 'F_class_compat': 4, 'F_method_compat': 4, 'F_arity': 3, 'F_keyword_schema': 3, 'F_return_shape': 2, 'F_ast_context': 2, 'F_scaffold_signature': 3, 'F_method_name_similarity': 1}`
- minimum_score=8, minimum_margin=2, similarity sole-decision ban=ON
- Evaluator not used for selection

## Eligible cell ids

- D5: `['qwen3_5_4b__ce113_q11_rationalize_denominator__ab2d__seed_2026072003']`
- D2: `['qwen3_5_4b__ce111_q08_polynomial_factor_parameter_recovery__ab2d__seed_2026072004']`

## Declarations

- Read-only census; no mutation; no post-source produced
- No D4/D6; no model calls; no candidate/evaluator execution
