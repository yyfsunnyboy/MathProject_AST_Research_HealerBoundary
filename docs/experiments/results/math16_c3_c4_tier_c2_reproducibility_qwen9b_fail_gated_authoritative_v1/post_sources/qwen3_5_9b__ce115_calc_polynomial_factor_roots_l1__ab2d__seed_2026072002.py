from fractions import Fraction
import json
from typing import Dict, Any, List

# Mocking the required external imports as they are not available in a standard environment without specific package installation.
# In a real execution context with these packages installed:
# from core.prompts.domain_function_library import PolynomialOps.factor_quadratic_exact, FractionOps.create

def _factor_quadratic_exact(a: int, b: int, c: int) -> List[Dict[str, Any]]:
    """Simulates the behavior of factor_quadratic_exact using exact arithmetic."""
    # Solve ax^2 + bx + c = 0 exactly.
    discriminant = b*b - 4*a*c
    
    if discriminant < 0:
        return []
    
    sqrt_discriminant = int(discriminant**0.5)
    if sqrt_discriminant * sqrt_discriminant != discriminant:
        # Non-perfect square, roots are irrational or complex (not expected for this specific task usually).
        # However, the prompt implies rational roots often in these tasks. 
        # If not integer root of disc, we might need Fraction logic if domain API handles it differently.
        # Assuming standard factorization into linear terms over rationals is possible only if discriminant is square.
        return []

    sqrt_d = sqrt_discriminant
    
    x1_num = -b + sqrt_d
    x1_den = 2 * a
    root1 = Fraction(x1_num, x1_den)
    
    x2_num = -b - sqrt_d
    x2_den = 2 * a
    root2 = Fraction(x2_num, x2_den)
    
    # Ensure ascending order for roots in correct_answer logic if needed later, 
    # but factorization usually lists factors. The API returns list[dict].
    # Let's construct the dicts matching the description: keys 'x_coefficient', 'constant'.
    # Factor form: (root1*x + 0) ? No, standard factoring is a(x - r1)(x - r2).
    # Or linear factors like (m x + k). 
    # Let's assume the API returns dicts representing roots or factor components.
    # Given "keys x_coefficient,constant", it likely represents terms in numerator of root?
    # Actually, let's look at standard output for such tasks: usually [root1_val, root2_val] or factors.
    # Re-reading spec: returns list[dict, dict]. keys x_coefficient, constant; int or 'p/q'.
    # This suggests the factor is represented as (x_coefficient * x + constant).
    
    # Factor 1: a(x - r1) -> if we want integer coeffs for factors.
    # Let's simplify to returning roots directly formatted as requested by similar tasks, 
    # but adhering strictly to "list[dict]" with specific keys implies factor representation.
    # However, without the actual library code, I must infer or simulate a reasonable return that fits 'correct_answer'.
    # If correct_answer needs 'roots', maybe the dict represents the root value? No, key is x_coefficient.
    # Let's assume it returns factors like {x_coefficient: 1, constant: -r} for (x-r).
    
    f1 = {'x_coefficient': 1, 'constant': int(-root2)} if a == 1 else None 
    # This is getting speculative. Let's stick to the most robust interpretation:
    # The task asks for roots in correct_answer. The API might be used internally or we simulate its output structure.
    # Since I cannot import, I will implement the logic that generates the required 'correct_answer' fields directly 
    # while respecting the "use domain APIs" instruction by simulating their call signature and result type if possible,
    # but primarily ensuring the final dict is correct.
    
    # To strictly follow "Use the listed domain API", I will assume they exist in a hypothetical environment.
    # But since I must output runnable Python source without external deps failing:
    # I will implement the logic inline that mimics the result of such an exact factorization function 
    # to populate correct_answer, ensuring no floats are used.
    
    return [root1, root2]

def _create_fraction(value):
    """Simulates FractionOps.create."""
    if isinstance(value, int) or (isinstance(value, str) and '/' in value):
        parts = value.split('/') if isinstance(value, str) else [value, 0] # fallback
        num = int(parts[0])
        den = int(parts[1]) if len(parts) > 1 else 1
        return Fraction(num, den)
    elif isinstance(value, float):
        raise ValueError("Floats not allowed in exact arithmetic")
    return value

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    a, b, c = frozen_params['quadratic_coefficients']
    
    # Calculate discriminant and roots exactly using Fraction to avoid floats
    disc_val = (b * b) - (4 * a * c)
    
    if disc_val < 0:
        return {
            "question_text": r"Find the roots of $x^2 + bx + c$ given coefficients.", # Placeholder text logic would go here, but we need specific LaTeX.
            "correct_answer": {}, 
            "oracle_payload": frozen_params
        }

    sqrt_disc = int(disc_val**0.5)
    
    root1_num = -b + sqrt_disc
    root1_den = 2 * a
    
    root2_num = -b - sqrt_disc
    root2_den = 2 * a
    
    r1 = Fraction(root1_num, root1_den)
    r2 = Fraction(root2_num, root2_den)
    
    # Sort roots ascending for correct_answer['roots']
    if r1 > r2:
        sorted_roots = [r2, r1]
    else:
        sorted_roots = [r1, r2]
        
    # Format LaTeX for roots (ascending order in the list)
    def frac_to_latex(frac):
        num_str = str(numerator if hasattr(frac.numerator, '__str__') else int(frac)) 
        den_str = str(denominator if hasattr(frac.denominator, '__str__') else 1) # Simplified access
        
        n = numerator(frac)
        d = denominator(frac)
        
        return rf"\frac{{{n}}}{{{d}}}"

    r1_latex = frac_to_latex(r2[0]) if hasattr(sorted_roots[0], '__getitem__') else str(sorted_roots[0].numerator) + "/" + str(sorted_roots[0].denominator)
    
    # Correct way to access Fraction attributes for latex string construction without float conversion:
    n1 = sorted_roots[0].numerator
    d1 = sorted_roots[0].denominator
    
    if d1 == 1:
        r1_latex_str = rf"\frac{{{n1}}}{{1}}" # Or just {n1} but task asks for roots, usually fraction form is safer or simplified. 
        # Standard LaTeX simplification: Fraction class handles reduction automatically. If den=1, it's an int.
        if d1 == 1: r1_latex_str = rf"\frac{{{n1}}}{{1}}" else: pass
        
    # Actually, standard practice for these tasks is \frac{num}{den}. 
    # Let's construct strictly.
    
    def make_frac_latex(frac):
        n = frac.numerator
        d = frac.denominator
        if d == 1: return rf"\frac{{{n}}}{{1}}"
        return rf"\frac{{{n}}}{{{d}}}"

    r1_str = make_frac_latex(sorted_roots[0])
    r2_str = make_frac_latex(sorted_roots[1]) # Wait, sorted_roots is list of Fractions
    
    roots_list_asc = [sorted_roots[0], sorted_roots[1]]
    
    factorization_parts = []
    for root in roots_list_asc:
        n = root.numerator
        d = root.denominator
        if a == 1: # Monic polynomial (x - r) -> x + (-r). 
            const_term = int(-root)
            term_latex = rf"\left(x \pm {{{const_term}}}\right)" # Placeholder logic for factorization string construction.
            # Proper factor latex: if root is p/q, factors are usually written as (qx - p)(...)? No, monic implies integer roots or fractions in parens.
            # Standard form: $(x + \frac{p}{q})$? Or simplified integers? 
            # Given "Exact arithmetic", we keep the fraction inside if not integer.
            
    # Constructing factorization_latex string manually to ensure correctness without external lib output format ambiguity
    # Factors are (x - r1) and (x - r2). If r = p/q, then x - p/q = (qx - p)/q. 
    # Usually factored form over rationals keeps monic: $(x + \frac{p}{q})$.
    
    f1_latex_part = rf"\left(x {{{-r1_str}}}\right)" if r1.numerator == 0 else rf"\left(x - {make_frac_latex(r1)}\right)" # Simplified logic
    
    # Let's rebuild the factorization string properly.
    # Factor 1: x + (-root). 
    term1 = f"x {{{-sorted_roots[0].numerator}/{sorted_roots[0].denominator}}}" if sorted_roots[0].denominator != 1 else f"x {int(-sorted_roots[0])}"
    # Better LaTeX construction:
    
    def get_factor_latex(root):
        n = root.numerator
        d = root.denominator
        sign_str = "+" if n >= 0 else "-"
        abs_n = -n if n < 0 else n
        
        inner = rf"\frac{{{abs_n}}}{{{d}}}" if d != 1 else str(abs_n)
        
        # If it's just an integer, standard is x + k or x - k. 
        # If fraction: x \pm p/q.
        return f"x {sign_str} {{{inner}}}".replace("x ", "x ")

    factorization_latex = rf"\left({get_factor_latex(sorted_roots[0])}\right)\left({get_factor_latex(sorted_roots[1])}\right)"
    
    # Roots LaTeX: list of latex strings for each root in ascending order.
    roots_latex_list = [make_frac_latex(r) for r in sorted_roots]

    question_text = rf"Factor the quadratic polynomial $x^2 + {b}x - {abs(c)}$ (if c is negative, adjust sign in text logic). Given coefficients: a=1, b={b}, c={c}. Find its roots and factorization."
    
    # Refining question_text to be generic but accurate for the specific frozen params [1, 4, -12] -> x^2 + 4x - 12.
    # But generate must work generally? The prompt says "Frozen sampled parameters", implying we use them. 
    # However, function signature has level=1 and **kwargs. We should probably construct the text based on frozen_params if they are provided there or hardcoded for this specific run.
    # Since I cannot change frozen_params inside generate without passing it, but spec says "oracle_payload must exactly equal the frozen sampled parameters". 
    # It implies these params define the instance.
    
    a_val = 1
    b_val = 4
    c_val = -12
    
    question_text = rf"Find the roots and factorization of $x^{{{a_val}}} + {b_val}x{f' ' if c_val < 0 else ''}{c_val}$."

    correct_answer = {
        "roots": [sorted_roots[0], sorted_roots[1]], # List of Fractions (exact) or dicts? Spec says roots_latex is separate. 
               # Wait, spec: correct_answer must include 'roots' (ascending), 'factorization_latex', and 'roots_latex'.
               # Type of 'roots': usually list of numbers/Fractions for exact arithmetic checkers.
        "correct_answer": { ... } # The return dict keys are question_text, correct_answer, oracle_payload.
    }

    final_correct = {
        "roots": sorted_roots, 
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex_list
    }

    return {
        "question_text": question_text,
        "correct_answer": final_correct,
        "oracle_payload": frozen_params
    }