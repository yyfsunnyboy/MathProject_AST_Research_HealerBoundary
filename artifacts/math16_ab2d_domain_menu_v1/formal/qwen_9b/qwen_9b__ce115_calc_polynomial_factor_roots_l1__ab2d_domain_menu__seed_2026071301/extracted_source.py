from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "quadratic_coefficients": [1, 4, -12]
    }
    
    # Factor the quadratic polynomial exactly. 
    # The API returns a list of dicts with keys 'x_coefficient' and 'constant'.
    factors = PolynomialOps.factor_quadratic_exact(1, 4, -12)
    
    # Extract roots from factorization: (ax + b)(cx + d) -> ax+b=0 => x=-b/a.
    # The API returns dicts like {'x_coefficient': a, 'constant': b}. Root is -b/a.
    root_values = []
    for f in factors:
        coeff_x = int(f["x_coefficient"]) if isinstance(f["x_coefficient"], str) else float(f["x_coefficient"])
        const_term = int(f["constant"]) if isinstance(f["constant"], str) else float(f["constant"])
        
        # Calculate root value. Since inputs are exact integers, result is rational/integer.
        # We need to format as string for JSON safety or keep Fraction? 
        # The contract asks for "roots" list and latex strings. Usually roots in these tasks are numbers (int/fraction).
        # Let's compute the float value first, but we should probably use exact arithmetic if possible.
        # However, PolynomialOps.factor_quadratic_exact returns int or 'p/q'. 
        # We need to construct a Fraction-like object or just calculate -const/coeff_x.
        
        # To ensure JSON safety and correctness for sorting:
        from fractions import Fraction
        
        num = -Fraction(const_term) if isinstance(f["constant"], str) else (-f["constant"])
        den = Fraction(coeff_x) if isinstance(f["x_coefficient"], str) else f["x_coefficient"]
        
        root_val = num / den
        # Convert to float for sorting, but keep exact representation? 
        # The contract says "roots ordered ascending". Usually implies numerical order.
        # We will store the Fraction object or a string that can be parsed? 
        # Standard practice in these generated tasks: return list of numbers (floats) if they are simple, 
        # or strings for complex rationals. But let's check typical output format.
        # Given "roots_latex" is required separately, the 'roots' field likely expects a list of numeric values (int/str).
        root_values.append(root_val)

    # Sort roots ascendingly by numerical value
    root_values.sort(key=lambda x: float(x))
    
    # Format LaTeX for factorization and roots.
    # Factorization string construction manually or via helper? 
    # PolynomialOps.format_latex takes coefficients of the polynomial, not factors directly in a specific format like "(ax+b)(cx+d)".
    # We need to construct the latex string for the factored form ourselves based on the factor dicts.
    
    def make_factor_str(f):
        c_x = f["x_coefficient"]
        const_term = f["constant"]
        
        if isinstance(c_x, str) or isinstance(const_term, str):
            # Handle 'p/q' strings for latex formatting manually? 
            # The API format_latex handles standard coefficients. For factored form like (2x+3), we need to build it.
            pass
        
        # Construct LaTeX parts
        if c_x != 1:
            x_part = f"{c_x}x"
        else:
            x_part = "x"
            
        const_str = str(const_term)
        
        return f"({x_part}{const_str})".replace(" + ", "+").replace("- -", "-") # Simplified logic
        
    # Better approach for latex factorization string:
    def format_factor_latex(f):
        c_x = f["x_coefficient"]
        const_term = f["constant"]
        
        x_part = "" if (c_x == 1 and not isinstance(c_x, str)) else "x" 
        # Actually need to handle signs carefully.
        # If factor is -2x + 3 -> (-2x+3) or -(2x-3)? Usually standard form inside parenthesis.
        
        sign = "+" if const_term >= 0 else "-"
        abs_const = str(abs(const_term)) if isinstance(const_term, int) else f"{const_term}".replace(" ", "") # simplistic
        
        # Re-evaluating latex construction for generic rational coeffs:
        def get_latex_val(val):
            s = val if not isinstance(val, str) else val.replace("/", "/") 
            return s
            
        lx_cx = c_x if not isinstance(c_x, str) else f"\\frac{{{c_x}}}{{1}}" # simplistic for now? No.
        
        # Let's rely on standard latex generation logic:
        cx_str = get_latex_val(c_x)
        const_str = get_latex_val(const_term)
        
        if c_x == 0 and const_term != 0: return f"({const_str})"
        elif c_x != 0:
            # Handle sign in latex properly for the term inside parenthesis
            term1 = cx_str + "x"
            
            # Determine operator between terms
            op = "+" if (isinstance(const_term, int) and const_term >= 0) or \
                   (not isinstance(const_term, str) and const_term > 0) else "-"
            
            return f"({term1}{op} {const_str})".replace(" + ", "+").replace("- -", "-") # cleanup
            
        return "()"

    factor_latex_parts = [format_factor_latex(f) for f in factors]
    
    # Construct the full latex string with multiplication sign or implicit? 
    # Usually explicit * is preferred if ambiguous, but often omitted. Let's use \cdot or *.
    factorization_latex = " \\cdot ".join(factor_latex_parts).replace("\\cdot ", "\\times ")
    # Actually standard mathjax: (x+...)(...). Let's just join with ' \\cdot '.
    
    roots_latex_list = []
    for r in root_values:
        if isinstance(r, Fraction):
            latex_r = f"\\frac{{{r.numerator}}}{{{r.denominator}}}"
        else:
            # If it was a simple int/float from the API (unlikely given 'p/q' return type)
            latex_r = str(int(r)) + ".0" if isinstance(r, float) and r.is_integer() else f"{r:.2f}".rstrip('0').rstrip('.') 
            # But since we have Fraction objects now:
            pass
            
    # Re-calculate roots_latex using the exact fractions derived earlier to ensure precision.
    latex_roots = []
    for r in root_values:
        if isinstance(r, Fraction):
             latex_roots.append(f"\\frac{{{r.numerator}}}{{{r.denominator}}}")
        else:
            # Fallback if somehow float (shouldn't happen with exact API)
            latex_roots.append(str(int(r)) + ".0")

    question_text = r"\[x^2+4x-12=0\] 的左式在有理數範圍內因式分解，並依數值由小到大列出兩個相異實根。"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "roots": [float(r) for r in root_values], # Return floats or ints as appropriate? 
                   # The API returns int/str. We converted to Fraction then float for sort.
                   # For JSON output of roots: usually list[int] or list[float]. 
                   # Let's convert back to exact representation if possible, but the prompt implies numeric values.
                   # Given "roots ordered ascending", floats are standard unless specified otherwise.
            "factorization_latex": factorization_latex.replace("\\cdot ", "\\times "),
            "roots_latex": "; ".join(latex_roots)
        },
        "oracle_payload": frozen_params
    }