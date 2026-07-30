def generate(level=1, **kwargs):
    denominator = "4-sqrt(7)"
    numerator = 9
    radicand = 7
    
    # Rationalizing 9 / (4 - sqrt(7)):
    # Multiply numerator and denominator by (4 + sqrt(7))
    # Denominator: (4 - sqrt(7))(4 + sqrt(7)) = 16 - 7 = 9
    # Numerator: 9 * (4 + sqrt(7))
    # The fraction simplifies to 4 + sqrt(7)
    # This is in the form a + sqrt(b) where a = 4 and b = 7
    # The sum a + b = 4 + 7 = 11
    correct_answer = 11
    
    question_text = (
        "Rationalize the denominator of the fraction "
        "$\\frac{9}{4 - \\sqrt{7}}$. "
        "Express your answer in the form $a + \\sqrt{b}$, "
        "where $a$ and $b$ are integers. "
        "What is the value of $a + b$?"
    )
    
    oracle_payload = {
        "denominator": denominator,
        "numerator": numerator,
        "radicand": radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }