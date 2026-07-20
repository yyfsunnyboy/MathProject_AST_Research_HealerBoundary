def generate(level=1, **kwargs):
    from math import isqrt
    
    radicand = kwargs.get('radicand', 135) if 'radicand' in kwargs else 135
    
    # Simplify sqrt(135)
    k = int(isqrt(radicand))
    
    coefficient = k
    simplified_radicand = radicand // (k * k)
    
    correct_answer = {
        "coefficient": coefficient,
        "radicand": simplified_radicand,
        "canonical_latex": f"{coefficient}\\sqrt{{{simplified_radicand}}}"
    }
    
    question_text = r"""Simplify the radical expression \(\sqrt{135}\) into its simplest form \(a\sqrt{n}\), where \(n\) is as small as possible. Express your answer in terms of a coefficient and radicand."""

    return {
        "question_text": question_text,
        "correct_answer": correct_answer["canonical_latex"],
        "oracle_payload": {"radicand": 135}
    }
