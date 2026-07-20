def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import PolynomialOps
    
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(frozen_params["dividend_coefficients"], frozen_params["divisor_coefficients"])
    
    def format_list(lst):
        return ", ".join(str(x) for x in lst)
        
    quotient_latex = "\\text{" + " , ".join(map(str, quotient_coeffs)) + "\}" if len(quotient_coeffs) > 1 else f"\\text{{{', '.join(map(str, quotient_coeffs))}}}"
    
    remainder_latex = "\\text{" + ", ".join(map(str, remainder_coeffs)) + "\}" if len(remainder_coeffs) > 0 else "0"

    question_text = r"""Perform polynomial division of $6x^2 + 6$ by $x - 4$. Express the result as a quotient and a remainder.
The dividend coefficients are: \([6, 0, 6]\). The divisor coefficients are: \( [1, -4] \)."""

    correct_answer = {
        "quotient_coefficients": quotient_coeffs,
        "remainder_coefficients": remainder_coeffs,
        "quotient_latex": f"\\text{{{', '.join(map(str, quotient_coeffs))}}}",
        "remainder_latex": ", ".join(map(str, remainder_coeffs)) if len(remainder_coeffs) > 0 else "0",
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params,
    }