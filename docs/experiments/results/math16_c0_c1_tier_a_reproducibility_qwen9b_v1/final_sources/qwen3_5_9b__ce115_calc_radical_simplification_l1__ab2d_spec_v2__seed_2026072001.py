# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per specification
    radicand = 27
    
    # Simplify sqrt(27) -> a*sqrt(b) form manually since no external RadicalOps module is provided in the environment.
    # Factorization: 27 = 9 * 3 = (3^2) * 3
    # sqrt(27) = sqrt(3^2 * 3) = 3 * sqrt(3)
    
    coefficient = 3
    simplified_radicand = 3
    
    # Construct canonical LaTeX: a\sqrt{b} -> "3\\sqrt{3}"
    canonical_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"

    question_text = r"Simplify the radical expression $\sqrt{" + str(radicand) + "}$. Express your answer in simplest form."
    
    # Construct correct_answer dict with coefficient, radicand, and canonical_latex
    correct_answer = {
        "coefficient": coefficient,
        "radicand": simplified_radicand,
        "canonical_latex": canonical_latex
    }

    oracle_payload = {"radicand": 27}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }