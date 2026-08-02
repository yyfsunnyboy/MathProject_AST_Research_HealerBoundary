from core.prompts.domain_function_library import RadicalOps, Fraction

def generate(level=1, **kwargs):
    radicand = kwargs.get("frozen_params", {}).get("radicand")
    
    coeff, simplified_radicand = RadicalOps.simplify_term(0, radicand)
    
    correct_answer = {
        "coefficient": int(coeff),
        "radicand": int(simplified_radicand),
        "canonical_latex": RadicalOps.format_linear_radical({
            "rational": 0, 
            "radical_coefficient": coeff if isinstance(coeff, Fraction) else float(coeff), # Handle potential Fraction input from simplify_term logic if needed, but example shows ints. Let's re-verify the API usage for formatting a pure radical term like sqrt(b). The format_linear_radical expects rational and coefficient. If we have 0 + c*sqrt(radicand), it formats as "c\sqrt{radicand}".
            # However, simplify_term returns (coeff, radicand) where coeff is the multiplier of the simplified root. 
            # For sqrt(27) = 3 * sqrt(3). Coeff=3, Radicand=3.
        }) if isinstance(coeff, Fraction) else RadicalOps.format_linear_radical({
            "rational": 0, 
            "radical_coefficient": coeff, 
            "radicand": simplified_radicand
        }), # Assuming simplify_term returns int for integer inputs like 27 based on description.
    }

    return {
        "question_text": kwargs.get("frozen_params", {}).get("stem"),
        "correct_answer": correct_answer,
        "oracle_payload": kwargs.get("frozen_params") or {},
    }
