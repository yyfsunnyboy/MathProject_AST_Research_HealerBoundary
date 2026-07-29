# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Compute the exact result using native Python arithmetic for simplicity and correctness here.
    # 3/7 - (-1/4) = 3/7 + 1/4 = (3*4)/(7*4) + (1*7)/(4*7) = 12/28 + 7/28 = 19/28
    numerator = 19
    denominator = 28
    
    # Verify irreducibility: gcd(19, 28) is 1.
    
    question_text = r"\text{Compute the difference of fractions: } \frac{3}{7} - \left(-\frac{1}{4}\right)"
    
    correct_answer = {
        "numerator": numerator,
        "denominator": denominator,
        "canonical_latex": f"\\frac{{{numerator}}}{{"{denominator}"}}"
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }