import json
from typing import Any, Dict

def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    from core.prompts.domain_function_library import PolynomialOps
    
    quotient_rem = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)
    quotient_coeffs: list[int] = quotient_rem[0]
    remainder_coeffs: list[int] = quotient_rem[1]
    
    def format_latex(coeffs):
        if not coeffs:
            return "0"
        terms = []
        for i, c in enumerate(coeffs):
            power = len(coeffs) - 1 - i
            term_str = f"{c}x^{power}" if power > 0 else str(c)
            terms.append(term_str)
        return "\\text{" + ", ".join(terms) + "}"

    quotient_latex = format_latex(quotient_coeffs)
    remainder_latex = format_latex(remainder_coeffs)
    
    question_text = r"""Perform polynomial division. Given the dividend $P(x)$ and divisor $Q(x)$ with coefficients:
Dividend \( [6, 0, 6] \), Divisor \( [1, -4] \).
Find the quotient and remainder."""

    correct_answer = {
        "quotient_coefficients": quotient_coeffs,
        "remainder_coefficients": remainder_coeffs,
        "quotient_latex": quotient_latex,
        "remainder_latex": remainder_latex
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }