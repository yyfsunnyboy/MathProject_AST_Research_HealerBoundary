def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }

    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]

    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    correct_answer_remainder = str(remainder[1]) if len(remainder) > 0 and isinstance(remainder[1], Fraction) else "0"
    
    # Ensure the remainder is formatted correctly as a string representation of the polynomial
    # Since div_qr returns coefficients (int or str), we can format it directly. 
    # However, to be safe with JSON serialization and exact value matching:
    if len(remainder) > 1:
        rem_coeffs = remainder[1]
        latex_str = PolynomialOps.format_latex(list(map(Fraction, rem_coeffs)))
        correct_answer_remainder = str(latex_str).replace(" ", "") # Remove spaces for canonical form usually expected in math tasks unless specified otherwise. 
    else:
        if len(remainder) == 0 or remainder[1] == "":
            correct_answer_remainder = "0"

    return {
        "question_text": f"計算多項式 \\({dividend_coeffs}[0]*x**2 + {dividend_coeffs}[1]*x + {dividend_coeffs}[2]} 除以 \\({divisor_coeffs[0]}*x**2 + {divisor_coeffs[1]}*x + {divisor_coeffs[2]}) 所得的餘式。",
        "correct_answer": {"remainder": correct_answer_remainder, "canonical_latex": PolynomialOps.format_latex(list(map(Fraction, remainder[1])) if len(remainder) > 0 else [Fraction(0)])},
        "oracle_payload": frozen_params
    }
