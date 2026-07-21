# Math16 Pilot-02 Qwen 3.5 9B Runtime Preregistration / Freeze

```text
QWEN9B_RUNTIME_PREREGISTRATION_FROZEN
QWEN9B_320CELL_PLAN_VERIFIED
QWEN9B_ZERO_MODEL_PREFLIGHT_PASSED
QWEN9B_320CELL_GENERATION_READY
```

**Policy:** zero-model freeze only — no generation, no Ollama `/api/chat` calls.
Probes allowed: `/api/tags` `/api/show` `/api/version` `/api/ps`.

## 1. Scope

Cross-model Math16 Pilot-02 geometry for **Qwen 3.5 9B**: 16 tasks × 4 conditions × 5 seeds = **320 cells**.

Except for the model itself, design is **identical to Qwen 4B**.

| Condition (machine) | Display | Prompt asset |
| :--- | :--- | :--- |
| `ab1` | Ab1 | Same builder as Qwen 4B / Gemini Pilot-02 |
| `ab2g` | Ab2g | Same builder as Qwen 4B / Gemini Pilot-02 |
| `ab2d` | Ab2d+api | Same builder as Qwen 4B / Gemini Pilot-02 |
| `ab2d_spec_v2` | Ab2d+spec-v2 | Frozen `ab2d_spec_v2` files (shared with Qwen 4B) |

## 2. Locked shared assets

- Seeds: `[2026071301, 2026072001, 2026072002, 2026072003, 2026072004]`
- Evaluator SHA: `2cca19f2258d4ba6134ff10d4e9bcff925e2441c32820fcbc151cb6b1dd740bc`
- Taxonomy v3 SHA: `7df8f4472ce048569967436cbc73ede8fd4bd117ad67d0028ddd95af2055a304`
- Healer allowlist SHA: `c8a9f1749411858c1dd5b437da44708b291f5d5e66e36ab9f04846d57f6bd5c4`
- Corrected-chain Healer runner SHA: `38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf`
- Healer protocol SHA: `bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39`
- Source commit (at freeze build): `7a7e0d95df1c16c698902c88a842e1f830ad69b8`
- Qwen 4B alignment reference: `math16_pilot02_qwen4b_runtime_manifest.json`

## 3. Sampling rationale

> 本實驗固定temperature=0.2、top_p=0.8、top_k=20與think=false，並與Qwen 4B完全一致。temperature作為主要抽樣隨機性控制參數；top_p與top_k沿用既有凍結設定，未另行調校。本設定目的不是尋找Qwen 9B最佳解碼參數，而是建立可重現且除模型大小外保持一致的公平比較。

## 4. Qwen 9B runtime (queried)

- **model_provider**: `ollama`
- **model_tag**: `qwen3.5:9b`
- **model_digest**: `6488c96fa5faab64bb65cbd30d4289e20e6130ef535a93ef9a49f42eda893ea7`
- **model_version**: `qwen3.5:9b@6488c96fa5fa`
- **architecture**: `qwen35`
- **parameter_count**: `9653104368`
- **parameter_count_label**: `9.7B`
- **parameter_count_basis**: `ollama /api/show model_info.general.parameter_count`
- **quantization**: `Q4_K_M`
- **runtime**: `ollama`
- **runtime_version**: `0.32.1`
- **transport**: `http://localhost:11434/api/chat`
- **endpoint**: `POST /api/chat`
- **thinking_mode**: `False`
- **temperature**: `0.2`
- **top_k**: `20`
- **top_p**: `0.8`
- **repeat_penalty**: `ollama_default_unset`
- **seed_transport_supported**: `True`
- **seed_transport_field**: `options.seed`
- **seed_role**: `model_rng_seed_and_cell_label`
- **context_window**: `65536`
- **max_output_tokens**: `24576`
- **timeout_seconds**: `1800`
- **stop_sequences**: `[]` (not set; Ollama default (empty))
- **retry_policy**: `{"max_attempts": 3, "retry_delays_seconds": [5, 20, 60], "retryable": ["timeout", "connection_failure", "empty_response"]}`

### Thinking mode

```text
think=false
```

### Hardware

- CPU: `AMD Ryzen 5 7500F 6-Core Processor`
- GPU: `NVIDIA GeForce RTX 5060 Ti`
- VRAM: `16311 MiB`
- RAM: `31.6 GiB` (`33934004224` bytes)
- OS: `Windows 11 (10.0.26200)`
- Driver: `591.86`

### Cold / warm

- Definition: warm = model currently listed in Ollama /api/ps; cold = not loaded into runner VRAM/process until first request
- Observed at preregistration: **cold**
- Policy: Generation may start cold or warm; do not treat warm-start latency differences as outcome confounds. Do not unload/reload mid-cohort to chase warm state.

## 5. Runtime fingerprint

- **Qwen 9B fingerprint**: `f45f79238bbf9400729fd00dbfaf4e33a7a7716cb9f81d4095a1fd1d52e0da5b`
- **Qwen 4B fingerprint (reference)**: `33fd7603f58cdc47843bb048456d6d167dd71dc891b636377baf33dea30358f7`

Fingerprint differs from 4B by model identity fields (tag/digest/parameters/version) while sharing prompt_manifest_hash, evaluator/taxonomy/healer hashes, seeds, and sampling.

## 6. Expected cell geometry

```text
16 tasks × 4 conditions × 5 seeds = 320 cells / model
4 families × 4 tasks × 4 conditions × 5 seeds = 80 cells / family
```

- 320 unique `cell_id`
- 80 / condition, 80 / family, 20 / task, 64 / seed
- Prompt SHA identical to Qwen 4B for all 16×4 condition/task pairs

## 7. Prompt SHA registry (16 × 4)

| Task | Cond | Path | SHA-256 |
| :--- | :--- | :--- | :--- |
| `ce111_q03_prime_factor_selection` | `ab1` | `(builder)` | `398a9ab7067574286a3f7b6a955033b2f3af8d244d34098aa907623bb706bcc4` |
| `ce111_q03_prime_factor_selection` | `ab2g` | `(builder)` | `5436b011cb2be3d0edee52770f8c5a28348f9ef4763ae485b8c6a80798ef1cbf` |
| `ce111_q03_prime_factor_selection` | `ab2d` | `(builder)` | `8704669323fb45ef6bd34331151b350845425d2d14e19b36c58bd2c2c86bc75f` |
| `ce111_q03_prime_factor_selection` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q03_prime_factor_selection.txt` | `5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0` |
| `ce112_q01_negative_integer_power` | `ab1` | `(builder)` | `d7f97e59388da3962bab6c3b0b55ebacdb7679340bf7955215431120c98301c9` |
| `ce112_q01_negative_integer_power` | `ab2g` | `(builder)` | `cf486895c58fc5f91aaf2ba8cb03259f0eb98cb10d99a9d8a5734721bfdd7edb` |
| `ce112_q01_negative_integer_power` | `ab2d` | `(builder)` | `a03c40a37de8c5652476da0fcd76dfc714ca55c19b0279b0452358c81ccde8d4` |
| `ce112_q01_negative_integer_power` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q01_negative_integer_power.txt` | `1aa4f2a789b546a5f81f4a773db6c783edb359f5fbbc3c21966853d57db6a61b` |
| `ce112_q09_divisor_multiple_intersection` | `ab1` | `(builder)` | `7eafd0610772ae6f3576a2d7d24017b28f0195d01e3b713feb8a6b629a79148e` |
| `ce112_q09_divisor_multiple_intersection` | `ab2g` | `(builder)` | `8465217dde30310c3f927c2ec00e152e065f40c5508cd0339ae46a541c19496e` |
| `ce112_q09_divisor_multiple_intersection` | `ab2d` | `(builder)` | `f4d5abe47b1d3dad2095dbc473b4f58b6f1c8cd4f9ece0ba8a1de9f5c68ad5cb` |
| `ce112_q09_divisor_multiple_intersection` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q09_divisor_multiple_intersection.txt` | `6ab35b719b39c1336e47f8fea3d373ec2482ad3f8d1c6979b192576090228035` |
| `ce111_nonchoice_q01_part1_exponential_growth` | `ab1` | `(builder)` | `105840296a8d546e9ca86a9aa27cf92df5da24004f78624f5fd96e031b114d62` |
| `ce111_nonchoice_q01_part1_exponential_growth` | `ab2g` | `(builder)` | `93f82f61b6271d56cbaf1b7bf1276afc821b055cf767d2e9a496414ee933441e` |
| `ce111_nonchoice_q01_part1_exponential_growth` | `ab2d` | `(builder)` | `1f1491d3b68e9620550398001b27cd72e2f8b6c08c2debbf346396314a69cb42` |
| `ce111_nonchoice_q01_part1_exponential_growth` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_nonchoice_q01_part1_exponential_growth.txt` | `5d8e3f4084038b1e99a581bf26ad77e49c295362a076ff374e5614960f38c019` |
| `ce111_q02_polynomial_division_remainder` | `ab1` | `(builder)` | `138e8eae8822fb96a655fd1cfb5c14873f5397fb4b5a09ed617defd5fc0e42e5` |
| `ce111_q02_polynomial_division_remainder` | `ab2g` | `(builder)` | `1cb912077ad2776904919f36b8947a00c6986c58c24c9311c1d8872dbc447e31` |
| `ce111_q02_polynomial_division_remainder` | `ab2d` | `(builder)` | `d625ce0bed3b073c6289454121ab9960e1c1965a824c9db6a575d7ecbd3c0aa9` |
| `ce111_q02_polynomial_division_remainder` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q02_polynomial_division_remainder.txt` | `f9a51940b166e8613557d1490cf1a331467ffd95af8ca96617aeded15c78fb87` |
| `ce111_q08_polynomial_factor_parameter_recovery` | `ab1` | `(builder)` | `447f8b48f394c373b3fa8d7fa4d11932cdce5b411bbf27f61cc9e822b2670cd4` |
| `ce111_q08_polynomial_factor_parameter_recovery` | `ab2g` | `(builder)` | `1ddb92a07ec3df5f46360fdf5c9881eb4745bf1f339bac0c6d00e5e41217ac17` |
| `ce111_q08_polynomial_factor_parameter_recovery` | `ab2d` | `(builder)` | `7d993c836b9ef40b49f4c57d44a4c2e08ef6a895b0f2e522f0e7c029fba0a27a` |
| `ce111_q08_polynomial_factor_parameter_recovery` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q08_polynomial_factor_parameter_recovery.txt` | `4e8f345ad99e87317c2bb38ce741268ce4f57d9e2ca98518eea4f37fb36fb477` |
| `ce115_calc_polynomial_division_l1` | `ab1` | `(builder)` | `fdf193cdb3bf18cbd3e37627168fd1824042198d278b2a45114ddc8bacd8ff86` |
| `ce115_calc_polynomial_division_l1` | `ab2g` | `(builder)` | `3d60a095612840e6d08496d68f759c891c049481c5af862609bd89ece29121b6` |
| `ce115_calc_polynomial_division_l1` | `ab2d` | `(builder)` | `79b1936f146728f178f71569aa7cab9c2d284ace6e3fa97604a96c7b97f250d0` |
| `ce115_calc_polynomial_division_l1` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_polynomial_division_l1.txt` | `aac0a64fb450e071435c5a4a1537bb5d9c1725f83c32044002263cfa175d7361` |
| `ce115_calc_polynomial_factor_roots_l1` | `ab1` | `(builder)` | `62fcdc20f64c26274f92f2d05134f84475477eacfec37cfadae8f5dd3505e50e` |
| `ce115_calc_polynomial_factor_roots_l1` | `ab2g` | `(builder)` | `9aa875c3c2de0b79cb0cf0bb5ec18ef9a02ead452db9d4d044500f175a8f485f` |
| `ce115_calc_polynomial_factor_roots_l1` | `ab2d` | `(builder)` | `46eb44551fe48e5def0a14fdfe506b30e5987c44c0dee69f259bf42b90ab54a0` |
| `ce115_calc_polynomial_factor_roots_l1` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_polynomial_factor_roots_l1.txt` | `64ff6dc7b8b1fe7e5e14585fdc620a7ed1d9b0c573d08f1674d5cd55f8709943` |
| `ce111_q10_ordered_quadratic_roots_radical` | `ab1` | `(builder)` | `8371aff72b11bd70ea327920302233f5b7d60c0e6e594daa5ce635ef386d56fb` |
| `ce111_q10_ordered_quadratic_roots_radical` | `ab2g` | `(builder)` | `6179a8fb58654189712d53044e6df49b7171ccf57f1b1666d3e735f38758a766` |
| `ce111_q10_ordered_quadratic_roots_radical` | `ab2d` | `(builder)` | `79e4e1abeee04352b1acfd797ec10815f2614f37bd4c94f0090c6ffef957d2c6` |
| `ce111_q10_ordered_quadratic_roots_radical` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q10_ordered_quadratic_roots_radical.txt` | `87ee0595a5ca441c1e15e5e7131277be034462d69eb6b3f90435a4d2507857f2` |
| `ce112_q04_radical_simplification` | `ab1` | `(builder)` | `f696edca9ba89d8daf6ae0a01bef98c0098c508517ba9d6e631b287fa5764d53` |
| `ce112_q04_radical_simplification` | `ab2g` | `(builder)` | `6d252e1058c14eee07326788693fec710a5247c404e7dd74f3d22156235a82f4` |
| `ce112_q04_radical_simplification` | `ab2d` | `(builder)` | `f4766019ab80cfea7d15b358786ad841f542d8cd57b9dd61f4e7098712dba731` |
| `ce112_q04_radical_simplification` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q04_radical_simplification.txt` | `14468d40af33b62b0c252bc11861baed124b1313d69a77fa4907ba256e91c080` |
| `ce113_q11_rationalize_denominator` | `ab1` | `(builder)` | `16c617438948cbd476c48addcd9cfc9b61c804e3e01b852d5a0eafb883cb34ce` |
| `ce113_q11_rationalize_denominator` | `ab2g` | `(builder)` | `61d3826e10d9cccb5d18a02c8aa951421bd38216d4cd773792201aac261778a7` |
| `ce113_q11_rationalize_denominator` | `ab2d` | `(builder)` | `9d3533f258e5c017845db746fbfb696ba432835385d9f38acf718a6bdff06514` |
| `ce113_q11_rationalize_denominator` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce113_q11_rationalize_denominator.txt` | `4033ab46b2fd824676ffbdde5923011d60dab8b2e0ae8d562ec42a32b75da01a` |
| `ce115_calc_radical_simplification_l1` | `ab1` | `(builder)` | `2a445d5de76c068590ce05619f521eff42098c71257319bf12d82796d4d92f86` |
| `ce115_calc_radical_simplification_l1` | `ab2g` | `(builder)` | `a88ec9aa5f19dc7b5348cdd1cfdc9b503c1fbefcc0ad12889e21eeff5cb19621` |
| `ce115_calc_radical_simplification_l1` | `ab2d` | `(builder)` | `7277f140eeaadbdfe1f64a2215413acadf06fb134b09efa280f2011d19e5588c` |
| `ce115_calc_radical_simplification_l1` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_radical_simplification_l1.txt` | `2708207ae203981a2788e092fe304786ba7cfebc62173946b16030a1bf045aee` |
| `ce111_q05_exact_fraction_expression` | `ab1` | `(builder)` | `321d4fd2830ebc32bfbb64fefd30735af2260cffbb4d5ce695cfe030ca6e2ece` |
| `ce111_q05_exact_fraction_expression` | `ab2g` | `(builder)` | `9932c16c2dd3109a2f340ae98c4b0e51ef01fe9e024fbcc5f63bab49ef3ae965` |
| `ce111_q05_exact_fraction_expression` | `ab2d` | `(builder)` | `68a00937bf4cad2e185ea854b3d92e6fc9615ee0f045b5c86e81879b64976d4b` |
| `ce111_q05_exact_fraction_expression` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce111_q05_exact_fraction_expression.txt` | `927977168ad6a72c644641fed7ef653495e55279689dc0beb06253033242926d` |
| `ce112_q12_independent_probability_fraction` | `ab1` | `(builder)` | `ce709937aef3026d48af8ea0b6eb6dbc53d0c07731b232df03b0657672d7d74c` |
| `ce112_q12_independent_probability_fraction` | `ab2g` | `(builder)` | `d68af74fd5f59ae1178e9835684479397bd58a2b1f31fd9ef7b022e34b96fcf1` |
| `ce112_q12_independent_probability_fraction` | `ab2d` | `(builder)` | `e0ceba6ddea69db946947e44372f0667b4445539f11857bbafa275c518a9506a` |
| `ce112_q12_independent_probability_fraction` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce112_q12_independent_probability_fraction.txt` | `183c3a708e2a1361e9ccd41de1cb33c51bb169b1f6b7cd99d874f98aa23ada51` |
| `ce113_q01_negative_fraction_subtraction` | `ab1` | `(builder)` | `d690b208e09d5f893ecd8b8abc38b4abb7d044968dc42c60dde3de96c0ad410d` |
| `ce113_q01_negative_fraction_subtraction` | `ab2g` | `(builder)` | `b0fe97bca3b7957bb481e88060e49681e6c7ccd67ff19c2eaf13d3ec47559a0b` |
| `ce113_q01_negative_fraction_subtraction` | `ab2d` | `(builder)` | `0fe4bd752d3760f08b8977916ba6edb99a7babd6cc53752bb9d80a684c8514f7` |
| `ce113_q01_negative_fraction_subtraction` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce113_q01_negative_fraction_subtraction.txt` | `319926943ccbc9ca260979e04cf024cc1d896f00bc3e6be23e7b9632170ca54a` |
| `ce115_calc_exact_rational_expression_l1` | `ab1` | `(builder)` | `c7bff96c64c0aa9785092575c7f89ece51cd11d03c72c8f801c6b629d791a0ec` |
| `ce115_calc_exact_rational_expression_l1` | `ab2g` | `(builder)` | `5f397d56fab2649201b606af7abf51780a93d6d74269fd5f5d216a538aa8b8d9` |
| `ce115_calc_exact_rational_expression_l1` | `ab2d` | `(builder)` | `ccc56c41370e2b807299372da9b9af0d6807abf4dbae441990b16044d5108244` |
| `ce115_calc_exact_rational_expression_l1` | `ab2d_spec_v2` | `docs/experiments/prompts/ab2d_spec_v2/prompts/ce115_calc_exact_rational_expression_l1.txt` | `f46b8a30d79d77ca3811c9d7dc202a0b65b50302395ca871a24d3129a0f4e7c2` |

## 8. Corrected-chain Healer pins (record only)

- Runner: `38453d1294382f061efe149484f5a3059a47d085d2aeef358874a954e37adebf`
- Protocol: `bdb4121ee266f91bfa116019a334cf4a528da0d71629b96540a5f763826aff39`
- This preregistration does **not** execute Healer.

## 9. Governance

- No generation in this freeze.
- Resume later: skip only if complete artifact metadata matches plan + fingerprint.
- Mismatch: fail-closed; never overwrite.
- After this freeze, do not switch think/sampling/model digest/prompt SHAs mid-cohort.

- Runtime manifest: `docs/experiments/manifests/math16_pilot02_qwen9b_runtime_manifest.json`
- Cell plan: `docs/experiments/manifests/math16_pilot02_qwen9b_cell_plan.json`
