# Math16 Healer Revalidation False-Loop Fix v1

```text
MATH16_HEALER_REVALIDATION_FALSE_LOOP_FIXED
MATH16_HEALER_TRUE_LOOP_GUARD_PRESERVED
MATH16_HEALER_RUNNER_SHA_REFROZEN
QWEN4B_POSTHOC_HEALER_REPLAY_READY
```

**Nature:** post-hoc **implementation consistency** fix — Math16 Healer revalidation must use the formal scoring path. **Not** a new repair capability, **not** a primary rescue/uplift rewrite.

## Freeze metadata

| Field | Value |
| :--- | :--- |
| Fix id | `math16_healer_revalidation_false_loop_fix_v1` |
| Primary Qwen4B ledger | `docs/experiments/results/math16_pilot02_qwen4b_healer_v4_r001/` **unchanged** |
| Primary score claim | baseline `78/320` → post-Healer `83/320` (rescued=5, no-op=2) **kept** |
| Old healer runner SHA-256 | `b89e6059ce67efb622aa2e085e365b909d0d4f7df1a6814c1dc83df029ce81e1` |
| New healer runner SHA-256 | `38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf` |
| Protocol SHA-256 | `bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39` (**unchanged**) |
| llm_calls | `0` |
| Full Qwen4B Healer replay | `false` |
| Gemini replay | `false` |
| Qwen9B | `false` |

## Root cause

`MathHealerRunner._maybe_reevaluate` always called CE115 pilot `classify_response`, while formal Math16 scoring uses `classify_math16_response`. For Math16 tasks with `oracle_type` prefix `math16_`, pilot and formal evaluators can disagree (e.g. both sides `runtime_failure` under pilot while formal flips schema→pass after wrap). Phase B then treated **identical coarse outcome strings** as an evaluator loop and rolled back a valid repair.

## Minimal fix (runner only)

Sites in `agent_tools/finals_rebuild/ce115_research_healer_runner.py`:

1. `_is_math16_task` — route when `oracle_type.startswith("math16_")`
2. `_maybe_reevaluate` — Math16 → `classify_math16_response`; else pilot `classify_response`; optional `context['reevaluator']` override; exceptions → fail-closed `evaluator_error`
3. `_failure_signature` — fingerprint beyond coarse outcome
4. `_is_phase_b_evaluator_loop` — loop only if same outcome **and** same failure signature **and** `_rule_would_change` still true
5. Apply path — reject change on revalidator error; Phase B uses stricter loop helper

## Explicit non-changes

- Repair rules / allowlist / priority / max_passes
- Eligibility / oracle / taxonomy / formal Math16 evaluator bytes
- Primary `healer_v4_r001` ledger JSON and score claims
- No `safe_eval` backfill for Cell B

## Cell expectations (targeted)

### Cell A — implementation gap

`qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2d__seed_2026071301`

- Rule: `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`
- After fix: change **retained**; formal `classify_math16_response` → **PASS**
- Must **not** be rewritten into primary `83/320` ledger

### Cell B — out-of-scope control

`qwen3_5_4b__ce112_q09_divisor_multiple_intersection__ab2d__seed_2026072001`

- Rule: `L2_CORRECT_ANSWER_JSON_DUMPS_UNWRAP`
- Root cause remains `safe_eval` NameError
- After fix: formal Math16 still **FAIL**; must stay **non-rescue**

## True-loop / fail-closed guards retained

- Same outcome + same signature + rule still would change → `fallback_loop_detected_evaluator_loop_with_verdict_*`
- Same outcome alone after rule exhausted → **not** loop
- Revalidator exception → rollback (`fallback_loop_detected_revalidator_error_*`)
- Phase A compiler loop unchanged
