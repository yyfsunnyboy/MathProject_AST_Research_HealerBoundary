# General safety Healer coverage (NOT Prompt contract coverage)

> **ARCHIVE NOTICE**
> - 資料來源主要為 V1 FAIL（V2 480-cell 正式重跑前）
> - 此批候選不得直接用於設計 V2 Healer 規則
> - 狀態：PENDING_V2_RESIDUAL_EVIDENCE
> - 下一個 gate：V2 480-cell 正式重跑完成後重新 census

Generated: 2026-08-03T05:35:49.969653+00:00
Baseline commit: `f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4`

These checks are **General safety** — independent of V2 prompt contract text.

## General safety coverage matrix

| contract_id | category | detection | repair | rule/file | action |
|---|---|---|---|---|---|
| GEN_EVAL_EXEC | forbidden_runtime_operations | full | deterministic | core/healers/ast_healer.py::visit_Call (eval/exec → safe_eval) | keep |
| GEN_INPUT | forbidden_runtime_operations | full | deterministic | core/healers/ast_healer.py, core/healers/regex_healer.py | keep |
| GEN_ILLEGAL_IMPORT | illegal_imports | partial | deterministic | core/healers/ast_healer.py::visit_Import/visit_ImportFrom | keep |
| GEN_UNSAFE_LOOP | unsafe_loops | partial | unsafe | core/healers/ast_healer.py (legacy; frozen research healer forbids legacy pipelines) | out_of_scope |
| GEN_SYNTAX_PAREN | generic_syntax_ast_repair | partial | deterministic | L1_CLOSE_UNBALANCED_PARENTHESIS, L1_CLOSE_UNBALANCED_DELIMITER_EXTENDED | keep |
| GEN_PROSE_RESIDUE | generic_syntax_ast_repair | partial | deterministic | L1_PROSE_RESIDUE_NARROW | keep |
| GEN_MARKDOWN_FENCE | generic_syntax_ast_repair | full | deterministic | core/healers/regex_healer.py, agent_tools/finals_rebuild/extraction.py | keep |
| GEN_HALLUCINATED_FUNC | forbidden_runtime_operations | partial | unsafe | core/healers/ast_healer.py (legacy; not in frozen research allowlist) | abstain_only |

## Frozen Math16 research Healer vs legacy core/healers

| Layer | Research healer (frozen) | Legacy core/healers |
|---|---|---|
| Production path | ce115_research_healer_runner.py allowlist L1+L2 | math_healer_runner unified cleanup (legacy) |
| Legacy AST/Regex | **Forbidden** in frozen research protocol | ast_healer.py, regex_healer.py still present read-only |

**Verdict:** General syntax/dangerous-call coverage exists in legacy healers but is **out of scope** for frozen Math16 research Healer production path.

