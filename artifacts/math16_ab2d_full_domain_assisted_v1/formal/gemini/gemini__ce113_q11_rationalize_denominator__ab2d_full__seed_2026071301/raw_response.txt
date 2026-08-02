from fractions import Fraction
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Frozen params
    frozen_params = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }
    
    # 1) Interpret the frozen denominator
    denom_rational = 4
    denom_radical_coeff = -1
    numerator = frozen_params["numerator"]
    radicand = frozen_params["radicand"]
    
    # Call rationalize_linear_denominator
    num_rational, num_radical_coeff, common_denom = RadicalOps.rationalize_linear_denominator(
        numerator, denom_rational, denom_radical_coeff, radicand
    )
    
    # 2) RadicalOps.exact_integer on both returned coefficients
    a_frac = Fraction(num_rational) / common_denom
    b_frac = Fraction(num_radical_coeff) / common_denom
    
    a = RadicalOps.exact_integer(a_frac)
    b = RadicalOps.exact_integer(b_frac)
    
    # 3) Native int add of those coefficients
    correct_answer = a + b
    
    # 4) Assemble correct_answer exactly according to the Answer contract
    question_text = "將\n\\[\n\\frac{9}{4-\\sqrt{7}}\n\\]\n化為 \\(a+b\\sqrt{7}\\)，其中 \\(a,b\\) 為整數，求 \\(a+b\\)。"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }