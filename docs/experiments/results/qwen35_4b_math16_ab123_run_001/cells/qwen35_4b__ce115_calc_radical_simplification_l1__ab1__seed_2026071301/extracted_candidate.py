def generate(level=1, **kwargs):
    return {
        "question_text": r" Simplify the radical $\sqrt[3]{27}$. Express your answer in the form $a\sqrt[n]{b}$ where $a$ is an integer coefficient and $b$ is a positive integer radicand such that no factor of $n$ divides any exponent in the prime factorization of $b$.",
        "correct_answer": {
            "coefficient": 3,
            "radicand": 1,
            "canonical_latex": "$3\\sqrt[3]{1}$"
        },
        "oracle_payload": {"radicand": 27}
    }