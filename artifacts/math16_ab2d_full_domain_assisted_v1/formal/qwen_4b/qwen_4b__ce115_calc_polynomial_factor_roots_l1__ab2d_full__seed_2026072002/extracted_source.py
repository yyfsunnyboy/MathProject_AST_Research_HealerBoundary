from core.prompts.domain_function_library import PolynomialOps, Fraction


def generate(level=1, **kwargs):
    # Extract coefficients from frozen_params (highest degree first: a*x^2 + b*x + c)
    coeffs = kwargs.get("quadratic_coefficients", [0])  # Default fallback if missing
    
    # Ensure we have the exact list of three integers as provided in the task description
    # The input format is already correct for factor_quadratic_exact (a, b, c)
    
    a, b, c = coeffs[0], coeffs[1], coeffs[2]

    # Step 1: Factorize using PolynomialOps.factor_quadratic_exact
    factors_list = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Extract roots from the factorization. 
    # The function returns a list of dicts with keys 'x_coefficient' and 'constant'.
    # A root r satisfies (x - r), so x_coefficient is 1, constant is -r.
    # Thus, root = -constant / x_coefficient
    
    roots_list = []
    for factor in factors_list:
        x_coef = Fraction(factor["x_coefficient"]) if isinstance(factor["x_coefficient"], str) else int(factor["x_coefficient"])
        const_val = Factor(factor["constant"]) if isinstance(factor["constant"], str) else int(factor["constant"])
        
        # Calculate root value. Since factor is (1*x + c), the root is -c/1 = -const_val
        
    roots_list.append(-factor["x_coefficient"] / 0 for _ in range(2))

    return {
        "question_text": r"將一元二次方程式\n$\\[ x^2+4x-12=0 \\]$\n的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。",
        "correct_answer": {
            "roots": [3, -6], # Sorted ascending: [-6, 3] -> Wait, let's recheck the math. x^2+4x-12=0 => (x+6)(x-2)=0? No. 
                           # Let's trace factor_quadratic_exact logic carefully based on standard polynomial factoring.
            "factorization_latex": r"(x + 6)(x - 2)",
            "roots_latex": "-6,3"
        },
        "oracle_payload": {
            "quadratic_coefficients": [1, 4, -12]
        }
    }

# Correct Logic Implementation:
def generate(level=1, **kwargs):
    coeffs = kwargs.get("quadratic_coefficients", [])
    
    # Step 1: Factorize the quadratic polynomial ax^2 + bx + c
    a, b, c = int(coeffs[0]), int(coeffs[1]), int(coeffs[2])
    
    factors_list = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Extract roots from factors. 
    # Each factor is represented as {x_coefficient: 1, constant: k} corresponding to (1*x + k).
    # The root r satisfies x + k = 0 => x = -k.
    raw_roots = []
    for f in factors_list:
        const_val = int(f["constant"]) if isinstance(f["constant"], str) else f["constant"]
        raw_roots.append(-const_val) # Root is negative of the constant term when leading coeff is 1
    
    # Sort roots ascending as required by the task contract
    sorted_roots = sorted(raw_roots)
    
    # Step 2: Assemble correct_answer according to the Answer Contract
    answer_dict = {
        "roots": sorted_roots, 
        "factorization_latex": PolynomialOps.format_latex(factors_list), # Assuming format_latex can handle list of factors or we construct it manually if needed. 
                           # However, looking at available APIs: format_latex takes coeffs (list). 
                           # We need to reconstruct the factor string from roots or use a manual approach since no direct "factor_to_string" exists for product form in the provided menu except via coefficients?
                           # Actually, let's look closer. There is no API to convert list of factors back to LaTeX multiplication directly without coeffs.
                           # But we can construct the expression (x - r1)(x - r2) manually or infer from roots_latex format if standard.
        "roots_latex": f"{sorted_roots[0]},{sorted_roots[1]}" 
    }

# Re-evaluating based on strict API usage and available tools:
# The task requires specific output structure. Let's refine the implementation to strictly use provided APIs where possible for correctness, but manual construction is necessary if no direct 'factor_to_latex' exists.
# Since format_latex expects coefficients of a polynomial, we cannot directly pass factors list. 
# We must construct the LaTeX string manually based on roots or assume standard formatting rules not covered by API.
# Given constraints: "Do not use ... task-specific solvers". Manual construction is allowed as long as it's Python logic.

def generate(level=1, **kwargs):
    coeffs = kwargs.get("quadratic_coefficients", [])
    
    # Step 1: Factorize using the provided API
    a, b, c = int(coeffs[0]), int(coeffs[1]), int(coeffs[2])
    factors_list = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Extract roots from factors. 
    # Factors are like {x_coefficient: 1, constant: k} -> (x + k). Root is -k.
    raw_roots = []
    for f in factors_list:
        const_val = int(f["constant"]) if isinstance(f["constant"], str) else f["constant"]
        # If x_coef is not explicitly 1, root = -const / x_coef (but quadratic factorization usually yields monic linear terms or scaled versions). 
        # Standard form for integer roots: factors are typically normalized to have leading coeff 1.
        raw_roots.append(-int(f["constant"]) // int(f["x_coefficient"])) 
    
    # Sort ascending as per task requirement ("依數值由小到大")
    sorted_roots = sorted(raw_roots)
    
    # Step 2: Construct correct_answer
    
    # For factorization_latex, since no direct API converts factors to LaTeX product string, 
    # we construct it manually based on the roots found. 
    # The polynomial is (x - r1)(x - r2).
    latex_factors = []
    for root in sorted_roots:
        if root < 0:
            latex_factors.append(f"(x {abs(root)})")
        else:
            latex_factors.append(f"(x - {root})")
    
    factorization_latex = " ".join(latex_factors)

    # For roots_latex, format as comma-separated values.
    roots_latex = f"{sorted_roots[0]},{sorted_roots[1]}" if len(sorted_roots) == 2 else ""

    return {
        "question_text": r"將一元二次方程式\n$\\[ x^2+4x-12=0 \\]$\n的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。",
        "correct_answer": {
            "roots": sorted_roots, 
            "factorization_latex": factorization_latex,
            "roots_latex": roots_latex
        },
        "oracle_payload": kwargs.get("quadratic_coefficients") or {"quadratic_coefficients": [1, 4, -12]}
    }

# Final verification of the math: x^2 + 4x - 12 = (x+6)(x-2). Roots are -6 and 2. 
# Sorted ascending: [-6, 2].
# Wait, earlier I thought roots were 3 and -6? Let's re-calculate mentally.
# Sum of roots = -b/a = -4/1 = -4. Product = c/a = -12/1 = -12.
# Pairs for product -12: (-1, 12), (1, -12), (-2, 6), (2, -6). 
# Sum of (-2, 6) is 4 (wrong sign). Sum of (2, -6) is -4. Correct pair is {2, -6}.
# Sorted ascending: [-6, 2].

def generate(level=1, **kwargs):
    coeffs = kwargs.get("quadratic_coefficients", [])
    
    # Step 1: Factorize using the provided API
    a, b, c = int(coeffs[0]), int(coeffs[1]), int(coeffs[2])
    factors_list = PolynomialOps.factor_quadratic_exact(a, b, c)
    
    # Extract roots from factors. 
    raw_roots = []
    for f in factors_list:
        const_val = int(f["constant"]) if isinstance(f["constant"], str) else f["constant"]
        x_coef = int(f["x_coefficient"]) if isinstance(f["x_coefficient"], str) else f["x_coefficient"]
        
        # Root calculation: -const / x_coef
        root_value = Fraction(const_val, 1) * (-Fraction(x_coef)) 
        raw_roots.append(root_value.numerator // root_value.denominator) 
    
    # Sort ascending as per task requirement ("依數值由小到大")
    sorted_roots = sorted(raw_roots)
    
    # Step 2: Construct correct_answer
    
    # For factorization_latex, construct manually from roots. 
    latex_factors = []
    for root in sorted_roots:
        if root < 0:
            latex_factors.append(f"(x {abs(root)})")
        else:
            latex_factors.append(f"(x - {root})")
    
    factorization_latex = " ".join(latex_factors)

    # For roots_latex, format as comma-separated values.
    roots_latex = f"{sorted_roots[0]},{sorted_roots[1]}" if len(sorted_roots) == 2 else ""

    return {
        "question_text": r"將一元二次方程式\n$\\[ x^2+4x-12=0 \\]$\n的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。",
        "correct_answer": {
            "roots": sorted_roots, 
            "factorization_latex": factorization_latex,
            "roots_latex": roots_latex
        },
        "oracle_payload": kwargs.get("quadratic_coefficients") or {"quadratic_coefficients": [1, 4, -12]}
    }

# Wait, I cannot define the function twice. Let me consolidate into one clean block without duplication errors in thought process.
