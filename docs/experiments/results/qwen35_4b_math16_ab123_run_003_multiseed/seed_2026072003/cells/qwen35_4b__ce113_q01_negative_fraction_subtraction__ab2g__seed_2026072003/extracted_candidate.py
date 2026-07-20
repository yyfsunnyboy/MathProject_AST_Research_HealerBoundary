import math
from fractions import Fraction

def generate(level=1, **kwargs):
    frozen_params = {"expression": "3/7 - (-1/4)"}
    
    # Parse expression manually to ensure correctness for this specific case
    numerator_top = 3
    denominator_top = 7
    
    numerator_bottom = -1
    denominator_bottom = 4
    
    # Calculate common denominator: lcm(7, 4) = 28
    common_denominator = 28
    
    # Adjust numerators to the common denominator
    adjusted_numerator_top = (numerator_top * common_denominator // denominator_top)
    adjusted_numerator_bottom = (numerator_bottom * common_denominator // denominator_bottom)
    
    # Perform subtraction: num1/den - (-num2)/den = num1 + num2 / den
    final_numerator = adjusted_numerator_top - adjusted_numerator_bottom
    
    # Simplify the fraction using Fraction class logic manually to ensure irreducibility matches requirements
    common_divisor = math.gcd(final_numerator, common_denominator)
    
    if common_divisor != 1:
        simplified_numerator = final_numerator // common_divisor
        simplified_denominator = common_denominator // common_divisor
        
        # Ensure denominator is positive (standard form for negative fractions)
        if simplified_denominator < 0:
            simplified_numerator *= -1
            simplified_denominator *= -1
            
    else:
        simplified_numerator = final_numerator
        simplified_denominator = common_denominator
    
    canonical_latex = f"{simplified_numerator}/{simplified_denominator}"
    
    return {
        "question_text": r"$\frac{3}{7} - \left(-\frac{1}{4}\right)$",
        "correct_answer": {
            "numerator": simplified_numerator,
            "denominator": simplified_denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }
