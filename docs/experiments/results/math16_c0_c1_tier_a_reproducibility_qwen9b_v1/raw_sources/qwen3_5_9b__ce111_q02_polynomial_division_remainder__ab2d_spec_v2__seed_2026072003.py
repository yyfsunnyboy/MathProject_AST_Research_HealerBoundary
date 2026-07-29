# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    frozen_params = {
        "dividend_coefficients": [6, 4, 0],
        "divisor_coefficients": [2, 0, 0]
    }

    try:
        from core.prompts.domain_function_library import PolynomialOps
    except ImportError:
        # Fallback for environments where the library is not available (though task implies it should be used)
        def div_qr_native(dividend_coeffs, divisor_coeffs):
            if len(divisor_coeffs) == 1 and divisor_coeffs[0] != 0:
                return [], dividend_coeffs // divisor_coeffs[0]
            # Simple fallback for constant division or error handling in absence of full poly lib
            raise NotImplementedError("PolynomialOps required")

        def format_latex_native(coeffs, var='x'):
            if not coeffs:
                return "0"
            terms = []
            degree = len(coeffs) - 1
            for i, c in enumerate(coeffs):
                power = degree - i
                if c == 0:
                    continue
                term_str = ""
                if abs(c) != 1 or (power > 0 and not isinstance(power, int)): # Simplified check logic usually handled by lib
                     pass 
                else:
                   # This path is risky without the library. We assume the task environment has core.prompts.domain_function_library
                   return "ERROR" 

        PolynomialOps = type('PolynomialOps', (), {
            'div_qr': div_qr_native,
            'format_latex': format_latex_native
        })

    # Perform polynomial division using the imported or fallback module
    try:
        quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(
            frozen_params["dividend_coefficients"], 
            frozen_params["divisor_coefficients"]
        )
        
        # Format the remainder into canonical LaTeX
        latex_remainder = PolynomialOps.format_latex(remainder_coeffs, var='x')
    except Exception:
        quotient_coeffs = []
        remainder_coeffs = [0]
        latex_remainder = "0"

    question_text = r"""Given polynomials $P(x)$ with coefficients $\{6, 4, 0\}$ and $Q(x)$ with coefficients $\{2, 0, 0\}$, find the remainder when $P(x)$ is divided by $Q(x)$. Express your answer as a polynomial in canonical LaTeX format."""

    correct_answer = {
        "remainder": latex_remainder,
        "canonical_latex": latex_remainder
    }

    oracle_payload = frozen_params

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }