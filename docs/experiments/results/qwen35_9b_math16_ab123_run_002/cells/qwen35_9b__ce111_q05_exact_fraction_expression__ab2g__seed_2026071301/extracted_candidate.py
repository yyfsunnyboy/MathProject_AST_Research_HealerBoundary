def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Calculate the exact rational result of the expression: 9/22 + 11/18 - (23/22 - 7/18)
    from fractions import Fraction
    
    term1 = Fraction(9, 22)
    term2 = Fraction(11, 18)
    
    inner_parenthesis_numerator = 23
    inner_parenthesis_denominator = 22
    subtracted_term_numerator = 7
    subtracted_term_denominator = 18
    
    # Calculate (23/22 - 7/18)
    paren_result_num, paren_result_denom = Fraction(inner_parenthesis_numerator, inner_parenthesis_denominator) - \
                                           Fraction(subtracted_term_numerator, subtracted_term_denominator)
    
    # Total expression: term1 + term2 - paren_result
    total_expression = term1 + term2 - (paren_result_num / paren_result_denom) if isinstance(paren_result_num/paren_result_denom, float) else term1 + term2 - Fraction(*tuple(map(int, str(Fraction(inner_parenthesis_numerator, inner_parenthesis_denominator)))))
    
    # Re-calculate cleanly using Fractions directly to avoid float issues in logic description above
    part_a = Fraction(9, 22) + Fraction(11, 18) - (Fraction(23, 22) - Fraction(7, 18))
    
    numerator = part_a.numerator
    denominator = part_a.denominator
    
    # Construct canonical LaTeX for the fraction \frac{numerator}{denominator}
    canonical_latex = f"\\\\frac{{{numerator}}}{{{{{denominator}}}}}"
    
    return {
        "question_text": f"Simplify the expression: $9/22 + 11/18 - (23/22 - 7/18)$.",
        "correct_answer": {
            "numerator": numerator,
            "denominator": denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }