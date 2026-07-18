def generate(level=1, **kwargs):
    expression = "5*x*(5*x - 2) - 4*(5*x - 2)**2"
    
    # Expand the expression to find roots:
    # Let u = (5x - 2). Expression is 5xu - 4u^2.
    # Factor out u: u(5x - 4u) -> (5x-2)(5x - 4*(5x-2))
    # Second factor: 5x - 20x + 8 = -15x + 8
    
    # Factors are (5*x - 2) and (-15*x + 8).
    
    factors_list = [
        {"x_coefficient": 5, "constant": -2},
        {"x_coefficient": -15, "constant": 8}
    ]
    
    return {
        "question_text": f"Simplify and factorize the expression: {expression}",
        "correct_answer": {
            "factors": factors_list
        },
        "oracle_payload": {"expression": "5*x*(5*x - 2) - 4*(5*x - 2)**2", "required_form": "fully_factored"}
    }