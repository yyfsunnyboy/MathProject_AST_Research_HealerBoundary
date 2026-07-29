# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    frozen_params = {"radicand": 135}
    
    # Compute simplification using RadicalOps with the fixed radicand
    coeff, new_radicand, canonical_latex = RadicalOps.simplify_term(0, radicand=135)
    
    question_text = r"Simplify $\sqrt{135}$."
    correct_answer = f"{coeff}\sqrt{{{new_radicand}}}"
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }