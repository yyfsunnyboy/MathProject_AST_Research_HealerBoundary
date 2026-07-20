import json
from fractions import Fraction as PyFraction

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse and compute the expression using standard Python Fraction for accuracy
    term1 = PyFraction(9, 22)
    term2 = PyFraction(11, 18)
    inner_parenthesis = term23_22 - PyFraction(7, 18)
    
    # Compute: (a + b) - c where a=9/22, b=11/18, c=(23/22-7/18)
    result = term1 + term2 - inner_parenthesis
    
    numerator = result.numerator
    denominator = result.denominator
    
    # Construct the correct answer structure
    correct_answer = {
        "numerator": str(numerator),
        "denominator": str(denominator),
        "canonical_latex": f"{numerator}/{denominator}" if numerator != 1 else "1" + "/" + str(0) or "" # Handle edge case where denom is 1, but here it's not. Just standard latex.
    }
    
    question_text = r"\text{Evaluate the following expression: $9/22 + 11/18 - (23/22 - 7/18)$}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }