# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters
    denominator = "4-sqrt(7)"
    numerator = 9
    radicand = 7

    # Rationalizing 9 / (4 - sqrt(7))
    # Multiply numerator and denominator by (4 + sqrt(7))
    # Denominator becomes 4^2 - 7 = 16 - 7 = 9
    # Numerator becomes 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7)
    # Dividing by 9 gives 4 + 1*sqrt(7)
    # So a = 4, b = 1
    # a + b = 5
    correct_answer = 5

    question_text = (
        "Rationalize the denominator of the expression "
        "$\\frac{9}{4 - \\sqrt{7}}$. "
        "If the simplified expression is written in the form $a + b\\sqrt{7}$ "
        "where $a$ and $b$ are integers, find the value of $a + b$."
    )

    oracle_payload = {
        "denominator": denominator,
        "numerator": numerator,
        "radicand": radicand
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }