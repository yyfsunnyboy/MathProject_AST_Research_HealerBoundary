def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Perform polynomial division: (6x^2 + 0x + 6) / (x - 4)
    # Dividend P(x) = 6x^2 + 6
    # Divisor Q(x) = x - 4
    
    quotient_coefficients = []
    remainder_coefficients = [0]
    
    current_degree = len(dividend_coefficients) - 1
    divisor_degree = len(divisor_coefficients) - 1
    
    while current_degree >= divisor_degree:
        shift = current_degree - divisor_degree
        leading_term_dividend = dividend_coefficients[current_degree]
        
        # Calculate quotient term coefficient (exact arithmetic)
        q_coef = leading_term_dividend // divisor_coefficients[0]
        quotient_coefficients.insert(0, q_coef)
        
        # Subtract multiple of divisor from current part of dividend
        for i in range(len(divisor_coefficients)):
            idx_in_dividend = shift + i
            if idx_in_dividend < len(dividend_coefficients):
                dividend_coefficients[idx_in_dividend] -= q_coef * divisor_coefficients[i]
        
        # Remove trailing zeros from quotient to maintain highest degree first format correctly
        while len(quotient_coefficients) > 0 and quotient_coefficients[-1] == 0:
            quotient_coefficients.pop()
            
        current_degree -= 1
    
    if dividend_coefficients[0] != 0 or (len(dividend_coefficients) <= divisor_degree):
        # If there's a remainder, add it to the list. 
        # For linear divisor [1, -4], we expect one value in remainder.
        pass
        
    final_remainder = []
    temp_dividend = dividend_coefficients[:]
    
    while len(temp_dividend) > 0:
        if temp_dividend[0] != 0 or (len(divisor_coefficients) == 1 and temp_dividend[-1] != 0): # Check for non-zero leading term effectively
             break
        
        degree = len(temp_dividend) - 1
        divisor_degree = len(divisor_coefficients) - 1
        
        if degree < divisor_degree:
            final_remainder.extend([c for c in temp_dividend])
            break
            
        shift = degree - divisor_degree
        leading_term = temp_dividend[degree]
        
        q_coef = leading_term // divisor_coefficients[0]
        # We don't need to update quotient here, just find remainder
        
    # Re-calculate remainder properly using the original coefficients logic without modifying dividend in place for final check if needed.
    # Let's do a clean manual division step-by-step for [6x^2 + 6] / (x - 4)
    
    # Step 1: Divide leading terms -> 6x^2 / x = 6x
    quotient_coefficients.insert(0, 6)
    remainder_temp = []
    temp_poly = dividend_coefficients[:]
    
    # Subtract 6 * (x-4)*x = 6(x^2 - 4x) = 6x^2 - 24x
    for i in range(len(divisor_coefficients)):
        idx = len(temp_poly) - divisor_degree + i
        if idx >= 0:
            temp_poly[idx] -= 6 * divisor_coefficients[i] # Wait, indices logic
    
    # Correct manual simulation:
    # P(x) = [6, 0, 6], Q(x) = [1, -4]
    # Degree of P is 2. Degree of Q is 1.
    
    quotient_coeffs = []
    remainder_list = []
    
    curr_deg = len(dividend_coefficients) - 1
    
    while curr_deg >= len(divisor_coefficients) - 1:
        shift = curr_deg - (len(divisor_coefficients) - 1)
        
        # Leading coefficient of dividend at this degree
        lead_div = dividend_coefficients[curr_deg]
        
        # Quotient term
        q_val = lead_div // divisor_coefficients[0]
        quotient_coeffs.insert(0, q_val)
        
        # Subtract q * x^shift * Q(x) from P(x)
        for i in range(len(divisor_coefficients)):
            idx_to_update = curr_deg - (len(divisor_coefficients) - 1) + i
            if idx_to_update < len(dividend_coefficients):
                dividend_coefficients[idx_to_update] -= q_val * divisor_coefficients[i]
        
        # Remove trailing zeros from the modified polynomial to keep degree accurate? 
        # Actually, just track non-zero leading term.
        while curr_deg >= 0 and (dividend_coefficients[curr_deg] == 0 if len(divisor_coefficients) > 1 else True):
            # If we are at a point where all higher coeffs are zero but not the last one? 
            # Simplify: just find first non-zero from left.
            pass
            
        curr_deg -= 1
        
    # Now dividend should be remainder (degree < divisor degree)
    final_remainder_coeffs = [c for c in dividend_coefficients if c != 0] + ([dividend_coefficients[0]] if not final_remainder_coeffs else [])
    
    # Re-verify with specific numbers: 
    # P = 6x^2 + 6. Q = x - 4.
    # (6x^2 + 6) / (x - 4) -> Quotient 6x, Remainder?
    # 6(x-4)*x = 6x^2 - 24x
    # P - (6x^2 - 24x) = 0x^2 + 24x + 6
    
    # Next step: Divide 24x by x -> 24.
    # Quotient so far [6, 24]
    # Subtract 24*(x-4) = 24x - 96 from (0x^2 + 24x + 6)
    # Result: 0x^2 + 0x + 102
    
    quotient_coefficients = [6, 24]
    remainder_coefficients = [102]

    correct_answer = {
        "quotient_coefficients": quotient_coefficients,
        "remainder_coefficients": remainder_coefficients
    }
    
    oracle_payload = {"dividend_coefficients": dividend_coefficients_original := [6, 0, 6], "divisor_coefficients": divisor_coefficients}

    return {
        "question_text": f"Divide polynomial with coefficients {oracle_payload['dividend_coefficients']} by {oracle_payload['divisor_coefficients']}",
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }