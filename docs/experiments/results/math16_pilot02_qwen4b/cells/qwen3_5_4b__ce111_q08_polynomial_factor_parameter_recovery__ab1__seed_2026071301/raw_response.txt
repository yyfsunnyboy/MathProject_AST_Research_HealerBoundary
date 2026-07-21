def generate(level=1, **kwargs):
    polynomials = []
    
    # Frozen sampled parameters from task specification
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    a = 20
    c = 7
    
    # Construct the polynomial based on frozen parameters and difficulty level 1
    # The problem implies recovering 'a' from factors (x+a) and another factor.
    # Given "correct_answer must be the integer a+2c", let's construct a scenario where this holds.
    
    # Let's assume the original polynomial is P(x).
    # If one factor is fixed as (3x + a), then we need to find 'a'.
    # The correct answer formula provided is a + 2*c = a + 14.
    
    # To make this solvable and consistent with "parameter recovery", let's define the polynomial explicitly using these constants.
    # Let P(x) = (3x + a) * Q(x).
    # We need to ensure that solving for 'a' yields an integer, and calculating a+2c gives the target answer.
    
    # Since we are generating content based on frozen parameters, let's fix:
    # Factor 1: (3*x + a) where a = 20 -> (3x + 20)
    # We need another factor Q(x). Let's choose Q(x) such that the resulting polynomial has integer coefficients.
    # Let Q(x) be linear for simplicity in level 1, say (x - c) or similar? 
    # Actually, usually these problems involve factoring a quadratic into two binomials.
    # If P(x) = (3x + 20)(x + k), expanding gives: 3x^2 + (3k+20)x + 20k.
    
    # However, the "correct_answer" is defined as `a + 2c`. 
    # With a=20 and c=7, answer = 20 + 14 = 34.
    # This suggests 'c' might be part of the polynomial structure or derived from it.
    
    # Let's construct P(x) such that factoring reveals (3x+20).
    # Maybe the other factor involves c? 
    # If we set Q(x) = x - 7, then roots are -20/3 and 7. Not integers for standard school problems usually unless specified otherwise.
    
    # Alternative interpretation: The polynomial is constructed such that 'a' is hidden in coefficients.
    # Let's define P(x) explicitly using the frozen parameters to ensure consistency.
    # We will create a quadratic equation where one root relates to -a/3 and another relates to something involving c? 
    # Or perhaps the "parameter recovery" task implies we are given coefficients of a polynomial that was formed by (x+a)(bx+c) or similar, but here factor_order_policy is strict_source_template meaning first factor IS fixed as (3x+a).
    
    # Let's assume the standard form: P(x) = (3x + a)(mx + n).
    # We need to pick m and n such that coefficients are nice integers.
    # If we want 'c' (which is 7) to be relevant, maybe one constant term involves c? 
    # Let's try Q(x) = x - (-2*c)? No.
    
    # Let's just define the polynomial directly using a=20 and some other integer k for simplicity, then verify if we can map 'c' into it logically or treat 'c' as an independent parameter given in frozen data that must appear in oracle_payload but maybe influences the question text generation logic implicitly?
    
    # Re-reading: "correct_answer must be the integer a+2c". 
    # This is likely the value of some variable x0 such that P(x0)=0 or similar, OR it's simply a derived answer for a specific sub-question.
    # Given the constraint to write ONLY Python source and no input/files/network:
    
    # Let's construct the question text around finding 'a' in (3x+a), then computing a+2c.
    # We need P(x) such that factoring gives (3x+20).
    # Let Q(x) = x + 14? Then constant term is -280. 
    # Or maybe the polynomial is: 39x^2 ... wait, quadratic_coefficients are [39, 5, -14]. These look like coefficients of a specific polynomial provided in the frozen data context (maybe from previous steps or as distractors?).
    
    # Actually, looking at "quadratic_coefficients": [39, 5, -14], this likely represents ax^2 + bx + c = 0.
    # But we also have a fixed factor (3x+a). 
    # If P(x) has roots related to the parameters...
    
    # Let's simplify: Generate a question where the polynomial is defined by coefficients that allow factoring into (3x+20)(something), and ask for 20 + 14.
    # To make it self-contained, let's define P(x) = (3x + 20)(x - (-7))? No, that makes constant term positive if signs match? 
    # Let's try: P(x) = (3x + 20)(x - k). Constant term is -20k.
    
    # Wait, the frozen parameters include "quadratic_coefficients": [39, 5, -14]. 
    # Could this be the polynomial we are factoring? 
    # If P(x) = 39x^2 + 5x - 14.
    # Let's check if (3x+20) is a factor of 39x^2 + 5x - 14.
    # Divide by (3x+20): 
    # 39x^2 / 3x = 13x.
    # 13x * (3x+20) = 39x^2 + 260x. Too big.
    
    # Maybe the coefficients [39, 5, -14] are NOT the polynomial to factor directly, but parameters used TO generate it? 
    # Or maybe they ARE the polynomial and my assumption about 'a' being 20 is wrong? 
    # But "factor_order_policy" says first factor IS (3x+a).
    
    # Let's reconsider: The task is `polynomial_factor_parameter_recovery`.
    # Frozen parameters are given. We must use them to generate the question and answer.
    # If we assume the polynomial provided by coefficients [39, 5, -14] IS the one being factored? 
    # Let's try finding factors of 39x^2 + 5x - 14.
    # Factors of 39: 1, 3, 13, 39. Factors of -14: ...
    # Try (3x+7)(13x-2) = 39x^2 -6x + 91x -14 = 39x^2 +85x -14. No.
    # Try (3x-?)(?). 
    # Maybe the polynomial is different and [39, 5, -14] are just extra frozen data for oracle_payload?
    
    # The instruction says: "oracle_payload must exactly equal the frozen sampled parameters."
    # So we don't need to derive anything from coefficients into the payload. We just echo them back in a dict structure if needed (but it's already provided as kwargs or global).
    
    # Focus on question_text and correct_answer.
    # Question: Factorize P(x) = ... such that one factor is (3x+a). Find a+2c.
    # We need to define P(x) consistently with 'a'=20, c=7? 
    # If we set P(x) = (3x + 20)(x - (-14/5))? No fractions preferred in simple tasks unless specified.
    
    # Let's create a synthetic polynomial that works perfectly with the given constants to ensure correctness without external validation logic running at runtime other than this generation function itself being deterministic based on frozen params.
    # Since I cannot run code here, I must hardcode the relationship or generate it logically within the thought process which is now part of the "source". 
    # But wait, `generate` runs in Python. It can compute things if needed? No, usually these tasks expect deterministic output based on frozen params without relying on external state that isn't passed.
    
    # Let's assume: a = 20, c = 7.
    # We need P(x) such that (3x+20) is a factor.
    # And the answer is 20 + 14 = 34.
    # Let's define P(x) = (3x + 20)(5x - ?). 
    # To make coefficients integers, let Q(x) be chosen such that expansion yields nice numbers.
    # How about we just state the polynomial in terms of a and c? No, question text must use formal LaTeX delimiters and likely explicit values or clear variables defined earlier. Since it's level 1, maybe explicit constants are better.
    
    # Let's define P(x) = (3x + 20)(x - (-7))? 
    # Expansion: 3x^2 + 95x? No. 3x*x=3x^2. 3x*-7=-21x. 20*x=20x. Sum x term is -x. Constant = -140.
    # P(x) = 3x^2 - x - 140. Factor: (3x+20)(x-7). 
    # Here a=20, c=-7? But frozen c is 7. 
    # Maybe the factor is (3x+a) and the other root involves c differently?
    
    # Let's try P(x) = (3x + 20)(x - (-14/5))? No.
    # How about we define the polynomial using a=20 and some k, then ask for a+2c where c is given as 7 in frozen params? 
    # The question text can reference 'a' found from factoring (3x+a), and then compute a + 2*c.
    
    # Let's construct P(x) = (3x + 20)(5x - ?). 
    # Actually, let's look at the coefficients [39, 5, -14] again. 
    # Is it possible the polynomial is: 39x^2 ... no we tried that.
    
    # Let's ignore the specific values in quadratic_coefficients for constructing P(x) and instead use them ONLY as part of oracle_payload (which must match frozen params). The task says "oracle_payload must exactly equal the frozen sampled parameters". It doesn't say they MUST be used to construct the polynomial, though that would be elegant. 
    # However, if I ignore them in construction, is it valid? Yes, as long as generate() returns correct_answer and oracle_payload correctly.
    
    # Plan:
    # 1. Set a = 20 (from frozen context or derived from level=1 default logic). Wait, 'a' isn't explicitly given as a number in the dict, but "factor_order_policy" implies structure. 
    # Actually, looking at similar tasks, usually there's an implicit mapping or we derive 'a' from the polynomial coefficients provided?
    # If I don't use [39, 5, -14] to build P(x), how do students know what a is? They would need to see it in the question. 
    # But if they see (3x+a) and no other info, 'a' is unknown.
    
    # Hypothesis: The polynomial IS defined by coefficients [39, 5, -14] but my previous check failed because I assumed integer roots? Or maybe factorization involves non-integers or different grouping? 
    # Let's re-check (3x+7)(13x-2) -> 85.
    # What about (3x+a)? If a=20, then we need P(x) divisible by (3x+20).
    # Maybe the polynomial is: P(x) = (39/3)x^2 ... no.
    
    # Let's assume 'a' and 'c' are derived from the frozen parameters in a specific way I might be missing, OR they are simply fixed values for this instance that we must know/use. 
    # Given "Frozen sampled parameters", these are constants of truth for this run.
    # So: factor_order_policy = strict_source_template -> Factor 1 is (3x+a).
    # We need to determine 'a'. Is it possible 'a' comes from the quadratic_coefficients? 
    # Maybe P(x) = x^2 + ... no, leading coeff of first factor is 3. So total degree must be at least 2 if second factor is linear.
    
    # Let's try a different angle: The "quadratic_coefficients" [39, 5, -14] might actually BE the coefficients of (x+a)(bx+c) expanded? 
    # If P(x) = x^2 + ... no leading coeff is not 1.
    
    # Okay, let's step back. The prompt asks to implement `generate`. It provides frozen parameters. I must return a dict with specific keys.
    # To be safe and deterministic:
    # - Use the provided constants directly if possible. 
    # - If 'a' is not explicitly given as an integer in the frozen params, but implied by "factor_order_policy", maybe it's 0? No, that makes (3x). Trivial factorization.
    # Maybe a=20 and c=7 are standard defaults for this specific problem ID `ce111_q08` if not overridden? 
    # The prompt says: Frozen sampled parameters include "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3.
    # It does NOT list 'a' or 'c' explicitly in the JSON snippet provided in the thought block description above? 
    # Wait, looking at the user prompt again: `{"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}`.
    # 'a' and 'c' are NOT in this dict! 
    # But the task says: "correct_answer must be the integer a+2c". And "first factor is fixed as (3x+a)".
    # This implies I need to derive or generate 'a'. 
    # How? Maybe from `quadratic_coefficients` [39, 5, -14]?
    # Let's try: P(x) = x^2 + bx + c? No.
    # What if the polynomial is constructed such that its coefficients match [39, 5, -14] after some transformation? 
    # Or maybe I should just pick arbitrary 'a' and 'c'? No, "parameter recovery" implies recovering them from data.
    
    # Let's assume the standard form for this problem type: P(x) = (x+a)(bx+c). But here factor is (3x+a), so P(x) = (3x+a)(mx+n). 
    # Expand: 3m x^2 + (3n+am)x + an.
    # We have coefficients [39, 5, -14]. Maybe these are the expanded coeffs?
    # Case A: Leading coeff is not normalized to 1 in the input list? List has 3 items -> ax^2+bx+c. So a=39, b=5, c=-14? 
    # If P(x) = 39x^2 + 5x - 14.
    # We need (3x+a) to be a factor.
    # Let's try synthetic division with root x = -a/3.
    # Value at x=-a/3: 39(a/3)^2 + 5(-a/3) - 14 = 0? 
    # 39*(a^2/9) - 5a/3 - 14 = 0
    # (13*a^2)/3 - 5a/3 - 14 = 0
    # Multiply by 3: 13a^2 - 5a - 42 = 0.
    # Solve for a: 
    # Discriminant D = (-5)^2 - 4*13*(-42) = 25 + 2184 = 2209.
    # sqrt(2209)? 47^2 = (50-3)^2 = 2500 - 300 + 9 = 2209. Yes, 47.
    # a = (5 +/- 47) / (2*13).
    # Option 1: (5+47)/26 = 52/26 = 2. So a=2? 
    # Option 2: (5-47)/26 = -42/26 = -21/13. Not integer.
    # If a=2, then factor is (3x+2).
    # Let's check if (3x+2) divides 39x^2 + 5x - 14.
    # Polynomial division: 
    # 39x^2 / 3x = 13x.
    # 13x * (3x+2) = 39x^2 + 26x.
    # Subtract from original: (5x - 14) - (26x) = -21x - 14.
    # Next term: -21x / 3x = -7.
    # -7 * (3x+2) = -21x - 14.
    # Remainder is 0! 
    # So P(x) = 39x^2 + 5x - 14 factors into (3x+2)(13x-7).
    
    # Now we have a=2 from the factor (3x+a).
    # We also need 'c'. The task says "correct_answer must be the integer a+2c". 
    # Where does c come from? In our expansion, the constant term was -14. 
    # Maybe c is related to 7 or -7? 
    # If we assume the second factor (mx+n) has n = -7? Or maybe c=7 is derived from |n|?
    # The frozen params have "quadratic_coefficients": [39, 5, -14]. This matches our P(x).
    # And 'c' in the answer formula a+2c. If we assume standard notation where factors are (x+a)(bx+c), but here it's (3x+a)... 
    # Perhaps c is simply half of the constant term? Or related to the other factor's constant?
    # In our case, second factor is (13x-7). Constant part is -7. Absolute value 7.
    # If we set c = 7 (positive magnitude), then answer = a + 2c = 2 + 14 = 16.
    # Does this make sense? 
    # The frozen params list "quadratic_coefficients" which matches our derived P(x). This confirms the polynomial is indeed 39x^2+5x-14.
    # And 'a' was recovered as 2 from (3x+a) factorization of that specific quadratic.
    # Now, what is c? The problem statement says "correct_answer must be the integer a+2c". 
    # It doesn't explicitly define how to get c in the spec text provided here, but typically in such problems involving parameters 'a' and 'c', they appear as constants in factors (x+a)(bx+c).
    # Our second factor is (13x-7). If we map this to standard form or if there's a convention that c=7? 
    # Given the frozen params don't list 'c', but the answer formula requires it, and 7 appears naturally as |constant term of second factor| / something?
    # Or maybe c is just 7 because in many contexts (like x^2+bx+c), c is the constant. Here we have two factors with constants a and -7. 
    # Let's assume c=7 based on symmetry or typical problem design where parameters are positive integers unless specified otherwise, OR derived from |constant term| of one factor?
    # Actually, if the original template was (3x+a)(bx+c), then constant terms would be ac = -14. 
    # If a=2 and c=-7, product is -14. Then answer = 2 + 2*(-7) = -12.
    # Or if c=7? Answer = 16.
    # Which one fits "parameter recovery"? Usually parameters are the values in the factors. 
    # If factor is (3x+2), a=2. Other factor (13x-7). Is it (bx+c) or (bx-c)? 
    # Standard form usually writes constants as they appear. So c=-7?
    # But "integer a+2c" might imply positive integers for simplicity in Level 1? 
    # Let's check if there is another factorization possibility with different 'a'? No, quadratic has unique factors over rationals (up to units).
    
    # Decision: I will assume c = -7 because it matches the actual constant term of the second linear factor derived from P(x)=39x^2+5x-14. 
    # However, often in these generated problems, 'c' might be defined as a positive parameter if the template was (bx-c). But without explicit instruction on sign convention for c beyond "a+2c", I need to make a choice that feels robust.
    # Wait, looking at the frozen params again: `quadratic_coefficients`: [39, 5, -14]. 
    # If we assume the standard form x^2 + bx + c doesn't apply directly due to leading coeff 39.
    # Let's reconsider the "parameter recovery" context. Often 'a' and 'c' refer to specific slots in a template like (x+a)(bx+c). 
    # Here factor is fixed as (3x+a). So we found a=2.
    # The other constant term is -7. If c represents that value, then c=-7. Answer = 2 + 2(-7) = -12.
    # But maybe the template was (3x-a)(bx-c)? No, spec says "(3x+a)". 
    # Let's try to infer if 'c' is meant to be positive. If I assume c=7, answer=16. 
    # Is there any hint in "quadratic_coefficients"? -14 suggests the product of constants is negative.
    # Without further constraints, both 12 and 16 are candidates depending on sign convention. 
    # However, usually parameter recovery problems aim for positive integers if possible? Or exact values from factors. 
    # Let's assume c = -7 (exact constant term). Answer = -12.
    # Wait, could 'c' be related to the coefficient 5 or something else? Unlikely.
    
    # Alternative: Maybe I should just output a=2 and calculate based on what makes sense for "Level 1". 
    # Let's assume c is simply the constant term of the second factor if we write it as (bx+c). So -7.
    # But wait, maybe the question asks for |a| + 2|c|? No, says "integer a+2c".
    
    # Let's try to verify if there's any other interpretation where c is positive and obvious. 
    # If P(x) = (3x-2)(13x+7)? Then constant term would be -4*... no 39x^2 + ... 
    # Our factorization was unique: (3x+2)(13x-7).
    # So a=2. Constant of second factor is -7. If we call this c, then c=-7.
    # Resulting answer = 2 + 2(-7) = -12.
    
    # However, consider the possibility that 'c' in "a+2c" refers to a parameter from a different template context not fully visible but implied by frozen params? 
    # No, we must use what's given. The only numbers are 39, 5, -14 and derived factors.
    
    # Let's go with c = -7. It is mathematically precise based on the factorization of [39, 5, -14].
    # Correct Answer: -12.
    
    # Wait, what if 'c' in "a+2c" refers to a parameter that was supposed to be positive? 
    # Let's check if there is an alternative reading where c=7 and the factor was (3x+a)(bx-c)? 
    # If the template assumed subtraction for both or something... but spec says "(3x+a)".
    
    # Okay, I will proceed with:
    # a = 2
    # c = -7 (from constant term of second factor)
    # answer = 2 + 2*(-7) = -12.
    
    # Wait, is it possible the "quadratic_coefficients" [39, 5, -14] are NOT for P(x)? 
    # What if they are just noise? No, in these tasks usually all frozen params are relevant.
    # The fact that [39, 5, -14] perfectly factors into (3x+2)(13x-7) is too coincidental to be random. This confirms the polynomial and values of a=2 and c=-7 (or related).
    
    # Final check on 'c': In many algebraic contexts involving ax^2+bx+c, c is the constant term. Here we have two factors with constants 2 and -7. 
    # If the "parameter recovery" implies recovering parameters of a form like (3x+a)(mx+n), then n=-7.
    # The formula asks for a+2c. It uses 'c'. Is c=n? Yes, likely.
    
    # One edge case: Maybe the problem expects positive integers and I should take absolute value? 
    # "integer a+2c" doesn't specify sign constraints on result, just that it's an integer. -12 is an integer.
    
    # Let's write the code to generate this deterministically.

    import math
    
    frozen_params = {
        "factor_order_policy": kwargs.get("frozen_factor_order", "strict_source_template"),
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }
    
    # Re-derive a and c from the polynomial coefficients to ensure consistency with frozen data usage.
    coeffs = kwargs.get("frozen_coeffs", [39, 5, -14])
    a_val = None
    
    if len(coeffs) == 3:
        A2, B1, C_const = coeffs # Ax^2 + Bx + C
        
        # Solve for 'a' in (A*x + a)(mx+n)? No, factor is (3x+a). So leading term of first factor is 3.
        # We assume P(x) = (3x+a)*(m x + n) = 3m x^2 + (3n+am)x + an.
        # Match with A2*x^2 + B1*x + C_const.
        # 3*m = A2 => m = A2/3 = 39/3 = 13.
        # a*n = C_const => n = C_const/a.
        # 3n + am = B1 => 3(C_const/a) + a*(A2/3) = B1
        
        # We know m=13, A2=39. 
        # Equation: 3*C_const/a + (a*39)/3 = 5
        # Multiply by 3a: 9*C_const + 39*a^2 = 15a
        # 39a^2 - 15a + 9*(-14) = 0 ? No, C_const is -14.
        # 39a^2 - 15a - 126 = 0? 
        # Wait previous derivation: 13a^2 - 5a - 42 = 0 was for P(x)=39x^2+5x-14 with factor (3x+a).
        # Let's re-solve that quadratic carefully.
        # Roots of 13a^2 - 5a - 42 = 0 were a=2 and a=-21/13.
        # Integer solution a=2 is the only valid one for "parameter recovery" (usually integers).
        
        if abs(13*a_val**2 - 5*a_val + C_const * something) == 0: 
            pass
            
    # Since I am writing Python code, I can compute this directly inside generate() to be safe.
    
    A2 = coeffs[0]
    B1 = coeffs[1]
    C_const = coeffs[2]
    
    # Solve for a in (3x+a)(mx+n) where m=A2/3 and an=C_const, 3n+am=B1
    # From earlier: 13a^2 - 5a + (-42)? 
    # Let's re-derive the equation symbolically to be sure.
    # P(x) = (3x+a)(mx+n) = 3m x^2 + (3n+am)x + an
    # Coeffs: [39, 5, -14] -> 3m=39 => m=13. a*n=-14. 3n+13a=5.
    # From n = -14/a: 3(-14/a) + 13a = 5
    # -42/a + 13a = 5
    # Multiply by a: -42 + 13a^2 = 5a
    # 13a^2 - 5a - 42 = 0. Correct.
    
    import cmath
    
    discriminant = (-B1/coeffs[0]/(A2//3) if A2%3==0 else ... ) 
    # Simpler: Use the derived quadratic equation for a directly based on coeffs.
    # Equation: (A2/3)*a^2 - B1*a + C_const = 0 ? No, let's re-verify signs.
    # From n = C/a and 3n+am=B => 3C/(a) + am*B_coeff? 
    # Wait m=A2/3. So 3(C/a) + a*(A2/3) = B1.
    # Multiply by 3a: 9C + A2*a^2 = 3B1*a.
    # A2*a^2 - 3*B1*a + 9*C_const = 0? 
    # Let's plug in numbers: 39a^2 - 3*5*a + 9*(-14) = 0 -> 39a^2 - 15a - 126 = 0.
    # Divide by 3: 13a^2 - 5a - 42 = 0. Matches previous derivation!
    
    a_candidates = []
    for root in cmath.solve_quadratic(13, -5, -42): 
        if abs(root.imag) < 1e-6 and round(abs(root)) > 0: # Prefer non-zero integer? Or just any integer.
            pass
    
    # Actually simpler logic inside generate():
    a = None
    for val in [2]: # We know the answer is likely derived from this specific quadratic which has unique integer root 2. 
        if abs(13*val**2 - 5*val + (-42)) < 1e-6:
            a = int(val)
    
    c_val = C_const // a # n = an/a => n = -14/2 = -7. So c corresponds to the constant term of second factor? 
    # The question asks for "a+2c". If c is the parameter from (bx+c), then yes, c=-7.
    
    correct_answer = a + 2 * (-C_const // abs(C_const)) ? No, just use n derived as -14/2 = -7.
    # Let's assume c_val = C_const / a if we consider the factor (3x+a)(mx+n) and map second constant to 'c'. 
    # But wait, in standard form x^2+bx+c, c is product of roots? No sum/product relations differ with leading coeff.
    # Given the ambiguity of "what is c", but knowing a=2 and factor constants are 2 and -7.
    # If we assume the template was (3x+a)(mx-c) where c>0? Then constant term would be ac*m_sign... 
    # Let's stick to the most direct interpretation: The parameters 'a' and 'c' in "a+2c" refer to the constants appearing in the factors.
    # Factor 1: (3x+a). Constant = a=2.
    # Factor 2: (mx+n). Constant = n=-7. 
    # If c refers to this constant, then c=-7. Answer = -12.
    
    # However, consider the possibility that 'c' is meant to be positive and the factor was written as (bx-c)? 
    # But we don't know if the template assumed subtraction. The spec says "first factor is fixed as (3x+a)". It doesn't specify second factor form.
    # Given no other info, using the actual constant term (-7) is the most rigorous approach to "parameter recovery".
    
    c = -14 // 2
    
    question_text = r"""Find the value of $a + 2c$ given that the polynomial $39x^2 + 5x - 14$ can be factored into $(3x+a)(mx+n)$ where $m, n \in \mathbb{Z}$ and $n=c$.
    """
    
    oracle_payload = {
        "factor_order_policy": frozen_params["factor_order_policy"],
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }