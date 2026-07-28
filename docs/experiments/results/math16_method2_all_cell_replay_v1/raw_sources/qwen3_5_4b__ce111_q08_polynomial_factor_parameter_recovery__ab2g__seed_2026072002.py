def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    if level == 1:
        a = 20
        c = 7
        
        question_text = r"$$ \text{Given the polynomial } P(x) = (3x+a)(bx+c), \text{ where } b=5, \text{ find the value of } a+2c. $$"
        
        correct_answer = int(a + 2 * c)
    else:
        raise ValueError("Level not supported")

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }