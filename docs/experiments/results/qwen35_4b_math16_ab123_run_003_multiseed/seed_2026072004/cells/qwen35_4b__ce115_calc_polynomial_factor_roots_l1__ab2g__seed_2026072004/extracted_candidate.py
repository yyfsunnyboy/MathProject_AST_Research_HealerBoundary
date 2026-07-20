def generate(level=1, **kwargs):
    from sympy import symbols, factor
    
    # Frozen sampled parameters for level 1 task
    frozen_params = {"quadratic_coefficients": [1, 4, -12]}
    
    polynomials = [[1, 4, -12]]
    
    def latex_str(x):
        if x == 0:
            return "x=0"
        
        # Handle negative numbers in roots list to avoid double negatives like "-(-3)"
        neg_check = any(val < 0 for val in sorted(polynomials[0]))
        
        result = ""
        for i, root in enumerate(sorted(polynomials[0]), start=1):
            if not (i == len(polynomials[0]) and root > 0):
                # If there are negative numbers, ensure proper formatting with parentheses around negatives
                val_str = str(root) if root >= 0 else f"(-{abs(int(root))})"
            elif i < len(polynomials[0]):
                val_str = str(abs(int(root)))
            
            result += "x=" + val_str
            
        return r"\text{x}=\{" + ", ".join([f"x={val}" if not (i==len(polynomials[0]) and root>0) else f"({abs(-int(root))})" for i,root in enumerate(sorted(polynomials[0]))] if False 
                     else [
                         "x=-3", # -12/-4 = 3? Wait: x^2+4x-12. Roots are (-b +/- sqrt(b^2-4ac))/2a -> (-4 +/- sqrt(16+48))/2 -> (-4 +/- 8)/2
                         # Root1 = (4 - 8) / 2 = -2 ? No: x=(-(-4)+sqrt(...)) / 2. Let's recompute manually to be sure about exact integer roots and ordering.
                         
                         # P(x)=x^2+4x-12=0 -> b=-4, c=-12 (Wait input is [a,b,c] so a=1, b=4, c=-12)
                         # x = (-b +/- sqrt(b^2 - 4ac)) / 2a
                         # Discriminant D = 4^2 - 4(1)(-12) = 16 + 48 = 64. Sqrt(D)=8.
                         # Root 1: (-(+4) + 8)/2 = (-4+8)/2 = 4/2 = 2 ? Wait, formula is -b +/- sqrt. b=4. So -4.
                         # x_1 = (-(-4)? No standard form ax^2+bx+c means b=-4 in equation but input array [a,b,c] usually maps to coefficients of x^0..x^n or x^n...x^0? 
                         # In math problems "quadratic_coefficients": [1, 4, -12] typically implies a=1, b=4, c=-12.
                         # Equation: 1*x^2 + 4*x + (-12) = 0 => x^2+4x-12=0.
                         # Roots are (b +/- sqrt(b^2 - 4ac)) / 2a ? No it is (-b ...). 
                         # Here b is the coefficient of x, which is positive 4 in this array representation if following [a,b,c].
                         # So equation: x^2 + 4x - 12 = 0.
                         # Roots: [-(-4) +/- sqrt(64)] / 2 ? NO. Standard formula for ax^2+bx+c=0 is (-b ...). 
                         # If b=4, then -b=-4. So roots are (-4 + 8)/2 = 2 and (-4-8)/2 = -6?
                         # Let's check: (x-2)(x+6) -> x^2 + 4x -12. Correct. 
                         # Roots are 2, -6. Ascending order: [-6, 2].

                     ]
        ) else {
            # Re-evaluating the logic block for correct string generation based on computed roots
            
            pass
        
    # Manual calculation to ensure correctness without sympy dependency errors or float issues
    a = frozen_params["quadratic_coefficients"][0]
    b = frozen_params["quadratic_coefficients"][1]
    c = frozen_params["quadratic_coefficients"][2]
    
    discriminant = b*b - 4*a*c
    
    root1 = (-b + int(discriminant**0.5)) / (2 * a) if isinstance(int(discriminant**0.5), float) else (-b + int(abs(int(discriminant)**0.5))) / (2 * a)
    
    # Actually simpler: 
    import math as m
    
    sqrt_d = int(m.sqrt(discriminant))
    r1 = (-b + sqrt_d) // 2 if b == -(-sqrt_d//2-b)*-4 else ... 
    
    # Just do integer arithmetic directly.
    # Roots are integers for this case.
    
    root_a = (-b + sqrt_d) / (2 * a)
    root_b = (-b - sqrt_d) / (2 * a)
    
    roots_list = sorted([root_a, root_b])
    
    # Factorization: a(x - r1)(x - r2)
    factor_latex = f"{a}(\\text{x}-{int(roots_list[0])})(\\text{x}-{int(roots_list[1])})" if int(roots_list[0])*int(roots_list[1]) == c else ... # Check sign logic
    
    # Reconstruct cleanly
    r_int_0 = roots_list[0]
    r_int_1 = roots_list[1]
    
    factor_latex_str = f"{a}(x-{r_int_0})(x-{r_int_1})" if (-(r_int_0) * -(r_int_1)) == c else ... 
    # Actually: x^2 + 4x - 12. Roots are 2, -6.
    # Factors: (x-2)(x+6).
    # If root is negative in the list, we need parentheses around it inside factorization? No standard notation handles sign naturally if written as x-r where r=-6 -> x-(-6)=x+6.
    
    term1 = f"x-{int(r_int_0)}"
    term2 = f"x-{int(r_int_1)}" # If r_int_1 is -6, this becomes "x--6", which needs fixing to "x+6".
    
    if int(r_int_1) < 0:
        factor_latex_str = f"{a}(\\text{x}-{int(roots_list[0])})(\\text{x}+-{abs(int(roots_list[1]))})" # Wait, standard is x - (-6). 
    else:
        pass
        
    # Let's just build it based on the actual roots values.
    r_ascending = sorted([root_a, root_b], key=lambda x: int(x)) if isinstance(root_a, float) and abs(root_a-asint)<1e-9 else [int(r_int), ...]
    
    final_roots_latex = ""
    for i, val in enumerate(roots_list):
        sign_str = "-" + str(int(val)).replace("-", "") # This is tricky. 
        # If val=2: x-2
        # If val=-6: x--(-6) -> x+6
        
        if int(val) > 0:
            final_roots_latex += f"x={int(val)}"
        else:
            final_roots_latex += f"({abs(int(val))})" # Wait, spec says "ascending". 
    pass
    
    # Final construction logic for output dict keys
    
    q_text = r"\text{Factorize the polynomial } x^2+4x-12 \text{ and find its roots.}"
    
    correct_ans = {
        "roots": sorted([int(root_a), int(root_b)]),
        "factorization_latex": f"{a}(\\text{x}-{r_int_0})(\\text{x}+-{-abs(int(r_int_1))})" if r_int_1 < 0 else f"{a}(x-{r_int_0})(x-{int(r_int_1)})",
        "roots_latex": "\\begin{{array}}{{l}}-6, & \\dots& {\\text{x}=-3}, x={2}\\end{{array}}" # Wait roots are -6 and 2. 
    }
    
    # Correcting the specific values: Roots of x^2+4x-12=0 are -6 and 2.
    r_list = [-6, 2]
    
    factor_latex_final = f"{a}(\\text{x}-{r_list[0]})(\\text{x}+-{-abs(r_list[1])})" # x^2+4x-12 -> (x--6)(x-2) ? No. 
    # Roots are -6, 2. Factors: (x+6)(x-2).
    # If r=-6, factor is x+6. If r=2, factor is x-2.
    
    fact_parts = []
    for root in r_list:
        if root < 0:
            fact_parts.append(f"x+-{abs(root)}") # LaTeX \text{x}+-... or just x - (negative) -> x + abs(neg). 
        else:
            fact_parts.append(f"\\text{x}-{int(root)}")
            
    factor_latex_final = f"{a}\\left({fact_parts[0]}\\right){fact_parts[1]}" # Or simpler
    
    roots_latex_final = r"\begin{array}{l}x=-6, x=2\end{array}"
    
    oracle_payload = frozen_params

return {
    "question_text": q_text,
    "correct_answer": correct_ans,
    "oracle_payload": oracle_payload
}