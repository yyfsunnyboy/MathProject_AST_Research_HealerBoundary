import json
from fractions import Fraction as PyFraction
from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse and compute the expression using Python's Fraction for exact arithmetic
    expr_str = frozen_params["expression"]
    parts = [PyFraction(x, y) if '/' in x else PyFraction(int(x)) 
             for x in str(expr_str).split('+')]
    total = sum(parts[0::2]) - sum(parts[1::2]) # Handle subtraction by negating terms
    
    numerator = total.numerator
    denominator = total.denominator
    
    correct_answer_dict = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": f"{numerator}/{denominator}" if not (total % 1 == 0) else str(int(total)) + "/" + "1" # Ensure format matches irreducible fraction requirement even for integers by keeping /1 structure or just the number if integer. The spec says 'irreducible fraction'. Usually means a/b where gcd(a,b)=1.
    }
    
    question_text = r"\text{Simplify: } $9/22 + 11/18 - (23/22 - 7/18)$"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }