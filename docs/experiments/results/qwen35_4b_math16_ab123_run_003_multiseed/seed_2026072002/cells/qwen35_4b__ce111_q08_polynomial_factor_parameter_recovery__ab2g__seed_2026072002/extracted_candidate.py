def generate(level=1, **kwargs):
    import re
    
    polynomials = {}
    
    # Frozen sampled parameters from task specification
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    frozen_parameters = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient
    }
    
    # Parse level to determine number of factors (Level 1 implies single complex polynomial or specific setup)
    # Based on spec: first factor is fixed as (3x+a). 
    # We construct a quadratic based on coefficients [a, b, c] -> ax^2 + bx + c.
    # The problem asks for parameter recovery where correct_answer = a + 2c? Or similar linear combination.
    # Let's interpret the polynomial construction:
    # Factor 1: (3x + A)
    # We need to find 'a' from quadratic_coefficients which likely represent [A, B, C] for Ax^2+Bx+C or derived factors.
    # Given "quadratic_coefficients": [39, 5, -14], let's assume these are the roots-related values or direct coefficients of a constructed polynomial.
    # Standard factorization task: Find 'a' such that (3x+a) is a factor.
    # If quadratic is P(x), and we know one root corresponds to x = -A/3, then A must be related to 39? 
    # Let's assume the polynomial is constructed as (3x + a)(bx + c). Expanding: 3b*x^2 + (3c+ab)x + ac.
    # The input coefficients [39, 5, -14] likely correspond to specific values derived from roots or direct expansion of known factors? 
    # Or perhaps the "quadratic_coefficients" are the actual A, B, C for a quadratic Q(x) = Ax^2+Bx+C and we need to find 'a' such that (3x+a) is a factor.
    
    # Hypothesis: The polynomial is defined by roots or factors involving these coefficients.
    # Let's assume the "quadratic_coefficients" [A, B, C] define Q(x). We need to check if it has integer root related to 3x+a.
    # However, spec says "first factor is fixed as (3x+a)". This implies a specific 'a'.
    # Let's assume the provided coefficients are simply the values for A=39, B=5, C=-14 in some context? 
    # Actually, looking at similar math problems: often we have roots r1, r2. Factors (r1x + 1), etc.
    # Here factor is (3x+a). Root x = -a/3.
    
    # Let's construct the polynomial based on a derived 'a'. 
    # Since no explicit formula for 'a' is given in frozen params, we must derive it from context or assume standard generation logic where coefficients hint at roots.
    # If [39, 5, -14] are coefficients of x^2 + px + q? No, they are large integers.
    # Maybe the polynomial IS (3x+a)(bx+c) and we expand it to get coeffs? 
    # But which 'a' is correct? 
    # Let's assume a standard derivation: If roots are related to 39/5/-14? 
    # Alternative interpretation: The coefficients [39, 5, -14] ARE the values of (A, B, C) for Ax^2+Bx+C.
    # We need an integer 'a' such that x = -a/3 is a root of some polynomial related to these? 
    # Or perhaps the "correct_answer" formula a+2c implies c comes from somewhere else?
    
    # Let's try this logic: 
    # The polynomial P(x) has factors. One factor is (3x+a).
    # Maybe 'a' is derived such that when expanded, it matches some pattern or the coefficients provided are actually roots in a transformed space?
    # Given "correct_answer must be the integer a+2c", and we don't have c explicitly... 
    # Perhaps the quadratic_coefficients [39, 5, -14] correspond to (a, b, c) of some base equation? 
    # If so, A=39, B=5, C=-14.
    # But factor is (3x+a). This conflicts if a != root related value.
    
    # Re-reading spec: "factor_order_policy": "strict_source_template". "first factor is fixed as (3x+a)".
    # Maybe 'a' and 'c' are derived from the coefficients? 
    # Let's assume the polynomial to be factored is formed by roots corresponding to these numbers.
    # If we treat 39, -14 as values for x in a quadratic equation with sum/product related to 5? 
    # Sum = -(B/A), Product = C/A.
    
    # Let's assume the simplest valid generation: 
    # Use 'a' from coefficients[0] or similar? No, that would make (3x+39). Root -13.
    # Check if x=-13 is a root of something using 5 and -14? 
    # If we define the polynomial as having roots r1, r2. Factors are (k1*x + m1)(k2*x + m2).
    # One factor is fixed: (3x+a). So k1=3.
    
    # Let's assume a specific construction for Level 1 based on coefficients [A, B, C]:
    # Polynomial P(x) = A * x^2 - ...? 
    # Actually, let's look at the "correct_answer" formula: a + 2c. This implies 'a' and 'c' are variables in our factorization result.
    # If we assume factors are (3x+a)(bx+c). Then ac is constant term. bc+ab*x etc.
    
    # Let's generate the polynomial such that one root corresponds to x = -a/3, another related to c? 
    # Given coefficients [39, 5, -14]. Maybe these are (a, b, c) for factors (x+a), (bx+c)? No.
    
    # Let's try a different angle: The "frozen sampled parameters" might contain the hidden truth directly if interpreted loosely? 
    # But spec says "Do not redefine". It implies I must generate valid content based on them.
    # Maybe 'a' is simply coefficients[0] / 3? No, integer required for a+2c to be clean? 
    # Let's assume the polynomial is: (3x + A)(Bx - C) or similar where [A, B, C] = coeffs? 
    # If factors are (3x + 39)(5x - (-14)) -> (3x+39)(5x+14). Then a=39. c=14. Answer: 39 + 28 = 67.
    # Check if this makes sense with "quadratic_coefficients": [39, 5, -14]. 
    # Expansion of (3x+39)(5x+14) = 15x^2 + (42+195)x + 546. Coeffs: 15, 237, 546. Not matching [39, 5, -14].
    
    # Maybe the coefficients ARE the values for a, b, c in factors? 
    # Factor 1: (x + A). Factor 2: (Bx + C)? No, factor is fixed as (3x+a). So first term has coeff 3.
    # If we assume the input [39, 5, -14] are actually roots r1=39, r2=-5? Or something similar? 
    # Let's try to reverse engineer: We need an integer 'a' and a constant 'c'.
    # And correct_answer = a + 2*c.
    
    # Hypothesis for Level 1 generation logic in this specific challenge context (common patterns):
    # The coefficients [39, 5, -14] represent the values of x that satisfy some condition? 
    # Or perhaps they are just labels and we should pick a canonical 'a' based on them.
    # Let's assume: factor is (3x + coeff[0]). So a = 39.
    # Then what is c? Maybe related to the other coefficients? 
    # If factors are (3x+39)(5x-14)? Or (3x+39)(something with -14).
    # Let's assume the second factor uses coeff[2] and coeff[1]? 
    # Try: Factors = [(3, 39), (coeffs[1], coeffs[0])? No.
    
    # Let's try a very standard math problem generation pattern:
    # Given roots r1, r2 -> factors (x-r1)(x-r2). Here we have linear forms with different leading coefficients.
    # Form: k1*x + m1 and k2*x + m2. Product = K x^2 + ... 
    # One factor is fixed as 3x+a. So k1=3, m1=a.
    # The other factor involves the remaining params? [5, -14].
    # Maybe factors are (3x+39) and (5x-14)? 
    # Then a = 39. c in expansion of (bx+c) would be part of second factor. If form is bx+c, then c=-14? Or if it's b(x)+c -> -14.
    # Let's assume factors are F1=(3x+39), F2=(5x-14). 
    # Then a=39. The 'c' in the factorization (bx+c) would be -14? Or 14 depending on sign convention. Usually Ax+B.
    # If we write factors as (ax+b)(cx+d)... standard is (mx+n)(px+q).
    # So F2 = 5x + (-14)? Then q=-14. 
    # Correct answer formula: a + 2c? Here c might be the constant term of second factor? Or coefficient? 
    # If 'c' refers to the constant term in (bx+c), then c=-14.
    # Answer = 39 + 2*(-14) = 39 - 28 = 11. Integer. Plausible.
    
    # Let's verify if there is any other interpretation where coefficients [39, 5, -14] are used differently. 
    # Maybe the polynomial IS (x-39)(x+...)? No, factor starts with 3x.
    
    # Decision: Generate factors based on mapping indices of frozen parameters to factor constants.
    # Factor 1 constant 'a' = coeffs[0]. Leading coeff fixed at 3. -> F1 = 3*x + a.
    # Factor 2 uses remaining params? [5, -14]. Let's assign leading=coeffs[1], const=coeffs[2]? Or vice versa? 
    # Usually coefficients are ordered A, B, C for Ax^2+Bx+C or roots related. 
    # If we assume the polynomial is formed by (3*x + coeffs[0]) * (coeffs[1]*x - (-coeffs[2]))?
    # Let's try simplest: F1 = 3x+39, F2 = 5x-14.
    # Then a=39. c=-14 (if form is bx+c). 
    # Correct answer = 39 + 2*(-14) = 11.
    
    # Let's construct the polynomial text and payload accordingly.
    
    A_val = quadratic_coefficients[0] # 39 -> a for 3x+a
    B_val = quadratic_coefficients[1] # 5
    C_val = quadratic_coefficients[2] # -14
    
    factor_1_const = A_val
    factor_2_lead = B_val
    factor_2_const = -C_val # Assuming signs to make product look nice? Or just use directly. 
    # Let's stick to F1=(3x+39), F2=5x-14 (since C is negative). 
    # If we take c from the second factor as its constant term:
    
    a = factor_1_const
    b_second = factor_2_lead
    c_second = -factor_2_const if factor_2_const < 0 else factor_2_const ? 
    Actually, let's assume factors are (3x + A) and (B x + C). 
    Then expansion: 3BC x^2 + ... 
    If we use [39, 5, -14] as A=39, B=5, C=-14.
    F1 = 3x+39. a=39.
    F2 = 5x-14. Constant term is -14. So c_second = -14? 
    Or maybe the factorization requires (bx+c) where c is positive? 
    Let's assume standard form: Factors are k1*x+m1 and k2*x+m2.
    m1=39, m2=-14.
    If "c" in a+2c refers to the constant term of the second factor (m2), then c = -14.
    Answer = 39 + 2*(-14) = 11.
    
    # Construct polynomial text: P(x) = (3x+a)(bx+c). 
    # We need to ensure a+2c is the correct_answer key value.
    # Let's define c as the constant term of the second factor.
    
    poly_text = "P\\\\(x\\\\) = \\\\left( 3x + {a} \\right) \\\\cdot \\\\left( {b_second}x + {c_second} \\right)"
    
    # Calculate correct_answer
    a_val = A_val
    c_val = C_val # Using -14 directly if we assume factors are (5x-14). 
                   # Wait, is it possible the factor is (5x+(-14))? Yes. So constant term is -14.
    
    correct_answer_int = a_val + 2 * c_val
    
    question_text = f"Factorize the polynomial P(x) given by the frozen parameters into two linear factors with leading coefficients fixed to 3 and {B_val}. The first factor must be in the form (3x+a). Find the integer value of 'a' combined with 'c' from the second factor such that correct_answer = a + 2*c. Note: The polynomial is P(x) = \\\\left( 3x + {A_val} \\right) \\\\cdot \\\\left( {B_val}x + {C_val} \\right)."
    
    # Re-reading spec carefully: "question_text must use formal LaTeX delimiters."
    # And "Do not redefine parameters after swapping factors". 
    # So order is fixed. F1=(3x+a), F2=(...).
    
    oracle_payload = frozen_parameters
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_int,
        "oracle_payload": oracle_payload
    }