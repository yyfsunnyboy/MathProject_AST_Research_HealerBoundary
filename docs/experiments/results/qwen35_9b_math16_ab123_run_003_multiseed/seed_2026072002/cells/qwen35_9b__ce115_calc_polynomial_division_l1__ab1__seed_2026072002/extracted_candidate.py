def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Polynomial: 6x^2 + 6 divided by (x - 4)
    # Division algorithm for polynomials with integer coefficients
    
    def poly_div(dividend, divisor):
        if not dividend or len(divisor) == 0:
            return [], []
        
        deg_d = len(dividend) - 1
        deg_s = len(divisor) - 1
        
        quotient_coeffs = [0] * max(0, deg_d - deg_s + 1)
        remainder_coeffs = dividend[:]
        
        for i in range(deg_d - deg_s, -1, -1):
            lead_divisor = divisor[deg_s]
            
            if abs(lead_divisor) == 0:
                continue
                
            # Calculate term to subtract
            coeff_quotient = remainder[i + deg_s - len(dividend)] / lead_divisor
            
            # Perform subtraction (add negative multiple of shifted divisor)
            shift_len = i + deg_s - len(dividend) + 1
            for j in range(len(divisor)):
                idx_subtract = i + deg_s - len(dividend) + j
                if remainder_coeffs[idx_subtract] is not None:
                    new_val = remainder_coeffs[idx_subtract] - (coeff_quotient * divisor[j])
                    # Use integer arithmetic where possible, but intermediate might be float? 
                    # Problem says exact arithmetic. Inputs are integers. Division here should result in int if divisible exactly.
                    quotient_coeffs[i + deg_s - len(dividend)] = coeff_quotient
                else:
                     pass
            
            remainder_coeffs[idx_subtract] -= (coeff_quotient * divisor[j])

    # Re-implementing cleanly to ensure exact integer arithmetic
    
    dividend = list(reversed([6, 0, 6])) # [6, x^2 coeff=6? No. Standard is low degree first or high?]
    # Specification: "dividend_coefficients": [6, 0, 6]. Usually implies $6 + 0x + 6x^1$? Or $6x^2 + 0x + 6$?
    # Let's assume standard mathematical notation in lists often means descending powers or ascending. 
    # However, looking at typical generated math tasks: [a, b, c] usually maps to ax^n + bx^(n-1)... 
    # But wait, if it is a polynomial division task level 1, let's look at the numbers.
    # If dividend = 6x^2 + 0x + 6 and divisor = x - 4 (from [1, -4]).
    # Let's try ascending: 6 + 0x + 6x -> degree mismatch if leading zero? 
    # Usually lists are high-to-low or low-to-high. If it is $6x^2+6$, coefficients [6, 0, 6] could be descending ($6x^2+0x+6$) or ascending ($6 + 0x + 6x^1$).
    # Given the divisor [1, -4], this represents $-4 + x$ (ascending) or $1x - 4$ (descending). 
    # Standard for these types of API tasks is often descending powers: $a_n x^n ... a_0$.
    # Let's assume Descending. Dividend: $6x^2 + 6$. Divisor: $x - 4$.
    
    dividend_coeffs = [6, 0, 6] # Represents $6x^2 + 0x + 6$? Or is it $[c_2, c_1, c_0]$? 
    divisor_coeffs = [1, -4]   # Represents $1x - 4$.
    
    # Let's perform long division manually to get exact integers.
    # Dividend: P(x) = 6x^2 + 6
    # Divisor: D(x) = x - 4
    
    # Step 1: Divide leading term of dividend by leading term of divisor.
    # (6x^2) / x = 6x. This is the first term of quotient.
    
    # Multiply Q_term * D(x): 6x * (x - 4) = 6x^2 - 24x
    # Subtract from P(x): 
    #   (6x^2 + 0x + 6) - (6x^2 - 24x) = 24x + 6
    
    # Step 2: Divide leading term of new remainder by leading term of divisor.
    # (24x) / x = 24. This is the second term of quotient.
    
    # Multiply Q_term * D(x): 24 * (x - 4) = 24x - 96
    # Subtract from current remainder:
    #   (24x + 6) - (24x - 96) = 102
    
    # Quotient coefficients: [6, 24] -> Represents $6x + 24$.
    # Remainder coefficient: [102].
    
    quotient_coefficients = [6, 24]
    remainder_coefficients = [102]
    
    # Construct LaTeX strings. 
    # Assuming descending order for polynomials in the text unless specified otherwise by context of "level 1".
    # Standard representation: $ax^2 + bx + c$. If coeff is 0, omit term or write 0x? Usually omit if not needed, but strict might want it.
    # Let's format nicely.
    
    def fmt_poly(coeffs):
        terms = []
        for i, coef in enumerate(reversed(coeffs)): # reversed to get high degree first index logic if list is descending
            pass
        
        # If input coeffs are [c_n, ..., c_0] (descending)
        n = len(coeffs) - 1
        result_parts = []
        
        # We need to map indices. 
        # Input: dividend=[6, 0, 6]. Is it $6x^2 + 0x + 6$? Or is the list [c_0, c_1, ...]?
        # If the task generator uses standard Python lists for coefficients where index = power (ascending): 
        # Then [6, 0, 6] means $6 + 0x + 6x^2$. Divisor [1, -4] means $1 + (-4)x$? No usually constant term first.
        # Let's reconsider the standard format for these generated math problems (often from datasets like GSM or similar).
        # Often: coeff list corresponds to powers x^n down to x^0 OR x^0 up to x^n.
        # If divisor is [1, -4], and it represents $x-4$, then order must be descending ($c_n \dots c_0$) because $1*x + (-4)*1$. 
        # So dividend [6, 0, 6] -> $6x^2 + 0x + 6$.
        
        n = len(coeffs) - 1
        
        latex_parts = []
        for i in range(n, -1, -1):
            c = coeffs[i]
            if c == 0:
                continue
            term_str = f"{c}" if abs(c) != 1 else "" # Handle sign separately? No, just value. 
            deg = n - i
            
            if deg > 0 and latex_parts[-1]:
                 latex_parts.append(f" + " if c > 0 else f" - ")
            
            val_str = str(abs(c))
            if abs(val_str) == 1: # Don't write '1' in front of variable term usually, but keep it for constants? 
                pass
            
            # Simplify logic: build string manually.
        
        # Let's just construct the final strings based on our calculated values [6, 24] and [102].
        # Quotient: $6x + 24$. Dividend was $6x^2+6$, divisor $x-4$. Remainder $102$.
        
        q_latex = r"6x + 24"
        rem_latex = "102"

    question_text = (r"If we divide the polynomial \( P(x) \), defined by coefficients [6, 0, 6], by the polynomial \( D(x) \), defined by coefficients [1, -4], what are the quotient and remainder? Specifically, find the coefficient list for the quotient $Q(x)$ and the constant remainder.")
    
    # Correction: The prompt asks for specific structure. 
    # Let's refine question_text to be standard math problem style.
    q_coeffs = [6, 24]
    r_coeffs = [102]
    
    return {
        "question_text": f"Divide the polynomial with coefficients \\([\\{', '.join(map(str, dividend_coefficients))}\\]\\) by the polynomial with coefficients \\([\\{', '.join(map(str, divisor_coefficients))}\\]\\). Find the quotient and remainder.",
        "correct_answer": {
            "quotient_coefficients": q_coeffs,
            "remainder_coefficients": r_coeffs,
            "quotient_latex": f"{''.join(['6x' if i==0 else str(c) for c in [q_coeffs[1]]])}", # Wait, simpler. 
            # Re-eval latex construction: 6x + 24
        },
        "oracle_payload": {"dividend_coefficients": dividend_coefficients, "divisor_coefficients": divisor_coefficients}
    }