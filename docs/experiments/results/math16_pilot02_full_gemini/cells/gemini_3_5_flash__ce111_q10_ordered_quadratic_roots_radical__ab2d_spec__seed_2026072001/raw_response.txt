# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen parameters
    oracle_payload = {
        "equation": "(x-2)^2=3",
        "order": "a>b",
        "target": "2a+b"
    }
    
    # Equation: (x-2)^2 = 3
    # Roots: x = 2 +/- sqrt(3)
    # Since a > b:
    # a = 2 + sqrt(3)
    # b = 2 - sqrt(3)
    # Target: 2a + b = 2*(2 + sqrt(3)) + (2 - sqrt(3)) = 4 + 2*sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3)
    
    question_text = (
        "Solve the quadratic equation \\((x-2)^2=3\\). "
        "Let the roots be \\(a\\) and \\(b\\) such that \\(a > b\\). "
        "Find the value of \\(2a+b\\), writing your answer in the form \\(p + q\\sqrt{r}\\) "
        "where \\(p\\), \\(q\\), and \\(r\\) are integers, and \\(r > 0\\) is square-free."
    )
    
    correct_answer = {
        "rational": 6,
        "radical_coefficient": 1,
        "radicand": 3,
        "canonical_latex": "6 + \\sqrt{3}"
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }