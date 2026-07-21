import json
from fractions import Fraction as PyFraction
from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse the expression manually to ensure correctness without external dependencies beyond standard library
    expr_str = str(frozen_params["expression"])
    
    # Evaluate using Python's Fraction for exact arithmetic
    parts = [PyFraction(9, 22), PyFraction(11, 18)]
    sub_parts = [PyFraction(23, 22), PyFraction(7, 18)]
    
    result_addition = sum(parts) - sum(sub_parts)
    
    # Convert to canonical form (numerator/denominator) and LaTeX string
    numerator = str(result_addition.numerator)
    denominator = str(result_addition.denominator)
    latex_str = f"{result_addition}"  # Python Fraction __str__ returns irreducible fraction
    
    question_text = r"\text{Simplify the expression: } $9/22 + 11/18 - (23/22 - 7/18)$"
    
    correct_answer_dict = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": latex_str
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }