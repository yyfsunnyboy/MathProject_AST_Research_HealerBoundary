# -*- coding: utf-8 -*-
from fractions import Fraction

def generate(level=1, **kwargs):
    # Frozen sampled parameters as defined in task specification
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Helper to convert decimal string to Fraction
    def str_to_frac(s):
        return Fraction(int(float(s) * 100), 100).limit_denominator()

    left1 = str_to_frac(frozen_params["products"][0]["left"])
    right1 = str_to_frac(frozen_params["products"][0]["right"])
    sign1 = frozen_params["products"][0]["sign"]

    left2 = str_to_frac(frozen_params["products"][1]["left"])
    right2 = str_to_frac(frozen_params["products"][1]["right"])
    sign2 = frozen_params["products"][1]["sign"]

    # Compute expression: (left1 * right1) + (left2 * right2) based on signs
    term1 = left1 * right1 if sign1 == 1 else -left1 * right1
    term2 = left2 * right2 if sign2 == 1 else -left2 * right2

    result_frac = term1 + term2
    # Simplify to irreducible form (Fraction does this automatically)
    
    canonical_latex = f"\\frac{{{result_frac.numerator}}}{{{{{result_frac.denominator}}}}}"
    
    question_text = r"The value of the expression $(\text{left}_1 \times \text{right}_1)$ plus or minus $(\text{left}_2 \times \text{right}_2)$ is requested. Compute: $({} + {})$."

    correct_answer_dict = {
        "value": f"{result_frac.numerator}/{result_frac.denominator}",
        "canonical_latex": canonical_latex
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }