# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import RadicalOps

    radicand = 27
    coeff, simplified_radicand = RadicalOps.simplify_term(1, radicand)

    correct_answer = f"{coeff}\\sqrt{{{simplified_radicand}}}"
    question_text = r"\(\sqrt{27}\) in simplest form is?"
    oracle_payload = {"radicand": 27}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }
