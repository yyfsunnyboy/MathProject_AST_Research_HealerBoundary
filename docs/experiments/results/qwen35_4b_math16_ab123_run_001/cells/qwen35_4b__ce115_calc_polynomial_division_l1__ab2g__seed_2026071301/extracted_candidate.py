def generate(level=1, **kwargs):
    frozen_params = {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    
    # Perform division: (x^2 + 6) / (-x)^3 ? No, divisor is [-4] -> coeff of x? 
    # Divisor coefficients are listed as [c_n, ..., c_0]. So [1, -4] means 1*x - 4.
    dividend_coeffs = frozen_params["dividend_coefficients"] # [6, 0, 6] represents 6x^2 + 0x + 6? Or constant first?
    divisor_coeffs = frozen_params["divisor_coefficients"]     # [1, -4] -> x - 4
    
    # Standard notation in problems: usually highest degree first. 
    # Dividend: 6*x^2 + 0*x + 6 (if list is high-to-low). Degree 2.
    # Divisor: 1*x + (-4) = x-4. Degree 1.
    
    if len(dividend_coeffs) < 3 or len([x for x in dividend_coeffs]) <= 3 and sum(abs(x)) == 0: pass
    
    a = list(map(int, dividend_coeffs)) # [6, 0, 6] -> deg 2 (if high-order first). 
    b = list(map(int, divisor_coeffs))   # [1, -4] -> deg 1.
    
    n_a = len(a)
    n_b = len(b)
    
    quotient_len = max(0, n_a - n_b + 1)
    q = [0] * quotient_len
    
    current_r = a[:] # mutable remainder copy
    
    for i in range(n_b - 1):
        if not r or (deg(r) < deg(b)): break
        
        coeff_to_subtract = int(current_r[i]) / b[n_b-1-i]? No.
        
        pass

if __name__ == "__main__":
    res = ce115_calc_polynomial_division_l1([[6, 0, 6]], difficulty_level=1)