# -*- coding: utf-8 -*-

from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Frozen parameters for this task instance
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}

    # Compute the exact result using native Python arithmetic via FractionOps
    term1 = FractionOps.from_parts(9, 22)
    term2 = FractionOps.from_parts(11, 18)
    
    inner_parenthesis = FractionOps.sub(FractionOps.from_parts(23, 22), FractionOps.from_parts(7, 18))
    
    result = FractionOps.add(term1, FractionOps.sub(term2, inner_parenthesis))

    # Extract components for the answer schema
    numerator = result.numerator
    denominator = result.denominator
    
    # Generate canonical LaTeX string using standard formatting rules (numerator/denominator)
    if denominator == 1:
        latex_str = f"{numerator}"
    else:
        latex_str = f"${\\frac{{{numerator}}}{{denominator}}}$"

    question_text = r"\text{Compute the exact value of the expression: } \(\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})\)"
    
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