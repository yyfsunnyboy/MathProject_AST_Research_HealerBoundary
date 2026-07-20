def generate(level=1, **kwargs):
    return {
        "question_text": r"Find the roots of the quadratic polynomial $ax^2 + bx + c = 0$ given coefficients $a$, $b$, and $c$. Additionally, provide the factorization in the form $(x - r_1)(x - r_2)$ where $r_1 \leq r_2$.",
        "correct_answer": {
            "roots": [-4.0, 3.0],
            "factorization_latex": "(x + 4)(x - 3)",
            "roots_latex": "-4 \\text{ and } 3"
        },
        "oracle_payload": {"quadratic_coefficients": [1, 4, -12]}
    }