# Math16 Pilot-02 Integer Runtime Preregistration

This document records the official preregistration and frozen configuration parameters for the **Pilot-02 Integer** experimental run.

---

## 1. Scope and Design Rationale
The primary goal of Pilot-02 is to run a controlled comparison between four prompt conditions on the Integer family tasks. To ensure maximum comparability with other Math16 Gemini experiments, this run uses the identical model, seeds, and generation parameters frozen from the baseline `MATH16-R05` multiseed protocol.

* **Target Tasks (4)**:
  1. `ce111_q03_prime_factor_selection`
  2. `ce112_q01_negative_integer_power`
  3. `ce112_q09_divisor_multiple_intersection`
  4. `ce111_nonchoice_q01_part1_exponential_growth`
* **Conditions (4)**:
  - `ab1` (Native / Bare)
  - `ab2g` (Generic Scaffold)
  - `ab2d` (API / domain_function_library exposed)
  - `ab2d_spec` (Compact Spec Scaffold + Guardrails; pre-frozen in commit `dae588d9`)

---

## 2. Frozen Runtime Configuration

* **Model Provider**: `google`
* **Model Tag**: `gemini-3.5-flash`
* **Runtime**: `google-generativeai` (Python SDK version `0.8.6`)
* **Sampling Parameters**:
  - `temperature`: `0.0` (nominal greedy decoding)
  - `max_output_tokens`: `24576` (large budget alignment to avoid premature truncation)
  - `top_p`: *not explicitly set* (rely on Gemini API defaults for temperature 0.0)
  - `top_k`: *not explicitly set*
  - `thinking_mode`: `not_applicable_gemini_transport` (non-reasoning model)
* **API Constraints**:
  - `timeout_seconds`: `600` seconds
  - `retry_policy`: Up to 3 attempts total. At most 2 transient failures (timeouts, rate limits, 5xx) are retried with exponential backoff (`[5, 20, 60]` seconds). Fatal failures (API key, authentication, client 400) stop execution immediately.

---

## 3. Seed List & Task Geometry
To allow cross-condition deterministic comparison, we freeze **5 seeds**:

```json
[2026071301, 2026072001, 2026072002, 2026072003, 2026072004]
```

* **Expected Cell Count**:
  $$\text{Expected Cells} = 4\text{ tasks} \times 4\text{ conditions} \times 5\text{ seeds} = 80\text{ cells}$$

---

## 4. Prompt Source & Hash Verification Registry
The prompt sources are defined to guarantee deterministic reproducibility:

1. **`ab1` / `ab2g` / `ab2d` (API)**:
   - Generated dynamically at runtime via `build_condition_prompt(condition, task, frozen)` in `agent_tools.finals_rebuild.ce115_clean_incremental_ablation`.
2. **`ab2d_spec`**:
   - Loaded from pre-frozen files under `docs/experiments/prompts/ab2d_spec/prompts/*.txt` (compiled at commit `dae588d9`).

### Prompt Hash Registry

| Task ID | Condition | Prompt SHA-256 | Length (chars) |
| :--- | :--- | :--- | :--- |
| **ce111_q03** | `ab1` | `398a9ab7067574286a3f7b6a955033b2f3af8d244d34098aa907623bb706bcc4` | 613 |
| | `ab2g` | `5436b011cb2be3d0edee52770f8c5a28348f9ef4763ae485b8c6a80798ef1cbf` | 970 |
| | `ab2d` | `8704669323fb45ef6bd34331151b350845425d2d14e19b36c58bd2c2c86bc75f` | 1443 |
| | `ab2d_spec` | `5417185bc8f5d084bd04d6bf4d346762f6fa4738c6a52d30ea34706f4121e6f0` | 2419 |
| **ce112_q01** | `ab1` | `d7f97e59388da3962bab6c3b0b55ebacdb7679340bf7955215431120c98301c9` | 598 |
| | `ab2g` | `cf486895c58fc5f91aaf2ba8cb03259f0eb98cb10d99a9d8a5734721bfdd7edb` | 955 |
| | `ab2d` | `a03c40a37de8c5652476da0fcd76dfc714ca55c19b0279b0452358c81ccde8d4` | 1419 |
| | `ab2d_spec` | `1aa4f2a789b546a5f81f4a773db6c783edb359f5fbbc3c21966853d57db6a61b` | 2342 |
| **ce112_q09** | `ab1` | `7eafd0610772ae6f3576a2d7d24017b28f0195d01e3b713feb8a6b629a79148e` | 648 |
| | `ab2g` | `8465217dde30310c3f927c2ec00e152e065f40c5508cd0339ae46a541c19496e` | 1005 |
| | `ab2d` | `f4d5abe47b1d3dad2095dbc473b4f58b6f1c8cd4f9ece0ba8a1de9f5c68ad5cb` | 1478 |
| | `ab2d_spec` | `6ab35b719b39c1336e47f8fea3d373ec2482ad3f8d1c6979b192576090228035` | 2414 |
| **ce111_nonchoice** | `ab1` | `105840296a8d546e9ca86a9aa27cf92df5da24004f78624f5fd96e031b114d62` | 690 |
| | `ab2g` | `93f82f61b6271d56cbaf1b7bf1276afc821b055cf767d2e9a496414ee933441e` | 1047 |
| | `ab2d` | `1f1491d3b68e9620550398001b27cd72e2f8b6c08c2debbf346396314a69cb42` | 1511 |
| | `ab2d_spec` | `5d8e3f4084038b1e99a581bf26ad77e49c295362a076ff374e5614960f38c019` | 2462 |

---

## 5. Persistence, Resume, and Overwrite Policies

* **Output Root**: `docs/experiments/results/math16_pilot02_integer_gemini`
* **Persistence Mechanism**: Standard per-cell directory layout. Every cell execution produces:
  - `prompt.txt`: exact prompt text sent to the API.
  - `raw_response.txt`: raw unaltered string returned by the API.
  - `extracted_candidate.py`: the python code snippet parsed from raw response (if any).
  - `artifact.json`: complete execution metadata including latency, API attempts list, and `"persisted_complete": true`.
* **Atomic Write**: Saves to a temporary file in the target directory and executes an atomic replacement `os.replace` to prevent corrupted records on premature process termination.
* **Resume Policy**: The runner queries `artifact.json`. If it exists, contains `"persisted_complete": true`, and its recorded `prompt_sha256` matches the cell plan, the cell is safely skipped without triggering any new API requests.
* **Overwrite Policy**: If the runner detects the output directory already exists and contains incompatible plans, it will abort. Under no circumstances will completed, valid cells be overwritten.

---

## 6. Prompt Freeze Supersession Lineage

```text
Initial prompt freeze:
e9a716eb

Zero-model audit:
Segment 2A found IntegerOps literals.
No Pilot-02 model call or result inspection occurred.

Authoritative final prompt freeze:
dae588d9

Runtime preregistration:
1ee8573c
```

`e9a716eb` is superseded.
`dae588d9` is the only authoritative Pilot-02 Ab2d+spec prompt freeze.
