def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]

    # Perform polynomial division
    quotient_coefficients = []
    remainder_coefficients = dividend_coefficients.copy()
    
    while len(remainder_coefficients) >= len(divisor_coefficients):
        leading_term_quotient = remainder_coefficients[-1] // divisor_coefficients[-1]
        quotient_coefficients.append(leading_term_quotient)
        
        new_remainder = []
        for i in range(len(remainder_coefficients)):
            if i < len(divisor_coefficients):
                new_remainder.append(remainder_coefficients[i] - leading_term_quotient * divisor_coefficients[i])
            else:
                new_remainder.append(remainder_coefficients[i])
        
        remainder_coefficients = [coeff for coeff in new_remainder if coeff != 0]
    
    quotient_latex = ' + '.join([f'{coeff}x^{len(quotient_coefficients)-i-1}' if i < len(quotient_coefficients)-1 else f'{coeff}' for i, coeff in enumerate(quotient_coefficients)])
    remainder_latex = ' + '.join([f'{coeff}x^{len(remainder_coefficients)-i-1}' if i < len(remainder_coefficients)-1 else f'{coeff}' for i, coeff in enumerate(remainder_coefficients)]) if remainder_coefficients else '0'

    return {
        "question_text": r"\[ \frac{" + ' '.join([f"{coeff}x^{len(dividend_coefficients)-i-1}" if i < len(dividend_coefficients)-1 else f"{coeff}" for i, coeff in enumerate(dividend_coefficients)]) + "}{" + ' '.join([f"{coeff}x^{len(divisor_coefficients)-i-1}" if i < len(divisor_coefficients)-1 else f"{coeff}" for i, coeff in enumerate(divisor_coefficients)]) + r"} = " + quotient_latex + r" \text{ remainder } " + remainder_latex + r" \]",
        "correct_answer": {
            "quotient_coefficients": quotient_coefficients,
            "remainder_coefficients": remainder_coefficients,
            "quotient_latex": quotient_latex,
            "remainder_latex": remainder_latex
        },
        "oracle_payload": {"dividend_coefficients": dividend_coefficients, "divisor_coefficients": divisor_coefficients}
    }
