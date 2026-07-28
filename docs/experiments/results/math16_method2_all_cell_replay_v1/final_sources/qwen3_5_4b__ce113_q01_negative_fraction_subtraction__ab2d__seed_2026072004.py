import json
from fractions import Fraction as PyFraction
from typing import Dict, Any


def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Parse the expression manually to ensure correctness for this specific case
    # 3/7 - (-1/4) is equivalent to 3/7 + 1/4
    
    a_num, a_den = 3, 7
    b_num, b_den = -1, 4
    
    # Perform subtraction: (a/b) - (c/d) = (ad - bc) / bd
    numerator = a_num * b_den - b_num * a_den
    denominator = a_den * b_den
    
    # Simplify fraction to ensure irreducibility
    common_divisor = PyFraction(numerator).gcd(PyFraction(denominator))
    
    final_numerator = numerator // int(common_divisor)
    final_denominator = denominator // int(common_divisor)
    
    if final_denominator < 0:
        # Ensure canonical form (negative sign in numerator only)
        final_numerator *= -1
        final_denominator *= -1
    
    correct_answer_dict = {
        "numerator": final_numerator,
        "denominator": final_denominator,
        "canonical_latex": f"{final_numerator}/{final_denominator}" if final_numerator != 0 else str(final_numerator)
    }
    
    question_text = r"\text{Calculate: $\frac{3}{7} - \left(-\frac{1}{4}\right)$}"
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }