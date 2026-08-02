from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }

    denom_rational = 4
    denom_radical_coeff = -1
    
    num_result_tuple = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], denom_rational, denom_radical_coeff, frozen_params["radicand"])
    
    a_exact = RadicalOps.exact_integer(num_result_tuple[0])
    b_exact = RadicalOps.exact_integer(num_result_tuple[1])
    
    result_sum = int(a_exact) + int(b_exact)

    return {
        "question_text": "將\n\\[\n\\frac{9}{4-\\sqrt{7}}\n\\]\n化為 \\(a+b\\sqrt{7}\\)，其中 \\(a,b\\) 為整數，求 \\(a+b\\)。",
        "correct_answer": result_sum,
        "oracle_payload": frozen_params
    }