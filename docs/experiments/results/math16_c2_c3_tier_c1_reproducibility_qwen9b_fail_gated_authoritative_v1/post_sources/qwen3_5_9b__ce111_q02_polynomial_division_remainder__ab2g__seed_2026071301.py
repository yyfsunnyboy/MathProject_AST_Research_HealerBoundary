def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    dividend_poly = sum(frozen_params["dividend_coefficients"][i] * (x**i) for i in range(len(frozen_params["dividend_coefficients"])))
    divisor_poly = sum(frozen_params["divisor_coefficients"][j] * (x**j) for j in range(len(frozen_params["divisor_coefficients"])))
    
    # Perform polynomial division manually to get quotient and remainder
    dividend_coeffs = frozen_params["dividend_coefficients"].copy()
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    if not divisor_coeffs:
        raise ValueError("Divisor cannot be empty.")
        
    leading_divisor_degree = len(divisor_coeffs) - 1
    
    quotient_coeffs = [0] * (len(dividend_coeffs) + len(divisor_coeffs))
    remainder_coeffs = dividend_coeffs.copy()
    
    for i in range(len(remainder_coeffs)):
        if abs(remainder_coeffs[i]) < 1e-9:
            continue
            
        current_degree = i - leading_divisor_degree
        
        if current_degree >= 0 and divisor_coeffs[leading_divisor_degree] != 0:
            factor = remainder_coeffs[i] / divisor_coeffs[leading_divisor_degree]
            
            for j in range(len(divisor_coeffs)):
                quotient_idx = (i + j) - leading_divisor_degree
                
                if current_degree >= 0 and quotient_idx < len(quotient_coeffs):
                    quotient_coeffs[current_degree + j] += factor * divisor_coeffs[j]
                    
    # Calculate remainder by subtracting the product of quotient and divisor from dividend
    for i in range(len(dividend_coeffs)):
        term = sum(frozen_params["divisor_coefficients"][j] * (x**(i - leading_divisor_degree)) for j in range(len(divisor_coeffs))) if i >= leading_divisor_degree else 0
        
    # Simplify remainder coefficients by removing trailing zeros and handling negative signs correctly
    while len(remainder_coeffs) > 1 and abs(remainder_coeffs[-1]) < 1e-9:
        remainder_coeffs.pop()
        
    canonical_remainder = " + ".join([f"{c}" if c >= 0 else f"-{abs(c)}" for c in reversed(remainder_coeffs)])
    
    question_text = (r"The polynomial $P(x) = {}$ is divided by the polynomial $D(x) = {}$. Find the remainder of this division.".format(dividend_poly, divisor_poly))
    
    return {
        "question_text": question_text,
        "correct_answer": canonical_remainder,
        "oracle_payload": frozen_params
    }