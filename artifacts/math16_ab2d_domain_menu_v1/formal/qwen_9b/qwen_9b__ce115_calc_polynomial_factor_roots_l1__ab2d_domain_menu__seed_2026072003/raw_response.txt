from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "quadratic_coefficients": [1, 4, -12]
    }
    
    # Factor the quadratic polynomial exactly. 
    # The API returns a list of two dicts with keys 'x_coefficient' and 'constant'.
    factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)
    
    # Extract roots from factorization: (ax + b)(cx + d) -> ax+b=0 => x=-b/a. 
    # The API returns dicts like {'x_coefficient': a, 'constant': b}. Root is -b/a.
    root_values = []
    for f in factors:
        a_val = int(f["x_coefficient"]) if isinstance(f["x_coefficient"], str) else float(f["x_coefficient"]) # Handle potential string fractions or ints
        b_val = int(f["constant"]) if isinstance(f["constant"], str) else float(f["constant"])
        
        # Calculate root: -b/a. Since inputs are exact, we compute the value. 
        # To ensure ascending order and handle Fraction types correctly for comparison/sorting later if needed,
        # but here coefficients are simple ints in this specific example [1, 4, -12].
        # Roots of x^2 + 4x - 12 = (x+6)(x-2). 
        # Factors returned will likely be {'x_coefficient': 1, 'constant': 6} and {'x_coefficient': 1, 'constant': -2}.
        # Root 1: -6/1 = -6. Root 2: -(-2)/1 = 2.
        
        root_val = -(b_val / a_val) if isinstance(b_val, str) else (-f["constant"] / f["x_coefficient"]) 
        # Note: The API returns 'p/q' as string or int. Division handles this safely in Python context for sorting logic usually implied by float conversion for ordering unless exact comparison needed.
        # However, to be safe with the "ascending" requirement and potential Fraction types from other tasks (though not here), 
        # we assume standard numeric evaluation is sufficient for 'roots_latex' generation if format_latex handles it or manual latex construction.
        # But wait: `format_latex` expects coefficients list. We need to reconstruct factors for factorization_latex and individual roots?
        # The contract asks for "factorization_latex" (the whole polynomial) and "roots_latex".
        
    # Reconstruct the original coefficient list from factors to use format_latex, or just pass frozen_params directly if it matches.
    # Frozen params are [1, 4, -12]. We can reuse this for factorization latex of the LHS.
    
    question_text = r"將一元二次方程式 $x^2+4x-12=0$ 的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。"
    
    # Generate factorization LaTeX for the LHS (the polynomial itself)
    factor_latex = PolynomialOps.format_latex(frozen_params["quadratic_coefficients"])
    
    # Calculate roots explicitly to sort them and format.
    # Roots are solutions to ax+b=0 => x = -b/a.
    r1_val = -(factors[0]["constant"] / factors[0]["x_coefficient"]) if isinstance(factors[0]["constant"], str) else (-int(factors[0]["constant"]) / int(factors[0]["x_coefficient"])) # Simplified for this specific case where inputs are ints
    r2_val = -(factors[1]["constant"] / factors[1]["x_coefficient"]) if isinstance(factors[1]["constant"], str) else (-int(factors[1]["constant"]) / int(factors[1]["x_coefficient"]))
    
    # Sort roots ascendingly
    sorted_roots_values = [min(r1_val, r2_val), max(r1_val, r2_val)]
    
    # Format roots LaTeX. Since they are rational numbers (integers in this case), we can format them directly or use a helper if available. 
    # No specific root formatter is listed in the menu except `format_latex` which takes coeffs.
    # We must construct the latex string for single values manually or assume standard formatting logic isn't provided via API for scalars.
    # However, looking at allowed ops: we can just format them as text if they are simple integers/floats? 
    # The prompt implies using Domain APIs only. There is no `format_latex_scalar`.
    # But wait, the example output contract usually expects a string. If roots are -6 and 2.
    # We need to generate LaTeX for "-6" and "2". Since we cannot call an API that doesn't exist, 
    # we must rely on standard Python f-strings or assume `format_latex` isn't the only way? 
    # Actually, usually in these tasks, if a scalar latex is needed, it's constructed manually for simple cases or via a specific helper not listed.
    # Given "Use only the Domain API methods listed", and none format scalars to LaTeX...
    # Perhaps we construct the string using f-strings with math symbols? 
    # Or maybe `format_latex` is meant for polynomials.
    # Let's assume manual construction for scalar roots if no API exists, as "arithmetic" ops are allowed natively.
    
    root1_str = str(sorted_roots_values[0])
    root2_str = str(sorted_roots_values[1])
    
    # If the values were fractions (e.g., 3/4), simple `str` might output '0.75' or 'Fraction(3, 4)'. 
    # The API returns strings for rational coefficients like "p/q". 
    # We need to ensure we format them nicely if they are not integers.
    def make_latex(val):
        s = str(val)
        if '/' in s:
            return f"${s}$"
        else:
            return f"${val}$"

    roots_latex = f"{make_latex(sorted_roots_values[0])}, {make_latex(sorted_roots_values[1])}"
    
    # Construct correct_answer dict exactly as per contract
    correct_answer = {
        "roots": sorted_roots_values, 
        "factorization_latex": factor_latex,
        "roots_latex": roots_latex
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }