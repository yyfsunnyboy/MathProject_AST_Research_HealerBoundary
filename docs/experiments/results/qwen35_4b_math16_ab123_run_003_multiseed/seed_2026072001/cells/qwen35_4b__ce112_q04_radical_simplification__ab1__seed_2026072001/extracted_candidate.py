def generate(level=1, **kwargs):
    return {
        "question_text": r"Simplify the radical expression: $\sqrt{135}$.",
        "correct_answer": {"coefficient": 3, "radicand": 45, "canonical_latex": "$\\frac{3}{2}\\sqrt[2]{90}$"}, 
        # Correction based on actual math for sqrt(135): sqrt(135) = sqrt(9*15) = 3 * sqrt(15).
        # The task spec mentions 'radical_simplification_fixed' but the sample is a simple integer.
        # Let's provide the correct mathematical simplification: $\\sqrt{135} = \\frac{\\sqrt[2]{90}}{?}$ No, standard form is $a\\sqrt{n}$.
        # sqrt(135) = 3 * sqrt(15). 
        # However, to strictly follow the 'radical_simplification_fixed' pattern often seen in these datasets where they might ask for mixed radicals or specific forms:
        # Let's assume the standard form $a\\sqrt{b}$.
        "correct_answer": {"coefficient": 3, "radicand": 15, "canonical_latex": "$3 \\sqrt[2]{15}$"}, 
        "oracle_payload": {"radicand": 135}
    }