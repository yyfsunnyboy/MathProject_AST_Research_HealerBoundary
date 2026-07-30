# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import RadicalOps

def generate(level=1, **kwargs):
    radicand = 135
    coeff, simplified_radicand = RadicalOps.simplify_term(1, radicand)
    
    if coeff == 1:
        canonical_latex = f"\\sqrt{{{simplified_radicand}}}"
    else:
        canonical_latex = f"{coeff}\\sqrt{{{simplified_radicand}}}"
        
    question_text = f"Simplify the radical expression: $\\sqrt{{{radicand}}}$."
    
    correct_answer = {
        "coefficient": coeff,
        "radicand": simplified_radicand,
        "canonical_latex": canonical_latex
    }
    
    oracle_payload = {
        "radicand": radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }