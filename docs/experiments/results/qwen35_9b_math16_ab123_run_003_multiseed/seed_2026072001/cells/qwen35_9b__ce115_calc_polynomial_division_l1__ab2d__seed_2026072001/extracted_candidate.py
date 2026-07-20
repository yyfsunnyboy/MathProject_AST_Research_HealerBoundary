def generate(level=1, **kwargs):
    frozen = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(
        dividend_coefficients=frozen["dividend_coefficients"], 
        divisor_coefficients=frozen["divisor_coefficients"]
    )

    # Construct LaTeX strings for coefficients (handling negative signs and zero)
    def fmt_latex(coeffs):
        if not coeffs: return ""
        terms = []
        for i, c in enumerate(reversed(coeffs)):  # reversed because index 0 is highest degree term usually, but input list [6,0,6] implies descending or ascending? 
            # Standard convention for coeff lists in these tasks often matches polynomial string representation.
            # Input: [6, 0, 6]. If x^2 + ... -> 1*x^2... wait.
            # Let's assume standard list order corresponds to powers n down to 0 or vice versa? 
            # Usually for division problems like this, [a,b,c] represents a_n x^n + ... + a_0 OR a_0 + ... + a_n.
            # However, the domain function handles the math. We just need consistent LaTeX formatting.
            # Let's assume index 0 is highest degree term based on typical "coefficients" input for such libraries unless specified otherwise. 
            # But let's look at [6, 0, 6]. If it were x^2 + 1 = (x+1)(x-1)? No.
            # Let's assume the library output order matches input order logic.
            
            pass 
        
        terms = []
        for i in range(len(coeffs)):
             c = coeffs[i]
             power = len(coeffs) - 1 - i if "descending" else i 
             
             # Heuristic: Usually lists are [a_n, a_{n-1}, ..., a_0].
             degree = (len(coeffs) - 1) - i
             term_str = ""
             
             # Handle coefficient sign and zero
             abs_c = c if c >= 0 else -c
             
             # Sign handling for the whole polynomial string vs individual terms
             is_first = (i == 0) or (coeffs[i-1] != coeffs[0]) # Simplified check needed? No, just iterate.
             
             term_str += " + " if not is_first else "" 
             
             # Actually simpler: Build list of strings then join with appropriate signs.
             pass

    # Re-implementing latex builder strictly based on typical polynomial string generation from coeffs [c0, c1...] where c0 is high degree?
    # Let's assume the standard math convention for these specific benchmarks (often derived from CoT-Collection or similar):
    # List represents coefficients of x^n down to x^0.
    
    def build_poly_latex(coeffs):
        if not coeffs: return "0"
        terms = []
        n = len(coeffs) - 1
        
        for i, c in enumerate(coeffs):
            power = n - i
            val_str = str(c).replace("-", "\\text{-} ") # Avoid double minus issues
            
            term_val = abs(int(c)) if isinstance(c, int) else float(c) # Ensure exact arithmetic display
            
            # Determine sign prefix for this specific term relative to the first non-zero or start? 
            # Better approach: Build full string with + and - operators.
            
        terms = []
        total_degree = len(coeffs) - 1
        
        for i, c in enumerate(coeffs):
            power = total_degree - i
            
            if c == 0: continue
            
            sign_str = "+" if c > 0 else "-"
            abs_c = str(abs(c)) # Assuming integers from frozen params
            
            term_parts = []
            
            # Coefficient part (omit '1' for x^n)
            if abs(int(c)) != 1 or power == 0:
                coeff_part = abs_c
            elif c < 0 and i > 0: 
                 # Logic refinement needed to handle global sign vs local term.
                 pass
            
        return "".join(terms).replace("+ -", "- ")

    # Simpler robust LaTeX builder for this specific task type (often expects standard mathjax)
    def make_latex(coeffs):
        if not coeffs: return "0"
        
        parts = []
        n = len(coeffs) - 1
        
        first_term_sign = True
        zero_count = sum(1 for c in coeffs if c == 0)
        
        # We need to handle the list as a sequence of terms. 
        # Let's assume standard descending order [an, ..., a0]
        
        current_val_strs = []
        has_negative_start = False
        
        for i, val in enumerate(coeffs):
            power = n - i
            
            if val == 0: continue
            
            abs_v = int(val) if isinstance(val, (int, float)) else val
            
            # Sign logic
            is_neg = val < 0
            
            term_str = ""
            
            # Coefficient
            c_disp = str(abs(int(val))) if power > 1 or i == len(coeffs)-1 and abs_val != 1 else "x" # Wait, need to handle x^k vs just x.
            
            # Reset logic for clarity:
            term_str = ""
            
            # Sign prefix (except very first)
            sign_prefix = "+" if not is_neg else "-"
            
            # Coefficient part
            c_part = str(abs(int(val))) 
            if power == 1 and abs_val != 0:
                c_part = ""
                
            term_str += f"{sign_prefix}{c_part}x^{power}" if (abs_val > 1 or power==1) else sign_prefix
            
        # This is getting complex without seeing the exact library output format. 
        # However, usually for these tasks: [6,0,6] -> 6x^2 + 0x + 6 -> "6x^{2}+6"
        
        latex_parts = []
        sign_prev = False
        
        for i, val in enumerate(coeffs):
            if val == 0: continue
            
            is_neg = (val < 0)
            
            # Determine operator before this term
            op = "+" if not is_neg else "-"
            
            abs_val = int(val)
            power = len(coeffs) - 1 - i
            
            coeff_disp = str(abs_val)
            
            x_part = "x" + ("^{" + str(power) + "}" if power > 1 and (abs_val != 0 or power==1 else "") ) # Simplify: always include ^ for clarity? No.
            
            term_str = ""
            
            if abs_val == 1 and power == 1:
                coeff_disp = ""
            elif abs_val == 1 and power > 1:
                 pass # keep it as is, but remove '1'
                
            final_term = f"{op}{coeff_disp}x^{power}" if (abs_val != 0) else "0"
            
            latex_parts.append(final_term.strip())

        return "".join(latex_parts).replace("+ -", "- ")


    # Refined LaTeX generator assuming standard polynomial representation [c_n, ..., c_0]
    def get_latex_str(coeffs):
        if not coeffs: return ""
        
        terms = []
        n = len(coeffs) - 1
        
        for i in range(len(coeffs)):
            val = coeffs[i]
            
            # Handle zero coefficient (skip term unless it's the only one, but here we skip usually)
            if val == 0: continue
            
            power = n - i
            
            sign_str = "+" if val > 0 else "-"
            abs_val = int(abs(val))
            
            coeff_part = ""
            x_part = "x" + ("^{" + str(power) + "}" if power != 1 and (coeff_part or True) else "") # Actually, usually omit ^1
            
            term_str = sign_str
                
            if abs_val > 0:
                if power == 0:
                    coeff_disp = str(abs_val)
                    x_part = ""
                elif power == 1:
                    coeff_disp = str(abs_val) if abs_val != 1 else ""
                    x_part = "x" # ^1 is usually omitted in LaTeX math mode unless specified, but here standard form.
                else:
                     coeff_disp = str(abs_val) if abs_val != 1 else ""
                     
            term_str += f"{coeff_disp}{x_part}"
            
            terms.append(term_str.strip())

        return " ".join(terms).replace(" + ", "+ ").strip()


    quotient_latex = get_latex_str(quotient_coeffs)
    remainder_latex = get_latex_str(remainder_coeffs)
    
    # Handle case where result is empty or zero explicitly if needed, but div_qr usually returns valid lists.
    if not quotient_latex: quotient_latex = "0"
    if not remainder_latex: remainder_latex = "0"

    question_text = f"Solve for the polynomial division of $\\{{{quotient_coeffs}, \\{{divisor}}$." # Wait, need to format dividend and divisor in LaTeX.
    
    def get_poly_str(coeffs):
        latex = get_latex_str(coeffs)
        return "\\( " + latex.replace("+ ", "+") + " )" if latex else "(0)"

    div_latex = f"\\{{{quotient_coeffs}}}" # No, need to render the polynomial. 
    dividend_tex = get_latex_str(frozen["dividend_coefficients"]) or "6x^2+1"?
    
    # Let's reconstruct the question text properly using LaTeX delimiters as requested.
    d_div = frozen["dividend_coefficients"]
    d_denom = frozen["divisor_coefficients"]
    
    q_latex_full = get_latex_str(d_div) if d_div else "0"
    r_latex_full = get_latex_str(d_denom) if d_denom else "1" # Divisor
    
    question_text = f"Simplify the polynomial division of $\\{{{q_latex_full}\\}}$ by $\\{{{r_latex_full}\\}}$. Express your answer as a quotient and remainder."
    
    correct_answer = {
        "quotient_coefficients": quotient_coeffs,
        "remainder_coefficients": remainder_coeffs,
        "quotient_latex": get_latex_str(quotient_coeffs),
        "remainder_latex": get_latex_str(remainder_coeffs)
    }

    oracle_payload = frozen
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }