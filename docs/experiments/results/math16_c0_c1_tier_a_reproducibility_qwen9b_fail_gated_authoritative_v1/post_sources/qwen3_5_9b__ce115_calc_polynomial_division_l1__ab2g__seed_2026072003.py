def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Polynomial: P(x) = 6x^2 + 0x + 6 (coeffs from highest to lowest degree implied by context of division usually, but list format often high-to-low or low-to-high. 
    # Standard math notation for "dividend_coefficients": [6, 0, 6] with divisor [1, -4].
    # If we assume standard polynomial representation where index i corresponds to x^(n-i) (high degree first):
    # Dividend: 6x^2 + 0x + 6. Degree 2.
    # Divisor: 1x^1 - 4. Degree 1.
    
    dividend_degree = len(dividend_coefficients) - 1
    divisor_degree = len(divisor_coefficients) - 1
    
    quotient_degree = dividend_degree - divisor_degree
    remainder_max_degree = min(quotient_degree, divisor_degree - 1) if quotient_degree >= 0 else -1
    
    # Initialize arrays for division (long division simulation)
    current_dividend_coeffs = list(dividend_coefficients)
    
    # We will perform synthetic/long division manually to ensure exact integer arithmetic.
    # Divisor: x - 4. Root is 4.
    # Synthetic division by root r=4 on [6, 0, 6]:
    # Bring down 6.
    # Multiply 6 * 4 = 24. Add to next coeff (0) -> 24.
    # Multiply 24 * 4 = 96. Add to next coeff (6) -> 102.
    
    r = divisor_coefficients[1] / divisor_coefficients[0] if len(divisor_coefficients) > 1 else 0
    
    quotient_coeffs = []
    remainder_coeffs = [current_dividend_coeffs[-1]] # Last element is initial remainder candidate before processing? No, synthetic division logic:
    
    working_list = list(current_dividend_coeffs)
    
    for i in range(len(working_list) - 1):
        val = working_list[i]
        quotient_val = val / divisor_coefficients[0] # Assuming monic or handling leading coeff
        
        if len(divisor_coefficients) == 2:
            div_lead = divisor_coefficients[0]
            const_term = divisor_coefficients[1]
            
            current_quotient_term = working_list[i] // div_lead
            
            quotient_coeffs.append(current_quotient_term)
            
            # Calculate next term for remainder accumulation logic in synthetic division style
            product = current_quotient_term * const_term
            new_val = working_list[i+1] + product
            working_list[i+1] = new_val
    
    final_remainder = working_list[-1] if len(working_list) > 0 else 0
    
    # Re-construct quotient coefficients properly based on the synthetic division result above.
    # The loop logic simplified:
    # Dividend: [6, 0, 6]. Divisor: x - 4.
    # Step 1: Bring down 6. Quotient term for x^1 is 6. Remainder accumulator = 0 + (6 * -(-4)) ? No.
    # Synthetic division by root r=4 on [6, 0, 6]:
    # Row 1: 6
    # Multiply 6*4 = 24. Add to next: 0+24=24. (This is quotient coeff for x^0? No, this is the intermediate sum).
    # Actually, standard synthetic division output list [q_n-k ... q_0 | r].
    
    correct_quotient_coeffs = []
    current_val = dividend_coefficients[0]
    leading_divisor = divisor_coefficients[0]
    
    for i in range(len(dividend_coefficients) - 1): # Iterate up to second to last element of dividend
        quotient_term = current_val // leading_divisor
        correct_quotient_coeffs.append(quotient_term)
        
        next_index = i + 1
        if next_index < len(dividend_coefficients):
            divisor_const = divisor_coefficients[1] # Assuming linear divisor x - c, coeff is [1, -c]. Here [-4]. So constant term in polynomial is -4.
            # Divisor poly: 1*x + (-4). Root r=4.
            # Synthetic step: next_val = dividend[next_index] + (quotient_term * root)
            
            if len(dividend_coefficients) > i + 2 or divisor_degree == 0: 
                pass
            
    # Let's restart the calculation cleanly for [6, 0, 6] / [1, -4].
    # Divisor is x - 4. Root r = 4.
    # Coeffs to process: 6, 0, 6.
    
    coeffs = dividend_coefficients[:]
    root = divisor_coefficients[1] // divisor_coefficients[0] if len(divisor_coefficients) > 1 else 0
    
    q_coeffs_list = []
    rem_val = 0
    
    for i in range(len(coeffs)):
        val = coeffs[i] + (rem_val * root) # Wait, standard synthetic: bring down first. Then multiply by root and add to next.
        
        if i == 0:
            q_coeffs_list.append(val // divisor_coefficients[0])
            rem_val = 0 # Reset for accumulation logic? No.
            
    # Correct Synthetic Division Algorithm Trace:
    # Input: [6, 0, 6], Root=4
    # 1. Bring down 6. (Quotient coeff x^1) -> q_1 = 6.
    # 2. Multiply 6 * 4 = 24. Add to next (0). Sum = 24. This is the new value for next step, which becomes quotient term? 
    # No, in synthetic division, the numbers generated below the line are the coefficients of the quotient and the remainder at the end.
    
    trace = [dividend_coefficients[0]]
    current_sum = dividend_coefficients[0]
    
    for i in range(1, len(dividend_coefficients)):
        # Multiply previous result by root
        product = current_sum * (root) 
        # Add to next coefficient? No. The standard algorithm:
        # Write down first coeff.
        # For each subsequent coeff c_i: new_val = c_i + (prev_result * r).
        
    # Let's do it simply with polynomial arithmetic logic since numbers are small integers.
    
    dividend_poly_degree = len(dividend_coefficients) - 1
    divisor_poly_degree = len(divisor_coefficients) - 1
    
    quotient_coeffs_list = []
    remainder_val = 0
    
    if divisor_lead := divisor_coefficients[0]:
        for i in range(len(dividend_coefficients)):
            current_term = dividend_coefficients[i] + (remainder_val * root) # This logic is flawed. 
            
    # Re-implementing strictly:
    # Divisor D(x) = d_1 x^k + ... + d_k
    # Here k=1, coeffs=[1, -4]. So 1*x - 4. Root r = 4/1 = 4.
    
    root_val = divisor_coefficients[1] / divisor_coefficients[0] if len(divisor_coefficients) > 1 else 0
    
    # Synthetic division trace list starts with first dividend coeff
    synthetic_trace = [dividend_coefficients[0]]
    
    for i in range(1, len(dividend_coefficients)):
        next_val = dividend_coefficients[i] + (synthetic_trace[-1] * root_val)
        synthetic_trace.append(next_val)
        
    # The quotient coefficients are the first N-1 elements of synthetic trace divided by leading divisor coeff? 
    # Actually, if we divide monic polynomial, they are exactly those values.
    # If not monic, we must adjust. Here divisor lead is 1. So exact integers.
    
    q_coeffs = [int(x) for x in synthetic_trace[:-1]]
    r_coeff = int(synthetic_trace[-1])
    
    # Format remainder coefficients: if degree > 0? Remainder here is a constant (degree 0). 
    # If remainder was higher, we'd have multiple coeffs. Here it's just [r].
    
    quotient_latex_str = ""
    for i, c in enumerate(q_coeffs):
        deg = len(q_coeffs) - 1 - i
        if c != 0:
            term = f"{c}" + "x^" + str(deg) if deg > 1 else ("x" if deg == 1 else "")
            quotient_latex_str += (term + " + ") if quotient_latex_str else term
            
    remainder_latex_str = ""
    r_deg = len([r_coeff]) - 1 # Always 0 for constant unless list is empty? 
    # Remainder is a single value. If it's non-zero, degree 0.
    
    final_rem_val = q_coeffs[-1] if not synthetic_trace else synthetic_trace[-1] # Wait, trace includes remainder at end.
    # My loop logic: synthetic_trace[0]=6 (q term), synthetic_trace[1]=24 (q term), synthetic_trace[2]=102 (remainder).
    
    q_coeffs = [int(x) for x in synthetic_trace[:-1]]
    r_val = int(synthetic_trace[-1])
    
    # Construct LaTeX strings carefully.
    def make_poly_latex(coeffs, name=""):
        if not coeffs: return "0"
        terms = []
        for i, c in enumerate(coeffs):
            deg = len(coeffs) - 1 - i
            sign = "+" if (i > 0 and c >= 0) or (name == "" and i==len(coeffs)-1) else "-" # Simplified logic needed.
            
    # Better LaTeX construction:
    q_latex_parts = []
    for idx, val in enumerate(q_coeffs):
        deg = len(q_coeffs) - 1 - idx
        if val != 0:
            s_val = str(val).replace("-", "\-") 
            term_str = f"{s_val}"
            if deg > 1:
                term_str += "x^{" + str(deg) + "}"
            elif deg == 1:
                term_str += "x"
            
            # Determine sign for placement in sum
            is_first = (idx == 0)
            prev_val = q_coeffs[idx-1] if idx > 0 else None
            
    # Let's just build the string directly.
    quotient_latex_parts = []
    remainder_latex_parts = []

    # Quotient: [6, 24]. Poly: 6x + 24.
    for i in range(len(q_coeffs)):
        c = q_coeffs[i]
        deg = len(q_coeffs) - 1 - i
        if c != 0:
            term = f"{c}"
            if deg > 1:
                term += "x^{" + str(deg) + "}"
            elif deg == 1:
                term += "x"
            
            # Handle sign for joining
            quotient_latex_parts.append(term)

    remainder_val_str = f"{r_val}"
    
    if len(quotient_latex_parts) > 0:
        quotient_latex = "+".join([p.replace("-", "\-") + (" " * (1 if i>0 else 0)) for i,p in enumerate(quotient_latex_parts)]) # Rough join. 
        # Proper joining with signs is tricky without full parser, but standard math format usually implies implicit addition/subtraction based on sign of number.
        
    # Refined LaTeX builder:
    def build_poly_str(coeffs):
        if not coeffs or all(c == 0 for c in coeffs): return "0"
        parts = []
        for i, coeff in enumerate(coeffs):
            deg = len(coeffs) - 1 - i
            val_str = str(coeff).replace("-", "\-") # Escape minus? No, just string. 
            term = f"{val_str}" if coeff != 0 else ""
            
            if deg > 1:
                term += "x^{" + str(deg) + "}"
            elif deg == 1:
                term += "x"
                
            parts.append(term)
        
        # Join with signs. The sign is part of the number string usually, but for first term we don't want leading plus if positive? 
        # Standard LaTeX polynomial often omits + between terms and relies on negative numbers having minus.
        return "+".join(parts).replace("+ -", "- ").replace("+-", "+-") # Cleanup
        
    quotient_latex = build_poly_str(q_coeffs)
    
    remainder_latex = f"{r_val}" if r_val != 0 else "0"

    question_text = (f"Determine the quotient and remainder when dividing the polynomial $P(x)$ by $D(x)$.\n\n"
                     fr"P(x): \({build_poly_str(dividend_coefficients)}\) \(\text{divided by}\) \(x - {abs(int(-divisor_coefficients[1]))} = x + {-int(divisor_coefficients[1])}\)\n\n"
                     f"D(Divisor coefficients provided: {[d for d in divisor_coefficients]})\n\n")

    # Wait, the prompt says "question_text must use formal LaTeX delimiters \( \) / \[". 
    # And oracle_payload must exactly equal frozen sampled parameters.
    
    return {
        "question_text": f"Determine the quotient and remainder when dividing $P(x)$ by $D(x)$.\n\n" + r"P(x): \\(" + build_poly_str(dividend_coefficients) + "\\)" + "\nDivisor: x - 4", 
        # Actually, let's make it cleaner.
        "question_text": f"Determine the quotient and remainder when dividing \({build_poly_str(dividend_coefficients)}\) by \(x - {-divisor_coefficients[1]}\).\n\nFind $Q(x)$ such that $\text{Dividend} = D(x) \\cdot Q(x) + R(x)$.",
        "correct_answer": {
            "quotient_coefficients": q_coeffs,
            "remainder_coefficients": [r_val],
            "quotient_latex": quotient_latex if len(q_coeffs)>0 else "0",
            "remainder_latex": f"{r_val}" if r_val != 0 else "0"
        },
        "oracle_payload": {"dividend_coefficients": dividend_coefficients, "divisor_coefficients": divisor_coefficients}
    }