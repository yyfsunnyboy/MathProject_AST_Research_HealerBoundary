# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per specification
    dividend_coefficients = [6, 0, 6]   # Represents 6x^2 + 0x + 6
    divisor_coefficients = [1, -4]      # Represents x - 4

    # Perform polynomial division using native Python arithmetic to ensure exactness and avoid float issues.
    # Dividend: P(x) = a_n*x^n + ... + a_0 -> coefficients are given in descending order of power? 
    # Wait, standard convention for lists [6, 0, 6] usually implies highest degree first or lowest?
    # Let's check the context. "dividend_coefficients": [6, 0, 6]. If this is x^2 term, then it's 6x^2 + 0x + 1*something? 
    # Actually, looking at typical math problem formats:
    # Case A: Descending order (highest power first). [6, 0, 6] -> 6x^2 + 0x + 6. Divisor [1, -4] -> x - 4.
    # Division of 6x^2+6 by x-4: 
    #   6x^2 / x = 6x. (6x)(x-4) = 6x^2 - 24x. Remainder so far: (0 - (-24))x + 6 = 24x + 6.
    #   24x / x = 24. (24)(x-4) = 24x - 96. Remainder: 6 - (-96) = 102.
    #   Quotient coeffs [6, 24], remainder const [102].

    # Case B: Ascending order (lowest power first). [6, 0, 6] -> 6 + 0x + 6x^2? No, that's same.
    # What if it is constant term first? [a_0, a_1, ...]. Then 6 + 0*x + 6*x^2 = 6x^2+6. Same polynomial.
    # So the interpretation of list order doesn't change the polynomial value here because middle coeff is 0.

    n_dividend = len(dividend_coefficients) - 1
    degree_d = n_dividend
    
    # We need to determine if coefficients are ascending or descending. 
    # Usually, in such tasks without explicit instruction, [6, 0, 6] for a quadratic often means:
    # If it were ascending (low->high): c[0]=const, c[n]=coeff of x^n.
    # If descending (high->low): c[0]=x^n coeff.
    # Let's assume standard numpy/scipy convention which is usually high-to-low or low-to-high? 
    # Actually, let's look at the divisor [1, -4]. This represents 1*x + (-4) = x-4 (high to low).
    # If it were low to high: 1 + (-4)x. That would be unusual for a simple division task unless specified.
    # Given "x-4", coefficients are typically [1, -4] in descending order of powers.
    
    dividend = []
    divisor = []

    if n_dividend == len(dividend_coefficients) - 1: 
        # Assume high-to-low based on divisor logic (x-4 -> [1, -4])
        pass
    
    # Let's re-evaluate the division manually to be safe and construct strings.
    # Polynomial P(x) = sum(c[i] * x^(n-i)) for descending list c of length n+1? 
    # Or is it ascending? 
    # If [6, 0, 6] means 6x^2 + 6 (descending), then:
    #   Quotient Q(x) = ax+b. Remainder R(x) = r.
    #   P = D*Q + R => 6x^2+6 = (x-4)(ax+b) + r
    #             = a x^2 + b x - 4a x - 4b + r
    #             = a x^2 + (b-4a)x + (-4b+r)
    #   Match coeffs: 
    #     a = 6
    #     b - 4a = 0 => b = 24
    #     -4b + r = 6 => -96 + r = 6 => r = 102.
    #   So Q(x) = 6x + 24, R(x) = 102.
    
    if n_dividend == len(divisor_coefficients): 
        pass

    # Let's assume the list is descending (standard for many libraries unless specified otherwise).
    # Dividend: [6, 0, 6] -> 6x^2 + 6
    # Divisor: [1, -4] -> x - 4
    
    a = dividend_coefficients[0]   # coeff of x^2
    c_const = dividend_coefficients[-1] # constant term (since middle is 0)
    
    b_div = divisor_coefficients[0] # coeff of x in divisor
    d_const = divisor_coefficients[1] # const in divisor
    
    # Quotient calculation:
    # Leading term quotient coefficient = a / b_div = 6/1 = 6.
    # Next term (linear) comes from matching the linear part after subtracting leading product.
    # Linear coeff of dividend is 0. 
    # Product so far: 6x * (x-4) = 6x^2 - 24x.
    # Current remainder linear part: 0 - (-24) = 24.
    # Next quotient term = 24 / 1 = 24.
    
    q_lead = a // b_div if (a % b_div == 0) else float(a/b_div) 
    # Since we need exact arithmetic and no floats, assume divisibility holds or use fractions?
    # The problem says "Exact arithmetic; no floats". This implies integer division is expected.
    
    q_lead = a // b_div
    
    # Calculate the next coefficient of quotient (linear term in Q)
    # We simulate long division steps mentally to get exact integers.
    current_linear_residual = dividend_coefficients[1] - (q_lead * d_const) 
    # Wait, standard algorithm:
    # Step 1: q0 = a_n / b_m
    #       rem_0 = P(x) - q0*D(x)*x^(n-m)
    # Here n=2, m=1. Shift is x^1.
    # D(x) shifted by x: [b_div*1, d_const] -> coefficients for x^2 and x terms? 
    # Actually easier to just use the derived values from manual check above which were integers.
    
    q_linear = current_linear_residual // b_div
    
    r_final = c_const - (q_lead * divisor_coefficients[0]*divisor_coefficients[1] + q_linear*d_const) ? No.
    # Let's stick to the algebraic derivation: 
    # R(x) constant term = P(4). Why? Because remainder of division by x-4 is f(4).
    # f(x) = 6x^2+6. f(4) = 6*16 + 6 = 96 + 6 = 102. Correct.
    
    r_val = c_const - (q_lead * divisor_coefficients[0] * d_const + q_linear * divisor_coefficients[1]) 
    # Wait, remainder is just a constant here because deg(P) < deg(D)+deg(Q)? No.
    # Remainder degree must be less than divisor degree (which is 1). So R(x) = r_val.
    
    # Re-calculate properly:
    # P(x) - Q(x)*D(x) = R(x)
    # At x=4, D(4)=0 => P(4) = R(4) = r_const.
    q_lead_int = dividend_coefficients[0] // divisor_coefficients[0]
    
    # Calculate linear term of quotient:
    # We need to eliminate the x^2 term first (done by q_lead). 
    # Then we look at the resulting polynomial's x coefficient and divide by leading coeff of D.
    # Resulting poly after removing 6x^2 from dividend? No, subtract product.
    
    # Let's just use the values derived: Q = [6, 24], R = [102] (constant).
    q_coeffs = [q_lead_int, current_linear_residual // divisor_coefficients[0]] 
    r_coeffs = [r_val]

    quotient_latex = f"{q_coeffs[0]}x + {q_coeffs[1]}" if len(q_coeffs) > 1 else str(q_coeffs[0])
    remainder_latex = f"{r_coeffs[0]}" # Constant
    
    question_text = (f"Divide the polynomial $\\left(6x^2+{dividend_coefficients[-1]}\\right)$ by $(x-4). "
                     f"What are the quotient and remainder coefficients? "
                     f"The dividend is represented as {dividend_coefficients} and divisor as {divisor_coefficients}.")

    correct_answer = {
        "quotient_coefficients": q_coeffs,
        "remainder_coefficients": r_coeffs,
        "quotient_latex": quotient_latex,
        "remainder_latex": remainder_latex
    }

    oracle_payload = {"dividend_coefficients": dividend_coefficients, "divisor_coefficients": divisor_coefficients}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }