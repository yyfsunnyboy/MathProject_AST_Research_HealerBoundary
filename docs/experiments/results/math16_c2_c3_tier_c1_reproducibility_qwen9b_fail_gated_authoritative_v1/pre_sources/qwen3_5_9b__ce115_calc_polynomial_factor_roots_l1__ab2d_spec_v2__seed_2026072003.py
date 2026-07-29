# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per specification
    quadratic_coefficients = [1, 4, -12]
    
    a, b, c = quadratic_coefficients
    
    # Compute discriminant using native Python arithmetic
    delta = b * b - 4 * a * c
    
    # Compute roots exactly. Since coefficients are integers and delta is perfect square (64),
    # we can compute integer roots directly to avoid floats.
    sqrt_delta = int(delta ** 0.5)
    
    root1_num = -b + sqrt_delta
    root2_num = -b - sqrt_delta
    
    denom = 2 * a
    
    # Calculate exact rational roots as tuples (numerator, denominator) for JSON serialization
    if denom != 0:
        r1_numerator = root1_num // denom
        r1_denominator = denom // gcd(abs(root1_num), abs(denom))
        
        r2_numerator = root2_num // denom
        r2_denominator = denom // gcd(abs(root2_num), abs(denom))
    else:
        # Should not happen for quadratic with a=1, but handled safely
        r1_numerator, r1_denominator = 0, 1
        r2_numerator, r2_denominator = 0, 1

    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x
    
    # Normalize fractions to ensure canonical representation (positive denominator)
    if r1_denominator < 0:
        r1_numerator = -r1_numerator
        r1_denominator = -r1_denominator
        
    if r2_denominator < 0:
        r2_numerator = -r2_numerator
        r2_denominator = -r2_denominator

    # Determine ascending order based on float value of the rational numbers for sorting,
    # but store exact rationals. Since we need to return a list in correct_answer['roots'],
    # and JSON doesn't support tuples well as distinct objects without custom encoding,
    # we will represent roots as strings "num/den" or just integers if den=1.
    
    def format_root(n, d):
        if d == 1:
            return str(n)
        else:
            return f"{n}/{d}"

    root_str_1 = format_root(r1_numerator, r1_denominator)
    root_str_2 = format_root(r2_numerator, r2_denominator)

    # Sort roots in ascending order for the final list representation
    val1 = float(root_str_1.replace('/', ' ').split()[0]) if '/' in root_str_1 else int(root_str_1)
    val2 = float(root_str_2.replace('/', ' ').split()[0]) if '/' in root_str_2 else int(root_str_2)

    # Re-evaluate sorting logic properly using cross-multiplication to avoid floats for comparison
    def compare_roots(n1, d1, n2, d2):
        return (n1 * d2) - (n2 * d1)

    if compare_roots(r1_numerator, r1_denominator, r2_numerator, r2_denominator) > 0:
        sorted_root_strs = [root_str_2, root_str_1]
        sorted_rational_pairs = [(r2_numerator, r2_denominator), (r1_numerator, r1_denominator)]
    else:
        sorted_root_strs = [root_str_1, root_str_2]
        sorted_rational_pairs = [(r1_numerator, r1_denominator), (r2_numerator, r2_denominator)]

    # Construct LaTeX for factorization: a(x - r1)(x - r2) -> 1*(x - (-3))(x - 4) => (x+3)(x-4)
    # Roots are integers here: x = -6/2 = -3, x = 8/2 = 4. Wait calculation check:
    # b=4, c=-12. delta = 16 - 4(1)(-12) = 16 + 48 = 64. sqrt=8.
    # r1 = (-4+8)/2 = 2. r2 = (-4-8)/2 = -6.
    # Roots are 2 and -6. Ascending: -6, 2.
    
    # Re-calculate specific values for this frozen set to ensure correctness in text generation logic above was generic but needs instantiation here? 
    # No, the code must compute it dynamically based on quadratic_coefficients passed as frozen constant inside function scope or derived from kwargs if allowed (but spec says do not read from kwargs).
    # The spec says "Frozen sampled parameters: {"quadratic_coefficients": [1, 4, -12]}". 
    # My code defines this variable directly. It works for any quadratic with integer roots ideally, but handles rationals too.

    r_asc_0 = sorted_rational_pairs[0]
    r_asc_1 = sorted_rational_pairs[1]

    root_latex_list = [format_root(r_asc_0[0], r_asc_0[1]), format_root(r_asc_1[0], r_asc_1[1])]
    
    # Factorization LaTeX: (x - r1)(x - r2) where r are the roots found.
    # If root is integer k, term is "(x-{k})". If rational p/q, usually written as "q(x-p/q)" or just standard form? 
    # Standard factorization for ax^2+bx+c = a(x-r1)(x-r2). Here a=1.
    # Term construction: if root r = n/d, term is (d*x - n) / d ? No, usually we keep monic factors if possible or just list roots.
    # Task asks for "factorization_latex". For x^2 + 4x - 12 = (x+3)(x-6)? 
    # Wait my manual calc: r = (-b +/- sqrt)/2a = (-4 +/- 8)/2 -> 4/2=2, -12/2=-6.
    # Factors are (x-2) and (x+6). Product is x^2 + 4x - 12. Correct.
    
    def make_factor_term(n, d):
        if d == 1:
            return f"(x-{n})"
        else:
            # For rational roots p/q with a=1, factor is (qx-p). 
            # Example: root -3/2 -> (-2)x + 3? No. x = -3/2 => 2x+3=0 => (2x+3)
            return f"({d}*x-{n})"

    term1 = make_factor_term(r_asc_0[0], r_asc_0[1]) # Note: order in factorization doesn't strictly matter but usually sorted or by appearance. 
    term2 = make_factor_term(r_asc_1[0], r_asc_1[1])
    
    # Actually, standard form often lists factors corresponding to roots found. Order of multiplication is commutative.
    # Let's just use the ascending order for consistency if needed, or arbitrary. Commutative property holds.
    factorization_latex = f"{term1} {term2}"

    question_text = r"Given the quadratic polynomial $x^2 + 4x - 12$, find its roots and express them in a list sorted in ascending order."
    
    # Construct correct_answer dict with exact types: 
    # 'roots': list of strings representing rational numbers (e.g., "-6", "2") or formatted fractions.
    # 'factorization_latex': string
    # 'roots_latex': list of LaTeX representations
    
    roots_list = root_latex_list
    roots_latex_str = f"${root_latex_list[0]}, ${root_latex_list[1]}$"

    correct_answer = {
        "roots": roots_list,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex_str
    }

    oracle_payload = {"quadratic_coefficients": [1, 4, -12]}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }