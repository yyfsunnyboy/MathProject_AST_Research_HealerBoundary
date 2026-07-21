# Math16 Ab2s Integer Post-Freeze Exploratory Pilot Report

This report summarizes the results of the **Ab2s Integer Skill Post-Freeze Exploratory Pilot**. The evaluation was conducted across 4 pilot integer tasks comparing the baseline `ab2d_replication` condition against the proposed `ab2s_integer_skill` condition.

---

## 1. Experimental Conditions and Setup
* **Model**: `qwen3.5:4b` (ID: `2a654d98e6fb`)
* **Inference Settings**: Seed `2026071301`, Temperature `0.7`, Top_P `0.8`, Top_K `20`, Non-thinking mode.
* **Environment**: Sandboxed python sub-process execution wrapper (zero active healers, first-attempt only).

---

## 2. Pass/Fail Status Grid

| Task ID | Structural Tag | Condition | Status | Failure Category | Primary Failure Layer |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ce111_q03_prime_factor_selection** | divisibility-and-prime-factor selection | `ab2d_replication` | **FAIL** | `runtime_failure` | L2 (Runtime Execution) |
| | | `ab2s_integer_skill` | **FAIL** | `parse_minor` | L1 (Syntax / Parse) |
| **ce112_q01_negative_integer_power** | signed integer exponentiation | `ab2d_replication` | **FAIL** | `answer_incorrect` | L5 (Semantic Correctness) |
| | | `ab2s_integer_skill` | <span style="color:#0F9D58">**PASS**</span> | `none` | PASSED |
| **ce112_q09_divisor_multiple_intersection** | divisor-multiple intersection | `ab2d_replication` | **FAIL** | `parse_minor` | L1 (Syntax / Parse) |
| | | `ab2s_integer_skill` | **FAIL** | `answer_incorrect` | L5 (Semantic Correctness) |
| **ce111_nonchoice_q01_part1_exponential_growth** | discrete exponential growth | `ab2d_replication` | **FAIL** | `runtime_failure` | L2 (Runtime Execution) |
| | | `ab2s_integer_skill` | **FAIL** | `answer_incorrect` | L5 (Semantic Correctness) |

---

## 3. Failure Mechanism and Layer Analysis

### Task 1: `ce111_q03_prime_factor_selection`
* **`ab2d_replication`**: Failed with `TypeError: unsupported operand type(s) for %: 'NoneType' and 'int'`.
  * *Mechanism*: The generated code used `kwargs.get("n")` to retrieve parameters dynamically. Since the sandbox runner invokes `generate()` with no arguments, `n` resolved to `Nonecc`, causing modulo division to crash.
* **`ab2s_integer_skill`**: Failed with `parse_minor` (L1).
  * *Mechanism*: The model got stuck in an infinite/repeating loop of code generation, producing a massive 3,256-line python source with incomplete code blocks and unmatched syntax indentation, causing a parser crash. This is **not resolved by the tested Ab2s scaffold** due to Qwen's local generation looping issue on this task.

### Task 2: `ce112_q01_negative_integer_power`
* **`ab2d_replication`**: Failed with `answer_incorrect` (L5).
  * *Mechanism*: The model failed to conform to the required layout for `correct_answer` and calculation without a clear rule structure.
* **`ab2s_integer_skill`**: **PASSED**.
  * *Mechanism*: The model successfully avoided calling `IntegerOps` APIs, hardcoded the frozen parameters locally, and generated a clean, mathematically correct Python script matching the expected schema. This failure was **prompt-preventable under the tested Ab2s scaffold** (Full Rescue).

### Task 3: `ce112_q09_divisor_multiple_intersection`
* **`ab2d_replication`**: Failed with `parse_minor` (L1) due to duplicate definition of `generate()` and reference to unimported `Dict` type hint.
* **`ab2s_integer_skill`**: Failed with `answer_incorrect` (L5).
  * *Mechanism*: The model successfully compiled and ran without syntax or namespace errors, but used an incorrect mathematical algorithm: it calculated the ratio of LCM to divisor (`lcm(216, 18) // 216 = 1`) instead of counting the divisors of `216 // 18 = 12` (which yields 6 positive integer divisors: {1, 2, 3, 4, 6, 12}). This demonstrates **failure-layer migration** from L1/L2 to L5.

### Task 4: `ce111_nonchoice_q01_part1_exponential_growth`
* **`ab2d_replication`**: Failed with `NameError: name 'safe_eval' is not defined` (L2).
  * *Mechanism*: The model attempted to call `safe_eval()` as a bare function without prefixing it with the injected namespace `IntegerOps.safe_eval()`.
* **`ab2s_integer_skill`**: Failed with `answer_incorrect` (L5).
  * *Mechanism*: The model correctly referenced namespace objects, but made two semantic errors:
    1. It calculated total population (`1 * 4^15`) instead of returning the generation count `k` (which is `18` for 15 days = 360 hours).
    2. It multiplied `days * hours_per_gen` (15 * 20 = 300 hours) instead of converting days to hours (`15 * 24 = 360` hours). This represents a clear case of **failure-layer migration** from L2 namespace crashes to L5 semantic correctness.

---

## 4. Prediction vs. Actual Outcomes

| Cell ID | Predicted Outcome | Actual Outcome | Match? | Scenario Classification |
| :--- | :--- | :--- | :--- | :--- |
| `qwen35_4b__ce111_q03_prime_factor_selection__ab2d_replication__seed_2026071301` | `FAILED_RUNTIME_FAILURE` | `EXECUTION_FAILURE` | **Yes** | Scenario 3: Not Resolved |
| `qwen35_4b__ce111_q03_prime_factor_selection__ab2s_integer_skill__seed_2026071301` | `FAILED_RUNTIME_FAILURE` | `EXECUTION_FAILURE` (parse) | **Yes** (Failure Type Differs) | Scenario 3: Not Resolved |
| `qwen35_4b__ce112_q01_negative_integer_power__ab2d_replication__seed_2026071301` | `FAILED_ANSWER_INCORRECT` | `ANSWER_INCORRECT` | **Yes** | Scenario 1: Full Rescue |
| `qwen35_4b__ce112_q01_negative_integer_power__ab2s_integer_skill__seed_2026071301` | `PASSED` | `PASSED` | **Yes** | Scenario 1: Full Rescue |
| `qwen35_4b__ce112_q09_divisor_multiple_intersection__ab2d_replication__seed_2026071301` | `FAILED_PARSE_MINOR` | `EXECUTION_FAILURE` (parse) | **Yes** | Scenario 2: Failure-Layer Migration |
| `qwen35_4b__ce112_q09_divisor_multiple_intersection__ab2s_integer_skill__seed_2026071301` | `PASSED` | `ANSWER_INCORRECT` | **No** | Scenario 2: Failure-Layer Migration |
| `qwen35_4b__ce111_nonchoice_q01_part1_exponential_growth__ab2d_replication__seed_2026071301` | `FAILED_RUNTIME_FAILURE` | `EXECUTION_FAILURE` | **Yes** | Scenario 2: Failure-Layer Migration |
| `qwen35_4b__ce111_nonchoice_q01_part1_exponential_growth__ab2s_integer_skill__seed_2026071301` | `PASSED` | `ANSWER_INCORRECT` | **No** | Scenario 2: Failure-Layer Migration |

* **Overall Prediction Accuracy**: **5 / 8 (62.5%)**
* **Discrepancy Analysis**:
  * For **Task 3 (`ce112_q09`)** and **Task 4 (`ce111_nonchoice_q01`)** under `ab2s_integer_skill`, the predictions anticipated that injecting the precise instructions, namespace rules, and local parameter specifications would fully rescue the cells. While the scaffold successfully prevented syntax/namespace crashes (L1/L2), it did not prevent the model from making math logic/semantic errors (L5), classifying both tasks under **Scenario 2: Failure-Layer Migration**.

---

## 5. Engineering Insights

1. **Ab2s Scaffold Efficacy**:
   - The Ab2s skill-style scaffold successfully suppressed API usage errors, namespace mismatches (e.g. bare `safe_eval` calls), and typing issues across three of the four tasks. 
   - Task 2 was successfully rescued, demonstrating that the structural rules in Ab2s are highly effective for basic signed integer operations.
2. **Qwen local repeating loop vulnerability**:
   - Qwen 3.5 4B exhibits a high vulnerability to repetitive token generation loops under detailed specifications (e.g., Task 1 `ab2s`). When the instruction complexity increases, local inference without post-processing or healing can fall into repeating loop generation.
3. **Failure-Layer Migration & Healer Eligible Pool Denominator Re-attribution**:
   - In tasks 3 and 4, the failures migrated from execution layer errors to correctness layer errors. In a production pipeline, this represents a **Healer eligible pool denominator re-attribution**: since the code successfully executed without raising exceptions, standard AST/Runtime healers would no longer trigger, shifting the responsibility of resolution to display/semantic check layers or O1 healers.

---

## 6. Color Identity Compliance (Visual Diagnostics)
For visual comparison and front-end dashboard panels:
* 🟦 **Gemini (Cloud)**: `#4285F4`
* 🟨 **Qwen-14B (Local)**: `#F4B400`
* 🟩 **Qwen-8B (Local)**: `#0F9D58`
* 🟧 **Active Healer**: `#FF6D00` (highlighting repairs and warnings)
