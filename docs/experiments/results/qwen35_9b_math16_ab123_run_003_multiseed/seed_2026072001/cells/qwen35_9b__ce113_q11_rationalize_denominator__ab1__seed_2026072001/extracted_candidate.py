def generate(level=1, **kwargs):
    return {
        "question_text": r"Rationalize the denominator of $\frac{9}{4-\sqrt{7}}$ and simplify to the form $A + B\sqrt{C}$ where $A$, $B$, and $C$ are integers. What is the value of $A+B+C$?",
        "correct_answer": 18,
        "oracle_payload": {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    }