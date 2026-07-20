def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Calculate roots for x^2 + 4x - 12 = 0 using exact arithmetic (fractions)
    from fractions import Fraction
    
    a = Fraction(quadratic_coefficients[0])
    b = Fraction(quadratic_coefficients[1])
    c = Fraction(quadratic_coefficients[2])
    
    discriminant = b * b - 4 * a * c
    sqrt_discriminant_num = int(discriminant.sqrt()) if discriminant >= 0 else None
    
    # Since we need exact roots and the example coefficients yield integer roots:
    # x^2 + 4x - 12 -> (x+6)(x-2) -> Roots are -6, 2.
    
    root1 = Fraction(-b - sqrt_discriminant_num, 2 * a) if discriminant >= 0 else None
    root2 = Fraction(-b + sqrt_discriminant_num, 2 * a) if discriminant >= 0 else None
    
    # Ensure ascending order
    roots_list = sorted([root1, root2])
    
    # Construct LaTeX strings for factors and roots using the exact integer values derived from the specific example
    # Factors: (x + p)(x + q). Here roots are -6 and 2. So factors are (x-2) and (x+6).
    r1_int = int(roots_list[0])
    r2_int = int(roots_list[1])
    
    factor_str_1 = f"(x{'+'.join([''] if str(r1_int)[0] in ['-', ''] else [str(abs(r1_int))] + ['+','']*r1_int < 0 or ['-']+abs(str(-r2))})" # Manual construction for LaTeX safety
    # Simpler manual string build:
    def format_factor(root_val):
        val = root_val.numerator // root_val.denominator if hasattr(root_val, 'numerator') else int(float(root_val))
        sign = '-' if val < 0 else '+'
        num_str = abs(val)
        return f"(x{sign}{num_str})"

    factor_latex = format_factor(roots_list[1]) + " \\cdot " + format_factor(roots_list[0])
    
    # Roots LaTeX: -6, 2 -> x_1=-6,\; x_2=2
    roots_latex = f"x_{len(roots_list)}={{-{r1_int}}},\; x_{len(roots_list)-1}={r2_int}" if len(roots_list) == 2 else ", ".join([f"{{{int(r)}}}" for r in roots_list])

    return {
        "question_text": f"Solve the quadratic equation $x^2 + {quadratic_coefficients[1]}x + {quadratic_coefficients[2]} = 0$ by factoring.",
        "correct_answer": {
            "roots": [int(r) for r in roots_list],
            "factorization_latex": f"(x{'-'.join([''] if int(roots_list[1]) > 0 else [''])}{'-' + str(abs(int(roots_list[1])))})(x{-''+str(abs(int(roots_list[0])))})" # Simplified logic for the specific case
        }, 
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }

# Corrected implementation to strictly follow the contract and arithmetic requirements without float errors:

def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    # Exact calculation for roots of x^2 + 4x - 12 = 0
    # Roots are integers: -6 and 2.
    exact_roots = [-6, 2]
    
    # Ascending order is already satisfied by the list above
    
    # Factorization LaTeX construction manually to ensure correctness
    r_asc = exact_roots[0]
    r_desc = exact_roots[1]
    
    factor_part_1 = f"(x{'' if -r_asc == 0 else ('+' if r_asc > 0 else '-')}{'-' + str(abs(r_asc))})" # This logic is flawed for negative roots in LaTeX string construction. 
    # Let's build the factors based on (x-root).
    # Factor 1: x - (-6) = x+6
    # Factor 2: x - 2 = x-2
    
    factor_latex_str = f"(x{'+'.join([''] if False else [''])}{'+' + str(abs(r_asc))})(x{-''+str(abs(-r_desc))})" 
    # Re-evaluating string construction for robustness
    def make_factor(root):
        val = root
        sign = '+' if val > 0 else '-'
        num_str = abs(val)
        return f"(x{sign}{num_str})"

    factor_latex = make_factor(r_asc) + " \\cdot " + make_factor(r_desc)
    
    # Roots LaTeX: x_{-6},\; x_{2} -> usually formatted as a set or list in text. 
    # The prompt asks for roots_latex. Let's format clearly.
    roots_latex = f"x_{{{r_asc}}},\\,x_{{{r_desc}}}"

    return {
        "question_text": r"Solve the quadratic equation $x^2 + 4x - 12 = 0$ by factoring.",
        "correct_answer": {
            "roots": [-6, 2],
            "factorization_latex": "(x+6) \\cdot (x-2)",
            "roots_latex": r"x_{-6},\\,x_2"
        }, 
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }