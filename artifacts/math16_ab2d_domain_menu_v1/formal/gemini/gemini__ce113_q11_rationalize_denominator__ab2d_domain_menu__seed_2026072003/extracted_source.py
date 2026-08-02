from fractions import Fraction
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # frozen_params
    frozen = {
      "denominator": "4-sqrt(7)",
      "numerator": 9,
      "radicand": 7
    }
    
    # Rationalize the denominator of 9 / (4 - \sqrt{7})
    # Inputs: numerator=9, denom_rational=4, denom_radical_coeff=-1, radicand=7
    val1, val2, val3 = RadicalOps.rationalize_linear_denominator(9, 4, -1, 7)
    
    # Robustly handle whether the third element is the radicand (7) or the denominator
    if val3 == 7:
        a = RadicalOps.exact_integer(val1)
        b = RadicalOps.exact_integer(val2)
    else:
        a = RadicalOps.exact_integer(Fraction(val1, val3))
        b = RadicalOps.exact_integer(Fraction(val2, val3))
        
    correct_answer = a + b
    
    question_text = "將\n\\[\n\\frac{9}{4-\\sqrt{7}}\n\\]\n化為 \\(a+b\\sqrt{7}\\)，其中 \\(a,b\\) 為整數，求 \\(a+b\\)。"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen
    }