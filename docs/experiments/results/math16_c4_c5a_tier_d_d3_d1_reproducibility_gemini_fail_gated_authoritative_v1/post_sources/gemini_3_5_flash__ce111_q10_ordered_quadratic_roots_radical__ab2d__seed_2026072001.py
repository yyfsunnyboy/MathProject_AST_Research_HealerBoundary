import re
from fractions import Fraction
from core.prompts.domain_function_library import RadicalOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    equation = "(x-2)^2=3"
    order = "a>b"
    target = "2a+b"
    
    # Parse equation (x - h)^2 = d
    match = re.match(r"\(x([+-]\d+)\)\^2=(\d+)", equation)
    if match:
        h_sign_val = match.group(1)
        h = -int(h_sign_val)
        d = int(match.group(2))
    else:
        h = 2
        d = 3
        
    # Roots are h + sqrt(d) and h - sqrt(d)
    r_pos = (h, 1, d)
    r_neg = (h, -1, d)
    
    if order == "a>b":
        a_rat, a_coeff, a_rad = r_pos[0], r_pos[1], r_pos[2]
        b_rat, b_coeff, b_rad = r_neg[0], r_neg[1], r_neg[2]
    else:
        a_rat, a_coeff, a_rad = r_neg[0], r_neg[1], r_neg[2]
        b_rat, b_coeff, b_rad = r_pos[0], r_pos[1], r_pos[2]
        
    # Parse target
    if target == "2a+b":
        ca, cb = 2, 1
    elif target == "a+2b":
        ca, cb = 1, 2
    elif target == "a-b":
        ca, cb = 1, -1
    elif target == "b-a":
        ca, cb = -1, 1
    elif target == "a+b":
        ca, cb = 1, 1
    else:
        ca, cb = 2, 1
        
    res_rat = ca * a_rat + cb * b_rat
    res_coeff = ca * a_coeff + cb * b_coeff
    
    # Simplify the radical term
    simplified_coeff, simplified_radicand = RadicalOps.simplify_term(res_coeff, d)
    
    # Format expression
    terms = {}
    if res_rat != 0:
        terms[1] = res_rat
    if simplified_coeff != 0:
        terms[simplified_radicand] = simplified_coeff
        
    canonical_latex = RadicalOps.format_expression(terms)
    if not terms:
        canonical_latex = "0"
        
    question_text = f"Solve the equation \\({equation}\\) for \\(x\\). Let the roots be \\(a\\) and \\(b\\) such that \\({order}\\). Find the value of \\({target}\\)."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "result": {
                "rational": int(res_rat),
                "radical_coefficient": int(simplified_coeff),
                "radicand": int(simplified_radicand),
                "canonical_latex": canonical_latex
            }
        },
        "oracle_payload": {
            "equation": equation,
            "order": order,
            "target": target
        }
    }