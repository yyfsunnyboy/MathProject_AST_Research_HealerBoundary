def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Calculate roots using exact arithmetic (fractions) to avoid floats
    from fractions import Fraction
    
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b*b - 4*a*c
    sqrt_discriminant_int = int(discriminant**0.5) if (sqrt_disc := float(discriminant)**0.5).is_integer() else None
    
    # Since coefficients are integers and we need exact roots, check for perfect square discriminant
    import math
    delta_sq = b*b - 4*a*c
    sqrt_delta = int(math.isqrt(delta_sq)) if (sqrt_delta * sqrt_delta == delta_sq) else None
    
    if sqrt_delta is not None:
        root1_num = (-b + sqrt_delta)
        root2_num = (-b - sqrt_delta)
        
        # Simplify fractions for roots
        def simplify_fraction(n):
            from math import gcd
            g = abs(gcd(a, n))  # Actually we need to divide by a first conceptually, but let's do standard fraction reduction
            if n == 0: return Fraction(0)
            
            # The root is (-b +/- sqrt(delta)) / (2a)
            num1 = -b + sqrt_delta
            den1 = 2 * a
            
            g1 = abs(gcd(num1, den1))
            simplified_num1 = num1 // g1
            simplified_den1 = den1 // g1
            
            if simplified_den1 == 1:
                return Fraction(simplified_num1)
            
            # For the second root
            num2 = -b - sqrt_delta
            g2 = abs(gcd(num2, den1))
            simplified_num2 = num2 // g2
            simplified_den2 = den1 // g2
            
            if simplified_den2 == 1:
                return Fraction(simplified_num2)
                
        root1 = simplify_fraction(root1_num) # This logic is slightly flawed above for separate calls, let's redo cleanly
        
    # Redo calculation cleanly with Fractions
    from fractions import Fraction
    
    delta_sq_val = b*b - 4*a*c
    sqrt_delta_val = int(delta_sq_val**0.5) if (sqrt_d := float(delta_sq_val)**0.5).is_integer() else None
    
    roots_list = []
    
    if sqrt_delta_val is not None:
        # Roots are (-b +/- sqrt(d)) / 2a
        numerator1 = -b + sqrt_delta_val
        denominator_common = 2 * a
        
        root1_frac = Fraction(numerator1, denominator_common)
        roots_list.append(root1_frac.numerator if root1_frac.denominator == 1 else f"{root1_frac.numerator}/{root1_frac.denominator}") # Store string representation for latex? No, store value. But correct_answer needs specific format.
        
        numerator2 = -b - sqrt_delta_val
        root2_frac = Fraction(numerator2, denominator_common)
        roots_list.append(root2_frac.numerator if root2_frac.denominator == 1 else f"{root2_frac.numerator}/{root2_frac.denominator}")
        
    # Sort roots ascending (numerical value comparison for sorting strings representing fractions is tricky, convert to float for sort key then map back? Or just compare Fraction objects)
    # We need the list of root values. Let's store as Fractions first.
    
    if sqrt_delta_val:
        r1 = Fraction(-b + sqrt_delta_val, 2*a)
        r2 = Fraction(-b - sqrt_delta_val, 2*a)
        
        sorted_roots = [min(r1, r2), max(r1, r2)] # Fractions support comparison
        
    else:
        # Complex roots? Task says difficulty level 1, usually implies real. 
        # If discriminant < 0, handle complex or assume valid input for L1.
        # Given frozen params [1, 4, -12], delta = 16 + 48 = 64 > 0. Real roots exist.
        sorted_roots = []

    # Format roots_latex and correct_answer.roots (ascending)
    def format_root(r):
        if r.denominator == 1:
            return str(r.numerator)
        else:
            return f"{r.numerator}/{r.denominator}"
            
    sorted_roots_str = [format_root(root) for root in sorted_roots]
    
    # Factorization: a(x - r1)(x - r2). Note roots are values. Factors are (ax + b +/- ...)? 
    # Standard factorization over rationals/integers usually looks like 1*(x - r1)*(x - r2) if monic, or scaled.
    # Since leading coeff is 1: (x - root1)(x - root2).
    # If roots are fractions p/q and u/v? 
    # Actually for integer coefficients, factors are usually linear terms with integer coeffs like (qx + p).
    # Let's construct factorization string.
    
    r1 = sorted_roots[0]
    r2 = sorted_roots[1]
    
    term1_num = -r1.numerator if r1.denominator == 1 else (-r1.numerator, r1.denominator)
    # Better approach for factorization string: (den*x + num)(other_den*x + other_num)? 
    # No, standard form is usually monic factors if possible or integer coefficients.
    # For x^2 + 4x - 12 = (x+6)(x-2). Roots are -6 and 2.
    
    # Let's reconstruct the linear factors from roots directly for LaTeX display: (x - r)
    def get_factor_latex(r):
        if r.denominator == 1:
            val = r.numerator
            sign = "+" if val < 0 else "-" if val > 0 else ""
            term_val = abs(val)
            return f"(x {sign} {term_val})" if (val != 0 and not (r==Fraction(0))) else "(x)" # Handle zero root case separately? 
            # Actually simpler: x - (-6) -> x + 6. x - (2) -> x - 2.
            return f"(x {'' if val == 0 else ('+' if val < 0 else '-')} {abs(val)})"
        else:
            # Fractional root p/q => factor is (qx - p). Root = p/q. Factor (q*x - p) or (-q*x + p)? 
            # If x^2+4x-12, roots are integers here.
            pass
            
    if r1.denominator == 1 and r2.denominator == 1:
        f1_str = f"(x {'' if r1.numerator==0 else ('+' if r1.numerator<0 else '-')} {abs(r1.numerator)})"
        f2_str = f"(x {'' if r2.numerator==0 else ('+' if r2.numerator<0 else '-')} {abs(r2.numerator)})"
    else:
        # General case for fractions p/q (root) -> factor is (q*x - p). 
        # Check sign. If root = 1/3, x=1/3 => 3x-1=0. Factor (3x-1).
        f1_str = f"({r1.denominator}*x {'' if r1.numerator==0 else ('+' if -r1.numerator>=0 and r1.numerator!=0 else '')} {-r1.numerator})" # Logic check: root=2 => 1*x-2. num=2, den=1. -> (1*x + (-2))
        f2_str = f"({r2.denominator}*x {'' if r2.numerator==0 else ('+' if -r2.numerator>=0 and r2.numerator!=0 else '')} {-r2.numerator})"
        
    factorization_latex = f"{a}{f1_str}{f2_str}" # a is 1 here. If not monic, need to distribute? 
    # Usually for "factor_roots", we want the product form. Since a=1 in frozen params:
    
    question_text = (
        r"Given the quadratic polynomial $x^2 + bx + c$ with coefficients from the set $\{a,b,c\} = \{" + str(quadratic_coefficients) + "}\$, find its roots and factorization."
    ) # Wait, need to use actual values in text.
    
    b_val = quadratic_coefficients[1]
    c_val = quadratic_coefficients[2]
    
    question_text = (
        r"Find the roots of the polynomial $x^{" + str(b_val) + "}" + f"x {'' if b_val==0 else ('+' if b_val>0 else '')} {b_val})$" 
        + f"+{c_val}$ and its factorization."
    ) # Simplified text generation. Let's make it robust.
    
    poly_str = f"x^2 {'+ ' if c_val>=0 else ''}{abs(c_val)} x {'+' if b_val>0 else '-'} {b_val}" 
    # Wait, standard form ax^2 + bx + c. Here a=1.
    term_b = ""
    sign_b = "+"
    val_b = abs(b_val)
    if b_val < 0:
        sign_b = "-"
        val_b = -b_val
    
    poly_str = f"x^2 {sign_b} {val_b}x" + (f"+{c_val}" if c_val >= 0 else "") # If c is negative, handled by logic? 
    # Let's just build the string carefully.
    
    term_c_sign = "+"
    term_c_abs = abs(c_val)
    if c_val < 0:
        term_c_sign = "-"
        
    poly_str = f"x^2 {'+' if b_val>=0 else ''}{b_val}x {term_c_sign}{c_val}" # This is getting messy. 
    # Let's just use the coefficients directly in a readable way or standard math notation.
    
    final_poly_text = (f"Find the roots and factorization of $x^2 {'+' if b_val>=0 else ''}{b_val}x {'' if c_val==0 else ('+' if c_val>0 else '')}{c_val}$.")

    correct_answer_dict = {
        "roots": sorted_roots_str, # List of strings representing roots ascending
        "factorization_latex": f"{a}*{f1_str}*{f2_str}", 
        "roots_latex": ", ".join(sorted_roots_str)
    }
    
    return {
        "question_text": final_poly_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }