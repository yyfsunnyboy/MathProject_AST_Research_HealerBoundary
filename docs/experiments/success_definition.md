# Generator Success Definition

## 1. Purpose and scope

This document freezes the success chain for generator runs in the Active Healer
research repository. It defines what counts as a technical success, a
presentation success, and a full success. It does not change the evaluator,
runner, manifest, artifact schema, prompts, models, or historical records.

## 2. Unit of analysis

The unit of analysis is:

`task_id × prompt_condition × model_tag × seed or run_id × ledger_stage`

The same unit is reported independently in the observed,
pipeline-corrected, and post-Healer ledgers. A missing artifact is evidence of
missing observation, not a failed model outcome.

## 3. Fixed evaluation order

The fixed order is G1 through G6. A later gate must not overwrite an earlier
gate's first-attempt observed result.

1. G1 — Evaluability
2. G2 — Executability
3. G3 — Contract Compliance
4. G4 — Semantic Correctness
5. G5 — Problem Presentation Quality
6. G6 — Mathematical Notation Validity

## 4. G1 — Evaluability

**PASS** requires a persisted first-attempt raw artifact, deterministic
extraction of one candidate, parseable Python source, and the required
`generate` entry point. Empty output, prose-only output, unrecoverable fence
contamination, truncated source, parse failure, or a missing entry point is
**FAIL**.

If raw evidence was not retained, G1 is **NOT_OBSERVED**, not FAIL.

## 5. G2 — Executability

**PASS** requires the candidate to load and invoke its required entry point in
the configured sandbox without a timeout, prohibited side effect, process
crash, or runtime exception. Runtime errors such as `NameError`,
`AttributeError`, and `TypeError` are **FAIL**. Syntax and extraction failures
remain classified at G1.

## 6. G3 — Contract Compliance

**PASS** requires the task contract to be satisfied: the required return
schema, keys, types, entry-point signature, and frozen `oracle_payload` must
match exactly. Missing/wrong keys, malformed payloads, frozen-parameter drift,
and schema/type mismatches are **FAIL**.

## 7. G4 — Semantic Correctness

**PASS** requires `correct_answer` to agree with the independent oracle over
the frozen parameters and to satisfy task-specific invariants. Arithmetic,
algebra, unit-conversion, ordering, quotient/remainder, oracle-payload, or
invariant errors are **FAIL**.

## 8. G5 — Problem Presentation Quality

G5 evaluates the actual emitted `question_text`, not a prompt, source template,
generated code, or pass/fail summary. Its automated checks cover presence,
non-truncation, absence of prompt/template/placeholder leakage, agreement with
frozen parameters and `correct_answer`, and absence of obvious contradictory
instructions. Readability and naturalness may be reported separately as an
optional human rubric.

Without persisted `actual_question_text`, G5 is **NOT_OBSERVED**. It must not
be inferred from generated code.

## 9. G6 — Mathematical Notation Validity

G6 evaluates notation in the actual question text. It covers LaTeX delimiter
pairing, malformed or truncated commands, consistent inline/display usage,
unsafe Unicode/LaTeX mixing, and parser/renderer validity where the question
contains mathematical notation. Notation syntax validity, rendered appearance,
and mathematical semantic correctness are separate concerns; semantic
correctness remains G4.

Without persisted actual question text, raw notation evidence, and the relevant
lint/render observation, G6 is **NOT_OBSERVED**. It must not be inferred from
generated code or evaluator pass/fail.

## 10. Composite outcomes

- **Technical Pass** = G1 ∧ G2 ∧ G3 ∧ G4
- **Presentation Pass** = G5 ∧ G6
- **Full Pass** = G1 ∧ G2 ∧ G3 ∧ G4 ∧ G5 ∧ G6

Any required gate that is FAIL makes Full Pass FAIL. Any required gate that is
NOT_OBSERVED makes Full Pass NOT_OBSERVED rather than FAIL.

## 11. Three-ledger reporting

### Observed

First-attempt raw model output only: `request_count = 1`, `retry_count = 0`,
before pipeline correction or Healer action.

### Pipeline-corrected

Condition-independent deterministic extraction or normalization may be applied
and must be recorded with its action. It must not synthesize an oracle answer
or fabricate a candidate. Its result remains distinct from Observed.

### Post-Healer

Only eligible deterministic, non-semantic Healer actions belong here. Report
attempted, rescued, regression, and ineligible failures separately. Do not
count an ineligible failure as a Healer attempt.

## 12. Status semantics

The only gate statuses are **PASS**, **FAIL**, **NOT_ASSESSED**, and
**NOT_OBSERVED**.

- **NOT_ASSESSED**: an earlier gate prevents a meaningful later evaluation.
- **NOT_OBSERVED**: the required artifact was never retained or the experiment
  was not run.

Neither status is equivalent to FAIL and neither is counted as zero.

## 13. Failure taxonomy mapping

| Failure taxonomy | Gate |
|---|---|
| `empty_response`, `extraction_failure`, `parse_failure` | G1 |
| `missing_entry_point` | G1 and G3, according to evaluator stage |
| `execution_failure`, `timeout` | G2 |
| `contract_schema_failure`, `frozen_parameter_violation` | G3 |
| `oracle_mismatch`, `semantic_invariant_failure` | G4 |
| `question_missing_or_truncated`, `placeholder_or_prompt_leakage` | G5 |
| `latex_delimiter_failure`, `latex_render_failure` | G6 |

## 14. Historical retro-application policy

Historical runs may be classified only from preserved raw artifacts and
documented deterministic stages. Generated code cannot stand in for actual
`question_text`; an evaluator summary cannot stand in for raw output. If actual
question text is absent, G5 and G6 are **NOT_OBSERVED**. No inferred result is
retroactively recorded as a PASS or FAIL.

## 15. Current observability coverage

| Gate | Current evidence source | Existing field/function | Coverage | Gap |
|---|---|---|---|---|
| G1 | generation results and evaluator | `raw_first_attempt_output`, `candidate_extracted`, extraction/parse status | PARTIAL | Field names and retention vary by runner; no single frozen schema across all artifacts. |
| G2 | evaluator/result artifacts | execution status, failure category/detail | PARTIAL | Not uniformly present in every historical artifact. |
| G3 | evaluator/result artifacts | schema validation, `oracle_payload`, parse/result status | PARTIAL | No common per-gate status ledger is persisted. |
| G4 | evaluator/result artifacts | `oracle_expected`, `oracle_pass`, task oracle checks | PARTIAL | Semantic invariant status is not a common explicit artifact field. |
| G5 | none for completed runs | contracts require `question_text` but results do not persist actual emitted text | ABSENT | No `actual_question_text` artifact or presentation check evidence. |
| G6 | none | no LaTeX lint, delimiter, display, parser, or render result artifact | ABSENT | No notation-validity or render observation. |

The corrected `ce115_calc_*` four-task families have manifests/design records,
but no corresponding run artifacts. Their current result is
`experiment_not_run / NOT_OBSERVED`, not FAIL.

## 16. Freeze and change-control policy

This definition is a documentation baseline. It does not retroactively alter
historical outcomes, rerun models, or treat unavailable evidence as failure.
Any future evaluator or artifact-schema change must preserve the three ledgers,
the fixed gate order, and the distinction between FAIL, NOT_ASSESSED, and
NOT_OBSERVED.
