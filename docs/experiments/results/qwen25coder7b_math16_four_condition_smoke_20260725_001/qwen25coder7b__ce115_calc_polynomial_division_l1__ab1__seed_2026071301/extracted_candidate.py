def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]

    # Perform polynomial division
    quotient_coefficients = []
    remainder_coefficients = dividend_coefficients[:]
    
    while len(remainder_coefficients) >= len(divisor_coefficients):
        leading_term_quotient = remainder_coefficients[-1] // divisor_coefficients[-1]
        quotient_coefficients.append(leading_term_quotient)
        
        new_term = [leading_term_quotient * coeff for coeff in divisor_coefficients]
        new_term.reverse()
        remainder_coefficients = [
            remainder_coefficients[i] - new_term[i]
            for i in range(len(remainder_coefficients))
        ]
        while len(remainder_coefficients) > 0 and remainder_coefficients[-1] == 0:
            remainder_coefficients.pop()

    quotient_latex = ' + '.join([f'{coeff}x^{len(quotient_coefficients)-i-1}' if i < len(quotient_coefficients)-1 else f'{coeff}' for i, coeff in enumerate(quotient_coefficients)])
    remainder_latex = ' + '.join([f'{coeff}x^{len(remainder_coefficients)-i-1}' if i < len(remainder_coefficients)-1 else f'{coeff}' for i, coeff in enumerate(remainder_coefficients)])

    return {
        "question_text": r'\(\text{Divide } (6x^2 + 0x + 6) \text{ by } (x - 4)\)',
        "correct_answer": {
            "quotient_coefficients": quotient_coefficients,
            "remainder_coefficients": remainder_coefficients,
            "quotient_latex": quotient_latex,
            "remainder_latex": remainder_latex
        },
        "oracle_payload": {"dividend_coefficients": dividend_coefficients, "divisor_coefficients": divisor_coefficients}
    }
