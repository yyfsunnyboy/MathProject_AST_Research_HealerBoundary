# CE115 Research Healer — Frozen Specification (Audit Closeout)

**Spec id:** `ce115_research_healer_frozen_spec_v1`
**Date:** 2026-07-17
**Status:** frozen for second external audit (hash/provenance closeout)
**Pilot lineage:** `ce115_clean_incremental_ablation_v1`

## 1. Clean ablation composition

| Condition | Composition |
|-----------|-------------|
| Ab1 | BASE only (`build_ab1_prompt`, unchanged) |
| Ab2g | BASE + GENERIC |
| Ab2d | BASE + GENERIC + DOMAIN |

- GENERIC is task-agnostic and identical across tasks.
- DOMAIN is task-local necessary APIs only.
- Do **not** claim `prompt.txt` on disk is byte-identical across runners; compare **canonical prompt strings** via `canonical_prompt_hash`.

## 2. Taxonomy

Allowed failure layers: **L0, L1, L2, L3, L4, L5, L6, META**.

| Name | Meaning |
|------|---------|
| Task difficulty `_l1` in `task_id` | Sampler difficulty rank only |
| Failure layer `L1` | Parse / comment-suite / syntax class |

**Prohibited:** inferring failure layer from `task_id` suffix or from `failure_class` alone.

## 3. Oracle-assisted boundary

Approved production rule:

- `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP`

Positioning (mandatory wording):

> **frozen-oracle-assisted deterministic structural repair**

- Reads frozen key/value from `context.frozen`.
- **Not** oracle-free; do not claim “no oracle contamination”.
- Evidence scope: single fixture `fail_radical_ab1_l2` (`schema_failure` → `passed`) only; do not generalize.

Paused / experimental (not production allowlist):

- `L1_COMMENT_ONLY_IF_INSERT_PASS` — draft parse-only probe; not safe / not semantic-preserving / not approved for formal commit.
- Fixture `fail_exact_ab2d_l1` = exploratory parse-only evidence.

## 4. Execution policy (frozen)

- Allowlist only (production = approved L2 only)
- Fixed ascending priority
- One change per pass; stop that pass after first `changed=true`
- After change: re-parse / re-validate / re-evaluate when task present
- `repair_attempted` only if `changed=true`
- No legacy Regex / AST / AntiDuplication / UnifiedCleanup pipeline

## 5. max_passes semantics — Option A (transactional rollback)

- `max_passes` is mandatory and explicit (`DEFAULT_MAX_PASSES = 1`).
- If another allowlisted rule would still change after the budget is exhausted:
  - `final_status = max_passes_exceeded`
  - **rollback** `output_source` to the original input
  - `rolled_back = true`
  - `consumer_may_use_output = false`
- This **is** transactional fail-closed (not partial-output).

## 6. Hash semantics

### Prompt hashes (companion ledger)

| Field | Meaning |
|-------|---------|
| `canonical_prompt_hash` | SHA-256 of UTF-8 text after universal-newline normalization (CRLF/CR → LF) |
| `prompt_file_byte_hash` | SHA-256 of on-disk `prompt.txt` raw bytes |
| `legacy_prompt_hash` | Deprecated alias of `canonical_prompt_hash` (as stored in pilot artifacts) |

Companion ledger (does **not** modify pilot manifests):

`docs/experiments/analysis/ce115_clean_incremental_prompt_hash_companion_ledger.json`

### Source / candidate hashes (7-cell forensic ledger)

| Field | Meaning |
|-------|---------|
| `source_file_byte_hash` | SHA-256 of on-disk `extracted_candidate.py` raw bytes |
| `canonical_source_hash` | SHA-256 of UTF-8 text after universal-newline normalization |
| `artifact_declared_candidate_hash` | `artifact.json` → `hashes.extracted_candidate` (equals canonical for these pilots) |

## 7. Publication-safe claims

Allowed:

- Single-fixture L2 repair-to-pass under frozen-oracle assistance.
- Clean ablation lineage and canonical prompt-hash equality across Gemini/Qwen builders.
- Frozen multi-rule execution policy with transactional rollback.
- Describing the 7-cell ledger as a **manually-labelled forensic ledger**.

## 8. Prohibited claims

- Oracle-free / no oracle contamination for L2.
- L1 is safe, semantic-preserving, or production-approved.
- Generalizing one L2 fixture to all SCHEMA_FAILURE cells.
- Deriving layer from `failure_class` or task difficulty `_l1`.
- Asserting on-disk `prompt.txt` byte-identity across runs/runners.
- Consumer use of output when `max_passes_exceeded`.
- Claiming the ledger is **independently human-verified**.
- Claiming the repository proves a human adjudication workflow.

## 9. Forensic ledger reference

`docs/experiments/analysis/ce115_qwen_clean_incremental_seven_cell_forensic_ledger.json`

Seven non-PASS cells from `ce115_qwen_clean_incremental_pilot_01` — **manually-labelled forensic ledger**.

Review provenance fields (only completed audits; no fabricated sign-off):

- `labelled_by`
- `first_audit_reviewed_by`
- `second_audit_reviewed_by`
- `review_dates`
- `review_status`

## 10. Line-ending policy

Accepted policy is recorded in `.gitattributes` (`* text=auto`). Historical pilot artifacts are **not** rewritten solely to silence checkout CRLF/LF warnings; compare via canonical hashes instead.
