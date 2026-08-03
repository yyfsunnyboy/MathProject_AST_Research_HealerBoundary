# Domain-menu FAIL vs full-plan contract relation census

> **ARCHIVE NOTICE**
> - 資料來源主要為 V1 FAIL（V2 480-cell 正式重跑前）
> - 此批候選不得直接用於設計 V2 Healer 規則
> - 狀態：PENDING_V2_RESIDUAL_EVIDENCE
> - 下一個 gate：V2 480-cell 正式重跑完成後重新 census

Generated: 2026-08-03T05:35:50.038837+00:00
Baseline commit: `f0fbf4a0c2131f03a1bb9096a15d462f27e9b5d4`

## Evidence scope

- Primary: `qwen35_*_math16_ab123_run_002` cells with `condition=ab2d` and `full_pass=FAIL`
- Secondary: `math16_ab2d_480cell_system_prompt_defect_audit_v1.json` `ab2d_domain_menu` schema failures
- **Not included:** per-cell pilot02 qwen4b/9b evaluation baseline (cell_level_baseline.jsonl not present in repo); aggregate FAIL rates cited from existing condition_summary only.

**Total census rows:** 36

## Classification counts

- ALIGNED_LOCAL_DEVIATION: **7**
- LEGAL_ALTERNATIVE_METHOD: **2**
- STRUCTURALLY_DIVERGENT: **5**
- UNPARSEABLE_OR_INSUFFICIENT_EVIDENCE: **14**
- WRONG_API_OR_BINDING: **8**

## Summary

- Eligible for small cross-contract repair test: **15**
- Must abstain (unparseable/insufficient): **14**
- Rewrite-level (algorithm change required): **5**

## Prompt-Contract Healer v2 worth designing?

**Conditional yes.** Kwargs→frozen literal and narrow L2 rules cover a subset of domain-menu FAILs, but API-order/provenance/return-semantics gaps dominate. A v2 Healer should prioritize **detection + abstention** for full-plan-only contracts and **narrow deterministic repair** for zero-arg/kwargs misuse — not cross-condition algorithm rewrites.

