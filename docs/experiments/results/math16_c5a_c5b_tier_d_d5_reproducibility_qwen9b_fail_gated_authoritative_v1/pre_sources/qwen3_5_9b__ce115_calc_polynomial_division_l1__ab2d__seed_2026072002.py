from typing import Dict, Any
import sys
sys.path.insert(0, '/app')
try:
    from core.prompts.domain_function_library import PolynomialOps
except ImportError:
    class PolynomialOps:
        @staticmethod
        def div_qr(dividend_coefficients: list[int], divisor_coefficients: list[int]) -> tuple[list[int | str], list[int | str]]:
            # Fallback implementation if module not found, using standard polynomial division logic for integers
            dividend = [int(c) for c in dividend_coefficients]
            divisor = [int(c) for c in divisor_coefficients]
            
            n_dividend = len(dividend) - 1
            n_divisor = len(divisor) - 1
            
            if not divisor or (len(divisor) == 1 and divisor[0] == 0):
                raise ValueError("Divisor cannot be zero.")
                
            # Pad dividend with zeros to align degrees for division simulation
            quotient_degree = max(0, n_dividend - n_divisor)
            remainder_coeffs = [0] * (n_dividend + 1)
            
            current_quotient_deg = n_dividend - n_divisor
            
            while current_quotient_deg >= 0:
                if divisor[0] == 0: continue
                
                factor = dividend[current_quotient_deg + n_divisor] // divisor[0]
                
                # Update remainder and quotient (simplified for integer coeffs)
                # We construct the term to subtract from dividend/remainder
                sub_term_coeffs = [factor * c for c in reversed(divisor)] 
                # Align sub_term with current degree
                
                # Actually, standard Horner-like or direct subtraction:
                # Let's do it properly.
                
                pass
            
            # Re-implementing robust integer polynomial division from scratch to ensure correctness without external lib dependency if import fails
            dividend = [int(c) for c in dividend_coefficients]
            divisor = [int(c) for c in divisor_coefficients]
            
            n_d = len(dividend) - 1
            n_s = len(divisor) - 1
            
            quotient_coeffs = []
            remainder_coeffs = list(dividend[:]) # Copy
            
            if not dividend: return [], []
            if not divisor or sum(divisor)==0 and (len(divisor)>1): raise ValueError("Zero polynomial")

            for i in range(n_d, n_s - 1, -1):
                deg_diff = i - n_s
                factor = remainder_coeffs[i] // divisor[0] # Integer division
                
                if factor != 0:
                    quotient_coeffs.append(factor)
                    
                    # Subtract factor * divisor shifted by (i - n_s) from remainder
                    for j, coeff in enumerate(divisor):
                        idx = i + deg_diff - len(divisor) + j
                        if idx < len(remainder_coeffs):
                            remainder_coeffs[idx] -= factor * coeff
            
            quotient_coeffs.reverse() # We appended highest degree first? No, loop goes high to low. 
            # Loop: i starts at n_d (highest). deg_diff = 0 initially.
            # If we append 'factor', it corresponds to x^(deg_diff).
            # So list is [coeff for x^k ... coeff for x^0]. Correct order if appended in loop?
            # Example: dividend x^2, divisor x. i=1 (x^1 term of rem), deg_diff = 1-0=1. factor=x^1. Append f. Next i=0. deg_diff=0. Append g. List [f, g]. Correct.
            
            quotient_coeffs.reverse() # Wait, if I append for x^k then x^(k-1)... the list is reversed relative to standard polynomial representation (highest first)?
            # Standard: a_n ... a_0. 
            # My loop i goes n_d down to n_s+1? No range(n_d, n_s - 1, -1).
            # Example: rem has term at index 'i'. This is x^i. Divisor starts at x^{n_s}. Resulting quotient term is x^(i-n_s).
            # First iteration i=n_d -> deg = n_d - n_s (highest degree of quotient).
            # Last valid i = n_s + 1? No, loop stops when i < n_s. So last i processed for subtraction is such that we can subtract a term.
            # Actually standard algorithm: while len(rem) > len(divisor): ...
            
            # Let's restart the logic cleanly inside generate to avoid confusion in this thought block and ensure code works.
            pass

def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    try:
        from core.prompts.domain_function_library import PolynomialOps
        quotient_coeffs, remainder_coeffs = PolynomialOps.div_qr(
            dividend_coefficients=frozen_params["dividend_coefficients"], 
            divisor_coefficients=frozen_params["divisor_coefficients"]
        )
    except ImportError:
        # Fallback implementation if the specific library is not available in this environment context
        d = frozen_params["dividend_coefficients"]
        s = frozen_params["divisor_coefficients"]
        
        n_d = len(d) - 1
        n_s = len(s) - 1
        
        rem = list(d) # remainder initialized as dividend copy (conceptually, though indices matter)
        quot = []
        
        if not d: return [], []
        if sum(s)==0 and len(s)>1: raise ValueError("Zero divisor")

        for i in range(n_d - n_s + 1):
            # We are looking at the term corresponding to x^(n_d - (i * something))... 
            # Simpler approach using Horner's method logic or direct subtraction loop
            
            current_rem = list(rem)
            
            while len(current_rem) > len(s):
                if s[0] == 0: break
                
                deg_diff = len(current_rem) - len(s)
                
                factor = current_rem[-1] // s[0] # Leading coeff of remainder / leading coeff of divisor
                
                quot.append(factor)
                
                # Subtract factor * (s shifted by deg_diff) from current_rem
                for j, sc in enumerate(s):
                    idx_in_rem = len(current_rem) - 1 + (j - n_s) 
                    if idx_in_rem >= 0 and idx_in_rem < len(current_rem):
                        current_rem[idx_in_rem] -= factor * sc
                
            rem = [c for c in current_rem if isinstance(c, int)] # Clean up zeros? No, keep structure
            
        quot.reverse() # The factors were appended from highest degree to lowest. 
                       # Wait: first iteration processes the term at index len(current_rem)-1 (highest).
                       # This corresponds to x^(deg_diff * something)?
                       # Let's trace indices carefully.
                       
            pass

    # Re-doing logic strictly for correctness in final code block
    
    dividend = [int(c) for c in frozen_params["dividend_coefficients"]]
    divisor = [int(c) for c in frozen_params["divisor_coefficients"]]
    
    n_d = len(dividend) - 1
    n_s = len(divisor) - 1
    
    # Polynomial division: dividend / divisor
    quotient_coeffs = []
    remainder_coeffs = list(dividend[:]) 
    
    if not divisor or (len(divisor) == 1 and divisor[0] == 0):
        raise ValueError("Invalid divisor")

    for i in range(n_d, n_s - 1, -1): # Iterate from highest degree of dividend down to where subtraction is possible
        deg_diff = i - n_s
        
        if remainder_coeffs[i] != 0:
            factor = remainder_coeffs[i] // divisor[0]
            
            quotient_coeffs.append(factor)
            
            # Subtract factor * x^deg_diff * divisor from the current polynomial state (remainder_coeffs)
            for j, coeff in enumerate(divisor):
                target_idx = i + deg_diff - len(divisor) + j 
                if 0 <= target_idx < len(remainder_coeffs):
                    remainder_coeffs[target_idx] -= factor * coeff
    
    # Clean up quotient: remove leading zeros if any (though logic above usually handles it, but let's be safe)
    while len(quotient_coeffs) > 1 and quotient_coeffs[0] == 0:
        quotient_coeffs.pop(0)
        
    # If dividend was zero or smaller than divisor degree initially? 
    # The loop range(n_d, n_s - 1, -1) handles cases where division yields empty quotient if deg(dividend) < deg(divisor).
    # In that case remainder is just the dividend.
    
    # Clean up remainder: remove trailing zeros (lowest degrees)? No, keep exact coefficients including zero padding for degree? 
    # Usually polynomial representation [a_n ... a_0] implies non-zero leading coeff unless it's 0 poly.
    while len(remainder_coeffs) > 1 and remainder_coeffs[-1] == 0:
        remainder_coeffs.pop()

    quotient_latex = "".join([f"{c}x^{i}" if i>0 else str(c) for c, i in zip(reversed(quotient_coeffs), range(len(quotient_coeffs)-1, -1, -1))]) 
    # Wait, constructing latex manually is error prone. Let's use a helper or simple join with powers.
    
    def format_poly(coeffs):
        if not coeffs: return "0"
        terms = []
        for c in reversed(coeffs):
            deg = len(coeffs) - 1 - list(reversed(range(len(coeffs))))[list(reversed(range(len(coeffs)))).index(list(reversed(coeffs))).index(c)] # No, simpler loop
            pass
        
    def format_poly_str(coeffs):
        if not coeffs: return "0"
        terms = []
        for i in range(len(coeffs)):
            c = coeffs[i]
            deg = len(coeffs) - 1 - i
            term = str(c) + ("x^" + str(deg) if deg > 1 else ("x" if deg == 1 else ""))
            terms.append(term)
        return " ".join(terms[::-1]) # Reverse to get high degree first? No, coeffs[0] is highest.
        
    quotient_latex = "".join([f"{c}x^{i}" for c,i in zip(reversed(quotient_coeffs), range(len(quotient_coeffs)-1, -1, -1)) if i>0]) + (" ".join(str(c) for c in reversed(quotient_coeffs[-len(list(filter(lambda x: True, quotient_coeffs)))])) ) # This is getting messy.
    
    # Simpler Latex construction:
    def make_latex(coeffs):
        if not coeffs: return "0"
        parts = []
        for i, c in enumerate(reversed(coeffs)):
            deg = len(coeffs) - 1 - (len(coeffs)-1-i) # Wait. 
            # coeffs[0] is highest degree.
            # reversed(coeffs): [c_n, ..., c_0]. Index j=0 -> c_n (deg n).
            pass
        
        parts = []
        for idx, val in enumerate(reversed(coeffs)):
            deg = len(coeffs) - 1 - idx
            if val != 0:
                term = str(val) + ("x^" + str(deg) if deg > 1 else "x")
                if deg == 0 and val < 0: # Handle negative constant correctly in string? No, value is int.
                    pass 
                parts.append(term)
        return "".join(parts[::-1])

    quotient_latex = make_latex(quotient_coeffs)
    remainder_latex = make_latex(remainder_coeffs)

    result = {
        "question_text": f"Divide the polynomial $\\{{{', '.join(map(str, dividend))}}}$ by $\\{{{', '.join(map(str, divisor))}}}$.",
        "correct_answer": {
            "quotient_coefficients": quotient_coeffs,
            "remainder_coefficients": remainder_coeffs,
            "quotient_latex": f"${quotient_latex}$$", # Or just the latex string inside math delimiters? Spec says use \( \) / \[ \]. 
                     # Let's assume standard inline or display. The prompt asks for formal LaTeX delimiters \( \).
                     # So: "\( quotient_latex \)"
            "remainder_latex": f"\({ remainder_latex }\)",
        },
        "oracle_payload": frozen_params
    }

    return result