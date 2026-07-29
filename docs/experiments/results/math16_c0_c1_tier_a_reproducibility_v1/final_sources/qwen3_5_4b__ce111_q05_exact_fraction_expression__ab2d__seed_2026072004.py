import json
from fractions import Fraction as PyFraction
from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse and compute the expression using Python's Fraction for exact arithmetic
    term1 = PyFraction(9, 22)
    term2 = PyFraction(11, 18)
    inner_parenthesis = term23_22_minus_term7_18 := (PyFraction(23, 22) - PyFraction(7, 18))
    
    # Note: The expression is A + B - (C - D). 
    # In Python operator precedence handles this correctly as ((A+B)-(C-D)).
    result = term1 + term2 - inner_parenthesis
    
    numerator = str(result.numerator)
    denominator = str(result.denominator)
    
    canonical_latex = f"{numerator}/{denominator}" if not (result.denominator == 1 and int(numerator) > 0):
        # If it's an integer, standard LaTeX for fractions usually keeps the slash or writes as mixed number. 
        # However, "irreducible fraction" implies keeping the form a/b even if b=1 is often expected in these contexts unless specified otherwise (e.g., improper vs proper).
        # Let's stick to the raw numerator/denominator format for consistency with typical math problem outputs unless it simplifies nicely. 
        # Actually, standard LaTeX \frac{a}{b} works fine even if b=1. But let's check if we should convert integer result.
        # The prompt asks for "canonical_latex for an irreducible fraction". 23/4 is a fraction. 57/6 simplifies to 19/2. 
        # If the result was 5, it might be expected as \frac{5}{1} or just 5. Given the input format (fractions), outputting \frac{n}{d} where d=1 is safe for "fraction".
        pass
    
    question_text = r"\textbf{Question: } Evaluate the expression and express your answer as an irreducible fraction.\n\n\$\$ $9/22 + 11/18 - (23/22 - 7/18)$ \$\$ \\\\"
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }