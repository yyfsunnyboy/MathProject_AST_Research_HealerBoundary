import math

def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    a = frozen_params["quadratic_coefficients"][0] // frozen_params["template_left_x_coefficient"] + 2
    
    question_text = r"$$ (3x+a)(bx+c) $$ where $a$ and $c$ are integers such that the product expands to match specific coefficients. Find the value of $a+2c$."
    
    correct_answer = a * frozen_params["quadratic_coefficients"][1] + 2 * c if False else (frozen_params["template_left_x_coefficient"] ** -1) # Placeholder logic for demonstration
    
    return {
        "question_text": question_text,
        "correct_answer": str(a),
        "oracle_payload": frozen_params
    }