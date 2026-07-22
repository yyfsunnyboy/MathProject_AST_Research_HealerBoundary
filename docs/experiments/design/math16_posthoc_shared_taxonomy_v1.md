# Math16 Post-hoc Shared Taxonomy v1

```text
MATH16_POSTHOC_SHARED_TAXONOMY_V1_FROZEN
IVAN_MACRONIX_SCIENCE_FAIR_OFFICIAL_TAXONOMY
```

> **Authority**: This document defines the frozen three-layer annotation vocabulary for
> the POST-HOC SIX-CELL RESCUE MECHANISM AUDIT (`math16_posthoc_six_cell_rescue_audit_v1`).
> No new taxonomy terms may be introduced during per-cell annotation.
> All cell-level annotation must use exactly the values defined here.

---

## Scope

This taxonomy is shared between:
- `docs/experiments/design/math16_posthoc_six_cell_rescue_audit_v1_spec.md`
- `docs/experiments/manifests/math16_posthoc_shared_taxonomy_v1.json`
- `docs/experiments/manifests/math16_posthoc_six_cell_rescue_audit_v1_manifest.json`
- `scripts/build_math16_posthoc_six_cell_rescue_audit_v1.py`
- `scripts/preflight_math16_posthoc_six_cell_rescue_audit_v1.py`
- `tests/test_math16_posthoc_six_cell_rescue_audit_v1.py`

Taxonomy applies exclusively to:
- **Model**: `Qwen 3.5 4B` (local)
- **Eligible cells**: 10 total (Eligible = 10, from 242 Baseline FAIL)
- **Post-hoc rescued cells**: exactly 6
- **Primary rescued cells**: exactly 5 (subset of the 6)
- **Incremental Post-hoc PASS**: exactly 1

---

## Layer A — Original Failure Layer

Describes the *deepest* error layer that caused the Baseline FAIL.
Exactly one value per cell.

| Code | Meaning |
|---|---|
| `L1_PARSE_SYNTAX` | Python `SyntaxError` — code does not parse at all; AST cannot be built. |
| `L2_CONTRACT_SCHEMA_ENTRYPOINT` | Code parses but violates the output-schema / entrypoint contract required by the Evaluator (e.g., missing oracle payload wrap, wrong JSON key, incorrect entrypoint signature). |
| `L3_DOMAIN_API` | Code parses and has correct schema structure but uses a domain API incorrectly (wrong function name, wrong argument order, missing import, incorrect kwargs). |
| `L4_RUNTIME_EXECUTION` | Code parses, schema is correct, API usage is correct, but a runtime exception (e.g., `NameError`, `TypeError`, `ZeroDivisionError`) prevents completion. |
| `L5_SEMANTIC_ANSWER` | Code runs to completion and produces output, but the mathematical answer is wrong (semantic / reasoning error). |

### Layer A Usage Rules
- Assign the *shallowest* layer that explains why the Evaluator could not award PASS.
- If a cell has both `L1` and `L2` symptoms, assign `L1` (parse error takes precedence).
- This field is set from the frozen Baseline evaluation artifact; it must not be re-evaluated.

---

## Layer B — Healer Disposition Result

Describes what the Healer did to the cell and the outcome.
Exactly one value per cell for each of Primary and Post-hoc columns.

| Code | Meaning |
|---|---|
| `NO_OP` | Healer ran but applied zero transformations (all candidate rules either did not match, were rejected, or a false-loop stop fired before any change). Code is byte-identical to input. |
| `ABSTAIN_NO_RULE` | Healer determined no frozen rule matches this cell. (Distinct from `NO_OP` in that no evaluation was even attempted.) |
| `ABSTAIN_AMBIGUOUS` | Healer matched multiple competing rules; intervention is not uniquely determined; Healer deliberately abstains. |
| `MODIFIED_RESCUED` | Healer applied a rule, the code was transformed, and the post-healer Evaluator returned PASS. |
| `MODIFIED_STILL_FAIL` | Healer applied a rule, the code was transformed, but the post-healer Evaluator still returned FAIL. |
| `MODIFIED_NEW_FAILURE` | Healer applied a rule, the code was transformed, and the post-healer Evaluator returned a *new* failure mode distinct from the original (regression indicator). |
| `MODIFIED_UNEVALUABLE` | Healer applied a rule, the code was transformed, but the post-healer Evaluator could not run to completion (e.g., timeout, schema crash). |

### Layer B Usage Rules
- The Healer disposition is read directly from `healer_outcome` / `healer_decision` in the frozen
  `eligible_execution_records.jsonl` and `primary_vs_corrected_chain_comparison.json`.
- `MODIFIED_RESCUED` corresponds to `healer_outcome == "rescue_to_pass"` (final PASS = true).
- `MODIFIED_STILL_FAIL` corresponds to `healer_outcome == "changed_partial_progress"` with FAIL.
- `NO_OP` corresponds to `healer_outcome == "no_op"`.
- Do not invent new codes; map any observed outcome to the nearest code and note in `analyst_notes`.

---

## Layer C — Repair Signature Match

Describes whether the Healer's applied repair(s) fall within the pre-registered frozen repair
signature(s) for this audit.

| Code | Meaning |
|---|---|
| `WITHIN_FROZEN_REPAIR_SIGNATURE` | All applied rules are listed in the frozen allowlist (`math16_ab3_freeze_manifest.json::frozen_rule_allowlist`), the rule fired as expected, and the change pattern is consistent with the rule specification. |
| `OUTSIDE_FROZEN_REPAIR_SIGNATURE` | At least one applied rule is not in the frozen allowlist, or the rule is listed but its application pattern deviates materially from the rule specification. |
| `AMBIGUOUS_SIGNATURE_MATCH` | Applied rules are in the allowlist, but the analyst cannot determine from available artifacts whether the change pattern is fully consistent with the rule specification (e.g., source span not recovered). |

### Layer C Usage Rules
- This field is populated by the Builder script (objective, automated) where rule_id is present
  in the frozen allowlist, supplemented by human analyst review for edge cases.
- Builder script must cross-reference `frozen_rule_allowlist` from `math16_ab3_freeze_manifest.json`.
- If `artifact_storage == "sha_only_not_committed_py"`, source span cannot be directly recovered
  without the original generation artifact; mark as `AMBIGUOUS_SIGNATURE_MATCH` and note in
  `analyst_notes`.

---

## Valid Condition Values

The following condition strings are the only valid values for the `condition` field in cell records.
These correspond exactly to the four Prompt conditions used in the Math16 Pilot-02 experiment.

| Condition Code | Full Name |
|---|---|
| `Ab1` | Native (no scaffold) |
| `Ab2g` | Generic Scaffold |
| `Ab2d+api` | Domain Scaffold + API |
| `Ab2d+spec` | Domain Scaffold + Standard Spec (v2 for Qwen 4B) |

---

## Valid Family Values

| Family Code | Math Domain |
|---|---|
| `integer` | Integer arithmetic |
| `polynomial` | Polynomial operations |
| `radical` | Radical / surd operations |
| `fraction` | Fraction / rational arithmetic |

---

## Taxonomy Freeze Attestation

```text
taxonomy_version = "1.0"
frozen_at_utc    = "2026-07-22T00:00:00Z"
layer_A_count    = 5
layer_B_count    = 7
layer_C_count    = 3
condition_count  = 4
family_count     = 4
mutation_policy  = "IMMUTABLE — no additions or renames permitted during per-cell annotation"
```

---

*End of taxonomy document.*
