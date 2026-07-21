# Qwen4B Post-hoc Corrected-Chain Healer Replay Freeze v1

```text
QWEN4B_POSTHOC_HEALER_REPLAY_COMPLETED
QWEN4B_CORRECTED_CHAIN_RESULTS_FROZEN
QWEN4B_PRIMARY_RESULT_PRESERVED
QWEN4B_QWEN9B_COMPARISON_READY
```

**Nature:** post-hoc corrected-chain replay after Math16 revalidation false-loop fix. **Not** preregistered primary.

## Freeze metadata

| Field | Value |
| :--- | :--- |
| Corrected-chain id | `math16_pilot02_qwen4b_healer_v4_posthoc_corrected_chain_r001` |
| Primary id (preserved) | `math16_pilot02_qwen4b_healer_v4_r001` |
| Primary post-Healer | `83/320` (rescued=5) **unchanged** |
| Corrected-chain post-Healer | `84/320` (rescued=6) |
| Replayed | 10 eligible only |
| Noneligible executed | 0 |
| Healer runner SHA-256 | `38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf` |
| Protocol SHA-256 | `bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39` |
| Evaluator SHA-256 | `2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc` |
| Taxonomy SHA-256 | `7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304` |
| Corpus SHA-256 | `7dd3ba5f7e7a38e7ad20142e8c5c5b2e84c20df1b7f5abcf5701c23d24172a22` |
| llm_calls | `0` |
| Qwen9B | `false` |

## Eligible deltas vs primary

| Cell | Primary | Corrected | Notes |
| :--- | :--- | :--- | :--- |
| radical `__ab2d__seed_2026071301` | no-op | **rescued / PASS** | false-loop fix retains wrap |
| q09 `__ab2d__seed_2026072001` | no-op | repaired-still-fail / **FAIL** | unwrap retained; `safe_eval` remains |
| other 8 eligible | unchanged | unchanged | no unexplained drift |

## Explicit non-claims

- Corrected-chain **must not** be reported as preregistered primary.
- Primary `83/320` remains the frozen primary claim.
- No eligibility / rule / allowlist / max_passes changes.
