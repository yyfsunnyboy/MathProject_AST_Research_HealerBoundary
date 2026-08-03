# Prompt-Contract Healer V2 — Hold Note

Archived: 2026-08-03
Baseline commit: `f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4`

## Phase 1 verdict

Prompt–Healer coverage audit + General safety Healer coverage: existing Healer machinery
covers generic syntax/dangerous-call repair (`GEN_*` contracts) but has **no** deterministic
or detection coverage for the V2-specific runtime-binding contracts
(`PC_ZERO_ARG_RUNTIME`, `PC_PROHIBIT_KWARGS_FROZEN`, `PC_FROZEN_LITERAL_BINDING`,
`PC_ORACLE_PAYLOAD_SOURCE`) beyond `narrow_rule` / `deterministic_repair_candidate` status,
and **no** coverage at all for full-plan-only contracts (`PC_FULL_REQUIRED_APIS`,
`PC_FULL_API_CALL_ORDER`, `PC_FULL_RETURN_BINDING`, `PC_FULL_ANSWER_PROVENANCE` — all
`not_covered` / `abstain_only`).

## Phase 2 verdict

Answer-assembly provenance audit + domain-menu FAIL/full-plan relation census: **no existing
Healer** performs AST def-use provenance tracing for `correct_answer` assembly
(`NOT_FEASIBLE_IN_CURRENT_HEALER` for all 16 tasks). The domain-menu FAIL census (36 rows,
V1-era `qwen35_*_math16_ab123_run_002` cells) found only 15/36 rows eligible for a narrow
cross-contract repair test; 14/36 must abstain (unparseable/insufficient evidence); 5/36
require an algorithm-level rewrite, which is out of scope for any repair rule.

## Why rule design is paused

All evidence in this audit batch is **V1 FAIL evidence** — collected before the V2 prompt
rewrite (`math16_ab2d_menu_vs_full_runtime_contract_v2`) that added the explicit
zero-argument runtime-binding contract and forbade `kwargs.get("frozen_params")` in-prompt.
V2's own qualification (6 live Qwen4B cells) already shows 0/6 recurrence of the
`kwargs.get("frozen_params")` pattern that motivated `PC_PROHIBIT_KWARGS_FROZEN` in the
first place. Designing a Healer repair rule from V1 FAIL evidence risks encoding a fix for a
failure mode the V2 prompt may have already eliminated, or missing whatever *new* residual
failure shape V2 produces at full-model, full-scale (480-cell). Rule design before that
evidence exists is premature by construction, not by caution alone.

## Judgment process after V2

1. Run the V2 480-cell formal rerun (3 models x 2 conditions x 16 tasks x 5 seeds) once
   `GEMINI_API_KEY` and a working Qwen9B host are available.
2. Re-run the same census/coverage methodology used in this batch (prompt-contract coverage
   matrix, general-safety coverage, answer-assembly provenance, domain-menu-FAIL relation
   census) against the **V2 480-cell** results specifically — not the V1 corpus.
3. Only after that V2-native census exists, re-evaluate contract-by-contract whether a
   `deterministic_repair_candidate` is still warranted, using V2 failure evidence as the
   basis, not V1's.
4. Any repair rule proposal must cite V2 cell IDs as its evidence, not V1
   `qwen35_*_math16_ab123_run_002` cell IDs or the V1 `math16_ab2d_480cell_system_prompt_defect_audit_v1.json`.

## Explicit prohibition

**Do not develop a kwargs→frozen literal Healer repair rule directly from this V1-evidence
batch.** `PC_PROHIBIT_KWARGS_FROZEN` / `PC_FROZEN_LITERAL_BINDING` / `PC_ZERO_ARG_RUNTIME`
candidates listed here are frozen as reference only, `status: PENDING_V2_RESIDUAL_EVIDENCE`.
The next allowed gate for rule design is the V2 480-cell re-census described above.
