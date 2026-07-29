# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen parameters must be used exactly as specified in the task specification.
    frozen_expression = "3/7 - (-1/4)"
    
    # Parse and compute using native Python arithmetic for simplicity given the small expression size, 
    # ensuring irreducible fraction output via standard math operations which Fraction handles automatically.
    # We construct fractions manually to avoid API misuse while adhering to logic requirements.
    num1 = 3
    den1 = 7
    num2 = -(-1)  # This is effectively +1, but we treat the term as (-1/4), so subtracting it means adding positive part? 
                 # Wait: Expression is "3/7 - (-1/4)". Subtracting a negative fraction adds its value.
                 # So mathematically: (3/7) + (1/4).
    den2 = 4
    
    # Compute common denominator and result using native arithmetic to ensure correctness without API overhead for simple ops,
    # then format as required by the task specification schema.
    
    lcm_denominator = den1 * den2 // math.gcd(den1, den2) if False else (den1 * den2) 
    # Since gcd is not imported yet and logic is trivial: 7*4=28
    
    common_num1 = num1 * (lcm_denominator // den1)
    common_num2 = -num2 * (lcm_denominator // den2) if False else (-(-1)) * (lcm_denominator // den2) # Actually we are subtracting the fraction. 
    # Let's re-evaluate: 3/7 - (-1/4). This is equivalent to adding 1/4.
    # Term A: 3/7 -> numerator 3, denominator 7
    # Term B: -(-1/4) = +1/4 -> we are ADDING this term in the subtraction operation? 
    # No, standard order of operations: subtract (-1/4). So add (1/4).
    
    # Let's stick to strict Fraction logic without external imports if possible or use minimal math.
    import math
    
    common_den = 28
    adjusted_num_3over7 = 3 * 4  # 12
    adjusted_num_pos_one_over_4 = 1 * 7  # 7 (since we are adding)
    
    final_numerator = adjusted_num_3over7 + adjusted_num_pos_one_over_4
    final_denominator = common_den
    
    from fractions import Fraction as PyFraction
    
    res_frac = PyFraction(final_numerator, final_denominator)
    
    # Format correct_answer with numerator, denominator, and canonical_latex
    num_str = str(res_frac.numerator)
    den_str = str(res_frac.denominator)
    latex_num = r"\frac{" + num_str + "}{\text{" + den_str + "} }" if False else f"{num_str}\\over{den_str}" # Standard LaTeX fraction
    
    correct_answer_dict = {
        "numerator": res_frac.numerator,
        "denominator": res_frac.denominator,
        "canonical_latex": r"\frac{" + str(res_frac.numerator) + "}{" + str(res_frac.denominator) + "}"
    }

    question_text = f"Compute the value of: {frozen_expression}."
    
    oracle_payload = frozen_expression
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }