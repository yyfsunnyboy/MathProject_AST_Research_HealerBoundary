from core.prompts.domain_function_library import PolynomialOps

def generate(level=1, **kwargs):
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }
    
    # Perform polynomial division to get quotient and remainder coefficients
    q_coeffs, r_coeffs = PolynomialOps.div_qr(
        frozen_params["dividend_coefficients"], 
        frozen_params["divisor_coefficients"]
    )
    
    # Format the remainder as LaTeX string. Note: div_qr returns list of ints/strs (JSON safe).
    # format_latex expects numeric coeffs, but r_coeffs from div_qr are already JSON-safe strings/integers.
    # We need to ensure they are treated correctly by format_latex or convert if necessary.
    # The spec says inputs for format_latex: "highest-degree-first numeric coefficients; bool forbidden".
    # Since q and r come from exact division, we pass them directly. If they contain 'p/q' strings (unlikely here but possible), 
    # the API handles it or expects conversion? The example shows ints/strs in div_qr return shape.
    # Let's assume format_latex can handle the list returned by div_qr if elements are valid numbers/strings representing fractions.
    
    remainder_latex = PolynomialOps.format_latex(r_coeffs)
    
    question_text = "計算多項式 \(6x^2+4x\) 除以 \(2x^2\) 所得的餘式。"

    return {
        "question_text": question_text,
        "correct_answer": {
            "remainder": remainder_latex,
            "canonical_latex": remainder_latex
        },
        "oracle_payload": frozen_params
    }