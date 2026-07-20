import sympy as sp

def generate(level=1, **kwargs):
    # Frozen sampled parameters from specification
    dividend_coeffs = [6, 0, 6]
    divisor_coeffs = [1, -4]
    
    x = sp.Symbol('x')
    
    # Construct polynomials using frozen coefficients (Exact arithmetic)
    P_dividend = sum(c * (x ** i) for i in range(len(dividend_coeffs)))
    P_divisor = sum(c * (x ** i) for i in range(len(divisor_coeffs)))
    
    # Perform polynomial division over integers/rational numbers to ensure exactness
    quotient, remainder = sp.div(P_dividend, P_divisor, domain='QQ')
    
    # Extract coefficients ensuring correct order from highest degree down to constant term
    q_degree = len(quotient) - 1 if len(quotient) > 0 else 0
    
    # Handle edge case where quotient is zero (though unlikely with these inputs)
    if len(quotient) == 0:
        q_coeffs = [0] * max(len(dividend_coeffs), len(divisor_coeffs))
    else:
        q_coeffs = list(map(int, sp.Poly(quotient, x).all_coeffs()))
    
    r_degree = len(remainder) - 1 if len(remainder) > 0 else 0
    
    # Ensure remainder length matches dividend degree or divisor logic (pad with zeros if needed for consistency in output format usually expected as list of same max length or aligned)
    # Standard representation: quotient and remainder coefficients lists. 
    # Let's align them to the maximum required length based on inputs, padding leading zeros where necessary for symmetry often seen in such tasks, but strictly following math results first.
    
    r_coeffs = list(map(int, sp.Poly(remainder, x).all_coeffs()))
    
    # Pad quotient and remainder with leading zeros so both lists have the same maximum expected length (max dividend degree + 1 usually)
    max_len = len(dividend_coeffs)
    
    while len(q_coeffs) < max_len:
        q_coeffs.insert(0, 0)
        
    while len(r_coeffs) < max_len:
        r_coeffs.insert(0, 0)
        
    # Generate LaTeX representations for coefficients using formal delimiters \( \) and \[ \] as requested in question_text structure logic (though specific format not fully defined beyond usage of delimiters)
    
    q_latex = ", ".join(f"{c}" if c != 0 else "0" for c in q_coeffs).replace(", 0", "\\,") # Simplified join
    r_latex = ", ".join(f"{c}" if c != 0 else "0" for c in r_coeffs)

    question_text = f"""Given the polynomials: \\( P(x) = {P_dividend} \\) and \( Q(x) = {P_divisor} \), perform polynomial division.
Find the quotient coefficients, remainder coefficients, their LaTeX representations, and verify with frozen parameters."""

    correct_answer = {
        "quotient_coefficients": q_coeffs,
        "remainder_coefficients": r_coeffs,
        "quotient_latex": f"\\({q_latex}\\)",
        "remainder_latex": f"[{r_latex}]" # Using bracket for list representation inside latex context if needed, or just text. 
    }

    oracle_payload = {
        "dividend_coefficients": dividend_coeffs,
        "divisor_coefficients": divisor_coeffs
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }