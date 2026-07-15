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

---

## Milestone 3A — Prompt Conditions and Run Manifest Freeze

### Goal

Freeze Ab1 / Ab2g / Ab2d prompt composition, Ab1 calc answer-contract wording,
deterministic prompt hashes, and the formal run manifest for the corrected four
L1 calc tasks — without any model calls.

### Formal conditions

- Ab1 = Task Contract + Frozen Parameters
- Ab2g = Math Core Scaffold + Task Contract + Frozen Parameters
- Ab2d = Math Core Scaffold + task-local reusable primitive + Task Contract +
  Frozen Parameters

### Ab1 contract decisions

Compact schema-only wording frozen for radical / exact-rational /
poly-division / factor-roots: return fields, types, canonical form, ordering,
exact arithmetic, frozen parameters immutable. No solving steps or answer
constants.

### Hash policy

UTF-8 + LF newline normalization → SHA-256 of final prompt text. Model identity
is excluded from the hashed bytes. Per-task × condition hashes live in the
manifest; shared Math Core / contract / primitive component hashes also recorded.

### Models/seeds resolved vs unresolved

Resolved:
- formal seeds `(2026071301, 2026071302, 2026071303)`
- Ollama 4B/8B tags, digests, quantization, runtime `0.31.2`
- temperature `0.0`, `num_predict=4096` for Ollama paths
- request_count=1, retry_count=0, healer_enabled=false

Unresolved (blocking full freeze):
- Ollama top_p / top_k
- 8B thinking requested/effective
- Gemini exact version string, confirmatory vs exploratory role, temperature/top_p/top_k/thinking
- Gemini cell geometry count

### Files changed

| Path | Purpose |
|---|---|
| `agent_tools/finals_rebuild/ce115_calc_prompt_freeze.py` | Condition assemblers, hashes, manifest builder |
| `docs/experiments/manifests/ce115_calc_main_experiment_manifest.json` | Formal run manifest |
| `tests/finals_rebuild/test_ce115_calc_prompt_freeze.py` | Freeze / composition / hash tests |
| `agent_tools/finals_rebuild/math_boundary_pilot.py` | Additive Ab1 calc answer-contract wording |
| `docs/experiments/ce115_computation_task_design.md` | Condition freeze note |
| `docs/experiments/healer_boundary_execution_log.md` | Milestone 3A record |

### Tests

```powershell
python -m pytest tests/finals_rebuild/test_ce115_calc_prompt_freeze.py tests/finals_rebuild/test_math_boundary_pilot.py tests/finals_rebuild/test_ce115_calc_reconstruction_readiness.py tests/finals_rebuild/test_ce115_calc_golden_dry_run.py --basetemp .pytest_tmp_m3a -q
```

- 63 passed; exit code 0

```powershell
python -m pytest tests/finals_rebuild/test_generator_success.py tests/finals_rebuild/test_generator_success_integration.py tests/finals_rebuild/test_generator_success_artifacts.py --basetemp .pytest_tmp_m3a_success -q
```

- 34 passed; exit code 0

### Blocking unresolved fields

Manifest `unresolved_fields` includes Ollama `top_p`/`top_k`, 8B thinking,
and Gemini version/role/sampling/thinking/cell counts. Therefore
`frozen=false`.

### Status

Milestone 3A completed with verdict **PARTIALLY FROZEN — UNRESOLVED FIELDS**.
No commit or push was made.

## Milestone 3B — Model and Runtime Provenance Resolution

### Goal

Resolve main-experiment manifest model/runtime provenance from existing runners,
saved config, historical artifacts, and read-only local metadata queries — no
model generation requests.

### Resolved fields (local confirmatory)

- Ollama 4B: `qwen3:4b-instruct-2507-q4_K_M`, digest `0edcdef34593`, Q4_K_M,
  runtime Ollama `0.31.2`
- Ollama 8B: `qwen3:8b`, digest `500a1f067a9f`, Q4_K_M, runtime `0.31.2`
- Confirmatory chat request profile (4B and 8B identical):
  - `temperature: 0.0` (explicit)
  - `seed`: per-cell `repeat_seed` (explicit)
  - `top_p` / `top_k` / `num_predict`: `not_explicitly_set` (omitted → Ollama
    runtime default; not substituted from Modelfile)
  - thinking `requested` / `effective`: `not_explicitly_set` (capability listed
    by `ollama show` does not imply enablement)
- Local confirmatory cell count: **72**
  (`4 × 3 × 3 × 2`)
- Gemini analysis role: **exploratory optional cloud comparison** (not part of
  confirmatory 72)

### Evidence sources

- `agent_tools/finals_rebuild/math_boundary_pilot.py`
- `scripts/run_ab2d_minimal_smoke.py`
- `agent_tools/finals_rebuild/math_generation_runner.py`
- `scripts/run_gemini_ab2g_math_core_qualification.py`
- `scripts/run_gemini_ab1_ab2d_diagnostic.py`
- `config.py`, `core/ai_wrapper.py`
- `docs/experiments/ab2g_math_core_qualification_design_20260714.md`
- Read-only: `ollama --version`, `ollama show` (4B/8B)

### runtime_default / not_explicitly_set decisions

- Unset Ollama options are recorded as `not_explicitly_set` with
  `unset_options_rely_on: ollama_runtime_default`
- Do not copy Modelfile `PARAMETER` values into the formal request profile
- Qualification `/api/generate` `num_predict=4096` is non-authoritative for the
  confirmatory `/api/chat` profile

### Gemini role / status

- Role: exploratory optional cloud comparison
- Runner tag `gemini-3.5-flash` vs Config preset model
  `gemini-3-flash-preview` → exact API identifier remains **UNRESOLVED**
- Sampling evidenced where request-built: temperature `0.1`, max_output_tokens
  `4096`; top_p/top_k `not_explicitly_set`; seed `unavailable` in generation
  config; thinking `not_explicitly_set`
- Exploratory / total planned cell counts remain **UNRESOLVED**

### Freeze result

- `local_confirmatory_frozen = true`
- `gemini_exploratory_frozen = false`
- `frozen = false` (single flag must not claim full completion)
- Verdict: **LOCAL CONFIRMATORY FROZEN**

### Tests

```powershell
python -m pytest tests/finals_rebuild/test_ce115_calc_prompt_freeze.py tests/finals_rebuild/test_math_boundary_pilot.py tests/finals_rebuild/test_ce115_calc_reconstruction_readiness.py tests/finals_rebuild/test_ce115_calc_golden_dry_run.py --basetemp .pytest_tmp_m3b -q
```

- 71 passed; exit code 0

```powershell
python -m pytest tests/finals_rebuild/test_generator_success.py tests/finals_rebuild/test_generator_success_integration.py tests/finals_rebuild/test_generator_success_artifacts.py --basetemp .pytest_tmp_m3b_success -q
```

- 34 passed; exit code 0

### Remaining blockers

- Gemini exact API model identifier / SDK version
- Gemini exploratory cell matrix (`exploratory_cloud_cell_count`,
  `total_planned_cell_count`)

### Status

Milestone 3B completed with verdict **LOCAL CONFIRMATORY FROZEN** (Gemini
separately unresolved). No commit or push was made.

## Milestone 3C — Zero-Model Local Confirmatory Preflight

### Goal

Validate that the frozen local confirmatory manifest expands deterministically
into 72 cells with consistent prompts, request settings, output paths, and
artifact schema — without any model calls.

### 72-cell expansion

- Geometry: `4 tasks × 3 conditions × 3 seeds × 2 local models = 72`
- Distribution checks: task 18 / condition 24 / seed 24 / model 36
- No Gemini; no legacy `ce115_cr01_*` tasks
- Deterministic `cell_id` /
  `docs/experiments/results/ce115_calc_local_confirmatory/...jsonl` paths

### Prompt/hash validation

- Prompts rebuilt via `ce115_calc_prompt_freeze` assemblers
- Seed `2026071301` hashes match manifest `per_task_prompt_hashes`
- 4B/8B prompts byte-identical for identical task×condition×seed
- Ab1 / Ab2g / Ab2d composition guards enforced

### Request-setting validation

- `temperature=0.0`, per-cell seed, `request_count=1`, `retry_count=0`,
  `healer_enabled=false`
- `top_p` / `top_k` / `num_predict` / thinking remain `not_explicitly_set`
  (no numeric fill-in; no auto-enable thinking)

### Output-path safety

- Unique deterministic paths under formal confirmatory results directory
- Duplicate path / non-empty existing artifact → fail
- Dry-run does not write formal JSONL results

### Artifact schema readiness

- Planned observed-record skeleton includes required identity, request,
  ledger, evaluation, diagnostics, and commit/manifest hash fields
- Observation fields left `null` (no fabricated model output)

### CLI result

```powershell
python scripts/preflight_ce115_calc_local_confirmatory.py --manifest docs/experiments/manifests/ce115_calc_main_experiment_manifest.json --dry-run
```

- planned_cells=72, duplicates=0, hash/request mismatches=0, model_calls=0,
  verdict=READY

### Tests

```powershell
python -m pytest tests/finals_rebuild/test_ce115_calc_prompt_freeze.py tests/finals_rebuild/test_ce115_calc_run_preflight.py tests/finals_rebuild/test_math_boundary_pilot.py tests/finals_rebuild/test_ce115_calc_reconstruction_readiness.py tests/finals_rebuild/test_ce115_calc_golden_dry_run.py --basetemp .pytest_tmp_m3c -q
```

- 92 passed; exit code 0

```powershell
python -m pytest tests/finals_rebuild/test_generator_success.py tests/finals_rebuild/test_generator_success_integration.py tests/finals_rebuild/test_generator_success_artifacts.py --basetemp .pytest_tmp_m3c_success -q
```

- 34 passed; exit code 0

### Blockers / runner drift notes (do not flip planning READY)

- `math_boundary_pilot` prompt builders still diverge from freeze assemblers
- Pilot does not yet execute the full 72-cell freeze plan in one pass with the
  planned observed success-field write path

### Status

Milestone 3C completed with verdict **READY FOR LOCAL CONFIRMATORY RUN**
(planning preflight). No commit or push was made.

## Milestone 3D — Frozen Plan / Formal Runner Integration

### Goal

Wire the frozen 72-cell local confirmatory plan into a formal Ollama runner path
so prompts come only from plan cells, request payloads match manifest unset
semantics, and observed artifacts assemble via the existing evaluator / G1–G6
pipeline — without live model calls.

### Runner prompt source

- Formal path: `cell.prompt_text` from `ce115_calc_run_plan` expansion
- Integrity: `sha256(prompt_text) == cell.prompt_hash` (+ manifest table for
  freeze seed)
- Legacy `math_boundary_pilot.build_ab*_prompt` not used on confirmatory path

### Payload policy

- `build_ollama_request_payload`: model, messages, `temperature=0.0`, `seed`
- Omit `top_p` / `top_k` / `num_predict` / think when `not_explicitly_set`
- No fill-in from legacy runner defaults; no retries

### Observed artifact schema

- Identity, policy, request provenance, and observed result fields
- Post-execution additive fill via `classify_response` → G1–G6 / composites
- Diagnostics from transport response when present

### Planned vs executed distinction

- `record_state=planned` vs `record_state=executed`
- Formal analysis loader accepts only `executed` local confirmatory rows

### Resume / overwrite policy

- Unique per-cell JSONL under formal confirmatory results dir
- Existing non-empty / duplicate `cell_id` → fail
- Resume skips already-executed cell_ids; does not rewrite them
- Milestone 3D writes only under pytest `tmp_path` in tests

### Tests

```powershell
python -m pytest tests/finals_rebuild/test_ce115_calc_prompt_freeze.py tests/finals_rebuild/test_ce115_calc_run_preflight.py tests/finals_rebuild/test_ce115_calc_formal_runner.py tests/finals_rebuild/test_ce115_calc_reconstruction_readiness.py tests/finals_rebuild/test_ce115_calc_golden_dry_run.py --basetemp .pytest_tmp_m3d -q
```

- 95 passed; exit code 0

```powershell
python -m pytest tests/finals_rebuild/test_generator_success.py tests/finals_rebuild/test_generator_success_integration.py tests/finals_rebuild/test_generator_success_artifacts.py --basetemp .pytest_tmp_m3d_success -q
```

- 34 passed; exit code 0

### CLI plan-only result

```powershell
python scripts/run_ce115_calc_local_confirmatory.py --manifest docs/experiments/manifests/ce115_calc_main_experiment_manifest.json --local-confirmatory --plan-only
```

- planned_cells=72, mismatches/conflicts=0, model_calls=0, verdict=READY

### Remaining blockers

- Live one-cell Ollama smoke not yet run (intentionally out of scope for 3D)
- Live transport injection wrapper for production execute mode not exercised

### Status

Milestone 3D completed with verdict **READY FOR ONE-CELL LIVE SMOKE**.
No commit or push was made.

## Milestone 3R2B — Qwen3.5 Local Cohort Refreeze

### Cohort replacement

Local confirmatory models replaced:

- `qwen3.5:4b` (edge-small; reported 4.7B params; digest `2a654d98e6fb`)
- `qwen3.5:9b` (edge-large; reported 9.7B params; digest `6488c96fa5fa`)

Runtime: Ollama `0.32.0` (model requires `0.17.1`). Quantization Q4_K_M both.
Cell geometry remains `4 × 3 × 3 × 2 = 72` (no 144-cell expansion).

### Thinking policy

- Formal request: top-level `think=false` (explicit)
- Capability: supported (listed by `ollama show`)
- External qualification: `THINK_FALSE_CLEAN`
  (`C:\Temp\qwen35_thinking_qualification`, 2026-07-15, non-formal)
- Does not claim perpetual zero-leakage; Gemini thinking not equated

### Sampling / defaults

Request explicit: temperature `0.0`, per-cell seed, `think=false`.
Not explicitly set: top_p / top_k / presence_penalty / num_predict.
Observed model defaults recorded separately (temp 1, top_k 20, top_p 0.95,
presence_penalty 1.5) and must not enter payloads.

### Historical cohort

`qwen3:4b-instruct-2507-q4_K_M` and `qwen3:8b` retained under
`historical_cohort` / `historical_mechanism_pilot`; excluded from new
confirmatory plan. Old artifact metadata not rewritten.

### Prompt hash invariance

All 12 task×condition SHA-256 values unchanged vs pre-Qwen3.5 freeze baseline.

### 72-cell regeneration

Cell IDs / paths use `qwen3_5_4b` / `qwen3_5_9b` slugs under
`docs/experiments/results/ce115_calc_local_confirmatory/`.

### Tests / CLI

Targeted pytest suites with basetemp `.pytest_tmp_m3r2b*` (no model calls):
99 + 34 passed.
Preflight dry-run and formal runner `--plan-only`: verdict READY,
`model_calls=0`, models `qwen3.5:4b` + `qwen3.5:9b`.

### Remaining blockers

- Live one-cell Ollama smoke not yet run
- Gemini exploratory cells still UNRESOLVED
- 144-cell / extra-task expansion not decided

### Status

Milestone 3R2B completed with verdict
**QWEN3.5 LOCAL COHORT REFROZEN — READY FOR RENDER VALIDATION**.
No commit or push was made.

## Milestone 3E — End-to-End LaTeX Render Validation and HTML Evidence Report

### Goal

Split G6 into G6a (notation lint) / G6b (real browser MathJax) / G6c (human
visual review), and build a rebuildable offline HTML evidence report. No formal
model, Healer, retry, or 72-cell run.

### Formal artifact schema (read-only)

- Planned path: `docs/experiments/results/ce115_calc_local_confirmatory/*.jsonl`
  (empty until live run; report also accepts fixture JSONL)
- Executed keys: `record_state`, `cell_id`, `task_id`, `prompt_condition`,
  `seed`, `model_tag`, `prompt_text`/`prompt_hash`, `raw_first_attempt_output`,
  `candidate_extracted`, `actual_question_text`, `evaluation_gates` (G1–G6),
  `composite_outcomes`, `ledger_stage`, `token_duration_diagnostics`,
  optional `healer`, `retry_count`
- Report overlays do not overwrite formal G1–G5 or formal G6 lint field

### G6 split

| Gate | Meaning | PASS rule |
|---|---|---|
| G6a | notation lint (`evaluate_math_notation`) | delimiter/brace/malformed checks |
| G6b | Chrome/Edge headless + vendored MathJax 3.2.2 `tex-svg.js` via `file://` + CDP | insert Q/A into DOM, typeset, capture mjx-merror / leftover commands / size / clipping / overlap |
| G6c | human visual score from independent JSON/CSV | score `2` only |

Aggregate G6 PASS requires question and answer each PASS on G6a+G6b and G6c=2.
Incomplete human review → G6 / Presentation / Full = `NOT_ASSESSED` (never
PASS/FAIL).

### Human review persistence

`docs/experiments/human_reviews/ce115_calc_g6c_reviews.json` (and sample
`ce115_calc_sample_g6c_reviews.json`). HTML rebuild reads this file; reviews
are never hard-coded into HTML generators.

### Report

- Builder: `agent_tools/finals_rebuild/ce115_calc_evidence_report.py`
- CLI: `scripts/build_ce115_calc_evidence_report.py`
- Sample offline report:
  `docs/experiments/reports/ce115_calc_sample_evidence/index.html`
- Shows planned/executed/failed, G1–G6, G6a/b/c, Technical/Presentation/Full,
  Healer eligible/attempted/rescued/regressed, retry-once, tokens/latency,
  filtered cell table, per-cell detail pages
- Ratios as `numerator / denominator`; planned excluded from executed denom
- Hashes: artifact / report dataset / report build

### Renderer

- Browser: Chrome `150.0.7871.115`
  (`C:\Program Files\Google\Chrome\Application\chrome.exe`); Edge available
- MathJax: vendored `agent_tools/finals_rebuild/vendor/mathjax/tex-svg.js`
  (3.2.2; SHA-256 in `SHA256SUMS`); frontend-equivalent config (`$`/`\(`/`dfrac`)
- Network during G6b: remote `network_calls=0`

### Files changed

| Path | Purpose |
|---|---|
| `agent_tools/finals_rebuild/browser_mathjax_renderer.py` | Offline Chrome/Edge CDP MathJax probe |
| `agent_tools/finals_rebuild/latex_render_validation.py` | G6a/G6b/G6c + status propagation |
| `agent_tools/finals_rebuild/ce115_calc_evidence_report.py` | HTML evidence report builder |
| `agent_tools/finals_rebuild/vendor/mathjax/*` | Offline MathJax vendor |
| `scripts/build_ce115_calc_evidence_report.py` | CLI |
| `tests/finals_rebuild/test_latex_render_validation.py` | Fixtures / negative / persistence tests |
| `tests/finals_rebuild/fixtures/latex_render/*` | Sample cells + reviews |
| `docs/experiments/human_reviews/*` | Persistent G6c store |
| `docs/experiments/reports/ce115_calc_sample_evidence/*` | Sample offline report |
| `docs/experiments/healer_boundary_execution_log.md` | Milestone 3E record |

### Tests

```powershell
$env:PYTHONPATH = "C:\Projects\MathProject_AST_Research_HealerBoundary"
python -m pytest tests/finals_rebuild/test_latex_render_validation.py --basetemp .pytest_tmp_m3e -q
```

### Call counts

- model_calls = 0
- healer_calls = 0
- network_calls = 0 (G6b remote requests)

### Status

Milestone 3E completed. No commit or push was made.

## Milestone 3E Closeout Audit

### Cleanups

- Removed `.pytest_tmp_m3e*` scratch; added `.pytest_tmp*/` and report
  `vendor/` copies to `.gitignore`
- Sample commit strategy **B**: minimal golden under
  `docs/experiments/reports/ce115_calc_sample_evidence/` (~189 KiB, 14 files),
  no duplicated MathJax blob, machine paths sanitized to `(local-browser)` /
  repo-relative paths; rebuild byte-deterministic for dataset/build hashes

### Vendor provenance

- `tex-svg.js` MathJax 3.2.2 + `LICENSE` (Apache-2.0 notice) + README + SHA256SUMS

### Naming / equivalence

- Distinct report fields: `artifact_g6_legacy_lint`,
  `report_g6a_notation_lint`, `report_g6b_renderer_parse`,
  `report_g6c_human_visual`, `report_g6_overall`
- Equivalence note: `docs/experiments/ce115_calc_g6_renderer_equivalence.md`

### Status

Milestone 3E closeout audit completed. No commit or push was made.

## Milestone 5B.1 — Empty-Block Safety Adjudication and Rule-Governance Freeze

### Goal

Conduct a forensic, read-only empty-block safety adjudication on 5 empty-block candidates and establish the rule-governance specifications. Exclude unsafe heuristics from the formal pipeline.

### Adjudication Outcomes

*   **Candidates Reviewed**: 5 empty-block candidates
*   **NONCORE_NOOP_BLOCK_SAFE count**: 0/5
*   **Reclassified Unsafe**: 5/5
    1.  `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301`: `CORE_LOGIC_MISSING`. Empty block in uncalled math helper `get_square_free` skips prime exponent reduction. The outer loop lacks increment logic (infinite loop if executed).
    2.  `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071302`: `CORE_LOGIC_MISSING`. Empty block in uncalled helper `get_prime_factorization_sqrt_v2` skips factor assignment. Loop variable `j` is static (infinite loop if executed).
    3.  `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303`: `CORE_LOGIC_MISSING`. Empty block `if temp_n > 1:` in prime factors helper skips remainder recording, breaking math correctness. File also lacks return dictionary in `generate()` (truncated).
    4.  `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301`: `TRUNCATED_BLOCK`. File ends in truncated declaration `def generate(level=1,` at the very end, preventing compilation regardless of block repairs.
    5.  `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301`: `CORE_LOGIC_MISSING`. Empty block `if sqrt_delta_int * sqrt_delta_int != delta:` in core generator branch was left unimplemented by the model, risking downstream value and type errors.

### Governance Decisions Frozen

*   **Three-Layer Split**:
    *   `Minimal Core Library`: Frozen and immutable (includes fullwidth punctuation rule).
    *   `Safe Historical Library`: Reconstructed deterministic rules (R01-R04).
    *   `Exploratory Sandbox`: Excluded rules (semantic self-heal, SyntaxError deletion, input replacement, loop rewrites, fallbacks, default injection). Restricts speculative rescues to future work only.
*   **No Duplicate Implementation**: Safe Historical rules must reference existing `core.normalize_fullwidth_python_punctuation` instead of duplicating it.
*   **Fixed Order & Convergence**: Steps run exactly once: Fence -> Leakage -> Trailing -> Fullwidth -> Empty-Block. A second run must result in zero modifications, else the script is rejected as `NON_CONVERGENT`.
*   **Verified Rescue Definition**: Defines `VERIFIED_RESCUE`, `PARTIAL_REPAIR`, and `REGRESSION`.

### Files Created/Tracked

*   **Adjudication Reports**:
    *   `docs/experiments/reports/ce115_empty_block_safety_adjudication.json`
    *   `docs/experiments/reports/ce115_empty_block_safety_adjudication.md`
    *   `docs/experiments/reports/safe_historical_healer_governance_spec.md`
*   **8 Historical Healer Audit Outputs** (now tracked in Git):
    *   `docs/experiments/reports/historical_healer_call_graph.md`
    *   `docs/experiments/reports/historical_healer_rule_inventory.json`
    *   `docs/experiments/reports/historical_healer_rule_inventory.md`
    *   `docs/experiments/reports/historical_healer_git_provenance.md`
    *   `docs/experiments/reports/historical_healer_pipeline_bugs.md`
    *   `docs/experiments/reports/historical_healer_test_artifact_index.json`
    *   `docs/experiments/reports/ce115_historical_rule_match_provisional.json`
    *   `docs/experiments/reports/historical_healer_requalification_recommendation.md`
*   **Execution Log Update**:
    *   `docs/experiments/healer_boundary_execution_log.md` (this file)

### Call Counts & Status
*   `model_calls` = 0
*   `healer_calls` = 0
*   `repair_calls` = 0
*   `replay_calls` = 0
*   `retry_calls` = 0
*   `api_calls` = 0

### Status
Milestone 5B.1 completed with verdict **EMPTY_BLOCK_REPAIR_UNSAFE**.
No code repairs or sandbox compilations were run.

## Milestone 5B.2 — Safe Generic Historical Rule Candidate Adjudication

### Goal

Conduct a forensic, read-only audit and safety adjudication of the 4 generic rules from the historical Healer codebase against the 18 CE115 taxonomy candidates. Evaluate safety profiles using a complete 18 × 4 matrix under the Governance Freeze Specification.

### Adjudication Outcomes

*   **Candidates Reviewed**: 18 taxonomy candidates
*   **Rules Adjudicated**: R01_markdown_fence_removal, R02_trailing_artifact_removal, R03_thinking_leakage_removal, R04_fullwidth_punctuation_normalization
*   **SAFE_PATTERN_MATCH count**: 0/72 entries
*   **Unique Safe Cells**: 0/18
*   **Unsafe Truncation Count**: 6 entries (Rules R02/R03 on 3 truncated cells)
*   **Unsafe Core Logic Count**: 8 entries (Rule R03 on 8 inline thinking leak cells)
*   **Insufficient Evidence Count**: 1 entry (Rule R03 on 1 English leakage cell)
*   **Not Applicable Count**: 57 entries

### Files Created/Tracked

*   **Adjudication Reports**:
    *   `docs/experiments/reports/ce115_safe_generic_rule_adjudication.json`
    *   `docs/experiments/reports/ce115_safe_generic_rule_adjudication.md`

### Call Counts & Status
*   `model_calls` = 0
*   `healer_calls` = 0
*   `repair_calls` = 0
*   `replay_calls` = 0
*   `retry_calls` = 0
*   `api_calls` = 0

### Status

Milestone 5B.2 completed with verdict **NO_SAFE_GENERIC_RULE_WINDOW**.
No code repairs or sandbox compilations were run.

