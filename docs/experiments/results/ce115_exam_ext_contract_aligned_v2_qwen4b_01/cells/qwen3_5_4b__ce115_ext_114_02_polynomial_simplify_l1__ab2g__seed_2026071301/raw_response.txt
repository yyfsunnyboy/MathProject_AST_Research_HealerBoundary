def generate(level=1, **kwargs):
    expression = "(5*x**2 - 2*x) - (4 - 3*x)"
    
    # Parse coefficients from the given polynomial: 5x^2 - 2x - 4 + 3x
    # Combine like terms: x^2 term is 5, x terms are (-2 + 3) = 1, constant is -4
    
    coeffs_2 = 5
    coeffs_1 = 1
    coeffs_0 = -4
    
    correct_answer = {
        "coefficients": {
            "2": coeffs_2,
            "1": coeffs_1,
            "0": coeffs_0
        }
    }
    
    return {
        "question_text": expression,
        "correct_answer": correct_answer,
        "oracle_payload": {"expression": "(5*x**2 - 2*x) - (4 - 3*x)"}
    }