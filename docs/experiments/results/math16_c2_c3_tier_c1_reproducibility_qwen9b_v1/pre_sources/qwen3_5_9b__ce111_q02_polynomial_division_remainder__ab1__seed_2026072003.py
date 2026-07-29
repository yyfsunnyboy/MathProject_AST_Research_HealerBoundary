def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    # Polynomial: P(x) = 6x^2 + 4x (from coefficients [6, 4, 0])
    # Divisor: D(x) = 2x^2 (from coefficients [2, 0, 0])
    # Division: (6x^2 + 4x) / (2x^2) = 3 + (4/x). 
    # Quotient is constant term of polynomial division if degree(dividend) >= degree(divisor), but here degrees are equal.
    # Standard polynomial long division for P(x)/D(x):
    # Leading coeff ratio: 6/2 = 3. New quotient term x^(deg_P - deg_D) = x^0 = 1. So Q=3? 
    # Wait, let's do it formally.
    # P(x) = 6x^2 + 4x + 0
    # D(x) = 2x^2 + 0x + 0
    # Step 1: (6x^2)/(2x^2) = 3. Multiply D by 3 -> 6x^2. Subtract from P -> remainder is 4x.
    # Degree of remainder (1) < degree of divisor (2). Stop.
    # Quotient Q(x) = 3. Remainder R(x) = 4x.
    
    quotient_coefficients = [3]
    remainder_coefficients = [0, 4]  # Represents 4x
    
    question_text = r"Given the dividend polynomial $P(x)$ with coefficients $\{6, 4, 0\}$ and the divisor polynomial $D(x)$ with coefficients $\{2, 0, 0\}$, perform polynomial division to find the remainder. Express your answer as a polynomial."
    correct_answer = f"remainder: {remainder_coefficients}, canonical_latex: \\{{{', '.join(map(str, reversed(remainder_coefficients)))}}\\}" if len(remainder_coefficients) > 1 else f"remainder: {remainder_coefficients[0]}, canonical_latex: {{{remainder_coefficients[0]}}}x^{{len(remainder_coefficients)-2}}"
    
    # Re-evaluating correct_answer format based on typical expectations for [0, 4]: it is $4x$. 
    # If remainder is constant c, latex is {c}. If linear ax+b (b=0 here), latex is {a}x.
    if len(remainder_coefficients) == 1:
        val = remainder_coefficients[0]
        correct_answer = f"remainder: [{val}], canonical_latex: {{{val}}}"
    else:
        # For [0, 4], it represents $0 + 4x$. Canonical latex usually omits leading zeros or writes standard form.
        # Standard polynomial string for coefficients [c_n, ..., c_0] is sum(c_i x^i).
        terms = []
        for i in range(len(remainder_coefficients) - 1, -1, -1):
            coeff = remainder_coefficients[i]
            if coeff == 0: continue
            power = len(remainder_coefficients) - 1 - i
            term_str = f"{coeff}x^{{{power}}}" if power > 1 else (f"({coeff})x" if abs(coeff)==1 and power==1 else str(coeff)) # Simplify signs? No, just raw.
            # Actually simpler: construct latex directly from coeffs list logic used in similar tasks usually implies standard form.
            pass
        
        # Let's stick to the specific calculation result: 4x.
        correct_answer = "remainder: [0, 4], canonical_latex: \\{4\\}x"

    oracle_payload = {"dividend_coefficients": dividend_coefficients, "divisor_coefficients": divisor_coefficients}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }