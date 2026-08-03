# Math16 Ab2d menu-vs-full Prompt V2 -- runtime-contract fix (notes)

**Base commit**: `f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4`
**New namespace**: `math16_ab2d_menu_vs_full_runtime_contract_v2`
**Scope this round**: prompt fix + mechanical verification + 8-cell qualification (6 live,
2 pending). No 480-cell rerun, no commit/push.

## 1. V1 defect

Three untracked audit docs already in the tree (`math16_ab2d_480cell_system_prompt_defect_audit_v1.md`,
`math16_gemini_full_rationalize_5cell_forensic_v1.md`, `math16_qwen_320cell_low_passrate_forensic_v1.md`)
found the dominant Qwen failure mode across the frozen 480-cell run was
`runtime_call_convention_misuse`: **95 of 164 failing cells** were models writing
`kwargs.get("frozen_params")` and receiving `None`.

Root cause, confirmed by reading the real executor
(`scripts/run_math16_latex_v1_gemini_live.py:210`, reused by
`agent_tools/finals_rebuild/math16_ab2d_formal_execution.py:637`): the harness calls the
model's generated function as `ns['generate']()` -- **zero arguments, always**. `kwargs` is
never populated. The model must read the frozen values from the prompt's prose
`## frozen_params` block and embed them as literals in the source it writes. V1 prompts
never state this explicitly, never show a concrete skeleton demonstrating it, and never
forbid the `kwargs.get(...)` guess -- worse for `ab2d_full`, where the only per-task addition
was a short prose `## Processing steps` list ("1) simplify_term(1, radicand).") with no
concrete runtime-binding code at all.

## 2. V2 fix

The runtime/evaluator is unchanged (still zero-argument `generate()`) -- confirmed with the
user before implementation, since documenting a fictitious `generate(level=1,
**frozen_params)` kwargs-binding contract (the initial framing of this task) would have been
actively false and likely made pass rates worse.

Every V2 prompt now contains, in a fixed position shared by both conditions:

- **`## Runtime binding contract (zero-argument evaluator call)`** -- states the real
  contract in prose and, in one designated callout (never inside a runnable code fence),
  shows the exact `kwargs.get("frozen_params")` anti-pattern with an explanation of why it
  always fails.
- **A per-task zero-argument skeleton** -- `def generate(level=1, **kwargs): frozen = {...
  this task's real frozen_params ...}; correct_answer = {... "..." placeholders matching
  this task's answer-contract keys/types ...}; return {question_text, correct_answer,
  oracle_payload}`. Domain-menu leaves the placeholders unfilled (no API name/order named);
  full-plan additionally appends `## Task-specific scaffold (full-plan only)`, a complete,
  runnable implementation using real Domain API calls (mined from an already-passing V1
  cell, then independently re-verified against the real oracle evaluator -- never a
  hardcoded ground-truth literal).

Everything else (`SYSTEM_HEADER`, the full per-domain Domain API menu rendered from
`domain_api_ssot.py`'s live `SUPPORTED_PUBLIC` inventory, the shared output contract, and
the task-specific answer contract from `math_answer_contracts.CONTRACTS`) is produced by
literally calling the existing V1 builder functions -- unmodified, unedited -- so it is
byte-identical to V1's content by construction, not by manual sync.

New files only; no V1 prompt/builder file was opened in write mode:
- `agent_tools/finals_rebuild/math16_ab2d_v2_scaffolds.py` (`TASK_SCAFFOLDS_V2`, 16 entries)
- `agent_tools/finals_rebuild/math16_ab2d_domain_menu_v2.py`
- `agent_tools/finals_rebuild/math16_ab2d_full_v2.py`
- `agent_tools/finals_rebuild/math16_ab2d_v2_qualification.py`
- `scripts/build_math16_ab2d_v2_domain_api_manifests.py`
- `scripts/audit_math16_ab2d_v2_semantic_census.py`
- `scripts/preflight_math16_ab2d_v2.py`
- `scripts/build_math16_ab2d_v2_sha256_manifest.py`
- `docs/experiments/prompts/ab2d_domain_menu_v2/prompts/*.txt` (16) + `manifest.json`
- `docs/experiments/prompts/ab2d_full_v2/prompts/*.txt` (16) + `manifest.json`
- `docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2/domain_api_coverage/*.{json,md}`
- `docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_semantic_census.{json,md}`
- `docs/experiments/results/Math16/math16_ab2d_menu_vs_full_runtime_contract_v2_zero_model_preflight.{json,md}`
- `artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/qualification/` (8-cell qualification artifacts)

## 3. Mechanical verification results (this round)

- Domain API coverage: 33/33 SUPPORTED_PUBLIC APIs (IntegerOps 7, FractionOps 8, RadicalOps
  9, PolynomialOps 9) documented with all 7 required fields, 0 missing, 0 example-execution
  failures, 0 rendered-vs-SSOT mismatches.
- 32-prompt semantic census: 32/32 complete, 0 missing, 0 duplicate, 0 fairness violations,
  0 answer-contract mismatches vs V1.
- Zero-model preflight: 80 code fences across 32 prompts, 0 AST-parse failures; all 16
  full-plan scaffolds executed locally against real frozen literals -- 0 execution
  failures, 0 schema failures, 0 oracle_payload mismatches, 0 incorrect answers (verified
  against the real `evaluate_math_task_oracle`, not just "runs without crashing").
- `kwargs.get("frozen_params")` appears in exactly one place per prompt: the designated
  "DO NOT DO THIS" callout inside the Runtime binding contract section, never inside a
  runnable/example fence -- checked mechanically for all 32 prompts.

## 4. 8-cell qualification (this round)

`planned=8, executed_live=6 (Qwen4B only), pending_9B=1, pending_gemini=1` -- Qwen9B cannot
run on this machine and no `GEMINI_API_KEY` was searched for or used, per explicit user
instruction. Live results: `live_pass=4, live_fail=2`,
**`kwargs_get_frozen_params_reappeared=0`** across all 6 live cells (the primary target of
this fix). The 2 live failures were `runtime_failure` under `ab2d_domain_menu_v2` (a
`ValueError` from a self-chosen invalid `LinearRadical` construction, and an `ImportError`
for a nonexistent `to_exact_str` the model invented) -- both are model API-choice mistakes
consistent with the previously-documented "small models are more sensitive to unscaffolded
prompt complexity" pattern (`math16_qwen_320cell_low_passrate_forensic_v1.md`), not
runtime-binding failures. Both `ab2d_full_v2` cells for the same two tasks passed. Full
per-cell detail: `artifacts/math16_ab2d_menu_vs_full_runtime_contract_v2/qualification/qualification_summary.json`.

## 5. 480-cell rerun plan (NOT executed this round)

If/when `GEMINI_API_KEY` is available and Qwen9B can run on the target machine, a full
3-model x 2-condition x 16-task x 5-seed (480-cell) formal run should be executed against
the V2 prompt set, using the same manifest/model-settings authority as V1
(`artifacts/math16_ab2d_full_domain_assisted_v1/preregistration/model_settings.json`) under
a new `experiment_id` (`math16_ab2d_menu_vs_full_runtime_contract_v2`), so V1's frozen 480
cells remain untouched and comparable as a baseline. Primary hypothesis to test: the
`runtime_call_convention_misuse` failure class (95/164 in V1) should drop to ~0, given 0/6
reappeared in this round's live qualification.
