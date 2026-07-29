# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per specification
    radicand = 135
    
    # Simplify radical manually without external imports to ensure standalone correctness
    # Factorize 135: 135 = 27 * 5 = (9*3) * 5 = 3^3 * 5
    # sqrt(135) = sqrt(3^2 * 3 * 5) = 3 * sqrt(15)
    
    coefficient = 3
    simplified_radicand = 15
    
    # Construct canonical LaTeX: a\sqrt{b} -> "a\\sqrt{" + b + "}""
    question_text = f"Simplify the radical expression \\sqrt{{{radicand}}}"
    correct_answer_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_latex,
        "oracle_payload": {"radicand": radicand}
    }