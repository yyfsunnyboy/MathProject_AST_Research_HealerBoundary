# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    radicand = 27
    
    # Simplify radical sqrt(27) -> a*sqrt(b)
    # 27 = 9 * 3 = (3^2) * 3
    # sqrt(27) = 3 * sqrt(3)
    
    coefficient = 3
    simplified_radicand = 3
    
    # Construct canonical LaTeX: a\sqrt{b} -> 3\sqrt{3}
    question_text = r"Simplify the radical expression $\sqrt{" + str(radicand) + "}$."
    correct_answer = f"{coefficient}\\sqrt{{{simplified_radicand}}}"
    
    # Oracle payload must exactly equal frozen sampled parameters
    oracle_payload = {"radicand": radicand}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }