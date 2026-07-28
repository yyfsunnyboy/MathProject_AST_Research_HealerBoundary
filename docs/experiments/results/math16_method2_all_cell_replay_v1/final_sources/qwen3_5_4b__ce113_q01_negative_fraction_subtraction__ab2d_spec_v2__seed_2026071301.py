# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen parameters for this task instance
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Compute the exact result using native Python arithmetic with fractions to ensure precision and irreducibility
    # 3/7 - (-1/4) is equivalent to 3/7 + 1/4
    num1, den1 = 3, 7
    num2, den2 = 1, 4
    
    common_denominator = den1 * den2
    adjusted_num1 = num1 * (common_denominator // den1)
    adjusted_num2 = num2 * (common_denominator // den2)
    
    final_numerator = adjusted_num1 + adjusted_num2
    final_denominator = common_denominator
    
    # Ensure irreducibility by dividing out GCD
    import math
    gcd_val = math.gcd(final_numerator, final_denominator)
    canonical_numer = final_numerator // gcd_val
    canonical_denom = final_denominator // gcd_val
    
    correct_answer_data = {
        "numerator": canonical_numer,
        "denominator": canonical_denom,
        "canonical_latex": f"\\frac{{{canonical_numer}}}{{{canonical_denom}}}"
    }
    
    question_text = r"\textbf{Question:} Compute the difference of fractions. \[ 3/7 - (-1/4) \]"
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_data,
        "oracle_payload": oracle_payload
    }