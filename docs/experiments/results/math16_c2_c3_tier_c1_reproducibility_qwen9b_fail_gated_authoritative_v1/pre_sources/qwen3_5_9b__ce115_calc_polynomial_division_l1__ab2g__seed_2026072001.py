def generate(level=1, **kwargs):
    import copy
    
    # Frozen sampled parameters from task specification
    frozen_params = {
        "dividend_coefficients": [6, 0, 6],
        "divisor_coefficients": [1, -4]
    }
    
    # Perform polynomial division: (6x^2 + 0x + 6) / (x - 4)
    # Dividend: P(x) = 6x^2 + 6
    # Divisor: D(x) = x - 4
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    n_dividend = len(dividend_coeffs) - 1
    n_divisor = len(divisor_coeffs) - 1
    
    # Initialize quotient and remainder coefficients arrays
    deg_quotient = n_dividend - n_divisor
    quotient_coeffs = [0] * (deg_quotient + 1)
    
    # Synthetic division / Long division logic for exact arithmetic
    current_remainder_coefficients = list(dividend_coeffs)
    
    leading_divisor_term = divisor_coeffs[0]  # Should be non-zero
    
    if n_dividend < n_divisor:
        quotient_coeffs = [0]
        remainder_coeffs = list(current_remainder_coefficients)
    else:
        for i in range(deg_quotient + 1):
            current_degree = deg_quotient - i
            
            # Calculate term to subtract from dividend/remainder
            if leading_divisor_term != 0:
                quotient_val = int(float(current_remainder_coefficients[current_degree]) / float(leading_divisor_term))
                
                # Ensure exact integer arithmetic by scaling if necessary, 
                # but here inputs are integers and divisor is monic (or simple), so direct division works.
                # However, to be safe with "Exact arithmetic; no floats", we assume the problem guarantees divisibility or rational results that map back cleanly?
                # The prompt says "Exact arithmetic". Let's implement integer-based logic assuming standard polynomial division where coefficients might become fractions if not monic divisor.
                # But looking at inputs: [6, 0, 6] / [1, -4]. Divisor is x-4 (monic). Division will yield integers or simple rationals? 
                # Let's trace: 
                # Step 1: 6x^2 / x = 6x. Quotient term index 0 gets 6.
                # Multiply divisor by 6x -> [6, -24]. Subtract from dividend [6, 0, 6] -> [0, 24, 6].
                # Step 2: Bring down next terms effectively. Current remainder poly is 24x + 6.
                # Divide 24x by x = 24. Quotient term index 1 gets 24.
                # Multiply divisor by 24 -> [24, -96]. Subtract from [0, 24, 6] (aligned) -> 
                # Actually alignment: Remainder is degree 1 now? No, we process highest degree first.
                
                # Let's do it strictly with integer arithmetic since divisor leading coeff is 1.
                quotient_coeffs[i] = current_remainder_coefficients[current_degree] // leading_divisor_term
                
                # Create the product of (quotient_term * x^i) and divisor to subtract
                shift_amount = n_divisor - i + deg_quotient - current_degree 
                # Actually simpler: The term we just found is for degree 'current_degree' in quotient.
                # We need to multiply this scalar by the whole divisor polynomial shifted appropriately.
                
                product_coeffs = [0] * (n_dividend) # Max size needed
                prod_val = quotient_coeffs[i]
                
                # Fill product coeffs starting at appropriate index
                start_idx = n_divisor - i + deg_quotient  # Wait, let's re-index carefully
                
                # Easier approach: Standard long division array manipulation
                pass
        
        # Re-implementing cleanly with integer arithmetic for monic divisor case (leading coeff 1)
        remainder_coeffs = list(dividend_coeffs)
        
        current_deg_divisor = n_divisor
        quotient_degree = deg_quotient
        
        for q_idx in range(quotient_degree + 1):
            # We are determining the coefficient for x^(current_target_power - q_offset)? 
            # Let's just iterate from highest degree down to lowest possible remainder.
            
            target_deg = n_dividend - (n_divisor - current_remainder_len_adjustment) 
            
        # Correct Algorithm:
        # Current working polynomial is in `remainder_coeffs` of length L+1 representing deg L.
        # We want to eliminate the highest term if degree >= divisor_degree.
        
        work_poly = list(dividend_coeffs)
        rem_deg = len(work_poly) - 1
        
        quotient_list = []
        
        while len(work_poly) > n_divisor:
            current_lead_idx = len(work_poly) - 1 # Highest index in current remainder poly
            
            if current_lead_idx < n_divisor + (len(quotient_list)): 
                break
                
            term_val = work_poly[current_lead_idx] // divisor_coeffs[0]
            
            quotient_list.append(term_val)
            
            # Subtract term_val * x^(current_lead_idx - n_divisor) from the polynomial?
            # No, we subtract (term_val * Divisor(x)) shifted to align with current_lead_idx.
            shift = current_lead_idx - n_divisor
            
            for k in range(len(divisor_coeffs)):
                work_poly[current_lead_idx - k] -= term_val * divisor_coeffs[k]
            
            # Remove leading zeros if any (though integer division by monic usually keeps it clean until end)
            while len(work_poly) > 0 and work_poly[-1] == 0:
                work_poly.pop()
        
        remainder_coeffs = work_poly
        
    else:
         quotient_list = [0] * (deg_quotient + 1) # Should not happen given logic above but safe fallback

    if len(quotient_list) > deg_quotient + 1 and sum(quotient_list[:-1]) == 0:
        # Trim leading zeros in quotient? Usually polynomial division keeps degree. 
        # But standard representation drops leading zero coefficients unless it's the constant term of a non-zero poly.
        pass

    final_quotient_coeffs = [c for c in quotient_list]
    
    # Handle case where result is 0 or empty list from trimming logic above if needed, but loop handles it naturally.
    # If work_poly became empty (exact division), remainder should be [] or [0]? 
    # Convention: Remainder coefficients usually include the constant term even if zero? Or just non-zero terms?
    # Standard math notation P(x) = Q(x)D(x) + R(x). If R=0, coeffs=[].
    
    final_remainder_coeffs = work_poly
    
    # Construct LaTeX strings
    def format_latex(coeffs):
        if not coeffs:
            return "0"
        
        terms = []
        for i, c in enumerate(reversed(coeffs)):
            power = len(coeffs) - 1 - i
            
            sign_str = ""
            abs_c = int(c) # Ensure integer representation
            
            if abs_c == 1 and power > 0:
                coeff_part = "x" + ("^{"+str(power)+"}" if power != 1 else "")
            elif c < 0:
                terms.append("-") 
                sign_str = "-"
            
            # Re-eval logic for clean LaTeX generation
            
        # Simpler generator
        latex_parts = []
        
        def get_term(c, p):
            s = ""
            if abs(c) == 1 and c > 0:
                 coef_s = ""
            elif abs(c) != 1 or c < 0:
                sign = "-" if c < 0 else "+"
                val_str = str(abs(c)) + "x" if p==1 else (str(abs(c))+"x^{"+str(p)+"}" if p!=1 else "") # Wait, x is variable. 
                
            # Let's restart the latex builder properly
            
        terms = []
        
        for i in range(len(coeffs)):
            c = coeffs[i]
            power = len(coeffs) - 1 - i
            
            term_str = ""
            
            if abs(c) == 0:
                continue
                
            sign = "-" if (i > 0 and c < 0) else ("+" if (i > 0 and c > 0) else "")
            
            coef_part = str(abs(c)) if abs(c) != 1 or power == 0 else ""
            
            var_part = "x" + ("^{"+str(power)+"}" if power != 1 else "")
            
            term_str = sign + coef_part + var_part
            
            terms.append(term_str)
        
        return "".join(terms).replace("+-", "-").replace("-+", "+") or "0"

    quotient_latex = format_latex(final_quotient_coeffs) if final_quotient_coeffs else "0"
    
    # Re-do latex generation carefully to ensure signs are correct and no spaces issues for strict matching usually expected.
    def build_poly_str(coeffs):
        if not coeffs: return "0"
        
        parts = []
        leading_sign = True
        
        for i, c in enumerate(reversed(coeffs)): # Iterate from highest power down? No, list is [high to low] or [low to high]? 
            # Input format usually [c_n, ..., c_0]. My logic above assumed that.
            pass
            
    # Let's assume standard input: coeffs[0] is highest degree term.
    
    def make_latex(coeffs):
        if not coeffs: return "0"
        
        res = ""
        for i in range(len(coeffs)):
            c = coeffs[i]
            deg = len(coeffs) - 1 - i
            
            # Determine sign and coefficient string
            is_negative = (c < 0)
            
            term_sign = "-" if (i > 0 and is_negative) else ("+" if (i > 0 and not is_negative) else "")
            
            abs_c = int(c)
            
            coef_str = ""
            x_part = "x" + ("^{"+str(deg)+"}" if deg != 1 else "") # Wait, if deg=0? 
            if deg == 0:
                x_part = ""
                
            if is_negative and i==0: term_sign = "-"
            
            final_coef_str = str(abs_c) if abs_c != 1 or (deg > 0 and deg!=1) else "" # If coeff is 1, omit. 
            # Exception: constant term with coefficient 1 -> "1" not omitted usually? Or just number.
            # Standard polynomial form: -x^2 + x + 5
            
            if abs_c == 1 and deg > 0:
                coef_str = ""
            else:
                coef_str = str(abs_c)
            
            term = f"{term_sign}{coef_str}{'x'*(deg!=0)}" # Simplified logic for single x. 
            # Better explicit construction
            
    # Robust LaTeX builder
    def latex_poly(coeffs):
        if not coeffs: return "0"
        
        terms = []
        first_term = True
        
        for i, c in enumerate(reversed(coeffs)): # Wait, my list was [high..low]. Let's stick to that.
            pass
            
        # Re-verify input order assumption from example: [6, 0, 6] -> 6x^2 + 0x + 6. Yes, high to low.
        
        terms = []
        for i in range(len(coeffs)):
            c = coeffs[i]
            deg = len(coeffs) - 1 - i
            
            if c == 0: continue
            
            sign = "-" if (i > 0 and c < 0) else ("+" if (i > 0 and c > 0) else "")
            
            abs_c = int(c)
            
            # Coefficient part
            coef_part = ""
            if deg == 0:
                coef_part = str(abs_c)
            elif abs_c != 1 or deg == 0: 
                 coef_part = str(abs_c)
            else:
                 coef_part = ""
                 
            x_part = "x" + ("^{"+str(deg)+"}" if deg > 1 else "") # If deg=1, just x. If deg=0 handled above.
            
            term_str = sign + coef_part + x_part
            
            terms.append(term_str)
        
        return "".join(terms).replace("+-", "-").replace("-+", "+") or "0"

    quotient_latex = latex_poly(final_quotient_coeffs) if final_quotient_coeffs else "0"
    
    # Fix remainder LaTeX logic similarly. 
    # If exact division, remainder is 0? Or empty list representing zero polynomial?
    # Usually represented as "0".
    
    rem_str = ""
    if len(final_remainder_coeffs) > 0:
        rem_latex_val = latex_poly(final_remainder_coeffs)
        # Check for leading zeros in remainder that might have been introduced by logic (unlikely with integer div monic)
        while len(rem_latex_val) == 1 and rem_latex_val[0] != 'x' or ('+' not in rem_latex_val): 
             pass
        
    else:
         # If work_poly was empty, it means exact division. Remainder is 0.
         rem_str = "0"

    if len(final_remainder_coeffs) > 1 and final_remainder_coeffs[0] == 0:
        # Trim leading zeros for remainder representation? 
        pass
        
    return {
        "question_text": f"Determine the quotient and remainder when dividing $\\left( \\sum_{i=0}^{2} a_i x^i \\right)$ by $\\left( \\sum_{j=0}^{1} b_j x^j \\right)$. Specifically, divide \({{6}}x^{{2}} + {{0}}x + {{{6}}}\\) by \( {1}x - 4 \).",
        "correct_answer": {
            "quotient_coefficients": final_quotient_coeffs if len(final_quotient_coeffs)>0 else [0], # Ensure non-empty list for consistency? Or allow empty? 
            "remainder_coefficients": final_remainder_coeffs,
            "quotient_latex": quotient_latex,
            "remainder_latex": latex_poly(final_remainder_coeffs) if final_remainder_coeffs and len(final_remainder_coeffs)>1 else ("0" if not final_remainder_coeffs or all(c==0 for c in final_remainder_coeffs) else "") # Simplified check
        }, 
        "oracle_payload": frozen_params
    }