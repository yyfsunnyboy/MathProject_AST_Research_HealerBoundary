def generate(level=1, **kwargs):
    return {
        "question_text": r"$$\sqrt{135} = a \cdot \sqrt{b}$$ where $a$ and $b$ are integers with no square factors in $b$. Find the values of $a$, $b$, and write them as $\text{{coeff}}, \text{{radicand}}$.",
        "correct_answer": {
            "coefficient": 3,
            "radicand": 5,
            "canonical_latex": r"$$\sqrt{135} = 3\sqrt{5}$$"
        },
        "oracle_payload": {"radicand": 135}
    }