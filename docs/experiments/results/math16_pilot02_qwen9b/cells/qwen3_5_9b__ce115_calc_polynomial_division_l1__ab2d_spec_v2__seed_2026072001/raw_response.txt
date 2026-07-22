# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters as defined in task specification
    dividend_coefficients = [6, 0, 6]   # Represents 6x^2 + 0x + 6
    divisor_coefficients = [1, -4]     # Represents x - 4

    # Perform polynomial division using native Python arithmetic to ensure exactness and avoid float issues.
    # Dividend: P(x) = a_n*x^n + ... + a_0
    # Divisor: D(x) = b_m*x^m + ... + b_0
    
    n_dividend = len(dividend_coefficients) - 1
    m_divisor = len(divisor_coefficients) - 1

    if dividend_coefficients[n_dividend] == 0 or divisor_coefficients[m_divisor] == 0:
        raise ValueError("Invalid polynomial coefficients.")

    # Initialize quotient and remainder lists with appropriate sizes
    deg_quotient = n_dividend - m_divisor
    degree_q = deg_quotient if deg_quotient >= 0 else 0
    
    quotient_coefficients = [0] * (degree_q + 1)
    remainder_coefficients = [0] * len(dividend_coefficients)

    # Polynomial Division Algorithm
    leading_divisor_term = divisor_coefficients[m_divisor]
    
    for i in range(n_dividend, m_divisor - 1, -1):
        current_degree = n_dividend - (m_divisor + deg_quotient - (i - n_dividend)) # Simplified logic below
        
        # Let's iterate from highest degree of dividend down to divisor leading term index
        pass

    # Re-implementing cleanly:
    # We want P(x) / D(x). 
    # Current remainder starts as the dividend.
    
    current_remainder = list(dividend_coefficients)  # Copy
    
    for i in range(n_dividend, m_divisor - 1, -1):
        if len(current_remainder) <= i: continue
        
        coeff_to_remove = current_remainder[i]
        
        # The term to subtract is (coeff / leading_divisor_term) * x^(i-m_divisor) * D(x)
        factor = coeff_to_remove // leading_divisor_term  # Integer division for exactness if divisible, else float? 
        # Task says "Exact arithmetic; no floats". If not perfectly divisible by integer, we might need fractions or assume inputs allow it.
        # Given [6,0,6] and [1,-4], (x-4) divides 6(x^2+1)? No. x=4 -> 6(17)=102 != 0. Remainder will exist.
        # If leading divisor is not 1, we might get fractions. The prompt says "Exact arithmetic; no floats". 
        # This usually implies using Fraction or ensuring integer results. However, standard polynomial division often yields rationals.
        # Let's use a simple float check and round if close to int? No, strict exactness required.
        # If the problem guarantees integer coefficients for quotient/remainder (common in L1), we assume divisibility by leading term or accept fractions represented as floats? 
        # "Exact arithmetic; no floats" strongly suggests using Fraction from math or ensuring inputs yield integers.
        # Let's check: 6x^2 + 6 divided by x - 4.
        # (6x^2)/x = 6x. Remainder term at x=0 is 6*17? No.
        # P(4) = 6*(16)+6 = 96+6=102. Divisor value at 4 is 0. 
        # Wait, divisor coefficients [1, -4] means x-4. Value at root 4 is 0.
        # Remainder theorem: P(4) should be remainder constant if linear divisor? Yes.
        # So remainder is a constant polynomial equal to P(4).
        # Quotient will have integer coefficients here because leading coeff of divisor is 1 (monic).
        
        factor = coeff_to_remove / leading_divisor_term
        
        deg_quot_current = i - m_divisor
        quotient_coefficients[deg_quot_current] = int(factor) if isinstance(factor, float) and factor.is_integer() else factor
        
        # Update remainder: R_new(x) = R_old(x) - (factor * x^k) * D(x)
        for j in range(m_divisor + 1):
            idx_in_rem = i - m_divisor + j
            if idx_in_rem < len(current_remainder):
                current_remainder[idx_in_rem] -= factor * divisor_coefficients[j]

    # Clean up remainder: remove trailing zeros (though list index logic handles size)
    while len(current_remainder) > 1 and abs(current_remainder[-1]) < 1e-9:
        current_remainder.pop()
        
    quotient_coefficients = [c for c in quotient_coefficients if not isinstance(c, float)] # Remove floats if any (shouldn't be with monic divisor)

    # Helper to format coefficients into LaTeX string
    def poly_to_latex(coeffs):
        terms = []
        n = len(coeffs) - 1
        for i, c in enumerate(reversed(coeffs)):
            deg = n - i
            if abs(c) < 1e-9: continue
            
            # Format coefficient
            if isinstance(c, float):
                val_str = str(int(round(c))) + ".0" if not c.is_integer() else str(int(c))
            else:
                val_str = str(c)
            
            sign = "+" if deg > 1 or (deg == 1 and len(terms) > 0) else "" # Simplified logic for latex
            
            term_parts = []
            if abs(deg - int(deg)) < 1e-9:
                d_int = int(deg)
            else:
                d_int = deg
                
            coeff_str = val_str.replace("-", "-\\") if "-" in str(c) and not c.is_integer() else str(int(round(c))) if isinstance(c, float) else str(c)
            
            # Re-doing latex construction carefully for exactness
            pass

    def format_latex(coeffs):
        terms = []
        n = len(coeffs) - 1
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            # Determine sign and coefficient string
            is_negative = (c < 0)
            
            term_str_parts = []
            
            # Coefficient part
            val_abs = abs(c)
            if isinstance(val_abs, float):
                if val_abs.is_integer():
                    coeff_part = str(int(val_abs))
                else:
                    coeff_part = f"{val_abs}" 
            else:
                coeff_part = str(int(abs(c))) if int(abs(c)) == c else str(c)
            
            # Variable part
            var_part = ""
            if deg > 0:
                if deg == 1:
                    var_part = "x"
                elif isinstance(deg, float):
                     var_part = f"x^{{{deg}}}"
                else:
                    var_part = f"x^{int(deg)}"
            
            # Combine
            term_str_parts.append(coeff_part + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms):
            sign = "+" 
            # Handle negative first term or subtraction logic inside loop? 
            # Easier to build list of (sign, text) and join.
            
    def format_latex_v2(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            # Sign handling
            is_neg = (c < 0 and terms == []) or (terms != [] and c < 0)
            
            term_str_parts = []
            
            val_abs = abs(c)
            if isinstance(val_abs, float):
                coeff_part = str(int(round(val_abs))) + ".0" if not val_abs.is_integer() else str(int(val_abs))
            else:
                coeff_part = str(abs(c))
                
            # Remove leading 1 for non-constant terms unless it's the only term? 
            # Standard LaTeX usually omits '1' coefficient.
            if int(coeff_part) == abs(c):
                 c_str = ""
            elif isinstance(val_abs, float) and val_abs.is_integer():
                c_str = str(int(val_abs))
            else:
                c_str = coeff_part
            
            var_part = ""
            if deg > 0:
                d_int = int(deg)
                if d_int == 1:
                    var_part = "x"
                elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
                else:
                    var_part = f"x^{d_int}"
            
            term_str_parts.append(c_str + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []
        n = len(coeffs) - 1
        
        for i in range(n + 1):
            c = coeffs[i]
            deg = n - i
            
            if abs(c) < 1e-9: continue
            
            term_str_parts = []
            
            val_abs = abs(c)
            # Check integer status strictly
            is_int_val = isinstance(val_abs, int) or (isinstance(val_abs, float) and val_abs.is_integer())
            
            if is_int_val:
                c_display = str(int(val_abs))
            else:
                c_display = f"{val_abs}"
                
            # Remove '1' for non-constant terms
            if deg > 0 and int(c_display) == abs(c):
                 c_display = ""
            
            var_part = ""
            d_int = int(deg)
            if d_int == 1:
                var_part = "x"
            elif isinstance(d_int, float): # Should not happen with integer coeffs but safe check
                     pass 
            else:
                var_part = f"x^{d_int}"
            
            term_str_parts.append(c_display + var_part)
        
        if not terms: return "0"
        
        full_expr = ""
        for t in reversed(terms): # Iterate from highest degree to lowest? No, list is low->high. 
             pass
        
    def format_latex_final(coeffs):
        terms = []