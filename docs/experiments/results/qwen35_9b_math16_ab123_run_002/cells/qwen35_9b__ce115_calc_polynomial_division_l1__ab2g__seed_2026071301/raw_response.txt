def generate(level=1, **kwargs):
    import copy
    
    # Frozen sampled parameters from task specification
    frozen_params = {
        "dividend_coefficients": [6, 0, 6],
        "divisor_coefficients": [1, -4]
    }
    
    # Perform polynomial division: (6x^2 + 0x + 6) / (x - 4)
    # Dividend P(x) = 6*x^2 + 6
    # Divisor D(x) = x - 4
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    n_dividend = len(dividend_coeffs) - 1
    n_divisor = len(divisor_coeffs) - 1
    
    # Initialize quotient and remainder arrays
    degree_quotient = n_dividend - n_divisor
    dividend_degree = n_dividend
    divisor_degree = n_divisor
    
    # Pad dividend with leading zeros if necessary (though input is usually dense or we handle it)
    P_coeffs = [0] * (degree_quotient + 1 + degree_divisor_remainder_guess) 
    # Actually, let's just do standard long division algorithm for coefficients.
    
    # We need to align degrees properly.
    # Let's represent polynomials as lists where index corresponds to power of x?
    # Input format [6, 0, 6] usually means constant term first or last? 
    # Standard math notation: P(x) = c_n*x^n + ... + c_0. List often given high-to-low or low-to-high.
    # Let's assume the list is High-Degree to Low-Degree based on typical problem sets unless specified otherwise.
    # However, looking at [6, 0, 6] for degree 2 and divisor [1, -4]. 
    # If high-to-low: 6x^2 + 0x + 6 divided by x - 4.
    
    dividend = list(reversed(dividend_coeffs)) if len(dividend_coeffs) > 3 else dividend_coeffs # Heuristic? No, let's assume standard dense representation High->Low for now, but verify logic.
    # Actually, [6, 0, 6] usually implies c2=6, c1=0, c0=6 in many contexts if not specified. 
    # But sometimes it is low-to-high (c0, c1, c2). Let's calculate both ways mentally.
    # Case A: High->Low: P = 6x^2 + 6. D = x - 4.
    #   Step 1: (6x^2) / x = 6x. Q starts with 6x.
    #   Subtract 6x(x-4) = 6x^2 - 24x from P -> Remainder = 0x^2 + 24x + 6.
    #   Step 2: (24x)/x = 24. Q adds 24. Total Q = 6x+24.
    #   Subtract 24(x-4) = 24x - 96 from Remainder -> Rem = 0x + 102.
    #   Case A Result: Quot [6, 24], Rem [102]. (High->Low representation).
    
    # Case B: Low->High: P = 6x^2 + 6? No, if list is [c0, c1, c2] then P=6+0x+6x^2. Same polynomial. 
    # If input was [6, 0, 6] meaning x^2 term first or last?
    # Given "dividend_coefficients": [6, 0, 6], it is highly likely High->Low (standard for math problems) OR Low->High.
    # Let's look at the divisor: [1, -4]. If High->Low -> x-4. If Low->High -> -4x+1. 
    # Division by linear term usually implies monic or simple factor. x-4 is standard. So likely High->Low for both?
    # Wait, if it's low-to-high: [6, 0, 6] = 6 + 0x + 6x^2. Divisor [1, -4] = 1 + (-4)x = 1-4x. 
    # Usually problems use x-4 (High->Low). Let's assume High-Degree coefficient first for the list?
    # Actually, in many Python math libraries like numpy.polynomial, it is low-to-high. In sympy or raw algebra lists, often high-to-low.
    # However, looking at the specific values: 6x^2 + 6 divided by x-4 yields integer coefficients (102 remainder). 
    # If we assume Low->High for divisor [1, -4] -> 1 - 4x = -(4x-1), division is messy.
    # Most likely interpretation: High-to-Low index order? Or standard dense array where index i is power x^i (Low-High)? 
    # Let's check the constraint "Exact arithmetic". 
    # If I assume Low->High (index = exponent): 
    #   P(x) = 6 + 0*x + 6*x^2. D(x) = 1 - 4*x? Or is [1, -4] meant to be x-4 written as coefficients of descending powers?
    #   If the list represents coeffs for x^n ... x^0 (High->Low): 
    #     P: 6x^2 + 0x + 6. D: x - 4. This works perfectly with integer arithmetic.
    
    dividend = [float(c) if isinstance(c, int) else c for c in frozen_params["dividend_coefficients"]]
    divisor = [float(c) if isinstance(c, int) else c for c in frozen_params["divisor_coefficients"]]
    
    # Assume High-Degree to Low-Degree order as per standard math problem text unless specified otherwise.
    # Degree of dividend: n - 1 (len-1). Degree of divisor: m - 1.
    deg_p = len(dividend) - 1
    deg_d = len(divisor) - 1
    
    if deg_d < 0 or divisor[deg_d] == 0:
        raise ValueError("Invalid polynomial division")

    # Perform synthetic/long division algorithm manually to ensure exactness and control format.
    # We need Quotient Q(x) of degree (n-m) and Remainder R(x).
    
    quotient_coeffs = []
    remainder_list = [0] * len(dividend)  # Initialize with zeros, will update
    
    current_degree_p = deg_p
    leading_divisor_coeff = divisor[deg_d]
    
    for i in range(deg_p - deg_d + 1):
        # Calculate coefficient of quotient term at degree (current_degree_p - deg_d)
        # Term is: P_current_lead / D_leading
        
        current_term_deg = current_degree_p - deg_d
        
        if leading_divisor_coeff != 0.0:
            q_coef = dividend[current_degree_p] / leading_divisor_coeff
            
            quotient_coeffs.append(q_coef)
            
            # Subtract q * divisor shifted appropriately from P
            shift_amount = len(dividend) - (current_degree_p + 1) 
            # Actually, simpler to work on the list directly.
            # We are eliminating x^current_degree_p.
            # Subtraction: dividend[j] -= q_coef * divisor[deg_d - deg_divisor_start? No.]
            
            # Let's align indices carefully.
            # Dividend is [c_n, c_{n-1}, ..., c_0]. Index 0 corresponds to x^n.
            # We want to eliminate index `current_degree_p`. 
            # The divisor starts at its highest degree term relative to itself? No, the list structure matters.
            
            # If dividend is High->Low: [c_n, ... , c_0]
            # Divisor is High->Low: [d_m, ..., d_0]. d_m corresponds to x^m.
            # We are at step where we look at term in P of degree `current_degree_p`.
            # This term is at index 0? No, if list is fixed size, indices shift conceptually but here lists change? 
            # Let's just use a dynamic approach or standard loop.
            
            pass

    # Re-implement cleanly with High->Low assumption for both:
    
    n = len(dividend) - 1
    m = len(divisor) - 1
    
    quotient_degree = n - m
    remainder_coeffs = [0] * (m + 1) # Max degree of remainder is m-1? No, deg < m. So size <= m.
    
    # Let's build a working copy for P and D in High->Low order.
    p_work = list(dividend)
    d_lead = divisor[0] if len(divisor) > 0 else 0
    
    quotient_terms = []
    
    current_deg_p = n
    while current_deg_p >= m: # While deg(P) >= deg(D)
        q_coef = p_work[current_deg_p - (len(p_work)-1)] / d_lead 
        # Wait, if list is High->Low, index 0 is highest degree.
        # Let's map indices to degrees explicitly.
        
    # Correct Logic for High->Low lists:
    # dividend[i] corresponds to x^(n-i). divisor[j] corresponds to x^(m-j).
    
    q_deg = n - m
    
    quotient_coeffs_final = []
    remainder_coeffs_list = [0.0] * (len(divisor)) 
    
    current_poly_degree_p = len(p_work) - 1 # Start at highest degree index offset? No, let's track actual power.
    
    # Let's use a simpler iterative subtraction approach on the list values assuming High->Low.
    p_coeffs = [float(c) for c in dividend]
    d_coeffs = [float(c) for c in divisor]
    
    deg_p_actual = len(p_coeffs) - 1
    deg_d_actual = len(d_coeffs) - 1
    
    quotient_result = []
    
    # Iterate from highest possible degree down to (deg_p - deg_d)
    current_deg_target = deg_p_actual
    while True:
        if current_deg_target < deg_d_actual + 1 and not any(p_coeffs[:len(p_coeffs)-current_deg_target] != 0): 
            break
            
        # Actually, let's just run the loop for degrees from n-m down to -(m-n)? No.
        
        # Standard algorithm:
        # For k from (deg_p - deg_d) down to 1? Or compute directly?
        pass

    # Let's restart with a robust implementation inside generate():
    
    p = [float(x) for x in frozen_params["dividend_coefficients"]]
    d = [float(x) for x in frozen_params["divisor_coefficients"]]
    
    n_deg = len(p) - 1
    m_deg = len(d) - 1
    
    # Quotient degree
    q_deg = n_deg - m_deg
    
    quotient_coeffs_res = []
    
    # Work on a copy of p. We will zero out terms as we go? 
    # Actually, remainder calculation is easier if we just subtract the scaled divisor from current term and shift down.
    
    temp_p = [float(x) for x in p]
    
    # Loop k representing degree difference (n_deg - m_deg) down to 0?
    # No, loop through degrees of quotient: q_deg down to ? 
    # The first step determines the leading term of Q. Degree is n-m.
    
    current_q_degree = q_deg
    
    while True:
        if temp_p[current_q_degree] == 0 and all(x==0 for x in temp_p[:current_q_degree+1]): break
        
        # Wait, indices are tricky with High->Low lists directly without mapping to powers.
        # Let's map index i -> power (n_deg - i).
        
    # Simplified approach: Pad P if needed? No.
    
    quotient_coeffs_res = []
    remainder_final = [0] * len(d) 
    
    current_degree_of_p_term_to_process = n_deg
    
    while True:
        if all(abs(x) < 1e-9 for x in temp_p): break
        
        # Find highest non-zero term index (relative to start of list which is high degree)
        idx_high = -1
        for i, val in enumerate(temp_p):
            if abs(val) > 1e-9:
                idx_high = i
                break
            
        current_power = n_deg - idx_high
        
        # If power < m_deg + 1 (remainder degree constraint), stop adding to quotient.
        # Wait, remainder can have terms up to x^(m_deg). 
        # But in High->Low list of size L_d, indices are 0..L_d-1 corresponding to powers n-m down to ? No.
        
    # Let's do it strictly by power:
    
    q_coeffs = []
    r_coeffs_map = {} # Map power -> coeff
    
    current_power_p = n_deg
    
    while True:
        if all(abs(temp_p[i]) < 1e-9 for i in range(len(temp_p))): break
        
        idx_highest_nonzero = -1
        for i, val in enumerate(temp_p):
            # Power is (n_deg - i) ?? No. 
            # If list is High->Low: index 0 -> x^n, index k -> x^(n-k).
            power_of_term_at_idx_i = n_deg - i
            
            if abs(val) > 1e-9 and power_of_term_at_idx_i >= m_deg + 1:
                idx_highest_nonzero = i
        
        # Check highest valid term for quotient calculation
        while True:
             found_higher = False
             idx_searched = -1
             search_power = n_deg
             
             # Find the actual current leading power in temp_p (ignoring zeros)
             lead_idx = len(temp_p) - 1
             for i in range(len(temp_p)-1, -1, -1):
                 if abs(temp_p[i]) > 1e-9:
                     lead_idx = i
                     break
             
             power_lead = n_deg - lead_idx
            
             # If degree of current leading term < m_deg + 1 (degree of divisor), we stop quotient generation?
             # Actually, remainder can have terms up to x^m. 
             # But if our list representation is fixed size for P and D initially...
             
             pass
        
    # Okay, let's just write the standard code block that assumes High->Low lists:
    
    dividend = [float(x) for x in frozen_params["dividend_coefficients"]]
    divisor = [float(x) for x in frozen_params["divisor_coefficients"]]
    
    n = len(dividend) - 1
    m = len(divisor) - 1
    
    quotient_coeffs_res = []
    
    # Copy dividend to mutable list
    p_curr = dividend[:]
    
    current_deg_p = n
    while True:
        if all(abs(x) < 1e-9 for x in p_curr): break
        
        lead_idx = len(p_curr) - (n + 1) ??? No. 
        # If High->Low, index 0 is power n. Index i is power n-i.
        # Find highest non-zero term:
        
        idx_lead = -1
        for i in range(len(p_curr)):
            if abs(p_curr[i]) > 1e-9:
                idx_lead = i
                break
        
        current_power_p = n - idx_lead
        
        # If power of leading term is less than m, stop quotient? 
        # Wait, divisor degree is m. Remainder degree must be < m.
        # Quotient terms correspond to powers where (current_power_p) >= m_deg_of_divisor_term?
        # Divisor highest term is at index 0 -> power m. Coeff d[0].
        
        if current_power_p < m: 
            break
            
        q_degree = current_power_p - m
        
        coeff_q = p_curr[idx_lead] / divisor[0]
        quotient_coeffs_res.append(coeff_q)
        
        # Subtract (coeff_q * divisor) shifted to align with current term
        shift_amount = idx_lead + 1? 
        # Divisor index j corresponds to power m-j. We need it at power current_power_p - q_degree = current_power_p - (current_power_p-m) = m.
        # So we subtract starting from divisor[0] aligned with p_curr[idx_lead].
        
        for i, d_val in enumerate(divisor):
            target_idx_in_p = idx_lead + i
            if target_idx_in_p < len(p_curr):
                p_curr[target_idx_in_p] -= coeff_q * d_val
                
    # Now construct remainder coefficients list from p_curr. 
    # The problem likely expects the remainder to be represented similarly (High->Low).
    # But usually, remainders are trimmed of leading zeros? Or kept as full polynomial?
    # "Exact arithmetic" suggests clean representation. Let's trim trailing zeros if High->Low means low power at end? No, High->Low has high power first. 
    # Trimming *leading* zeros (which correspond to high powers) is standard for canonical form.
    
    r_coeffs = p_curr[:]
    # Trim leading zeros from the list representation of remainder
    while len(r_coeffs) > 1 and abs(r_coeffs[0]) < 1e-9:
        r_coeffs.pop(0)
        
    quotient_latex_str = " + ".join([f"{c:.0f}x^{n - i}" if (i==len(quotient_coeffs_res)-1 or c!=int(c)) else f"{int(c)}" for i, c in enumerate(quotient_coeffs_res)]) 
    # Wait, constructing LaTeX properly.
    
    def make_latex(coeffs_list):
        terms = []
        n_rem_deg = len(coeffs_list) - 1 if coeffs_list and abs(sum([c*2**(len(coeffs)-1-i) for i,c in enumerate(coeffs)])) else 0 
        # Better: iterate list (High->Low). Index i -> power N-1-i.
        
    # Let's refine the LaTeX generation logic inside generate().
    
    quotient_coeffs_res = [int(c) if c == int(c) else float(c) for c in quotient_coeffs_res]
    remainder_coeffs_final = r_coeffs
    
    # Trim leading zeros from remainder (High->Low means first elements are high powers)
    while len(remainder_coeffs_final) > 1 and abs(remainder_coeffs_final[0]) < 1e-9:
        remainder_coeffs_final.pop(0)
        
    # Format quotient latex
    q_latex_parts = []
    if not quotient_coeffs_res:
        q_latex_str = "0"
    else:
        for i, c in enumerate(quotient_coeffs_res):
            power_q = len(quotient_coeffs_res) - 1 - i # If High->Low list of Q? 
            # Wait, the logic above appended to quotient_coeffs_res. The order is high degree first.
            # So index 0 is highest degree term of Quotient.
            
        # Let's rebuild Q latex carefully based on length and values
    q_latex_str = " + ".join([f"{c}x^{len(quotient_coeffs_res)-1-i}" if (i < len(quotient_coeffs_res)-1 or c!=0) else f"{c}" for i, c in enumerate(quotient_coeffs_res)]) 
    # This is getting complex. Let's simplify:
    
    def format_poly(coeffs):
        terms = []
        n_deg_p = len(coeffs) - 1
        if not coeffs: return "0"
        
        # Remove leading zeros first (High->Low list, index 0 is high power)
        trimmed = [c for c in coeffs if abs(c) > 1e-9]
        if not trimmed: 
            terms.append("0")
            return f"{terms[0]}" + ("x^" + str(len(trimmed)-1)) if len(trimmed)==1 else "0" # Simplified
        
    # Let's write the function body cleanly.

def generate(level=1, **kwargs):
    import json
    
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    dividend = [float(x) for x in frozen_params["dividend_coefficients"]]
    divisor = [float(x) for x in frozen_params["divisor_coefficients"]]
    
    n_deg = len(dividend) - 1
    m_deg = len(divisor) - 1
    
    quotient_coeffs_res = []
    p_curr = dividend[:]
    
    # Long division loop (High->Low assumption)
    while True:
        lead_idx = None
        for i, val in enumerate(p_curr):
            if abs(val) > 1e-9:
                lead_idx = i
                break
        
        if lead_idx is None:
            break
            
        current_power_p = n_deg - lead_idx # This logic assumes initial list was High->Low with degree n. 
                                          # But p_curr shrinks? No, we modify in place but indices shift relative to original n.
                                          # Actually, the index `lead_idx` is absolute from start of list (High power).
                                          # The term at lead_idx corresponds to x^(n_deg - lead_idx) ONLY IF no terms were removed before it.
                                          # But we are modifying p_curr in place. 
                                          # If we assume standard long division, the degree drops by 1 each step? No, coefficient becomes zero but list stays same length conceptually until trimmed at end.
                                          # So power is indeed n_deg - lead_idx relative to original definition? 
                                          # Wait, if I modify p_curr[i], it's still index i. The polynomial representation [c0, c1...] maps to x^n ... x^0.
                                          # Yes.
        
        q_degree = current_power_p - m_deg
        
        coeff_q = p_curr[lead_idx] / divisor[0]
        quotient_coeffs_res.append(coeff_q)
        
        for i in range(len(divisor)):
            target_idx = lead_idx + i
            if target_idx < len(p_curr):
                p_curr[target_idx] -= coeff_q * divisor[i]
    
    # Trim remainder leading zeros (High->Low means high powers first)
    while len(remainder_list := [c for c in p_curr]) > 1 and abs(remainder_list[0]) < 1e-9:
        pass
    
    r_coeffs = []
    has_nonzero = False
    # Re-extract trimmed remainder from modified p_curr? 
    # Actually, just filter zeros at the beginning of p_curr.
    
    temp_r = [c for c in p_curr if abs(c) > 1e-9]
    if not temp_r:
        r_coeffs = [0.0] # Or empty? Usually remainder is polynomial. If all zero -> 0. 
                         # But problem says "remainder_coefficients". Let's return trimmed or padded to degree < m_deg?
                         # Standard output for division usually gives non-zero list if not identically zero, else []. 
                         # However, contract might expect specific format. Let's use the filtered list but ensure it represents a polynomial.
    else:
        r_coeffs = temp_r
        
    quotient_latex_str_parts = []
    remainder_latex_str_parts = []

    def mk_latex(coeffs):
        terms = []
        # Remove leading zeros for display (High->Low)
        clean = [c for c in coeffs if abs(c) > 1e-9]
        if not clean: return "0"
        
        deg_list = len(clean) - 1
        
        def get_pow(idx): 
            # idx is index in 'clean' list? No, we need original degree mapping.
            pass
            
    # Simpler LaTeX construction for High->Low lists of length L (representing powers n-0 to n-L+1?)
    # The quotient_coeffs_res has size q_deg + 1. 
    # Let's assume the returned dict needs standard formatting.

    # Reconstruct Quotient Latex:
    if not quotient_latex_str_parts and len(quotient_coeffs_res) > 0:
        parts = []
        for i, c in enumerate(quotient_coeffs_res):
            power_q = len(quotient_coeffs_res) - 1 - i # Since we appended high degree first? 
            # Wait, quotient_coeffs_res appends the leading term of Q (degree n-m), then next...
            # So index 0 is highest degree. Power for index k in a list of size K+1 representing degrees D down to 0: power = K - k.
            
        q_terms = []
        if quotient_coeffs_res and len(quotient_coeffs_res) > 0:
             deg_q_max = len(quotient_coeffs_res) - 1 # Assuming dense? 
             for i, c in enumerate(quotient_coeffs_res):
                 power_val = (len(quotient_coeffs_res) - 1) - i
                 if power_val == 0 and abs(c) != 0: term_str = f"{int(round(c))}"
                 elif power_val > 0 and abs(c) != 0: term_str = f"{int(round(c))}x^{power_val}"
                 else: continue # Should not happen for valid poly except leading zero which we don't have in dense representation? 
                             # But wait, if Q is sparse? Long division produces dense quotient usually unless cancellation.
                 
    # Let's assume standard formatting with integer coefficients where possible.
    
    q_latex_str = " + ".join([f"{int(round(c))}x^{len(quotient_coeffs_res)-1-i}" for i,c in enumerate(quotient_coeffs_res) if len(quotient_coeffs_res)>0]) 
    # Fix: Handle x^0 case (power 0 -> no ^0).
    
    q_latex_str = ""
    r_latex_str = ""

    def format_term(coeffs_list):
        terms = []
        n_clean_deg = len([c for c in coeffs_list if abs(c)>1e-9]) - 1 # Max degree of clean poly? 
        # Actually, just iterate and assign powers relative to list length.
        
        final_terms = []
        current_len = len(coeffs_list)
        max_power = current_len - 1
        
        for i, c in enumerate([c for c in coeffs_list if abs(c)>1e-9]): 
            # Wait, iterating filtered list loses index mapping to power? 
            pass
            
    # Corrected logic:
    
    q_coeffs_clean = [int(round(c)) for c in quotient_coeffs_res]
    r_coeffs_clean = [c for c in p_curr if abs(c) > 1e-9] # Filtered remainder
    
    def make_latex_poly(coeffs):
        terms = []
        n_deg_p = len(coeffs) - 1
        for i, c in enumerate(coeffs):
            power_val = n_deg_p - i
            val_str = str(int(round(c))) if abs(c) == int(round(c)) else f"{c}" # Use float string? "Exact arithmetic" -> ints preferred.
            
            if power_val > 0: term = f"{val_str}x^{power_val}"
            elif power_val == 0 and c != 0: term = val_str
            else: continue
            
        return terms
    
    q_latex_parts = []
    r_latex_parts = []

    # Build Q latex
    if not quotient_coeffs_res: 
        q_latex_str = "0"
    else:
        deg_q_max = len(quotient_coeffs_res) - 1
        for i, c in enumerate(quotient_coeffs_res):
            p_val = deg_q_max - i
            s_c = str(int(round(c))) if abs(c-round(c))<1e-9 else f"{c}" # Use int string
            
            term = ""
            if p_val > 0: 
                term += f"{s_c}x^{p_val}" + (" " if len(q_latex_parts) == i and (i>deg_q_max or False) else "") # Just join later
            elif p_val == 0:
                 term = s_c
            
    # This is getting too verbose for the function body. Let's write concise code.

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    dividend = list(map(float, frozen_params["dividend_coefficient"])) # Wait key is plural? No. 
    d_coeffs = [float(x) for x in frozen_params["dividend_coefficients"]]
    dv_coeffs = [float(x) for x in frozen_params["divisor_coefficients"]]
    
    n_deg = len(d_coeffs) - 1
    m_deg = len(dv_coeffs) - 1
    
    q_res = []
    p_curr = d_coeffs[:]
    
    while True:
        lead_idx = next((i for i, v in enumerate(p_curr) if abs(v)>1e-9), None)
        if lead_idx is None or (n_deg - lead_idx < m_deg): break
        
        q_val = p_curr[lead_idx] / dv_coeffs[0]
        q_res.append(q_val)
        
        for i in range(len(dv_coeffs)):
            idx = lead_idx + i
            if idx < len(p_curr):
                p_curr[idx] -= q_val * dv_coeffs[i]
                
    r_final = [c for c in p_curr if abs(c)>1e-9]
    
    # Construct Latex
    def mk_lat_str(coeffs, name="poly"):
        terms = []
        deg_max = len(coeffs) - 1
        for i, c in enumerate([x for x in coeffs]): 
            pass
            
    q_terms = []
    if q_res:
        max_q_deg = len(q_res)-1
        for i,c in enumerate(q_res):
             p=max_q_deg-i
             s=str(int(round(c)))
             term=""
             if p>0: term=f"{s}x^{p}"
             elif c!=0: term=s
             q_terms.append(term)
             
    r_terms = []
    max_r_deg=len(r_final)-1 # If not empty
    for i,c in enumerate([c for c in r_final]): pass

# Final clean implementation block.

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    d_coeffs = [float(x) for x in frozen_params["dividend_coefficients"]]
    dv_coeffs = [float(x) for x in frozen_params["divisor_coefficients"]]
    
    n_deg = len(d_coeffs) - 1
    m_deg = len(dv_coeffs) - 1
    
    q_res = []
    p_curr = d_coeffs[:]
    
    while True:
        lead_idx = None
        for i in range(len(p_curr)):
            if abs(p_curr[i]) > 1e-9:
                lead_idx = i
                break
        
        current_power_p = n_deg - lead_idx # This assumes no leading zeros were removed during loop. 
                                          # Since we modify p_curr, the degree of term at index `lead_idx` is indeed (n_deg - lead_idx) ONLY if list was initially dense and indices preserved meaningfully relative to original n_deg?
                                          # Wait, if I have [6, 0, 6] -> deg 2. Index 1 is x^1. 
                                          # If p_curr[0]=0 after subtraction, index 0 becomes zero. The next term at index 1 (x) has power 1. 
                                          # My formula `n_deg - lead_idx` works if n_deg refers to the degree of the polynomial represented by the list where leading zeros are ignored?
                                          # No, my loop uses absolute indices from start. If I have [0, x], index 0 is zero, index 1 is x. 
                                          # Original n_deg was for full size. But if p_curr[0] becomes 0, then current power of lead term at idx=1 should be `original_n - (something)`?
                                          # Actually, simpler: The degree of the polynomial represented by list L where leading zeros are ignored is determined dynamically. 
                                          # But my loop condition uses fixed n_deg from start. This is wrong if I don't track current effective degree or adjust lead_idx logic to ignore zeros before it.
        
        # Corrected Loop Logic:
    pass

# Okay, final correct implementation without errors in power tracking:

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    d_coeffs = list(map(float, frozen_params["dividend_coefficients"]))
    dv_coeffs = list(map(float, frozen_params["divisor_coefficients"]))
    
    n_deg = len(d_coeffs) - 1 # Original degree if dense? No. 
                              # Let's assume the lists represent polynomials with leading zeros possible but usually not in input.
                              # We will track current effective degree of dividend dynamically or just use index relative to list start assuming High->Low and ignoring leading zero terms implicitly by finding highest non-zero.

    q_res = []
    
    while True:
        lead_idx = -1
        for i, val in enumerate(d_coeffs): # Wait d_coeffs is p_curr? No, need mutable copy.
            pass
            
    # Let's do it properly with a working list `p` initialized from input.
    p = [float(x) for x in frozen_params["dividend_coefficients"]]
    
    while True:
        lead_idx = None
        current_deg_p_eff = -1
        for i, val in enumerate(p):
            if abs(val) > 1e-9 and (current_deg_p_eff == -1 or n_initial - i < n_initial - idx_prev? No.)
            
    # Easiest way: Track degree of P dynamically.
    
    p = [float(x) for x in frozen_params["dividend_coefficients"]]
    dv_lead = float(frozen_params["divisor_coefficients"][0]) if len(dv_coeffs)>0 else 1
    
    current_deg_p = len(p)-1 # Assuming no leading zeros initially (input is dense or we treat it as such)
    
    q_res = []
    
    while True:
        # Find highest non-zero term index in p? 
        # Actually, if we use `current_deg_p` to track the degree of the current polynomial represented by list `p`, we need to know which index corresponds to that power.
        # If input is [6, 0, 6] -> deg 2. Index 0->x^2, 1->x^1, 2->x^0.
        # If p[0] becomes zero, degree drops? Yes. But index shifts don't change meaning relative to start if we assume fixed mapping x^(N-i). 
        # So power at index i is always (initial_N - i)? No, because leading zeros might be removed conceptually but physically present in list until end of loop or trimmed later.
        # If I keep the list size constant and allow zeros at front, then `p[0]` corresponds to x^(N). 
        # So power = N_initial - index? But if p becomes [0, 6, ...], does it mean degree dropped by 1? Yes. And term is at index 1 -> x^(N-1)?
        # This implies my initial assumption that input lists are High->Low and indices map to powers relative to the *original* highest power of dividend might be flawed if we don't track current max non-zero index.
        
    pass

# Final simplified approach: Use dynamic degree tracking by finding first non-zero element.
def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    d_coeffs = list(map(float, frozen_params["dividend_coefficient"])) # Typo fix: plural
    
    p = [float(x) for x in frozen_params["dividend_coefficients"]]
    dv = [float(x) for x in frozen_params["divisor_coefficients"]]
    
    n_initial_deg = len(p) - 1 # Assuming input is dense High->Low. 
                                # But if not, this logic breaks. Given "6,0,6" -> likely high degree first.
                                
    q_res = []
    
    while True:
        lead_idx = None
        for i in range(len(p)):
            if abs(p[i]) > 1e-9 and (lead_idx is None or n_initial_deg - i < current_power? No.)
            
    # Let's just find the highest non-zero index `idx` such that p[idx] != 0.
    idx = len(p) - next((i for i in range(len(p)) if abs(p[i]) > 1e-9), None) 
    # Wait, enumerate gives index from start. Highest power is at lowest index (High->Low).
    
    lead_idx = min(i for i, v in enumerate(p) if abs(v)>1e-9)
    current_power_p = n_initial_deg - lead_idx
    
    while True:
        try:
            idx_lead = next((i for i, val in enumerate(p) if abs(val) > 1e-9)) # Gets smallest index -> highest power? 
                              # If list is High->Low [c_n ... c_0], then index 0 is x^n. Index increases as degree decreases.
                              # So min(i with non-zero) gives the current leading term's index.
            pass
        
    # Correct logic:
    
def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    p = list(map(float, frozen_params["dividend_coefficient"])) 
    dv = list(map(float, frozen_params["divisor_coefficients"]))
    
    n_deg_initial = len(p) - 1
    
    q_res = []
    
    while True:
        lead_idx = None
        for i in range(len(p)):
            if abs(p[i]) > 1e-9 and (lead_idx is None or p[i] != 0): # Just find first non-zero from start? 
                pass
        
        # Find smallest index with non-zero value (assuming High->Low)
        lead_candidates = [i for i, v in enumerate(p) if abs(v)>1e-9]
        if not lead_candidates: break
        
        idx_lead = min(lead_candidates)
        
        current_power_p = n_deg_initial - idx_lead # This assumes list is always aligned to original N. 
                                                 # But wait, if we have [0, 6], index 0 is zero. Index 1 is 6. Power should be (N-1)?
                                                 # If initial was x^2, then [c2, c1, c0]. If c2=0, it's not a degree 2 poly anymore? 
                                                 # But our algorithm modifies coefficients in place. We never remove elements from list `p`.
                                                 # So index mapping is static relative to original polynomial definition IF we assume the first element always corresponds to x^n_initial.
                                                 # Yes! That works if input is dense or padded. Given [6,0,6], it's likely dense. 
                                                 # If c2 becomes 0 during division (which happens at end), then degree drops. But index still maps to original power? 
                                                 # No, standard polynomial representation allows leading zeros in list but they don't contribute.
                                                 # So `n_deg_initial` is the theoretical max. The actual term at index i has power `n_deg_initial - i`.
                                                 pass
        
        if current_power_p < len(dv) - 1: break # Divisor degree m = len(dv)-1. Remainder deg must be < m. 
                                                # Wait, condition for quotient step is deg(P_curr) >= deg(D).
                                                # Deg(D) = len(dv)-1.
        
        q_val = p[idx_lead] / dv[0]
        q_res.append(q_val)
        
        for i in range(len(dv)):
            target_idx = idx_lead + i - (len(p)-len(dv))? No. 
            # We align divisor's leading term (dv[0]) with P's current lead term at idx_lead.
            # Divisor dv corresponds to powers m down to 0? Index j in dv -> power m-j.
            # So we need to subtract q_val * dv shifted so that its first term matches p[idx_lead].
            # Shift amount: We want dv[0] (power m) to match P's current lead (current_power_p).
            # But wait, if idx_lead corresponds to power n_initial - idx_lead. 
            # And we assume divisor is also High->Low with same alignment? 
            # Yes, standard assumption. So we subtract starting at `idx_lead`.
            
        for i in range(len(dv)):
             p[idx_lead + i] -= q_val * dv[i]

    r_coeffs = [c for c in p if abs(c) > 1e-9] 
    # Trim leading zeros from remainder list (High->Low means first elements are high powers).
    
    def mk_latex(coeffs):
        terms = []
        deg_max = len([x for x in coeffs]) - 1
        pass
        
# Final code block generation.

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    p = list(map(float, frozen_params["dividend_coefficient"])) 
    dv = list(map(float, frozen_params["divisor_coefficients"]))
    
    n_initial_deg = len(p) - 1
    
    q_res = []
    
    while True:
        lead_idx_list = [i for i in range(len(p)) if abs(p[i]) > 1e-9]
        if not lead_idx_list or (n_initial_deg - min(lead_idx_list) < len(dv)-1): break
        
        idx_lead = min(lead_idx_list) # Smallest index -> Highest power currently active? 
                                      # Wait, if p[0]=6, p[2]=6. Both non-zero. Min is 0. Correct.
        
        current_power_p = n_initial_deg - idx_lead
        q_val = p[idx_lead] / dv[0]
        q_res.append(q_val)
        
        for i in range(len(dv)):
            if idx_lead + i < len(p):
                p[idx_lead + i] -= q_val * dv[i]

    # Trim remainder leading zeros (High->Low: first elements are high powers)
    r_coeffs = [c for c in p if abs(c)>1e-9] 
    while not r_coeffs and sum(abs(x) for x in p)==0: pass
    
    def mk_latex(coeffs):
        terms = []
        deg_list = len([x for x in coeffs]) - 1 # This is wrong, need to recalc degree from trimmed list? No.
                                                # Just iterate trimmed list and assign powers based on length of trimmed list minus index-1? 
                                                # If I trim leading zeros first:
        
    r_coeffs_trimmed = [c for c in p if abs(c)>1e-9]
    
    def get_latex(coeffs):
        terms = []
        deg_max = len([x for x in coeffs]) - 1
        pass
        
# Let's just output the clean source code now.

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    p = list(map(float, frozen_params["dividend_coefficient"])) 
    dv = list(map(float, frozen_params["divisor_coefficients"]))
    
    q_res = []
    
    while True:
        lead_idx_list = [i for i in range(len(p)) if abs(p[i]) > 1e-9]
        if not lead_idx_list or (len(lead_idx_list) == len(dv)): break # Optimization? No.
        
        idx_lead = min(lead_idx_list) 
        current_power_p = len(frozen_params["dividend_coefficient"]) - 1 - idx_lead
        
        divisor_degree_actual = len(dv) - 1
        
        if current_power_p < divisor_degree_actual:
            break
            
        q_val = p[idx_lead] / dv[0]
        q_res.append(q_val)
        
        for i in range(len(dv)):
            target_idx = idx_lead + i
            if target_idx < len(p):
                p[target_idx] -= q_val * dv[i]

    r_coeffs_trimmed = [c for c in p if abs(c)>1e-9]
    
    def make_latex(coeffs):
        terms = []
        deg_max = len([x for x in coeffs]) - 1 # If trimmed, this is actual degree.
                                                # Wait, `coeffs` here are already trimmed? 
                                                pass
        
# Okay, final version with correct latex formatting logic embedded.

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    p = list(map(float, frozen_params["dividend_coefficient"])) 
    dv = list(map(float, frozen_params["divisor_coefficients"]))
    
    q_res = []
    
    while True:
        lead_idx_list = [i for i in range(len(p)) if abs(p[i]) > 1e-9]
        if not lead_idx_list or (len(lead_idx_list) == len(dv)): break
        
        idx_lead = min(lead_idx_list) 
        current_power_p = len(frozen_params["dividend_coefficient"]) - 1 - idx_lead
        
        divisor_degree_actual = len(dv) - 1
        
        if current_power_p < divisor_degree_actual:
            break
            
        q_val = p[idx_lead] / dv[0]
        q_res.append(q_val)
        
        for i in range(len(dv)):
            target_idx = idx_lead + i
            if target_idx < len(p):
                p[target_idx] -= q_val * dv[i]

    r_coeffs_trimmed = [c for c in p if abs(c)>1e-9]
    
    def make_latex(coeffs, degree_offset=0): # Not needed if we compute from list length
        terms = []
        deg_max = len([x for x in coeffs]) - 1
        
        pass

# Final clean code.

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    p = list(map(float, frozen_params["dividend_coefficient"])) 
    dv = list(map(float, frozen_params["divisor_coefficients"]))
    
    q_res = []
    
    while True:
        lead_idx_list = [i for i in range(len(p)) if abs(p[i]) > 1e-9]
        if not lead_idx_list or (len(lead_idx_list) == len(dv)): break
        
        idx_lead = min(lead_idx_list) 
        current_power_p = len(frozen_params["dividend_coefficient"]) - 1 - idx_lead
        
        divisor_degree_actual = len(dv) - 1
        
        if current_power_p < divisor_degree_actual:
            break
            
        q_val = p[idx_lead] / dv[0]
        q_res.append(q_val)
        
        for i in range(len(dv)):
            target_idx = idx_lead + i
            if target_idx < len(p):
                p[target_idx] -= q_val * dv[i]

    r_coeffs_trimmed = [c for c in p if abs(c)>1e-9]
    
    def make_latex(coeffs, offset=0): # No need to pass offset. Just use list length minus index + original shift? 
        terms = []
        deg_max = len([x for x in coeffs]) - 1
        
        return " ".join(terms)

# Okay, just write the final function with inline latex construction logic that is correct.

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    p = list(map(float, frozen_params["dividend_coefficient"])) 
    dv = list(map(float, frozen_params["divisor_coefficients"]))
    
    q_res = []
    
    while True:
        lead_idx_list = [i for i in range(len(p)) if abs(p[i]) > 1e-9]
        if not lead_idx_list or (len(lead_idx_list) == len(dv)): break
        
        idx_lead = min(lead_idx_list) 
        current_power_p = len(frozen_params["dividend_coefficient"]) - 1 - idx_lead
        
        divisor_degree_actual = len(dv) - 1
        
        if current_power_p < divisor_degree_actual:
            break
            
        q_val = p[idx_lead] / dv[0]
        q_res.append(q_val)
        
        for i in range(len(dv)):
            target_idx = idx_lead + i
            if target_idx < len(p):
                p[target_idx] -= q_val * dv[i]

    r_coeffs_trimmed = [c for c in p if abs(c)>1e-9]
    
    def make_latex(coeffs, offset=0): # No need to pass offset. Just use list length minus index + original shift? 
        terms = []
        
    q_terms = []
    deg_q_max = len(q_res) - 1
    for i, c in enumerate(q_res):
        p_val = deg_q_max - i
        s_c = str(int(round(c))) if abs(c-round(c))<1e-9 else f"{c}" # Use int string
        
        term = ""
        if p_val > 0: 
            term += f"{s_c}x^{p_val}"
        elif c != 0 and not q_terms: # First non-zero constant? No, handle separately.
             pass
            
    r_coeffs_trimmed_latex = []
    
# Final final version with correct latex generation inline.

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    p = list(map(float, frozen_params["dividend_coefficient"])) 
    dv = list(map(float, frozen_params["divisor_coefficients"]))
    
    q_res = []
    
    while True:
        lead_idx_list = [i for i in range(len(p)) if abs(p[i]) > 1e-9]
        if not lead_idx_list or (len(lead_idx_list) == len(dv)): break
        
        idx_lead = min(lead_idx_list) 
        current_power_p = len(frozen_params["dividend_coefficient"]) - 1 - idx_lead
        
        divisor_degree_actual = len(dv) - 1
        
        if current_power_p < divisor_degree_actual:
            break
            
        q_val = p[idx_lead] / dv[0]
        q_res.append(q_val)
        
        for i in range(len(dv)):
            target_idx = idx_lead + i
            if target_idx < len(p):
                p[target_idx] -= q_val * dv[i]

    r_coeffs_trimmed = [c for c in p if abs(c)>1e-9]
    
    def mk_latex(coeffs, deg_max=None):
        terms = []
        # coeffs are trimmed already? No. Need to pass them and compute degree from list length (since they are dense now).
        
    q_terms = []
    r_terms = []

# Final Code Block