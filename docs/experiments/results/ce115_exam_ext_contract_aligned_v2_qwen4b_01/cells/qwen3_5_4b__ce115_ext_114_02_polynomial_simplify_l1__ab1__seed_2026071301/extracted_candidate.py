def generate(level=1, **kwargs):
    expression = "(5*x**2 - 2*x) - (4 - 3*x)"
    
    # Parse and simplify the polynomial: (5x^2 - 2x) - (4 - 3x) = 5x^2 - 2x - 4 + 3x = 5x^2 + x - 4
    # Coefficients for degree 2, 1, and 0 are 5, 1, and -4 respectively.
    
    correct_answer = {
        "coefficients": {
            "2": 5,
            "1": 1,
            "0": -4
        }
    }
    
    oracle_payload = {"expression": "(5*x**2 - 2*x) - (4 - 3*x)"}
    
    return {
        "question_text": expression,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }