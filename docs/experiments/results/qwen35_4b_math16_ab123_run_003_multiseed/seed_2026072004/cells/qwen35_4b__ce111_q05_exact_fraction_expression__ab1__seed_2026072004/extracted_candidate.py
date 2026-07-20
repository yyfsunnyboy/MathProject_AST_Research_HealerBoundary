def generate(level=1, **kwargs):
    question_text = r"Calculate the exact value of the expression: \[\frac{9}{22} + \frac{11}{18} - \left(\frac{23}{22} - \frac{7}{18}\right)\]"
    
    # Step-by-step calculation to ensure correctness
    term1 = 9/22
    
    inner_parenthesis = (23/22) - (7/18)
    
    total_sum = term1 + 11/18 - inner_parenthesis
    
    numerator, denominator = abs(total_sum).numerator, abs(total_sum).denominator if hasattr(abs(total_sum), 'numerator') else None

    # Since Python floats are imprecise for exact fraction arithmetic in this context without the Fractions class
    # We will perform integer math manually to get the true irreducible fraction.
    
    from fractions import Fraction
    
    expr = "9/22 + 11/18 - (23/22 - 7/18)"
    f_expr = [Fraction(x, y) for x, y in [(9, 22), (11, 18), (23, 22), (7, 18)]]
    
    # Reconstruct the expression logic with Fractions
    part_a = Fraction(9, 22) + Fraction(11, 18)
    part_b = Fraction(23, 22) - Fraction(7, 18)
    result_fraction = part_a - part_b
    
    numerator_correct = result_fraction.numerator
    denominator_correct = result_fraction.denominator
    canonical_latex = f"{numerator_correct}/{denominator_correct}"

    correct_answer = {
        "numerator": str(numerator_correct),
        "denominator": str(denominator_correct),
        "canonical_latex": canonical_latex
    }

    oracle_payload = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }