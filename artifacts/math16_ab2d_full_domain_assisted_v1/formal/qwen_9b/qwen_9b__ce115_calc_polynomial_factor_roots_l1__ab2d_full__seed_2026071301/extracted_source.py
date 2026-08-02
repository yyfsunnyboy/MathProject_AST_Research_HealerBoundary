def generate(level=1, **kwargs):
    frozen_params = {
        "quadratic_coefficients": [1, 4, -12]
    }

    # Step 1: Factor the quadratic exactly using coefficients a,b,c from highest degree first.
    # The API expects (a, b, c) where polynomial is ax^2 + bx + c.
    factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)

    # Step 2: Extract roots and sort ascending.
    # Each factor dict has keys 'x_coefficient' and 'constant'.
    # Factor form: (x_coeff * x + constant). Root is where expression = 0 => x = -constant / x_coeff.
    raw_roots = []
    for f in factors:
        a_coef = f["x_coefficient"]
        b_const = f["constant"]
        root_val = -(b_const) / (a_coef)
        raw_roots.append(root_val)

    # Sort roots ascending as required by the contract.
    sorted_roots = sorted(raw_roots, reverse=False)  # Ascending order

    # Step 3: Format LaTeX for factors and roots.
    # We need to reconstruct the factorization string from the API results or format individually.
    # The API returns dicts like {'x_coefficient': -2, 'constant': 6} representing (-2x + 6).
    # To get a clean "factorization_latex", we construct it manually based on sorted factors for consistency with roots order? 
    # Usually factorization is written as product of linear terms. The problem asks to list roots ascending.
    # Let's format each factor and join them. Note: standard form often prefers monic or simplified, but API gives exact rational coeffs.
    
    def fmt_factor(f):
        a = f["x_coefficient"]
        b = f["constant"]
        if isinstance(a, int) and abs(a) == 1:
            # If coefficient is +/- 1, handle sign in x term or constant appropriately for latex display? 
            # API returns exact values. e.g., -2x + 6 -> "-2x+6". 
            # We need to ensure standard LaTeX spacing if possible, but format_latex works on coeffs list.
            pass
        
        # Construct a string representation manually since we have dicts, not lists directly for single factor formatting via API easily without reconstructing full poly?
        # Actually, we can use PolynomialOps.format_latex on the reconstructed coefficient list of each factor if needed, 
        # but format_latex expects highest degree first. A linear term [a, b] represents ax+b.
        
        # However, to ensure clean output matching typical expectations:
        # Factor 1: -2x + 6 -> "-2x+6" or "(-2)x+6"? 
        # Let's build the latex string manually for precision given we have exact rationals/integers.
        a_str = str(a) if isinstance(a, int) else f"{a}"
        b_str = str(b) if isinstance(b, int) else f"{b}"
        
        term1 = ""
        sign1 = "+"
        # Handle x term: ax
        if abs(float(a)) > 0.5 and float(a).is_integer():
            a_int = int(round(float(a)))
            if a_int == -2 or a_int == 2:
                term1 += f"{a_str}x"
            else:
                 # General case, though quadratic factorization usually yields simple integers for this level.
                 term1 += f"{a_str}x" 
        elif float(a).is_integer():
             if abs(float(a)) == 0: pass # Should not happen in valid factors of non-zero poly
             
        # Handle constant term
        sign2 = "+"
        
        # Re-evaluating manual construction vs format_latex.
        # Let's create a list for each factor and use format_latex to be safe with LaTeX rendering rules (e.g., 1x -> x).
        if isinstance(a, int) and abs(a) == 1:
            term_x = "x" if float(b_const / float(a)) > -0.5 else "-x"? No.
            # If a=2, b=-6 => 2x-6. format_latex([2,-6]) -> '2x-6'. Correct.
            # If a=-1, b=4 => -x+4? Or -(x)-4? 
            # Let's rely on format_latex for the linear term [a_coef, b_const].
            
        factor_list = [float(a), float(b)] if isinstance(a, int) else [a, b]
        # Wait, API returns ints or 'p/q'. format_latex handles these. But we must ensure 1x is rendered as x.
        # The example `PolynomialOps.format_latex([2, 0])` -> `'2x'`. 
        # What about `[1, -5]`? Likely `'x-5'`. Let's assume format_latex handles coefficient normalization for display (e.g., omitting '1').
        
        f_list = [a, b] if isinstance(a, int) else [float(a), float(b)] 
        # Actually inputs to factor are ints/strs. We should pass the exact types back or convert carefully?
        # The API returns `int` or `'p/q'`. format_latex accepts numeric coeffs.
        
        # Let's just use a helper to create latex for one linear term properly if needed, 
        # but simpler: construct string manually to guarantee "x" instead of "1x".
        
        ax = ""
        bx = ""
        
        val_a = float(a)
        val_b = float(b)
        
        if abs(val_a - round(val_a)) < 0.5 and not isinstance(a, str): # Integer check roughly
            a_int = int(round(val_a))
        else:
             # Fraction string handling? The API returns 'p/q' as strings for fractions in div_qr results sometimes, 
             # but factor_quadratic_exact says value_types ["int", "str"]. So if fraction, it's str.
             ax_str = f"{a}" + "x" if a != 0 else ""
        else:
            pass
            
    # Refined manual latex construction for robustness given the specific requirements (ascending roots):
    
    def make_latex_linear(a_val, b_val):
        # a_val can be int or str 'p/q'
        # We want to format ax + b
        
        if isinstance(a_val, str):
            return f"{a_val}x{b_val}" # Simplified assumption for fraction string input? 
            # Actually better: just use the values directly. If a is "1/2", it's "(1/2)x".
        
        # Let's assume standard integer inputs from factor_quadratic_exact usually yield integers or simple fractions represented as strings like '3/4'.
        # To be safe with LaTeX rendering of 1x -> x:
        
        if isinstance(a_val, int):
            a_str = str(abs(a_val)) + "x" * (a_val != 0)
            sign_a = "-" if a_val < 0 else ""
            
            # Handle b term
            if isinstance(b_val, int):
                b_sign = "+" if b_val > 0 else ""
                b_abs_str = str(abs(b_val)) if b_val != 0 else ""
                
                part_x = f"{sign_a}{a_str}" if a_val != 0 else "x" # If coeff is -1, sign handled? 
                # Correction: if a=-2, we want "-2x". My logic above adds "-" then abs. Correct.
                # But if a=1, part_x="x". Logic: f"{sign_a}{a_str}" -> "" + "1x" = "1x"? No need 1x.
                
                # Re-doing clean construction:
                term_x = ""
                sign_x = "+" 
                abs_a = int(abs(a_val)) if isinstance(a_val, (int, float)) else eval(f"{a_val}") # risky with str
                
        # Simpler approach using format_latex on the list [a,b] but post-processing "1x" to "x"?
        # Or trust that for this specific domain task level 1, inputs are integers.
        
        if isinstance(a_val, int):
            term_x = f"{abs(a_val)}x" * (a_val != 0)
            sign_x = "-" if a_val < 0 else ""
            
            # Handle constant b
            term_const = ""
            if b_val != 0:
                sign_c = "+" if b_val > 0 else ""
                abs_b = str(abs(b_val))
                term_const = f"{sign_c}{abs_b}"
                
            return f"{term_x} {term_const}".replace(" + ", "+").replace("- -", "-") # Clean up double signs? 
            # Actually format_latex does this. Let's just call it and fix "1x".
            
        else:
             term = str(a_val) + "x" + ("+" if float(b_val)>0 else "") + (str(abs(float(b_val))) if b_val!=0 else "")
             
    # Actually, let's use the API `format_latex` on `[a,b]` and then regex replace `"1x"` to `"x"`? 
    # But wait, format_latex might return `-2x+6`. If a=-1, it returns `-x+4` or `-1x+4`?
    # Standard polynomial libraries usually output `x` for coeff 1. Let's assume the API is smart enough OR we fix it.
    
    factor_list = [a, b] if isinstance(a, int) else [float(a), float(b)] 
    # Wait, inputs to format_latex must be numeric or str? "bool forbidden". Ints are fine.
    # Let's try:
    
    latex_factors_parts = []
    for f in factors:
        a_val = f["x_coefficient"]
        b_val = f["constant"]
        
        # Construct list of coefficients [a, b]
        coeffs_list = [int(a_val) if isinstance(a_val, int) else float(float(a_val)), 
                       int(b_val) if isinstance(b_val, int) else float(float(b_val))]
                       
        latex_str = PolynomialOps.format_latex(coeffs_list)
        
        # Post-process to ensure "1x" becomes "x" and "- 1x" becomes "- x"?
        # The API example `format_latex([2,0])` -> `'2x'`. 
        # If input is `[1,-5]`, likely returns `'x-5'` or `'1x-5'`. We need to be sure.
        # Given the constraints and typical behavior of such APIs in this context:
        if latex_str == "": continue
        
        # Fix potential 1x issues manually just in case
        import re
        latex_str = re.sub(r'\b(1)x\b', 'x', latex_str)
        
        latex_factors_parts.append(latex_str)

    factorization_latex = "*".join(latex_factors_parts) if len(factors) > 0 else ""
    
    # Format roots LaTeX: list of numbers. If integer, int; if fraction, str or formatted?
    # The contract says "roots" is a list (likely JSON serializable). 
    # For latex, we format each root.
    def fmt_root(r):
        if isinstance(r, float) and r.is_integer():
            return f"{int(r)}"
        elif isinstance(r, str):
             return r.replace('/', '\\frac')? No, standard mathjax usually handles / or \frac. 
             # The API format_latex might handle fractions nicely if passed a list like [0, 1/2]? 
             # But roots are values. We need to convert value to latex string.
             # If r is str '3/4', we want `\frac{3}{4}`? Or just `3/4`?
             # Usually for these tasks, if it's a fraction, use \frac.
             return f"\\frac{{{r.split('/')[0]}}}{{{{{r.split('/')[1]}}}}}" 
        else:
            return str(r)

    roots_latex_parts = [fmt_root(r) for r in sorted_roots]
    # Join with commas and spaces? "list of two distinct real roots". Usually comma separated.
    roots_latex = ", ".join(roots_latex_parts) if len(sorted_roots) > 0 else ""

    return {
        "question_text": "\\將一元二次方程式\\[x^2+4x-12=0\\]的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。",
        "correct_answer": {
            "roots": sorted_roots, # List of numbers (int or float/fraction string)
            "factorization_latex": factorization_latex,
            "roots_latex": roots_latex
        },
        "oracle_payload": frozen_params
    }