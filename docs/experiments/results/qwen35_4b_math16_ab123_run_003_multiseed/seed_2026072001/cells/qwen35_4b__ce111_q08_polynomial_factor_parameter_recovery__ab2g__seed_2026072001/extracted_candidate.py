def generate(level=1, **kwargs):
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }
    
    a, b, c = frozen_params["quadratic_coefficients"]
    
    question_text = r"\text{Given the polynomial } P(x) = ax^2 + bx + c \text{ with coefficients } [a, b, c] = [\underline{\mathbf{39}}, 5, -14], \text{ find the integer value of } a+2c \text{ assuming one factor is fixed as } (3x+\underline{\mathbf{a}}) \text{ and the other linear term contributes to forming the product.}"
    
    correct_answer = int(a + 2 * c)
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }