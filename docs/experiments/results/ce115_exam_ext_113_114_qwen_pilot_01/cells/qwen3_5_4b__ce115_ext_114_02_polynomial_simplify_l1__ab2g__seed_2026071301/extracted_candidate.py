def generate(level=1, **kwargs):
    expression = "(5*x**2 - 2*x) - (4 - 3*x)"
    
    # Parse coefficients from expression: 5x^2 - 2x + 0 - (-4 + 3x) -> 5x^2 - 2x - 4 + 3x = 5x^2 + x - 4
    coeffs = {
        '2': 5,
        '1': 1,
        '0': -4
    }
    
    correct_answer = {"coefficients": coeffs}
    oracle_payload = expression
    
    return {
        "question_text": f"Simplify the polynomial: {expression}",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }