from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    outer_coefficient = kwargs.get("outer_coefficient", 1)
    
    coeff, rad = RadicalOps.simplify_term(outer_coefficient, radicand)
    
    try:
        coeff_int = int(coeff)
    except (TypeError, ValueError):
        coeff_int = int(coeff.numerator // coeff.denominator)
        
    if outer_coefficient == 1:
        question_text = f"Rewrite $\\sqrt{{{radicand}}}$ in simplest radical form."
    else:
        question_text = f"Rewrite ${outer_coefficient}\\sqrt{{{radicand}}}$ in simplest radical form."
        
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coeff_int,
            "radicand": int(rad)
        },
        "oracle_payload": {
            "radicand": radicand
        }
    }