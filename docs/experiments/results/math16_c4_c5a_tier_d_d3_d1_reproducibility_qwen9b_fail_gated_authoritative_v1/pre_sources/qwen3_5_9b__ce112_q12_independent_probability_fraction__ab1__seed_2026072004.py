def generate(level=1, **kwargs):
    return {
        "question_text": r"Two independent events $A$ and $B$ have probabilities of occurrence given by the fractions $\frac{p_1}{q_1}$ and $\frac{p_2}{q_2}$. Given that event $A$ occurs with probability $\frac{2}{6}$ and event $B$ occurs with probability $\frac{1}{5}$, calculate the probability of both events occurring simultaneously. Express your final answer as an irreducible fraction in LaTeX format.",
        "correct_answer": {
            "numerator": 1,
            "denominator": 30,
            "canonical_latex": r"\frac{1}{30}"
        },
        "oracle_payload": {"p1": [2, 6], "p2": [1, 5]}
    }