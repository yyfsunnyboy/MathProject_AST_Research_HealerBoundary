# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per specification
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse components from the expression string to build fractions explicitly
    # Expression: 9/22 + 11/18 - (23/22 - 7/18)
    # Term 1: 9/22
    t1 = FractionOps.from_parts(9, 22)
    
    # Term 2: 11/18
    t2 = FractionOps.from_parts(11, 18)
    
    # Inner parenthesis term A: 23/22
    inner_a = FractionOps.from_parts(23, 22)
    
    # Inner parenthesis term B: 7/18
    inner_b = FractionOps.from_parts(7, 18)
    
    # Compute inner difference: (23/22 - 7/18)
    inner_diff = FractionOps.sub(inner_a, inner_b)
    
    # Full expression: t1 + t2 - inner_diff
    result_sum = FractionOps.add(t1, t2)
    final_result = FractionOps.sub(result_sum, inner_diff)
    
    # Extract numerator and denominator from the resulting fraction object
    num = final_result.numerator
    den = final_result.denominator
    
    # Construct canonical LaTeX for an irreducible fraction: \frac{num}{den}
    canonical_latex = f"\\frac{{{num}}}{{{den}}}"
    
    question_text = r"The value of the expression $9/22 + 11/18 - (23/22 - 7/18)$ is equal to:"
    correct_answer = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }