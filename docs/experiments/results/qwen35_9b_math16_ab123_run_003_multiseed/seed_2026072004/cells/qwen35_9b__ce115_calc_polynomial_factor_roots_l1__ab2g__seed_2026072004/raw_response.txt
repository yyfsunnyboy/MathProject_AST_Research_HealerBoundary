def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Solve x^2 + 4x - 12 = 0 using exact arithmetic (integers)
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    discriminant = b*b - 4*a*c
    
    # Roots calculation: (-b ± sqrt(discriminant)) / (2a)
    root_diff_part = int((discriminant ** 0.5)) if (int(root := ((-b + root_diff_part) // (2 * a))) == (-b + root_diff_part) / (2 * a)) else None
    
    # Re-calculate roots safely for exact integer representation
    sqrt_d = discriminant ** 0.5
    r1_num = -b + int(sqrt_d)
    r1_denom = 2 * a
    r2_num = -b - int(sqrt_d)
    
    # Construct simplified fractions or integers as appropriate
    def simplify_fraction(n, d):
        if n == 0: return "0"
        common_divisor = abs(d)
        while True:
            try:
                if (n % common_divisor) != 0 and (d % common_divisor) != 0: break 
                # This logic is flawed for arbitrary integers without GCD. Let's use Euclidean algorithm.
                pass 
            except ZeroDivisionError: break
        
        import math
        gcd_val = math.gcd(n, d)
        return f"{n // gcd_val}/{d // gcd_val}" if abs(d) != 1 else str(n // gcd_val)

    r1_simplified = simplify_fraction(r1_num, r2_denom) # Placeholder logic fixed below in final code block thought process
    
    # Correct exact arithmetic implementation
    import math
    
    sqrt_d_int = int(math.isqrt(discriminant)) if discriminant >= 0 else None
    
    def to_str_frac(n, d):
        g = math.gcd(n, d)
        n //= g
        d //= g
        return f"{n}/{d}" if d != 1 else str(n)

    r1_numerator = -b + sqrt_d_int
    r2_numerator = -b - sqrt_d_int
    
    root1_str = to_str_frac(r1_numerator, 2 * a)
    root2_str = to_str_frac(r2_numerator, 2 * a)
    
    # Ensure ascending order for the list of roots string representation
    r_list = [root1_str, root2_str]
    if float(root1_str.split('/')[0]) > float(root2_str.split('/')[0]):
        r_list.reverse()
        
    correct_roots_tuple = tuple(r_list)
    
    # Factorization: a(x - r1)(x - r2). Since roots might be fractions, we express factors carefully.
    # However, for standard school math context with integer coefficients and discriminant perfect square (here 64), 
    # the form is usually written as leading_coeff * (x + b/2a +/- sqrt...).
    # Or simply finding linear factors over rationals: a(x - r1)(x - r2).
    
    # Let's construct the factorization string.
    # The polynomial is x^2 + 4x - 12 = (x + 6)(x - 2)
    # Roots are -6, 2. Ascending: [-6, 2].
    
    final_roots_str_list = sorted([root1_str, root2_str], key=lambda s: float(s.split('/')[0]))
    
    factorization_latex = f"{quadratic_coefficients[0]}\\left(x-{final_roots_str_list[0]}.split('-')[1])right)({quadratic_coefficients[0]}x+{b})" # This manual construction is error prone. 
    # Let's build it logically:
    
    if discriminant == 0:
        root_val = to_str_frac(-b, 2*a)
        factorization_latex = f"{a}(x - {root_val})(x - {root_val})"
    else:
        r1_simpl_n, r1_simpl_d = int(root_diff_part), 1 # Re-eval properly
        
        # Proper calculation for roots of x^2+4x-12=0 -> (b±sqrt(d))/(-2a) ?? No. (-b ± sqrt)/2a
        # b=-4, -b=4. d=64, sqrt=8. Roots: (4+8)/2 = 6? Wait equation is x^2 + bx + c. 
        # Here coeffs are [1, 4, -12]. a=1, b=4, c=-12.
        # Discriminant = 16 - 4(1)(-12) = 16+48 = 64. sqrt=8.
        # Roots: (-4 ± 8)/2 => (4/2)=2 and (-12/2)=-6.
        
    r_val_1_num = -b + int(math.isqrt(discriminant))
    r_val_2_num = -b - int(math.isqrt(discriminant))
    
    root_str_1 = to_str_frac(r_val_1_num, 2*a)
    root_str_2 = to_str_frac(r_val_2_num, 2*a)
    
    sorted_roots = [root_str_1, root_str_2]
    if float(root_str_1.split('/')[0]) > float(root_str_2.split('/')[0]):
        sorted_roots.reverse()
        
    roots_latex = f"[{sorted_roots[0]}, {sorted_roots[1]}]"
    
    # Factorization logic for x^2+bx+c where discriminant is square:
    # (x - r1)(x - r2) if monic. If not, a(x-r1)(x-r2).
    factorization_latex = f"{a}\\left(x-{sorted_roots[0]}\\right){''if abs(a)==1 else ''}" + "\\cdot \\left(" \
                          f" {int( (b - int(math.isqrt(discriminant)) ) / a} " 
                          if False else "" # Simplified logic for monic case mostly, but general form needed.
    
    # Correct factorization string construction:
    # We need to represent the linear factors exactly.
    # Factor 1: (x - r1) where r1 is root_str_1
    # Factor 2: (a*x + b + sqrt_d)/a ? No, just plug roots in monic form if possible or adjust constant.
    
    # Let's stick to the simplest exact representation for this specific task type usually expected:
    # "x - r1" and "x - r2". If leading coeff != 1, we factor it out or distribute? 
    # Usually (ax + c)(dx + e).
    # For [1, 4, -12]: Roots are integers. Factors are (x-2) and (x+6).
    
    if a == 1:
        f_latex = f"\\left(x-{sorted_roots[0]}\\right) \\cdot \\left(x-{sorted_roots[1]}\\right)" # Wait, roots are numbers. 
        # r_str_1 is "2", so (x-2). r_str_2 is "-6". So (x - (-6)) = (x+6).
        # My to_str_frac returns string like "2" or "-6".
        # The LaTeX should be x - root. If root is negative, it becomes +ve term automatically? 
        # No: latex(x - (-6)) -> x + 6.
        
    # Reconstructing the factorization string precisely for generic quadratic ax^2+bx+c with integer roots r1, r2:
    # It factors as a*(x-r1)*(x-r2). But typically we write (ax+b)(cx+d) or similar if coefficients allow integers.
    # Given the constraints and "Exact arithmetic", let's format it cleanly.
    
    term1 = f"x - {sorted_roots[0]}"
    term2 = f"x - {sorted_roots[1]}"
    factorization_latex = f"{a} \\cdot ({term1}) \\cdot ({term2})" # Might be overkill, but safe for non-monic. 
    if a == 1:
        factorization_latex = term1 + " \\cdot " + term2
        
    correct_answer_dict = {
        "roots": sorted_roots,
        "factorization_latex": factorization_latex.replace("\\left(", "\\left(").replace("\\right)", ")").replace("\\cdot", "\\cdot"), # Just formatting checks
        "roots_latex": roots_latex 
    }
    
    return {
        "question_text": f"Find the roots of $x^2 + 4x - 12 = 0$ and provide its factorization.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }