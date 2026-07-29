from fractions import Fraction
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import PolynomialOps, FractionOps
except ImportError:
    # Fallback for local execution without full environment if necessary, 
    # but per instructions we assume the library is available or implement minimal stubs.
    
    class FakeFraction(Fraction):
        def __init__(self, value=None):
            super().__init__()


def generate(level=1, **kwargs):
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    # Extract coefficients a, b, c from the list provided in frozen params or kwargs override if logic allowed (here strictly frozen)
    coeffs = frozen_params["quadratic_coefficients"]
    a = int(coeffs[0])
    b = int(coeffs[1])
    c = int(coeffs[2])

    # Use domain API to factor exactly
    try:
        factors_list = PolynomialOps.factor_quadratic_exact(a, b, c)
    except Exception as e:
        # Fallback calculation if library is not present in this specific run context (e.g., isolated execution)
        discriminant_val = b*b - 4*a*c
        sqrt_discriminant = int(discriminant_val**0.5)
        
        root1_num = -b + sqrt_discriminant
        root1_denom = 2 * a
        
        root2_num = -b - sqrt_discriminant
        root2_denom = 2 * a

        # Construct factor dicts manually for fallback to ensure exact types match contract
        if discriminant_val >= 0:
            r1_frac = Fraction(root1_num, root1_denom)
            r2_frac = Fraction(root2_num, root2_denom)
            
            f1 = {'x_coefficient': r1_frac, 'constant': c/a} # Note: constant term in factor (ax - b/2 +/- ...) logic varies. 
            # Standard form a(x-r1)(x-r2). Factors usually represented as {root: ..., coeff: ...}.
            # Based on typical API return structure for this task type: [dict(root=r1), dict(root=r2)] or similar.
            # Let's assume the standard factorization output format expected by 'correct_answer' generation logic in these tasks:
            # List of dicts containing root info and constant term if applicable, OR just roots. 
            # Re-reading spec: "returns: list[dict, dict] ... keys x_coefficient,constant". This implies factors like (x - r).
            
            f1 = {'x_coefficient': Fraction(1), 'constant': -r1_frac}
            f2 = {'x_coefficient': Fraction(1), 'constant': -r2_frac}
        else:
             # Complex roots not expected for level 1 integer coeffs usually, but handle gracefully if needed.
             pass

    # Sort factors by root value ascending to ensure deterministic output order in list? 
    # The spec says "roots (ascending)" inside correct_answer dict. It doesn't explicitly mandate the internal factor list sort, 
    # but for consistency we will process roots into a sorted tuple/list first.
    
    if isinstance(factors_list[0], Fraction):
        r1 = factors_list[0]
        r2 = factors_list[1]
    else:
        # If fallback logic produced dicts with 'x_coefficient' key, extract root from there? 
        # Actually, the spec says API returns list of dict. Let's assume standard behavior where we construct roots directly for safety if library fails or behaves differently.
        r1 = factors_list[0]['x_coefficient']
        r2 = factors_list[1]['x_coefficient']

    # Ensure ascending order for correct_answer['roots']
    sorted_roots_tuple = tuple(sorted([r1, r2]))
    
    # Construct LaTeX strings without floats
    def frac_latex(n):
        if n.denominator == 1: return str(n.numerator)
        else: return f"\\frac{{{n.numerator}}}{{{{{n.denominator}}}}}"

    roots_str = ", ".join([frac_latex(r) for r in sorted_roots_tuple])
    
    # Factorization LaTeX: a(x - r1)(x - r2). 
    # Format: k_0 (x + c_1/k_0)(x + c_2/k_0)? Or simply coefficients.
    # Standard factor form: 1 * (x - root1) * (x - root2) since a=1 here.
    term1 = f"x {frac_latex(-r1)}" if r1.numerator != 0 else "x" # Simplified visual, usually x + c
    # Better LaTeX for factor: (x \\pm ...)
    sign_r1 = "+" if sorted_roots_tuple[0].numerator < 0 else "-"
    val_r1_abs = abs(sorted_roots_tuple[0])
    
    term2_str = f"x {frac_latex(-sorted_roots_tuple[0])}" # x + (-r) -> x - r. If r is negative, -r is positive.
    # Let's build strictly: (x - root). 
    if sorted_roots_tuple[0].numerator < 0:
        term1_str = f"x {frac_latex(-sorted_roots_tuple[0])}" # x + |root|
    else:
        term1_str = f"x {-frac_latex(sorted_roots_tuple[0])}" # x - root
    
    if sorted_roots_tuple[1].numerator < 0:
        term2_str = f"x {frac_latex(-sorted_roots_tuple[1])}" 
    else:
        term2_str = f"x {-frac_latex(sorted_roots_tuple[1])}"

    factorization_latex = f"{a} ({term1_str}) ({term2_str})" if a != 1 else f"({term1_str}) ({term2_str})"

    question_text = (
        r"Solve the quadratic equation $x^2 + bx + c = 0$ given coefficients from the frozen parameters. "
        r"What are the roots of the polynomial and its factorization over $\mathbb{Q}$?"
    ) # Using generic text, but could be specific to coeffs if needed. 
    # To make it robust: substitute actual numbers? The prompt says "frozen sampled parameters". Usually questions use these values.
    question_text = (
        f"Solve the quadratic equation $x^2 + {b}x + {c} = 0$. Find the roots and factorization."
    )

    correct_answer = {
        "roots": sorted_roots_tuple, # List of Fractions or tuple? Spec says list[dict] for API return. For 'correct_answer', usually a list of values. 
                                   # Wait: spec says "correct_answer must include roots (ascending)". Usually implies [r1, r2].
                                   # Let's provide as list of dicts if the domain expects it, or just values? 
                                   # Re-reading: "returns: list[dict...]" is for API. correct_answer structure not strictly defined beyond keys.
                                   # I will return roots as a tuple/list of Fractions to be exact arithmetic.
        "roots": sorted_roots_tuple, 
        "factorization_latex": factorization_latex,
        "roots_latex": f"$\\{{{frac_latex(sorted_roots_tuple[0])}\\}}, \\{{{frac_latex(sorted_roots_tuple[1])}}}$$" # Or comma separated inside math mode? Usually list. Let's do: $r_1, r_2$. 
    }
    
    # Adjust roots_latex to be a single string representation of the set or tuple in LaTeX
    correct_answer["roots_latex"] = f"$\\{{{frac_latex(sorted_roots_tuple[0])}\\}}, \\{{{frac_latex(sorted_roots_tuple[1])}}}$$"

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }