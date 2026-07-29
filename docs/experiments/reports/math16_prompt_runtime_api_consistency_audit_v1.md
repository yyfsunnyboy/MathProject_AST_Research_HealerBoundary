# Math16 Prompt↔Runtime API Consistency Audit v1 (draft)

> **status:** `development_candidate_not_frozen`
> **HEAD:** `f0eae63fe8c3760e9912589654657510119175ce`
> **origin/main:** `f0eae63fe8c3760e9912589654657510119175ce`

## Verdict

Ab2d+api and Ab2d+spec（現行 `ab2d_spec_v2`）**不是同一組暴露面**。Math16 runtime 對所有 cell 注入四個 Ops class，因此存在大量 `AVAILABLE_NOT_EXPOSED` 可呼叫表面；Aggressive Healer 正式 contract 候選只能來自各 condition 的 `EXPOSED_AND_AVAILABLE` 且 `allow_model_direct_call=true` 項目。

## Checks performed

| Check | Result |
|---|---|
| Prompt claims missing at runtime | **None** among positively exposed method names (no `EXPOSED_NOT_AVAILABLE` class_method). Negative mention of absent `PolynomialOps.to_latex` documented under C5. |
| Runtime exists but prompt does not expose | **Yes** — majority of 43 methods are `AVAILABLE_NOT_EXPOSED` under both conditions. |
| Same name, signature mismatch (Ab2d+api vs SSOT) | **None detected** (SSOT render is the Ab2d+api prompt line source). |
| Return shape vs prompt (Ab2d+api) | **Aligned** with `DOMAIN_API_SSOT` via `render_api_prompt_line`. |
| Ab2d+api vs Ab2d+spec exposure equality | **Not equal** (C1). |
| Four-domain exposure style consistency | **Not consistent under Ab2d+spec** (C8); Ab2d+api uses uniform SSOT card format but task-local subsets differ. |
| Same-name global function vs class method | **No collision** on Math16 injected surface (C9). |
| Import required? | Prompt documents import path; **runtime injects classes** (import optional). |
| Model redefines Ops class/function | **Overwrites injection**; not blocked (C4). |
| Early incomplete spec-v1 included? | **No** — excluded by design. |
| ab2d_spec_v2 byte SHA == manifest? | **No on this tree (CRLF)**; canonical LF SHA **matches** all 16 (C10/U5). |

## Major findings

### C1 — Ab2d+api vs Ab2d+spec exposure lists differ (high)

Ab2d+api exposed methods: ['FractionOps', 'FractionOps.add', 'FractionOps.create', 'FractionOps.mul', 'FractionOps.sub', 'FractionOps.to_latex', 'IntegerOps', 'IntegerOps.fmt_num', 'IntegerOps.is_divisible', 'IntegerOps.safe_eval', 'PolynomialOps', 'PolynomialOps.div_qr', 'PolynomialOps.factor_quadratic_exact', 'PolynomialOps.format_latex', 'PolynomialOps.mul', 'RadicalOps', 'RadicalOps.format_expression', 'RadicalOps.format_term', 'RadicalOps.simplify_term']. Ab2d+spec exposed methods: ['FractionOps', 'FractionOps.add', 'FractionOps.create', 'FractionOps.from_parts', 'FractionOps.mul', 'FractionOps.sub', 'PolynomialOps', 'PolynomialOps.div_qr', 'PolynomialOps.format_latex', 'RadicalOps', 'RadicalOps.simplify_term']. Only-in-api: ['FractionOps.to_latex', 'IntegerOps', 'IntegerOps.fmt_num', 'IntegerOps.is_divisible', 'IntegerOps.safe_eval', 'PolynomialOps.factor_quadratic_exact', 'PolynomialOps.mul', 'RadicalOps.format_expression', 'RadicalOps.format_term']. Only-in-spec: ['FractionOps.from_parts'].

### C2 — Integer family is API-exposed under Ab2d+api but native-only under Ab2d+spec (high)

All four Integer Math16 tasks are native-only in ab2d_spec_v2 (no Domain API). Ab2d+api exposes IntegerOps.is_divisible / safe_eval / fmt_num.

### C3 — Runtime injects all four Ops classes for every Math16 cell (medium)

_execute_generate_all_ops always injects IntegerOps, FractionOps, RadicalOps, PolynomialOps regardless of prompt condition or family. Prompt may say import is required; runtime does not require import. Many AVAILABLE_NOT_EXPOSED methods are therefore callable if the model invents them.

### C4 — Model redefinition of Ops is not blocked by Math16 evaluator (medium)

Candidate exec shares the injected namespace. A later class/assignment named IntegerOps/FractionOps/RadicalOps/PolynomialOps overwrites the injected binding. Math16 pilot02 path does not run CE115 assembly FORBIDDEN_HELPER_REDEFINED scanner.

### C5 — Negative mention of non-existent PolynomialOps.to_latex in Ab2d+spec (medium)

API Signature Cards explicitly state there is NO PolynomialOps.to_latex. Runtime confirms absence. Recorded as consistency note, not as inventory symbol.

### C6 — ce115_calc_exact_rational_expression_l1 operator mismatch across conditions (medium)

Ab2d+api exposes FractionOps.add; Ab2d+spec guardrail names FractionOps.sub; Ab2d+spec scaffold example shows FractionOps.add. Both add and sub exist at runtime.

### C7 — Ab2d+api Radical task ce113_q11 exposes FractionOps only (low)

ce113_q11_rationalize_denominator is Radical family under Ab2d+api but TASK_DOMAIN_APIS lists FractionOps.create/mul/add only; RadicalOps.rationalize_linear_denominator is SUPPORTED_PUBLIC in SSOT but AVAILABLE_NOT_EXPOSED for Math16 Ab2d+api. Ab2d+spec makes this task native-only.

### C8 — Four domains do not use identical exposure style under Ab2d+spec (low)

Integer: native-only. Fraction: API cards (+ create/from_parts) + guardrail methods. Polynomial: mixed (native-only q08/factor_roots; API cards / guardrails on others). Radical: mostly guardrail/class mentions without SSOT-style cards; q11 native-only.

### C9 — No same-name global function vs class method collision on Math16 Ops surface (info)

Live Math16 surface uses Class.method only. Module globals get_required_domains / get_domain_helpers_code are not injected. No bare fmt_num/create global aliases observed in Math16 runner namespace.

### C10 — ab2d_spec_v2 prompt files are CRLF on this working tree (medium)

Byte SHA of frozen prompt files != manifest exact_prompt_sha256 due to CRLF. Canonical LF SHA matches manifest for all 16 tasks. Dual map in registry `ab2d_spec_v2_prompt_hash_dual`.

## UNRESOLVED

### U1 — Whether Aggressive Healer should treat cross-family FractionOps exposure on Radical/Polynomial Ab2d+api tasks as in-scope Integer/Fraction/Radical/Polynomial contract buckets

- Missing evidence: No frozen Aggressive Healer scope decision document in this Step -1 pass; inventory records home domain of the symbol, plus exposing_task_domains.

### U2 — Ab2d+spec tasks that say 'Use RadicalOps' without naming methods (e.g. ce111_q10)

- Missing evidence: No method-level API Signature Card in frozen prompt; cannot mark specific RadicalOps.* methods as prompt_exposed without guessing.

### U3 — Historical Gemini primary Ab2d+spec-v1 incompleteness details

- Missing evidence: Intentionally excluded: current formal Ab2d+spec is ab2d_spec_v2 only. v1 paths under docs/experiments/prompts/ab2d_spec/ are not contract evidence for this audit.

### U4 — Return-shape prose for Ab2d+spec methods that lack SSOT card lines

- Missing evidence: Where Ab2d+spec only names a method in guardrails without signature/returns card, return_type_or_shape falls back to DOMAIN_API_SSOT if present, else UNRESOLVED.

### U5 — ab2d_spec_v2 frozen prompt on-disk byte SHA vs manifest exact_prompt_sha256

- Observed: working-tree prompt files use CRLF; byte SHA != manifest; canonical LF SHA matches all 16.
- Freeze implication: lock byte policy and/or normalize before hashing; do not treat CRLF byte-drift as content change without checking canonical hash.

## Status statistics

| Status | Ab2d+api | Ab2d+spec |
|---|---:|---:|
| `EXPOSED_AND_AVAILABLE` | 19 | 11 |
| `AVAILABLE_NOT_EXPOSED` | 30 | 38 |
| `EXPOSED_NOT_AVAILABLE` | 0 | 0 |
| `LEGACY_ONLY` | 0 | 0 |

## Evidence source SHA-256

| Path | SHA-256 |
|---|---|
| `core/prompts/domain_function_library.py` | `836de2f9229f1b2b52765d0a9c7b91af0e61eb58e092ffd8dd607d975ef80e3c` |
| `agent_tools/finals_rebuild/domain_api_ssot.py` | `5801f7ad3c7876fecbf672be034501e205d01dc0107694c886826537e148b443` |
| `agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py` | `7b7f373fc648048e0770a686ac823848ac077873a9ce6fce737d8cf3b3501c90` |
| `agent_tools/finals_rebuild/math16_pool.py` | `406965451600809fb0abb771073b90080eb2bc195fb4aabb8339413d42734a59` |
| `scripts/run_math16_latex_v1_gemini_live.py` | `fd757e612e9a82dcb0036796113f6e1ab368d65e8e4c30a9abfb9a9c5f2015d4` |
| `scripts/evaluate_math16_pilot02_full_v4.py` | `2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc` |
| `docs/experiments/prompts/ab2d_spec_v2/manifest.json` | `e204e07957b7b88ffb60e8d93e9f9a3ab7661c33c81877d1ad29f3d038f29ffd` |
| `tests/finals_rebuild/test_math16_domain_api_ssot.py` | `9657e0ae7a56f0cd0e5021f68cfa3c09d6f7d68bd677d74c1c46732a6d62db67` |
| `tests/finals_rebuild/test_domain_api_contract_hardening_v2.py` | `26efbf14e6ca8d897296d9739bd1e19e6b4c37493cd6bc7aaef506beca546638` |
| `tests/test_math16_ab2d_spec_v2.py` | `d7d882695ea1ee82f3449cd0a69156e13cb186aaf6686f49fb79c6e9a9d3b082` |
| `docs/experiments/templates/ab2d_spec_v2/integer_domain_scaffold_compact.py` | `657069bd70e3507be53c337716683e96f67b0321c3ac000b4a2177df903ff799` |
| `docs/experiments/templates/ab2d_spec_v2/fraction_domain_scaffold_compact.py` | `66a7e1dd30bac50608f685b78a798fada0a6dc54b7df9e2fe236753bfc9f6b4a` |
| `docs/experiments/templates/ab2d_spec_v2/polynomial_domain_scaffold_compact.py` | `8aadbb6a9eb7a591e4bcbe2d5300e44a8b5ebb1f215451411cea076c85a7ed1b` |
| `docs/experiments/templates/ab2d_spec_v2/fraction_api_signature_card.md` | `4aaca01072b24d7688a70d309d53022d41425889ee905b3b61d5cec6fa23e39a` |
| `docs/experiments/templates/ab2d_spec_v2/polynomial_api_signature_card.md` | `c2188e6133254f65f073b4da7cc52243013a945b6a0c22d7eaa0847c86c6440b` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q03_prime_factor_selection.txt` | `c956a2a44c3fd9140b6cf0a456ca6c9be05edf181c270367ef38b5b84555f863` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q01_negative_integer_power.txt` | `c35bade2203f604df9a893d692deb38fd82bc8899dfeba56893b4966f699290b` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q09_divisor_multiple_intersection.txt` | `121936689c850cfca329f2c605b90159bef31fea727950e221004d37e23f03c2` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_nonchoice_q01_part1_exponential_growth.txt` | `07834f7481b95ac7bf03eab19b339d0094c312b01eb6c3f0be4d345ef64688dc` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q02_polynomial_division_remainder.txt` | `6519e47182f1bc18b1d2be6919de8fb4a674bd05884c96d748f18e91ff91648a` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q08_polynomial_factor_parameter_recovery.txt` | `dcae6133350560dce6afb58b968f780d77003c1d27fc66562fe8d8cd7c7829d9` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_polynomial_division_l1.txt` | `f94f4bdfe0ac93412a9239feee82ce612f19b21adf5b8937be3a0f845d956f9c` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_polynomial_factor_roots_l1.txt` | `f964fcf6767715d080db4c660c0d87fa02f58d75fb9cbeacf2ffbd34191dd04b` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q10_ordered_quadratic_roots_radical.txt` | `15601ab1ed75054ddb60ba5d91cd1bcc88250f78d4f78b94b03e6ab98157e2e1` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q04_radical_simplification.txt` | `3c4fb3e875ca39aa1ac8dcbb6004fd897a32717867992a87620b1a46fbbba701` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce113_q11_rationalize_denominator.txt` | `1089e14bff6d728ee94f9c6551e9469fd8c685830c393d119dd4a01bc04d43e7` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_radical_simplification_l1.txt` | `41020a535d5116a6075bfdb126eede46b763385498ce7e4c5c5c79eafd2c3481` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q05_exact_fraction_expression.txt` | `5fcface8323398af41c3ad69a79f44554a4ea4a4c1338f1e46450a565f078828` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q12_independent_probability_fraction.txt` | `12d4f290ea1ba1e4d212da8caa8cc9df80a10c87bb043d2fd8294391778d9a48` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce113_q01_negative_fraction_subtraction.txt` | `0da97fd94d049db659321a60e253b21007aa38de1dba22edde05ebd48bc2347d` |
| `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_exact_rational_expression_l1.txt` | `a69b56dbc115527e4b3481363595caa57bbcb7cf0f0729b77ecb948ce9647d57` |

## Draft artifact SHA-256

| Path | SHA-256 |
|---|---|
| `docs/experiments/design/math16_domain_api_inventory_v1.md` | `353804b3bc18532b86060ed1e915ecf3244907930426baddae46e4516871e972` |
| `docs/experiments/manifests/math16_domain_api_contract_registry_v1.json` | `9e2ae6ca6ce0570bbb2d409278baef57910f182b5baeec7e92d6fce6b2d857c7` |
| `docs/experiments/reports/math16_prompt_runtime_api_consistency_audit_v1.md` | *(Post-write digest)* |

## Future freeze lock list

- `agent_tools/finals_rebuild/domain_api_ssot.py (DOMAIN_API_SSOT + API_CLASSIFICATION)`
- `agent_tools/finals_rebuild/ce115_clean_incremental_ablation.py (TASK_DOMAIN_APIS + domain_section)`
- `docs/experiments/prompts/ab2d_spec_v2/manifest.json and prompts/*.txt`
- `docs/experiments/templates/ab2d_spec_v2/*`
- `core/prompts/domain_function_library.py (four Ops classes)`
- `scripts/run_math16_latex_v1_gemini_live.py::_execute_generate_all_ops`
- `scripts/evaluate_math16_pilot02_full_v4.py`
- `tests/finals_rebuild/test_math16_domain_api_ssot.py`
- `tests/finals_rebuild/test_domain_api_contract_hardening_v2.py`
- `tests/test_math16_ab2d_spec_v2.py`

## Declarations for this Step -1 pass

- Did not modify `core/healers`
- Did not execute models
- Did not run formal Healer replay / evaluator scoring of Math16 cells
- Did not modify existing 320-cell results / figures / one-pager / final report
- Did not commit or push
- Did not invent alias mappings

## Post-write artifact digest

- inventory: `353804b3bc18532b86060ed1e915ecf3244907930426baddae46e4516871e972`
- registry: `9e2ae6ca6ce0570bbb2d409278baef57910f182b5baeec7e92d6fce6b2d857c7`
- consistency audit: `cb1218a416bc4cce510da69a736daca1d30a8ddf638b5a4b68dcc24eb5397170`
