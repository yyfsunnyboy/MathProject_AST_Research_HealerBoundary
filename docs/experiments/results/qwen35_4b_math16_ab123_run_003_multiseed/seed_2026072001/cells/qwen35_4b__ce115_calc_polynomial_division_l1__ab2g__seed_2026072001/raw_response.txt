def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    # Polynomial division: (6x^2 + 0x + 6) / (x - 4)
    # Dividend degree: 2, Divisor degree: 1 -> Quotient degree: 1
    
    dividend_poly = sum(c * x**i for i, c in enumerate(dividend_coeffs))
    divisor_poly = sum(c * x**i for i, c in enumerate(divisor_coeffs))
    
    # Synthetic division or long hand calculation logic here to ensure exact arithmetic
    # Dividend: 6x^2 + 0x + 6
    # Divisor: x - 4 (root at 4)
    # Leading term of dividend: 6x^2 / x = 6x
    
    quotient_coeffs = []
    remainder_coeffs = [0] * len(dividend_poly[-1]) if not divisor_coeffs else [0]*(len(dividend_poly)-len(divisor_coeffs)+1) 
    # Actually, let's compute manually for precision without external libraries
    
    dividend_list = list(reversed(dividend_coeffs))  # [6, 0, 6] -> reversed: [6, 0, 6] (deg 2 to 0)
    divisor_list = list(reversed(divisor_coeffs))     # [1, -4] -> reversed: [-4, 1]
    
    if len(dividend_list) < len(divisor_list):
        return {"question_text": "Error", "correct_answer": {}, "oracle_payload": frozen_params}
        
    quotient_degree = len(dividend_list) - len(divisor_list)
    quotient_coeffs_init = [0] * (quotient_degree + 1)
    
    # Perform division step by step from highest degree down to lowest in dividend
    current_dividend = list(reversed([6, 0, 6])) # Start with reversed original for easier index access? 
    # Let's stick to standard long division logic on the lists as they are [high_to_low]
    
    working_poly = list(dividend_coeffs)[:] # Copy
    
    q_idx = len(working_poly) - 1
    d_lead_index = 0
    divisor_len = len(divisor_coeffs)
    
    quotient_result = []
    remainder_result = list(workings_poly[:])
    
    for i in range(len(working_poly)):
        if working_poly[i] == 0: continue
        
        # The leading term of current dividend is working_poly[len(working_poly)-1-i]? No.
        # Working poly [6, 0, 6]. Leading coeff is index 0 (value 6).
        
    # Re-implementing clean synthetic division logic
    
    n = len(dividend_coeffs) - 1
    m = len(divisor_coeffs) - 1
    
    if n < m:
        q_deg = -2 # Error case handled by check above, but returning early for safety
        
    quotient_list = [0] * (n + 1 - m)
    
    curr_poly = list(reversed([6, 0, 6])) 
    divisor_rev = list(reversed([-4, 1])) 
    
    # Standard synthetic division with root r=4
    
    # Coeffs of dividend: a2=6, a1=0, a0=6
    # Divisor x-4 -> root b=4
    
    coeffs_to_divide = [6, 0, 6]
    
    q_coeffs_calc = []
    rem_val = 0
    
    for i in range(len(coeffs_to_divide)):
        if i == len(q_coeffs_calc): continue # Skip first init
        
        val = coeffs_to_divide[i-1] + (rem_val) * divisor_rev[1] 
        wait, synthetic division logic:
        
        b_0 = 6 // (-4)? No. Synthetic uses root r such that x-r is divisor.
        Here divisor is x - 4, so r = 4.
        
        # Bring down leading coeff
        q_list = [coeffs_to_divide[0]] 
        rem_acc = coeffs_to_divide[1] + (q_list[-1]) * (-r) ? No formula: new_val = prev_coeff + root*prev_q
        
        r_val = 4
        
        # Synthetic Division Algorithm
        b_coeffs = list(coeffs_to_divide[:]) # Copy dividend coefficients [6, 0, 6]
        
        quotient_temp = []
        remainder_temp = 0
        
        for i in range(len(b_coeffs)-1):
            if not quotient_temp:
                quotient_temp.append(0) 
                
            next_val = b_coeffs[i+1] + (quotient_temp[-1]) * r_val
            
            # Wait, standard synthetic division adds root*prev_quotient to current coeff?
            # Actually: new_coeff = old_coeff - q*r ? Or +?
            # Polynomial P(x) / (x-r). 
            # If we have coeffs [a_n ... a_0].
            # b_{n-1} = a_n. Then b_i = a_{i+1} + r * b_{i+1}. No, it's usually: carry down, add product.
            
        Let's do direct polynomial long division to be absolutely safe and exact.
        
    dividend_poly_str = "6x^2"
    
    # Long Division Manual Trace
    # Dividend: 6x^2 + 0x + 6
    # Divisor: x - 4
    
    # Step 1: Divide leading terms -> (6x^2) / (x) = 6x. Add to quotient list [6, 0] (since deg is 1).
    # Multiply divisor by 6x: 6x(x-4) = 6x^2 - 24x
    
    # Subtract from dividend: 
    #   (6x^2 + 0x + 6)
    # - (6x^2 - 24x)
    # ----------------
    #      24x + 6
    
    # Step 2: Divide leading terms -> (24x) / (x) = 24. Add to quotient list [6, 0] *-> [6, 24].
    # Multiply divisor by 24: 24(x-4) = 24x - 96
    
    # Subtract from remainder:
    #      24x + 6
    #   - (24x - 96)
    # --------------
    #         102
    
    quotient_coeffs_final = [6, 24]
    remainder_val_final = 102
    
    question_text = r"Calculate the division of polynomials. \n\(\text{Dividend: } (6x^2 + 0x + 6)\) divided by \(x - 4\)."
    
    quotient_latex = "$$\\frac{(6x^2+1)}{1}$$".replace("","").split("/")[-1] # Placeholder fix needed
    
    # Constructing correct LaTeX properly
    q_str = "6x + 24"
    r_str = "102"
    
    quotient_latex = f"{q_str}"
    remainder_latex = str(r_str)
    
    correct_answer_dict = {
        "quotient_coefficients": [6, 24],
        "remainder_coefficients": [102], # Represented as constant term in list of length deg+1? Or just value. Spec says coefficients. For degree -1 (constant), it's a single element list or empty if remainder is zero? 
                           # Usually for scalar remainder, we provide the coefficient(s) relative to x^(-k)? No, standard output is [remainder_value]
        "quotient_latex": quotient_latex,
        "remainder_latex": remainder_latex
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }