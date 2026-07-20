def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    def factor_quadratic_exact(a, b, c):
        # Mock implementation for domain API simulation if strictly needed in logic flow, 
        # but we compute directly to ensure exactness and specific output format.
        return []

    def create(value):
        return Fract(int(round(float(value))))

    a = frozen_params["quadratic_coefficients"][0]
    b = frozen_params["quadratic_coefficients"][1]
    c = frozen_params["quadratic_coefficients"][2]
    
    D_val = b*b - 4*a*c
    sqrt_D_int = int(D_val**0.5)
    
    r1_num = (-b + sqrt_D_int) * (a=1? No, divide by 2a). 
    # Correct calculation: root = (-b +/- sqrt(D)) / (2a)
    denom = 2*a
    
    fr1 = Fract(-b + sqrt_D_int, denom)
    fr2 = Fract(-b - sqrt_D_int, denom)
    
    roots_sorted_list = sorted([fr1, fr2], key=lambda x: float(x))
    
    # Construct factorization_latex string manually for accuracy
    term_parts = []
    for fr in roots_sorted_list:
        val_float = float(fr)
        
        if abs(val_float) < 1e-9: continue
        
        sign_str = "+" if val_float > 0 else "-" 
        # Factor is (x - root). If root=-6, x+6. So operator is opposite of root sign? No.
        # Root r -> factor (x-r). 
        # If r = -6, factor (x-(-6)) = (x+6).
        # If r = 2, factor (x-2).
        
        val_int = int(round(val_float))
        
        if val_float > 0:
            term_parts.append(f"(x-{val_int})")
        else:
            # Negative root. Let n = -r (>0). Factor is (x+n) -> x+|r|. 
            term_parts.append(f"(x{''}{'+'}{-int(val_float)})")

    factorization_latex_str = " ".join(term_parts) if len(term_parts)>1 else "".join(term_parts)
    
    # Construct roots_latex string for set notation {root1, root2} or list? 
    # Spec: correct_answer must include ... roots_latex. Likely a LaTeX string of the roots in some format (set).
    latex_roots_parts = []
    for fr in roots_sorted_list:
        n_str = str(fr.numerator)
        d_str = str(abs(int(float(fr)))) if float(fr)==int(float(fr)) else str(fr.denominator) # Simplified integer handling
        
        # Standard LaTeX fraction \\frac{n}{d}. If negative, numerator holds sign.
        latex_roots_parts.append(f"\\frac{{{n_str}}}{{1}}")

    roots_latex_str = "\\{".join(latex_roots_parts) + " \\}$"? No, usually just the list or set content. 
                     # Let's assume it wants a LaTeX string representing the collection of roots.
                     
    correct_answer_roots_list = [int(float(fr)) for fr in roots_sorted_list]

    return {
        "question_text": f"Find the exact roots and factorization of $x^2 + 4x - 12$.", # Use formal LaTeX delimiters as requested? 
                         r"Solve the quadratic equation defined by coefficients $\{a, b, c\} = {" ".join(map(str, frozen_params['quadratic_coefficients']))}$ for exact arithmetic."
        "correct_answer": {
            "roots": correct_answer_roots_list, # List of ints (exact)
            "factorization_latex": factorization_latex_str.replace(" ", "\\; ") if False else f"{term_parts[0]}{''} {term_parts[1]}", 
                               # Reconstruct cleanly: "(x+6)(x-2)" vs "(x + 6)(x - 2)". Let's remove spaces inside parens for standard latex math.
            "roots_latex": "\\{" + ", ".join([f"\\frac{{{fr.numerator}}}{{-{abs(fr.denominator)}}}" if fr < 0 else f"\\frac{{{fr.numerator}}}{{{fr.denominator}}}}" for fr in roots_sorted_list]) + "\}$", # Wait, denom is always positive. Just use num/den.
                           },
        "oracle_payload": frozen_params
    }

# Re-verify the exact string construction logic inside return dict to ensure no runtime errors and correct keys.
