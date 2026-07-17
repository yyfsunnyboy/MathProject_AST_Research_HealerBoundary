# Task provenance: `ce115_calc_common_factor_quadratic_root_ordering_l1`

Status: clean-incremental formal L1 (prompt freeze + oracle/evaluator + zero-model preflight).
No model calls. No Healer. Does not re-run the existing three calc pilots.

## A. Original exam → task mapping

| Field | Value |
|---|---|
| Source | 115 會考 第 9 題 |
| Original stem | `2x(x+7)-10(x+7)=0` 的兩根為 a、b，且 a>b，求 a+2b |
| Formal task_id | `ce115_calc_common_factor_quadratic_root_ordering_l1` |
| skill_id / oracle_type | `common_factor_quadratic_root_ordering` |
| Historical sibling (unchanged) | `ce115_q09_common_factor_quadratic_root_ordering_l1` |
| Out of scope sibling | `ce115_calc_polynomial_factor_roots_l1` (roots-only; drops a+2b / a>b contract) |

Preserved mathematical structure:

1. Common factor `(x + 7)`
2. Linear factors `(x + 7)` and `(2x - 10)`
3. Solve both roots
4. Order by `a > b`
5. Evaluate `a + 2b`

Not rewritten into a generic quadratic-formula item, sequence, or application problem.

## B. Frozen input schema (unique reconstruction)

```json
{
  "shared_shift": 7,
  "leading_factor": 2,
  "subtracted_factor": 10,
  "root_order": "a>b",
  "linear_combination": {"a": 1, "b": 2}
}
```

Reconstruction identity:

`(leading_factor * x - subtracted_factor) * (x + shared_shift) = 0`

→ `(2x - 10)(x + 7) = 0`

→ `2x(x + 7) - 10(x + 7) = 0` (original stem)

`oracle_payload` must equal this full frozen input exactly.

## C. Correct answer contract

```json
{
  "roots": [5, -7],
  "a": 5,
  "b": -7,
  "value": -9
}
```

- `roots` ordered as `a > b` (a first)
- `a` / `b` labeled under `root_order`
- `value = linear_combination.a * a + linear_combination.b * b`
- Oracle **computes** these from frozen parameters; it does not hardcode `-9`

## D. Evaluator checks

Oracle `common_factor_quadratic_root_ordering` verifies by exact dict equality after computing:

1. Distinct roots from the two linear factors
2. Strict `a > b` ordering
3. `value = coeff_a * a + coeff_b * b`

## E. Prompt composition (clean-incremental)

Shared lineage: `ce115_clean_incremental_ablation_v1`

| Condition | Composition |
|---|---|
| Ab1 | BASE (`build_ab1_prompt`) |
| Ab2g | BASE + shared frozen GENERIC (unchanged text) |
| Ab2d | BASE + GENERIC + task-local DOMAIN (`FractionOps.create` / `mul` / `add`) |

Gemini and Qwen pilots share the same builder; GENERIC is not rewritten for Q9.

## F. Seed

Formal freeze seed: `2026071301` (same seed family as the three-condition pilots).
