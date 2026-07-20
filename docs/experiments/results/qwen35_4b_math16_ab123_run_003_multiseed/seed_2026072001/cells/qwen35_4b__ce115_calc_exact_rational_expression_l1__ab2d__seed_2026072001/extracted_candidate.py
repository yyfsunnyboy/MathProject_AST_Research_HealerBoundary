import json
from fractions import Fraction
from typing import Dict, Any


def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {
        "products": [
            {"left": "2.79", "right": "89.3", "sign": 1},
            {"left": "-0.21", "right": "89.3", "sign": -1}
        ]
    }

    # Parse inputs as Fractions for exact arithmetic
    p1_left = Fraction("2.79")
    p1_right = Fraction("89.3")
    
    p2_left = Fraction("-0.21")
    p2_right = Fraction("89.3")

    # Calculate first product: 2.79 * 89.3
    term1 = p1_left * p1_right
    
    # Calculate second product: -0.21 * 89.3
    term2 = p2_left * p2_right

    # Sum the terms (implicit addition based on typical rational expression problems)
    total = term1 + term2

    # Format answer value as irreducible fraction string "p/q" if not integer, else just numerator
    ans_value_str = f"{total.numerator}/{total.denominator}" if total.denominator != 1 else str(total.numerator)

    correct_answer_dict = {
        "value": ans_value_str,
        "canonical_latex": r"\frac{" + str(total.numerator) + "}{" + str(total.denominator) + "}"
    }

    question_text = r"Calculate the exact value of the rational expression formed by the sum of two products: \((2.79)(89.3) + (-0.21)(89.3)\). Express your answer as an irreducible fraction \(p/q\)."

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }