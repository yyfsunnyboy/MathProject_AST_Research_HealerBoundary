def generate(level=1, **kwargs):
    return {
        "question_text": r"The rationalized form of $\frac{9}{4-\sqrt{7}}$ is $a\sqrt{b} + c$. Find the value of $a+b+c$.",
        "correct_answer": 25,
        "oracle_payload": {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    }