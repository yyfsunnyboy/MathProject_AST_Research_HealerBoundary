def generate(level=1, **kwargs):
    return {
        "question_text": r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$ and express your answer in the form $a + b\sqrt{n}$ where $n > 0$, $b \neq 0$, and all quantities are integers. What is the value of $|a|$?",
        "correct_answer": 16,
        "oracle_payload": {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    }