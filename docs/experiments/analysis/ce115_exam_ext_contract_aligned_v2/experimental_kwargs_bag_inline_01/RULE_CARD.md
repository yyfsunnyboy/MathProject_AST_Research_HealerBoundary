# Experimental rule card: `L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM`

Status: **experimental_candidate** (production allowlist unchanged)

## 9-field provenance (target apply)

| Field | Value |
|---|---|
| rule_id | `L2_KWARGS_EMPTY_BAG_INLINE_UNIQUE_PARAM` |
| layer | L2 |
| guards | see summary.json target_113_10.rule_result.guards |
| transform | replace `kwargs.get(K, {})` RHS with literal unique covering param bag |
| triggered | True |
| changed | True |
| reason | inlined_unique_covering_param_bag |
| before_hash / after_hash | `83902452cc616115ac671ed0b06375e6f824db935487c353c0da41a79c2291f6` / `4d05a9ff1a3a418bf05a659d1296d8a89912ceab892b8e2d1f4317b65d496394` |
| validation | reparse_ok + correct_answer fingerprint unchanged |

## Safety argument (why unique covering bag is safe)

1. Evaluation invokes `generate(level=...)` without kwargs (empty `kwargs`).
2. Pattern `bag = kwargs.get(K, {})` therefore always binds `{}` at runtime.
3. Subsequent `bag[static_key]` reads are statically enumerated as set `S`.
4. Available parameter bags are defined as the singleton universe `{context.frozen}`.
5. Trigger requires `|{ B in universe : S ⊆ keys(B) }| == 1` (fail-closed uniqueness).
6. Transform only inlines that unique bag as a literal; invents no keys/values.
7. `correct_answer` AST/text fingerprint must be unchanged; else rollback.
8. Re-parse must succeed; else rollback.
9. Guards contain no task_id, exam numerics, or candidate snippets.

## Held-out regression

- regression_pass: True
- pass misfires: 0
- other-fail misfires: 0
- rescue_to_pass (report-only): False
