from core.prompts.domain_function_library import PolynomialOps, Fraction


def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_params", {})
    
    # Extract coefficients from oracle_payload (highest degree first: a, b, c)
    coeffs = frozen_params["quadratic_coefficients"]
    if not isinstance(coeffs[0], Fraction):
        coeffs = [Fraction(c) for c in coeffs]

    # Step 1: Factor the quadratic exactly to get root factors
    factor_result = PolynomialOps.factor_quadratic_exact(
        a=coeffs[0], b=coeffs[1], c=coeffs[2]
    )
    
    # The result is [dict, dict]. Each dict has keys 'x_coefficient' and 'constant'.
    # For ax^2 + bx + c = (px - r)(qx - s), the roots are r/p and s/q.
    factor_list = factor_result
    
    if len(factor_list) != 2:
        raise ValueError("Expected exactly two factors.")

    f1, f2 = factor_list[0], factor_list[1]
    
    # Calculate roots from (px - root_val). The constant term is the negative of the product.
    # If we have a factor like [p, q_const], it represents p*x + q_const. 
    # Root x = -q_const / p.
    
    def get_root_from_factor(f):
        coeff_x = f["x_coefficient"]
        const_term = f["constant"]
        
        if isinstance(coeff_x, str) or (isinstance(const_term, Fraction)):
            # Handle mixed types by converting to Fractions for precision
            c1 = Fraction(coeff_x) if not isinstance(coeff_x, Fraction) else coeff_x
            c2 = Fraction(const_term) if not isinstance(const_term, Fraction) else const_term
            
            root_val = -c2 / c1
        elif isinstance(coeff_x, int):
            # If both are ints (unlikely for exact factorization of this type but possible), use float logic or keep as fraction
            root_val = -(const_term if not isinstance(const_term, Fraction) else const_term) / coeff_x
            
        return root_val

    roots_raw = [get_root_from_factor(f1), get_root_from_factor(f2)]
    
    # Step 2: Sort roots ascending (numerical comparison required for ordering)
    sorted_roots = sorted(roots_raw)
    
    # Format LaTeX for the answer contract
    def format_latex_val(val):
        if isinstance(val, Fraction):
            return f"${val}$"
        else:
            return f"${float(val)}$"

    roots_latex_str = ", ".join(format_latex_val(r) for r in sorted_roots)
    
    # Construct the correct_answer object matching the contract schema
    correct_answer = {
        "roots": [str(int(round(float(r))) if isinstance(r, Fraction) else float(r)) for r in sorted_roots], 
        "factorization_latex": f"${f1['x_coefficient']}x + {f1['constant']}, ${f2['x_coefficient']}x + {f2['constant']}$",
        "roots_latex": roots_latex_str
    }

    # Ensure question_text is the provided stem string (already in frozen_params description)
    question_text = f"將一元二次方程式\n\\[\nx^2+4x-12=0\n\\]\n的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }
