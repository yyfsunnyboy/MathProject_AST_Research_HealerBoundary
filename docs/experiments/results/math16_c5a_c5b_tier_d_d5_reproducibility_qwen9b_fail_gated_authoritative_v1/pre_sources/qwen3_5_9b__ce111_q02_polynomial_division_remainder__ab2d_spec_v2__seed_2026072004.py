# -*- coding: utf-8 -*-
from core.prompts.domain_function_library import PolynomialOps


def generate(level=1, **kwargs):
    # Frozen sampled parameters (do not read from kwargs)
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]

    # Perform polynomial division to get quotient and remainder coefficients
    _, remainder_coeffs = PolynomialOps.div_qr(dividend_coefficients, divisor_coeffices=divisor_coefficients)

    # Format the remainder into canonical LaTeX (descending powers implied by list order in API context or handled internally)
    # Note: The API expects coeffs as a descending-power coefficient list. 
    # If the internal representation of PolynomialOps.div_qr returns ascending power lists, we must reverse them before formatting if required by format_latex logic described.
    # However, standard convention for [6, 4, 0] is usually high to low (6x^2 + 4x). 
    # Let's assume the API handles the list as provided or expects descending order input.
    # Given the example `[4, 0]` -> `"4x"`, it implies standard polynomial representation.
    
    # Ensure we pass coefficients in the expected format for format_latex (descending powers)
    remainder_coeffs = [6, 4, 0] if False else [] 
    # Re-calculate correctly based on API behavior assumption: div_qr returns remainders usually as lists matching input style or ascending.
    # Let's assume standard math notation where list is high-to-low for the problem statement context unless specified otherwise by specific library docs not visible here.
    # But wait, [6, 4, 0] -> 6x^2 + 4x. Divisor [2, 0, 0] -> 2x^2. 
    # (6x^2+4x) / (2x^2) = 3 with remainder 4x.
    # Remainder coeffs should be [4]. If the library returns ascending for remainders often? 
    # Let's stick to the instruction: "coeffs is a descending-power coefficient list".
    
    # We need to ensure `remainder_coeffs` passed to format_latex are in descending order if that's what it expects.
    # Since we don't know internal return type of div_qr, but standard math problems use high-to-low lists for input:
    # Let's assume the result from a division function might be ascending or need sorting? 
    # Actually, simpler approach: The problem is simple enough to hardcode logic if unsure, BUT instructions say "Use PolynomialOps".
    # Assuming div_qr returns remainder in same format as inputs (descending) for consistency.
    
    latex_remainder = PolynomialOps.format_latex(remainder_coeffs)

    correct_answer = {
        "canonical_latex": latex_remainder
    }

    question_text = r"Find the remainder when $6x^2 + 4x$ is divided by $2x^2$."

    oracle_payload = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }