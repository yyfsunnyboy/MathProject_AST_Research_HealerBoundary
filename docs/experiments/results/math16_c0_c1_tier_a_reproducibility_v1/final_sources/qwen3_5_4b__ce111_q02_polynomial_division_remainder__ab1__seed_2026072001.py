def generate(level=1, **kwargs):
    import random
    
    # Frozen parameters from task specification
    dividend_coeffs = [6, 4, 0]
    divisor_coeffs = [2, 0, 0]
    
    # Construct polynomials: P(x) = sum(coeffs[i]*x^i), Q(x) = sum(divisor_coeffs[j]*x^j)
    # Dividend: 6 + 4x (degree 1) -> coefficients are constant term first? 
    # Standard convention in many coding tasks is highest degree first, but let's check the list length vs degree.
    # If [6, 4, 0] represents a=2nd deg, b=1st, c=0th: P(x)=x^2+4x+6? Or x^2+4x (if last is constant)?
    # Usually in these specific math tasks (ce111), the list [a, b, c] often maps to ax^2 + bx + c.
    # Let's assume standard polynomial representation where index 0 is highest degree or lowest?
    # Given "dividend_coefficients": [6, 4, 0], if it were x^2+4x+6, division by 2 might not yield integer remainder easily without specific setup.
    # However, looking at the divisor [2, 0, 0] -> likely 2x^2? Or just constant 2? 
    # If divisor is [2, 0, 0], and dividend is [6, 4, 0].
    # Let's assume the list represents coefficients from highest degree to lowest (standard in many contexts).
    # Dividend: 6x^2 + 4x + 0 = 6x^2 + 4x. Degree 2.
    # Divisor: 2x^2 + 0x + 0 = 2x^2. Degree 2.
    
    # Perform polynomial division manually to ensure correctness for the oracle payload match logic if needed, 
    # but since parameters are frozen and fixed here, we can hardcode the result of this specific instance 
    # or implement a generic solver that matches these inputs exactly.
    
    def poly_divide(dividend_coeffs, divisor_coeffs):
        """Returns (quotient_coefficients, remainder_coefficients)"""
        if len(divisor_coeffs) == 0:
            return [], dividend_coeffs
        
        deg_d = len(divisor_coeffs) - 1 # Assuming highest degree first index 0 is max power? 
                                        # Wait, let's re-evaluate the list structure.
                                        # If [6,4,0] means c_2*x^2 + c_1*x + c_0, then deg=2.
        if len(dividend_coeffs) < len(divisor_coeffs):
            return [], dividend_coeffs
        
        quotient = []
        remainder = list(dividend_coeffs)
        
        # Align degrees: assume index 0 is highest degree term (e.g., x^n)
        while True:
            deg_r = len(remainder) - 1
            
            if deg_r < len(divisor_coeffs) - 1:
                break
                
            leading_div_term_coefficient = remainder[deg_r] / divisor_coeffs[len(divisor_coeffs)-1] # Assuming last index is constant? 
                                                    # NO, standard math notation in lists for polynomials often puts highest power first.
                                                    # Let's assume [a,b,c] -> ax^2 + bx + c.
            # So leading coeff of remainder at deg_r (which corresponds to index len-1-deg_r) is remainder[deg_r]? 
            # Actually, if list is [c_n, ..., c_0], then term x^n has coefficient list[n]. No, that's wrong.
            
        # Let's try the other common convention: List[i] = coeff of x^i (lowest power first).
        # Dividend [6, 4, 0]: 6 + 4x + 0x^2 -> P(x) = 4x+6? Or 6+4x. Degree 1 if last is highest? 
        # Usually in Python libraries like sympy or numpy:
        # If we assume [a,b,c] corresponds to a*x^n + b*x^(n-1) ... c (highest first).
        # Dividend: 6, 4, 0 -> 6x^2 + 4x. 
        # Divisor: 2, 0, 0 -> 2x^2.
        
        # Let's implement division based on Highest Degree First convention (Index 0 = Max Power).
        n_dividend = len(dividend_coeffs) - 1
        n_divisor = len(divisor_coeffs) - 1
        
        if n_divisor == 0: # Divisor is constant? [2,0,0] -> x^2 term exists. So not constant.
            pass
            
        quotient_degree = max(0, n_dividend - n_divisor)
        
        q_coefficients = []
        r_coeffs = list(dividend_coeffs)
        
        # We need to subtract multiples of divisor * x^k from dividend until degree < deg(divisor)
        current_r_deg = len(r_coeffs) - 1
        
        while True:
            if current_r_deg < n_divisor:
                break
            
            leading_coeff_rem = r_coeffs[current_r_deg] # Coeff of highest power in remainder? 
                                                        # Wait, if list is [c_n ... c_0], then index i corresponds to x^(n-i)? No.
                                                        # If list is [a,b,c] for ax^2+bx+c:
                                                        # Index 0 -> a (x^2)
                                                        # Index 1 -> b (x^1)
                                                        # Index 2 -> c (x^0)
            
            leading_coeff_div = divisor_coeffs[n_divisor] # Coeff of x^n in divisor
            
            if abs(leading_coeff_rem - leading_coeff_div * q_val) > 1e-9: 
                pass
                
        # Simpler approach for this specific frozen case to ensure exact match without complex float logic errors
        # Dividend P(x): [6, 4, 0] -> 6x^2 + 4x (assuming x^2 is first) or 6+4x? 
        # Let's assume the task implies: List index i corresponds to power n-i where n=len-1.
        # Dividend: 6*x^2 + 4*x + 0 = 6x^2 + 4x
        # Divisor: 2*x^2 + 0*x + 0 = 2x^2
        
        # Division of (6x^2 + 4x) by (2x^2):
        # Term x^2 / x^2 -> coeff 3. Quotient term: 3 * 1? No, quotient is polynomial Q(x).
        # P = D*Q + R
        # 6x^2 + 4x = (2x^2) * (3) + (-0*x - 4x)? 
        # Let's do it properly.
        
        q_coeffs = []
        r_list = list(dividend_coeffs)
        
        # Degree of divisor is n_divisor_idx? If [2,0,0] -> deg=2.
        # Leading coeff of D is 2 (at index 0).
        # We iterate from highest possible power in Q down to constant or zero.
        
        max_q_deg = len(dividend_coeffs) - 1
        
        for i in range(max_q_deg, -1, -1):
            if len(r_list) <= i: break
            
            term_rem_coeff = r_list[i] # Coeff of x^(max_power-i)? 
                                      # If list is [c2, c1, c0], then index 0 is c2 (x^2).
            
            leading_div_coeff = divisor_coeffs[0] if len(divisor_coeffs) > 0 else 1
            
            q_val = term_rem_coeff / leading_div_coeff
            
            if abs(q_val - round(q_val)) < 1e-9: # Integer arithmetic preferred for exactness in these tasks usually
                q_val = int(round(q_val))
                
            quotient_degree = i 
            q_coeffs.append(q_val)
            
            # Subtract q(x)*D(x) from current remainder
            # D(x) shifted by (i - n_divisor_idx)? No.
            # If we are at power x^k in Q, and leading term of D is x^n_d...
            # Let's restart the logic with clear indices.
            
        # Re-implementation: 
        # P = [p_n, p_{n-1}, ..., p_0] where degree n.
        # D = [d_m, d_{m-1}, ..., d_0] where degree m.
        
        deg_p = len(dividend_coeffs) - 1
        deg_d = len(divisor_coeffs) - 1
        
        if deg_d == 0: 
            return [], dividend_coeffs
            
        quotient_degree = max(0, deg_p - deg_d)
        q_list = [0] * (quotient_degree + 1)
        
        # Work backwards from highest degree of Q to lowest
        for i in range(deg_p - deg_d, -1, -1): 
            if len(dividend_coeffs) <= i: break
            
            coeff_to_remove = dividend_coeffs[i] / divisor_coeffs[0] # Leading term division
            
            q_list[len(q_list)-1-i] = int(round(coeff_to_remove))
            
        return [], []

    # Since the parameters are fixed and simple, let's calculate manually to be safe.
    # Dividend: [6, 4, 0]. Interpretation: 6x^2 + 4x (if index 0 is x^2). 
    # Or maybe [c_0, c_1, c_2] -> 6 + 4x? 
    # Let's look at the divisor [2, 0, 0]. If it were constant 2, list would be [2].
    # Since length is 3 and values are non-zero only at start, likely highest power first.
    # P(x) = 6x^2 + 4x. D(x) = 2x^2.
    # Q(x) = (6x^2)/2x^2 = 3. Remainder R(x) = 4x - 0? 
    # Wait, if we divide by x^2 term only:
    # P / D -> Leading terms cancel. Next term in remainder is the lower degree part of dividend which cannot be divided further because divisor has no lower degree terms (only x^2).
    # So Remainder = 4x + 0? 
    # But wait, if we treat coefficients as [a,b,c] for ax+b+c:
    # Dividend: 6+4x. Divisor: 2+x? No divisor is [2,0,0].
    
    # Let's assume the standard "highest degree first" convention used in many coding challenges (e.g., LeetCode polynomial division).
    # P(x) = 6*x^2 + 4*x + 0. D(x) = 2*x^2 + 0*x + 0.
    # Division: 
    # Step 1: Multiply D by 3 -> 6x^2. Subtract from P -> Remainder becomes [0, 4, 0] (coeffs of x^2, x, const).
    # Now remainder degree is 1 (< deg(D)=2). Stop.
    # Quotient = [3]. Remainder coeffs = [0, 4, 0]? Or just the part that couldn't be divided? 
    # Usually remainder should have same length as dividend or padded with zeros to match alignment? 
    # The task asks for "remainder". In polynomial division P=QD+R.
    # R(x) = 4x + 0. Coefficients [0, 4, 0] if aligned to degree 2? Or just [4]? 
    # Given the input format is a list of length 3, output likely expects same structure or trimmed.
    
    # Let's construct the answer string and payload.
    
    question_text = r"Find the remainder when dividing $P(x) = \sum_{i=0}^{2} c_i x^{\text{deg}-1-i}$ by $Q(x)$, where coefficients are given as lists." 
    # Actually simpler: "Compute the polynomial division of P(x) with coefficients [6, 4, 0] and Q(x) with coefficients [2, 0, 0]. Provide the remainder in canonical LaTeX format."
    
    correct_answer = {
        "remainder": "4x", 
        "canonical_latex": r"R(x) = 4x" # Or just $4x$? Task says include only remainder and canonical latex.
    }
    
    oracle_payload = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}

    return {
        "question_text": r"Given polynomials $P(x)$ with coefficients \texttt{[6, 4, 0]} and $Q(x)$ with coefficients \texttt{[2, 0, 0]}, compute the remainder of their division. Express the result in canonical LaTeX format.",
        "correct_answer": {
            "remainder": "4x", 
            "canonical_latex": r"R(x) = 4x"
        },
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }