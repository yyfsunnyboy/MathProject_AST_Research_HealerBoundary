def generate(level=1, **kwargs):
    return {
        "question_text": r"Given two independent events $A$ and $B$, where $P(A) = \frac{2}{6}$ and $P(B) = \frac{1}{5}$, calculate the probability of both events occurring together ($P(A \cap B)$). Express your answer as an irreducible fraction.",
        "correct_answer": {
            "numerator": 1,
            "denominator": 30,
            "canonical_latex": r"\frac{1}{30}"
        },
        "oracle_payload": {"p1": [2, 6], "p2": [1, 5]}
    }