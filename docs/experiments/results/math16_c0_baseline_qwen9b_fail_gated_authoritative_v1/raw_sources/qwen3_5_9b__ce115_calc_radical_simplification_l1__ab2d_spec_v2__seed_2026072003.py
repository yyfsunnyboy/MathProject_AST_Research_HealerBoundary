# -*- coding: utf-8 -*-
def generate(level=1, **kwargs):
    # Frozen sampled parameters as per specification
    radicand = 27
    
    # Compute simplification for sqrt(27) -> a*sqrt(b)
    # 27 = 9 * 3 = (3^2) * 3
    # Simplified form: 3 * sqrt(3)
    
    coefficient = 3
    simplified_radicand = 3
    
    # Construct canonical LaTeX string for the answer
    correct_answer_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"

    return {
        "question_text": r"Simplify \(\sqrt{" + str(radicand) + "}\).",
        "correct_answer": correct_answer_latex,
        "oracle_payload": {"radicand": radicand}
    }