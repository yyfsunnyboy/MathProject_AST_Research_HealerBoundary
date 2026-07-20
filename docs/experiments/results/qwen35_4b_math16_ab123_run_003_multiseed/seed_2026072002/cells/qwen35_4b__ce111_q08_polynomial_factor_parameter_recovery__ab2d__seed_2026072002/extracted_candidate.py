from fractions import Fraction
import math

def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    a = frozen_params["quadratic_coefficients"][0] // frozen_params["template_left_x_coefficient"]

    c = Frozen(frozen_params)
    correct_answer = int(a + 2 * c[0])
    
    return {
        "question_text": r"\text{Given the polynomial } P(x) = (3x+a)(b x^2+cx+d), \text{ where } a, b, c, d \in \mathbb{Z} \text{ and } ab=39,\ ac=-14,\ ad+b=c,\ bd+c=d. \text{ Find the value of } 5a + bc - 7d.",
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }