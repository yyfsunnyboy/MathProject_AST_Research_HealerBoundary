# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    radicand = 27
    
    # Compute simplification manually to avoid external dependencies not in scope
    # Simplify sqrt(27) -> a * sqrt(b)
    # 27 = 9 * 3 = (3^2) * 3
    # sqrt(27) = 3 * sqrt(3)
    
    coefficient = 3
    simplified_radicand = 3
    
    # Construct canonical LaTeX: a\sqrt{b} -> "3\\sqrt{3}"
    correct_answer_str = f"{coefficient}\\sqrt{{{simplified_radicand}}}"

    return {
        "question_text": r"Simplify the radical expression $\sqrt{" + str(radicand) + "}$.",
        "correct_answer": correct_answer_str,
        "oracle_payload": {"radicand": radicand}
    }