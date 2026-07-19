def generate(level=1, **kwargs):
    return {
        "question_text": r"Rationalize the denominator of $\\frac{9}{4-\\\\sqrt{7}}$. Express your answer in the form $\\\\frac{A+B\\\\sqrt{C}}{D}$ where $A$, $B$, and $C$ are integers, $>0$, and square-free. What is the value of $A+B+C+D$?",
        "correct_answer": 274,
        "oracle_payload": {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    }