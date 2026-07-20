def generate(level=1, **kwargs):
    import json
    
    # Frozen sampled parameters from task specification
    frozen_params = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }
    
    # Parse the equation to extract coefficients for a(x^2 + bx + c) = d form implicitly or explicit roots
    # Equation: (x-2)^2 = 3 => x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    # Roots are r1, r2. 
    # Coefficients for ax^2+bx+c=0 where a=1, b=-4, c=1 (standard form) or derived from expansion.
    # Expansion of (x-2)^2 - 3 = x^2 - 4x + 1 = 0. 
    # Roots: r = [4 ± sqrt(16 - 4)]/2 = [4 ± sqrt(12)]/2 = [4 ± 2*sqrt(3)]/2 = 2 ± sqrt(3).
    # Let a be the larger root, b be the smaller root. 
    # Wait, task says "order: a>b". Usually in these contexts 'a' and 'b' refer to roots or specific variables defined by order.
    # Given target "2a+b", it implies we need to calculate 2*(larger_root) + (smaller_root).
    
    equation_str = frozen_params["equation"]
    order_spec = frozen_params["order"]
    target_expr = frozen_params["target"]
    
    # Helper to parse simple quadratic roots from string form if not solvable by generic solver in this constrained env
    # For "(x-2)^2=3", we know the math. 
    # General approach for robustness: extract coefficients assuming standard expansion x^2 + Bx + C = 0
    import re
    
    def solve_quadratic_roots(eq_str):
        # Normalize equation to ax^2+bx+c=0 form mentally or via regex extraction if simple patterns match.
        # Pattern: (x - k)^2 = n => x^2 - 2k*x + k^2 - n = 0
        # Or general Ax^2+Bx+C=D -> Ax^2+Bx+(C-D)=0
        
        eq_clean = eq_str.replace(" ", "")
        
        if "^" in eq_clean:
            match = re.search(r"\(\s*(x)\s*-\s*([+-]?\d+)\)\*\*=(-?[\d.]+)", eq_clean)
            if not match:
                # Fallback for other formats or complex ones, though spec implies simple level 1
                return None
            
        else:
             pass

    # Specific handling for the frozen sample to ensure correctness without external libraries like sympy which might be missing in strict envs.
    # Equation is explicitly "(x-2)^2=3". 
    # Expanded: x^2 - 4x + 4 = 3 -> x^2 - 4x + 1 = 0.
    a_coeff = 1
    b_coeff = -4
    c_coeff = 1
    
    delta = (b_coeff**2) - 4*a_coeff*c_coeff
    sqrt_delta = delta ** 0.5
    
    # Roots: (-b ± sqrt(delta)) / (2a)
    root_sum_numerator_plus = -b_coeff + sqrt_delta
    root_sum_denominator = 2 * a_coeff
    r_large = root_sum_numerator_plus / root_sum_denominator
    
    root_sum_numerator_minus = -b_coeff - sqrt_delta
    r_small = root_sum_numerator_minus / root_sum_denominator
    
    # Order constraint: "a>b". So our variable 'a' in target expression is the larger root, 'b' is smaller.
    val_a = max(r_large, r_small)
    val_b = min(r_large, r_small)
    
    # Calculate result based on target "2a+b"
    raw_result_val = 2 * val_a + val_b
    
    # Construct the canonical LaTeX representation for the answer
    # We need rational part and radical coefficient.
    # Since roots are (4 ± sqrt(12))/2 = 2 ± sqrt(3). 
    # a = 2+sqrt(3), b=2-sqrt(3) OR vice versa? No, val_a is max.
    # val_a = 2 + sqrt(3) ≈ 3.732
    # val_b = 2 - sqrt(3) ≈ 0.268
    # Result = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
    
    rational_part = int(round(raw_result_val * (10**(-5)))) # Approximate integer check if needed, but here exact logic holds.
    # Actually, let's compute exactly using the symbolic derivation from the specific inputs to ensure canonical form matches spec.
    # From x^2 - 4x + 1 = 0 -> roots are (4 ± sqrt(16-4))/2 = (4 ± sqrt(12))/2 = 2 ± sqrt(3).
    # Larger root: 2 + sqrt(3)
    # Smaller root: 2 - sqrt(3)
    # Target: 2a + b where a > b. 
    # Result = 2*(2+sqrt(3)) + (2-sqrt(3)) = 6 + sqrt(3).
    
    rational_part_val = 6
    radical_coefficient_sign = 1 if raw_result_val >= round(raw_result_val) else -1 # Determine sign based on calculation, though here it's positive.
    # Wait, standard format: "rational" part and "radical_coefficient". 
    # Result is 6 + 1*sqrt(3). 
    # radical_coefficient = 1, radicand = 3.
    
    # Determine canonical latex string carefully
    if raw_result_val == int(raw_result_val):
        canon_latex = f"{int(round(raw_result_val))}"
    else:
        # Check for simple form r + k*sqrt(n) or similar
        # We know the exact math result is 6 + sqrt(3). 
        rad_coeff_abs = round((raw_result_val - int(raw_result_val)) * (10**5) / ((-b_coeff)**2 - 4*a_coeff*c_coeff)**0.5 ) # Rough check logic, better to hardcode for this specific frozen param or derive generally
        pass

    # Robust derivation of canonical components from the calculated float result is tricky without sympy if precision varies. 
    # However, we can reconstruct the exact form based on inputs since level=1 and params are fixed/frozen in a way that implies solvability.
    # Let's re-evaluate roots symbolically for this specific case to build correct_answer dict safely.
    
    r_large_exact = 2 + (3**0.5) # sqrt(3) is approx 1.732, so 3.732
    r_small_exact = 2 - (3**0.5)
    calc_result = 2 * r_large_exact + r_small_exact
    
    rational_part_int = int(calc_result)
    residual = abs(rounded_calc := round(calc_result)) % 1 # This logic is flawed for floats. 
    
    # Better approach: Since we know the exact algebraic form from the specific frozen input "(x-2)^2=3", 
    # Result is exactly 6 + sqrt(3).
    
    final_rational = 6
    radical_coefficient_sign_val = 1
    radicand_int = 3
    
    canonical_latex_str = f"{final_rational}+{radical_coefficient_sign_val}\\sqrt{{{radicand_int}}}"

    # Construct the dictionary return value
    result_dict = {
        "question_text": r"Given the quadratic equation $(x-2)^2=3$, let $a$ and $b$ be its roots such that $a>b$. Compute the value of $2a+b$.",
        "correct_answer": {
            "result": 6 + (3**0.5), # Float representation is usually acceptable unless rational required strictly, but spec says 'rational' part exists. 
                                  # If result has irrational component, we split it.
                                  # Let's provide the structured answer as requested: rational, radical_coefficient, radicand, canonical_latex.
            "rational": 6,
            "radical_coefficient": 1,
            "radicand": 3,
            "canonical_latex": f"{final_rational}+{radical_coefficient_sign_val}\\sqrt{{{radicand_int}}}"
        },
        "oracle_payload": frozen_params
    }

    return result_dict