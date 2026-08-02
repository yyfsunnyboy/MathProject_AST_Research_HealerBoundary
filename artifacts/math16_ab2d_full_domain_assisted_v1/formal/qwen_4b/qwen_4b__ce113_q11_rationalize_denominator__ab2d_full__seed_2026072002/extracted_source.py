from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_params", {})
    
    denom_rational = 4
    denom_radical_coeff = -1
    radicand = 7
    
    numerator_result_tuple = RadicalOps.rationalize_linear_denominator(9, denom_rational, denom_radical_coeff, radicand)
    a, b, _ = numerator_result_tuple

    if not isinstance(a, int):
        a = RadicalOps.exact_integer(a)
    
    if not isinstance(b, int):
        b = RadicalOps.exact_integer(b)

    correct_answer_value = a + b
    
    return {
        "question_text": frozen_params.get("stem", ""),
        "correct_answer": correct_answer_value,
        "oracle_payload": frozen_params
    }
