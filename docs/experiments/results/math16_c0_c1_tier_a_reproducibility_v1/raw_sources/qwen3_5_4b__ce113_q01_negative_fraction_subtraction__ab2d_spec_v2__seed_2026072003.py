# -*- coding: utf-8 -*-

from core.prompts.domain_function_library import FractionOps


def generate(level=1, **kwargs):
    # Frozen parameters as per task specification
    frozen_params = {"expression": "3/7 - (-1/4)"}

    # Compute the exact result using native Python arithmetic for simplicity and correctness
    # 3/7 - (-1/4) is equivalent to 3/7 + 1/4
    num1, den1 = 3, 7
    num2, den2 = 1, 4
    
    common_denominator = den1 * den2
    adjusted_num1 = num1 * (common_denominator // den1)
    adjusted_num2 = num2 * (common_denominator // den2)
    
    total_numerator = adjusted_num1 + adjusted_num2
    total_denominator = common_denominator
    
    # Simplify the fraction if necessary, though 3/7 and 1/4 are already coprime with each other's denominators
    gcd_val = FractionOps.gcd(total_numerator, total_denominator)
    
    simplified_numerator = total_numerator // gcd_val
    simplified_denominator = total_denominator // gcd_val
    
    # Ensure the denominator is positive (standard form for fractions)
    if simplified_denominator < 0:
        simplified_numerator *= -1
        simplified_denominator *= -1

    correct_answer_dict = {
        "numerator": simplified_numerator,
        "denominator": simplified_denominator,
        "canonical_latex": f"{simplified_numerator}/{simplified_denominator}"
    }

    question_text = r"\text{Compute the value of: $\frac{3}{7} - \left(-\frac{1}{4}\right)$."}

    oracle_payload = frozen_params

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }
