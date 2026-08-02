from core.prompts.domain_function_library import RadicalOps


def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_params", {})
    
    radicand = frozen_params["radicand"]
    
    coeff, rest = RadicalOps.simplify_term(1, radicand)
    
    correct_answer = {
        "coefficient": int(coeff),
        "radicand": int(rest),
        "canonical_latex": RadicalOps.format_linear_radical({
            "rational": 0, 
            "radical_coefficient": coeff, 
            "radicand": rest
        }) if isinstance(coeff, (int, type(frozen_params["radicand"]))) else str(int(coeff)) + "\\sqrt{" + str(rest) + "}"
    }

    return {
        "question_text": frozen_params.get("stem", ""),
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }
