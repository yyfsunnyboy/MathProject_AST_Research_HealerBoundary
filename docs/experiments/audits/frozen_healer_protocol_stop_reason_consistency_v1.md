# Frozen Healer Protocol Stop-Reason Consistency Fix v1

```text
FROZEN_HEALER_PROTOCOL_STOP_REASON_MISMATCH_FIXED
FROZEN_HEALER_SHA_REFROZEN
QWEN4B_FROZEN_HEALER_RETRY_READY
```

**Nature:** protocol consistency only — **not** a new Healer capability, **not** a rescue/uplift claim.

## Freeze metadata

| Field | Value |
| :--- | :--- |
| Fix id | `frozen_healer_protocol_stop_reason_consistency_v1` |
| Source blocker cell | `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301` |
| Producer site | `agent_tools/finals_rebuild/ce115_research_healer_runner.py` ≈ L635 (`fallback_loop_detected_{loop_reason}`) |
| Validator site | `agent_tools/finals_rebuild/ce115_research_healer_protocol.py` (`validate_provenance` / `validate_rule_outcome`) |
| Old healer **runner** SHA-256 | `b89e6059ce67efb622aa2e085e365b909d0d4f7df1a6814c1dc83df029ce81e1` |
| New healer **runner** SHA-256 | `b89e6059ce67efb622aa2e085e365b909d0d4f7df1a6814c1dc83df029ce81e1` (**unchanged**) |
| Old protocol SHA-256 | `77fc807579d966bf59e7a53a46ea2e6a1f0438654dafab270d94f6a684d30bc9` |
| New protocol SHA-256 | `bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39` |
| llm_calls | `0` |
| Full Qwen4B Healer run | `false` |
| Qwen9B | `false` |

## stop_reason protocol

### Before

Literal allowlist only:

`None`, `not_applicable`, `not_triggered`, `guards_blocked`, `no_change`, `changed_stop_pass`, `allowlist_empty`, `no_candidate_selected`, `validation_failed`, `max_passes_exceeded`, `stable_no_further_change`, `transaction_rollback`

### After

Same literal allowlist **plus** any string starting with:

`fallback_loop_detected_`

Producer loop_reason suffixes (unchanged):

- `compiler_loop_at_line_{lineno}`
- `evaluator_loop_with_verdict_{evaluator_outcome}`

## Explicit non-changes

- Repair rules / allowlist unchanged
- Loop detection / fallback semantics unchanged
- Eligibility unchanged
- Evaluator / oracle / taxonomy / raw unchanged
- No full 242-cell Healer execution in this fix
