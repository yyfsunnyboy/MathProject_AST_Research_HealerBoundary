import math
from fractions import Fraction

def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Calculate correct answer using Fractions for precision
    term1 = Fraction(3) / 7
    term2 = Fraction(-1) / 4
    
    result = term1 - term2
    
    numerator = result.numerator
    denominator = result.denominator
    
    canonical_latex = f"{numerator}/{denominator}"
    
    question_text = r"Calculate the difference: $\frac{3}{7} - \left(-\frac{1}{4}\right)$."
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {'expression': '3/7 - (-1/4)'}
    }