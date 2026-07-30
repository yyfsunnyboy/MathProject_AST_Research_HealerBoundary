def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    question_text = "Factor the polynomial $P(x) = x^2 + 4x - 12$ and find its roots."
    
    correct_answer = {
        "roots": [-6, 2],
        "factorization_latex": "(x + 6)(x - 2)",
        "roots_latex": "-6, 2"
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "quadratic_coefficients": quadratic_coefficients
        }
    }