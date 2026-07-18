# Experimental rule card: `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP`

Status: **experimental_candidate** (production allowlist unchanged)

## Forensic verdict on post-kwargs-inline G4

- Class: `a_format_wrapping`
- 格式/包裝層錯誤：值（經 json.loads + 符號翻轉等價）通過 oracle，但 correct_answer 以 json.dumps 字串回傳導致 oracle 拒收
- Raw type: `str`
- Oracle on raw: `is_correct=False`
- Oracle on parsed dict: `is_correct=True`

## 9-field provenance (apply on repaired candidate)

| Field | Value |
|---|---|
| rule_id | `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP` |
| layer | L2 |
| guards | see summary.json target_chain.rule_result.guards |
| transform | unwrap `json.dumps(<expr>)` → `<expr>` on return `correct_answer` |
| triggered | True |
| changed | True |
| reason | unwrapped_json_dumps_correct_answer |
| before_hash / after_hash | `4d05a9ff1a3a418bf05a659d1296d8a89912ceab892b8e2d1f4317b65d496394` / `0dfdb8e77440afd7cf2ecf52ab0cee1874c319ad05509cb14ccbb8d81dc68671` |
| validation | reparse_ok + post_unwrap_clean + correct_answer present |

## Safety argument

1. Generator contract requires `correct_answer` to be a JSON-compatible object (dict), not `str`.
2. `json.dumps(expr)` always produces `str` — structurally wrong return type.
3. Transform only removes the dumps wrapper; inner AST expression is unchanged (no invented values).
4. Guards: single `generate`, return dict, `correct_answer` is `json.dumps` with one positional arg, `import json` present.
5. No task_id / exam numerics / snippets; no oracle/evaluator used to accept/reject.
6. Transactional reparse + post-condition (no longer dumps) or rollback.

## Held-out regression

- regression_pass: True
- pass misfires: 0
- other-fail misfires: 0
- same-pattern expected (v2 113-10 Ab2d original): 1
- rescue_to_pass after chain: True
