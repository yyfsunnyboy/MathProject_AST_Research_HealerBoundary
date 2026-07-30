def generate(level=1, **kwargs):
    denominator_str = "4-sqrt(7)"
    numerator = 9
    radicand = 7
    
    # Rationalizing 9 / (4 - sqrt(7)):
    # Multiply numerator and denominator by (4 + sqrt(7))
    # Denominator becomes 4^2 - 7 = 16 - 7 = 9
    # Expression becomes 9 * (4 + sqrt(7)) / 9 = 4 + 1 * sqrt(7)
    # So a = 4, b = 1
    # a + b = 5
    correct_answer = 5
    
    question_text = (
        f"Rationalize the denominator of $\\frac{{{numerator}}}{{4 - \\sqrt{{{radicand}}}}}}$. "
        f"If the simplified form is written as $a + b\\sqrt{{{radicand}}}$ where $a$ and $b$ are integers, "
        f"find the value of $a + b$."
    )
    
    oracle_payload = {
        "denominator": denominator_str,
        "numerator": numerator,
        "radicand": radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }