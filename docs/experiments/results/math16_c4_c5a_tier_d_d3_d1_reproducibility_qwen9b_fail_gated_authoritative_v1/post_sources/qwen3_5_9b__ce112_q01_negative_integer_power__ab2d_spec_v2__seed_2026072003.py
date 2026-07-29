# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Define all frozen parameters directly as per task specification
    base = -3
    exponent = 3
    
    # Compute the exact result using native Python arithmetic
    correct_answer = base ** exponent
    
    question_text = r"Calculate $(-3)^{3}$."
    
    oracle_payload = {"base": -3, "exponent": 3}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }