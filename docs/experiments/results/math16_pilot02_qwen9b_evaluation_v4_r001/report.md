# Math16 Pilot-02 Qwen 3.5 9B Evaluation v4_r001 (baseline only)

- Evaluation ID: `math16_pilot02_qwen9b_evaluation_v4_r001`
- Evaluator hash: `2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc`
- Taxonomy hash: `7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304`
- Corpus SHA closure: `dedac60aceb5d285a86d3b5cc35ce8064a317c2b52ecc66a673f48632fb6cccf`
- Runtime fingerprint: `f45f79238bbf9400729fd00dbfaf4e33a7a7716cb9f81d4095a1fd1d52e0da5b`
- Model digest: `6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7`
- LLM calls: `0`
- Healer / Ab3: **not run**
- Suspected schema FN candidates (audit only): `0`

## Overall
- Baseline pass: `101/320`
- Baseline fail: `219/320`

## By condition
| Condition | Pass |
| :--- | ---: |
| Ab1 (`ab1`) | 18/80 |
| Ab2d+api (`ab2d`) | 16/80 |
| Ab2d+spec-v2 (`ab2d_spec_v2`) | 40/80 |
| Ab2g (`ab2g`) | 27/80 |

## By family
| Family | Pass |
| :--- | ---: |
| fraction | 31/80 |
| integer | 42/80 |
| polynomial | 9/80 |
| radical | 19/80 |

## Failure layers (baseline failures)
{"L0": 0, "L1": 65, "L2": 10, "L3": 2, "L4": 45, "L5": 97}

QWEN9B_320CELL_SCORING_COMPLETED
QWEN9B_SCORING_COMPLETENESS_AUDIT_PASSED
QWEN9B_BASELINE_RESULTS_FROZEN
QWEN9B_HEALER_ELIGIBILITY_READY
