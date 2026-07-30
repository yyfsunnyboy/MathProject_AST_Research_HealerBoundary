# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    base = -3
    exponent = 3

    # Compute the exact result
    correct_answer = base ** exponent

    # Format the question text with LaTeX delimiters
    question_text = f"What is the value of $({base})^{{{exponent}}}$?"

    oracle_payload = {
        "base": base,
        "exponent": exponent
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }