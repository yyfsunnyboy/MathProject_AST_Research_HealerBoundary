def generate(level=1, **kwargs):
    return {
        "question_text": r"Given two independent events with probabilities $p_1 = \frac{2}{6}$ and $p_2 = \frac{1}{5}$, what is the probability that both events occur? Express your answer as an irreducible fraction.",
        "correct_answer": {
            "numerator": 1,
            "denominator": 30,
            "canonical_latex": r"\frac{1}{30}"
        },
        "oracle_payload": {"p1": [2, 6], "p2": [1, 5]}
    }