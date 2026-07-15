# 🧬 Historical Healer Git Provenance

This document records the forensic git provenance for the two repositories under audit. It details their branches, HEAD commits, remote configurations, working tree statuses, and identifies the exact commit representing the competition release version.

---

## 1. Repository Statuses (Audit Time: 2026-07-15)

### Repository A: Parent / Shared Repo
*   **Local Path**: `C:\Projects\MathProject_AST_Research`
*   **Active Branch**: `main` (up-to-date with `origin/main`)
*   **HEAD Commit**: `a47bf295c1b8f392341dcccbd9b978aec110e530` ("20260714旺宏_AST_Healer_分層實驗與邊界驗證計畫_V5")
*   **Git Remotes**:
    *   `origin`: `https://github.com/yyfsunnyboy/MathProject_AST_Research.git` (fetch/push)
*   **Working Tree**: Clean (nothing to commit).

### Repository B: Formal Boundary Repo
*   **Local Path**: `C:\Projects\MathProject_AST_Research_HealerBoundary`
*   **Active Branch**: `main` (up-to-date with `origin/main`)
*   **HEAD Commit**: `8c8ff3078b5915f45d9d25b4c08a97595a53ecc6` ("document zero frozen-rule Healer applicability in CE115 confirmatory run")
*   **Git Remotes**:
    *   `origin`: `https://github.com/yyfsunnyboy/MathProject_AST_Research_HealerBoundary.git` (fetch/push)
    *   `upstream`: `https://github.com/yyfsunnyboy/MathProject_AST_Research.git` (fetch/push)
*   **Working Tree**: Uncommitted changes in `docs/experiments/analysis/ce115_healer_eligibility_census.json` and some untracked experimental logs.

---

## 2. Competition Release Version Determination

### Timeline Audit
Based on the project's work journal (`专案速查.md`) and core integration reports (`00_核心報告.md`), the core system was deemed **"ready for science fair"** around **mid-February 2026** (specifically between February 15 and February 20, 2026). The following three candidate commits are identified as the most likely representation of the competition release version:

1.  **Commit `8e453e3c` (Date: Wed Feb 25 15:02:53 2026 +0800)** — **FINAL CHOICE**
    *   *Message*: `*8b解析題目失敗 改由gemini解析 前`
    *   *Reason*: This is the last commit modifying the core healer scripts (`regex_healer.py`, `ast_healer.py`, and `unified_cleanup_healer.py`) during the February development cycle, capturing the exact code state active during the final competitive experiments.
2.  **Commit `2815f295` (Date: Fri Feb 27 00:03:52 2026 +0800)**
    *   *Message*: `*UPDATE SKILL.MD`
    *   *Reason*: The last commit prior to March 1, 2026, capturing the overall codebase state right at the end of the competition month.
3.  **Commit `7313e632` (Date: Mon Mar 2 17:00:12 2026 +0800)**
    *   *Message*: `*接近完成版v0.99`
    *   *Reason*: Represents the near-completion state before subsequent March features (fraction addition, UI restructuring) were integrated.

---

## 3. Healer File Blob Hashes Audit

The table below contrasts the git blob hashes for the key Healer-related files at the competition release state (Commit `8e453e3c`) versus the current `HEAD` state.

| File Path | Competition Hash (`8e453e3c`) | Current HEAD Hash | Status |
| :--- | :---: | :---: | :--- |
| `core/healers/regex_healer.py` | `38632f0b` | `e9aab2ac` | **Modified** (Post-competition rules added) |
| `core/healers/ast_healer.py` | `5f6e3f51` | `32d79432` | **Modified** (Jul 2026 configurability added) |
| `core/healers/unified_cleanup_healer.py` | `b1e134d6` | `b1e134d6` | **Identical** (Unchanged since Feb 2026) |
| `core/code_generator.py` | `5bdfcd04` (at `9c1fae77`) | `488d36dc` | **Modified** (Domain library JIT injection added) |
| `core/prompts/domain_function_library.py` | `c8a27321` (at `9c1fae77`) | `180f4775` | **Modified** (Polynomial classes added) |

### Verdict on User-Provided Workspace Code
**The workspace code does NOT exactly match the competition release commit.** Several advanced post-competition rules and configuration options were added to the codebase after March 1, 2026.

---

## 4. Post-Competition Code Modifications

The following rules and configurations were introduced **after** the competition release:

*   **In `regex_healer.py`**:
    *   `simplify_term` tuple-as-key dict repair (V4.3b)
    *   `fix_missing_correct_answer` (V4.3)
    *   `fix_shadowed_correct_answer` (V4.1)
    *   LaTeX regex syntax corrections and standard library import protections (V3.4, V3.5)
*   **In `ast_healer.py`**:
    *   Configurable `require_entry_point` and `entry_point` parameters for `ASTHealer` (Jul 2026).
    *   Module whitelist protections in `visit_Import`/`visit_ImportFrom` (allowing `math`, `random`, `fractions`, `decimal`, `re`, `typing`, `core`).
*   **Live Show Core**:
    *   `live_show_healer.py` and `live_show_iso_guard.py` (which implement UI display sanitizing, display logging, and ISO/STYLE guard decision fallbacks) were created entirely post-competition (first added in March 2026, commit `3b1bffe8`).
