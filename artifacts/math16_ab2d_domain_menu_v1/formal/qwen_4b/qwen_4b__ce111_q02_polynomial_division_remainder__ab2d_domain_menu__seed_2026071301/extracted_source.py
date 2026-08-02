from core.prompts.domain_function_library import PolynomialOps


def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }

    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]

    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    # Convert coefficients to strings for the 'remainder' field in correct_answer
    remainder_strs = [str(c) if isinstance(c, (int, float)) else c for c in remainder]
    
    # Format LaTeX using the API
    quotient_latex = PolynomialOps.format_latex(quotient)

    return {
        "question_text": f"計算多項式 \\({dividend_coeffs[0]}x^{len(dividend_coeffs)-1}+{dividend_coeffs[1]}x\\) 除以 \\({divisor_coeffs[0]}x^{len(divisor_coeffs)-1}\\) 所得的餘式。",
        "correct_answer": {
            "remainder": ",".join(remainder_strs),
            "canonical_latex": f"{quotient_latex}" if len(remainder) == 0 else PolynomialOps.format_latex(remainder)
        },
        "oracle_payload": frozen_params
    }
