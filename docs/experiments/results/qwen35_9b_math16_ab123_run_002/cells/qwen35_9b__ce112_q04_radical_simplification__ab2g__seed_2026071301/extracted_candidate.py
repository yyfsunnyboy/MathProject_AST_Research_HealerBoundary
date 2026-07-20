def generate(level=1, **kwargs):
    frozen_params = {"radicand": 135}
    
    radicand = frozen_params["radicand"]
    # Prime factorization of 135: 3^3 * 5
    # Simplified radical form for sqrt(135) is 9*sqrt(5), but standard math format often keeps coefficient outside.
    # However, the prompt asks for "coefficient", "radicand", and "canonical_latex".
    # For sqrt(135): 
    #   Perfect square factor: 9 (since 9^2 = 81) -> wait, 135/9 = 15. No, 135 = 27 * 5 = 3^3 * 5.
    #   Largest perfect square divisor is 9? No. 3^3 means one pair of 3s (which makes 3) and a leftover 3. 
    #   So sqrt(135) = sqrt(27*5) = sqrt(9*15)? No, 135/9=15. Correct.
    #   Let's re-calculate: 135 / 9 = 15. Is 9 the largest square? 
    #   Factors of 135: 1, 3, 5, 9, 15, 27, 45, 135.
    #   Squares among factors: 1, 9. Largest is 9.
    #   So sqrt(135) = 3 * sqrt(15).
    
    coefficient = 3
    simplified_radicand = 15
    
    canonical_latex = f"{coefficient}\\sqrt{{{simplified_radicand}}}"

    question_text = (f"Simplify the radical expression $\\sqrt{{{radicand}}}$. "
                     f"Write your answer in the form $a\\sqrt{b}$, where $a$ and $b$ are integers. ")

    return {
        "question_text": question_text,
        "correct_answer": canonical_latex,
        "oracle_payload": frozen_params
    }