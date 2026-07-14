# Milestone 1A — Generator Success Chain Definition

## Goal

Freeze a documentation-only generator success chain (G1–G6), composite
outcomes, ledger definitions, status semantics, failure taxonomy mapping, and
current observability coverage for the Active Healer research repository.

## Starting baseline

- Branch: `main`
- Starting HEAD: `a47bf295c1b8f392341dcccbd9b978aec110e530`
- Working tree: clean
- Origin: `MathProject_AST_Research_HealerBoundary`
- Upstream: `MathProject_AST_Research`

## Decisions frozen

- Evaluation order is G1 Evaluability, G2 Executability, G3 Contract
  Compliance, G4 Semantic Correctness, G5 Problem Presentation Quality, then
  G6 Mathematical Notation Validity.
- Technical Pass is G1–G4; Presentation Pass is G5–G6; Full Pass requires all
  six gates.
- Observed, pipeline-corrected, and post-Healer are separate ledgers.
- PASS, FAIL, NOT_ASSESSED, and NOT_OBSERVED are distinct statuses.
- Missing artifacts and experiments not run are not model failures.
- G5/G6 require actual persisted question text; generated code and evaluator
  summaries are not substitutes.

## Read-only files inspected

| Path | Relevance |
|---|---|
| `agent_tools/finals_rebuild/math_evaluator.py` | Existing extraction, parse, execution, and evaluator-result structures. |
| `agent_tools/finals_rebuild/ollama_generation_runner.py` | Persisted extraction/parse metadata and generation-row fields. |
| `agent_tools/finals_rebuild/math_generation_runner.py` | Prompt construction and generation artifact handling. |
| `docs/experiments/results/*.jsonl` | Existing raw-output/result-field examples. |
| `tests/finals_rebuild/fixtures/math_generation_tasks_ce115_pilot.jsonl` | CE115 task manifests, including corrected `ce115_calc_*` families. |
| `docs/experiments/ce115_computation_task_design.md` | Corrected four-task family definition. |
| `docs/experiments/gemini_ab2g_math_core_l1_seed_20260714_rerun1_forensic_reevaluation.md` | Historical-scope and replacement-task evidence. |

## Observability findings

- G1–G4 have partial evidence through raw response, extraction/parse status,
  candidate source, execution/failure fields, contract checks, and oracle
  results; field availability is not uniform across historical artifacts.
- G5 has no persisted actual emitted `question_text` for the audited completed
  artifacts, so its historical status is NOT_OBSERVED.
- G6 has no persisted LaTeX lint, delimiter, display, parser, or renderer
  evidence, so its historical status is NOT_OBSERVED.
- Corrected `ce115_calc_*` four-task families have no run artifact. They are
  `experiment_not_run / NOT_OBSERVED`; they are not failed runs.

## Files changed

| Path | Purpose |
|---|---|
| `docs/experiments/success_definition.md` | Frozen G1–G6 definition, ledgers, statuses, taxonomy, retro-application policy, and coverage table. |
| `docs/experiments/healer_boundary_execution_log.md` | Milestone 1A baseline, inspected evidence, findings, and checks. |

## Tests / checks

Documentation-only checks required for this milestone:

- `git diff --check`
- Markdown consistency review of the two changed files
- `git status --short`

No Python, evaluator, runner, manifest, JSONL/CSV, test, model, Ollama/Gemini,
or formal evaluator execution was performed.

## Known gaps

- No unified artifact schema records all G1–G6 gate statuses.
- Actual question text is absent from the audited result artifacts.
- LaTeX lint/render evidence is absent.
- Corrected `ce115_calc_*` four-task pilot has not been run and cannot be
  retro-applied.

## Status

Milestone 1A documentation baseline completed. No commit or push was made.

---

## Milestone 1B — Generator Success Chain Observability Implementation

### Goal

Persist additive G1–G6 evaluation gates, composite outcomes, `ledger_stage`,
and `actual_question_text` on every new generator-run artifact without changing
prompts, manifests, oracle answers, or historical JSONL.

### Starting baseline

- Branch: `main`
- HEAD: `a47bf295c1b8f392341dcccbd9b978aec110e530`
- Pre-existing untracked helpers from Milestone 1A follow-on:
  `generator_success.py`, `test_generator_success.py`,
  `success_definition.md`, and this execution log
- Origin / upstream unchanged

### Existing helper reused

- Reused G5 `evaluate_problem_presentation`, G6 `evaluate_math_notation`, and
  `composite_outcomes` from `generator_success.py`
- Flattened gate evidence to top-level fields; fixed G3/G4 mapping so schema
  and oracle are no longer conflated
- Added outcome→gate mapper, `assemble_observed_success_fields`,
  `merge_success_fields`, and tolerant `read_success_fields`

### Integration decisions

- Primary assembly point is `math_boundary_pilot.classify_response`, which already
  sees the entry-point return value and writes into pilot / qualification JSONL
- `actual_question_text` comes only from the returned dict’s `question_text`
- Qualification scripts merge the four additive fields without deleting legacy keys
- Schema supports `observed` / `pipeline_corrected` / `post_healer`; new runs set
  `ledger_stage = observed` only

### Files changed

| Path | Purpose |
|---|---|
| `agent_tools/finals_rebuild/generator_success.py` | Gate mapping, assembly, G5/G6 reuse |
| `agent_tools/finals_rebuild/math_boundary_pilot.py` | Emit success-chain fields from classify |
| `scripts/run_gemini_ab2g_math_core_qualification.py` | Merge additive fields into JSONL rows |
| `scripts/run_gemini_ab1_ab2d_diagnostic.py` | Merge additive fields into JSONL rows |
| `scripts/run_ab2d_minimal_smoke.py` | Merge additive fields into JSONL rows |
| `scripts/run_ollama_math_track_qualification.py` | Merge additive fields into JSONL rows |
| `tests/finals_rebuild/test_generator_success.py` | Retained pure helper assertions |
| `tests/finals_rebuild/test_generator_success_integration.py` | Targeted integration coverage |
| `docs/experiments/healer_boundary_execution_log.md` | Milestone 1B record |

### Gate coverage

| Gate | Coverage |
|---|---|
| G1 | COMPLETE for new classify-path artifacts |
| G2 | COMPLETE for new classify-path artifacts |
| G3 | COMPLETE for observed schema/frozen-payload checks; signature evidence remains null when not checked |
| G4 | COMPLETE via existing oracle verdict mapping |
| G5 | COMPLETE when `actual_question_text` is present; otherwise NOT_OBSERVED |
| G6 | COMPLETE delimiter/brace/malformed lint only; no renderer |

### Tests

Commands:

```powershell
python -m pytest tests/finals_rebuild/test_generator_success.py tests/finals_rebuild/test_generator_success_integration.py --basetemp .pytest_tmp_m1b -v
```

- Assertion results: 14 passed (3 helper + 11 integration)
- Pytest exit code: 0
- Teardown status: clean under repo-local `.pytest_tmp_m1b`

### Pytest temp issue

Prefer `--basetemp .pytest_tmp_m1b` so Windows `%TEMP%` permission teardown does
not obscure assertion results. Assertion pass/fail and process exit code are
reported separately.

### Remaining gaps

- True LaTeX renderer validation is not implemented
- Human readability rubric is not part of automatic G5
- Corrected `ce115_calc_*` formal runs have not been executed
- Historical artifacts are not backfilled with the new fields

### Status

Milestone 1B observability implementation completed for new generator artifacts.
No commit or push was made.

---

## Milestone 1C — Synthetic Artifact and Three-Ledger Validation

### Goal

Validate full artifact schema, G1–G6 gates, composite outcomes, and
observed / pipeline_corrected / post_healer three-ledger separation with
synthetic tests only — no model, API, or formal experiment runs.

### Synthetic scenarios

1. Observed full success (G1–G6 / technical / presentation / full PASS)
2. Observed runtime failure (G2 FAIL; G3/G4 NOT_ASSESSED; G5/G6 NOT_OBSERVED)
3. Observed semantic failure (G4 FAIL; presentation PASS; technical/full FAIL)
4. Presentation failure (G6 FAIL; technical PASS; presentation/full FAIL)
5. Experiment not run (all NOT_OBSERVED; distinct from generator failure)
6. Pipeline-corrected independent record (source_record_id, correction_actions,
   raw_first_attempt_output preserved)
7. Post-Healer rescued (eligible/attempted/rescued; observed unchanged)
8. Post-Healer ineligible (attempted forced false; no repaired candidate)
9. Healer regression (attempted/regression; prior ledgers untouched)
10. Backward compatibility (legacy records missing new fields do not crash /
    auto-FAIL)

### Three-ledger decisions

- Ledgers are independent records: `observed`, `pipeline_corrected`,
  `post_healer`
- Non-observed rows require `source_record_id` pointing at the observed record
- `correction_actions` are recorded on pipeline rows; oracle answers never edit
  candidates
- Healer metadata uses `eligible` / `attempted` / `rescued` / `regression` /
  `reason` / `actions`; ineligible never counts as attempted and must not
  invent repaired candidates
- Additive JSON-safe builders: `build_generator_artifact`,
  `derive_pipeline_corrected_record`, `derive_post_healer_record`

### Files changed

| Path | Purpose |
|---|---|
| `tests/finals_rebuild/test_generator_success_artifacts.py` | Synthetic schema / three-ledger / taxonomy coverage |
| `agent_tools/finals_rebuild/generator_success.py` | Minimal additive three-ledger helpers and ineligible/regress rules |
| `docs/experiments/healer_boundary_execution_log.md` | Milestone 1C record |

### Tests

```powershell
python -m pytest tests/finals_rebuild/test_generator_success.py tests/finals_rebuild/test_generator_success_integration.py tests/finals_rebuild/test_generator_success_artifacts.py --basetemp .pytest_tmp_m1c -v
```

- Assertion results: 34 passed
- Pytest exit code: 0

### Schema coverage

- Gate statuses restricted to PASS / FAIL / NOT_ASSESSED / NOT_OBSERVED
- `actual_question_text` is str or null; artifacts must `json.dumps`
- Exceptions persist as type/message strings only
- Taxonomy: empty_response / parse_failure → G1; execution_failure → G2;
  contract_schema_failure → G3; oracle_mismatch → G4; question_missing →
  presentation NOT_OBSERVED; placeholder_leak → G5; latex_delimiter_failure → G6

### Remaining gaps

- corrected `ce115_calc_*` 正式 run 尚未執行
- 真 LaTeX renderer 尚未納入
- 人工 readability rubric 尚未納入
- 真實 post-Healer replay 尚未執行
- 歷史 artifact 不 retroactively 補欄位

### Status

Milestone 1C synthetic artifact and three-ledger validation completed.
No commit or push was made.

---

## Milestone 1 Closeout — Generator Success Chain

### Final files

| Path | Role |
|---|---|
| `docs/experiments/success_definition.md` | Frozen G1–G6 / ledger / taxonomy definition |
| `docs/experiments/healer_boundary_execution_log.md` | Milestone 1A–1C + closeout record |
| `agent_tools/finals_rebuild/generator_success.py` | Pure success-chain + three-ledger helpers |
| `agent_tools/finals_rebuild/math_boundary_pilot.py` | Emit additive success fields from classify |
| `scripts/run_gemini_ab2g_math_core_qualification.py` | Merge success fields into JSONL rows |
| `scripts/run_gemini_ab1_ab2d_diagnostic.py` | Merge success fields into JSONL rows |
| `scripts/run_ab2d_minimal_smoke.py` | Merge success fields into JSONL rows |
| `scripts/run_ollama_math_track_qualification.py` | Merge success fields into JSONL rows |
| `tests/finals_rebuild/test_generator_success.py` | Pure helper tests |
| `tests/finals_rebuild/test_generator_success_integration.py` | Classify-path integration tests |
| `tests/finals_rebuild/test_generator_success_artifacts.py` | Synthetic schema / three-ledger tests |

### Final tests

```powershell
python -m pytest tests/finals_rebuild/test_generator_success.py tests/finals_rebuild/test_generator_success_integration.py tests/finals_rebuild/test_generator_success_artifacts.py --basetemp .pytest_tmp_m1_final -v
```

- 34 passed; exit code 0; teardown clean under `.pytest_tmp_m1_final`

```powershell
python -m pytest tests/finals_rebuild/test_math_boundary_pilot.py tests/finals_rebuild/test_ab2d_minimal_smoke_runner.py --basetemp .pytest_tmp_m1_related -v
```

- 4 passed / 9 failed; exit code 1
- Failures are pre-existing `load_pilot_tasks` missing
  `ce115_cr01_training_sequence_threshold_l3` in the CE115 pilot fixture;
  unrelated to Milestone 1 success-chain changes and not expanded here
- Direct classify / smoke coverage that does not depend on that TASK_IDS gate
  still passed (`unicode` / condition registry / ab2d domain API /
  ab2d smoke runner); Milestone 1 classify-path coverage remains in the
  34 success-chain tests above

### Remaining gaps

- corrected `ce115_calc_*` 正式 run 尚未執行
- 真 LaTeX renderer 尚未納入
- 人工 readability rubric 尚未納入
- 真實 post-Healer replay 尚未執行
- 歷史 artifact 不 retroactively 補欄位
- V6 plan file `20260714旺宏_AST_Healer_分層實驗與邊界驗證計畫_V6.md`
  was not present in this repo; V6 progress update was skipped
- Pre-existing pilot TASK_IDS / fixture mismatch for
  `ce115_cr01_training_sequence_threshold_l3` remains outside Milestone 1

### Commit / push

- Commit hash: recorded in final closeout report after commit
- Push target: `origin main` only (upstream not pushed)

### Status

Milestone 1 closeout ready to commit/push. Commit hash recorded in the
final report rather than amended into this log.
