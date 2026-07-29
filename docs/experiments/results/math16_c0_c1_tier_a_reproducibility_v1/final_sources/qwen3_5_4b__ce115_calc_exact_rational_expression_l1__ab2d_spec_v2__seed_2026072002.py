# -*- coding: utf-8 -*-

from fractions import Fraction as F


def generate(level=1, **kwargs):
    # Frozen sampled parameters used exactly here
    frozen_params = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }

    # Convert decimal strings to exact fractions
    p1_left = F("279/100")
    p1_right = F(893) / 10
    
    p2_left = F(-21) / 100
    p2_right = F(893) / 10

    # Compute first product: (2.79 * 89.3) -> exact fraction multiplication
    term1_num, term1_den = p1_left * p1_right
    
    # Compute second product: (-0.21 * 89.3) -> exact fraction multiplication with sign handling
    # Note: -0.21 is already negative in F(-21/100), so direct mul handles the sign
    term2_num, term2_den = p2_left * p2_right

    # Compute final result: (term1 + term2) -> exact fraction addition/subtraction
    total_num, total_den = term1_num + term2_num
    
    # Ensure irreducible form and positive denominator for canonical representation
    if total_den < 0:
        total_num *= -1
        total_den *= -1

    def format_fraction(numerator):
        """Returns string 'p/q' where q is the denominator."""
        return f"{numerator}/{total_den}"

    # Generate LaTeX for exact rational expression
    latex_str = r"\frac{" + str(total_num) + "}{"} + str(total_den) + r"}"

    correct_answer_value = format_fraction(total_num)
    
    question_text = (r"$\text{Calculate the value of: } 2.79 \times 89.3 + (-0.21) \times 89.3$")

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_value,
        "oracle_payload": frozen_params
    }
