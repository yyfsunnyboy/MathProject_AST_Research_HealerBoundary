# Gemini Math16 Pilot-02 Post-hoc Corrected-Chain Healer Replay

```text
GEMINI_POSTHOC_CORRECTED_CHAIN_REPLAY_COMPLETED
GEMINI_PRIMARY_RESULT_PRESERVED
GEMINI_HEALER_ELIGIBILITY_REVALIDATED
QWEN9B_PREREGISTRATION_READY
```

**Nature:** post-hoc corrected-chain — **not** preregistered primary.

- Primary baseline / Healer (preserved): **289/320**, rescued=0, eligible=0
- Corrected-chain post-Healer: **289/320**
- FAIL cells: **31**; eligible: **0**; noneligible: **31**
- Rescued / still-fail / no-op / abstain / regression: **0 / 0 / 0 / 31 / 0**
- FAIL layers: `{'L3': 17, 'L5': 11, 'L1': 3}`
- Healer runner SHA: `38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf`
- Protocol SHA: `bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39`
- LLM calls: **0**

## Special adjudication

1. eligible=0 still holds? **True**
2. corrected-chain added rescue? **False**
3. failures mostly L5/non-repairable (L3+L5≥80%)? **True** (L1=3, L3=17, L5=11)
4. false-loop shadowed rescue cases? **False** (eligible=0 ⇒ runner never applied)
5. Gemini vs Qwen4B Healer differential still holds? **True** (Gemini eligible/rescued remain 0; Qwen4B corrected rescued=6)

## Condition

| Condition | Baseline | Post-Healer | Eligible | Rescued | Abstained |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Ab1 | 72/80 | 72/80 | 0 | 0 | 8 |
| Ab2g | 76/80 | 76/80 | 0 | 0 | 4 |
| Ab2d+api | 78/80 | 78/80 | 0 | 0 | 2 |
| Ab2d+spec | 63/80 | 63/80 | 0 | 0 | 17 |

## Family

| Family | Baseline | Post-Healer | Eligible | Rescued | Abstained |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Integer | 80/80 | 80/80 | 0 | 0 | 0 |
| Polynomial | 74/80 | 74/80 | 0 | 0 | 6 |
| Radical | 70/80 | 70/80 | 0 | 0 | 10 |
| Fraction | 65/80 | 65/80 | 0 | 0 | 15 |
