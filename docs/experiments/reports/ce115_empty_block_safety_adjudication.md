# 🔎 empty-block Structural Candidates Safety Adjudication Report

This document records the safety adjudication and forensic analysis of the 5 empty-block structural candidates. For each candidate, we present 20 lines of code context before and after the empty block, detail parent/child relationships, evaluate the risk of pass-insertion, and classify the candidate.

---

## 1. Executive Summary

Following a forensic audit of the raw outputs for the 5 empty-block candidates:
*   **Total Candidates Audited**: 5
*   **Reclassified Unsafe**: 5
*   **Verified Safe Candidates**: 0
*   **Verdict**: All 5 candidates represent missing core mathematical statements, loop index progression bugs, or truncated code. **No candidate is safe for deterministic pass-insertion.** Inserting a pass would compile the script but hide serious logical defects.

---

## 2. Cell-by-Cell Forensic Adjudication

### 2.1 Candidate 1: `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071301`
*   **Task**: `ce115_calc_radical_simplification_l1`
*   **Parent Function**: `get_square_free(n)` (nested inside `simplify_sqrt` inside `generate()`)
*   **Helper Call Site**: `get_square_free` is defined but never called inside the script.
*   **Classification**: `CORE_LOGIC_MISSING`
*   **Safe for pass-insertion**: **FALSE**

#### Code Context (around empty block)
```python
        # Re-calculate properly to ensure correctness for any input
        def get_square_free(n):
            i = 2
            while i * i <= n:
                count = 0
                temp_n = n
                while temp_n % (i*i) == 0:
                    count += 1
                    temp_n //= (i*i)
                
                if count >= 2: # Actually we just divide by the square part directly in one go per prime factor logic below is simpler
                
            return remaining_radicand, total_factor
```

#### Detailed Parent Function `simplify_sqrt`
```python
    def simplify_sqrt(n):
        if n <= 0:
            return 1, n
        
        temp_n = n
        k = int(math.sqrt(temp_n))
        
        while True:
            root_of_k_squared = k * k
            remaining_part = temp_n // (k * k)
            
            # Check for perfect square factorization logic more robustly by removing all squared factors from the start
            if math.isqrt(remaining_part)**2 == remaining_part and remaining_part > 1:
                break
            
            # Better approach: find largest integer m such that m^2 divides n, then return (m, n // m^2)
            pass
```

#### Adjudication Analysis
1.  **Missing Math Semantics**: The `if count >= 2:` block was intended to perform division of the radicand by square factors to simplify the root. Leaving it empty results in no simplification logic inside the helper.
2.  **Loop Progress Dependency**: The outer loop `while i * i <= n:` contains no increment logic for loop variable `i` (missing `i += 1`). Consequently, if this helper were ever executed, it would run in an **infinite loop**. Inserting `pass` would conceal this critical loop index bug.

---

### 2.2 Candidate 2: `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071302`
*   **Task**: `ce115_calc_radical_simplification_l1`
*   **Parent Function**: `get_prime_factorization_sqrt_v2(n)` (nested inside `generate()`)
*   **Helper Call Site**: Sibling helper `get_prime_factorization_sqrt_v2` is defined but never called.
*   **Classification**: `CORE_LOGIC_MISSING`
*   **Safe for pass-insertion**: **FALSE**

#### Code Context (around empty block)
```python
    def get_prime_factorization_sqrt_v2(n):
        if n <= 0: return 1, 1
        
        temp = n
        coeff = 1
        while True:
            i = int(math.sqrt(temp)) + 1
            
            # Check for square factors starting from the largest possible down to small ones? 
            # Or just iterate up. Since we want the LARGEST square factor, maybe check downwards or use prime factorization logic directly.
            
            found_sq = False
            j = int(math.sqrt(temp)) + 1
            
            while True:
                sq_val = j * j
                
                if temp % sq_val == 0 and is_square_free(temp // sq_val):
                    # Found a square that leaves the rest square-free? 
                    # Wait, this logic might miss cases where multiple squares exist.
                    # Example n=72 -> sqrt(72) = 6 * sqrt(2). 
                    # j starts at int(sqrt(72))+1 = 9. 81 > 72. Loop doesn't run?
                    
                if sq_val <= temp:
                     pass
```

#### Adjudication Analysis
1.  **Missing Math Semantics**: The `if temp % sq_val == 0...` block is empty, which completely omits the assignment or return statements needed for square factor reduction.
2.  **Loop Progress Dependency**: Inside `while True:`, index `j` is defined but never decremented or incremented. This loop is an **infinite loop** by design. Inserting `pass` masks this severe logical error.

---

### 2.3 Candidate 3: `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab1__seed_2026071303`
*   **Task**: `ce115_calc_radical_simplification_l1`
*   **Parent Function**: `get_prime_factors(n)` (nested inside `robust_simplify` inside `generate()`)
*   **Helper Call Site**: Sibling helpers `robust_simplify` and `get_prime_factors` are defined but never called.
*   **Classification**: `CORE_LOGIC_MISSING`
*   **Safe for pass-insertion**: **FALSE**

#### Code Context (around empty block)
```python
        # Let's just do standard prime factorization
        def get_prime_factors(n):
            factors = {}
            d = 2
            temp = n
            while d * d <= temp:
                if temp % d == 0:
                    count = 0
                    while temp % d == 0:
                        count += 1
                        temp //= d
                    factors[d] = count
                d += 1
            if temp > 1: # Wait, need to update logic here
            
        def get_prime_factors_v2(n):
```

#### Adjudication Analysis
1.  **Missing Math Semantics**: The empty block `if temp_n > 1:` (and `if t > 1:` in `get_prime_factors_v2`) is a remainder handler for prime factorization. Skipping it fails to record the remaining prime factor in the `factors` dictionary, leading to mathematical errors.
2.  **Truncation Evidence**: The file ends abruptly with `rem_final = n` at line 251. There is no return dictionary constructed for `generate()`, meaning the script is structurally incomplete.

---

### 2.4 Candidate 4: `qwen3_5_4b__ce115_calc_radical_simplification_l1__ab2g__seed_2026071301`
*   **Task**: `ce115_calc_radical_simplification_l1`
*   **Parent Function**: `generate()` (first defined block, containing the empty block)
*   **Helper Call Site**: This is inside the main generator body.
*   **Classification**: `TRUNCATED_BLOCK`
*   **Safe for pass-insertion**: **FALSE**

#### Code Context (around empty block)
```python
                    j = i + 1
                    while j * j <= final_val and not found_factor:
                         if final_val % (j ** 2) == 0:
                             # This logic is getting messy. Let's restart the extraction cleanly inside the function body directly.
                             
                pass
```

#### Adjudication Analysis
1.  **Missing Math Semantics**: The model abandoned this block due to complexity ("This logic is getting messy...").
2.  **Truncation Evidence**: The file contains multiple attempts to redefine `generate()` and ends abruptly on line 269 with `def generate(level=1,` without any parameters or block body. Even if the empty block on line 98 is patched, the file remains completely unparseable due to this trailing truncation.

---

### 2.5 Candidate 5: `qwen3_5_9b__ce115_calc_polynomial_factor_roots_l1__ab2g__seed_2026071301`
*   **Task**: `ce115_calc_polynomial_factor_roots_l1`
*   **Parent Function**: `generate()` (core function)
*   **Helper Call Site**: Core execution flow.
*   **Classification**: `CORE_LOGIC_MISSING`
*   **Safe for pass-insertion**: **FALSE**

#### Code Context (around empty block)
```python
    a = quadratic_coefficients["a"]
    b = quadratic_coefficients["b"]
    c = quadratic_coefficients["c"]

    # Calculate discriminant using integer arithmetic to avoid float issues
    delta = (b * b) - (4 * a * c)
    
    if delta < 0:
        raise ValueError("No real roots for this polynomial.")
        
    sqrt_delta_int = int(delta ** 0.5)
    if sqrt_delta_int * sqrt_delta_int != delta:
        # If not a perfect square, we need to handle the irrational root case or assume it's reducible in rationals? 
        # The task says "exact roots" and allows fractions p/q but implies rational coefficients usually lead to rational/irrational.
        # However, standard factorization tasks often imply finding real roots. If delta is not a perfect square, we can't express as simple fraction unless the problem expects surds (not in schema). 
        # Let's assume for this specific task contract that inputs will yield integer or fractional roots based on "irreducible p/q".
        # But wait: if discriminant isn't a perfect square, roots are irrational. The schema only allows int | str ("p/q").
        # This implies the test cases provided (like frozen params) MUST have perfect square discriminants for this specific output format to work without surds.
        
    sqrt_delta = delta ** 0.5
```

#### Adjudication Analysis
1.  **Missing Math Semantics**: The empty block `if sqrt_delta_int * sqrt_delta_int != delta:` was meant to check for non-perfect square discriminants (which yield irrational roots incompatible with the string/fraction schema).
2.  **Pass Insertion Risk**: Inserting `pass` lets the engine proceed to evaluate irrational roots as floats, leading to downstream formatting crashes in `simplify_fraction` (raising type or value errors). It represents an unhandled math contract gap.

---

## 3. Distinguishing Trailing Residue vs Truncated Trailer

To govern future cleanup rules, we establish a strict boundary between trailing residue (removable) and truncated code (unremovable):

*   **TRAILING_RESIDUE**: Conversational text, trailing markdown block closing symbols, or literal explanations appended *after* a syntactically complete Python module.
*   **TRUNCATED_TRAILER**: A cutoff at the end of the file occurring mid-statement, mid-expression, or mid-block (e.g. trailing comma, unclosed parenthesis, dangling `=`, or unfinished `def generate`).

### Negative Fixtures for `R02_trailing_artifact_removal`
The following truncated structures must **never** be cleaned or completed by the healer, and must instead be rejected as compile errors:
1.  **Incomplete assignment**: `x =`
2.  **Incomplete function call**: `math.gcd(a,`
3.  **Unclosed string or brackets**: `{'answer':`
4.  **Dangling operators**: `a + b +`
5.  **Dangling comma or colon**: `def generate(level=1,`
6.  **Empty Core block**: An empty `if` or `while` block in the core generator flow that lacks any subsequent execution block.
