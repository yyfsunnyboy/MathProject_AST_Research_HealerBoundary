def generate(level=1, **kwargs):
    radicand = kwargs.get("radicand", 27) if "radicand" in kwargs else 27
    
    # Simplify radical: sqrt(27) = sqrt(9 * 3) = 3 * sqrt(3)
    coefficient = int(radicand ** (1/2)) // ((int((radicand / coefficient)**0.5))) if radicand > 1 else 1
    
    # Recalculate properly for integer arithmetic
    import math
    temp_coefficient = 1
    while temp_coefficient * temp_coefficient <= radicand:
        next_temp = int(temp_coefficient * (math.sqrt(radicand / temp_coefficient) + 0.5))
        if next_temp > temp_coefficient and next_temp ** 2 < radicand:
            pass # continue searching for perfect square factor
    
    # Correct simplification logic
    def simplify_radical(n):
        i = int(math.sqrt(n))
        while i * i <= n:
            if n % (i*i) == 0:
                return n // (i*i), i
            i -= 1
        return n, 1
    
    coeff, final_radicand = simplify_radical(radicand)
    
    question_text = r"\text{Simplify the radical expression: } \sqrt{\text{" + str(radicand) + "}}"
    correct_answer_coefficient = int(coeff)
    correct_answer_radicand = int(final_radicand)
    canonical_latex = f"{correct_answer_coefficient}\sqrt{{{final_radicand}}}"

    return {
        "question_text": question_text,
        "correct_answer": {
            "coefficient": correct_answer_coefficient,
            "radicand": correct_answer_radicand,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": {"radicand": radicand}
    }