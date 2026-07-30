def generate(level=1, **kwargs):
    # Frozen parameters
    quadratic_coefficients = [1, 4, -12]

    # Roots of x^2 + 4x - 12 = 0 are -6 and 2
    roots = [-6, 2]
    factorization_latex = "(x + 6)(x - 2)"
    roots_latex = "x = -6, 2"

    question_text = "Factor the quadratic polynomial $x^2 + 4x - 12$ and find its roots."

    correct_answer = {
        "roots": roots,
        "factorization_latex": factorization_latex,
        "roots_latex": roots_latex,
    }

    oracle_payload = {
        "quadratic_coefficients": quadratic_coefficients
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }