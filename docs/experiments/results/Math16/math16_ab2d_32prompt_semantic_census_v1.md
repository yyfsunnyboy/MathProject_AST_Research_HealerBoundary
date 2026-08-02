# Math16 Ab2d 32-prompt semantic census v1

**Date:** 2026-08-02  
**HEAD:** `5adecb775291f8c2927e80c4b7bd04c66c3aea8a` (`origin/main`)  
**Mode:** Read-only semantic census of rendered prompts; **no model calls**; no builder/prompt/manifest edits; no qualification re-run; no formal; no commit/push.

**Scope:** 16 domain-menu + 16 full-plan = **32** rendered prompts under:
- `docs/experiments/prompts/ab2d_domain_menu/prompts/*.txt`
- `docs/experiments/prompts/ab2d_full/prompts/*.txt`

**SHA convention:** SHA-256 over raw UTF-8 bytes with **LF** line endings. After freeze-prep normalization, `ab2d_full` and `ab2d_domain_menu` prompts are both LF on disk; raw-byte SHA == LF text SHA (16/16).

**Supersedes (prompt inventory / 清冊):**  
`docs/experiments/results/Math16/math16_ab2d_domain_menu_vs_full_plan_prompt_review_v1.md`  
— post-API-fairness **current** 16×2 prompt index/review (SHA ledger + path inventory; pre–answer-contract SHAs). This census fully replaces that role for the **answer-contract-aligned** prompts.

**Not deleted (explicit keep):**
- `…_prompt_review_v1_BEFORE_FAIRNESS_FIX.md` — historical fairness-defect archive  
- `math16_ab2d_answer_contract_fairness_review_v1.md/.json` — fairness checklist  
- `math16_ab2d_qualification_8cell_forensic_v1.md`  
- `math16_historical_answer_contract_audit_v1.md`  
- `ab2d_full_prompt_sha_before_fairness_fix_v1.json` / void notice  
- manifests, freezes, rendered prompts, qualification artifacts  

---

## VERDICT

**`ALL_32_PROMPTS_SEMANTICALLY_CLEAN`**

All 16 task pairs (32 prompts) classified **PASS**. No CONTRACT / API / STEP / ASYMMETRY / CONTRADICTION / OTHER defects under the required semantic checks.

---

## 32_PROMPT_LEDGER

| # | task_id | domain | oracle_type | menu SHA-256 (LF) | full SHA-256 (LF) | class |
|---|---------|--------|-------------|-------------------|-------------------|-------|
| 1 | `ce115_calc_polynomial_division_l1` | PolynomialOps | `math16_polynomial_division_general` | `144140ee65e58fc71e1ec91af2e26d4a863f23a573e1ad7749a1755aa302a2d9` | `8ecdb1868647c3e0c0b1ea7d11f8b095ad469b915d6ef5190f8fb8de2e7ffb24` | **PASS** |
| 2 | `ce115_calc_polynomial_factor_roots_l1` | PolynomialOps | `math16_polynomial_factor_roots` | `0bc09d453a5dc1ccea4bd4c71fc3cdbc1bc1e608898f639391b499b4f38b5dd5` | `9a19a9367399acf7fc4caca863da11813a36469fd9cafd3013bccb4a8a9dabf7` | **PASS** |
| 3 | `ce115_calc_exact_rational_expression_l1` | FractionOps | `math16_exact_rational_expression` | `795455a908a80eaf519907d374f5fd0ba1dc51427e1fabfe1e8a15c8c4727c9e` | `8780284cc27ea2c065955fe87008d41de62a7d941931d1bb026222792e211b9a` | **PASS** |
| 4 | `ce115_calc_radical_simplification_l1` | RadicalOps | `math16_radical_simplification` | `b263e45893394834484a4aae030836eadf40b024f0663b0fa287f708105f6227` | `de7a60324c63c57bc7f6a827d34dc4fe7f20557e4c345c449f34b6fc35bcc294` | **PASS** |
| 5 | `ce111_q02_polynomial_division_remainder` | PolynomialOps | `polynomial_division_remainder_only` | `15567f15032a8ccf9ffe63f9206d61803c05ec3393d55a4bee82a625ed3dedbe` | `c121b04a30653d3116be4c4065941a588dbb1604d00f84fc357dd585d9adbb10` | **PASS** |
| 6 | `ce111_q08_polynomial_factor_parameter_recovery` | PolynomialOps | `polynomial_factor_parameter_recovery` | `e130eaffa24f327a71c9028827955a6e61af8751d90b6056f13a172c7a05841c` | `408fd9da7874800eeace4bf846604067fcd8eeb3d9cb38051685fb79be0197ea` | **PASS** |
| 7 | `ce111_q03_prime_factor_selection` | IntegerOps | `integer_exact` | `0b27ebe0d9223f8e08095a312655fb782539eb81c60eb2ae14becbe872bf7c9f` | `d09e8efa62e427f8769c437d7a5d289196070cb6845e68bb9e98fcaa650445b6` | **PASS** |
| 8 | `ce112_q01_negative_integer_power` | IntegerOps | `integer_exact` | `d5a5c3a6308cac2c4da8aaee26981fe5cd281714aaf3a1b21042cf63f8d37a10` | `44257e3240107a4efa29464d474ddd902bb8ba5bfeba8dd81d63f69cddf3f774` | **PASS** |
| 9 | `ce112_q09_divisor_multiple_intersection` | IntegerOps | `integer_count` | `2092a5831e773fb1d16b1744eaf5a6155569d9f55749f30930e252040e61bc89` | `70ff0014ba7307ce7daf80dc35ac3fccc703047b2bfb117845912188223eed48` | **PASS** |
| 10 | `ce111_nonchoice_q01_part1_exponential_growth` | IntegerOps | `integer_exact_k` | `7e3e01be7ef566d40dd4e9575a73f2300f3ca15036ff658b15990c7a72196786` | `8e8af118e3e098a9fdcb85e24a823453fb8c90ae2581a3f1c6c0373f17a34532` | **PASS** |
| 11 | `ce111_q05_exact_fraction_expression` | FractionOps | `exact_fraction_canonical` | `bcbdcfa292675732a0d5b95312bb02cabec512f149150cc576ed9cdff2116249` | `149220bc6dd69e3fb7d2821cc5cec2addaf615e27b0a9624c6c7547058396cb6` | **PASS** |
| 12 | `ce113_q01_negative_fraction_subtraction` | FractionOps | `exact_fraction_canonical` | `83f2ae1baaac8eb910bd088232f714f7fcfb6795ef5fa33cf188916279c252a4` | `567e001ca17e997d1b76e14a260c2eaff560f40fdc9420812f1583c05663fbcc` | **PASS** |
| 13 | `ce112_q12_independent_probability_fraction` | FractionOps | `exact_fraction_canonical` | `6ca558abfe3866eb6372c4e64039e7f6e761515be54de795c150d847c9229f1d` | `a042962c632f3c51e5aaa594f290f11ed015979240613a2d53bfc1fc875e3e07` | **PASS** |
| 14 | `ce112_q04_radical_simplification` | RadicalOps | `radical_simplification_canonical` | `cb7fe9221d5d3267564ae35f4adfadd6efe30f565cb6b5cfbec4ee51c9ea8c41` | `c591224324d70c6807c06cf0721a9f57f5b3663010f53ffd5ed95dfa0cab911c` | **PASS** |
| 15 | `ce111_q10_ordered_quadratic_roots_radical` | RadicalOps | `compound_radical_result` | `ee73cd2c4d253cd3270339c542816490d92a803d7f4f3fede0a987b861ddf61b` | `130a3ea350a0961dceae182a61d0bf9d280f85ec0f2a5a79b1542973f6e1f0ae` | **PASS** |
| 16 | `ce113_q11_rationalize_denominator` | RadicalOps | `integer_exact` | `02a0c92cd478f68facad4c46aed1e6ae4f59f021d95182c84b7bb62017beeeb3` | `508fbeb9fe57425ee0e471a3d3b7a7e6c507c9115eae7ad5e7bb98b41da26f5a` | **PASS** |

**Pair count:** 16 pairs × 2 = **32 prompts**, all **PASS**.

Paths: `docs/experiments/prompts/ab2d_domain_menu/prompts/{task_id}.txt` and `docs/experiments/prompts/ab2d_full/prompts/{task_id}.txt`.

---

## DOMAIN_SUMMARY

| Domain | Tasks | APIs exposed (menu=full block) | Cross-domain exposure | Notes |
|--------|------:|-------------------------------:|----------------------:|-------|
| PolynomialOps | 4 | full SUPPORTED_PUBLIC | 0 | div_qr / factor / format covered |
| FractionOps | 4 | full SUPPORTED_PUBLIC | 0 | `to_exact` = serialization only |
| RadicalOps | 4 | full SUPPORTED_PUBLIC | 0 | simplify / compound / rationalize |
| IntegerOps | 4 | full SUPPORTED_PUBLIC | 0 | bare int / `{count}` / `{k}` via contract only |

---

## CONTRACT_CHECK

| Check | Result |
|-------|--------|
| `## Task-specific answer contract` in all 32 (after domain API end) | **PASS** |
| menu ↔ full contract block byte-identical (LF text, 16/16) | **PASS** |
| Body contains verbatim `CONTRACTS[oracle_type]` | **PASS** |
| Contains `Required return schema:` | **PASS** |
| Matches task `oracle_type` / evaluator schema | **PASS** |
| No gold `correct_answer` dump inside contract | **PASS** |
| Shared output points to Task-specific contract (not vague-only shape) | **PASS** |
| Generic example marked `ILLUSTRATIVE ONLY — see Task-specific answer contract` | **PASS** |

---

## API_SURFACE_CHECK

| Check | Result |
|-------|--------|
| `Domain for this task: {Ops}.` correct per task | **PASS** |
| Domain API blocks menu ↔ full identical (LF text) | **PASS** |
| Foreign `*Ops` absent from block | **PASS** |
| Fraction `to_exact` clarified (does not decide final schema) | **PASS** |
| `derived_scaffold` absent | **PASS** |
| No template placeholders `{{` / TODO / FIXME | **PASS** |

---

## PROCESSING_STEPS_CHECK

| Check | Result |
|-------|--------|
| domain-menu has **no** `## Processing steps` | **PASS** |
| full-plan has `## Processing steps` for all 16 | **PASS** |
| Final step: `Assemble correct_answer exactly according to the Answer contract.` | **PASS** |
| No banned schema literals in steps (`{"count"}`, `{"k"}`, Pack, bare-return, nested-or-flat, Required return schema) | **PASS** |
| No gold-answer leakage in steps | **PASS** |
| Math/API flow reasonable (incl. native arithmetic where appropriate) | **PASS** |

`ce111_nonchoice_q01_part1_exponential_growth` uses native `*` / `//` without `IntegerOps.` — intentional for generation-count; **PASS** (not an API defect).

Fraction exact-rational step 3 restates that `to_exact` does not define final schema — clarification, not schema-literal assembly.

---

## CROSS_CONDITION_DIFF_CHECK

| Check | Result |
|-------|--------|
| LF-normalized `full` base == `menu` | **PASS** 16/16 |
| Sole semantic delta = trailing `## Processing steps` | **PASS** 16/16 |
| Stem + `frozen_params` identical across conditions | **PASS** |
| Answer contract / API / shared contract / examples identical | **PASS** |
| On-disk line endings: menu=LF, full=LF (normalized) | **PASS** |

---

## DEFECT_LIST

*(none)*

---

## FORMAL_FREEZE_READINESS

**READY** for formal freeze of the answer-contract-aligned prompt set (LF-normalized; raw-byte SHA aligned with qualification locks and `prompt_freeze.json`).

Qualification artifacts were **not** overwritten; their recorded prompt SHAs match the post-LF formal freeze (4/4 full-plan + 4/4 domain-menu locks checked).

---

## OLD_INVENTORY_DISPOSITION

| Path | Role | Action |
|------|------|--------|
| `docs/experiments/results/Math16/math16_ab2d_domain_menu_vs_full_plan_prompt_review_v1.md` | Current pre-contract-fix **prompt 清冊 / index review** | **Deleted** (replaced by this census) |
| `…_BEFORE_FAIRNESS_FIX.md` | Historical fairness-defect archive | **Kept** |
| `math16_ab2d_answer_contract_fairness_review_v1.*` | Fairness checklist | **Kept** |

---

## REVIEW_DOCUMENT_PATH

`docs/experiments/results/Math16/math16_ab2d_32prompt_semantic_census_v1.md`
