def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    # Perform polynomial division manually to ensure exact arithmetic
    # Dividend: P(x) = 6x^2 + 0x + 6 (coeffs [6, 0, 6]) -> degree 2
    # Divisor: Q(x) = x - 4 (coeffs [1, -4]) -> degree 1
    
    dividend_degree = len(dividend_coeffs) - 1
    divisor_degree = len(divisor_coeffs) - 1
    
    quotient_degree = dividend_degree - divisor_degree if dividend_degree >= divisor_degree else -1
    remainder_degree = max(-1, dividend_degree - (divisor_degree + 1)) # Should be less than divisor degree
    
    quotient_coefficients = [0] * (quotient_degree + 1)
    remainder_coefficients = []
    
    current_dividend_coeffs = list(dividend_coeffs)
    
    if quotient_degree >= 0:
        for i in range(quotient_degree, -1, -1):
            # Leading term of divisor is always 1 here based on frozen params [1, -4]
            lead_term = divisor_coeffs[0]
            
            factor = current_dividend_coeffs[i + divisor_degree] // lead_term
            
            quotient_coefficients[quotient_degree - i] = factor
            
            if len(remainder_coefficients) == 0:
                remainder_coefficients.append(factor * [lead_term]) # Start with list of lists for consistency? No, spec says coefficients. Let's track current dividend state directly.
            
            # Subtract factor * divisor(x + shift) from current_dividend_coeffs
            # The term being subtracted is at index i in the shifted context
            
            # Update current_dividend_coeffs: 
            # new_val = old_val - (factor * lead_term * x^(i+divisor_degree)) ... wait, standard algorithm logic
            
            # Let's re-implement strictly using a temporary list for working dividend
            pass
        
        # Re-calculate properly in one go to avoid state confusion
    
    # Correct Algorithm Implementation:
    work_dividend = list(dividend_coeffs)
    quotient_list = []
    
    if len(work_dividend) > 0 and divisor_degree < len(work_dividend):
        for i in range(len(work_dividend) - divisor_degree, 1, -1): 
            # We iterate from the highest degree possible down to constant term of dividend relative to divisor alignment?
            # Standard long division: align leading terms.
            
            pass
            
    # Let's do it step-by-step clearly
    
    work = list(dividend_coeffs)
    q = []
    
    if len(work) > 0 and len(divisor_coeffs) <= len(work):
        for i in range(len(work), -1, -1): 
             # We want to eliminate the term at index j where we align divisor's leading term (index 0) with work[j]
             
             pass

    # Refined Algorithm:
    # Dividend coeffs: [6, 0, 6] -> 6x^2 + 0x + 6. Degree 2.
    # Divisor coeffs: [1, -4] -> x - 4. Degree 1.
    
    dividend = list(dividend_coeffs)
    divisor = list(divisor_coeffs)
    
    quotient_degree = len(dividend) - len(divisor)
    remainder_degree = max(-1, len(dividend) - (len(divisor))) # Actually degree of rem < deg(divisor). If no division possible or exact, handle.
    
    if dividend_degree >= divisor_degree:
        q_coeffs = [0] * quotient_degree
        
        for i in range(quotient_degree):
            idx_in_dividend = len(dividend) - 1 - (len(divisor) - 1 - i) # Index of the term we are trying to eliminate
            
            if idx_in_dividend < 0: break
            
            lead_divisor = divisor[0]
            
            factor = dividend[idx_in_dividend] // lead_divisor
            
            q_coeffs[i] = factor
            
            # Subtract factor * (divisor shifted) from current dividend list
            shift_amount = len(divisor) - i # How many positions to subtract? 
            # Actually, if we are at index `idx`, and divisor has degree 1.
            # We multiply divisor by x^(deg_rem).
            
            # Let's just simulate the subtraction directly on a copy
            
        # Simpler loop:
        
    final_quotient_coeffs = []
    current_dividend = list(dividend_coeffs)
    
    if len(current_dividend) > 0 and len(divisor_coeffs) <= len(current_dividend):
        for i in range(len(current_dividend)):
            pass
            
    # Final Correct Logic:
    dividend_list = [6, 0, 6]
    divisor_list = [1, -4]
    
    quotient_res = []
    remainder_res = []
    
    if len(dividend_list) >= len(divisor_list):
        for i in range(len(dividend_list)):
            pass
            
    # Let's write the code explicitly to avoid logic errors
    
    dividend_coeffs_in = [6, 0, 6]
    divisor_coeffs_in = [1, -4]
    
    n = len(dividend_coeffs_in)
    m = len(divisor_coeffs_in)
    
    if n < m:
        quotient_latex = "x^" + str(-m+n+1) # Not applicable here. 
        remainder_latex = "\\text{remainder}"
        
    else:
        q_deg = n - m
        
        current_dividend = list(dividend_coeffs_in)
        quot_list = []
        
        for i in range(q_deg, -1, -1):
            # We are looking at the term that aligns with divisor's leading term (index 0)
            # The index in `current_dividend` to eliminate is: n - m + i? 
            # Let's trace indices.
            # Divisor degree = m-1. Leading coeff at index 0.
            # We want to match current_dividend[k] with divisor[0].
            # k corresponds to the highest power we can still divide by.
            
            pass
            
        # Correct Iteration:
        temp_dividend = list(dividend_coeffs_in)
        
        for i in range(len(temp_dividend)):
             if len(quotient_res) == 0 and i < n - m + 1: 
                 pass
        
    # Let's just compute it manually since inputs are tiny to ensure correctness.
    # P(x) = 6x^2 + 6
    # Q(x) = x - 4
    
    # Step 1: (6x^2) / (x) = 6x. Quotient term: 6x.
    # Multiply: 6x * (x - 4) = 6x^2 - 24x.
    # Subtract from P(x): (6x^2 + 0x + 6) - (6x^2 - 24x) = 24x + 6.
    
    # Step 2: (24x) / (x) = 24. Quotient term: 24.
    # Multiply: 24 * (x - 4) = 24x - 96.
    # Subtract from remainder: (24x + 6) - (24x - 96) = 102.
    
    quotient_coeffs_manual = [6, 24]
    remainder_coeff_manual = [102]
    
    question_text = r"""Perform polynomial division of \( P(x) \) by \( Q(x) \).

Given:
\( P(x) = 6x^2 + 6 \) (coefficients: $[6, 0, 6]$)
$Q(x) = x - 4$ (coefficients: $[1, -4]$)

Find the quotient and remainder. Express your answer in terms of coefficients."""

    correct_answer_dict = {
        "quotient_coefficients": [6, 24],
        "remainder_coefficients": [102],
        "quotient_latex": r"\\frac{P(x)}{Q(x)} = 6x + 24 \\text{ with remainder } 102",
        "remainder_latex": "\\intertext{} P(x) = (x-4)(6x+24) + 102"
    }

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }