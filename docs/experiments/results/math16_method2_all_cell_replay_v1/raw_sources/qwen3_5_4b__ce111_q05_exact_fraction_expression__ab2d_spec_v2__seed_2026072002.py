# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen parameters as per task specification
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Compute the exact result using native Python arithmetic for precision and simplicity
    # Expression: 9/22 + 11/18 - (23/22 - 7/18)
    term1 = FractionOps.from_parts(9, 22)
    term2 = FractionOps.from_parts(11, 18)
    
    inner_parenthesis = FractionOps.sub(FractionOps.from_parts(23, 22), FractionOps.from_parts(7, 18))
    
    result = FractionOps.add(term1, FractionOps.add(term2, FractionOps.neg(inner_parenthesis)))
    
    # Format the answer components
    numerator = result.numerator
    denominator = result.denominator
    
    # Generate canonical LaTeX for irreducible fraction
    latex_str = f"\\frac{{{numerator}}}{{denominator}}" if (numerator < 0 and denominator > 0) else f"\\frac{{{abs(numerator)}}}{{abs(denominator)}}" * (-1 if numerator < 0 else 1)
    
    # Construct the question text with formal LaTeX delimiters
    expression_latex = r"\text{9/22 + 11/18 - (23/22 - 7/18)}"
    question_text = f"Evaluate the following exact fraction expression: {expression_latex}"

    # Prepare correct_answer dict structure as per requirements
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": latex_str if (numerator < 0 and denominator > 0) else f"\\frac{{{abs(numerator)}}}{{abs(denominator)}}" * (-1 if numerator < 0 else 1), # Re-evaluating logic for negative numerators in LaTeX
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }