from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    frozen = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }
    
    denom_rational = 4
    denom_radical_coeff = -1
    
    num_new, den_num, den_denom = RadicalOps.rationalize_linear_denominator(frozen["numerator"], denom_rational, denom_radical_coeff, frozen["radicand"])
    
    a_int = RadicalOps.exact_integer(num_new)
    b_int = RadicalOps.exact_integer(den_num / den_denom if isinstance(den_num, int) else den_num)

    return {
        "question_text": "將\\[\\frac{9}{4-\\sqrt{7}}\\]化為 \(a+b\\sqrt{7}\)，其中 \(a,b\) 為整數，求 \(a+b\)。",
        "correct_answer": a_int + b_int,
        "oracle_payload": frozen
    }