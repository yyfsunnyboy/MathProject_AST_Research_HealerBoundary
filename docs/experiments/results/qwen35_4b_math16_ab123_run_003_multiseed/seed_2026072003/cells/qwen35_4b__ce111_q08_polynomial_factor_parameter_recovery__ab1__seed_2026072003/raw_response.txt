def generate(level=1, **kwargs):
    from math import gcd
    
    # Frozen sampled parameters as per specification
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    a, b, c = quadratic_coefficients[0], quadratic_coefficients[1], quadratic_coefficients[2]
    
    # Construct the polynomial P(x) = (3x + a)(bx^2 + cx + d)? 
    # Wait, the task says "factor_order_policy is strict_source_template: first factor is fixed as (3x+a)".
    # The correct_answer must be the integer a+2c. This implies there's a specific structure where the constant term or linear term relates to this sum.
    # Usually in these challenges, we have P(x) = L1 * Q(x). If answer is a + 2*c, it suggests d (the constant of quadratic part) might be related to c? 
    # Or perhaps the polynomial is defined such that one root or evaluation yields a+2c.
    # Let's assume the standard form for this specific challenge type: P(x) = (3x+a)(bx^2 + cx + d).
    # If correct_answer = a + 2*c, and we need to find 'a', it implies we are solving for parameters in the factorization.
    # However, since frozen params provide coefficients [39, 5, -14] which likely correspond to (b, c, d) or similar? 
    # Let's re-read carefully: "quadratic_coefficients": [39, 5, -14]. These are the coeffs of x^2 + ...? Or just coefficients.
    # Usually quadratic is Ax^2+Bx+C. Here we have three numbers. Likely b=39, c=5, d=-14 or similar order. 
    # Given "correct_answer must be a+2c", if the answer depends on finding 'a', then 'a' comes from solving P(x)=0?
    # Actually, looking at typical patterns for this specific problem ID (ce111_q08...), often the polynomial is given as:
    # P(x) = 39x^2 + 5x - 14. We need to factor it into (3x+a)(bx+c)? No, that doesn't fit dimensions well unless degrees are different.
    
    # Let's assume the quadratic coefficients provided [39, 5, -14] correspond to a polynomial Q(x) = 39x^2 + 5x - 14? 
    # Or maybe they define the factors directly? "first factor is fixed as (3x+a)".
    # If P(x) = (3x+a)(bx+c), expanding gives 3b x^2 + ...
    # Let's try to match [39, 5, -14] with b=39. Then we need a and c such that:
    # Coeff of x is ac + ab? No. (3x+a)(bx+c) = 3b x^2 + (3c+ab)x + ac.
    # If coeffs are [A, B, C] for Ax^2+Bx+C. 
    # Maybe the "quadratic_coefficients" refer to the coefficients of the quadratic factor itself? i.e., bx^2+cx+d = 39x^2+5x-14?
    # Then P(x) = (3x+a)(39x^2+5x-14). 
    # Correct answer is a + 2*c. Here c=5. So ans = a + 10. We need to find 'a'.
    # But how do we determine 'a'? Is it derived from the constant term of P(x)?
    # Constant term of P(x) would be -14 * a. 
    # Often in these problems, there is an implicit constraint or the polynomial given IS (3x+a)(...) and we need to recover a such that...?
    # Wait, if the parameters are "frozen sampled", maybe 'a' is fixed by some hidden rule related to integer factorization properties not fully visible here, OR 
    # perhaps the problem implies P(x) has an integer root or specific property.
    
    # Alternative interpretation: The polynomial IS defined as (3x+a)(bx^2+cx+d). 
    # And we are given coefficients [b, c, d] = [39, 5, -14]. 
    # We need to find 'a'. Is there enough info?
    # Maybe the "correct_answer" being a+2c implies that for some reason (like evaluating at x=-something or root finding), we get this.
    # Actually, looking at similar challenges: Often P(x) is constructed such that one factor is linear and the other quadratic. 
    # If no further constraints on 'a' are given in frozen params, maybe 'a' makes the constant term of P(x) satisfy a specific condition? 
    # Or perhaps I should assume 'a' is determined by making the product have integer coefficients (which it always does if a,b,c,d integers).
    
    # Let's reconsider the "correct_answer" formula: `a + 2*c`. 
    # If c=5, answer = a+10. We need to output this value. This means we MUST know 'a'.
    # Is it possible that P(x) is monic? No, leading coeff would be 3*39=117.
    # Maybe the polynomial provided in kwargs (if any) or implied by context defines `a`. 
    # Since I cannot see input data beyond frozen params here, and this is a generation task for a specific test case...
    # Hypothesis: In many of these "parameter recovery" tasks, there's an implicit assumption that the linear factor corresponds to a root found via rational root theorem on a monic-like structure or similar. 
    # BUT, without explicit P(x) definition in frozen params (only coeffs), maybe the polynomial IS just 39x^2 + 5x - 14 and we are factoring IT?
    # If Q = 39x^2 + 5x - 14. Can it be factored into rational terms? 
    # Discriminant D = b^2 - 4ac = 5^2 - 4*39*(-14) = 25 + 2184 = 2209. sqrt(2209) = 47.
    # Roots are (-5 +/- 47) / (2*39). 
    # Root 1: (42)/78 = 2/13 -> Factor (13x - 2)? No, we need integer factorization usually.
    # Let's check factors of 39 and -14 with sum/diff related to roots?
    # If root is 2/13, then x=2/13 => 13x-2=0. Factor (13x-2). 
    # Other factor: (-5+47)/(78) = 42/78 = -(-2)/? No.
    # Let's calculate the other root properly: (-5 - 47) / 78 = -52 / 78 = -26/39 = -2/3. 
    # So factors are (13x-2)(3x+2). Product: 39x^2 + 26x - 6x - 4 = 39x^2 + 20x - 4. Doesn't match [5, ...].
    
    # Let's re-evaluate the "quadratic_coefficients" meaning. 
    # Maybe they are coefficients of (bx+c) and something else? No, length is 3. Quadratic has 3 coeffs.
    # So Q(x) = 39x^2 + 5x - 14 seems correct for the quadratic part.
    # Why would `a` be recoverable then? 
    # Perhaps the "strict_source_template" implies a specific form where `a` is chosen to make P(x) have integer roots or satisfy some other property mentioned in the original challenge (which I don't see).
    
    # Wait, could it be that the polynomial IS defined as `(3x+a)(bx^2+cx+d)` and we are GIVEN the expanded coefficients? 
    # No, frozen params only give `[39, 5, -14]`. That's exactly 3 numbers. Fits a quadratic `Ax^2+Bx+C`.
    # If P(x) = (3x+a)(bx+c), then expansion is `3b x^2 + ...` 
    # Maybe the provided coefficients ARE the expanded polynomial? i.e., P(x) = 39x^2 + 5x - 14.
    # And we need to find `a` such that one of its factors is `(3x+a)`? 
    # If so, then (3x+a) must be a factor of 39x^2+5x-14 over integers/rationals.
    # We found roots were x = 2/13 and x = -2/3 earlier with discriminant calc... wait my manual factoring was messy. 
    # Let's redo: P(x) = 39x^2 + 5x - 14.
    # We need integer factors? Or rational factor (3x+a)? a must be such that `a/(-3)` is the root. So x = -a/3. 
    # Since roots are rational, let's check if any root has denominator dividing by 3 to give an integer 'a'.
    # Roots: (-5 ± sqrt(2209)) / (78) = (-5 ± 47)/78.
    # r1 = 42/78 = 7/13. x = -a/3 => a = -3x = -21/13 -> Not integer? 
    # Wait, if factor is (3x+a), then root is -a/3. 
    # If r1 = 7/13, then -a/3 = 7/13 => a = -21/13. Not nice.
    # If r2 = -52/78 = -26/39 = -2/3. Then -a/3 = -2/3 => a=2. 
    # Ah! So if the factor is (3x+2), then root is x=-2/3. 
    # Does 39x^2 + 5x - 14 have root -2/3?
    # P(-2/3) = 39*(4/9) + 5*(-2/3) - 14 = (78*2)/6 ? No. 
    # 39 * 4 / 9 = 156/9 = 52/3.
    # 5 * (-2/3) = -10/3.
    # Sum: 52/3 - 10/3 - 14 = 42/3 - 14 = 14 - 14 = 0. 
    # YES! So (3x+2) is a factor of 39x^2 + 5x - 14.
    # Therefore, `a` must be **2**.
    
    # Now we can compute the answer: correct_answer = a + 2*c.
    # Given c from [39, 5, -14] is likely the middle term (linear coeff) -> 5? 
    # Wait, standard quadratic coefficients for Ax^2+Bx+C are A=39, B=5, C=-14. So b_coeff=5, which corresponds to `c` in my previous notation where I assumed Q(x)=bx^2+cx+d?
    # The prompt says "quadratic_coefficients": [39, 5, -14]. 
    # Usually order is high-to-low degree: x^2, x^0. So A=39, B=5, C=-14.
    # My derivation used c (linear coeff) = 5 in the formula `a+2c`. 
    # If "c" refers to the coefficient of x in the quadratic part, then c=5.
    # Answer = a + 2*5 = 2 + 10 = 12.
    
    # Let's double check if 'c' could be -14? Unlikely for linear term. 
    # So:
    # factor_order_policy -> strict_source_template (first factor fixed as 3x+a)
    # quadratic_coefficients -> [39, 5, -14] implies P(x) = 39x^2 + 5x - 14 and the linear coeff is 5.
    # template_left_x_coefficient -> 3 (matches our factor derivation).
    # Recovered a = 2.
    # Correct answer integer = a + 2*c = 2 + 2*5 = 12.
    
    oracle_payload = {
        "factor_order_policy": factor_order_policy,
        "quadratic_coefficients": quadratic_coefficients,
        "template_left_x_coefficient": template_left_x_coefficient
    }
    
    a_val = 2
    
    # Construct Question Text with LaTeX
    question_text = r"""Find the integer $a$ such that $(3x+a)$ is a factor of the polynomial defined by coefficients $[39, 5, -14]$. Calculate the value $a + 2c$, where $c=5$."""

    correct_answer_str = str(a_val + 2 * quadratic_coefficients[1])
    
    return {
        "question_text": question_text,
        "correct_answer": int(correct_answer_str),
        "oracle_payload": oracle_payload
    }