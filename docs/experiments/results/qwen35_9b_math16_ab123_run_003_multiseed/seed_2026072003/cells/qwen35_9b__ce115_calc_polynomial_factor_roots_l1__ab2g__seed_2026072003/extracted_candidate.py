def generate(level=1, **kwargs):
    # Frozen sampled parameters for this specific instance
    quadratic_coefficients = [1, 4, -12]
    
    # Parse coefficients: ax^2 + bx + c
    a = quadratic_coefficients[0]
    b = quadratic_coefficients[1]
    c = quadratic_coefficients[2]
    
    # Calculate discriminant and roots using exact arithmetic (fractions)
    from fractions import Fraction
    
    discriminant_val = b * b - 4 * a * c
    
    if discriminant_val < 0:
        raise ValueError("No real roots for the given coefficients.")
        
    sqrt_discriminant = int(discriminant_val ** 0.5)
    
    # Roots formula: (-b ± sqrt(D)) / (2a)
    root1_num = -b + sqrt_discriminant
    root2_num = -b - sqrt_discriminant
    
    denom = 2 * a
    
    # Construct Fraction objects for exact roots
    if denom == 0:
        raise ValueError("Coefficient 'a' cannot be zero.")
        
    root1_frac = Fraction(root1_num, denom)
    root2_frac = Fraction(root2_num, denom)
    
    # Ensure ascending order of roots (compare values)
    if float(root1_frac) > float(root2_frac):
        sorted_roots_list = [root2_frac, root1_frac]
    else:
        sorted_roots_list = [root1_frac, root2_frac]
        
    # Format factorization latex: a(x - r1)(x - r2) -> simplified if possible
    # We need to represent roots as fractions in LaTeX. 
    # Factor form: (ax + b')(cx + d') or k*(x-r1)*(x-r2). Let's use standard factored form with integer coefficients inside.
    
    def simplify_factor(num, den):
        """Returns simplified factor string for term 'den*x - num' if root is num/den"""
        common = 0
        n_abs = abs(int(num))
        d_abs = int(den)
        
        # Handle negative signs carefully
        sign_num = '-' if num < 0 else '+'
        sign_den = '-' if den < 0 else ''
        
        val_str = f"{sign_num}{n_abs}/{d_abs}" if n_abs != 1 and d_abs > 1 else (f"±{n_abs}" if d_abs == 1 else f"x") # Simplified logic below
        
        # Actually, let's construct the polynomial factors directly:
        # Root r = p/q. Factor is (q*x - p).
        
    root1_p = int(root1_frac.numerator)
    root1_q = abs(int(root1_frac.denominator))
    
    root2_p = int(root2_frac.numerator)
    root2_q = abs(int(root2_frac.denominator))
    
    # Construct LaTeX for roots: \frac{p}{q} -> p/q or just integer if q=1
    def format_root_latex(p, q):
        if q == 1:
            return f"{int(p)}"
        else:
            return rf"\frac{{{p}}}{{{q}}}"

    roots_latex_str = f"[{format_root_latex(root1_p, root1_q)}, {format_root_latex(root2_p, root2_q)}]"
    
    # Construct factorization LaTeX. 
    # The polynomial is a(x - r1)(x - r2). 
    # To avoid fractions in factors: (root1.q * x + (-root1.p)) and (root2.q * x + (-root2.p)).
    # Note: root = p/q implies factor (q*x - p). If q is negative, adjust signs. We used abs(q) above for latex but Fraction handles sign in numerator usually? 
    # Let's stick to the definition: if r = num/den, factor is den*x + (-num).
    
    f1_term_num = int(root2_frac.numerator) * root1_q - 0 # Wait, logic check.
    # Root r implies (x - r) -> x - p/q -> q*x - p.
    # We need to ensure the product equals a*(q1*x-p1)*(q2*x-p2). 
    # Let's just output the standard form: factorization_latex = rf"\left({root1_q}x {sign_op1}{abs(root1_p)}\right)\left({root2_q}x {sign_op2}{abs(root2_p)}\right)"
    
    def get_factor_str(p, q):
        # p is numerator of root (can be negative), q is denominator (always positive in Fraction usually? No, keep sign logic)
        # We want factor: qx - p. 
        # If p is negative (-5), then qx - (-5) = qx + 5.
        if p == 0:
            return f"{q}x"
        
        term_sign = "+" if (p < 0 and q > 0) or (p >= 0 and q < 0) else "-" # Wait, standard is x - r. If r=-2, factor is x+2. 
        # Root p/q. Factor: qx - p.
        
        val_sign = "+" if (q * (-1)) + (-p) > 0 else "" # No, let's just compute the sign of the constant term in 'qx +/- |c|'
        
        const_val = abs(p)
        
        # Determine operator between x and constant
        # Factor is qx - p. 
        if q < 1: # Should not happen with integer inputs usually but safe to handle
             pass
        
        # Standard form: (den*x + num') where root is -num'/den? No, roots are (-b +/- ...)/2a.
        # Let's rebuild cleanly.
        
    # Re-calculate specific factor strings for this instance logic
    r1_num = int(root1_frac.numerator)
    r1_den = abs(int(root1_frac.denominator))
    
    r2_num = int(root2_frac.numerator)
    r2_den = abs(int(root2_frac.denominator))
    
    # Factor 1: (r1_den * x - r1_num) -> if r1_num is negative, it becomes + 
    sign_r1 = "-" if r1_num > 0 else "+"
    term_r1_const = str(abs(r1_num)) if abs(r1_num) != 1 or False else "" # Keep simple
    
    def mk_factor(n):
        q = n[0] # numerator? No, let's use the tuple (num, den) from Fraction directly
        
    # Simpler approach for latex: 
    # Root r. Factor is written as (den*x - num). If num < 0, it becomes + abs(num)*x ... wait.
    # Example: root = 2/3 -> factor (3x - 2). root = -1/2 -> factor (2x + 1) because x - (-1/2) = x+1/2 -> 2x+1 scaled? 
    # Actually, if we write factors as integers to match 'a', we need:
    # P(x) = a * (r1_den*x - r1_num) / r1_den * ... No.
    
    # Let's just output the mathematical factorization over rationals or integer scaled ones? 
    # Usually "factorization" implies linear factors with leading coeff distributed if possible, but for exactness:
    # We will provide (qx + c)(rx + d) such that product is a*x^2+bx+c.
    
    # Since roots are p/q and r/s, P(x) = a * (x - p/q) * (x - r/s) 
    #       = (a/qs) * (qx - p) * (sx - r).
    # To make integer coefficients: let K = qs. Then factorization is K*(...) or distribute 'a'.
    # However, the prompt asks for "factorization_latex". Common format is just listing linear terms with leading coeffs if needed to clear denominators.
    
    def get_factor_expr(p, q):
        # Returns string like "(3x - 2)" where root is 2/3 (p=2, q=3) -> factor (qx-p). 
        # If p=-1, q=2 (root -0.5), factor should be (2x + 1)? Yes because x - (-0.5) = x+0.5 ~ 2x+1 scaled by 2?
        # Wait, if I write (3x-2)(4x-5), the constant term is 10. 
        # Let's assume we output factors with integer coefficients that multiply to a*x^2... 
        # Actually, simplest exact factorization in latex often just lists roots and mentions factoring over Q?
        # Or writes (q x - p). If root is negative, it adds sign.
        
        if q == 1:
            return f"(x {''} {-p})" if p < 0 else f"(x {'+'}{p})" 
        else:
             # Check sign of constant term in (qx - p)
             const_sign = "+" if (-p > 0 and q > 1) or (-p >= 0 and q == 1) else ""? No.
             # Expression is qx + C where root is x = -C/q => r = -C/q => C = -qr.
             # We want factor (qx - p). If we write it as (q*x {op} |p|), op depends on sign of p relative to minus in formula?
             # Formula: q*x - p. 
             if p < 0:
                 return f"({q}x + {-p})"
             else:
                 return f"({q}x - {p})"

    fact1 = get_factor_expr(r1_num, r1_den)
    fact2 = get_factor_expr(r2_num, r2_den)
    
    # Note: The product of these two factors will be (qs)*P(x)/a. 
    # To be strictly correct "factorization", we might need to include the scalar 'a' or distribute it? 
    # Usually for integer coeffs problem like [1, 4, -12], roots are integers (-6, 2). Factors (x-6)(x+2)? No.
    # Let's check: x^2 + 4x - 12 = (x+6)(x-2). Roots: 2, -6. Ascending: [-6, 2].
    # My logic for get_factor_expr with p=6, q=1 -> "(x - 6)". Correct.
    # With p=-6, q=1 -> "(x + 6)". Correct.
    
    factorization_latex_str = f"{fact1} {fact2}" if fact1[0] == "(" else "" # Just join them
    
    question_text = rf"Find the roots and factorize the polynomial $P(x) = \{a\}x^2 + \{b\}x + \{c\}$."
    
    correct_answer_dict = {
        "roots": [root1_frac, root2_frac], # List of Fraction objects? Or strings? 
                                          # Prompt says: roots (ascending), factorization_latex, and roots_latex.
                                          # Does not specify type for 'roots' key specifically in the dict description other than implied content.
                                          # Usually JSON requires lists of numbers or strings. Fractions are Python specific.
                                          # I will return list of dictionaries with numerator/denominator if floats forbidden? 
                                          # "Exact arithmetic; no floats". So maybe tuples (num, den) or Fraction objects if allowed in internal logic but output needs to be serializable?
                                          # The prompt says "Write only Python source... generate() must return a dict". It doesn't say the return value is JSON serialized immediately. 
                                          # But standard practice for these tasks: roots should likely be list of dicts {"num":..., "den":...} or just Fraction objects if environment supports it.
                                          # Given strict constraints, I'll use tuples (n, d) to ensure exactness without float conversion in the value itself? Or keep Fractions. 
                                          # Let's assume returning Python objects is fine as long as no floats are used.
        "factorization_latex": factorization_latex_str.replace(" ", ""),
        "roots_latex": roots_latex_str
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": quadratic_coefficients
    }