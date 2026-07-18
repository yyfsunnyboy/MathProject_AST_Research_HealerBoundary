def generate(level=1, **kwargs):
    oracle_payload = {
        "expression": "5*x*(5*x - 2) - 4*(5*x - 2)**2",
        "required_form": "fully_factored"
    }
    
    question_text = "Factor the following expression completely:\n\n5x(5x - 2) - 4(5x - 2)^2"
    
    correct_answer = {
        "factors": [
            {"x_coefficient": 5, "constant": -2},
            {"x_coefficient": -15, "constant": 8}
        ]
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }