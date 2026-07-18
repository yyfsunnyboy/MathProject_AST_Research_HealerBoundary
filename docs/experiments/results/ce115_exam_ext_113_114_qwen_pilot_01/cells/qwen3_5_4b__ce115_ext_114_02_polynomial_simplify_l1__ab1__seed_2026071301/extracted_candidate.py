def generate(level=1, **kwargs):
    expression = "(5*x**2 - 2*x) - (4 - 3*x)"
    
    # Parse and simplify the polynomial: (5x^2 - 2x) - (4 - 3x) = 5x^2 - 2x - 4 + 3x = 5x^2 + x - 4
    
    coefficients = {
        "2": 5,
        "1": 1,
        "0": -4
    }
    
    return {
        "question_text": expression,
        "correct_answer": {"coefficients": coefficients},
        "oracle_payload": {"expression": "(5*x**2 - 2*x) - (4 - 3*x)"}
    }