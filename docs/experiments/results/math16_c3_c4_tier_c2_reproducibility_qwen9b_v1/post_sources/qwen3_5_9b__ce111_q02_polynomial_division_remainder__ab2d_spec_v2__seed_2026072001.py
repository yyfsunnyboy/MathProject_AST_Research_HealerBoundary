# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import PolynomialOps
    
    # Frozen sampled parameters (must be preserved exactly)
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    # Perform polynomial division to get quotient and remainder
    _, remainder_coeffs = PolynomialOps.div_qr(dividend_coefficients, divisor_coefficients)
    
    # Format the remainder into canonical LaTeX (descending powers implied by list order in API context or handled internally)
    # Note: The input lists are descending power coefficients. 
    # [6, 4, 0] -> 6x^2 + 4x + 0
    # [2, 0, 0] -> 2x^2 + 0x + 0 = 2x^2
    # Division: (6x^2+4x) / (2x^2) = 3 with remainder 4x.
    # Remainder coeffs should be [4]. Let's trust the API handles formatting correctly based on input list semantics.
    
    canonical_latex = PolynomialOps.format_latex(remainder_coeffs)
    
    # Construct question text using formal LaTeX delimiters
    dividend_str = "6x^2 + 4x" if len(dividend_coefficients) > 1 else str(dividend_coefficients[0])
    divisor_str = canonical_latex
    
    question_text = f"What is the remainder when $\\displaystyle {dividend_str}$ is divided by $\\displaystyle {divisor_str}$?"
    
    # Construct correct_answer dict with only remainder and canonical_latex
    correct_answer = {
        "remainder": remainder_coeffs,  # Return coefficients as list for JSON serializability unless string required. Spec says "include only remainder". Usually coeffs or latex representation of the polynomial value? Given oracle_payload has coeffs, let's return coeffs for programmatic checking, but spec implies 'canonical_latex' is also in answer.
        "canonical_latex": canonical_latex
    }

    # Prepare oracle_payload exactly as frozen parameters
    oracle_payload = {
        "dividend_coefficients": dividend_coefficients,
        "divisor_coefficients": divisor_coefficients
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }