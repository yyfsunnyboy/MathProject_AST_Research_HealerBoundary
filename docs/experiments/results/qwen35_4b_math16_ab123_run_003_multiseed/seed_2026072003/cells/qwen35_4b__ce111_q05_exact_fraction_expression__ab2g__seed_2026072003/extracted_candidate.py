import math
from fractions import Fraction

def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Calculate the correct answer using Python's Fraction for exact arithmetic
    term1 = Fraction(9, 22)
    term2 = Fraction(11, 18)
    inner_parenthesis = Fraction(23, 22) - Fraction(7, 18)
    
    numerator_sum = term1 + term2
    
    # The expression is: (term1 + term2) - inner_parenthesis
    result_fraction = numerator_sum - inner_parenthesis
    
    # Extract components for the answer dictionary
    num_str = str(result_fraction.numerator)
    den_str = str(result_fraction.denominator)
    
    canonical_latex = f"{num_str}/{den_str}"
    
    return {
        "question_text": r"\text{Simplify the expression: } $\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$",
        "correct_answer": {
            "numerator": result_fraction.numerator,
            "denominator": result_fraction.denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }
