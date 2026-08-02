from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 135)
    
    coeff, simplified_radicand = RadicalOps.simplify_term(0, radicand)
    
    correct_answer = {
        "coefficient": int(coeff),
        "radicand": int(simplified_radicand),
        "canonical_latex": RadicalOps.format_linear_radical({"rational": 0, "radical_coefficient": coeff, "radicand": simplified_radicand}) if not isinstance(coeff, Fraction) else f"{coeff} * \\sqrt{{{simplified_radicand}}}", # Handle fractional coefficients properly
    }

    return {
        "question_text": r"將\n\[\n\\sqrt{135}\n\)化為最簡根式。",
        "correct_answer": correct_answer,
        "oracle_payload": {"radicand": radicand}
    }
