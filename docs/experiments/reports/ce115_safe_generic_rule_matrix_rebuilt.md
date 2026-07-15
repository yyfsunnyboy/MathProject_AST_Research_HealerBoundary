# 🕵️ CE115 Rebuilt Safe Generic Rule Matrix Report

This report presents the rebuilt 18 × 4 safe generic rule adjudication matrix. It compares the reconstructed scanner verdicts directly with the previous manual baseline from Milestone 5B.2.

---

## 1. Summary comparison (Rebuilt vs. Milestone 5B.2)

| Rule ID | Classification | Old Count (5B.2) | Rebuilt Count | Status |
| :--- | :--- | :---: | :---: | :---: |
| `R01_markdown_fence_removal` | `SAFE_PATTERN_MATCH` | 0 | 0 | MATCH |
| `R01_markdown_fence_removal` | `UNSAFE_TRUNCATION` | 0 | 0 | MATCH |
| `R01_markdown_fence_removal` | `UNSAFE_CORE_LOGIC` | 0 | 0 | MATCH |
| `R01_markdown_fence_removal` | `UNSAFE_RULE_INTERACTION` | 0 | 0 | MATCH |
| `R01_markdown_fence_removal` | `NOT_APPLICABLE` | 18 | 18 | MATCH |
| `R01_markdown_fence_removal` | `INSUFFICIENT_EVIDENCE` | 0 | 0 | MATCH |
| `R02_trailing_artifact_removal` | `SAFE_PATTERN_MATCH` | 0 | 0 | MATCH |
| `R02_trailing_artifact_removal` | `UNSAFE_TRUNCATION` | 3 | 3 | MATCH |
| `R02_trailing_artifact_removal` | `UNSAFE_CORE_LOGIC` | 0 | 0 | MATCH |
| `R02_trailing_artifact_removal` | `UNSAFE_RULE_INTERACTION` | 0 | 0 | MATCH |
| `R02_trailing_artifact_removal` | `NOT_APPLICABLE` | 15 | 15 | MATCH |
| `R02_trailing_artifact_removal` | `INSUFFICIENT_EVIDENCE` | 0 | 0 | MATCH |
| `R03_thinking_leakage_removal` | `SAFE_PATTERN_MATCH` | 0 | 0 | MATCH |
| `R03_thinking_leakage_removal` | `UNSAFE_TRUNCATION` | 3 | 3 | MATCH |
| `R03_thinking_leakage_removal` | `UNSAFE_CORE_LOGIC` | 8 | 8 | MATCH |
| `R03_thinking_leakage_removal` | `UNSAFE_RULE_INTERACTION` | 0 | 0 | MATCH |
| `R03_thinking_leakage_removal` | `NOT_APPLICABLE` | 6 | 6 | MATCH |
| `R03_thinking_leakage_removal` | `INSUFFICIENT_EVIDENCE` | 1 | 1 | MATCH |
| `R04_fullwidth_punctuation_normalization` | `SAFE_PATTERN_MATCH` | 0 | 0 | MATCH |
| `R04_fullwidth_punctuation_normalization` | `UNSAFE_TRUNCATION` | 0 | 0 | MATCH |
| `R04_fullwidth_punctuation_normalization` | `UNSAFE_CORE_LOGIC` | 0 | 0 | MATCH |
| `R04_fullwidth_punctuation_normalization` | `UNSAFE_RULE_INTERACTION` | 0 | 0 | MATCH |
| `R04_fullwidth_punctuation_normalization` | `NOT_APPLICABLE` | 18 | 18 | MATCH |
| `R04_fullwidth_punctuation_normalization` | `INSUFFICIENT_EVIDENCE` | 0 | 0 | MATCH |

### Key Verdict
- **MATCH Rate**: 100% of the 72 matrix entries match their respective manual classifications from Milestone 5B.2.
- **Unique Cells**: 18 unique cells with `outcome == parse_minor` were scanned.
- **Total Matrix Entries**: 18 cells × 4 rules = 72 entries total.

---

## 2. Rule Applicability Breakdown

- **R01 Markdown Fence**: 0/18 applicable (stripped prior to candidate python code extraction).
- **R02 Trailing Residue**: 0/18 applicable (3 cells are truncated, hence classified as `UNSAFE_TRUNCATION`; other 15 cells have no trailing residue).
- **R03 Non-code Leakage**: 8 cells exhibit inline reasoning leakage (`UNSAFE_CORE_LOGIC`), 3 cells are truncated (`UNSAFE_TRUNCATION`), 1 cell contains English conversational text (`INSUFFICIENT_EVIDENCE`), and 6 cells have no leakage (`NOT_APPLICABLE`).
- **R04 Fullwidth Punctuation**: 0/18 applicable (no fullwidth characters exist in active syntax positions).

---

## 3. Freeze Status & Actionable Recommendation

> [!IMPORTANT]
> **Conclusion Preservation**:
> The safe historical healer library remains empty (`0 / 18` applicability) for the CE115 task suite. No rules can enter the freeze status, and the eligible safe pool remains empty (`eligible safe pool = ∅`).

> [!NOTE]
> **Limitations Statement**:
> `eligible safe pool = ∅` is strictly applicable only to the current CE115 task set × Qwen3.5 models × frozen prompt conditions × current safe rule set, and does not represent a general invalidation of the Healer mechanism.
