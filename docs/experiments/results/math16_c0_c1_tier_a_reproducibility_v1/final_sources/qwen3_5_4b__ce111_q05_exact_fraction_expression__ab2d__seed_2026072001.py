import json
from fractions import Fraction as PyFraction
from typing import Dict, Any


def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}

    # Parse and compute the expression using Python's Fraction for precision
    expr_str = str(frozen_params["expression"])
    
    # Evaluate the arithmetic manually to ensure correctness without external libraries
    term1 = PyFraction(9, 22)
    term2 = PyFraction(11, 18)
    inner_parenthesis = term2 - PyFraction(7, 18)  # Note: expression is A + B - (C - D), so it's A + B - C + D? 
    # Wait, let's re-read the frozen string carefully.
    # "9/22 + 11/18 - (23/22 - 7/18)"
    # This is equivalent to: 9/22 + 11/18 - 23/22 + 7/18
    
    a = PyFraction(9, 22)
    b = PyFraction(11, 18)
    c = PyFraction(23, 22)
    d = PyFraction(7, 18)
    
    # Calculate: a + b - (c - d) => a + b - c + d
    result = a + b - c + d
    
    numerator = result.numerator
    denominator = result.denominator

    question_text = r"\text{Simplify the expression: } \frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right)"
    
    # Construct canonical latex for irreducible fraction
    correct_answer_latex = f"\\frac{{{numerator}}}{{denominator}}"

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": correct_answer_latex
        },
        "oracle_payload": frozen_params
    }