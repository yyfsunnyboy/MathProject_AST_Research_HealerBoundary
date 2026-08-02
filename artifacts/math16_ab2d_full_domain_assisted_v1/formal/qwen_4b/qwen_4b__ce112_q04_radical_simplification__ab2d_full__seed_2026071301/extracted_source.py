from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = kwargs.get('frozen_params', {"radicand": 135})
    
    radicand = frozen_params["radicand"]
    
    coeff, rest = RadicalOps.simplify_term(1, radicand)
    
    correct_answer = {
        "coefficient": int(coeff),
        "radicand": int(rest),
        "canonical_latex": RadicalOps.format_linear_radical({"rational": 0, "radical_coefficient": coeff, "radicand": rest}) if not isinstance(coeff, str) else f"{coeff}\\sqrt{{{rest}}}"
    }

    return {
        "question_text": "將\n\\[\n\\sqrt{135}\n\\]\n化為最簡根式。",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }
