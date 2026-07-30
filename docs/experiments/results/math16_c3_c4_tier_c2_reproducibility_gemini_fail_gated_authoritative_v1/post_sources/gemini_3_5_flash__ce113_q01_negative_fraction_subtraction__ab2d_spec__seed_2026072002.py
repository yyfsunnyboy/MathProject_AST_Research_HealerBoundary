# -*- coding: utf-8 -*-

from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    expression = "3/7 - (-1/4)"
    
    # Create fraction objects for 3/7 and -1/4
    f1 = FractionOps.create(3, 7)
    f2 = FractionOps.create(-1, 4)
    
    # Perform subtraction: 3/7 - (-1/4)
    result = FractionOps.sub(f1, f2)
    
    # Extract numerator, denominator, and LaTeX representation
    num = FractionOps.numerator(result)
    den = FractionOps.denominator(result)
    latex = FractionOps.to_latex(result)
    
    # Format the question text with formal LaTeX delimiters
    question_text = r"Evaluate the expression: \[\frac{3}{7} - \left(-\frac{1}{4}\right)\]"
    
    correct_answer = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": latex
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "expression": expression
        }
    }