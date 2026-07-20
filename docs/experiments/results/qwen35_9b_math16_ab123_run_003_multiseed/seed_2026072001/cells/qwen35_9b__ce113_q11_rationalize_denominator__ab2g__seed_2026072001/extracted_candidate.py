def generate(level=1, **kwargs):
    frozen_params = {"denominator": "4-sqrt(7)", "numerator": 9, "radicand": 7}
    
    # Task: Rationalize denominator for (9 / (4 - sqrt(7)))
    # Conjugate of (a - b) is (a + b). Multiply numerator and denominator by (4 + sqrt(7)).
    # New Denominator = (4)^2 - (sqrt(7))^2 = 16 - 7 = 9.
    # Numerator becomes: 9 * (4 + sqrt(7)) = 36 + 9*sqrt(7).
    # The expression is now (36 + 9*sqrt(7)) / 9.
    # Simplify by dividing terms: 36/9 + (9/9)*sqrt(7) = 4 + sqrt(7).
    
    question_text = r"Rationalize the denominator of the fraction $\frac{9}{4-\sqrt{7}}$ and simplify to a form $a+b\sqrt{n}$ where $a, b,$ and $n$ are integers. What is the value of $(a^2 + b^2)$?"
    
    # The simplified result is 4 + 1*sqrt(7). So a=4, b=1, n=7.
    # We need to calculate a^2 + b^2 = 4^2 + 1^2 = 16 + 1 = 17.
    
    correct_answer = 17
    
    oracle_payload = frozen_params

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }