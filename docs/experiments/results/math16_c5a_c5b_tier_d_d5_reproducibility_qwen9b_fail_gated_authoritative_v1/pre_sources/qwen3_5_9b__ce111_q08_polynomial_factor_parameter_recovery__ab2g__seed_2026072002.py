def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    # Extract coefficients from the list: ax^2 + bx + c -> a=39, b=5, c=-14
    a = frozen_params["quadratic_coefficients"][0]
    b = frozen_params["quadratic_coefficients"][1]
    c = frozen_params["quadratic_coefficients"][2]
    
    # The first factor is fixed as (ax + k). Based on standard integer root problems, we look for factors of a*c.
    # However, the prompt specifies "first factor is fixed as (3x+a)". This seems to be a template instruction where 'a' in the text refers to the constant term variable, but here it conflicts with coefficient 'a'.
    # Let's re-read carefully: "template_left_x_coefficient": 3. So first factor starts with (3x + ...).
    # The quadratic is likely constructed such that one root corresponds to this factor.
    # If the polynomial is P(x) = a*x^2 + b*x + c, and we force a factor of form (mx + n), then m must divide 'a'.
    # Here template_left_x_coefficient=3 divides 39? Yes (13*3). So one root x0 satisfies 3x0 + k = 0 => x0 = -k/3.
    # Then P(-k/3) = a*(k^2/9) - b*k/3 + c = 0 => ak^2 - 3bk + 9c = 0.
    # We need to find integer k such that this holds for given a,b,c? Or is the polynomial generated randomly and we just report parameters?
    # The task says "Frozen sampled parameters". This implies we use these specific numbers to construct the problem instance.
    # Usually in these recovery tasks, 'a' (the constant term of the factor) is an integer variable we solve for or it's part of a random seed not shown here but implied by coefficients? 
    # Wait, "correct_answer must be the integer a+2c". Here 'a' and 'c' likely refer to specific variables in the problem context (e.g., if factors are (3x+a) and (13x+c)).
    # Let's assume the factorization is P(x) = (mx + n)(px + q). 
    # Given a=39, b=5, c=-14. Discriminant D = 25 - 4*39*(-14) = 25 + 2184 = 2209 = 47^2.
    # Roots are (-5 +/- 47) / (2*39). 
    # Root 1: x1 = 42/78 = 7/13 -> Factor (13x - 7). Here m=13, n=-7.
    # Root 2: x2 = (-5-47)/78 = -52/78 = -2/3 -> Factor (3x + 2). Here m=3, n=2.
    # The template says "first factor is fixed as (3x+a)". This matches the second root found above where coefficient of x is 3 and constant term is a=2.
    # So in this context: 
    # Factor 1: (3x + a) -> here 'a' = 2.
    # Factor 2: (13x + c')? Wait, the prompt says "correct_answer must be the integer a+2c". This implies there are two variables named 'a' and 'c' in the answer formula context, distinct from polynomial coefficients A,B,C. 
    # Let's look at the variable names in `quadratic_coefficients`: [39, 5, -14]. These are usually A, B, C for Ax^2+Bx+C.
    # But the correct_answer is "a+2c". If 'a' and 'c' refer to the constant terms of the factors? 
    # Factor 1: (3x + a_const). From calculation above, factor is (3x+2), so a_const = 2.
    # Factor 2: (13x - 7). Let's call its constant term c_val = -7.
    # Then answer = a_const + 2*c_val = 2 + 2*(-7) = 2 - 14 = -12? 
    # Or maybe the polynomial is defined as (ax+b)(cx+d)? No, standard form Ax^2+Bx+C.
    # Let's reconsider the "a+2c" instruction. In many such datasets (like GSM8k or similar math tasks), 'a' and 'c' might be specific parameters of a linear function y=ax+c? 
    # However, given the strict constraint: "correct_answer must be the integer a+2c". And we have coefficients [39, 5, -14].
    # If we assume the factorization is (3x + k)(13x + m) = 39x^2 + ... 
    # We found factors: (3x + 2) and (13x - 7).
    # Let's try to interpret "a" as the constant term of the first factor (which is fixed x-coeff 3), so a=2.
    # And "c" might be related to the other parameter? Or maybe c is just the variable name for the second constant? 
    # If answer = a + 2c, and we need an integer result.
    # Is it possible the polynomial was generated as (3x+a)(13x+c)? Then expansion: 39x^2 + (3c+13a)x + ac.
    # We have B=5, C=-14. So ac = -14 and 3c+13a = 5.
    # From ac = -14, pairs for (a,c): (-1,14), (1,-14), (-2,7), (2,-7)...
    # Check 3c+13a=5: 
    # If a=-1, c=14 -> 3(14)+13(-1) = 42-13 = 29 != 5.
    # If a=1, c=-14 -> -42 + 13 = -29.
    # If a=-2, c=7 -> 21 - 26 = -5. Close but sign wrong? 
    # If a=2, c=-7 -> 3(-7) + 13(2) = -21 + 26 = 5. MATCH!
    # So the factors are indeed (3x+2) and (13x-7). Here 'a' in the factor expression is 2, and 'c' in the second factor is -7.
    # The question asks for "a + 2c" where a=2, c=-7? 
    # Result: 2 + 2(-7) = -12.
    # Wait, usually these tasks have positive answers or specific structures. Let's check if 'c' refers to the polynomial coefficient C (-14)? 
    # If answer = a (from factor) + 2*C_poly? 2 + 2*(-14) = -26.
    # Or maybe 'a' and 'c' are just placeholders for the constants found in factors: k1, k2.
    # Given "correct_answer must be the integer a+2c", and we identified variables named `a` (const of first factor) and `c` (const of second factor). 
    # Let's assume the question text defines parameters $a$ and $c$ as the constants in $(3x+a)$ and $(13x+c)$.
    # Then correct_answer = a + 2*c.
    
    # Constructing the problem string with LaTeX
    poly_str = f"{frozen_params['quadratic_coefficients'][0]}x^2 + {b}x + {c}"
    factor1_str = f"(3x+{a})" 
    factor2_str = f"(13x+{c_val})" # where c_val is the second constant term
    
    question_text = (f"Solve for $k$ such that if a quadratic polynomial $P(x) = {poly_str}$ "
                     f"is factored into $(3x+a)(13x+c)$, then find the value of $a + 2c$.")
    
    # Wait, I need to define 'a' and 'c' in the text clearly. 
    # Let's refine question_text:
    # "Consider the polynomial P(x) = {A}x^2 + {B}x + {C}. It factors as (3x+a)(13x+c). Find a+2c."
    
    A, B, C = frozen_params["quadratic_coefficients"]
    question_text = f"Consider the polynomial $P(x) = {A}x^2 + {B}x + {C}$ which factors as $(3x+a)(13x+c)$ for some integers $a$ and $c$. Find the value of $a+2c$."

    # Calculate correct answer
    a_val = 2
    c_val = -7
    correct_answer = a_val + 2 * c_val
    
    return {
        "question_text": question_text,
        "correct_answer": str(correct_answer),
        "oracle_payload": frozen_params
    }