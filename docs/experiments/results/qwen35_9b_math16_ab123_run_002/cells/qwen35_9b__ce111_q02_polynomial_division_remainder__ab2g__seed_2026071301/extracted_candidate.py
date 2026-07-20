def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    # Interpret coefficients: 
    # Dividend (descending powers implied by typical math problem context or ascending?): 
    # Usually lists are given as highest degree to lowest for polynomials in such contexts unless specified otherwise.
    # However, standard Python list representation often implies [a_n, ..., a_0] or [a_0, ..., a_n].
    # Let's assume the provided format is descending order (highest power first) based on common math problem inputs like [6x^2 + 4x + 0].
    # Dividend: 6x^2 + 4x = P(x). Degree 2.
    # Divisor: 2x^2 + 0x + 0 = Q(x) = 2x^2. Degree 2.
    
    dividend_poly_coeffs_desc = [float(c) for c in dividend_coefficients] 
    divisor_poly_coeffs_desc = [float(c) for c in divisor_coefficients]
    
    # Perform polynomial division to find quotient and remainder manually or logically:
    # Dividend P(x) = 6x^2 + 4x
    # Divisor Q(x) = 2x^2
    
    # Division step: 
    # Leading term of dividend / leading term of divisor = (6x^2) / (2x^2) = 3.
    # Quotient is constant polynomial 3.
    
    remainder_poly_coeffs_desc = [0, 4] if len(dividend_coefficients) > len([c for c in divisor_coefficients]) else [] 
    # Actually, let's compute strictly:
    # P(x) / Q(x):
    # (6x^2 + 4x) / (2x^2) = 3 with remainder?
    # Wait, if we divide a polynomial by another of same degree:
    # Quotient term c_0 = dividend[0] / divisor[0] -> 6/2 = 3.
    # Multiply quotient * divisor -> 3 * (2x^2) = 6x^2.
    # Subtract from dividend -> (6x^2 + 4x) - 6x^2 = 4x.
    # Degree of remainder (1) is less than degree of divisor (2). So division stops here.
    
    quotient_val = float(dividend_coefficients[0] / divisor_coefficients[0]) if len(divisor_coefficients) > 0 and dividend_coefficients[0] != 0 else 0
    
    # Remainder coefficients: The result after subtraction, padded to match structure or just the remaining terms.
    # Remaining polynomial is 4x. Coeffs descending [4]. Or should we keep degree alignment? 
    # Standard remainder representation usually lists non-zero coeffs or full vector of lower degree.
    # Let's represent remainder as list starting from highest power present in remainder down to x^0, excluding leading zeros if not standard form required, but for consistency with input format (lists), let's return [4].
    
    remainder_coeffs = []
    current_remainder_val = 4.0 # The coefficient of x term remaining
    
    # Constructing the specific lists expected by oracle_payload which must match frozen parameters exactly as provided in kwargs or defaults? 
    # Instruction says: "oracle_payload must exactly equal the frozen sampled parameters."
    # Frozen params are {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}.
    
    oracle_payload = {
        "dividend_coefficients": dividend_coefficients,
        "divisor_coefficients": divisor_coefficients
    }
    
    # Correct answer string: remainder and canonical_latex. 
    # Remainder is polynomial 4x. Latex: $4x$.
    # Canonical latex for quotient (not scored) but required in logic? No, only remainder needed in correct_answer text usually, plus identifier.
    # Format requirement: "correct_answer must include only remainder and canonical_latex". 
    # Let's construct a JSON-serializable string or dict part? Usually these tasks expect a specific format like {"remainder": "...", "canonical_latex": "..."}.
    
    remainder_str = f"{current_remainder_val}x" if current_remainder_val != 0 else "0"
    canonical_latex = f"${remainder_str}$"
    
    # Handling case where remainder is constant or zero properly for the specific input [6,4,0] / [2,0,0]:
    # Dividend: 6x^2 + 4x. Remainder after dividing by 2x^2 is indeed 4x.
    # If dividend was just x term? No, it's degree 2 vs degree 2.
    
    final_remainder_str = "4x" if current_remainder_val != 0 else "0"
    
    return {
        "question_text": f"Determine the remainder when $P(x) = {' + '.join([f'{c}x^{i}' for i, c in enumerate(reversed(dividend_coefficients))])}$ is divided by $Q(x) = {' + '.join([f'{c}x^{len(divisor_coefficients)-1-i if len(divisor_coefficients)>0 else 0}' for i,c in enumerate(divisor_coefficients)])}$.",
        # Simplifying the latex generation to be robust and standard:
        "question_text": r"Determine the remainder when $P(x) = 6x^2 + 4x$ is divided by $Q(x) = 2x^2$", 
        "correct_answer": {
            "remainder": "4x",
            "canonical_latex": "$4x$"
        },
        "oracle_payload": oracle_payload
    }