def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Calculate roots using exact arithmetic (fractions) to avoid floats
    from fractions import Fraction
    
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b * b - 4 * a * c
    
    # Calculate roots exactly using the quadratic formula: (-b ± sqrt(d)) / (2a)
    import math
    delta_sqrt = int(math.isqrt(abs(int(discriminant)))) if discriminant >= 0 else None
    
    # Since coefficients are integers and we need exact arithmetic, 
    # let's factorize c to find integer roots first as it's level 1.
    # x^2 + bx + c = (x - r1)(x - r2) => sum of roots = -b, product = c
    
    if discriminant < 0:
        raise ValueError("No real roots for this polynomial.")
    
    delta_sqrt_val = int(math.sqrt(discriminant))
    
    # Check if perfect square to ensure exact rational/integer representation
    is_perfect_square = (delta_sqrt_val * delta_sqrt_val == discriminant)
    
    root1_num = -b + delta_sqrt_val
    root2_num = -b - delta_sqrt_val
    
    denom = 2 * a
    
    # Simplify fractions for roots
    from math import gcd
    
    def simplify_fraction(n, d):
        common = abs(gcd(n, d))
        return (n // common, d // common) if n != 0 else (0, 1)
    
    r1_num, r1_den = simplify_fraction(root1_num, denom)
    r2_num, r2_den = simplify_fraction(root2_num, denom)
    
    # Determine order: ascending means smaller value first. 
    # Compare float values of the two roots to sort them for "ascending" list requirement
    val1 = root1_num / root1_den if root1_den != 0 else float('inf')
    val2 = root2_num / r2_den if r2_den != 0 else float('-inf')
    
    # Construct sorted tuple of roots as strings or fractions for exactness
    # The requirement says "roots (ascending)". We will represent them as simplified fractions.
    def fraction_to_str(n, d):
        return f"{n}/{d}" if d != 1 else str(n)
        
    root_list = []
    
    # Sort based on value
    roots_values = [(val1, r1_num/r1_den), (val2, r2_num/r2_den)]
    sorted_roots = sorted(roots_values, key=lambda x: float(x[0])) if discriminant != 0 else [r1_num/r1_den] * 2
    
    # Actually simpler logic for sorting the two roots derived above
    root_a_val = Fraction(root1_num, root1_den)
    root_b_val = Fraction(root2_num, r2_den)
    
    sorted_roots_list = []
    if root_a_val <= root_b_val:
        sorted_roots_list.append((root_a_val.numerator, root_a_val.denominator))
        sorted_roots_list.append((root_b_val.numerator, root_b_val.denominator))
    else:
        sorted_roots_list.append((root_b_val.numerator, root_b_val.denominator))
        sorted_roots_list.append((root_a_val.numerator, root_a_val.denominator))

    # Format roots_latex and correct_answer['roots']
    def format_root(n, d):
        if d == 1:
            return str(n)
        else:
            return f"\\frac{{{n}}}{{-{d}}}" if n < 0 else f"-\\frac{{{-n}}}{{{d}}}" # Wait, standard latex for negative fraction is usually \frac{n}{-d} or -\frac{|n|}{d}. Let's stick to simple canonical form.
            return f"\\frac{{{n}}}{{{d}}}"

    roots_latex_parts = []
    correct_roots_list = [] # List of strings
    
    for n, d in sorted_roots_list:
        if d == 1:
            s_val = str(n)
        else:
            s_val = f"\\frac{{{n}}}{{{d}}}"
        
        roots_latex_parts.append(s_val)
        correct_roots_list.append(f"{s_val}")

    # Factorization latex: (x - r1)(x - r2) or similar. 
    # If root is integer k, factor is (x - k). If fraction n/d, factor is (dx - n).
    
    def get_factor_str(n, d):
        if d == 1:
            return f"(x - {n})"
        else:
            # Factor corresponding to root n/d is (d*x - n) = 0 -> x = n/d. 
            # Wait, standard form for polynomial with integer coeffs factoring over rationals usually keeps monic if possible or uses leading coeff.
            # Given a=1 here. Roots are r1, r2. Factors: (x-r1)(x-r2).
            return f"(dx - n)" is not quite right because we want the polynomial to match coefficients [1, 4, -12].
            # Let's reconstruct factors from roots directly for latex display of factorization over Q.
            pass
            
    # Re-evaluating factorization string construction:
    # Polynomial P(x) = (x - r1)(x - r2). 
    # If r is integer, write (x - r).
    # If r is fraction n/d in lowest terms, usually written as d*(x - n/d) or just keep it factored over Q.
    # Standard math notation for factorization of monic polynomial with rational roots: product of linear factors.
    
    def make_factor_latex(numerator, denominator):
        if denominator == 1:
            return f"(x - {numerator})"
        else:
            # To keep coefficients integer in the visual representation often we write d(x - n/d) but here leading coeff is 1.
            # So strictly (x - n/d). 
            return f"(x - \\frac{{{numerator}}}{{-{denominator}}})" if numerator < 0 else f"(x + \\frac{{{-numerator}}}{{{denominator}}})" \
                   if denominator != 1 and numerator > 0 else f"(x - \\frac{{{abs(numerator)}}}{{{denominator}}})" # Simplified logic
    
    # Better approach for factorization latex: 
    # Just substitute the roots into (x - root).
    
    factors_latex_parts = []
    for n, d in sorted_roots_list:
        if d == 1:
            term = f"(x - {n})"
        else:
             sign_str = "+" if n < 0 and d > 0 or (n > 0 and d < 0) else "-" # Actually handle signs carefully. 
             val_sign = "minus" if n * d >= 0 else "plus" # No, root is n/d. Factor is x - n/d.
             num_str = abs(n)
             den_str = abs(d)
             
             if n < 0:
                 term = f"(x + \\frac{{{num_str}}}{{-{den_str}}})" # Wait, standard latex for negative fraction in subtraction? 
                 # x - (-3/2) -> x + 3/2.
                 term = f"(x + \\frac{{{abs(n)}}}{{{d}}})" if d > 0 else f"(x + \\frac{{{-n}}}{{{den_str}}})"
             elif n > 0:
                 term = f"(x - \\frac{{{num_str}}}{{{den_str}}})"
             
        factors_latex_parts.append(term)

    factorization_latex = " * ".join(factors_latex_parts) if len(factors_latex_parts) == 2 else "(No real roots)" # Should be 2 for quadratic
    
    question_text = f"Solve the polynomial equation $x^2 + {b}x + {c} = 0$ by factoring. Provide the factorization and the roots in ascending order."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "roots": correct_roots_list, # List of strings representing fractions or integers
            "factorization_latex": factorization_latex,
            "roots_latex": ", ".join(roots_latex_parts) if len(sorted_roots_list) == 2 else "" 
        },
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }