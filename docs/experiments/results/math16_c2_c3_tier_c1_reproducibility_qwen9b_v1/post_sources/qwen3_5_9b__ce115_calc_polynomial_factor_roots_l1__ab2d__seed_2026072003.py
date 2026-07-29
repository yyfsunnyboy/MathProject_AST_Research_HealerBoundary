from fractions import Fraction
import math

def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    # Import domain functions (simulating the environment where these are available)
    try:
        from core.prompts.domain_function_library import PolynomialOps, FractionOps
    except ImportError:
        # Fallback implementation if imports fail in this specific execution context, 
        # though the prompt implies they should be present. We implement logic inline to ensure correctness without external deps failing silently.
        
        def create_fraction(numerator=0, denominator=1):
            return Fraction(numerator, denominator)

        class PolynomialOps:
            @staticmethod
            def factor_quadratic_exact(a, b, c):
                # Solve ax^2 + bx + c = 0 for roots using quadratic formula or factoring if integer factors exist.
                # Returns list of dicts with keys 'x_coefficient', 'constant'.
                
                discriminant = b*b - 4*a*c
                
                if discriminant < 0:
                    return []
                
                sqrt_discriminant = int(math.isqrt(discriminant))
                if sqrt_discriminant * sqrt_discriminant != discriminant:
                    # Irrational roots, but task implies exact arithmetic. 
                    # However, for level 1 and given coefficients [1,4,-12], disc is positive perfect square (64).
                    pass
                
                root_delta = Fraction(sqrt_discriminant) if math.isqrt(discriminant)**2 == discriminant else None
                
                # Calculate roots: (-b +/- sqrt(D)) / (2a)
                
                denom = 2 * a
                
                term1_num = -b + int(math.sqrt(discriminant))
                term2_num = -b - int(math.sqrt(discriminant))
                
                root1_frac = Fraction(term1_num, denom) if math.isqrt(discriminant)**2 == discriminant else None
                root2_frac = Fraction(term2_num, denom) if math.isqrt(discriminant)**2 == discriminant else None
                
                # Format roots as dicts for the factorization structure requested: 
                # The prompt asks for a list of dict with keys 'x_coefficient', 'constant'.
                # This likely represents factors like (x - r1)(x - r2) -> x + (-r), const = 0? 
                # Or perhaps it wants the linear factor components. Let's assume standard form: (x + p/q).
                
                results = []
                if root1_frac is not None and math.isqrt(discriminant)**2 == discriminant:
                    res_dict = {
                        "x_coefficient": 1, 
                        "constant": -root1_frac.numerator // root1_frac.denominator # Simplified integer logic for exact roots? No.
                    }
                else:
                     pass
                
                # Re-evaluating the specific return format based on typical polynomial factorization tasks in this context:
                # Usually returns factors like (x + 2) and (x - 6). 
                # The dict keys 'x_coefficient' and 'constant' suggest a linear term Ax + B.
                
                r1 = Fraction(-b, denom) if discriminant == 0 else None
                
                # Let's calculate exact roots for [1, 4, -12] -> x^2 + 4x - 12 = (x+6)(x-2). Roots: -6, 2.
                # Factors: (x + (-(-6)))? No, factors are (x - root). 
                # Factor 1: x - (-6) => x + 6 -> coeff=1, const=6.
                # Factor 2: x - 2    => x - 2  -> coeff=1, const=-2.
                
                roots_list = []
                if discriminant >= 0 and math.isqrt(discriminant)**2 == discriminant:
                    sqrt_d = int(math.sqrt(discriminant))
                    
                    r1_num = (-b + sqrt_d) * Fraction(1, denom).denominator # Keep as fraction logic
                    r1_frac = Fraction(-b + sqrt_d, 2*a) if a != 0 else None
                    
                    r2_num = -b - sqrt_d
                    r2_frac = Fraction(r2_num, 2*a) if a != 0 else None
                    
                    roots_list.append({
                        "x_coefficient": 1, 
                        "constant": -r1_frac.numerator // r1_frac.denominator # Wait, constant in (x + c). If root is r, factor is x-r. So const = -r.
                        # But the prompt says 'exact arithmetic'. Let's store as Fraction for precision then convert if needed? 
                        # The example output format isn't fully specified beyond keys. I will use simplified integers or Fractions.
                    })
                    
                return roots_list

    a, b, c = frozen_params["quadratic_coefficients"]
    
    # Calculate discriminant and check for perfect square to ensure exact arithmetic (no floats)
    disc_val = b*b - 4*a*c
    
    if disc_val < 0:
        raise ValueError("No real roots")
        
    sqrt_disc = int(math.isqrt(disc_val))
    is_perfect_square = (sqrt_disc * sqrt_disc == disc_val)
    
    # Calculate exact roots as Fractions
    denom = 2 * a
    
    if not is_perfect_square:
        raise ValueError("Roots are irrational, cannot represent exactly with simple fractions in this context without surds.")
        
    root1_num = -b + sqrt_disc
    root2_num = -b - sqrt_disc
    
    # Create Fraction objects for roots
    r1_frac = Fraction(root1_num, denom) if a != 0 else None
    r2_frac = Fraction(root2_num, denom) if a != 0 else None
    
    # Sort roots ascending
    sorted_roots = [r1_frac, r2_frac]
    sorted_roots.sort()
    
    # Construct factorization components: (x + c). If root is r, term is x - r => constant part is -r.
    # Factor 1: coeff=1, const=-sorted_roots[0].numerator // ... 
    # We need to represent the linear factors exactly.
    
    def get_factor_const(root_frac):
        return Fraction(-root_frac.numerator, root_frac.denominator)

    factor_1 = {
        "x_coefficient": 1,
        "constant": -sorted_roots[0].numerator // sorted_roots[0].denominator # Simplify to int if possible? 
        # Actually, Fraction handles simplification. Let's return the integer value of the constant term in (x + k).
    }
    
    factor_2 = {
        "x_coefficient": 1,
        "constant": -sorted_roots[1].numerator // sorted_roots[1].denominator
    }
    
    # Re-construct properly using Fraction arithmetic for the constant term in (x + k)
    const1_frac = Fraction(-r2_frac.numerator * r1_frac.denominator, r2_frac.denominator * r1_frac.numerator)? No.
    # If root is p/q, factor is x - p/q => q*x/p? No. Factor is (qx - p)/q. 
    # Standard monic factors: (x - p/q). The constant term in the polynomial representation of the factor scaled to integer coefficients might be different.
    # However, usually "factorization" implies finding linear terms like (x+6) and (x-2).
    
    const1 = Fraction(-sorted_roots[0].numerator, sorted_roots[0].denominator)
    const2 = Fraction(-sorted_roots[1].numerator, sorted_roots[1].denominator)
    
    # Format for correct_answer: roots (ascending), factorization_latex, roots_latex
    
    root_str_1 = str(sorted_roots[0]) if isinstance(sorted_roots[0], int) else f"{sorted_roots[0]}"
    root_str_2 = str(sorted_roots[1]) if isinstance(sorted_roots[1], int) else f"{sorted_roots[1]}"
    
    # Roots latex: x_{-6}, x_{2} or just -6, 2? Usually "roots" means the values. 
    roots_latex = f"x_{{{root_str_0}}}, x_{{{root_str_1}}}" if len(sorted_roots) == 2 else str(sorted_roots[0])
    
    # Let's refine root string formatting for LaTeX
    def format_root_for_latex(frac):
        n, d = frac.numerator, frac.denominator
        if d == 1:
            return f"{n}"
        elif n % d == 0:
             return str(n // d) # Should be simplified by Fraction constructor usually.
        else:
            return rf"\frac{{{n}}}{{{d}}}"

    root_latex_1 = format_root_for_latex(sorted_roots[0])
    root_latex_2 = format_root_for_latex(sorted_roots[1])
    
    # Roots latex string (ascending)
    roots_latex_str = f"x_{root_latex_1}, x_{root_latex_2}" if len(sorted_roots) == 2 else str(root_latex_1)

    # Factorization LaTeX: (x + c)(x + d). 
    # Note: factor is (x - root). So constant in latex is (-root).
    
    def format_factor_term(const_frac):
        n, d = const_frac.numerator, const_frac.denominator
        if d == 1:
            term_str = f"x {n}" if n > 0 else f"x{n}" # x + c or x - |c|? 
            # If n is negative: "x -5". If positive: "x +5"
            sign = "+" if n >= 0 else "-"
            abs_n = abs(n)
            return rf"(x {sign} {abs_n})"
        else:
             term_str = f"x \pm ..." 
             # Complex formatting for fractions in factors. Let's assume integer roots for level 1 usually, but handle general case.
             sign = "+" if n >= 0 else "-"
             abs_n = abs(n)
             return rf"(x {sign} \frac{{{abs_n}}}{{{d}}})"

    term_1_latex = format_factor_term(const1) # const is -root
    term_2_latex = format_factor_term(const2)
    
    factorization_latex_str = f"{term_1_latex}{term_2_latex}" if len(sorted_roots) == 2 else term_1_latex

    question_text = rf"Find the roots and factorize the quadratic polynomial $x^2 + {b}x + {c}$."
    
    correct_answer = {
        "roots": [sorted_roots[0], sorted_roots[1]], # List of Fractions or ints? Prompt says exact arithmetic. Keep as Fraction objects if possible, but JSON requires serializable types usually. 
                # However, the prompt asks for 'correct_answer' dict content. If it needs to be returned by Python function, keeping Fraction is fine unless specified otherwise.
                # But often these tasks expect a specific structure. Let's assume standard list of numbers (int or float). Since exact arithmetic required -> int if possible else Fraction? 
                # The prompt says "Exact arithmetic; no floats". Fractions are the way to go in Python for this constraint.
        "correct_answer_roots": sorted_roots, # List of Fractions
        "factorization_latex": factorization_latex_str,
        "roots_latex": roots_latex_str
    }

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }