def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Calculate roots using exact arithmetic (fractions) to avoid floats
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b * b - 4 * a * c
    
    if discriminant < 0:
        raise ValueError("No real roots for the given coefficients.")
    
    sqrt_discriminant_int = int(discriminant ** 0.5)
    if sqrt_discriminant_int * sqrt_discriminant_int != discriminant:
        # If not a perfect square, we handle rational approximation or keep as fraction logic implicitly via string formatting later? 
        # Task says "Exact arithmetic; no floats". We must represent roots exactly.
        # Since inputs are integers and level 1 usually implies nice numbers, let's assume perfect squares for this specific frozen sample.
        # However, to be robust: if not integer sqrt, we use Fraction logic or string representation of surds? 
        # Given "Exact arithmetic", using fractions module is safer.
        from fractions import Fraction
        
        root1_num = -b + discriminant ** 0.5
        root2_num = -b - discriminant ** 0.5
        
        if discriminant > 0:
            sqrt_val = (discriminant) ** 0.5
            # Check for perfect square again with tolerance or exact check? 
            # For integer inputs, isqrt works perfectly in Python 3.8+
            import math
            s = int(math.isqrt(discriminant))
            
            if s * s == discriminant:
                root1_num = -b + s
                root2_num = -b - s
            else:
                # Irrational roots case for level 1? Usually L1 is rational. 
                # If irrational, we format as LaTeX surds.
                pass
        
        if s * s == discriminant:
             denom_a = a
             r1_numerator = root2_num // -denom_a if (root2_num % -denom_a) == 0 else None # Simplify logic
            
            # Let's re-calculate roots properly with Fraction for exactness
            from fractions import Fraction
            
            disc_frac = Fraction(discriminant, 1)
            
            # Check perfect square in fraction terms? No, discriminant is int.
            s_int = math.isqrt(discriminant)
            
            if s_int * s_int == discriminant:
                root1_val = Fraction(-b + s_int, a)
                root2_val = Fraction(-b - s_int, a)
                
                # Sort ascending
                roots_list = sorted([root1_val, root2_val])
                correct_roots_str = ", ".join(str(r) for r in roots_list)
            else:
                # Irrational case (unlikely for L1 with these specific frozen params but handled for correctness)
                s_int = math.isqrt(discriminant)
                term_sqrt = f"\\sqrt{{{discriminant}}}"
                
                root1_expr = Fraction(-b + 0, a) + Fraction(0, 1) # Placeholder logic correction needed
                
                # Actually: x = (-b +/- sqrt(D)) / (2a) ?? No, standard quadratic formula is for ax^2+bx+c=0.
                # Roots are (-b ± √D) / (2a). Wait, the coefficients given [1, 4, -12] usually mean a*x^2 + b*x + c? 
                # Or does it mean x^3... ? "quadratic_coefficients" implies quadratic.
                # Standard form: ax^2 + bx + c = 0. Roots are (-b ± sqrt(b^2-4ac)) / (2a).
                
                numerator1 = -b + s_int
                denominator_common = 2 * a
                
                root1_val = Fraction(numerator1, denominator_common) if discriminant == s_int*s_int else None
                
                # Re-evaluating the specific frozen sample: [1, 4, -12] -> x^2 + 4x - 12 = 0
                # D = 16 - 4(1)(-12) = 16 + 48 = 64. sqrt(64)=8. Perfect square.
                # Roots: (-4 ± 8)/2 -> (4/2, -12/2) -> (2, -6). Sorted: [-6, 2].
                
                root1_val = Fraction(-b + s_int, 2 * a)
                root2_val = Fraction(-b - s_int, 2 * a)
                roots_list = sorted([root1_val, root2_val])
                correct_roots_str = ", ".join(str(r) for r in roots_list)

        else:
            # Fallback if discriminant is not perfect square (shouldn't happen with this specific sample but good practice)
             s_int = math.isqrt(discriminant)
             root1_val = Fraction(-b + s_int, 2 * a)
             root2_val = Fraction(-b - s_int, 2 * a)
             roots_list = sorted([root1_val, root2_val])
             correct_roots_str = ", ".join(str(r) for r in roots_list)

    else:
        # Re-run the logic cleanly inside the block to avoid scope confusion
        
        import math
        from fractions import Fraction
        
        s_int = int(math.isqrt(discriminant))
        
        if s_int * s_int == discriminant:
            root1_val = Fraction(-b + s_int, 2 * a)
            root2_val = Fraction(-b - s_int, 2 * a)
            
            # Sort ascending numerically (Fraction supports comparison)
            roots_list = sorted([root1_val, root2_val])
        else:
             raise ValueError("Discriminant is not a perfect square. Level 1 expects rational roots.")

    correct_roots_str = ", ".join(str(r) for r in roots_list)
    
    # Factorization latex: (x - r1)(x - r2) if monic, else a(x-r1)(x-r2). 
    # Since coefficients are [a,b,c], and we found exact rational roots.
    # If root is integer k, factor is (x-k). If fraction p/q, usually written as (qx-p)? Or just keep standard form?
    # Standard polynomial factoring over rationals: a(x - r1)(x - r2) where r are the actual roots found by formula.
    
    if len(roots_list) == 0:
        factorization_latex = "No real factors"
    else:
        r1, r2 = roots_list[0], roots_list[1] # Already sorted
        
        # Construct LaTeX for (x - root). If root is Fraction(p/q), usually we write (qx - p) scaled? 
        # But the prompt asks for factorization_latex. Usually implies monic factors if possible or standard form.
        # Let's assume standard expansion: a(x - r1)(x - r2).
        
        def format_root(root):
            num = root.numerator
            den = root.denominator
            
            if den == 1:
                return f"x - {num}"
            else:
                # For rational roots, e.g., x - (p/q) -> qx - p? 
                # Or just keep as fraction in LaTeX. Let's use standard fractional form for clarity unless integer.
                # However, factoring usually prefers integer coefficients inside the binomial if possible.
                # Example: 2x^2 + ... root = 1/2. Factor (2x - 1). 
                # But here we have 'a' outside? The roots are defined by ax^2+bx+c=0.
                # If we write a(x-r1)(x-r2), then r1, r2 are the exact values from formula (-b±√D)/2a.
                # So (x - 1/2) is correct if root is 1/2. 
                return f"x - \\frac{{{num}}}{{den}}"

        term1 = format_root(r1)
        term2 = format_root(r2)
        
        factorization_latex = f"{a}({term1})({term2})"
    
    roots_latex_str = ", ".join([f"\\left(\\\\frac{{{r.numerator}}}{{r.denominator}}\\\\right)" if r.denominator != 1 else str(r) for r in roots_list]) # Wait, question asks for "roots_latex". Usually just the values.
    
    # Let's refine roots_latex: list of LaTeX strings representing the root values.
    latex_roots = []
    for r in roots_list:
        if r.denominator == 1:
            latex_roots.append(f"{r.numerator}")
        else:
            latex_roots.append(f"\\\\frac{{{r.numerator}}}{{r.denominator}}") # Wait, variable name clash. Use 'num', 'den'.

    final_latex_roots = ", ".join([f"\\\\frac{{{root.numerator}}}{{root.denominator}}" if root.denominator != 1 else str(root) for root in roots_list])
    
    question_text = f"Solve the quadratic equation $x^2 + {quadratic_coefficients[1]}x + {quadratic_coefficients[2]} = 0$. Find the real roots and factorize." # Adjusted to match coefficients exactly. 
    # Actually, better: "Find the roots of the polynomial defined by coefficients [a,b,c]".
    
    a_val = quadratic_coefficients[0]
    b_val = quadratic_coefficients[1]
    c_val = quadratic_coefficients[2]
    
    question_text = f"Given the quadratic equation $x^{{2}} + {b_val}x + {c_val} = 0$, find its real roots and express them in ascending order. Also, provide the factorization of the polynomial."

    return {
        "question_text": question_text,
        "correct_answer": {
            "roots": [float(r) for r in roots_list], # Wait: "Exact arithmetic; no floats". 
            # The spec says correct_answer must include roots. If I put float list it violates "no floats"? 
            # But JSON requires standard types. Usually, we return the Fraction objects converted to strings or a specific format?
            # Re-reading: "correct_answer must include roots (ascending), factorization_latex, and roots_latex."
            # It doesn't explicitly say 'roots' field in correct_answer dict MUST be floats if not specified type. 
            # But JSON cannot hold Fraction. I will store them as strings or a list of lists [numerator, denominator]?
            # Or maybe the user expects a specific structure for roots? "Exact arithmetic" implies we shouldn't compute float approximations internally, but output format might be flexible.
            # However, standard API responses often use floats unless specified otherwise (e.g., symbolic). 
            # Given "no floats", I will represent roots in correct_answer['roots'] as a list of strings or dicts? 
            # Let's assume the 'roots' key expects a list of values that are exact. Since JSON doesn't support Fraction, I'll use [numerator/denominator] tuples encoded as lists [[n,d], ...].
            
            # Wait, looking at similar tasks: often roots is expected to be a list of numbers if they are integers, or strings for fractions? 
            # Let's try to output them as strings in the JSON value for 'roots' to ensure exactness.
            
            root_strs = [str(r) for r in roots_list]
            
        },
        "factorization_latex": factorization_latex,
        "roots_latex": final_latex_roots
    }

# Correction: The return statement needs to be valid Python dict construction inside the function.
# I need to rewrite the logic cleanly without variable leakage errors in thought process.

def generate(level=1, **kwargs):
    import math
    from fractions import Fraction
    
    quadratic_coefficients = [1, 4, -12]
    
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b * b - 4 * a * c
    
    if discriminant < 0:
        raise ValueError("No real roots.")
        
    s_int = int(math.isqrt(discriminant))
    
    # Check perfect square for exact rational roots (Level 1 assumption)
    if s_int * s_int != discriminant:
         # If not perfect square, we might need symbolic representation. 
         # But let's assume the frozen sample guarantees nice numbers or handle surds in latex only?
         # The task says "Exact arithmetic; no floats". We will use Fraction for roots regardless if possible, else stringify sqrt.
         pass
    
    s = int(math.isqrt(discriminant))
    
    root1_val = Fraction(-b + s, 2 * a)
    root2_val = Fraction(-b - s, 2 * a)
    
    # Sort ascending
    roots_list = sorted([root1_val, root2_val])
    
    correct_roots_strs = [str(r) for r in roots_list]
    
    def format_root_latex(root):
        if root.denominator == 1:
            return f"{root.numerator}"
        else:
            return f"\\\\frac{{{root.numerator}}}{{r{root.denominator}}}" # Wait, variable name 'den' is better.
            
    r = roots_list[0]
    term1 = f"x - {format_root_latex(r)}".replace("r", "d") if False else "" 
    # Let's rebuild the latex string carefully
    
    def get_term(root):
        num, den = root.numerator, root.denominator
        if den == 1:
            return f"(x - {num})"
        else:
            return f"(qx - p)" style? No. 
            # Standard LaTeX for factor with rational root p/q is usually (q x - p).
            # But the polynomial is monic in our example [1,4,-12]. So factors are (x-r).
            # If r = 3/5, then (x - 3/5) or (5x-3)/5? 
            # Usually factorization of ax^2+bx+c over Q is a(x-p/q)(x-q/p)? No.
            # It's a * product of monic factors with rational roots.
            return f"(x - \\\\frac{{{num}}}{{den}})"

    term1_latex = get_term(roots_list[0])
    term2_latex = get_term(roots_list[1])
    
    factorization_latex = f"{a}{term1_latex}{term2_latex}" # Remove spaces for compactness or keep? Keep standard.
    
    roots_latex_strs = []
    for r in roots_list:
        if r.denominator == 1:
            roots_latex_strs.append(f"\\\\frac{{{r.numerator}}}{{1}}") # Or just the number? Usually numbers are fine, but spec says "roots_latex". Maybe formatted as fractions always.
            # Let's format all as fractions for consistency in latex field if requested, or integers without denominator. 
            # Better: if int, print integer; else fraction.
        roots_latex_strs.append(f"\\\\frac{{{r.numerator}}}{{{r.denominator}}}" if r.denominator != 1 else str(r))

    question_text = f"Solve the quadratic equation $x^2 + {b}x + {c} = 0$. Find the real roots in ascending order and provide the factorization."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "roots": correct_roots_strs, # List of strings for exactness
            "factorization_latex": f"{a}{term1_latex.replace('\\\\', '\\\\')}{term2_latex.replace('\\\\', '\\\\')}", 
            "roots_latex": ", ".join(roots_latex_strs)
        },
        "oracle_payload": quadratic_coefficients
    }

# Wait, I need to ensure the latex escaping is correct for the final string.
# And handle the specific case of [1, 4, -12] correctly in the code logic so it's generic enough but works for this sample.
# Also "correct_answer" roots field: if JSON expects numbers, strings are safer for exactness.

def generate(level=1, **kwargs):
    import math
    from fractions import Fraction
    
    quadratic_coefficients = [1, 4, -12]
    
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b * b - 4 * a * c
    s_int = int(math.isqrt(discriminant))
    
    # Ensure perfect square for exact rational roots (Level 1)
    if s_int * s_int != discriminant:
        raise ValueError("Discriminant is not a perfect square.")

    root1_val = Fraction(-b + s_int, 2 * a)
    root2_val = Fraction(-b - s_int, 2 * a)
    
    roots_list = sorted([root1_val, root2_val])
    
    # Format for correct_answer['roots'] as strings to maintain exactness in JSON
    roots_strs = [str(r) for r in roots_list]
    
    # Build LaTeX terms
    def make_latex_term(root):
        num, den = root.numerator, root.denominator
        if den == 1:
            return f"(x - {num})"
        else:
            return f"(x - \\\\frac{{{num}}}{{den}})"

    term1 = make_latex_term(roots_list[0])
    term2 = make_latex_term(roots_list[1])
    
    # Combine with 'a' coefficient. Note: if a is not 1, we multiply outside? 
    # The factorization of ax^2+bx+c where roots are r1,r2 is a(x-r1)(x-r2).
    full_factor_latex = f"{a}{term1} {term2}"

    # Roots latex list (comma separated)
    def make_roots_latex(root):
        num, den = root.numerator, root.denominator
        if den == 1:
            return str(num)
        else:
            return f"\\\\frac{{{num}}}{{den}}"
            
    roots_latex_list = [make_roots_latex(r) for r in roots_list]

    question_text = f"Solve the quadratic equation $x^2 + {b}x + {c} = 0$. Find the real roots and factorize."

    return {
        "question_text": question_text,
        "correct_answer": {
            "roots": roots_strs,
            "factorization_latex": full_factor_latex.replace(" ", ""), # Compact latex often preferred? Or with spaces. Let's keep readable.
            "roots_latex": ", ".join(roots_latex_list)
        },
        "oracle_payload": quadratic_coefficients
    }

# Final check on escaping: In Python f-strings, \\ becomes \\. 
# When printing or returning string for JSON serialization later, it should be correct.
# The function returns a dict. The values inside are strings containing LaTeX commands like \\frac.
# This is standard practice for such tasks.

def generate(level=1, **kwargs):
    import math
    from fractions import Fraction
    
    quadratic_coefficients = [1, 4, -12]
    
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b * b - 4 * a * c
    s_int = int(math.isqrt(discriminant))
    
    if s_int * s_int != discriminant:
        raise ValueError("Discriminant is not a perfect square.")

    root1_val = Fraction(-b + s_int, 2 * a)
    root2_val = Fraction(-b - s_int, 2 * a)
    
    roots_list = sorted([root1_val, root2_val])
    
    # Format for correct_answer['roots'] as strings to maintain exactness in JSON
    roots_strs = [str(r) for r in roots_list]
    
    def make_latex_term(root):
        num, den = root.numerator, root.denominator
        if den == 1:
            return f"(x - {num})"
        else:
            return f"(x - \\\\frac{{{num}}}{{den}})"

    term1 = make_latex_term(roots_list[0])
    term2 = make_latex_term(roots_list[1])
    
    full_factor_latex = f"{a}{term1} {term2}"

    def make_roots_latex(root):
        num, den = root.numerator, root.denominator
        if den == 1:
            return str(num)
        else:
            return f"\\\\frac{{{num}}}{{den}}"
            
    roots_latex_list = [make_roots_latex(r) for r in roots_list]

    question_text = f"Solve the quadratic equation $x^2 + {b}x + {c} = 0$. Find the real roots and factorize."

    return {
        "question_text": question_text,
        "correct_answer": {
            "roots": roots_strs,
            "factorization_latex": full_factor_latex.replace(" ", ""), 
            "roots_latex": ", ".join(roots_latex_list)
        },
        "oracle_payload": quadratic_coefficients
    }