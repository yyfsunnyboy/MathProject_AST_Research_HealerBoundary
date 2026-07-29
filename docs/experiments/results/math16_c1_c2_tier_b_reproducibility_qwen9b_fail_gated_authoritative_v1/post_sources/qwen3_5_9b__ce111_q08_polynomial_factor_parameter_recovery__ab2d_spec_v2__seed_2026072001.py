# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification.
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    # Extract coefficients: ax^2 + bx + c -> coeffs[0]=a, coeffs[1]=b, coeffs[2]=c
    a_quad = frozen_params["quadratic_coefficients"][0]  # 39
    b_quad = frozen_params["quadratic_coefficients"][1]  # 5
    c_quad = frozen_params["quadratic_coefficients"][2]  # -14

    # Template: (template_left_x_coefficient * x + a) * (b_factor * x + c)
    left_x_coef = frozen_params["template_left_x_coefficient"]  # 3
    
    # We need to find integers 'a' and 'c' such that:
    # (left_x_coef * x + a) * (b_factor * x + c) expands to the quadratic.
    # Expansion: left_x_coef*b_factor*x^2 + (left_x_coef*c + b_factor*a)*x + a*c
    
    # Let L = left_x_coef, B = unknown integer factor for second term's x coefficient? 
    # Wait, standard factoring of Ax^2+Bx+C into (Lx+a)(Mx+c) where LM=A.
    # Here A=39. Factors of 39: (1,39), (3,13).
    # Template says first factor is fixed as (3x + a). So L=3.
    # Therefore M must be 39/3 = 13.
    
    left_x_coef_val = frozen_params["template_left_x_coefficient"]
    right_x_coef_val = a_quad // left_x_coef_val
    
    # Now solve for 'a' and 'c':
    # Constant term: a * c = C (which is -14)
    # Linear term coefficient: left_x_coef*c + right_x_coef*a = B (which is 5)
    
    # System of equations:
    # 3c + 13a = 5
    # ac = -14
    
    # From first eq: c = (5 - 13a) / 3
    # Substitute into second: a * ((5 - 13a)/3) = -14
    # => a(5 - 13a) = -42
    # => 5a - 13a^2 = -42
    # => 13a^2 - 5a - 42 = 0
    
    import math

    A_eq = 13
    B_eq = -5
    C_eq = -42
    
    discriminant = (B_eq**2) - 4*A_eq*C_eq
    sqrt_discriminant = int(math.isqrt(discriminant))
    
    if sqrt_discriminant * sqrt_discriminant != discriminant:
        # Should not happen with valid inputs, but safety check
        raise ValueError("Discriminant is not a perfect square")

    solutions_a = []
    for sign in [1, -1]:
        num = (-B_eq + (sign * sqrt_discriminant)) / 2.0
        if abs(num % A_eq) < 1e-9: # Check divisibility roughly or exact int check later
             val_a = int(round(num / A_eq)) 
             solutions_a.append(val_a)

    valid_as = []
    for candidate_a in set(solutions_a):
        c_val = (5 - 13 * candidate_a) // 3
        if left_x_coef_val * c_val + right_x_coef_val * candidate_a == b_quad:
            # Verify product ac equals constant term just to be sure, though linear eq ensures it given integer constraints usually.
             if candidate_a * c_val == c_quad:
                 valid_as.append(candidate_a)

    # The problem implies a unique solution or specific recovery logic. 
    # Given the quadratic nature and integer coefficients, there should be one valid pair fitting the template structure.
    
    final_a = None
    for val in valid_as:
        calc_c = (b_quad - left_x_coef_val * val) // right_x_coef_val
        if calc_c == c_quad: # Double check consistency with derived C from ac=constant? 
            # Actually, the system 3c+13a=5 and ac=-14 defines unique integers.
            pass
        
    # Let's just solve for 'a' directly using integer search since coefficients are small or use quadratic formula result precisely.
    # Roots of 13x^2 - 5x - 42 = 0: x = (5 +/- sqrt(25 + 2184)) / 26 = (5 +/- 47) / 26
    # Root 1: (5+47)/26 = 52/26 = 2. So a=2.
    # Check c: 3c + 13(2) = 5 => 3c = -21 => c = -7. 
    # Product ac = 2 * (-7) = -14. Matches C_quad. Correct.
    
    recovered_a = 2
    recovered_c = (b_quad - left_x_coef_val * recovered_a) // right_x_coef_val
    
    # The task asks for correct_answer to be the integer a + 2c.
    final_correct_answer = recovered_a + 2 * recovered_c

    # Construct LaTeX question text using native string formatting and simple math representation, 
    # avoiding external domain APIs as per "Use native Python only" rule in Task Guardrails section override?
    # Wait, the prompt says: "Do not use a Domain API." but also provides `PolynomialOps.format_latex` signature.
    # However, under "Task Guardrails": "Solve quadratic factoring using native integer arithmetic... Use native Python only; do not use a Domain API."
    # This is contradictory if I must format LaTeX. 
    # Re-reading: "API Signature Cards" section says `PolynomialOps.format_latex` exists but imports from domain library which might be forbidden by "Do not import, reference, or call any domain APIs".
    # The instruction "Use native Python only; do not use a Domain API." is in the specific Task Guardrails block. 
    # I will construct LaTeX manually using f-strings to ensure compliance with "native Python only" and avoiding imports of external libraries like `core.prompts.domain_function_library`.

    left_term = f"{left_x_coef_val}x + {recovered_a}"
    right_term = f"{right_x_coef_val}x + {recovered_c}"
    
    # Construct the polynomial expression: (3x+2)(13x-7) -> 39x^2 + ... 
    question_text = r"Given the quadratic $P(x)$ with coefficients \texttt{[39, 5, -14]}, factor it into two linear terms $(\mathbf{L}x + a)(\mathbf{R}x + c)$. The first term is fixed as $\left(3x + a\right)$. Determine the integer value of $a + 2c$."

    # Ensure oracle_payload matches frozen_params exactly
    return {
        "question_text": question_text,
        "correct_answer": final_correct_answer,
        "oracle_payload": frozen_params
    }