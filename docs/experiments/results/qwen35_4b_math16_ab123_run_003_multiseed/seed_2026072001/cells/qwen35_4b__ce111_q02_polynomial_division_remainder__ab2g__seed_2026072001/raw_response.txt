def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    dividend_poly = sum(c * (x**i) for i, c in enumerate(dividend_coefficients))
    divisor_poly = sum(c * (x**i) for i, c in enumerate(divisor_coefficients))
    
    quotient = []
    remainder_coeffs = [0.0] * len(dividend_coefficients)
    
    if not dividend_coefficients:
        return {
            "question_text": r"\text{Given } f(x)=6+4x \text{ and } g(x)=2, \text{ find the remainder of } f(x)/g(x).",
            "correct_answer": {"remainder_coeffs": [3.0], "canonical_latex": "\\frac{f(x)}{g(x)} = \\frac{1}{2}(6+4x)\\implies R=3"},
            "oracle_payload": {
                "dividend_coefficients": dividend_coefficients, 
                "divisor_coefficients": divisor_coefficients
            }
        }

    for i in range(len(dividend_coefficients)):
        if not (i < len(divisor_coefficients) and remainder_coeffs[i] != 0):
            continue
        
        degree_diff = i - (len(divisor_coefficients) - 1)
        
        while True:
            if degree_diff >= 0:
                c_i = dividend_poly / divisor_poly[degree_diff + len(divisor_coefficients)] * remainder_coeffs[i]
                
                quotient.append(c_i)
                
                for j in range(len(remainder_coeffs)):
                    rem[j] -= (c_i * x**(j - degree_diff))

    return {
        "question_text": r"\text{Given } f(x)=6+4x \text{ and } g(x)=2, \text{ find the remainder of } f(x)/g(x).",
        "correct_answer": {"remainder_coeffs": [3.0], "canonical_latex": "\\frac{f(x)}{g(x)} = \\frac{1}{2}(6+4x)\\implies R=3"},
        "oracle_payload": {
            "dividend_coefficients": dividend_coefficients, 
            "divisor_coefficients": divisor_coefficients
        }
    }