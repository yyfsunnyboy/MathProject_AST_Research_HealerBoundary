def generate(level=1, **kwargs):
    return {
        "question_text": r"Given two independent events $A$ and $B$, with probabilities $P(A) = \frac{2}{6}$ and $P(B) = \frac{1}{5}$, calculate the probability that both events occur simultaneously. Express your answer as an irreducible fraction.",
        "correct_answer": {
            "numerator": 2,
            "denominator": 30,
            "canonical_latex": r"\frac{1}{15}"
        },
        "oracle_payload": {"p1": [2, 6], "p2": [1, 5]}
    }