# Math16 Ab2d answer-contract fairness review v1

**Date:** 2026-08-02  
**HEAD at review:** `5adecb77` (committed with answer-contract + LF freeze-prep)  
**Scope:** Zero-model fairness after injecting task-specific answer contracts into domain-menu and full-plan.  
**Line endings:** `ab2d_full` prompts normalized to LF; raw-byte SHA == prior LF text SHA (unchanged ledger).

Machine checklist JSON: `docs/experiments/results/Math16/math16_ab2d_answer_contract_fairness_review_v1.json`

## Checklist

| Check | Result |
|-------|--------|
| task-specific answer contract present in both | **PASS** |
| answer contract byte-identical (menu ↔ full) | **PASS** |
| API surface (domain block) byte-identical | **PASS** |
| derived_scaffold absent both | **PASS** |
| difference only Processing steps | **PASS** |
| stem / frozen_params match | **PASS** |
| contract body == `math_answer_contracts.CONTRACTS[oracle_type]` | **PASS** |
| no answer leakage in contract blocks | **PASS** |
| cross-domain isolation | **PASS** |
| Processing steps free of schema-literal assembly | **PASS** |
| to_exact clarified (Fraction prompts) | **PASS** |
| generic examples marked non-normative | **PASS** |

**Overall:** **PASS** (`all_pass: true`)

## Contract source

- Authoritative: `agent_tools/finals_rebuild/math_answer_contracts.py` → `CONTRACTS[oracle_type]`
- Injected as `## Task-specific answer contract` (outside domain API markers; per-task)
- Not rewritten; verbatim Required return schema blocks

## Processing steps cleanup

Schema literals removed (`{"count"}`, `{"k"}`, bare int / Pack / num·den / nested-or-flat / final bare).  
Final step on every task: `Assemble correct_answer exactly according to the Answer contract.`
