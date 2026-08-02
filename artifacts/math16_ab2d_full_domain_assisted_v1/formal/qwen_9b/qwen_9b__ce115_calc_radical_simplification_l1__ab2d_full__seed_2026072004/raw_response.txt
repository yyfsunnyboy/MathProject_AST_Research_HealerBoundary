from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = {"radicand": 27}
    
    coeff, radicand = RadicalOps.simplify_term(1, frozen_params["radicand"])
    
    canonical_latex = RadicalOps.format_term(coeff, radicand)
    
    return {
        "question_text": "將\\n[\\sqrt{27}]\\n化為最簡根式 \\(a\\sqrt{b}\\)，其中 \\(a\\) 為正整數，且 \\(b\\) 不含大於 \\(1\\) 的完全平方因數。",
        "correct_answer": {
            "coefficient": coeff,
            "radicand": radicand,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }