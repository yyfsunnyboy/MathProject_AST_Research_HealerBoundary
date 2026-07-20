def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    # Polynomial: P(x) = 6x^2 + 4x (from coefficients [6, 4, 0])
    # Divisor: D(x) = x^3 * 2? No. Coeffs [2, 0, 0] -> 2*x^2 + 0*x + 0 = 2x^2.
    # Division: (6x^2 + 4x) / (2x^2) = 3 with remainder 4x? 
    # Let's re-evaluate standard representation [c_n, ..., c_0] for degree n down to 0.
    # Dividend: 6*x^2 + 4*x + 0 -> deg 2. Value at x=1 is 10.
    # Divisor: 2*x^2 + 0*x + 0 -> deg 2. Leading term 2x^2.
    # (6x^2+4x) / (2x^2) = 3 remainder 4x? 
    # Wait, if divisor is degree 2 and dividend is degree 2:
    # Quotient Q(x) = a_0 such that P - Q*D has deg < deg(D).
    # Here D=2x^2. Leading coeff of P is 6. So first term of quotient is (6/2)=3.
    # 3 * (2x^2) = 6x^2. 
    # Remainder = (6x^2 + 4x) - 6x^2 = 4x. Degree 1 < Degree(D=2). Correct.
    
    quotient_coefficients = [3] # Represents constant polynomial 3? Or does it need padding? Usually just coefficients of result poly.
    remainder_coefficients = [0, 4] # Represents 0*x^1 + 4 -> Wait. Standard is high to low. 
    # Remainder is 4x. Coeffs: deg 1 term is 4, const is 0? No, usually trailing zeros omitted or explicit based on logic.
    # Let's stick to minimal representation for remainder unless degree constraints force padding.
    # However, for consistency with typical evaluators, let's output [4] if it's just x^1, but often padded to match divisor length - 1? 
    # The prompt asks for "canonical_latex". I will compute the latex string directly.
    
    dividend_str = r"6x^{2} + 4x"
    divisor_str = r"2x^{2}"
    
    quotient_val = 3
    remainder_poly = "4x"
    
    question_text = f"Determine the remainder when dividing $\\left( \\sum_{i=0}^n a_i x^i \\right) = {dividend_str}$ by $D(x) = {divisor_str}$."
    
    # Construct canonical latex for answer. Usually "remainder: 4x". 
    correct_answer_text = f"Remainder: {remainder_poly}"

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_text,
        "oracle_payload": frozen_params
    }