# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen parameters for this task instance
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Compute the exact result using native Python arithmetic (Fraction class handles reduction automatically)
    # We construct fractions manually to ensure correct handling of negative signs and subtraction
    num1, den1 = 3, 7
    num2, den2 = -1, 4
    
    # Calculate common denominator: lcm(7, 4) = 28
    # Convert both fractions to have the same denominator
    factor1, factor2 = 4, 7
    new_denom = 28
    new_num1 = num1 * factor1
    new_num2 = num2 * factor2
    
    # Perform subtraction: (new_num1 / new_denom) - (new_num2 / new_denom)
    result_numerator = new_num1 - new_num2
    result_denominator = new_denom
    
    # Ensure the fraction is irreducible and denominator is positive
    common_divisor = 1
    test_val = abs(result_numerator) if result_numerator != 0 else 1
    for i in range(2, int(test_val**0.5) + 1):
        if test_val % i == 0:
            gcd_temp = 1
            a, b = result_numerator, result_denominator
            while b:
                a, b = b, a % b
            common_divisor = abs(a)
    
    final_num = result_numerator // common_divisor
    final_denom = result_denominator // common_divisor
    
    # If numerator is negative and denominator positive, keep sign in numerator
    if final_num < 0:
        final_num = -abs(final_num)
        final_denom = abs(final_denom)
    
    correct_answer_numerator = final_num
    correct_answer_denominator = final_denom
    
    # Generate canonical LaTeX for the irreducible fraction
    latex_str = f"\\frac{{{correct_answer_numerator}}}{{correct_answer_denominator}}"

    return {
        "question_text": r"$\frac{3}{7} - \left(-\frac{1}{4}\right)$",
        "correct_answer": {
            "numerator": correct_answer_numerator,
            "denominator": correct_answer_denominator,
            "canonical_latex": latex_str
        },
        "oracle_payload": frozen_params
    }