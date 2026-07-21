# Math16 Pilot-02 Integer Evaluation Revision v3_r001 Report

This report summarizes the baseline evaluation and Healer execution statistics for the **Pilot-02 Integer** runs under taxonomy version `v3`.

## 1. Metadata Summary
- **Evaluation ID**: `math16_pilot02_integer_evaluation_v3_r001`
- **Revision**: `v3_r001`
- **Taxonomy Version**: `v3`
- **Taxonomy MD SHA-256**: `7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304`
- **Source Commit**: `ca76b491659178f76e15a540ca653cbe5327eaa5`
- **Evaluator SHA-256**: `c2ac09440c1749db2d1834fc2ae168bd9d2cb64e7c59e9d652f3c145c093c26b`
- **Dataset**: `CE115_Math16`
- **Evidence Role**: `post_hoc_exploratory` (historical-error-informed, pre-run-frozen exploratory ceiling test)

## 2. Executive Summary Metrics
- **Total Planned Cells**: `80`
- **Baseline Passed**: `80` (`100.0%` pass rate)
- **Baseline Failed**: `0`
- **Post-Healer Passed**: `80` (`100.0%` pass rate)
- **Healer Uplift**: `0.0%` (no failing cells were generated in H0, resulting in clean negative control coverage)

## 3. Failure Taxonomy Breakdown (L0–L5)
| Layer | Description | Cell Count |
| :--- | :--- | :--- |
| **L0** | Infrastructure Failure | 0 |
| **L1** | Parse / Syntax Failure | 0 |
| **L2** | Contract / Signature Mismatch | 0 |
| **L3** | Domain API / Tool Mismatch | 0 |
| **L4** | Runtime / Control Flow Exception | 0 |
| **L5** | Semantic Incorrect Answer | 0 |

### Outcome Validity Distribution
| Validity Class | Cell Count |
| :--- | :--- |
| `VALID_MODEL_OUTCOME` | 80 |
| `INVALID_EVALUATOR` | 0 |
| `INVALID_CONTRACT` | 0 |
| `INVALID_INFRASTRUCTURE` | 0 |
| `PENDING_REVIEW` | 0 |

## 4. Condition-by-Condition Analysis
| Condition | Total | Passed | Failed | Pass Rate |
| :--- | :--- | :--- | :--- | :--- |
| **Ab1 (Native)** | 20 | 20 | 0 | 100.0% |
| **Ab2g (Generic)** | 20 | 20 | 0 | 100.0% |
| **Ab2d+api (API)** | 20 | 20 | 0 | 100.0% |
| **Ab2d+spec (Spec)** | 20 | 20 | 0 | 100.0% |

> [!IMPORTANT]
> Ab2d+api 與 Ab2d+spec 比較為完整介入策略比較，不是單純 API 有無的因果估計。

## 5. Task-by-Task Analysis
| Task ID | Total | Passed | Failed | Pass Rate |
| :--- | :--- | :--- | :--- | :--- |
| `ce111_q03_prime_factor_selection` | 20 | 20 | 0 | 100.0% |
| `ce112_q01_negative_integer_power` | 20 | 20 | 0 | 100.0% |
| `ce112_q09_divisor_multiple_intersection` | 20 | 20 | 0 | 100.0% |
| `ce111_nonchoice_q01_part1_exponential_growth` | 20 | 20 | 0 | 100.0% |

## 6. Healer Execution Statistics
- **Eligible Cells**: `0`
- **Transformed Cells**: `0`
- **Abstained Cells**: `0`
- **Rescued Cells**: `0`
- **Preserved Passes**: `80`
- **Rollback / Regressions**: `0`

## 7. Methodological Conclusions
The complete 80-cell evaluation reveals 100% correct generations across all baseline seeds and prompt conditions. Gemini 3.5 Flash successfully followed the required schema and correctness criteria on all four Integer tasks. Due to zero failure layers encountered at baseline, Healer transformations were not triggered, confirming the robust ceiling performance of the current LLM configurations on these specific targets.
