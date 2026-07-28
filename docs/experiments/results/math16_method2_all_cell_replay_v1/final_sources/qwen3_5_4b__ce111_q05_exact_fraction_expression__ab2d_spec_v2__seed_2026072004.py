# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen parameters as per task specification
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Compute the exact result using native Python arithmetic with Fractions for precision
    # The expression is: 9/22 + 11/18 - (23/22 - 7/18)
    term1 = FractionOps.from_parts(9, 22)
    term2 = FractionOps.from_parts(11, 18)
    
    # Inner parenthesis: 23/22 - 7/18
    inner_parenthesis = FractionOps.sub(FractionOps.from_parts(23, 22), FractionOps.from_parts(7, 18))
    
    # Full expression: term1 + term2 - inner_parenthesis
    result = FractionOps.add(term1, FractionOps.add(term2, FractionOps.neg(inner_parenthesis)))
    
    numerator = result.numerator
    denominator = result.denominator
    
    # Generate canonical LaTeX for the irreducible fraction
    latex_str = f"\\frac{{{numerator}}}{{denominator}}"
    
    question_text = r"\text{Simplify the expression: } \(\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})\)"
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": latex_str
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }