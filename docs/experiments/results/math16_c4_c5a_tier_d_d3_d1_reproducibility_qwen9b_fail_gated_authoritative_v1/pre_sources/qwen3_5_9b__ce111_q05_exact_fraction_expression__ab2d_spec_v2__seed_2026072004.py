# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen sampled parameters as defined in task specification
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse and compute the expression using FractionOps
    term1 = FractionOps.create("9/22")
    term2 = FractionOps.create("11/18")
    inner_paren_1 = FractionOps.create("23/22")
    inner_paren_2 = FractionOps.create("7/18")
    
    # Compute: 9/22 + 11/18 - (23/22 - 7/18)
    part_a = term1.add(term2)
    part_b = inner_paren_1.sub(inner_paren_2)
    result = part_a.sub(part_b)
    
    # Extract components for correct_answer dict
    numerator = result.numerator
    denominator = result.denominator
    
    # Construct canonical LaTeX string: \frac{numerator}{denominator}
    import math
    if denominator < 0:
        numerator = -numerator
        denominator = -denominator
        
    canonical_latex = f"\\frac{{{numerator}}}{{{{{denominator}}}}}"
    
    # Build correct_answer dict with required fields
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": canonical_latex
    }
    
    question_text = r"Compute the exact value of $9/22 + 11/18 - (23/22 - 7/18)$."
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }