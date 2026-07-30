def generate(level=1, **kwargs):
    quadratic_coefficients = [1, 4, -12]
    
    question_text = "Factor the polynomial $x^2 + 4x - 12$ and find its roots."
    
    # Roots are -6 and 2.
    # Factorization is (x - 2)(x + 6) or (x + 6)(x - 2).
    # Roots in ascending order: -6, 2.
    correct_answer = "Factorization: (x - 2)(x + 6), Roots: -6, 2"
    
    oracle_payload = {
        "quadratic_coefficients": quadratic_coefficients
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }