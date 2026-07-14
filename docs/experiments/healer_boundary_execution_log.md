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

---

## Milestone 2A — Corrected Task ID and Fixture Alignment

### Goal

Align formal pilot / smoke loaders and tests to the corrected `ce115_calc_*`
four-task L1 set so runners and tests load the same authoritative IDs without
model runs, prompt changes, or oracle redesign.

### Authoritative corrected task IDs

Family prefixes (design):

- `ce115_calc_radical_simplification`
- `ce115_calc_exact_rational_expression`
- `ce115_calc_polynomial_division`
- `ce115_calc_polynomial_factor_roots`

Formal L1 rows actually loaded (manifest task_id, preferred over bare family ID):

- `ce115_calc_radical_simplification_l1`
- `ce115_calc_exact_rational_expression_l1`
- `ce115_calc_polynomial_division_l1`
- `ce115_calc_polynomial_factor_roots_l1`

### Legacy task exclusion rule

- Old `ce115_cr01_training_sequence_threshold_l3` and other non-`ce115_calc_*`
  rows may remain in the shared fixture as historical content.
- Formal `load_pilot_tasks` / Ab2d smoke selection return only the corrected
  four L1 IDs in deterministic TASK_IDS order.
- Missing formal IDs or duplicate task_id values fail explicitly; extra legacy
  rows are ignored, never mixed into the formal set.

### Files changed

| Path | Purpose |
|---|---|
| `agent_tools/finals_rebuild/math_boundary_pilot.py` | Corrected TASK_IDS + stricter/missing-aware loader |
| `scripts/run_ab2d_minimal_smoke.py` | Smoke task set = shared formal TASK_IDS |
| `tests/finals_rebuild/test_math_boundary_pilot.py` | Alignment + loader contract tests |
| `tests/finals_rebuild/test_ab2d_minimal_smoke_runner.py` | Assert smoke uses corrected four-task set |
| `docs/experiments/healer_boundary_execution_log.md` | Milestone 2A record |

### Tests

```powershell
python -m pytest tests/finals_rebuild/test_math_boundary_pilot.py tests/finals_rebuild/test_ab2d_minimal_smoke_runner.py --basetemp .pytest_tmp_m2a -v
```

- 18 passed; exit code 0

```powershell
python -m pytest tests/finals_rebuild/test_generator_success.py tests/finals_rebuild/test_generator_success_integration.py tests/finals_rebuild/test_generator_success_artifacts.py --basetemp .pytest_tmp_m2a_success -q
```

- 34 passed; exit code 0

### Remaining gaps

- corrected `ce115_calc_*` 正式 run 尚未執行
- Ab1 prompt still lacks per-family answer-contract text for the new calc
  oracles (no prompt rewrite in 2A)
- 真 LaTeX renderer / 人工 readability / 真實 post-Healer replay 仍是 gap
- 歷史 JSONL / legacy fixture rows are retained, not rewritten

### Status

Milestone 2A corrected task-id / fixture alignment completed.
No commit or push was made.

---

## Milestone 2B — Corrected Four-Task Reconstruction Readiness

### Goal

Complete source alignment, frozen-parameter / contract / independent-oracle /
golden-generator / G1–G6 readiness for the corrected four L1 calc tasks without
model runs, prompt changes, or formal dry runs.

### Formal task IDs

- `ce115_calc_radical_simplification_l1`
- `ce115_calc_exact_rational_expression_l1`
- `ce115_calc_polynomial_division_l1`
- `ce115_calc_polynomial_factor_roots_l1`

### Readiness matrix

| task_id | source alignment | frozen parameters | answer contract | oracle | golden generator | G1–G6 ready |
|---|---|---|---|---|---|---|
| `ce115_calc_radical_simplification_l1` | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE |
| `ce115_calc_exact_rational_expression_l1` | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE |
| `ce115_calc_polynomial_division_l1` | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE |
| `ce115_calc_polynomial_factor_roots_l1` | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE | COMPLETE |

Initial inventory before 2B golden work: source/frozen/contract/oracle were already
COMPLETE via design + sampler + contracts + `math_task_oracles`; golden generate()
and end-to-end G1–G6 were ABSENT and are now filled.

### Source-alignment decisions

- Families map to CAP Q3/Q5/Q7/Q9 skills, not hard-coded single-question answers.
- Formal set remains L1 only; legacy `ce115_cr01_*` / alternating stay excluded.
- Calc roots family validates ordered rational roots only; CAP linear-combination
  stays outside this reconstruction.

### Oracle/golden decisions

- Reused existing independent oracles; no parallel oracle layer.
- Golden generators are tests-only helpers that sample frozen payloads at
  `GOLDEN_SEED`, recompute answers via oracle, and emit non-leaking question text
  under a fixed non-LaTeX notation policy.
- Golden sources are asserted absent from Ab1/Ab2g/`render_answer_contract` text.

### Files changed

| Path | Purpose |
|---|---|
| `tests/finals_rebuild/ce115_calc_golden_generators.py` | Deterministic golden generate()/question builder |
| `tests/finals_rebuild/test_ce115_calc_reconstruction_readiness.py` | Readiness + invariant + G1–G6 coverage |
| `docs/experiments/ce115_computation_task_design.md` | Formal L1 IDs + reconstruction notes |
| `docs/experiments/healer_boundary_execution_log.md` | Milestone 2B record |
| (carry-over from 2A) pilot/smoke alignment files | Unchanged in purpose from 2A |

### Tests

```powershell
python -m pytest tests/finals_rebuild/test_math_boundary_pilot.py tests/finals_rebuild/test_ab2d_minimal_smoke_runner.py tests/finals_rebuild/test_ce115_calc_reconstruction_readiness.py --basetemp .pytest_tmp_m2b -v
```

- 48 passed; exit code 0

```powershell
python -m pytest tests/finals_rebuild/test_generator_success.py tests/finals_rebuild/test_generator_success_integration.py tests/finals_rebuild/test_generator_success_artifacts.py --basetemp .pytest_tmp_m2b_success -q
```

- 34 passed; exit code 0

### Remaining gaps

- corrected `ce115_calc_*` 正式 dry run / model qualification 尚未執行
- Ab1 still lacks per-family answer-contract prose for calc oracles (prompt
  frozen; contracts available via `render_answer_contract` for Ab2d paths)
- 真 LaTeX renderer 尚未納入
- 人工 readability rubric 尚未納入
- 真實 post-Healer replay 尚未執行

### Status

Milestone 2B reconstruction readiness completed.
No commit or push was made.

---

## Milestone 2C — No-Model Infrastructure Dry Run

### Goal

Run a no-model infrastructure dry run over the corrected four L1 calc tasks
using tests/infrastructure golden generators, confirming the existing
classify/success-field pipeline emits G1–G6 full-PASS serializable artifacts.

### Dry-run exclusion policy

- `run_type = infrastructure_dry_run`
- `included_in_formal_analysis = false`
- `model_called = false`
- `model_tag = synthetic_golden_no_model`
- `request_count = 0`, `retry_count = 0`
- `ledger_stage = observed` only (no synthetic pipeline/post-healer rows)
- Refuse writes under `docs/experiments/results`
- `record_eligible_for_formal_analysis()` excludes these records

### Formal task IDs

- `ce115_calc_radical_simplification_l1`
- `ce115_calc_exact_rational_expression_l1`
- `ce115_calc_polynomial_division_l1`
- `ce115_calc_polynomial_factor_roots_l1`

### Artifact fields verified

task_id, run_id, run_type, included_in_formal_analysis, model_called,
model_tag, request_count, retry_count, ledger_stage,
raw_first_attempt_output, candidate_extracted, actual_question_text,
evaluation_gates g1–g6, composite_outcomes, oracle_pass/failure_category,
JSON serializable.

### Result

- records = 4
- full PASS = 4/4
- model/API calls = 0
- Manual offline command wrote under `.pytest_tmp_m2c_manual/` then cleaned

### Files changed

| Path | Purpose |
|---|---|
| `agent_tools/finals_rebuild/ce115_calc_golden_generators.py` | Shared golden helpers (moved from tests/) |
| `agent_tools/finals_rebuild/ce115_calc_golden_dry_run.py` | No-model dry-run pipeline |
| `scripts/run_ce115_calc_golden_dry_run.py` | Offline CLI entrypoint |
| `tests/finals_rebuild/test_ce115_calc_golden_dry_run.py` | Dry-run artifact / exclusion tests |
| `tests/finals_rebuild/test_ce115_calc_reconstruction_readiness.py` | Import shared golden module |
| `docs/experiments/healer_boundary_execution_log.md` | Milestone 2C record |

### Tests

```powershell
python -m pytest tests/finals_rebuild/test_math_boundary_pilot.py tests/finals_rebuild/test_ab2d_minimal_smoke_runner.py tests/finals_rebuild/test_ce115_calc_reconstruction_readiness.py tests/finals_rebuild/test_ce115_calc_golden_dry_run.py --basetemp .pytest_tmp_m2c -v
```

- 53 passed; exit code 0

```powershell
python -m pytest tests/finals_rebuild/test_generator_success.py tests/finals_rebuild/test_generator_success_integration.py tests/finals_rebuild/test_generator_success_artifacts.py --basetemp .pytest_tmp_m2c_success -q
```

- 34 passed; exit code 0

### Remaining gaps

- 正式模型 run 尚未執行
- Ab1 calc 專屬 answer-contract wording 尚未凍結
- 真 renderer 未納入
- 人工 readability rubric 未納入
- 真實 post-Healer replay 未執行

### Status

Milestone 2C no-model infrastructure dry run completed.
No commit or push was made.

---

## Milestone 2 Closeout — Corrected Four-Task Readiness

- Milestone 2A / 2B / 2C completed
- Antigravity read-only audit passed (READY FOR MILESTONE 2 CLOSEOUT)
- Formal task IDs:
  - `ce115_calc_radical_simplification_l1`
  - `ce115_calc_exact_rational_expression_l1`
  - `ce115_calc_polynomial_division_l1`
  - `ce115_calc_polynomial_factor_roots_l1`
- Final tests: 53 + 34 passed
- No-model dry run: 4/4 Full PASS
- Model/API calls: 0
- Remaining gaps:
  - 正式模型 run 尚未執行
  - Ab1 calc answer-contract wording 尚未凍結
  - 真 LaTeX renderer 尚未納入
  - 人工 readability rubric 尚未納入
  - 真實 post-Healer replay 尚未執行
- Commit/push: completed in this closeout to `origin main` only

### Status

Milestone 2 closeout completed.
