# CE115 Evidence Freeze — Publication-safe / Prohibited Claims

Aligned with `ce115_research_healer_frozen_spec_v1.md` and this freeze matrix.

## Publication-safe claims

1. Core clean pilot (cohort A) shows Gemini 9/9 natural PASS and Qwen 2/9 natural PASS on tasks 3/5/7 under Ab1/Ab2g/Ab2d.
2. Among Qwen’s 7 natural failures, forensic labelling yields mixed L1/L2/L4/L5 layers (manually-labelled ledger).
3. Exactly **one** formal production Healer success exists in this freeze: L2 `L2_SINGLE_KEY_ORACLE_PAYLOAD_WRAP` repair-to-pass on the radical Ab1 single-key schema fixture.
4. That L2 success is **frozen-oracle-assisted deterministic structural repair**, evidence-scoped to that fixture.
5. L1 comment-only insert remains **exploratory / paused**; it is not a production repair-to-pass claim.
6. Regression corpus shows expected **no-op** on protected PASS / multi-key / value-mismatch guards (false-positive count 0 in expected outcomes).
7. q09 diagnostic (cohort C) documents Gemini **EQUATION_RECONSTRUCTION_WRONG** with secondary **SPURIOUS_SHARED_BINOMIAL_SQUARE_TEMPLATE** as a stable cross-condition mechanism for `[12,7]` and related templates.
8. q09 L5 equation-reconstruction failures are **out of scope** for the current production Healer allowlist.
9. Clean ablation lineage Ab1=BASE / Ab2g=BASE+GENERIC / Ab2d=BASE+GENERIC+DOMAIN remains the prompt composition claim (canonical prompt hashes, not on-disk byte identity across runners).
10. Cohorts A, B, and C must be reported with **separate** denominators.

## Prohibited claims

1. A single overall “CE115 success rate” pooling A+B+C.
2. Counting exploratory L1 as formal Healer success or production-approved repair.
3. Claiming L2 is oracle-free / has no oracle contamination.
4. Generalizing the single L2 fixture to all `SCHEMA_FAILURE` cells.
5. Claiming q09 / sign-pairing L5 failures are Healer-repairable under the current allowlist.
6. Mixing q09 diagnostic outcomes into core Healer success numerators or denominators.
7. Inferring failure layer from `task_id` `*_l1` or from `failure_class` alone.
8. Asserting on-disk `prompt.txt` byte-identity across runners/models.
9. Claiming the forensic ledger is “independently human-verified” or that the repo proves a human adjudication workflow.
10. Treating sign-pairing as a production task expansion or new Healer rule justification.
11. Describing regression no-ops as natural pilot PASS improvements.
12. Using Qwen q09 mechanism labels beyond `NOT_VERIFIED` without a separate forensic freeze.

## Aggregation rules (short)

| May combine | Must not combine |
|---|---|
| Within-cohort status tallies | A pilot PASS rate with B repair-to-pass |
| B natural failures with B regression guards (labelled separately) | B Healer rate with C q09 fail rate |
| Gemini L5 mechanism counts within C | Exploratory L1 with formal L2 success count |
