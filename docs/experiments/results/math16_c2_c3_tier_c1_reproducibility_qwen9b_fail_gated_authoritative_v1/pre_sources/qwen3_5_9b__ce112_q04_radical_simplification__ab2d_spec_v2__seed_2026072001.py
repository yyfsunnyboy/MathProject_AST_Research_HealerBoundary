# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per specification
    radicand = 135
    
    # Simplify radical manually without external imports to ensure native compliance and correctness
    # Factorization of 135: 135 = 27 * 5 = (9*3) * 5 = 3^3 * 5
    # sqrt(135) = sqrt(9 * 3 * 5) = sqrt(9) * sqrt(15) = 3 * sqrt(15)
    
    coefficient = 3
    simplified_radicand = 15
    
    # Construct canonical LaTeX for the answer: a\sqrt{b} -> "3\sqrt{15}"
    correct_answer_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"

    question_text = (f"Simplify the radical expression $\\sqrt{{{radicand}}}$. "
                     f"Express your answer in simplest form as an integer coefficient times a square root of an integer.")

    oracle_payload = {"radicand": radicand}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_latex,
        "oracle_payload": oracle_payload,
    }