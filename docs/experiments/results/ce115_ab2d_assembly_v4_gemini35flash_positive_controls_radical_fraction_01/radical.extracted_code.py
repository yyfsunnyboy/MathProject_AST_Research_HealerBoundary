from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27)
    outer_coefficient = kwargs.get("outer_coefficient", 1)
    
    coeff_out, rad_out = RadicalOps.simplify_term(outer_coefficient, radicand)
    
    coeff_out = int(coeff_out)
    rad_out = int(rad_out)
    
    if outer_coefficient == 1:
        question_text = f"Rewrite $\\sqrt{{{radicand}}}$ in simplest radical form."
    else:
        question_text = f"Rewrite ${outer_coefficient}\\sqrt{{{radicand}}}$ in simplest radical form."
        
    oracle_payload = {"radicand": radicand}
    if "outer_coefficient" in kwargs:
        oracle_payload["outer_coefficient"] = outer_coefficient
        
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coeff_out,
            "radicand": rad_out
        },
        "oracle_payload": oracle_payload
    }