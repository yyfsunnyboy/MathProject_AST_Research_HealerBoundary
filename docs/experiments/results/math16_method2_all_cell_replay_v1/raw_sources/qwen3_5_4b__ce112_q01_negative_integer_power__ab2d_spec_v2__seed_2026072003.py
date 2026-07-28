# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    base = -3
    exponent = 3
    
    correct_answer = base ** exponent
    question_text = r"Calculate the value of $(-3)^{3}$."
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": {"base": -3, "exponent": 3}
    }