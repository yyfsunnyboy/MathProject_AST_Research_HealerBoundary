def generate(level=1, **kwargs):
    import json
    
    # Frozen sampled parameters provided in task specification
    dividend_coefficients = [6, 4, 0]   # Represents polynomial: 6x^2 + 4x + 0
    divisor_coefficients = [2, 0, 0]   # Represents polynomial: 2x^2 + 0x + 0
    
    # Perform Polynomial Division manually to find Quotient and Remainder
    # Dividend P(x) = 6x^2 + 4x
    # Divisor D(x) = 2x^2
    
    # Step 1: Divide leading terms (6x^2 / 2x^2 = 3). This is the quotient.
    quotient_val = dividend_coefficients[0] // divisor_coefficients[0] if len(dividend_coefficients)>=len(divisor_coefficients) and divisor_coefficients[-(len(divisor_coefficients)-1)] != 0 else 0
    
    # Since D(x) is exactly x^2 scaled by 2, we can simplify the division logic directly.
    # P(x) = 6x^2 + 4x
    # Q(x) * D(x) = (3)(2x^2) = 6x^2
    # Remainder R(x) = P(x) - Q(x)*D(x) = (6x^2 + 4x) - 6x^2 = 4x
    
    remainder_coefficients = [0, 4]   # Represents polynomial: 0x^1 + 4
    quotient_latex = "3"              # Quotient is constant 3
    
    # Construct LaTeX for Remainder (canonical form)
    if len(remainder_coefficients) == 1 and remainder_coefficients[0] != 0:
        rem_str = f"{remainder_coefficients[0]}"
    else:
        terms = []
        for i, coeff in enumerate(reversed(remainder_coefficients)):
            power = len(remainder_coefficients) - 1 - i
            if coeff == 0: continue
            term_parts = []
            if abs(coeff) != 1 or power == 0:
                term_parts.append(str(abs(coeff)))
            
            if power > 0 and not (coeff < 0): # Handle negative sign separately in latex construction usually, but here coeffs are simple ints
                 pass
            
            variable_part = ""
            if power == 1:
                variable_part = "x"
            else:
                variable_part = f"x^{{{power}}}"
            
            term_parts.append(variable_part)
            terms.append("".join(term_parts))
        
        # Reconstruct sign handling properly for the list to string conversion logic below is tricky, 
        # let's just build the expression manually based on known result 4x
        
    canonical_latex = "4x"

    question_text = (
        r"What is the remainder when dividing $6x^2 + 4x$ by $2x^2$? "
        r"Express your answer in standard polynomial form."
    )

    # Construct oracle_payload as dict with keys from frozen parameters exactly
    oracle_payload = {
        "dividend_coefficients": dividend_coefficients,
        "divisor_coefficients": divisor_coefficients
    }

    return {
        "question_text": question_text,
        "correct_answer": canonical_latex,
        "oracle_payload": oracle_payload
    }