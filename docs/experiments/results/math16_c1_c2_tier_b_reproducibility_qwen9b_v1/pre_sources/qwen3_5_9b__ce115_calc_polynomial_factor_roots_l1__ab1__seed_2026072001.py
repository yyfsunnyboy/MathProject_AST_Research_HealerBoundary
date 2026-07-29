def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Parse coefficients: ax^2 + bx + c
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    # Calculate discriminant and roots using exact arithmetic (fractions)
    from fractions import Fraction
    
    disc_val = b*b - 4*a*c
    if disc_val < 0:
        raise ValueError("No real roots for given coefficients")
    
    sqrt_disc = int(disc_val ** 0.5)
    # Ensure perfect square check implicitly handled by integer math here since inputs are small integers and problem implies solvable
    
    root1_num = -b + sqrt_disc
    root2_num = -b - sqrt_disc
    
    common_denom = a * (root1_num // gcd(root1_num, 4*a)) if False else 1 # Simplified logic for exact roots
    # Actually, let's compute roots exactly: (-b +/- sqrt(disc)) / (2a)
    
    def get_gcd(x, y):
        while y:
            x, y = y, x % y
        return abs(x) if x else 0
    
    denom_1 = 2 * a
    gcd_num_denom_1 = get_gcd(root1_num, denom_1)
    
    root1_frac_numerator = (root1_num // gcd_num_denom_1)
    root1_frac_denominator = (denom_1 // gcd_num_denom_1)
    
    # Handle negative denominator for canonical form
    if root1_frac_denominator < 0:
        root1_frac_numerator *= -1
        root1_frac_denominator *= -1
        
    denom_2 = 2 * a
    gcd_num_denom_2 = get_gcd(root2_num, denom_2)
    
    root2_frac_numerator = (root2_num // gcd_num_denom_2)
    root2_frac_denominator = (denom_2 // gcd_num_denom_2)

    if root2_frac_denominator < 0:
        root2_frac_numerator *= -1
        root2_frac_denominator *= -1
        
    # Sort roots ascending by value. Since denominators are positive, compare numerators directly? 
    # No, must convert to float for comparison or cross-multiply fractions.
    val1 = Fraction(root1_frac_numerator, root1_frac_denominator)
    val2 = Fraction(root2_frac_numerator, root2_frac_denominator)
    
    if val1 > val2:
        sorted_roots_fractions = [val2, val1]
    else:
        sorted_roots_fractions = [val1, val2]
        
    # Format roots for latex and answer string
    def format_fraction(n, d):
        if d == 1:
            return str(n)
        elif n % d == 0:
            return str(n // d)
        else:
            sign = "-" if (n < 0 or (d > 0 and n < 0)) else "" # Simplified check
            num_str = f"{abs(n)}"
            den_str = f"{abs(d)}"
            
            # Check for reducible forms like -1/2 vs -(1/2) usually standard is \frac{-n}{d} or similar. 
            # Standard LaTeX: \frac{numerator}{denominator}. If negative, put sign in numerator.
            if n < 0 and d > 0:
                num_str = f"-{abs(n)}"
            elif n > 0 and d < 0:
                den_str = f"{-d}" # Should not happen with our normalization but safe check
                num_str = str(abs(n))
                
            return rf"\frac{{{num_str}}}{{{{{den_str}}}}}"

    root1_latex = format_fraction(root1_frac_numerator, root1_frac_denominator)
    root2_latex = format_fraction(root2_frac_numerator, root2_frac_denominator)
    
    # Construct factorization: a(x - r1)(x - r2). 
    # Need to expand or present in factored form? "factorization_latex" usually implies (ax+b)(cx+d) or similar.
    # Let's construct linear factors from roots.
    # Root x = n/d => d*x - n = 0 => factor is (d*x - n). But we need monic inside if possible? 
    # Standard factored form for ax^2+bx+c: a(x-r1)(x-r2) or equivalent integer factors.
    
    # Factor 1 corresponding to root r1: (denom_1 * x + (-root_num)) -> denom*x - num = 0 => factor is (d*x - n). 
    # Wait, if root is p/q, then qx - p = 0. So factor is (qx - p).
    
    def get_factor_numerator(root_frac):
        return root_frac.denominator * "x" + "-" + str(abs(root_frac.numerator))

    # Let's build the string carefully for LaTeX
    r1_val = sorted_roots_fractions[0]
    r2_val = sorted_roots_fractions[1]
    
    factor_1_str = f"{r1_val.denominator}x - {abs(r1_val.numerator)}" if (r1_val.numerator < 0) else f"{r1_val.denominator}x + {-r1_val.numerator}" # Logic error in string concat above.
    
    def make_factor_string(frac):
        num = frac.numerator
        den = frac.denominator
        sign_str = "+" if (num > 0 and den < 0) or (num <= 0 and den > 0) else "" 
        # Actually simpler: term is den*x + (-num). If -num is positive, use +.
        const_term = -num
        if const_term >= 0:
            return rf"\left({den}x+{const_term}\right)"
        else:
            return rf"\left({den}x{const_term}\right)" # LaTeX handles negative numbers fine without space usually, but let's be clean.

    factor_1 = make_factor_string(r1_val)
    factor_2 = make_factor_string(r2_val)
    
    # The leading coefficient 'a' must be outside or distributed? 
    # Usually "factorization" for ax^2+bx+c is a(x-r1)(x-r2).
    # Or (denom*x - num)... Let's stick to standard form: a * factor1 * factor2 where factors are monic if possible, but here roots are rational.
    # Best representation: \left({r1_den}x-{r1_num}\right)\left({r2_den}x-{r2_num}\right) / (something)? 
    # No, the polynomial is exactly equal to a(x-r1)(x-r2).
    # Let's write it as: {a}(x - r_1)(x - r_2) with fractions inside.
    
    factorization_latex = rf"\left({r1_val.denominator}x{'' if r1_val.numerator >= 0 else ''}{-r1_val.numerator}\right)\left({r2_val.denominator}x{'' if r2_val.numerator >= 0 else ''}{-r2_val.numerator}\right)"
    # Correction: If numerator is positive, it's +num. If negative, -|num|. 
    # Let's rebuild factor strings properly for LaTeX
    
    def build_factor_latex(frac):
        den = frac.denominator
        num = frac.numerator
        if num > 0:
            return rf"\left({den}x+{num}\right)"
        elif num < 0:
            # -|num|. e.g. x + (-2) -> x-2. 
            val_str = str(-num)
            return rf"\left({den}x-{val_str}\right)"
        else:
             return rf"\left({den}x\right)"

    factor_1_latex = build_factor_latex(r1_val)
    factor_2_latex = build_factor_latex(r2_val)
    
    # The full polynomial is a * (factor1 without 'a' inside?) 
    # Actually, if we use roots r1, r2, then P(x) = k*(x-r1)*(x-r2). Here leading coeff is 1 in the monic version? No.
    # If we write factors as (den*x - num), their product has leading term den1*den2 * x^2. 
    # We need to divide by something or include 'a'.
    # Correct factorization: a(x-r1)(x-r2).
    
    roots_list = [str(r) for r in sorted_roots_fractions] # Just string representation? No, exact arithmetic required.
    correct_answer_str = rf"Roots: {r1_val}, {r2_val}. Factorization: \left({r1_val.denominator}x{'' if r1_val.numerator >= 0 else ''}{-r1_val.numerator}\right)\left({r2_val.denominator}x{'' if r2_val.numerator >= 0 else ''}{-r2_val.numerator}\right)"
    
    # Let's refine the correct_answer dict structure. 
    # "correct_answer" must include roots (ascending), factorization_latex, and roots_latex.
    
    final_roots = [f"{val}" for val in sorted_roots_fractions] # Wait, need to format nicely? Usually just Fraction string or specific latex?
    # Prompt says: correct_answer must include roots (ascending). Let's provide them as LaTeX fractions too if they are not integers.
    
    root1_display = f"{r1_val.numerator}/{r1_val.denominator}" if r1_val.denominator != 1 else str(r1_val.numerator)
    # Handle sign: -2/3 vs -(2/3). Standard is usually \frac{-2}{3}. 
    # Let's use a helper for display string.
    
    def get_root_display(frac):
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            num = frac.numerator
            den = frac.denominator
            sign = "-" if (num < 0 and den > 0) or (num > 0 and den < 0) else "" # Logic for negative fraction display in plain text? 
            # Usually just " -2/3 ". Let's assume standard math notation.
            return f"{sign}{abs(num)}/{den}"

    root1_disp = get_root_display(r1_val)
    root2_disp = get_root_display(r2_val)
    
    roots_latex_str = rf"\frac{{{r1_val.numerator}}}{{{{{r1_val.denominator}}}}}, \frac{{{r2_val.numerator}}}{{{{{r2_val.denominator}}}}}" # This is messy. 
    # Better: use the build_factor logic but for just root display?
    # Let's stick to simple LaTeX fractions in roots_latex.
    
    def make_root_latex(frac):
        n = frac.numerator
        d = frac.denominator
        if d == 1: return str(n)
        sign_n = "-" if n < 0 else ""
        abs_n = -n if n < 0 else n
        # If negative, put minus in numerator for standard LaTeX \frac{-a}{b} or just let it be? 
        # Usually \frac{numerator}{denominator}. If num is neg, write -2/3.
        return rf"\frac{{{sign_n}{abs_n}}}{{{{{d}}}}}"

    root1_latex = make_root_latex(r1_val)
    root2_latex = make_root_latex(r2_val)
    
    # Ensure ascending order in roots_latex string matches sorted_roots_fractions.
    # The list `sorted_roots_fractions` is already ordered.
    
    factorization_latex_str = rf"\left({r1_val.denominator}x{'' if r1_val.numerator >= 0 else ''}{-r1_val.numerator}\right)\left({r2_val.denominator}x{'' if r2_val.numerator >= 0 else ''}{-r2_val.numerator}\right)"
    # Wait, the product of these two factors is den1*den2 * x^2 + ... 
    # The original polynomial has leading coeff 'a'. 
    # So we must include 'a' in front? Or distribute it? 
    # If a=1 (as in example [1,4,-12]), then just the product.
    # General case: P(x) = a * factor1_monics * factor2_monics ? No.
    # Roots r1=p/q, r2=u/v. Factors are (qx-p), (vx-u). Product is qv x^2 ... 
    # We need to scale by 1/(qv)? Or just state the factors that multiply to give P(x) including 'a'.
    # Standard: a(x-r1)(x-r2).
    
    factorization_latex_str = rf"{r1_val.denominator}x{'' if r1_val.numerator >= 0 else ''}{-r1_val.numerator}" + " \cdot " + rf"{r2_val.denominator}x{'' if r2_val.numerator >= 0 else ''}{-r2_val.numerator}"
    # This is not monic. 
    # Let's try: a(x - p/q)(x - u/v) = (a/qv) * ... No, that introduces fractions in factors.
    # Usually factorization over rationals allows integer coefficients if possible? 
    # Given the constraints and "Exact arithmetic", let's output `a` times `(den1*x + num1)` etc divided by something? 
    # Actually, simplest exact factorization for ax^2+bx+c is: a(x-r1)(x-r2).
    
    roots_asc = [root1_latex, root2_latex] if r1_val <= r2_val else [root2_latex, root1_latex]
    # But we already sorted `sorted_roots_fractions`. 
    # Let's re-verify sorting.
    
    final_roots_list = []
    for f in sorted_roots_fractions:
        n = f.numerator
        d = f.denominator
        if d == 1: s = str(n)
        else:
            sign = "-" if (n < 0 and d > 0) or (n > 0 and d < 0) else "" # Simplified for display string logic, but let's just use LaTeX directly.
            abs_n = -n if n < 0 else n
            s = rf"\frac{{{sign}{abs_n}}}{{{{{d}}}}}" 
        final_roots_list.append(s)

    question_text = f"Find the roots and factorization of the polynomial $x^2 + {b}x + {c}$." # Wait, coefficients are [1, 4, -12]. So x^2+4x-12.
    # But need to handle general case if level changes? Frozen params fixed this one. 
    # However, the function signature allows kwargs/level. The frozen param is specific. 
    # I will construct the question based on the provided coefficients in `quadratic_coefficients`.
    
    a_val = quadratic_coefficients[0]
    b_val = quadratic_coefficients[1]
    c_val = quadratic_coefficients[2]
    
    q_text = rf"Find the roots and factorization of the polynomial $a x^2 + bx + c$ where coefficients are ${quadratic_coefficients}$." 
    # Or specifically: "Given the polynomial with coefficients [1, 4, -12], find..."
    q_text = f"Solve for the roots and provide the factorization of the quadratic equation defined by coefficients {quadratic_coefficients}."

    return {
        "question_text": question_text.replace("a", str(a_val)).replace("b", str(b_val)).replace("c", str(c_val)), # No, keep variables or substitute? 
        # Better: Substitute values for clarity.
        "correct_answer": {
            "roots": final_roots_list,
            "factorization_latex": rf"\left({sorted_roots_fractions[0].denominator}x{'' if sorted_roots_fractions[0].numerator >= 0 else ''}{-sorted_roots_fractions[0].numerator}\right)\left({sorted_roots_fractions[1].denominator}x{'' if sorted_roots_fractions[1].numerator >= 0 else ''}{-sorted_roots_fractions[1].numerator}\right)",
            "roots_latex": ", ".join(final_roots_list) # Wait, roots should be a list in the dict? Or string? 
        },
        "oracle_payload": quadratic_coefficients
    }

# Refining the return structure to match exactly: correct_answer must include keys.
# Let's rewrite cleanly without intermediate variable cluttering logic errors.

def generate(level=1, **kwargs):
    from fractions import Fraction
    
    # Frozen sampled parameters
    params = {"quadratic_coefficients": [1, 4, -12]}
    
    a = params["quadratic_coefficients"][0]
    b = params["quadratic_coefficients"][1]
    c = params["quadratic_coefficients"][2]
    
    # Discriminant
    disc = b*b - 4*a*c
    
    sqrt_disc_int = int(disc ** 0.5)
    if sqrt_disc_int * sqrt_disc_int != disc:
        raise ValueError("Discriminant not a perfect square")
        
    root1_num = -b + sqrt_disc_int
    root2_num = -b - sqrt_disc_int
    
    denom_common = 2 * a
    
    # Create fractions for roots
    def make_frac(n, d):
        g = abs(gcd_func := __import__('math').gcd(abs(n), d)) if n != 0 else d
        return Fraction(n // (d//g) , d // g) # Wait, gcd logic. 
        # Correct: num //= g, den //= g
    
    r1_num = root1_num
    r2_num = root2_num
    
    def simplify_frac(num, denom):
        common = abs(__import__('math').gcd(abs(num), denom)) if num != 0 else denom
        return Fraction(num // common, denom // common)

    f1 = simplify_frac(r1_num, denom_common)
    f2 = simplify_frac(r2_num, denom_common)
    
    # Sort ascending
    roots_sorted = sorted([f1, f2], key=lambda x: float(x)) if a != 0 else [f1, f2] # Handle degenerate? Assume quadratic.
    
    def format_latex_fraction(frac):
        n = frac.numerator
        d = frac.denominator
        if d == 1: return str(n)
        sign_n = "-" if (n < 0 and d > 0) or (n > 0 and d < 0) else "" # Actually, standard LaTeX puts minus in numerator.
        abs_n = -n if n < 0 else n
        return rf"\frac{{{sign_n}{abs_n}}}{{{{{d}}}}}"

    root1_latex_str = format_latex_fraction(f1)
    root2_latex_str = format_latex_fraction(f2)
    
    # Ensure order in roots_latex matches sorted list
    r_a, r_b = roots_sorted[0], roots_sorted[1]
    final_roots_list = [format_latex_fraction(r_a), format_latex_fraction(r_b)]
    roots_latex_str_combined = rf"{final_roots_list[0]}, {final_roots_list[1]}"

    # Factorization: a(x-r1)(x-r2) -> but we want integer coefficients in factors if possible? 
    # Factors are (den*x - num). Product is den_a*den_b * x^2 ...
    # We need to include 'a' explicitly or distribute. 
    # Standard form for ax^2+bx+c: a(x-r1)(x-r2) where r_i are fractions.
    # Let's write as: {a}(x - \frac{n_1}{d_1})(x - \frac{n_2}{d_2})
    
    def make_factor_latex(frac):
        n = frac.numerator
        d = frac.denominator
        if n > 0: return rf"\left(x+\frac{{{n}}}{{{{{d}}}}}\right)" # x + p/q -> (x - (-p/q)) -> factor is (qx+p) ? 
        # Wait, standard factored form usually keeps monic inside? No.
        # Let's use the integer coefficient factors: (dx - n). But then we need to divide by d1*d2 and multiply by a.
        # If we write P(x) = \frac{a}{d_1 d_2} (d_1 x - n_1)(d_2 x - n_2). 
        # This is exact arithmetic.
        
    f_a_latex = str(a_val if isinstance(a, int) else a.numerator/a.denominator) # 'a' from params
    
    factorization_str = rf"\left({r_b.denominator}x{'' if r_b.numerator >= 0 else ''}{-r_b.numerator}\right)\left({r_a.denominator}x{'' if r_a.numerator >= 0 else ''}{-r_a.numerator}\right)"
    # This misses the 'a' scaling. 
    # Let's assume the question asks for factorization over rationals, so a(x-r1)(x-r2) is best.
    
    final_factor_latex = rf"{a}(x - {root1_latex_str})(x - {root2_latex_str})"

    return {
        "question_text": f"Determine the roots and factorization of the polynomial $ax^2 + bx + c$ with coefficients ${params['quadratic_coefficients']}.$",
        "correct_answer": {
            "roots": final_roots_list,
            "factorization_latex": final_factor_latex,
            "roots_latex": roots_latex_str_combined
        },
        "oracle_payload": params["quadratic_coefficients"]
    }

# Wait, I need to import gcd or use math.gcd. And ensure no floats in output except for sorting logic which is internal.
# The prompt says: Do not use input, files, network... 
# My code uses `__import__('math')`. That's fine.
# Also "Exact arithmetic; no floats." -> Sorting using float() might be risky if roots are very close? But here integers/small ints. 
# Better sort by Fraction comparison directly.

def generate(level=1, **kwargs):
    from fractions import Fraction
    
    params = {"quadratic_coefficients": [1, 4, -12]}
    
    coeffs = params["quadratic_coefficients"]
    a_val = coeffs[0]
    b_val = coeffs[1]
    c_val = coeffs[2]
    
    disc = b_val*b_val - 4*a_val*c_val
    
    # Roots: (-b +/- sqrt(disc)) / (2a)
    import math
    sqrt_disc = int(math.isqrt(abs(disc))) if disc >= 0 else None
    if sqrt_disc * sqrt_disc != abs(disc):
        raise ValueError("Invalid discriminant")
    
    root1_num = -b_val + sqrt_disc
    root2_num = -b_val - sqrt_disc
    
    denom_common = 2 * a_val
    
    def simplify(n, d):
        if n == 0: return Fraction(0)
        g = math.gcd(abs(n), abs(d))
        return Fraction(n // g, d // g)

    r1 = simplify(root1_num, denom_common)
    r2 = simplify(root2_num, denom_common)
    
    # Sort ascending using Fraction comparison (exact)
    if r1 > r2:
        sorted_roots = [r2, r1]
    else:
        sorted_roots = [r1, r2]
        
    def fmt_latex_frac(f):
        n, d = f.numerator, f.denominator
        if d == 1: return str(n)
        sign_n = "-" if (n < 0 and d > 0) or (n > 0 and d < 0) else "" # Logic for negative fraction display in LaTeX usually puts minus on top.
        abs_n = -n if n < 0 else n
        return rf"\frac{{{sign_n}{abs_n}}}{{{{{d}}}}}"

    root1_latex = fmt_latex_frac(sorted_roots[0])
    root2_latex = fmt_latex_frac(sorted_roots[1])
    
    roots_list_str = [root1_latex, root2_latex] # Already sorted
    
    # Factorization: a(x-r1)(x-r2)
    factorization_latex = rf"{a_val}(x - {root1_latex})(x - {root2_latex})"

    return {
        "question_text": f"Solve for the roots and provide the factorization of $ax^2+bx+c$ given coefficients ${coeffs}$.",
        "correct_answer": {
            "roots": roots_list_str,
            "factorization_latex": factorization_latex,
            "roots_latex": rf"{root1_latex}, {root2_latex}" # Wait, order matters. 
        },
        "oracle_payload": coeffs
    }

# Re-check sorting in `correct_answer` roots list vs `roots_latex`. They must be consistent.
# In the dict above: `roots` is a list of strings (LaTeX). `roots_latex` is a string combining them with comma.
# The order in `roots` list should match ascending order. My code does that.

def generate(level=1, **kwargs):
    from fractions import Fraction
    
    params = {"quadratic_coefficients": [1, 4, -12]}
    
    coeffs = params["quadratic_coefficients"]
    a_val = coeffs[0]
    b_val = coeffs[1]
    c_val = coeffs[2]
    
    disc = b_val*b_val - 4*a_val*c_val
    
    import math
    sqrt_disc = int(math.isqrt(abs(disc))) if disc >= 0 else None
    
    root1_num = -b_val + sqrt_disc
    root2_num = -b_val - sqrt_disc
    
    denom_common = 2 * a_val
    
    def simplify(n, d):
        if n == 0: return Fraction(0)
        g = math.gcd(abs(n), abs(d))
        return Fraction(n // g, d // g)

    r1 = simplify(root1_num, denom_common)
    r2 = simplify(root2_num, denom_common)
    
    if r1 > r2:
        sorted_roots = [r2, r1]
    else:
        sorted_roots = [r1, r2]
        
    def fmt_latex_frac(f):
        n, d = f.numerator, f.denominator
        if d == 1: return str(n)
        sign_n = "-" if (n < 0 and d > 0) or (n > 0 and d < 0) else "" 
        abs_n = -n if n < 0 else n
        return rf"\frac{{{sign_n}{abs_n}}}{{{{{d}}}}}"

    root1_latex = fmt_latex_frac(sorted_roots[0])
    root2_latex = fmt_latex_frac(sorted_roots[1])
    
    roots_list_str = [root1_latex, root2_latex] 
    combined_roots_latex = rf"{root1_latex}, {root2_latex}"

    factorization_latex = rf"{a_val}(x - {root1_latex})(x - {root2_latex})"

    return {
        "question_text": f"Solve for the roots and provide the factorization of $ax^2+bx+c$ given coefficients ${coeffs}$.",
        "correct_answer": {
            "roots": roots_list_str,
            "factorization_latex": factorization_latex,
            "roots_latex": combined_roots_latex
        },
        "oracle_payload": coeffs
    }