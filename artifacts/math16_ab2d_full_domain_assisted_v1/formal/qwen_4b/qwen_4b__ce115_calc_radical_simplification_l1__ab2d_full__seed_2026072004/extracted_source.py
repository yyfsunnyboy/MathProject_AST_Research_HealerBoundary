from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_params", {})
    
    radicand = frozen_params["radicand"]
    
    # Step 1: Simplify the term to get coefficient and square-free radicand
    coeff, rest = RadicalOps.simplify_term(1, radicand)
    
    # Step 2 & 3: Assemble correct_answer according to contract
    canonical_latex = RadicalOps.format_linear_radical({
        "rational": 0, 
        "radical_coefficient": int(coeff), 
        "radicand": rest
    }) if coeff != 1 else f"{int(coeff)}\\sqrt{{{rest}}}"

    correct_answer = {
        "coefficient": int(coeff),
        "radicand": rest,
        "canonical_latex": canonical_latex
    }
    
    return {
        "question_text": frozen_params["description"],
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }
