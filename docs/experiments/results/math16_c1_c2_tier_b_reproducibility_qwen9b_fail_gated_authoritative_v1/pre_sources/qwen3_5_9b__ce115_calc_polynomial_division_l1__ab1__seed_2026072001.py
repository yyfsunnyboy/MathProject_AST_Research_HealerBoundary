def generate(level=1, **kwargs):
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Polynomial: P(x) = 6x^2 + 6 (since coeff of x is 0) -> represented as [6, 0, 6] for [c2, c1, c0]? 
    # Standard list representation in such tasks usually maps index i to coefficient of x^(n-i).
    # Let's assume standard convention: dividend_coefficients = [a_n, ..., a_0].
    # Dividend: 6x^2 + 0x + 6. Degree 2.
    # Divisor: 1x - 4. Degree 1.
    
    # Perform polynomial division manually to ensure exact arithmetic.
    dividend = list(dividend_coefficients)
    divisor_lead = divisor_coefficients[0]
    divisor_degree = len(divisor_coefficients) - 1
    
    quotient_coefficients = []
    remainder_coefficients = [0] * (len(dividend)) # Initialize with zeros, will truncate later if needed
    
    current_dividend_deg = len(dividend) - 1
    
    while current_dividend_deg >= divisor_degree:
        deg_diff = current_dividend_deg - divisor_degree
        coeff_val = dividend[current_dividend_deg] // divisor_lead
        
        quotient_coefficients.append(coeff_val)
        
        # Subtract (coeff * x^deg_diff) * divisor from current dividend part
        subtract_term = [0] * len(divisor_coefficients)
        for i in range(len(subtract_term)):
            idx_in_dividend = deg_diff - i + 1 if i == 0 else deg_diff - i # Wait, let's align powers correctly.
            
    # Re-implementing division logic cleanly:
    
    dividend_coeffs = list(dividend_coefficients)
    divisor_lead = int(divisor_coefficients[0])
    divisor_deg = len(divisor_coefficients) - 1
    
    quotient_coeffs_list = []
    current_degree = len(dividend_coeffs) - 1
    
    while current_degree >= divisor_deg:
        if dividend_coeffs[current_degree] == 0:
            # Skip leading zeros in the working polynomial implicitly by checking degree, 
            # but our list includes them. We need to find the highest non-zero index effectively.
            pass
        
        term_coeff = int(dividend_coeffs[current_degree]) // divisor_lead
        quotient_coeffs_list.append(term_coeff)
        
        # Construct the subtraction vector: term_coeff * x^(current_degree - divisor_deg) * (divisor polynomial)
        shift = current_degree - divisor_deg
        sub_vector = [0] * len(dividend_coeffs)
        
        for i, d_val in enumerate(divisor_coefficients):
            power_idx_in_sub = shift + i # Because divisor coeffs are high to low? 
            # Let's stick to the list index convention: index 0 is highest degree.
            # Divisor: [1, -4] -> x^1 term at idx 0, x^0 term at idx 1.
            # We want to subtract (term_coeff * divisor) shifted by 'shift' positions in terms of power reduction?
            # Actually, if we are dividing x^n / x^(n-1), the result is x^1. 
            # The subtraction happens starting from index corresponding to current_degree - shift = 0 relative to quotient term?
            
        # Correct logic for list indices [high degree ... low degree]:
        # Current dividend highest non-zero power corresponds to len(dividend_coeffs) - 1 - (number of leading zeros skipped).
        # However, the input lists are dense. Let's iterate from top down.
        
    # Reset and do it properly:
    
    p = list(dividend_coefficients)
    q_lead = int(divisor_coefficients[0])
    d_deg = len(divisor_coefficients) - 1
    
    quotient_coeffs_list = []
    
    n = len(p)
    m = len(divisor_coefficients)
    
    # We process from highest degree down to divisor_degree
    for i in range(n - m + 1):
        if p[i] == 0:
            continue
            
        term_val = int(p[i]) // q_lead
        
        quotient_coeffs_list.append(term_val)
        
        # Subtract term_val * divisor shifted by i positions (since we are at index i, which corresponds to x^(n-1-i))
        # The subtraction affects indices from i to i + m - 1
        for j in range(m):
            p[i + j] -= term_val * int(divisor_coefficients[j])
            
    # Remaining coefficients form the remainder. 
    # Truncate trailing zeros if any, but usually keep up to degree of divisor-1? Or just non-zero part.
    # Standard representation: remove leading zeros from the list (which are at the start).
    
    while len(p) > 0 and p[0] == 0:
        p.pop(0)
        
    remainder_coefficients = p
    
    quotient_latex = ""
    if not quotient_coeffs_list:
        quotient_latex = "0"
    else:
        # Construct LaTeX for polynomial from coefficients [c_k, ..., c_0] where k is degree.
        terms = []
        current_deg = len(quotient_coeffs_list) - 1
        sign_str = "+" if any(c > 0 for c in quotient_coeffs_list) and not all(c == 0 for c in quotient_coeffs_list[:current_deg]) else "" # Simplified logic
        
        # Better: iterate through coefficients, handle signs manually.
        latex_parts = []
        
        def get_term_latex(coeff):
            if coeff == 0: return None
            sign = "+" if coeff > 0 and len(latex_parts) > 0 else ("-" if coeff < 0 else "") # Handle first term separately? No, build string.
            
    # Let's rebuild the LaTeX construction function inline for clarity
    
    def make_poly_latex(coeffs):
        if not coeffs: return "0"
        parts = []
        sign_prefix = ""
        
        # Determine overall structure to handle signs correctly in a single pass or post-process
        # Simpler approach: iterate and build string with explicit + - handling
        
        latex_str_parts = []
        for i, c in enumerate(coeffs):
            if c == 0: continue
            
            deg = len(coeffs) - 1 - i
            
            sign = "+" if c > 0 else "-"
            
            # Handle first term specially to avoid leading +/- unless it's negative? 
            # Actually standard math notation doesn't have + at start.
            pass
        
        # Re-doing latex construction cleanly:
        
    def construct_latex(coeffs):
        if not coeffs or all(c == 0 for c in coeffs): return "0"
        
        terms = []
        sign_first = True
        
        for i, coeff in enumerate(coeffs):
            deg = len(coeffs) - 1 - i
            
            # Skip leading zeros (handled by caller usually, but here we might have them if not trimmed? 
            # Our remainder trimming handles it. Quotient should be dense or handled similarly).
            
            if coeff == 0: continue
            
            sign_str = "+" if coeff > 0 else "-"
            abs_coeff = abs(coeff)
            
            term_parts = []
            
            if deg == 0:
                term_parts.append(str(abs_coeff))
            elif deg == 1:
                term_parts.append(f"{abs_coeff}x")
            else:
                term_parts.append(f"{abs_coeff}x^{{{deg}}}")
                
            full_term = sign_str + "".join(term_parts) if len(full_term := " ".join(term_parts)) > 0 else "" # Dummy
            
        # Correct loop logic for LaTeX string building
        
    def build_latex(coeffs):
        if not coeffs: return "0"
        
        latex_terms = []
        leading_zeros_removed = True # Assume caller ensures no leading zeros or we handle them. 
        # Our remainder trimming removes leading zeros (index 0). Quotient construction appends to list, might have trailing zeros in logic? No, loop runs exactly degree times.
        
        for i, c in enumerate(coeffs):
            if c == 0: continue
            
            deg = len(coeffs) - 1 - i
            sign = "+" if c > 0 else "-"
            
            term_str = ""
            val = abs(c)
            
            if deg == 0:
                term_str += str(val)
            elif deg == 1:
                term_str += f"{val}x"
            else:
                term_str += f"{val}x^{{{deg}}}"
                
            latex_terms.append(sign + term_str)
            
        return "".join(latex_terms).replace("+ -", "-").replace("-+", "+-") # Fix double signs
        
    quotient_latex = build_latex(quotient_coeffs_list)
    
    remainder_latex = build_latex(remainder_coefficients)
    
    question_text = f"Divide the polynomial $\\left\\\\sum_{i=0}^{2}{dividend\_coefficients[2-i]}x^{{i}}\\\\right$ by $\\left\\\\sum_{j=0}^{1}{divisor\_coefficients[1-j]}x^{{j}}\\\\right$. Find the quotient and remainder."
    # Wait, need to format coefficients into LaTeX properly in question_text.
    
    def fmt_poly(coeffs):
        if not coeffs: return "0"
        parts = []
        for i, c in enumerate(coeffs):
            deg = len(coeffs) - 1 - i
            sign = "+" if c > 0 else "-"
            val = abs(c)
            
            term = ""
            if deg == 0: term += str(val)
            elif deg == 1: term += f"{val}x"
            else: term += f"{val}x^{{{deg}}}"
            
            parts.append(sign + term)
        return "".join(parts).replace("+ -", "-").replace("-+", "+-")

    dividend_latex = fmt_poly(dividend_coefficients)
    divisor_latex = fmt_poly(divisor_coefficients)
    
    question_text = f"Divide the polynomial $\\left({dividend\_latex}\\right)$ by $\\left({divisor\_latex}\\right)$. Find the quotient and remainder."

    return {
        "question_text": question_text,
        "correct_answer": {
            "quotient_coefficients": quotient_coeffs_list,
            "remainder_coefficients": remainder_coefficients,
            "quotient_latex": build_latex(quotient_coeffs_list),
            "remainder_latex": build_latex(remainder_coefficients)
        },
        "oracle_payload": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    }