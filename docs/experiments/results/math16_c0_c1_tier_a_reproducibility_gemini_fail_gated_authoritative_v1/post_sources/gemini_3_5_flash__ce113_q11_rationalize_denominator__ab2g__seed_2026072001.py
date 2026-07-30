def generate(level=1, **kwargs):
    # Frozen parameters
    denominator_str = "4-sqrt(7)"
    numerator = 9
    radicand = 7
    
    # Rationalizing 9 / (4 - sqrt(7))
    # Multiply numerator and denominator by (4 + sqrt(7))
    # Denominator becomes 4^2 - 7 = 16 - 7 = 9
    # Expression becomes 9 * (4 + sqrt(7)) / 9 = 4 + sqrt(7)
    # This is in the form a + b*sqrt(7) with a = 4, b = 1
    # a + b = 4 + 1 = 5
    correct_answer = 5
    
    question_text = (
        "Rationalize the denominator of $\\frac{9}{4 - \\sqrt{7}}$. "
        "If the simplified expression is written in the form $a + b\\sqrt{7}$ "
        "where $a$ and $b$ are integers, find the value of $a + b$."
    )
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {
            "denominator": denominator_str,
            "numerator": numerator,
            "radicand": radicand
        }
    }