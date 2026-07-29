def generate(level=1, **kwargs):
    radicand = 27
    import math
    
    # Simplify sqrt(27) -> sqrt(9*3) = 3 * sqrt(3)
    coefficient = int(math.isqrt(radicand))
    
    temp_radicand = radicand // (coefficient ** 2)
    simplified_radicand = temp_radicand
    
    correct_answer_dict = {
        "coefficient": coefficient,
        "radicand": simplified_radicand,
        "canonical_latex": f"{coefficient}\\sqrt{{{simplified_radicand}}}"
    }
    
    return {
        "question_text": r"\\text{Simplify the radical: } \\sqrt{{27}}",
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"radicand": 27}
    }