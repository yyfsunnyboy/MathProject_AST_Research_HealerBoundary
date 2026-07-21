# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Rules:
    # - Do not read frozen parameters from kwargs or external state.
    # - Do not import, reference, or call IntegerOps.
    # - Use native Python arithmetic, %, **, //, loops, and comparisons.
    # - Do not use eval, exec, safe_eval, files, network, or fabricated helpers.
    # - Return exactly question_text, correct_answer, and oracle_payload.
    # - All returned values must be JSON-serializable.

    # Define all frozen parameters directly. Do not read kwargs.
    pass

    # Compute the exact result using native Python.
    pass

    correct_answer = "correct_answer"
    question_text = "question_text"
    oracle_payload = "oracle_payload"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }
