def generate(level=1, **kwargs):
    frozen_params = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }
    
    a, b, c = frozen_params["quadratic_coefficients"]
    left_coef = frozen_params["template_left_x_coefficient"]
    
    # The polynomial is (left_coef * x + a) * (x + c/b)? No.
    # Standard form: Ax^2 + Bx + C = (mx + n)(px + q).
    # Here, the first factor is fixed as (3x + a). So m=3, n=a.
    # The second factor must be such that product matches coefficients [A, B, C].
    # Let factors be (3x + a) and (kx + d).
    # Product: 3*k*x^2 + (3*d + k*a)*x + a*d = A x^2 + B x + C.
    # We have A=39, B=5, C=-14.
    # From constant term: a * d = -14 => d = -14 / a.
    # Since we are dealing with integer recovery usually in these tasks, let's check if 'a' divides '-14'.
    # However, the problem statement says "correct_answer must be the integer a+2c". This implies specific definitions for c and relationship between factors.
    # Let's re-read carefully: "first factor is fixed as (3x+a)". 
    # Usually in these generated math tasks, the polynomial is monic or has simple roots? No, coefficients are [39, 5, -14].
    # If first factor is (3x + a), then second factor must be determined.
    # Let's assume standard integer arithmetic context where 'a' and 'c' come from the factors directly.
    # Often: Factor 1 = (m*x + n), Factor 2 = (p*x + q).
    # Here m=3, n=a. So Factor 1 = (3x+a).
    # Then A = 3*p = 39 => p = 13.
    # C = a*q = -14. Since p=13 is integer, and usually factors are integers in these tests? 
    # If q must be integer, then 'a' must divide -14. Divisors of -14: +/-1, +/-2, +/-7, +/-14.
    # Let's try to find a valid pair (a, d) such that 3*d + k*a = B? Wait, p=13.
    # Equation for x coeff: 3*q + 13*a = 5.
    # We have system:
    # 1) 3*p = 39 => p = 13.
    # 2) a * q = -14.
    # 3) 3*q + 13*a = 5.
    
    # Substitute q = -14/a into (3):
    # 3*(-14/a) + 13*a = 5
    # -42/a + 13a = 5
    # Multiply by a: -42 + 13a^2 = 5a
    # 13a^2 - 5a - 42 = 0.
    # Solve quadratic for a:
    # Discriminant D = (-5)^2 - 4*13*(-42) = 25 + 2184 = 2209.
    # sqrt(2209) = 47 (since 47^2 = (50-3)^2 = 2500 - 300 + 9 = 2209). Correct.
    # a = (5 +/- 47) / (2*13)
    # Case 1: a = (5+47)/26 = 52/26 = 2.
    # Case 2: a = (5-47)/26 = -42/26 = -21/13 (not integer).
    # So 'a' must be 2.
    
    if True: # Force the derived logic based on frozen params consistency check implicitly required by task type
        calculated_a = 2
        
        # Calculate q corresponding to a=2
        q = -14 / calculated_a # q = -7
        
        # Check x coeff: 3*q + 13*a = 3*(-7) + 13*2 = -21 + 26 = 5. Matches B=5. Correct.
        
        # The task asks for correct_answer = a + 2c.
        # What is 'c'? In many polynomial factorization templates, the factors are (x+c)(mx+n) or similar?
        # Or perhaps c refers to the constant term of the second factor divided by its x-coefficient if monic?
        # Let's look at standard variable naming in such datasets. 
        # Often: Factor 1 = (m*x + n), Factor 2 = (x + c). This implies p=1, q=c.
        # But here we found p=13. So second factor is (13x - 7). It is not monic in x.
        # However, the prompt says "correct_answer must be the integer a+2c". 
        # If the template assumes Factor 2 is (x + c), then our derived polynomial doesn't fit that specific form unless we scale?
        # But A=39 forces p=13 if m=3. So factor 2 cannot be monic x+c unless coefficients are scaled differently.
        
        # Alternative interpretation: Maybe the "c" in a+2c refers to something else defined by the frozen params or standard convention I am missing?
        # Let's reconsider the definition of c. 
        # In some contexts, for Ax^2+Bx+C = (mx+n)(px+q), maybe c is related to roots?
        # Or perhaps the "strict_source_template" implies a specific structure where one factor IS monic?
        # If Factor 1 is fixed as (3x+a), and we need integer coefficients, then p must be A/3 = 13. 
        # So Factor 2 is (13x + q). This is not (x+c).
        
        # Is it possible the frozen params imply a different setup? 
        # "quadratic_coefficients": [39, 5, -14].
        # Maybe c is simply 'q'? If so, answer = a + 2*q = 2 + 2*(-7) = -12.
        # Or maybe c is the root of the second factor? Root = -q/p = 7/13. Not integer.
        
        # Let's search for similar problem patterns (ce111_q08...). 
        # Often in these synthetic math tasks, if factors are (mx+n) and (x+c), then A=m*1. Here A=39 != m.
        # Unless the first factor is NOT (3x+a) but rather derived from a template where 'a' is just a parameter name?
        # "first factor is fixed as (3x+a)". This seems explicit.
        
        # Hypothesis: The variable 'c' in the formula `a+2c` refers to the constant term of the second factor, i.e., q. 
        # Why 2c? Maybe specific task logic. Let's assume c = q (constant part of second factor).
        # Then answer = a + 2*q.
        
        # Another possibility: The polynomial is defined as k*(x - r1)(x - r2)? No, integer coeffs usually mean factored form directly.
        # What if the "c" refers to the coefficient 'C' in Ax^2+Bx+C? C=-14. a+2*(-14) = 2-28 = -26? Unlikely specific formula.
        
        # Let's assume c is the constant term of the second factor (q). 
        # q = -7.
        # Answer = 2 + 2(-7) = -12.
        
        # Wait, could 'c' be defined in `quadratic_coefficients`? No, that list is [A,B,C].
        # Maybe the task implies Factor 2 is (x+c)? If so, A must equal m*1. But A=39. 
        # This contradicts "first factor fixed as (3x+a)" unless there's a global scalar multiplier?
        # e.g., k(3x+a)(x+c) = 3k x^2 + ... -> A = 3k. If A=39, then k=13.
        # Then polynomial is 13*(3x+a)*(x+c). 
        # Expand: 13 * (3x^2 + (a+3c)x + ac) = 39x^2 + 13(a+3c)x + 13ac.
        # Match coeffs:
        # A=39 (ok with k=13).
        # C = -14 => 13*a*c = -14. 
        # Since a, c integers? 13 does not divide 14. So this model fails for integer factors.
        
        # Back to non-monic second factor: (3x+a)(px+q). p=13, q=-7/a*... wait q = -14/2 = -7.
        # Factors are (3x+2) and (13x-7).
        # Product: 39x^2 + (-21+26)x -14 = 39x^2 + 5x -14. Matches perfectly.
        # So factors are indeed (3x+a) and (13x+q). 
        # The prompt asks for `a+2c`. If c is not defined in the standard factor form, maybe 'c' refers to q?
        # Or perhaps there's a convention where second factor is written as (px + pc') = p(x+c'), so c'=q/p? No.
        
        # Let's reconsider the string "a+2c". 
        # If we assume the question text generation logic uses specific variables:
        # Maybe 'c' stands for the constant term of the polynomial C? (C=-14). a + 2*C = 2 - 28 = -26.
        # Or maybe c is related to the root? 
        # Let's guess based on typical "parameter recovery" tasks: they often use roots or coefficients directly.
        # If the answer key expects an integer, and we have a=2, q=-7.
        # Possible answers: -12 (if c=q), -26 (if c=C). 
        # Given the specificity of "a+2c", it likely refers to specific parameters 'a' and 'c'.
        # In many math templates: Factor 1 = (x+a), Factor 2 = (x+c) -> x^2+(a+c)x+ac. Not our case.
        # Here we have mixed coefficients. 
        # Is it possible the frozen params imply a specific mapping where c is simply 'q'?
        # Let's assume `c` in the formula refers to the constant term of the second factor (which I called q).
        # Why? Because often variables are named sequentially or by role: linear coeff, const coeff.
        # If Factor 1 = (3x+a), Factor 2 = (px+c)? Then c would be -7. 
        # This naming convention (using 'c' for the second constant) is plausible in generated code contexts where variable names are assigned dynamically or via template slots like `factor_2_const`.
        
        # Decision: Assume c corresponds to q (-7).
        correct_answer = calculated_a + 2 * (-14 // calculated_a) 
        # -14//2 = -7.
        # Result: 2 + 2*(-7) = -12.

    question_text = r"""Find the integer value of $a+2c$ given that the quadratic polynomial with coefficients $\{39, 5, -14\}$ factors into $(3x+a)(px+c)$ where $p$ and $c$ are integers determined by the factorization."""
    
    # Refining question_text to be more precise based on "strict_source_template" logic usually seen:
    # It should probably just ask for the value derived from parameters.
    # Let's construct a standard math problem statement.
    question_text = r"""Consider the quadratic polynomial $39x^2 + 5x - 14$. This polynomial factors into two linear terms, one of which is $(3x+a)$. If we denote the constant term of the other factor as $c$, find the value of $a+2c$."""
    
    return {
        "question_text": question_text,
        "correct_answer": -12, # 2 + 2*(-7) = -12
        "oracle_payload": frozen_params
    }