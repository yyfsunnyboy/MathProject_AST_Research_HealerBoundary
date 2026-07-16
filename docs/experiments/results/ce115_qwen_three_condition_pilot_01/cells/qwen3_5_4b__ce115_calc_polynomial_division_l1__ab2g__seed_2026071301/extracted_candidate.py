def generate(level=1, **kwargs):
    # Frozen sampled parameters from task specification
    frozen_params = {
        "dividend_coefficients": [6, 0, 6],
        "divisor_coefficients": [1, -4]
    }
    
    # Construct the polynomial strings for question_text
    dividend_str = f"{frozen_params['dividend_coefficients'][0]}x^2 + {frozen_params['dividend_coefficients'][1]}x + {frozen_params['dividend_coefficients'][2]}" if len(frozen_params['dividend_coefficients']) > 1 else str(frozen_params['dividend_coefficients'][0])
    divisor_str = f"{frozen_params['divisor_coefficients'][0]}x + {frozen_params['divisor_coefficients'][1]}"
    
    # Perform polynomial division with exact arithmetic (integers only)
    # Dividend: 6x^2 + 0x + 6 -> [6, 0, 6]
    # Divisor: x - 4 -> [1, -4]
    
    dividend = frozen_params['dividend_coefficients'][:]
    divisor = frozen_params['divisor_coefficients'][::-1]  # Reverse to match standard long division (highest degree first)
    
    quotient_coeffs = []
    remainder_coeffs = []
    
    while len(dividend) > 0:
        if dividend[0] == 0 and len(dividend) > 1:
            break
            
        divisor_degree = len(divisor) - 1
        
        # Calculate leading coefficient of the term to subtract
        lead_divisor = divisor[-1]
        
        if lead_divisor != 0:
            factor = dividend[0] // lead_divisor
            quotient_coeffs.append(factor)
            
            # Subtract (factor * x^(deg_diff)) from current dividend
            deg_diff = len(dividend) - 1 - divisor_degree
            
            for i in range(len(divisor)):
                idx_in_dividend = i + deg_diff
                if idx_in_dividend < len(dividend):
                    dividend[idx_in_dividend] -= factor * divisor[i]
    
    # Normalize quotient coefficients (remove trailing zeros)
    while len(quotient_coeffs) > 1 and quotient_coeffs[-1] == 0:
        quotient_coeffs.pop()
        
    # Construct remainder list from remaining dividend elements, padded with leading zeros if necessary to match degree of divisor - 1? 
    # Actually, standard representation is just the coefficients.
    # The problem asks for "degree lower than the divisor". Divisor is linear (deg 1), so remainder should be constant or empty/zero list if divisible.
    
    # Ensure quotient and remainder are JSON compatible integers
    final_quotient = [int(c) for c in quotient_coeffs]
    final_remainder = dividend[:]
    
    while len(final_remainder) > 0 and final_remainder[-1] == 0:
        if len(final_remainder) <= 2: # If it's just zeros, stop to avoid empty list issues unless strictly zero remainder is expected as [] or [0]? 
            break
        final_remainder.pop()
    
    # For linear divisor x-4 dividing a quadratic with even roots (6x^2+6 = 3(2)(x^2+1) no wait, 6(x^2+1), remainder is not zero.
    # Let's re-calculate manually to be sure:
    # Dividend: 6x^2 + 0x + 6
    # Step 1: (6/1)x = 6x. Quotient so far [6]. 
    # Subtract 6x * (x - 4) = 6x^2 - 24x.
    # New dividend: (6-6)x^2 + (0 - (-24))x + 6 = 0x^2 + 24x + 6 -> [0, 24, 6]
    # Step 2: Leading term is 24x. Divisor leading x. Factor 24/1 = 24. Quotient so far [6, 24].
    # Subtract 24 * (x - 4) = 24x^2? No wait. 
    # Current dividend degree is 1 (coeffs [0, 24, 6] means 24x + 6). Divisor degree 1.
    # Factor: 24 / 1 = 24.
    # Subtract 24 * x? No, divisor is x - 4. 
    # Term to subtract: 24 * (x) -> wait, alignment matters.
    # Current dividend polynomial: P(x). Divisor D(x)=x-4.
    # Leading term of current remainder after step 1 was 0*x^2 + 24*x + 6. 
    # We divide by x. So we take 24*x / x = 24.
    # Multiply divisor by 24: 24*(x-4) = 24x - 96.
    # Subtract from current remainder (0, 24, 6): 
    # Coeff of x^1: 24 - 24 = 0.
    # Constant term: 6 - (-96) = 102.
    # New dividend: [0, 0, 102]. Loop ends because leading coeff is 0 and length > degree? 
    # Actually loop condition `len(dividend) > 0` with check for zero lead handles it.
    
    # Let's re-verify the manual calculation logic in code trace above:
    # Initial: [6, 0, 6] (deg 2)
    # Divisor reversed: [-4, 1]? No, standard is high to low. 
    # My previous reversal was correct for indexing but let's stick to math.
    # D(x) = x - 4. Coeffs [1, -4]. High degree first.
    
    # Iteration 1:
    # Lead dividend (deg 2): 6. Lead divisor (deg 1): 1. Factor = 6/1 = 6.
    # Quotient term: +6x^(2-1) -> coeff index -1 in quotient list? 
    # Let's build quotient from high degree to low.
    # Q0 = 6.
    # Subtract 6 * (x^1 * D(x)) = 6*(x*x - 4x)? No, x^(2-1) is x^1. So 6*x*D(x).
    # Wait, polynomial division: 
    # Dividend A = a_n x^n + ...
    # Divisor B = b_m x^m + ... (b_m != 0)
    # Term T = (a_n / b_m) * x^(n-m).
    # Subtract T*B from A.
    
    # Step 1: n=2, m=1. a_2=6, b_1=1. Factor f=6. Power k=1.
    # Term = 6x^1. 
    # Multiply by B(x)=x-4 -> 6x^2 - 24x.
    # A_new = (6x^2 + 0x + 6) - (6x^2 - 24x) = 24x + 6. Coeffs [0, 24, 6].
    
    # Step 2: n=1, m=1. a_1=24, b_1=1. Factor f=24. Power k=0.
    # Term = 24x^0 = 24.
    # Multiply by B(x)=x-4 -> 24x - 96.
    # A_new = (24x + 6) - (24x - 96) = 102. Coeffs [0, 0, 102].
    
    # Step 3: n=0? Leading coeff is 102 at degree 0. 
    # But divisor has m=1. We cannot divide x^0 by x^1 in standard polynomial division (degree of remainder must be < degree of divisor).
    # So we stop here. Remainder is 102. Quotient coeffs are [6, 24].
    
    final_quotient = quotient_coeffs[:]
    final_remainder = dividend[:]
    
    # Clean up trailing zeros in lists to match standard representation (highest degree first)
    while len(final_quotient) > 1 and final_quotient[-1] == 0:
        final_quotient.pop()
        
    if not any(final_remainder):
        final_remainder = [0] # Represent zero remainder as list containing one zero? Or empty? 
        # Specification says "degree lower than the divisor". A constant is degree 0. Divisor deg 1. So valid.
        # If result is exactly divisible, usually represented as quotient and [] or [0]. 
        # Given exact arithmetic requirement, let's keep it as a list of coefficients for the remainder polynomial.
    
    question_text = f"Divide {dividend_str} by {divisor_str}"
    
    correct_answer = {
        "quotient_coefficients": final_quotient,
        "remainder_coefficients": final_remainder
    }
    
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }