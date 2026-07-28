import json
from fractions import Fraction as PyFraction
from typing import Dict, Any


def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Parse the expression manually to ensure correct handling of negative signs in subtraction context
    # Expression: 3/7 - (-1/4) is equivalent to 3/7 + 1/4
    
    term_a_num = 3
    term_a_den = 7
    term_b_num = -(-1)  # The expression has a double negative for the numerator part in context of subtraction: -( -1 ) -> +1, but we subtract (-1/4), so it's adding (1/4). 
                        # Let's re-evaluate based on standard math parsing.
    # "3/7 - (-1/4)" means 3/7 minus negative one quarter.
    # This is equivalent to 3/7 + 1/4.
    
    a = PyFraction(term_a_num, term_a_den)
    b = PyFraction(0, 1)
    
    # The second part is -(-1/4). 
    # We are subtracting the fraction (-1)/4.
    subtrahend_numerator = -1
    subtrahend_denominator = 4
    
    # Calculate: a - (subtrahend_numerator / subtrahend_denominator)
    result_fraction = a - PyFraction(subtrahend_numerator, subtrahend_denominator)
    
    numerator = result_fraction.numerator
    denominator = result_fraction.denominator
    
    canonical_latex = f"{numerator}/{denominator}"
    
    question_text = r"\text{Calculate: } $\frac{3}{7} - \left(-\frac{1}{4}\right)$"
    
    correct_answer_dict = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }