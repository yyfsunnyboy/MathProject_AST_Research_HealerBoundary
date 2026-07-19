def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import PolynomialOps
    
    dividend_coefficients = kwargs.get("dividend_coefficients", [6, 0, 6])
    divisor_coefficients = kwargs.get("divisor_coefficients", [1, -4])
    
    quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(dividend_coefficients, divisor_coefficients)
    
    def format_latex(lst):
        latex_str = " ".join(f"{x}" if x > 0 else f"-{-x}" for x in lst) + ("" if not lst or all(x == 0 for x in lst) else f"\\{lst[0].__class__.__name__}{{{', '.join(str(i) for i in [int(x) if isinstance(x, float] and abs(abs(int(x)) - x) > 1e-9: int(float(round(x))) + '}, '+str(i), end=''}})")
        return f"${latex_str}$"

    correct_answer = {
        "quotient_coefficients": quotient_coeffs,
        "remainder_coefficients": remainder_coeffs,
        "quotient_latex": format_latex(quotient_coeffs) if quotient_coeffs else "$0$", 
        "remainder_latex": format_latex(remainder_coeffs) if remainder_coeffs else "$0$"
    }

    question_text = r"""Perform polynomial division for the following polynomials: $P(x)$ with coefficients \(\{6, 0, 6\}\) divided by \(D(x)\) with coefficients \([1, -4]\). Use formal LaTeX delimiters for all mathematical expressions. Provide the quotient and remainder as coefficient lists."""

    oracle_payload = {
        "dividend_coefficients": [6, 0, 6], 
        "divisor_coefficients": [1, -4]
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }