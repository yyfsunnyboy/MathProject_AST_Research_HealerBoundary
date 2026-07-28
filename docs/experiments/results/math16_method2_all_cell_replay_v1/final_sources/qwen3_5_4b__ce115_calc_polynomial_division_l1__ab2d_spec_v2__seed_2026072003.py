# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    frozen_parameters = {
        "dividend_coefficients": [6, 0, 6],
        "divisor_coefficients": [1, -4]
    }

    from core.prompts.domain_function_library import PolynomialOps
    
    dividend_coeffs = frozen_parameters["dividend_coefficients"]
    divisor_coeffs = frozen_parameters["divisor_coefficients"]
    
    # Perform polynomial division using the domain library
    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    def format_list(lst):
        return f"[{', '.join(map(str, lst))}]"

    question_text = r"""Perform polynomial long division for: \[ (6x^2 + 0x + 6) \div (1x - 4) \] """

    correct_answer = {
        "quotient_coefficients": quotient,
        "remainder_coefficients": remainder,
        "quotient_latex": r"\( [{}], x^{len([{}])-2} ... \)".format(format_list(quotient), format_list(quotient)), # Simplified for direct latex representation of list structure if needed, but standard is just the coefficients. Let's use a cleaner LaTeX string construction based on coeffs.
        "remainder_latex": r"\( [{}] \)".format(format_list(remainder))
    }

    # Constructing proper Latex strings directly from lists to ensure correctness without complex formatting logic errors in this context
    quotient_str = ", ".join(map(str, quotient)) if isinstance(quotient, list) else str(quotient)
    remainder_str = ", ".join(map(str, remainder)) if isinstance(remainder, list) else str(remainder)

    # Re-defining correct_answer with explicit LaTeX strings for clarity and correctness
    qa_dict = {
        "quotient_coefficients": quotient,
        "remainder_coefficients": remainder,
        "quotient_latex": r"\(" + ", ".join(map(str, quotient)) + r")",
        "remainder_latex": r"\(" + ", ".join(map(str, remainder)) + r")"
    }

    return {
        "question_text": question_text,
        "correct_answer": qa_dict,
        "oracle_payload": frozen_parameters
    }
