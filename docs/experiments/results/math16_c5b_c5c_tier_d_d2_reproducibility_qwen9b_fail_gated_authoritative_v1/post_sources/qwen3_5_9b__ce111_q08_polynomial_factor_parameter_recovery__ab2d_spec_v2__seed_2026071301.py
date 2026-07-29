# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    # Extract coefficients: ax^2 + bx + c -> coeffs[0]=a, coeffs[1]=b, coeffs[2]=c
    a_quad = frozen_params["quadratic_coefficients"][0]  # 39
    b_quad = frozen_params["quadratic_coefficients"][1]  # 5
    c_quad = frozen_params["quadratic_coefficients"][2]  # -14

    # Template: (Lx + m)(Nx + p) where L is fixed to template_left_x_coefficient
    L_fixed = frozen_params["template_left_x_coefficient"]  # 3
    
    # We need to find integers m, N, p such that:
    # L * N = a_quad => 3 * N = 39 => N = 13
    # L * p + m * N = b_quad => 3*p + 13*m = 5
    # m * p = c_quad => m * p = -14
    
    # From N=13, we substitute into the middle term equation:
    # 3p + 13m = 5
    # And mp = -14.
    
    # Solve for integer factors of c (-14): pairs (m, p) such that m*p = -14
    possible_m_values = []
    n_factors = [i for i in range(-abs(c_quad), abs(c_quad)+1) if c_quad % i == 0]
    
    found_solution = False
    
    # Iterate through divisors of c to find valid (m, p) pairs satisfying the middle term constraint
    for m_candidate in n_factors:
        if m_candidate != 0 and (c_quad // m_candidate) * L_fixed + m_candidate == b_quad - (L_fixed * (b_quad)): 
            # This logic is flawed. Let's restart with direct substitution.
            
            pass

    # Correct derivation:
    # Equation system:
    # 1) N = a_quad / L_fixed
    # 2) m * p = c_quad
    # 3) L_fixed * p + m * N = b_quad
    
    if a_quad % L_fixed != 0:
        raise ValueError("Left coefficient does not divide quadratic leading term.")

    N_val = a_quad // L_fixed
    
    # Now solve for m and p where mp = c_quad and L*p + m*N = b
    # Substitute p = c/m into linear eq: L*(c/m) + m*N = b
    # (L*c)/m + m*N - b = 0
    # Multiply by m: L*c + m^2*N - b*m = 0
    # N*m^2 - b*m + L*c = 0
    
    A_coeff = N_val
    B_coeff = -b_quad
    C_const = L_fixed * c_quad
    
    discriminant = B_coeff**2 - 4*A_coeff*C_const
    
    if discriminant < 0:
        raise ValueError("No real integer solution found.")
    
    sqrt_discriminant = int(discriminant ** 0.5)
    if sqrt_discriminant * sqrt_discriminant != discriminant:
         # Should not happen with valid inputs but good to check for integers
         pass
        
    m_candidates_1 = (-B_coeff + sqrt_discriminant) // (2*A_coeff)
    m_candidates_2 = (-B_coeff - sqrt_discriminant) // (2*A_coeff)
    
    possible_ms = []
    if discriminant >= 0:
        # Check both roots for integer validity and corresponding p being integer
        root1_num = -B_coeff + sqrt_discriminant
        root2_num = -B_coeff - sqrt_discriminant
        
        if (root1_num % (2*A_coeff)) == 0:
            m_val = root1_num // (2*A_coeff)
            # Verify mp = c_quad holds exactly with integer division to avoid float issues
            p_val = c_quad / m_val
            if isinstance(p_val, int):
                possible_ms.append(m_val)
                
        if discriminant > 0 and (root2_num % (2*A_coeff)) == 0:
             m_val = root2_num // (2*A_coeff)
             p_val = c_quad / m_val
             if isinstance(p_val, int):
                 possible_ms.append(m_val)

    # If no solution found via quadratic formula due to integer division nuances, brute force small range for safety in this specific constrained problem
    if not possible_ms:
        # Brute force search since coefficients are integers and likely small
        limit = abs(c_quad) + 10
        for m_test in range(-limit, limit+1):
            if c_quad % m_test == 0:
                p_test = c_quad // m_test
                if L_fixed * p_test + m_test * N_val == b_quad:
                    possible_ms.append(m_test)

    # According to strict_source_template policy, we assume a unique valid factorization exists matching the template.
    # The problem asks for "the" correct answer implying uniqueness or specific selection logic not fully detailed but standard in these tasks is usually positive m if ambiguous? 
    # However, looking at constraints: (3x+a)(13x+p). 3p + 13a = 5, ap = -14.
    # Factors of -14: (-1, 14), (1, -14), (-2, 7), (2, -7)... and negatives swapped.
    # Check pairs for a*p=-14 in equation 3p + 13a = 5:
    # If a=1, p=-14 -> 3(-14) + 13(1) = -42+13 != 5
    # If a=-1, p=14 -> 3(14)+13(-1)=42-13=29!=5
    # If a=2, p=-7 -> 3(-7)+13(2) = -21+26=5. Match! So a=2 is one solution.
    # If a=-2, p=7 -> 3(7)+13(-2)=21-26=-5!=5
    # If a=7, p=-2 -> 3(-2)+13(7) = -6+91 != 5
    # If a=-7, p=2 -> 3(2)+13(-7) = 6-91 != 5
    
    # So the only integer solution is m=a=2. 
    # The task asks for correct_answer as integer a + 2c.
    
    if possible_ms:
        selected_m = possible_ms[0] # Assuming unique or first valid found in order
        
        # Calculate c from oracle payload directly to ensure consistency with frozen params logic, though we derived it.
        # The prompt says "correct_answer must be the integer a+2c". 
        # Here 'a' is our recovered m (coefficient of x in left factor).
        # And 'c' corresponds to p? Wait, standard form (x+a)(bx+c) usually implies constant terms are a and c.
        # In template (3x + a), the constant term is named 'a'. 
        # The other factor is (13x + p). Let's call its constant term 'c' for the formula "a+2c".
        # So we need to identify which variable in our derivation maps to 'c' in the final answer string.
        
        # Re-reading: "(factor_order_policy": "strict_source_template", ... correct_answer must be the integer a+2c"
        # Template left factor is (3x+a). Right factor derived as (13x+p).
        # Usually polynomial factors are written (Ax+B)(Cx+D). 
        # If template says (3x+a), then B=a.
        # The other constant term D would be 'c' in the expression a+2c? Or is it referring to coefficients of original quadratic ax^2+bx+c?
        # "quadratic_coefficients": [A, B, C] usually means Ax^2+Bx+C. Here A=39, B=5, C=-14.
        # If the answer formula uses 'c' from the quadratic coefficients list (the constant term of original poly), then c = -14.
        # Then a+2c would be 2 + 2*(-14) = 2 - 28 = -26? 
        # But wait, if factors are (3x+a)(13x+p), expanding gives:
        # 39x^2 + (3p + 13a)x + ap.
        # Here a is the constant in left factor, p is constant in right factor.
        # Original C = -14. So ap = -14. We found a=2, so p=-7. 
        # If 'c' in "a+2c" refers to the original quadratic's constant term (-14), result is 2 + 2(-14) = -26.
        # If 'c' refers to the constant of the right factor (p=-7), result is 2 + 2(-7) = -12.
        
        # Context clue: "math16_polynomial_factor_parameter_recovery". Often these tasks define specific variables for the answer key. 
        # Given "quadratic_coefficients": [39, 5, -14], let's assume standard notation where quadratic is Ax^2+Bx+C.
        # The prompt asks for a+2c. If 'a' and 'c' are parameters of the factors (constants), then it likely refers to constants in the factorization.
        # However, without explicit definition that c=p, there is ambiguity. 
        # BUT: looking at similar tasks from this dataset style, often "c" in such expressions refers to the constant term of the *second* factor if not specified otherwise? Or maybe it's a trick and 'c' IS the original C?
        
        # Let's look at the variable names in frozen_params. There is no 'a' or 'c' key, only coefficients list.
        # If I assume standard math notation for factors (x+a)(bx+c), then constants are a and c.
        # In our case: Left factor constant = m (found as 2). Right factor constant = p (-7).
        # So if the expression is "a+2c", it likely means (LeftConst) + 2*(RightConst).
        # Let's proceed with a=2, c=p=-7. Result: -12.
        
        left_const = selected_m
        right_const = c_quad // selected_m
        
        correct_answer_val = left_const + 2 * right_const

    else:
         raise ValueError("No valid factorization found.")

    # Construct LaTeX question text
    # Factors are (3x+a) and (13x+c_right). 
    # We need to format them. Since we cannot import PolynomialOps, we construct string manually or use allowed helper if signature matches exactly?
    # The prompt says: "Use ONLY the signatures below... There is NO `PolynomialOps.to_latex`. Do not call `to_latex`."
    # It also lists `PolynomialOps.format_latex` but then in Task Guardrails it says "Do not use a Domain API". 
    # This creates a conflict. The prompt header says "Use native Python only; do not use a Domain API" under Task Guardrails.
    # But the Compact Domain Scaffold section mentions PolynomialOps.
    # Resolution: Follow "Task Guardrails" strictly -> Use native Python for string construction to avoid dependency/API usage issues in this isolated environment simulation.
    
    left_const_str = str(left_const) if isinstance(left_const, int) else f"{left_const}"
    right_const_str = str(right_const) if isinstance(right_const, int) else f"{right_const}"
    
    # Format: Factor 1 * Factor 2 = Quadratic
    factor1_latex = f"(3x{'' if left_const == 0 else '+' + (left_const if left_const > 0 else '')})" 
    # Handle signs properly for LaTeX display of factors like (3x-5) vs (3x+5)
    
    def format_factor(coeff_x, const_val):
        term = ""
        sign = "+"
        val_str = str(abs(const_val)) if abs(const_val) != 0 else ""
        if const_val < 0:
            sign = "-"
        elif const_val > 0:
             # If positive, usually + is omitted in math notation but included for clarity? 
             # Standard LaTeX factor (3x+5). Let's include +.
             term += f"+{val_str}" if val_str else ""
        
        return f"({coeff_x}x {sign}{term})".replace(" ", "")

    # Re-evaluate formatting logic to be robust:
    def make_factor_latex(x_coeff, const_val):
         s = str(const_val)
         sign_part = "+" if const_val > 0 else ("-" if const_val < 0 else " ")
         
         # If constant is positive, we write +c. If negative -|c|. If zero just x term? 
         # But template says (3x+a). Usually a!=0 in these problems unless specified.
         final_s = f"({x_coeff}x{sign_part}{s})".replace(" ", "") if s else f"({x_coeff}x)"
         
         # Special case: if const is 1 or -1, usually just +x or -x? 
         # But here we have specific integers. Let's stick to literal representation.
         return final_s

    factor_latex_1 = make_factor_latex(3, left_const)
    factor_latex_2 = make_factor_latex(N_val, right_const)
    
    quadratic_str = f"{a_quad}x^2 + {b_quad if b_quad >= 0 else ''}{'' if b_quad == 0 else '+'}{'-' if b_quad < 0 else ''}{abs(b_quad)}x{'' if c_quad==0 else '+'}{'-' if c_quad<0 else ''}{c_quad}"
    # Simplify quadratic string construction:
    
    def make_poly_str(a, b, c):
        terms = []
        term1 = f"{a}x^2"
        if b != 0:
            sign_b = "+" if b > 0 else "-"
            val_b = abs(b)
            terms.append(f"{sign_b}{val_b}x")
        if c != 0:
             sign_c = "+" if c > 0 else "-"
             val_c = abs(c)
             # If it's the last term, ensure space before + or -? 
             # Usually "39x^2+5x-14". No extra spaces around operators in standard compact latex.
        return f"{term1}{' '.join(terms)}"

    poly_str = make_poly_str(a_quad, b_quad, c_quad)
    
    question_text_latex = f"Solve for the integer value of $a + 2c$ where $(3x{'' if left_const==0 else '+'}{left_const})({N_val}x{'+' if right_const>0 else ''}{right_const}) = {poly_str}$."

    # Wait, need to handle signs in poly string correctly for LaTeX
    def format_poly_term(coeff):
        return f"{coeff}"
    
    term1 = f"{a_quad}x^2"
    term2 = ""
    if b_quad != 0:
         s_b = "+" if b_quad > 0 else "-"
         t_val = abs(b_quad)
         term2 += f"{s_b}{t_val}x "
         
    term3 = ""
    if c_quad != 0:
        s_c = "+" if c_quad > 0 else "-"
        t_val = abs(c_quad)
        # Remove trailing space before adding last term logic implicitly handled by join or just string concat? 
        # Better to build list.
        
    poly_parts = [f"{a_quad}x^2"]
    if b_quad != 0:
         s_b = "+" if b_quad > 0 else "-"
         t_val = abs(b_quad)
         poly_parts.append(f"{s_b}{t_val}x")
         
    if c_quad != 0:
        s_c = "+" if c_quad > 0 else "-"
        t_val = abs(c_quad)
        # If b was present, we need space? 
        # Actually standard latex spacing is handled by user or simple string. Let's just use + and - signs directly with values.
        
    final_poly_parts = []
    if a_quad != 0: final_poly_parts.append(f"{a_quad}x^2")
    if b_quad != 0: 
        sign_b = "+" if b_quad > 0 else "-"
        val_b = abs(b_quad)
        final_poly_parts.append(f"{sign_b}{val_b}x")
        
    if c_quad != 0:
         # If we have x term, add space? No, usually "39x^2+5x-14". 
         sign_c = "+" if c_quad > 0 else "-"
         val_c = abs(c_quad)
         final_poly_parts.append(f"{sign_c}{val_c}")

    # Reconstruct properly:
    parts = []
    if a_quad != 0: parts.append(f"{a_quad}x^2")
    if b_quad != 0: 
        sign_b = "+" if b_quad > 0 else "-"
        val_b = abs(b_quad)
        parts.append(f"{sign_b}{val_b}x")
        
    if c_quad != 0:
         # If previous part exists, we need to ensure correct spacing? 
         # Actually just appending is fine for latex math mode usually.
         sign_c = "+" if c_quad > 0 else "-"
         val_c = abs(c_quad)
         parts.append(f"{sign_c}{val_c}")

    poly_str_final = "".join(parts)

    question_text_latex = f"Given the polynomial equation $(3x{'' if left_const==0 else '+'}{left_const})({N_val}x{'+' if right_const>0 else ''}{right_const}) = {poly_str_final}$, solve for the integer value of $a + 2c$."

    # Oracle payload must exactly equal frozen sampled parameters
    oracle_payload = frozen_params
    
    return {
        "question_text": question_text_latex,
        "correct_answer": correct_answer_val,
        "oracle_payload": oracle_payload
    }