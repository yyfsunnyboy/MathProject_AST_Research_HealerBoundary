# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen sampled parameters
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse components using the API signature cards strictly
    term1 = FractionOps.create("9/22")
    term2 = FractionOps.create("11/18")
    inner_paren_1 = FractionOps.create("23/22")
    inner_paren_2 = FractionOps.create("7/18")
    
    # Compute the expression: 9/22 + 11/18 - (23/22 - 7/18)
    # Step 1: Calculate inside parentheses: 23/22 - 7/18
    inner_result = FractionOps.sub(inner_paren_1, inner_paren_2)
    
    # Step 2: Add first two terms: 9/22 + 11/18
    left_sum = FractionOps.add(term1, term2)
    
    # Step 3: Subtract the result of parentheses from the sum
    final_result = FractionOps.sub(left_sum, inner_result)
    
    numerator = final_result.numerator
    denominator = final_result.denominator
    
    # Construct canonical LaTeX for irreducible fraction
    if denominator == 1:
        latex_val = f"{numerator}"
    else:
        latex_val = rf"\frac{{{numerator}}}{{{denominator}}}"
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": latex_val
    }
    
    question_text = r"Compute the exact value of $9/22 + 11/18 - (23/22 - 7/18)$."
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }