def generate(level=1, **kwargs):
    # The fraction is 9 / (4 - sqrt(7))
    # Rationalizing the denominator:
    # 9 * (4 + sqrt(7)) / (4^2 - 7) = 9 * (4 + sqrt(7)) / 9 = 4 + sqrt(7)
    # The simplified form is a + sqrt(b) where a = 4 and b = 7.
    # The sum a + b is 4 + 7 = 11.
    
    question_text = (
        "Rationalize the denominator of the expression $\\frac{9}{4 - \\sqrt{7}}$. "
        "If the simplified form is written as $a + \\sqrt{b}$ where $a$ and $b$ are integers, "
        "find the value of $a + b$."
    )
    correct_answer = 11
    oracle_payload = {
        "denominator": "4-sqrt(7)",
        "numerator": 9,
        "radicand": 7
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }