from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }
    
    denom_rational = 4
    denom_radical_coeff = -1
    
    num_result_tuple = RadicalOps.rationalize_linear_denominator(
        numerator=frozen_params["numerator"], 
        denom_rational=denom_rational, 
        denom_radical_coeff=denom_radical_coeff, 
        radicand=frozen_params["radicand"]
    )
    
    rational_part = RationalOps.exact_integer(num_result_tuple[0]) if hasattr(RadicalOps, 'exact_integer') else num_result_tuple[0]
    radical_part = RadicalOps.exact_integer(num_result_tuple[1]) if hasattr(RadicalOps, 'exact_integer') else num_result_tuple[1]

    sum_val = rational_part + radical_part
    
    return {
        "question_text": "將\\n\\frac{9}{4-\\sqrt{7}}\\n化為 \\(a+b\\sqrt{7}\\)，其中 \\(a,b\\) 為整數，求 \\(a+b\\)。",
        "correct_answer": sum_val,
        "oracle_payload": frozen_params
    }