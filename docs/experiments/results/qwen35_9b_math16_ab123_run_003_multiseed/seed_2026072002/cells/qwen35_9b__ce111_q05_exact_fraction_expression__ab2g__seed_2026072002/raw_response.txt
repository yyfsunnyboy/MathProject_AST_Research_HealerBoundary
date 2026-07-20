def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Parse components to compute correct answer manually without external libraries for precision verification
    from fractions import Fraction
    
    term1 = Fraction(9, 22)
    term2 = Fraction(11, 18)
    inner_subtrahend_term_a = Fraction(23, 22)
    inner_subtrahend_term_b = Fraction(7, 18)
    
    # Calculate the expression: A + B - (C - D) = A + B - C + D
    result_numerator = term1.numerator * term2.denominator * inner_subtrahend_term_a.denominator * inner_subtrahend_term_b.denominator \
                     + term2.numerator * term1.denominator * inner_subtrahend_term_a.denominator * inner_subtrahend_term_b.denominator \
                     - (inner_subtrahend_term_a.numerator * term1.denominator * term2.denominator * inner_subtrahend_term_b.denominator) \
                     + (inner_subtrahend_term_b.numerator * term1.denominator * term2.denominator * inner_subtrahend_term_a.denominator)
    
    result_denominator = term1.denominator * term2.denominator * inner_subtrahend_term_a.denominator * inner_subtrahend_term_b.denominator
    
    # Simplify by GCD (fractions.Fraction does this automatically, but we reconstruct here to be explicit if needed)
    common_divisor = __import__('math').gcd(result_numerator, result_denominator)
    
    simplified_num = result_numerator // common_divisor
    simplified_denom = result_denominator // common_divisor
    
    # Format canonical LaTeX: \frac{num}{den} or integer if denom is 1
    if simplified_denom == 1:
        canon_latex = f"{simplified_num}"
    else:
        canon_latex = rf"\frac{{{simplified_num}}}{{{simplified_denom}}}"
    
    # Construct question text with formal LaTeX delimiters
    question_text = (f"Compute the exact value of the expression using rational arithmetic:\n\n"
                     f"${expression}$\n\n"
                     f"Simplify your final answer to an irreducible fraction.")
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": simplified_num,
            "denominator": simplified_denom,
            "canonical_latex": canon_latex
        },
        "oracle_payload": {"expression": expression}
    }