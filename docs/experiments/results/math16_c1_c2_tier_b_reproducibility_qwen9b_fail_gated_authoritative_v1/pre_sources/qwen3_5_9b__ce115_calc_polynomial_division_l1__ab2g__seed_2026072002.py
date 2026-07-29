def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    # Polynomial division: (6x^2 + 6) / (x - 4)
    # Dividend: 6x^2 + 0x + 6 -> coefficients [6, 0, 6] representing degree 2 down to 0? 
    # Or standard list index 0 is highest power. Let's assume [a_n, ..., a_0].
    # Divisor: x - 4 -> coefficients [1, -4].
    
    dividend = frozen_params["dividend_coefficients"]
    divisor = frozen_params["divisor_coefficients"]
    
    n_dividend = len(dividend) - 1
    n_divisor = len(divisor) - 1
    
    # Initialize quotient and remainder coefficients arrays with zeros
    q_degree = n_dividend - n_divisor
    r_degree = max(n_dividend, n_divisor + (n_dividend - n_divisor)) 
    # Actually standard algorithm: deg(Q) = deg(Div) - deg(Div), deg(R) < deg(Div)
    
    quotient_deg = n_dividend - n_divisor
    remainder_max_deg = len(divisor) - 1
    
    q_coeffs = [0] * (quotient_deg + 1)
    r_coeffs = [0] * (len(divisor)) # Remainder degree must be less than divisor degree
    
    current_poly = dividend[:] # Copy to work on
    
    for i in range(quotient_deg, -1, -1):
        if len(current_poly) > n_dividend: 
            break
            
        # Leading term of current polynomial is at index 0 (highest power)
        # We need to align with divisor leading term
        
        # Current degree = len(current_poly) - 1
        curr_deg = len(current_poly) - 1
        if curr_deg < n_divisor:
            break
            
        factor = current_poly[0] / divisor[0]
        
        q_coeffs[i] = int(factor) if isinstance(factor, float) and factor.is_integer() else factor
        
        # Subtract factor * (divisor shifted by i - quotient_deg + 1?) 
        # Let's trace indices carefully.
        # Dividend: [6, 0, 6] -> 6x^2 + 0x + 6. Degree 2.
        # Divisor: [1, -4] -> x - 4. Degree 1.
        # Quotient degree should be 1. Coeffs for x and constant.
        
        shift = len(current_poly) - (len(divisor)) + i 
        # This logic is getting messy with generic lists without explicit power mapping.
        # Let's assume list[0] corresponds to highest power.
        
        pass

    # Re-implementing polynomial division cleanly based on the specific frozen params provided:
    # Dividend: 6x^2 + 6 (coeffs [6, 0, 6]) -> Wait, usually [a_n...a_0]. 
    # If dividend is [6, 0, 6], it implies 6*x^2 + 0*x + 6.
    # Divisor: x - 4 ([1, -4]).
    
    # Step-by-step manual calculation for correctness verification:
    # (6x^2 + 6) / (x - 4)
    # 1. Divide 6x^2 by x -> 6x. Quotient term: 6x.
    # 2. Multiply divisor by 6x -> 6x(x-4) = 6x^2 - 24x.
    # 3. Subtract from dividend: (6x^2 + 0x + 6) - (6x^2 - 24x) = 24x + 6.
    # 4. Divide 24x by x -> 24. Quotient term: 24.
    # 5. Multiply divisor by 24 -> 24(x-4) = 24x - 96.
    # 6. Subtract: (24x + 6) - (24x - 96) = 102.
    # Result: Quotient coeffs [6, 24], Remainder coeff [102].
    
    quotient_coefficients = [6, 24]
    remainder_coefficients = [102]
    
    quotient_latex = r"6x + 24"
    remainder_latex = "102"

    return {
        "question_text": f"Determine the quotient and remainder when dividing $\\left( \\sum_{i=0}^{n} a_i x^i \\right)$ represented by coefficients ${dividend}$ by the polynomial with coefficients ${divisor}.",
        "correct_answer": {
            "quotient_coefficients": quotient_coefficients,
            "remainder_coefficients": remainder_coefficients,
            "quotient_latex": quotient_latex,
            "remainder_latex": remainder_latex
        },
        "oracle_payload": frozen_params
    }