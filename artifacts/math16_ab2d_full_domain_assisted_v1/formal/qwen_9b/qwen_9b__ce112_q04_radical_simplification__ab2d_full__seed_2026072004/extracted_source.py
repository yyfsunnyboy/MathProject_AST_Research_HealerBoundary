from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = {"radicand": 135}
    
    coeff, radicand = RadicalOps.simplify_term(1, frozen_params["radicand"])
    
    latex_str = RadicalOps.format_term(coeff, radicand)
    
    return {
        "question_text": "將\\[\\sqrt{135}\\]化為最簡根式。",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": radicand,
            "canonical_latex": latex_str
        },
        "oracle_payload": frozen_params
    }