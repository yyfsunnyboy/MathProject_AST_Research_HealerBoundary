from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = {
        "radicand": 27
    }
    
    radicand = frozen_params["radicand"]
    coeff, rest = RadicalOps.simplify_term(1, radicand)
    
    coeff_int = RadicalOps.exact_integer(coeff)
    rest_int = RadicalOps.exact_integer(rest)
    
    canonical_latex = RadicalOps.format_term(coeff_int, rest_int)
    
    question_text = (
        "將\n"
        "\\[\n"
        "\\sqrt{27}\n"
        "\\]\n"
        "化為最簡根式 \\(a\\sqrt{b}\\)，其中 \\(a\\) 為正整數，且 \\(b\\) 不含大於 \\(1\\) 的完全平方因數。"
    )
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": coeff_int,
            "radicand": rest_int,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }