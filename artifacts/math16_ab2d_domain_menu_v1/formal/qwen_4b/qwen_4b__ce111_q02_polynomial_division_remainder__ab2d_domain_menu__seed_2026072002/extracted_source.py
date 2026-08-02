from core.prompts.domain_function_library import PolynomialOps


def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }

    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]

    q, r = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    remainder_latex = PolynomialOps.format_latex(r)

    return {
        "question_text": f"計算多項式 \\({PolynomialOps.to_degree_map(dividend_coeffs)}\\) 除以 \\({PolynomialOps.to_degree_map(divisor_coeffs)}\\) 所得的餘式。",
        "correct_answer": {"remainder": str(r), "canonical_latex": remainder_latex},
        "oracle_payload": frozen_params,
    }
