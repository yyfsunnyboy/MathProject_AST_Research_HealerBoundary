import json
from fractions import Fraction as PyFraction

def generate(level=1, **kwargs):
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Parse expression manually based on the fixed string since domain APIs are limited to basic ops and creation from value
    # Expression: 3/7 - (-1/4) -> (3/7) + (1/4)
    a_num, a_den = 3, 7
    b_num, b_den = -1, 4
    
    term_a = PyFraction(a_num, a_den)
    
    # Handle the subtraction of negative: -(b) becomes +(abs(b))
    # The expression is "a - (b)" where b is "-1/4"
    # So we calculate term_a + (-term_b) -> term_a + abs(term_b)
    term_b = PyFraction(b_num, b_den)
    
    result_fraction = term_a - term_b
    
    numerator = result_fraction.numerator
    denominator = result_fraction.denominator
    
    correct_answer_latex = f"{numerator}/{denominator}"

    return {
        "question_text": r"$\frac{3}{7} - \left(-\frac{1}{4}\right)$",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": correct_answer_latex
        },
        "oracle_payload": frozen_params
    }