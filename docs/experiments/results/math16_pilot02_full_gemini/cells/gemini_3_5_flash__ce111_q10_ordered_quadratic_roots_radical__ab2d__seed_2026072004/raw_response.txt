import re
from core.prompts.domain_function_library import RadicalOps, FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    equation = "(x-2)^2=3"
    order = "a>b"
    target = "2a+b"
    
    # Parse equation
    match_eq = re.match(r"\(x([+-]\d+)\)\^2=(\d+)", equation)
    if not match_eq:
        raise ValueError("Failed to parse equation")
    h = -int(match_eq.group(1))
    d = int(match_eq.group(2))
    
    # Parse target
    s = target.replace(" ", "")
    if s.startswith("a"):
        s = "1" + s
    elif s.startswith("-a"):
        s = "-1" + s[1:]
    elif s.startswith("+a"):
        s = "1" + s[1:]
    s = s.replace("+b", "+1b").replace("-b", "-1b")
    match_tgt = re.match(r"([+-]?\d+)a([+-]?\d+)b", s)
    if not match_tgt:
        raise ValueError("Failed to parse target")
    C1 = int(match_tgt.group(1))
    C2 = int(match_tgt.group(2))
    
    # Simplify radical part of the roots
    coeff_d, radicand_d = RadicalOps.simplify_term(1, d)
    
    # Roots are h +/- coeff_d * sqrt(radicand_d)
    if order == "a>b":
        rational_part = (C1 + C2) * h
        radical_coeff = (C1 - C2) * coeff_d
    else:
        rational_part = (C1 + C2) * h
        radical_coeff = (C2 - C1) * coeff_d
        
    radicand = radicand_d
    
    # Simplify the resulting radical term
    final_coeff, final_radicand = RadicalOps.simplify_term(radical_coeff, radicand)
    
    # Format canonical LaTeX
    terms_dict = {}
    if rational_part != 0:
        terms_dict[1] = rational_part
    if final_coeff != 0:
        terms_dict[final_radicand] = final_coeff
        
    canonical_latex = RadicalOps.format_expression(terms_dict)
    
    question_text = f"Solve the equation \\((x-2)^2=3\\). Let \\(a\\) and \\(b\\) be the roots of the equation with \\(a>b\\). Find the value of \\(2a+b\\)."
    
    oracle_payload = {
        "equation": equation,
        "order": order,
        "target": target
    }
    
    correct_answer = {
        "rational": rational_part,
        "radical_coefficient": final_coeff,
        "radicand": final_radicand,
        "canonical_latex": canonical_latex,
        "result": {
            "rational": rational_part,
            "radical_coefficient": final_coeff,
            "radicand": final_radicand,
            "canonical_latex": canonical_latex
        }
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }