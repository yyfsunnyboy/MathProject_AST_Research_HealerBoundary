# Math16 Post-hoc Six-Cell Rescue Mechanism Audit — Specification v1

```text
MATH16_POSTHOC_SIX_CELL_RESCUE_AUDIT_V1_SPEC_FROZEN
IVAN_MACRONIX_SCIENCE_FAIR_OFFICIAL_AUDIT_SPEC
EXPERIMENT_TYPE = POST_HOC_SUPPLEMENTARY
READ_ONLY_SPEC — NO MODEL CALLS — NO HEALER EXECUTION — NO RESCORING
```

---

## 0. Motivation and Scope

The primary Math16 Pilot-02 experiment (Final Report v1.3) reports:
- **Primary rescued = 5** (Qwen 4B, 83/320 final, pre-registered)
- **Post-hoc total rescued = 6** (Qwen 4B, 84/320 final, post-hoc corrected-chain replay)
- **Incremental Post-hoc PASS = +1** (exactly one cell changed from Primary FAIL → Post-hoc PASS)

This audit provides a structured, read-only, per-cell characterization of the exact mechanism
by which each of those 6 Post-hoc rescued cells was repaired. It is a **supplementary
mechanism audit**, not a re-analysis or extension of the primary results.

**This specification governs the following activities:**
1. Read-only extraction of 6 cell identities from frozen artifacts
2. Objective AST-diff and hash computation (no model calls)
3. Production of an audit roster draft for human review
4. Preflight validation of all preconditions

**This specification expressly prohibits:**
- Any model call (LLM, VLM, or any external API)
- Any execution of the Healer or Evaluator
- Any rescoring or re-classification of official PASS/FAIL outcomes
- Modification of any frozen artifact
- Production of a new official result or conclusion report

---

## 1. Formal Reference Documents

| Document | Path | SHA256 |
|---|---|---|
| Final Report v1.3 | `docs/experiments/reports/math16_pilot02_final_report_v13.md` | `dcf6ae6ee0ac94b5896d8bc0d037ef4f06b7a3de905edf1be891022c6fd0754b` |
| Final Report v1.3 Manifest | `docs/experiments/reports/math16_pilot02_final_report_v13_manifest.json` | `893170c249bc3d93ea288a03dbc45b44001175c788626455214b5da12ddab987` |
| Evidence Complete Manifest | `docs/experiments/milestones/math16_pilot02_evidence_complete_v1/evidence_complete_manifest.json` | `de11b9bd5038171689ee2895fc3a499a7b404f5259b3f5b3bcc31cb4d4af2225` |
| Ab3 Freeze Manifest (Frozen Rules) | `docs/experiments/manifests/math16_ab3_freeze_manifest.json` | `84556dc38e0d21cc57f96b0d44092a516cdd76806c6f7468c0286475e23676b1` |
| Qwen4B Post-hoc Corrected Chain Freeze | `docs/experiments/audits/math16_pilot02_qwen4b_posthoc_corrected_chain_freeze_v1.json` | `d6060e712a38738396119d148f30cb15978c25d85cbce188ef43ccd4e07dcdae` |
| Primary Eligible Execution Records | `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/eligible_execution_records.jsonl` | `2ff030890ea301cb2d94d791f88be8f5a8fa49d46e9b21dbae454c7da5a504e4` |
| Primary vs Corrected Chain Comparison | `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001/primary_vs_corrected_chain_comparison.json` | `e199110fa67459de663a60f5ca03085b6a1f42cba2c6a0bdd470f36c1ff2266a` |
| Shared Taxonomy v1 | `docs/experiments/design/math16_posthoc_shared_taxonomy_v1.md` | *(computed at creation)* |
| Shared Taxonomy JSON | `docs/experiments/manifests/math16_posthoc_shared_taxonomy_v1.json` | *(computed at creation)* |

> **Frozen-artifact protection**: All listed files above must have their SHA256 verified by
> the preflight script before any audit roster is produced. If any SHA mismatch is detected,
> the Builder must stop immediately.

---

## 2. Accounting Verification Requirements

The audit MUST verify the following numeric invariants before proceeding to per-cell analysis.
These values come from the frozen Primary and Post-hoc artifacts; they must not be changed.

| Metric | Required Value | Source |
|---|---|---|
| Eligible cells replayed | 10 | `qwen4b_posthoc_corrected_chain_freeze_v1.json::replayed` |
| Primary rescued | 5 | `primary_vs_corrected_chain_comparison.json::primary_rescued` |
| Post-hoc rescued | 6 | `primary_vs_corrected_chain_comparison.json::corrected_rescued` |
| Incremental PASS (+1) | 1 | `corrected_rescued − primary_rescued` |
| Post-hoc `repaired_still_fail` | 4 | `qwen4b_posthoc_corrected_chain_freeze_v1.json::corrected_repaired_still_fail` |
| Post-hoc `no_op` | 0 | `qwen4b_posthoc_corrected_chain_freeze_v1.json::corrected_no_op` |
| Post-hoc regression | 0 | `qwen4b_posthoc_corrected_chain_freeze_v1.json::corrected_regression` |
| Corrected chain (10 / 8 / 2 / 1) | 10 eligible / 8 unchanged / 2 changed / 1 PASS-changed | `primary_vs_corrected_chain_comparison.json` |

The "corrected chain" breakdown:
- **10** cells replayed in Post-hoc corrected chain
- **8** cells with `same_as_primary == true` (disposition unchanged)
- **2** cells with `same_as_primary == false` (disposition changed vs. Primary)
- **1** cell where the PASS/FAIL outcome changed (`noop_to_rescue == true`)

---

## 3. Six Post-hoc Rescued Cell Identities

The 6 Post-hoc rescued cells are identified solely from the frozen artifact
`primary_vs_corrected_chain_comparison.json` (field `corrected_rescued == 6`) and
`eligible_execution_records.jsonl` (Primary run).

The following table is derived from those frozen sources. **It must not be modified.**

| # | cell_id | condition | task_id | family | seed | Primary disp. | Post-hoc disp. | Final PASS |
|---|---|---|---|---|---|---|---|---|
| 1 | `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d_spec_v2__seed_2026071301` | Ab2d+spec | ce115_calc_radical_simplification_l1 | radical | 2026071301 | rescued | rescued | ✅ |
| 2 | `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026072002` | Ab2d+api | ce115_calc_radical_simplification_l1 | radical | 2026072002 | rescued | rescued | ✅ |
| 3 | `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2d_spec_v2__seed_2026072002` | Ab2d+spec | ce113_q01_negative_fraction_subtraction | fraction | 2026072002 | rescued | rescued | ✅ |
| 4 | `qwen3_5_4b__ce113_q01_negative_fraction_subtraction__ab2g__seed_2026072003` | Ab2g | ce113_q01_negative_fraction_subtraction | fraction | 2026072003 | rescued | rescued | ✅ |
| 5 | `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072004` | Ab2g | ce112_q04_radical_simplification | radical | 2026072004 | rescued | rescued | ✅ |
| 6 | `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` | Ab2d+api | ce115_calc_radical_simplification_l1 | radical | 2026071301 | **no_op** | **rescued** | ✅ |

> **Cell #6** is the incremental Post-hoc PASS (Primary disposition = `no_op`, which blocked
> rescue due to a false-loop rollback; Post-hoc disposition = `rescued` after false-loop fix).

### Non-rescued Post-hoc Eligible Cells (for completeness, not audited as rescue cells)

| # | cell_id | condition | task_id | Primary disp. | Post-hoc disp. | Final PASS |
|---|---|---|---|---|---|---|
| A | `qwen3_5_4b__ce112_q04_radical_simplification__ab2g__seed_2026072002` | Ab2g | ce112_q04_radical_simplification | repaired_still_fail | repaired_still_fail | ❌ |
| B | `qwen3_5_4b__ce115_calc_polynomial_factor_roots_l1__ab2d_spec_v2__seed_2026072002` | Ab2d+spec | ce115_calc_polynomial_factor_roots_l1 | repaired_still_fail | repaired_still_fail | ❌ |
| C | `qwen3_5_4b__ce115_calc_exact_rational_expression_l1__ab1__seed_2026072004` | Ab1 | ce115_calc_exact_rational_expression_l1 | repaired_still_fail | repaired_still_fail | ❌ |
| D | `qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026072001` | Ab2d+api | ce112_q09_divisor_multiple_intersection | no_op | repaired_still_fail | ❌ |

---

## 4. Per-Cell Required Annotation Fields

Each of the 6 Post-hoc rescued cells must have the following fields populated in the audit roster.
Fields marked `[BUILDER]` are computed by the Builder script from frozen artifacts.
Fields marked `[HUMAN]` require human analyst review.
Fields marked `[PREFLIGHT]` are verified by the preflight script.

### 4.1 Identity Fields
| Field | Type | Source | Notes |
|---|---|---|---|
| `cell_id` | string | [PREFLIGHT] Frozen | Exact cell_id from primary_vs_corrected_chain_comparison.json |
| `model` | string | [BUILDER] | Always `qwen3_5_4b` for this audit |
| `task_id` | string | [BUILDER] | Extracted from cell_id token 3 |
| `family` | string | [BUILDER] | One of: `integer`, `polynomial`, `radical`, `fraction` |
| `condition` | string | [BUILDER] | One of: `Ab1`, `Ab2g`, `Ab2d+api`, `Ab2d+spec` |
| `seed` | string | [BUILDER] | Extracted from cell_id last token |

### 4.2 Disposition Fields
| Field | Type | Source | Notes |
|---|---|---|---|
| `is_primary_rescued` | boolean | [PREFLIGHT] | true if Primary disposition == `rescued` |
| `is_posthoc_rescued` | boolean | [PREFLIGHT] | Always true for these 6 cells |
| `primary_disposition` | string [Layer B] | [BUILDER] | From primary_vs_corrected_chain_comparison.json |
| `posthoc_disposition` | string [Layer B] | [BUILDER] | From primary_vs_corrected_chain_comparison.json |
| `final_pass_fail` | string | [PREFLIGHT] | Always `PASS` for these 6 cells |

### 4.3 Failure Analysis Fields
| Field | Type | Source | Notes |
|---|---|---|---|
| `baseline_evaluator_outcome` | string | [BUILDER] | `FAILED` (all are Baseline FAIL) |
| `baseline_failure_layer` | string [Layer A] | [HUMAN] | Read from frozen baseline evaluation artifact |
| `surface_failure` | string | [HUMAN] | Brief description of the observable symptom |
| `root_mechanism` | string | [HUMAN] | Underlying cause of the failure |

### 4.4 Healer Intervention Fields
| Field | Type | Source | Notes |
|---|---|---|---|
| `healer_rule_id` | string | [BUILDER] | From applied_rules in frozen artifact; first rule if multiple |
| `precondition_evidence` | string | [HUMAN] | Evidence that the rule precondition was met |
| `source_span` | string | [BUILDER/HUMAN] | Line range or AST node path of the changed code; `UNKNOWN_SHA_ONLY` if not recoverable |
| `changed_line_count` | integer | [BUILDER] | Number of lines changed; -1 if not recoverable |
| `changed_ast_node_count` | integer | [BUILDER] | Number of AST nodes changed; -1 if not recoverable |
| `changed_ast_node_types` | list[string] | [BUILDER] | List of changed AST node type names |
| `tree_depth_range` | string | [BUILDER] | `"min–max"` depth of changed nodes; `"UNKNOWN"` if not recoverable |
| `control_flow_changed` | boolean | [BUILDER] | True if any branch/loop/exception structure changed |
| `literals_changed` | boolean | [BUILDER] | True if any literal value changed |
| `function_signature_changed` | boolean | [BUILDER] | True if any function def signature changed |
| `semantic_operator_changed` | boolean | [BUILDER] | True if any arithmetic/comparison operator changed |

### 4.5 Artifact Hash Fields
| Field | Type | Source | Notes |
|---|---|---|---|
| `before_snippet_hash` | string | [PREFLIGHT] | SHA256 of before-code from frozen artifact |
| `after_snippet_hash` | string | [PREFLIGHT] | SHA256 of after-code from frozen artifact |

### 4.6 Classification and Governance Fields
| Field | Type | Source | Notes |
|---|---|---|---|
| `repair_signature_match` | string [Layer C] | [BUILDER/HUMAN] | One of: `WITHIN_FROZEN_REPAIR_SIGNATURE`, `OUTSIDE_FROZEN_REPAIR_SIGNATURE`, `AMBIGUOUS_SIGNATURE_MATCH` |
| `oracle_answer_used` | boolean | [PREFLIGHT] | MUST be `false`; oracle answer must never be used to construct the repair |
| `unique` | boolean | [HUMAN] | True if the repair is uniquely determined by the rule |
| `local` | boolean | [HUMAN] | True if the repair is local (narrow scope, not structural) |
| `offline_verifiable` | boolean | [HUMAN] | True if correctness of repair can be verified without running models |
| `analyst_notes` | string | [HUMAN] | Free-form notes; required for any `AMBIGUOUS_SIGNATURE_MATCH` |

---

## 5. Core Research Questions

This audit is designed to produce evidence answering the following questions:

1. **Which condition?** — Do the 6 cells come from `Ab1`, `Ab2g`, `Ab2d+api`, or `Ab2d+spec`?
2. **Which family and task?** — What math domain and specific task is each cell from?
3. **What failure layer?** — Is the original failure `L1`–`L5`?
4. **What did the Healer change?** — What AST node(s) or source span was modified?
5. **Is the repair unique, local, offline-verifiable?** — Does it meet the HealerBoundary contract?
6. **What is the Primary-vs-Post-hoc difference?** — Specifically for Cell #6, what changed between Primary and Post-hoc that enabled the rescue?
7. **Which repair signatures are candidates for Stress Test classification?** — Which rules, when applied successfully, form a replicable and generalizable repair signature?

---

## 6. Builder Behavior Specification

The Builder script (`scripts/build_math16_posthoc_six_cell_rescue_audit_v1.py`) must:

### MUST DO
- Read frozen artifact files listed in Section 1 (read-only)
- Extract 6 cell identities from `primary_vs_corrected_chain_comparison.json`
- Verify accounting invariants (Section 2) before proceeding
- Compute `before_snippet_hash` and `after_snippet_hash` from frozen artifact fields
- Attempt AST diff for any cells where before/after source is available
- Populate all `[BUILDER]` fields in the audit roster template
- Write output to `artifacts/math16_posthoc_six_cell_rescue_audit_v1/preflight/` (draft only)
- Mark `[HUMAN]` fields with `"PENDING_HUMAN_REVIEW"` placeholder
- Log all decisions and sources

### MUST NOT DO
- Call any model (LLM, VLM, API)
- Execute the Healer or any code transformation
- Execute the Evaluator or any scoring script
- Assign a PASS or FAIL outcome to any cell
- Modify any source file in the frozen artifact directories
- Write any output outside `artifacts/math16_posthoc_six_cell_rescue_audit_v1/preflight/`

### Output Path (Preflight Only)
```
artifacts/math16_posthoc_six_cell_rescue_audit_v1/
  preflight/
    audit_roster_draft.json       ← Draft with BUILDER fields populated, HUMAN fields = PENDING
    accounting_check.json         ← Verification of 10/8/2/1 invariants
    sha_verification.json         ← Per-file SHA256 verification results
    preflight_summary.json        ← Overall pass/fail for preflight checks
```

---

## 7. Preflight Validation Checklist

The preflight script (`scripts/preflight_math16_posthoc_six_cell_rescue_audit_v1.py`) must
verify ALL of the following before declaring `PREFLIGHT_PASS`:

### 7.1 Source Integrity
- [ ] Final Report v1.3 SHA256 matches frozen value
- [ ] Evidence Complete Manifest SHA256 matches frozen value
- [ ] Primary vs Corrected Chain Comparison SHA256 matches frozen value
- [ ] Primary Eligible Execution Records SHA256 matches frozen value
- [ ] Ab3 Freeze Manifest SHA256 matches frozen value
- [ ] Qwen4B Post-hoc Corrected Chain Freeze SHA256 matches frozen value

### 7.2 Cell Identity Uniqueness
- [ ] Exactly 6 distinct cell_ids with `new_post_healer_status == "PASSED"` in comparison artifact
- [ ] Exactly 5 cells with `primary_post_healer_status == "PASSED"` (Primary rescued)
- [ ] Exactly 1 cell with `noop_to_rescue == true` (incremental PASS)
- [ ] All 6 cell_ids have `model == "qwen3_5_4b"` (derived from cell_id prefix)
- [ ] No duplicate cell_ids in the 6-cell roster

### 7.3 Attribute Completeness
- [ ] All 6 cells have non-empty `condition` (one of valid taxonomy conditions)
- [ ] All 6 cells have non-empty `task_id`
- [ ] All 6 cells have non-empty `family` (one of valid taxonomy families)
- [ ] All 6 cells have non-empty `seed`
- [ ] All 6 cells have `before_snippet_hash` from frozen artifact
- [ ] All 6 cells have `after_snippet_hash` from frozen artifact

### 7.4 Artifact Existence
- [ ] `eligible_execution_records.jsonl` exists and is readable
- [ ] `primary_vs_corrected_chain_comparison.json` exists and is readable
- [ ] `math16_ab3_freeze_manifest.json` exists and is readable
- [ ] `math16_posthoc_shared_taxonomy_v1.json` exists and is readable

### 7.5 AST Parsability
- [ ] For each cell where before/after source is recoverable: attempt `ast.parse()` and record
  `ast_parseable: true/false`. If `artifact_storage == "sha_only_not_committed_py"`, record
  `ast_parseable: "UNKNOWN_SOURCE_NOT_AVAILABLE"`.

### 7.6 Governance Checks
- [ ] No `oracle_answer_used == true` values (all must be `false` or `"PENDING_HUMAN_REVIEW"`)
- [ ] No new scoring columns overwrite official result fields in frozen artifacts
- [ ] Output directory is isolated from frozen artifact directories
- [ ] Taxonomy value domain is fixed (no extra codes added)
- [ ] No Stress Test execution occurred
- [ ] No official analysis result report was produced

### 7.7 Accounting Check
- [ ] `replayed == 10`
- [ ] `primary_rescued == 5`
- [ ] `corrected_rescued == 6`
- [ ] `corrected_rescued - primary_rescued == 1`
- [ ] `corrected_repaired_still_fail == 4`
- [ ] `corrected_no_op == 0`
- [ ] `corrected_regression == 0`

---

## 8. Output Isolation Policy

All Builder and Preflight outputs are written to:
```
artifacts/math16_posthoc_six_cell_rescue_audit_v1/preflight/
```

This directory is NOT in `docs/experiments/` and does NOT share a directory with any frozen
artifact. It is safe for read-write access by the Builder/Preflight scripts without risk of
overwriting frozen sources.

No file in `docs/experiments/` is written by any script in this audit.

---

## 9. Relationship to Primary Experiment

| Attribute | Primary Experiment | This Audit |
|---|---|---|
| Official result | 83/320 (rescue = 5) | Not changed |
| Post-hoc result | 84/320 (rescue = 6) | Not changed |
| Reported in Final Report v1.3 | Yes | Read-only reference |
| New PASS/FAIL assignments | N/A | Prohibited |
| Model calls | During generation | Prohibited |
| Healer execution | During Primary/Post-hoc | Prohibited |
| Evaluator execution | During Primary/Post-hoc | Prohibited |
| Output | Official result artifacts | Draft audit roster only |

---

## Attestation

```text
spec_version          = "1.0"
experiment_type       = "POST_HOC_SUPPLEMENTARY"
frozen_anchor_head    = "969f1a8897c1440e685cd5abc7ee060f5467d39a"
evidence_complete_git = "5c15b0aee0ef0d4bfa0439c8d0759ed0e4e2af49"
no_model_calls        = true
no_healer_execution   = true
no_rescoring          = true
no_official_result_mutation = true
expected_cell_count   = 6
expected_primary_rescues   = 5
expected_posthoc_rescues   = 6
expected_incremental_pass  = 1
corrected_chain       = "10 / 8 / 2 / 1"
```

---

*End of specification.*
