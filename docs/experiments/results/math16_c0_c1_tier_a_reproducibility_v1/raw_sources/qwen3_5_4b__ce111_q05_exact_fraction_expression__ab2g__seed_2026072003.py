import fractions
from typing import Dict, Any

def generate(level: int = 1, **kwargs) -> Dict[str, Any]:
    question_text = r"\text{Simplify the expression } \frac{9}{22} + \frac{11}{18} - \left( \frac{23}{22} - \frac{7}{18} \right)."
    
    # Calculate the correct answer using fractions module for precision
    term1 = fractions.Fraction(9, 22)
    term2 = fractions.Fraction(11, 18)
    inner_parenthesis = fractions.Fraction(23, 22) - fractions.Fraction(7, 18)
    
    result = term1 + term2 - inner_parenthesis
    
    numerator = result.numerator
    denominator = result.denominator
    
    canonical_latex = f"\\frac{{{numerator}}}{{denominator}}" if (numerator == 0 or denominator != abs(numerator)) else "integer_value" # Simplified logic for display, but we need the fraction form specifically requested. 
    # Re-evaluating based on standard output requirements:
    canonical_latex = f"\frac{{{numerator}}}{{denominator}}"

    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = kwargs
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }