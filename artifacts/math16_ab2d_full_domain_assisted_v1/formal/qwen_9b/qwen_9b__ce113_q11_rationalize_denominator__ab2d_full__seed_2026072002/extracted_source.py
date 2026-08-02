def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }
    
    denom_rational = 4
    denom_radical_coeff = -1
    
    num_result_tuple = RadicalOps.rationalize_linear_denominator(frozen_params["numerator"], denom_rational, denom_radical_coeff, frozen_params["radicand"])
    
    a_val = int(RadicalOps.exact_integer(num_result_tuple[0]))
    b_val = int(RadicalOps.exact_integer(num_result_tuple[1]))
    
    result_sum = a_val + b_val
    
    return {
        "question_text": "將\\n\\[\\"frac{9}{4-\\\\sqrt{7}}\\"\\]\\n化為 \\\\left(a+b\\\\sqrt{7}\\\\right)，其中 a,b 為整數，求 a+b。",
        "correct_answer": result_sum,
        "oracle_payload": frozen_params
    }