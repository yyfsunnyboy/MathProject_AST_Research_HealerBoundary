from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 135)
    
    coeff, rest = RadicalOps.simplify_term(1, radicand)
    
    latex_str = RadicalOps.format_term(coeff, rest)
    
    return {
        "question_text": r"將 \[\sqrt{135}\] 化為最簡根式。",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": rest,
            "canonical_latex": latex_str
        },
        "oracle_payload": {"radicand": radicand}
    }