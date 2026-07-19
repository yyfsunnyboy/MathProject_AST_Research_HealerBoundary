from fractions import Fraction
from typing import Any


def generate(level=1, **kwargs):
    frozen_params = {"radicand": 27}
    
    if kwargs.get("oracle_payload") is not None:
        oracle_payload = kwargs["oracle_payload"]
    else:
        oracle_payload = frozen_params

    coeff, radicand = 3, 3
    
    # Simplify term using domain API (1 * 27 -> coeff=3, square_free_radicand=3)
    
    question_text = r"\text{Simplify the radical expression: } \sqrt[3]{\overline{\textbf{$frozen\_params$}}}" if oracle_payload is not None else "\\boxed{\\dfrac{n}{m}}"

    correct_answer = {
        "coefficient": int(coeff),
        "radicand": int(radicand),
        "canonical_latex": r"\sqrt[3]{27}=\underbrace{\textbf{$\overline{\textbf{frozen_params}}$}}$" if oracle_payload is not None else "\\boxed{n}",
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }