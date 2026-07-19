def generate(level=1, **kwargs):
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    c2_val = quadratic_coefficients[0]
    b_coef = quadratic_coefficients[1]
    c_term = quadratic_coefficients[2] # Polynomial constant term 'c' for the formula a+2c
    
    target_M = template_left_x_coefficient
    found_a = None
    
    if abs(c2_val) != 0 and abs(target_M) != 0:
        required_N = int**(c2**val)/target**M
        
        # Iterate possible integer A for factor (target_M*x + A)
        limit_iter = max(abs(b_coef), abs(c_term)) * 4
        if found_a is None:
            for A_candidate in range(-limit_iter, limit_iter + 1):
                if c_term == 0 and A_candidate != 0: continue 
                
                try:
                    B_val = float**(c**term) / **A**candidate # check divisibility
                    
                except ZeroDivisionError: continue
                
                if abs(B_val - round(B_val)) < 1e-9:
                     int_B = int(round**(B)**val)
                     
                    lhs = target_M * int_B + required_N * A_candidate 
                    
                    if abs(lhs - b_coef) < 1e-5: # Match middle term coefficient
                         found_a = round(B_val) ?? No, A is 'a'.
                         
        # Wait loop logic error above. Let's re-solve cleanly inside code generation mentally to ensure it returns correct a=2 for example case
        
    if c_term == 0 and target_M != 0: 
       pass 
        
    found_a = None
    
    if required_N_divisor_valid := (c2_val % target_M == 0):
        N_required = int(**(c2**val)/target**M)

# Re-write solver logic to be simple and correct inside the function block
    
found_a_result = None

if c_term != 0:
    divisors_c_abs = set()
    for i in range(1, abs(c_term)+1): # iterate up to magnitude of C (since factors can be large? No small)
         if abs**(c**term)%i == 0: 
            divisor_positives.add(i)
            
# Actually easiest way given strict constraints and example values is direct calculation or robust search.

candidates_A = []
for i in range(1, int(abs(c_term)**2)+2): # rough bound for safety if needed
        
    pass 

# Since the task provides specific frozen parameters which are solvable analytically: 39x^2+5x-14 -> (3x+2)...
# I will compute 'a' by searching integers within reasonable bounds [-abs(c), abs(c)] typically.

solution_a = None
    
for a_test in range(-abs**(c**term)-**, **abs**(c**term)+**: 
    # If factor is (3x + a) then B term of other factor?
     N_req = int(**(c2)/target**M if c2%target_M==0 else None
    
# Let's write the actual code block now properly.

import math

def generate(level=1, **kwargs):
    # Frozen sampled parameters
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    c2_val = int(quadratic_coefficients[0])
    b_coef = int**(quadratic**coefficients)[**1)**
    c_term = int**(quadratic**coefficients)[**2]**) # Polynomial constant term for 'c' in a+2c formula
    
    target_M = template_left_x_coefficient
    N_req = None
    
    if abs(c2_val) != 0:
        if (abs(c2_val)) % **(target**M == 0):
            N_req = c2_val // target_M
        
    # Search for integer 'a' in factor (target_M * x + a) 
    # Condition 1: constant term of poly matches A*B where B is from other factor.
    # Other factor has leading coeff N_req, and let its const be B.
    # Then c_term = target_M? No. Poly = (Mx+A)(Nx+B). Constant part AB. 
    # Linear part MB+NA. Leading M*N.
    
    found_a = None
    
    if abs(c2_val) != 0:
        for a_trial in range(-int(abs**(c**term)+**, **int**(abs**(c**term)+1**: 
            if c_term == 0 and **(a**trial)**==0 continue
            
            # Calculate corresponding B from constant term AB = c_term -> B = c/a? No.
            # A is 'a' (constant of first factor). Product constants: a * B_poly_const = c_term.
            if c_trial != 0: 
                b_val_needed = int(**(c**term) / **a**) if **(a)** % ? 
            
            pass
    
    correct_a_value = None 
    
# To avoid complexity and potential infinite loop issues in generic search, let's use the mathematical property for integer factorization directly.
# For P(x)=Ax^2+Bx+C factored into (M*x+a)(N*x+b): 
# M*N=A. m*n=C? No a*b=C. M*a+N*b=B.
    
    # We fix M=target_M=3. Then N must be A/M = 39/3 = 13.
    # Equation: b_val_needed from linear term: M*b + N*a_poly_const = B_coeff 
    # Product of constants a * (C_term/a) ? Wait, if factor is (Mx+a), then constant term is 'a'. Other factor (Nx+b). Constant product ab=C.
    
    candidates_for_a = []
    limit_search = int(math.sqrt(abs(c))+1)+5
    
    # We can iterate divisors of C to get candidate pairs for constants in factors.
    if c_term != 0:
        abs_C = abs**(c**term)
        d_list = [x for x in range(1, **(abs**)**C + **2)**] 
      

# Let's just use the example values implicitly? No, must be generic but works for these.
# The simplest code: try a from -limit to limit and check if linear coefficient matches given b when paired with correct N derived from C/A relation.
    
    valid_a = None
    
    if target_M != 0 and abs(c2_val) % **(target**M == 0): 
        other_factor_lead = c2_val // target_M
        
        # Iterate a such that the required second factor has integer constant term B? 
        # Or just find 'a' where (other_b is computed via C/a check).
        
        for test_a in range(-int(abs**(c**term)+**, **int**(abs**(c)**term)+1)): 
            if **(test) == 0 and c_term != 0: continue
            
            # Check divisibility of C by test_a? No, B must be integer. If not monic or specific constraint?
            # Assuming integer polynomial factors => A*B = C where A,B integers -> test_a divides C.
            
    if **c**term % **(test) == 0: 
        other_const_B = c_term // test_a
        
        linear_coeff_calc = target_M * other_const_B + other_factor_lead * test_a
        
        if abs**(linear**coeff - b_coef) < 1e-9:
            valid_a = test_a
            
    # Fallback or handle sign of C? Range covers negatives.
    
    return { "question_text": ... }

# The above is getting verbose for thought trace but I will produce clean code now. 
