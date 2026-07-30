# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Compute using FractionOps
    f9_22 = FractionOps.create(9, 22)
    f11_18 = FractionOps.create(11, 18)
    f23_22 = FractionOps.create(23, 22)
    f7_18 = FractionOps.create(7, 18)
    
    # 23/22 - 7/18
    sub_part = FractionOps.sub(f23_22, f7_18)
    # 9/22 + 11/18
    add_part = FractionOps.add(f9_22, f11_18)
    # (9/22 + 11/18) - (23/22 - 7/18)
    res = FractionOps.sub(add_part, sub_part)
    
    # Extract numerator and denominator
    num = res.numerator
    den = res.denominator
    
    # Format canonical LaTeX
    if den == 1:
        canonical_latex = str(num)
    else:
        canonical_latex = f"\\frac{{{num}}}{{{den}}}"
        
    question_text = f"Evaluate the following expression:\n\n\\[ {expression} \\]"
    
    correct_answer = {
        "numerator": num,
        "denominator": den,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = {
        "expression": expression
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }