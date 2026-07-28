# -*- coding: utf-8 -*-

from fractions import Fraction


def generate(level=1, **kwargs):
    # Frozen sampled parameters used for this task instance
    frozen_params = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }

    # Convert decimal strings to Fractions for exact arithmetic
    def str_to_fraction(s):
        return Fraction(float(s)) if '.' in s else int(s)

    # Process the first product: left * right (positive sign)
    term1_left = str_to_fraction(frozen_params["products"][0]["left"])
    term1_right = str_to_fraction(frozen_params["products"][0]["right"])
    
    # Process the second product: left * right (negative sign, so we subtract or multiply by -1)
    term2_left = str_to_fraction(frozen_params["products"][1]["left"])
    term2_right = str_to_fraction(frozen_params["products"][1]["right"])

    # Calculate exact values using Fraction arithmetic
    val1 = term1_left * term1_right
    
    # The second operation is effectively adding (term2_left * term2_right) because sign is -1
    # But since term2_left is already negative (-0.21), multiplying by 89.3 gives a negative result.
    # With sign=-1, we are subtracting the product of absolute values? 
    # Let's interpret "sign": -1 as: result = (left * right) + (second_term_sign * second_left * second_right)
    # Or more likely based on typical expression generation patterns:
    # Expression = (2.79 * 89.3) + (-0.21 * 89.3 * -1)? 
    # Actually, looking at the structure "products": [{"left", "right", "sign"}], it implies an operation like:
    # Result = term1_left * term1_right (with sign=1 means add positive) + term2_left * term2_right (with sign=-1 means subtract? or multiply by -1?)
    
    # Let's assume the standard interpretation for such tasks: 
    # We have two terms. Term 1 is added if sign is 1, subtracted if sign is -1? 
    # Or simply: total = term1 * right + (term2_left * term2_right) * term_sign
    
    val2_base = term2_left * term2_right
    val2_adjusted = val2_base * frozen_params["products"][1]["sign"]

    final_value = val1 + val2_adjusted

    # Ensure irreducible fraction and get numerator/denominator
    num, den = final_value.numerator, final_value.denominator
    
    # Format canonical LaTeX: \frac{num}{den} if positive or negative sign handled correctly in value
    latex_str = r"\frac{" + str(num) + "}" + "/" + str(den)

    correct_answer_obj = {
        "value": f"{num}/{den}",
        "canonical_latex": latex_str
    }

    question_text = r"Calculate the exact rational expression: $2.79 \times 89.3 - (-0.21 \times 89.3)$."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_obj,
        "oracle_payload": frozen_params
    }
