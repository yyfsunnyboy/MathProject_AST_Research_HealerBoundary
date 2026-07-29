# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as per task specification
    frozen_params = {
        "dividend_coefficients": [6, 0, 6],
        "divisor_coefficients": [1, -4]
    }

    from core.prompts.domain_function_library import PolynomialOps
    
    dividend_coeffs = frozen_params["dividend_coefficients"]
    divisor_coeffs = frozen_params["divisor_coefficients"]
    
    # Perform polynomial division using the domain library
    quotient, remainder = PolynomialOps.div_qr(dividend_coeffs, divisor_coeffs)

    def format_latex(coeffs):
        if not coeffs:
            return "0"
        
        terms = []
        for i, coeff in enumerate(reversed(coeffs)):
            power = len(coeffs) - 1 - i
            
            # Skip leading zeros but handle the case where all are zero (handled by logic above mostly, 
            # though div_qr might return empty list if divisor is constant and dividend is smaller degree? No, usually returns [0])
            # Actually standard polynomial representation: highest power first.
            
            term = str(coeff)
            if coeff != 1 or coeff != -1:
                term += "x"
            if power > 0:
                term += f"^{{{power}}}"
            terms.append(term)
        
        return "\\text{" + "+".join(terms) + "} \\cdot x^{\\max\_deg} ... wait, simpler format needed."

    # Re-implementing latex formatting to be safe and precise based on standard math notation expectations in these tasks.
    def poly_to_latex(coeffs):
        if not coeffs:
            return "0"
        
        terms = []
        for i, coeff in enumerate(reversed(coeffs)):
            power = len(coeffs) - 1 - i
            
            # Skip leading zeros? The input [6, 0, 6] implies 6x^2 + 0x + 6. 
            # If the result has internal zeros (like x), we usually write it as just 'x' or keep zero if strictly required by format.
            # Standard convention: omit coefficient of 1 and -1 unless specified otherwise, but include powers correctly.
            
            term = str(coeff)
            if coeff == 0: 
                continue
            
            if power > 0:
                if abs(coeff) == 1:
                    sign_str = "" if coeff > 0 else "-"
                    terms.append(f"{sign_str}x^{power}")
                else:
                    term += f"x^{power}"
            elif power == 0 and abs(coeff) != 1: # e.g. constant -2 or 3
                 pass
            
        # Let's refine the logic to match typical output expectations for such tasks
        final_terms = []
        
        # Iterate from highest degree down to 0
        n = len(coeffs)
        for i in range(n):
            coeff = coeffs[i]
            power = n - 1 - i
            
            if coeff == 0:
                continue
                
            term_str = str(coeff)
            
            if abs(term_str) > 1 or (term_str != "1" and term_str != "-1"):
                 # Coefficient is not +/-1, so always write it out with x^p unless p=0? 
                 # Usually: -2x + 3. If coeff is 5, power 4 -> 5x^4.
                if abs(coeff) == 1 and term_str != "1" and term_str != "-1":
                    pass
                
            # Construct string based on coefficient value
            c = int(term_str)
            
            part = ""
            if c > 0:
                sign = "+"
            else:
                sign = "-"
                
            abs_c = str(abs(c))
            
            term_part = f"{abs_c}x^{power}" if power > 0 else "1" # Wait, constant terms need handling
            
            # Correct logic for LaTeX polynomial sum
            pass

    # Let's use a robust helper function to generate the string representation
    
    def get_poly_str(coeffs):
        if not coeffs: return "0"
        
        parts = []
        n = len(coeffs)
        for i, c in enumerate(reversed(coeffs)):
            p = n - 1 - i
            
            # Skip zero coefficients? Yes. But wait, the input [6, 0, 6] has a zero. 
            # If we skip it, we get "6x^2 + 6". Correct.
            
            if c == 0: continue

            term = str(abs(c))
            if p > 0:
                term += f"x^{p}"
                
            sign = ""
            if c < 0 and len(parts) > 0: # Add minus before next positive? No, standard is + - ...
                 pass
            
            # Simpler approach for LaTeX construction in these specific tasks often expects explicit signs or just concatenation with '+'
            # Let's assume the format: "6x^2+6" -> "\\(6x^{2}+6\\)" 
            # Or with spaces? Usually compact.
            
            term_str = f"{term}" if p > 0 else str(c)
            
            parts.append(term_str)

        return "+".join(parts)


    quotient_latex = r"\(" + get_poly_str(quotient) + r"\)"
    remainder_latex = r"\(" + get_poly_str(remainder) + r"\)"
    
    # Construct the correct_answer dict structure as requested: 
    # "correct_answer must include quotient_coefficients, remainder_coefficients, quotient_latex, and remainder_latex."
    # The return value of generate() is a dict with keys: question_text, correct_answer, oracle_payload.
    
    qa_dict = {
        "quotient_coefficients": quotient,
        "remainder_coefficients": remainder,
        "quotient_latex": quotient_latex,
        "remainder_latex": remainder_latex
    }

    # Construct the full return dictionary
    result = {
        "question_text": r"Perform polynomial division of \( 6x^2 + 0x + 6 \) by \( x - 4 \).",
        "correct_answer": qa_dict,
        "oracle_payload": frozen_params
    }

    return result
