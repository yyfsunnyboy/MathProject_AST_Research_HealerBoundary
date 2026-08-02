def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_params", {})
    
    numerator = frozen_params["numerator"]
    denom_rational = 4
    denom_radical_coeff = -1
    radicand = frozen_params["radicand"]
    
    result_tuple = RadicalOps.rationalize_linear_denominator(numerator, denom_rational, denom_radical_coeff, radicand)
    
    a, b, _ = result_tuple
    
    if not isinstance(a, int):
        a = RadicalOps.exact_integer(a)
        
    if not isinstance(b, int):
        b = RadicalOps.exact_integer(b)
        
    total_sum = a + b
    
    return {
        "question_text": frozen_params["denominator"] + "\\frac{" + str(numerator) + "}"}{frozen_params['numerator']}\\sqrt{{{radicand}}}",
        "correct_answer": int(total_sum),
        "oracle_payload": frozen_params,
    }
