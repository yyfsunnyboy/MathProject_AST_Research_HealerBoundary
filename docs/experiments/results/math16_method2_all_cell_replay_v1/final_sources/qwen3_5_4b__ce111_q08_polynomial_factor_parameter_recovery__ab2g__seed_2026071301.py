def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    a = frozen_params["quadratic_coefficients"][0] // frozen_params["template_left_x_coefficient"] + 2 * (frozen_params["quadratic_coefficients"][1] / frozen_params["template_left_x_coefficient"]) - (frozen_params["quadratic_coefficients"][2] / (frozen_params["template_left_x_coefficient"] ** 2))
    c = a
    
    question_text = r"\text{Given the polynomial } P(x) = ax^2 + bx + c \text{ with coefficients derived from factorization, find the value of } a+2c."
    
    correct_answer = int(a + 2 * c)
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }