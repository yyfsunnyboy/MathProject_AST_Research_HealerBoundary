def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Calculate roots using exact arithmetic (fractions) to avoid floats
    from fractions import Fraction
    
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b * b - 4 * a * c
    sqrt_discriminant_int = int(discriminant ** 0.5)
    
    # Roots formula: (-b +/- sqrt(D)) / (2a)
    root1_num = -b + sqrt_discriminant_int
    root1_denom = 2 * a
    
    root2_num = -b - sqrt_discriminant_int
    root2_denom = 2 * a
    
    # Simplify fractions for roots
    def simplify_fraction(n, d):
        if n == 0:
            return Fraction(0)
        common = abs(int(d)) // gcd(abs(n), int(d)) # Need to import math.gcd or define it
        from math import gcd as _gcd
        g = _gcd(n, d)
        sign = -1 if (n < 0 and d > 0) or (n > 0 and d < 0) else 1
        return Fraction(sign * abs(n // g), abs(d // g))

    # Re-implement gcd logic inline to ensure no external dependency issues if needed, 
    # but math.gcd is standard. Let's use fractions directly for exactness.
    
    root1 = Fraction(root1_num, 2*a)
    root2 = Fraction(root2_num, 2*a)
    
    # Sort roots ascending (numerical comparison of Fractions works correctly)
    sorted_roots = sorted([root1, root2])
    
    # Construct LaTeX for factors: a(x - r1)(x - r2) -> but usually monic form is preferred or expanded. 
    # Task asks for factorization_latex and roots_latex.
    # Standard factorization of ax^2+bx+c = a(x-r1)(x-r2).
    
    def format_fraction(frac):
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            return f"\\frac{{{frac.numerator}}}{{{{{frac.denominator}}}}}"

    r1_str = format_fraction(sorted_roots[0])
    r2_str = format_fraction(sorted_roots[1])
    
    # Roots LaTeX (ascending order as requested by "roots_latex")
    roots_latex = f"\\left( {r1_str} \\right), \\left( {r2_str} \\right)"
    
    # Factorization LaTeX: a(x - r1)(x - r2)
    factorization_latex = f"{a}(x-{format_fraction(Fraction(-sorted_roots[0].numerator, sorted_roots[0].denominator))})(x-{format_fraction(Fraction(-sorted_roots[1].numerator, sorted_roots[1].denominator))})" 
    # Wait, the roots are already negative in value if we write (x - r).
    # If root is 2/3, factor is (x - 2/3). If root is -4, factor is (x + 4) which is (x - (-4)).
    # Let's reconstruct carefully.
    
    # Correct logic for LaTeX factors:
    # Factor = a * (x - r1) * (x - r2)
    # We need to format the term inside parenthesis correctly handling signs in numerator/denominator
    
    def get_factor_term(r):
        num = r.numerator
        den = r.denominator
        if den == 1:
            val_str = str(num)
        else:
            val_str = f"\\frac{{{num}}}{{{{{den}}}}}"
        
        # If value is positive, we write (x - val). If negative, (x + abs(val)).
        # However, standard LaTeX often just uses minus and lets the fraction handle sign.
        # Let's stick to strict mathematical notation: x - r.
        return f"\\left(x-{val_str}\\right)"

    factor1 = get_factor_term(sorted_roots[0])
    factor2 = get_factor_term(sorted_roots[1])
    
    factorization_latex = f"{a}{factor1}{factor2}"
    
    # Question text construction
    question_text = (f"Find the roots and factorize the quadratic polynomial with coefficients {quadratic_coefficients}. "
                     f"The polynomial is $x^{{4}} + 4x - 12$? No, it's degree 2. "
                     f"The polynomial is ${a}x^2+{b}x+{c}$." )
    
    # Let's make the question text formal and precise using LaTeX delimiters for math parts if needed, 
    # but plain text with latex inside strings is fine per instructions ("use formal LaTeX delimiters").
    poly_str = f"{a}x^2 + {b}x + {c}"
    
    return_dict = {
        "question_text": (f"Determine the roots and factorization of the quadratic polynomial defined by coefficients: $\\{poly_str}$." ),
        "correct_answer": {
            "roots": [sorted_roots[0], sorted_roots[1]], # List of Fractions or strings? 
                     # Task says "Exact arithmetic; no floats". Usually implies Fraction objects or string representations.
                     # Given the context of 'latex', maybe strings are safer for display, but list usually expects values.
                     # Let's provide Fraction objects as they represent exact roots perfectly in Python.
            "factorization_latex": factorization_latex, 
            "roots_latex": roots_latex
        },
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }

# Fix: The previous code block had a syntax error in the thought process regarding variable scope and imports inside function.
# Re-writing cleanly without errors.

def generate(level=1, **kwargs):
    from math import gcd as _gcd
    from fractions import Fraction
    
    quadratic_coefficients = [1, 4, -12]
    
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b * b - 4 * a * c
    sqrt_discriminant_int = int(discriminant ** 0.5)
    
    root1_num = -b + sqrt_discriminant_int
    root1_denom = 2 * a
    
    root2_num = -b - sqrt_discriminant_int
    root2_denom = 2 * a
    
    r1 = Fraction(root1_num, root1_denom)
    r2 = Fraction(root2_num, root2_denom)
    
    sorted_roots = sorted([r1, r2])
    
    def format_latex_frac(frac):
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            # Ensure sign is handled in numerator for cleaner LaTeX usually, 
            # but standard fraction handles it. Let's keep simple.
            num_str = f"{frac.numerator}"
            den_str = f"{{{frac.denominator}}}"
            return f"\\frac{{{num_str}}}{{{{{den_str}}}}}"

    r1_latex_val = format_latex_frac(sorted_roots[0])
    r2_latex_val = format_latex_frac(sorted_roots[1])
    
    roots_latex = f"\\left( {r1_latex_val} \\right), \\left( {r2_latex_val} \\right)"
    
    # Factorization: a(x - r1)(x - r2)
    term1 = f"x-{format_latex_frac(sorted_roots[0])}" if sorted_roots[0].numerator > 0 else f"x+{abs(format_latex_frac(Fraction(-sorted_roots[0])))}" # Simplified logic below
    
    # Better approach for factor latex: just use x - r
    def make_factor_term(r):
        val = format_latex_frac(r)
        return f"\\left(x-{val}\\right)"

    term1 = make_factor_term(sorted_roots[0])
    term2 = make_factor_term(sorted_roots[1])
    
    factorization_latex = f"{a}{term1}{term2}"
    
    poly_str = f"{a}x^2 + {b}x + {c}"
    
    return_dict = {
        "question_text": (f"Determine the roots and factorization of the quadratic polynomial defined by coefficients: $\\{poly_str}$." ),
        "correct_answer": {
            "roots": sorted_roots, 
            "factorization_latex": factorization_latex, 
            "roots_latex": roots_latex
        },
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }

# Wait, the previous thought block had a function definition inside another. I need to output ONLY ONE valid Python source file content starting with def generate...
# The logic above is correct but needs to be in one clean block without comments that break syntax if not careful. 
# Also, ensure `sorted_roots` contains Fraction objects for "Exact arithmetic".

def generate(level=1, **kwargs):
    from math import gcd as _gcd
    from fractions import Fraction
    
    quadratic_coefficients = [1, 4, -12]
    
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b * b - 4 * a * c
    sqrt_discriminant_int = int(discriminant ** 0.5)
    
    root1_num = -b + sqrt_discriminant_int
    root1_denom = 2 * a
    
    root2_num = -b - sqrt_discriminant_int
    root2_denom = 2 * a
    
    r1 = Fraction(root1_num, root1_denom)
    r2 = Fraction(root2_num, root2_denom)
    
    sorted_roots = sorted([r1, r2])
    
    def format_latex_frac(frac):
        if frac.denominator == 1:
            return str(frac.numerator)
        else:
            num_str = f"{frac.numerator}"
            den_str = f"{{{frac.denominator}}}"
            return f"\\frac{{{num_str}}}{{{{{den_str}}}}}"

    r1_latex_val = format_latex_frac(sorted_roots[0])
    r2_latex_val = format_latex_frac(sorted_roots[1])
    
    roots_latex = f"\\left( {r1_latex_val} \\right), \\left( {r2_latex_val} \\right)"
    
    def make_factor_term(r):
        val = format_latex_frac(r)
        return f"\\left(x-{val}\\right)"

    term1 = make_factor_term(sorted_roots[0])
    term2 = make_factor_term(sorted_roots[1])
    
    factorization_latex = f"{a}{term1}{term2}"
    
    poly_str = f"{a}x^2 + {b}x + {c}"
    
    return_dict = {
        "question_text": (f"Determine the roots and factorization of the quadratic polynomial defined by coefficients: $\\{poly_str}$." ),
        "correct_answer": {
            "roots": sorted_roots, 
            "factorization_latex": factorization_latex, 
            "roots_latex": roots_latex
        },
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }