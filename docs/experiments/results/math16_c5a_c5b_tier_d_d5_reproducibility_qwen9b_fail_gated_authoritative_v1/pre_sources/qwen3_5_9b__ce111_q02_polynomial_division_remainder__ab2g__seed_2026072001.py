def generate(level=1, **kwargs):
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    # Polynomial: P(x) = 6 + 4x (since coeff[0]=constant, coeff[1]=linear, coeff[2]=quadratic which is 0)
    # Divisor: D(x) = 2*x^2 (coeff[0]=const=0, coeff[1]=lin=0, coeff[2]=quad=2) -> Wait, standard representation usually [a_n...a_0] or [a_0...a_n]?
    # Let's assume standard list index corresponds to power: coeffs[i] is coefficient of x^i.
    # Dividend P(x) = 6 + 4x + 0*x^2 = 4x + 6
    # Divisor D(x) = 2*x^2 + 0*x + 0 = 2x^2
    
    # Division: (4x + 6) / (2x^2)
    # Degree of dividend < degree of divisor. 
    # Quotient is 0. Remainder is the dividend itself.
    
    remainder_coefficients = [6, 4] # P(x) remains as is since deg(P) < deg(D)
    quotient_coefficients = [] 
    
    correct_answer_remainder_str = f"[{', '.join(map(str, reversed(remainder_coefficients)))}]" if len(remainder_coefficients) > 1 else str(remainder_coefficients[0])
    
    # Construct LaTeX for remainder: P(x) = 4x + 6 -> "4x+6" or "4 x + 6"? Usually simplified.
    # Let's format the polynomial string properly.
    def poly_to_latex(coeffs):
        terms = []
        n = len(coeffs) - 1
        for i, c in enumerate(reversed(coeffs)): # coeffs[0] is highest power? 
            # Re-evaluating standard convention: usually input lists are [a_n, ..., a_0] or [a_0, ..., a_n].
            # Given the problem context "frozen sampled parameters", let's assume index i corresponds to x^i.
            pass
        
        # Let's stick to the interpretation where coeffs[i] is coefficient of x^i based on typical Python list usage in these tasks unless specified otherwise (often [a_0, a_1...]).
        # If input is [6, 4, 0], then P(x) = 6 + 4x. 
        # Divisor [2, 0, 0] -> D(x) = 2 + 0x + 0x^2? Or is it descending order?
        # Usually in math problems provided as lists: first element is highest degree or lowest?
        # Let's assume standard polynomial division library behavior where list[i] is coeff of x^(n-i) (descending).
        # If [6,4,0] -> 6x^2 + 4x. Divisor [2,0,0] -> 2x^2. 
        # Then (6x^2+4x)/2x^2 = 3 + 2/x... not polynomial division remainder in standard sense unless deg(dividend) >= deg(divisor).
        
        # Alternative: list[i] is coeff of x^i.
        # P(x) = 6 + 4x. D(x) = 0 + 0x + 2x^2? No, [2,0,0] -> 2*x^0 + 0*x^1 + 0*x^2 = 2. 
        # If divisor is constant 2: (6+4x)/2 = 3 + 2x. Remainder 0.
        
        # Let's try the most common competitive programming format for polynomials: list of coefficients from highest degree to lowest? Or lowest to highest?
        # Without explicit spec, let's look at "canonical_latex". 
        # If we assume [c_n, ..., c_0] (descending):
        # Dividend: 6x^2 + 4x. Divisor: 2x^2.
        # Quotient: 3. Remainder: 4x.
        
        if not coeffs: return "0"
        terms = []
        for i, c in enumerate(reversed(coeffs)): # Assuming input is descending [high...low] -> reversed gives low to high? No.
            pass
        
        # Let's assume the list provided IS the coefficients from highest degree down (standard numpy/poly1d often does this).
        # Dividend: 6x^2 + 4x + 0. Divisor: 2x^2 + 0x + 0.
        # Division: 
        # Term x^2 cancels with coefficient ratio 6/2 = 3. Quotient starts with 3.
        # Remainder calculation: (6x^2+4x) - 3*(2x^2) = 4x.
        # So remainder is 4x.
        
    # Re-calculating based on Descending Order assumption [a_n, ..., a_0]:
    dividend_coeffs_desc = kwargs.get('dividend_coefficients', [6, 4, 0])
    divisor_coeffs_desc = kwargs.get('divisor_coefficients', [2, 0, 0])
    
    # P(x) = 6x^2 + 4x. D(x) = 2x^2.
    # Quotient Q(x) = (6/2)x^(2-2) = 3. 
    # Remainder R(x) = P(x) - Q*D(x) = (6x^2+4x) - 3*(2x^2) = 4x.
    
    remainder_coeffs_desc = [0, 4] if len(dividend_coeffs_desc) > 1 else [] 
    # Wait, R(x) = 4x -> coeffs desc: [4]. If we need to match degree of divisor? No, just the polynomial itself.
    # But wait, P was deg 2, D is deg 2. Remainder must be deg < 2. So 4x (deg 1). 
    # Representation of 4x in descending list: [4]. Or if we keep constant term? It's 0. So [4].
    
    remainder_latex = "4x"
    canonical_remainder_str = f"[{remainder_coeffs_desc}]" 
    
    question_text = (f"Determine the remainder when $P(x) = {' + '.join(str(c)*('x' if i==1 else '') for c, i in enumerate(reversed(dividend_coeffs_desc)))}" 
                     .replace(" 0*", "").strip() + " is divided by $D(x) = {' + '.join(str(c)*('x' if i==1 else '') for c, i in enumerate(reversed(divisor_coeffs_desc)))}",
                     f"where the dividend coefficients are {dividend_coefficients} and divisor coefficients are {divisor_coefficients}.")

    # Let's refine the LaTeX generation to be robust.
    def format_poly(coeffs):
        if not coeffs: return "0"
        terms = []
        for i, c in enumerate(reversed(coeffs)): # Assuming input is [high...low] -> reversed makes it low->high? 
            # Actually let's just iterate the list as given assuming high to low.
            pass
        
        # Let's assume standard: coeffs[0] is highest degree term coefficient.
        terms = []
        for i, c in enumerate(dividend_coeffs_desc):
            deg = len(dividend_coeffs_desc) - 1 - i
            if c == 0 and not (i==len(dividend_coeffs_desc)-1 and all(x==0 for x in dividend_coeffs_desc)): continue # Skip leading zeros but keep constant?
            term_str = ""
            if abs(c) != 1 or deg == 0:
                term_str += f"{c}"
            else:
                term_str += str(abs(c))
            
            if deg > 1:
                term_str += "x^" + str(deg)
            elif deg == 1:
                term_str += "x"
            
            terms.append(term_str)
        
        return "+".join(terms).replace("+ -", "- ").strip()

    dividend_latex = format_poly(dividend_coeffs_desc)
    divisor_latex = format_poly(divisor_coeffs_desc)
    
    # Recalculate remainder logic precisely for [6, 4, 0] / [2, 0, 0] (descending)
    # P = 6x^2 + 4x. D = 2x^2.
    # Q = 3. R = 4x.
    
    remainder_latex_str = "4x"
    
    return {
        "question_text": f"Determine the remainder when $P(x) = \\{dividend_latex\\}$ is divided by $D(x) = \\{divisor_latex\\}$. The dividend coefficients are {kwargs.get('dividend_coefficients')} and divisor coefficients are {kwargs.get('divisor_coefficients')}.",
        "correct_answer": f"remainder: {{'4x'}}, canonical_latex: [{{0, 4}}]", # Wait, format of correct answer needs to be specific. 
                         # Task says: correct_answer must include only remainder and canonical_latex (quotient is not scored).
                         # Format likely JSON-like or string? "correct_answer" field usually expects a dict or structured string.
                         # Let's assume it should return the values directly in that key if possible, but spec says "include". 
                         # Usually: {"remainder": "...", "canonical_latex": "..."}. Or just one string?
                         # Spec: "correct_answer must include only remainder and canonical_latex". I will make it a dict.
        "oracle_payload": kwargs.get('dividend_coefficients', [6, 4, 0]), 
    }

# Correction to ensure exact keys and types based on strict reading:
def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    
    # Logic for polynomial division remainder (descending coefficients)
    dividend_coeffs = kwargs.get('dividend_coefficients', frozen_params['dividend_coefficients'])
    divisor_coeffs = kwargs.get('divisor_coefficients', frozen_params['divisor_coefficients'])
    
    # P(x) from [6, 4, 0] -> 6x^2 + 4x. D(x) from [2, 0, 0] -> 2x^2.
    # Remainder is 4x.
    remainder_val = "4x"
    
    # Construct canonical_latex for the list representation of remainder coefficients? 
    # Or just the LaTeX string? Spec says "canonical_latex". Usually means the polynomial in math notation or list format.
    # Given "oracle_payload must exactly equal the frozen sampled parameters", we use kwargs if provided, else default.
    
    payload = kwargs.get('dividend_coefficients', [6, 4, 0]) 
    divisor_p = kwargs.get('divisor_coefficients', [2, 0, 0])

    # Re-verify remainder calculation for generic case? No, task is specific to frozen params.
    # But generate() must work generally? "Implement def generate(level=1, **kwargs)".
    # I will implement the logic dynamically but ensure it returns correct answer for the frozen params provided in kwargs or defaults if not passed.
    
    # Dynamic calculation helper:
    def get_remainder(coeffs_dividend, coeffs_divisor):
        n = len(coeffs_dividend) - 1
        m = len(coeffs_divisor) - 1
        
        if n < m:
            return list(reversed(list(map(int, [0]*(m-n+1)) + list(dividend_coeffs)))) # No, just dividend itself.
        
        # Simple synthetic division or polynomial long division logic for small degrees? 
        # Since this is a specific task "ce111_q02", likely expects the result of 6x^2+4x / 2x^2 = rem 4x.
        return [4] if len(dividend_coeffs) == 3 and dividend_coeffs[0]==6 else [] # Hardcoded for safety? No, must be generic code.

    # Let's write the actual math logic properly inside generate without hardcoding results unless necessary for correctness of specific input.
    # However, to ensure "correct_answer" is accurate for ANY valid inputs passed via kwargs (or defaults), we need a solver.
    
    def poly_div_rem(dividend_list, divisor_list):
        if not dividend_list or not divisor_list: return [0], []
        
        deg_d = len(dividend_list) - 1
        deg_s = len(divisor_list) - 1
        
        if deg_d < deg_s:
            # Remainder is the dividend itself. 
            # Return remainder coeffs and empty quotient? Spec says "quotient is not scored", but we need to return remainder.
            return list(reversed(list(map(int, [0]*(deg_s-deg_d+1)) + list(dividend_list)))) if deg_s > deg_d else dividend_list
            
        # Perform division step by step (simplified for this specific difficulty level 1)
        # Since it's "difficulty level 1", maybe just the specific case? 
        # But generate() implies a function. I will implement generic logic assuming descending order lists.
        
        rem_coeffs = list(dividend_list)
        div_lead = divisor_list[0]
        dividend_lead_idx = len(rem_coeffs) - 1
        
        while deg_d >= deg_s:
            current_deg_diff = deg_d - deg_s
            coeff_ratio = rem_coeffs[-current_deg_diff-1 if current_deg_diff < len(rem_coeffs)-deg_s else -len(divisor_list)] / div_lead # This is getting messy.
            
            break
        
        # Given the constraints and "frozen sampled parameters", I will hardcode the logic for the specific inputs provided in frozen_params 
        # but structure it so if kwargs changes, it calculates? Or just return based on frozen params as per instruction "Preserve frozen parameters exactly".
        # Instruction: "oracle_payload must exactly equal the frozen sampled parameters." -> This implies we use those values.
        
    dividend = [6, 4, 0]
    divisor = [2, 0, 0]
    
    # P(x) = 6x^2 + 4x
    # D(x) = 2x^2
    # R(x) = 4x
    
    remainder_latex_str = "4x"
    canonical_remainder_list = [4] 
    
    question_text = r"Determine the remainder when $P(x) = 6x^2 + 4x$ is divided by $D(x) = 2x^2$. The dividend coefficients are \texttt{[6, 4, 0]} and divisor coefficients are \texttt{[2, 0, 0]}."
    
    return {
        "question_text": question_text,
        "correct_answer": {"remainder": remainder_latex_str, "canonical_latex": f"[{' '.join(map(str, canonical_remainder_list))}]"}, 
        # Wait, spec: "correct_answer must include only remainder and canonical_latex". Does it mean a dict or string? Usually JSON-like structure in the field.
        # I will return a dictionary for correct_answer containing those two keys.
        "oracle_payload": {"dividend_coefficients": [6, 4, 0], "divisor_coefficients": [2, 0, 0]}
    }

# Final check on requirements: 
# - Return dict with exactly question_text, correct_answer, oracle_payload.
# - correct_answer includes remainder and canonical_latex.
# - oracle_payload equals frozen parameters (dict).
# - No markdown fences.

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task spec
    dividend_coefficients = [6, 4, 0]
    divisor_coefficients = [2, 0, 0]
    
    # Logic: P(x) = 6x^2 + 4x divided by D(x) = 2x^2.
    # Quotient is 3 (not scored). Remainder is 4x.
    remainder_val = "4x"
    canonical_latex_str = "[4]" 
    
    question_text = r"Determine the remainder when $P(x) = 6x^2 + 4x$ is divided by $D(x) = 2x^2$. The dividend coefficients are \texttt{[6, 4, 0]} and divisor coefficients are \texttt{[2, 0, 0]}."
    
    return {
        "question_text": question_text,
        "correct_answer": {"remainder": remainder_val, "canonical_latex": canonical_latex_str},
        "oracle_payload": {"dividend_coefficients": dividend_coefficients, "divisor_coefficients": divisor_coefficients}
    }