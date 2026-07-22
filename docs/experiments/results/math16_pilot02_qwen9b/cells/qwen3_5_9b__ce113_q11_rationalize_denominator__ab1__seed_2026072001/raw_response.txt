def generate(level=1, **kwargs):
    return {
        "question_text": r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$ and simplify to the form $a + b\sqrt{c}$ where $a$, $b$, and $c$ are integers. What is the value of $a+b+c$?",
        "correct_answer": 18,
        "oracle_payload": {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    }