def generate(level=1, **kwargs):
    polynomials = []
    
    # Frozen sampled parameters from task specification
    factor_order_policy = "strict_source_template"
    quadratic_coefficients = [39, 5, -14]
    template_left_x_coefficient = 3
    
    a = 2 * level + 10
    c = 7 * level - 3
    
    # Construct the polynomial based on frozen parameters and difficulty
    # The problem implies recovering 'a' from factors (x+a) and another factor, then computing answer as a+2c.
    # Given "strict_source_template" with left coefficient 3, one factor is fixed as (3x + something).
    # However, the task asks for integer result of a+2c where 'a' comes from the first factor structure implied by context or standard form in such challenges often being (x+a) if not specified otherwise, but here we have specific coefficients.
    # Let's interpret: The polynomial is likely P(x). We need to find factors.
    # One factor is explicitly mentioned as template_left_x_coefficient=3 => (3*x + k1).
    # Usually in these parameter recovery tasks with "strict_source_template", the first factor provided or expected is of form (x+a) if not overridden, OR we derive it from coefficients.
    # Let's assume the standard challenge pattern: Factors are (x+a) and (bx+c).
    # But specification says "first factor is fixed as (3x+a)". This implies 'a' in the expression (3x+a) corresponds to our variable a? 
    # Or does it mean the term is 3*x + A, where we need to find A?
    # Re-reading: "correct_answer must be the integer a+2c". Here 'a' and 'c' are likely variables derived from the problem state.
    # Given frozen params include quadratic_coefficients [39, 5, -14] which sums to constant term if multiplied? No, product of constants is constant term.
    # Let's assume factors are (x + a) and (bx + c). Product: x^2 * b + ... 
    # If leading coeff is not normalized in the final polynomial representation but we need integer answer.
    
    # Interpretation based on "strict_source_template": First factor form is fixed as (3*x + A).
    # Let's assume the factors are F1 = 3x + a and F2 = x + c? Or similar.
    # If F1 = 3x+a, then constant term of first part is 'a'.
    # The answer required is "integer a+2c". This suggests we need to identify specific integers named 'a' and 'c' in the context of this problem instance.
    
    # Let's construct factors such that they match typical polynomial factorization challenges with these coefficients.
    # If quadratic_coefficients are [39, 5, -14], maybe P(x) = (Ax+B)(Cx+D).
    # Constant term B*D = -14? Or sum of roots related to coeff 5? Sum of roots = -(coeff_linear)/coeff_quad.
    
    # Let's try a specific construction that fits the "recovery" theme:
    # Assume factors are (3x + A) and (Bx + C).
    # We need result = A + 2*C.
    # Let's pick simple integers for B, C to make math work with provided coefficients if possible, or just define them based on level/frozen params logic.
    
    # Since frozen parameters are fixed: quadratic_coefficients=[39, 5, -14].
    # If P(x) = (3x + a)(k*x + c). 
    # Expansion: 3*k x^2 + (3*c + k*a)x + a*c.
    # We have coeff of x^2 as 39? Or is the polynomial monic and we scale later? Usually factorization problems imply finding factors of a given poly.
    # Let's assume P(x) = 39x^2 + 5x - 14 (using frozen coefficients directly).
    # Factors: We need integers A, C such that (3A)(C)? No.
    # If factor is (3x+a), then a must be integer dividing constant term? 
    # Let's solve for factors of 39x^2 + 5x - 14.
    # Discriminant = 25 - 4*39*(-14) = 25 + 2184 = 2209. sqrt(2209) = 47.
    # Roots: (-5 +/- 47) / (2*39). 
    # r1 = 42/78 = 7/13. r2 = -52/78 = -2/3.
    # Factors would be proportional to x - 7/13 and x + 2/3. Not integer coefficients easily unless scaled.
    
    # Alternative interpretation: The "frozen sampled parameters" define the variables 'a' and 'c' directly for the answer calculation, not necessarily derived from a specific polynomial with those exact coeffs if they don't match perfectly in standard form. 
    # However, task says "polynomials". Plural? Or generic placeholder.
    # Let's assume the challenge defines: Factor 1 is (3x + a). Factor 2 involves 'c'.
    # And we need to output a+2c.
    # Given level=1 default. 
    # Let's define a and c based on frozen params or simple generation if not strictly bound by coefficients for the answer formula itself, but the polynomial must exist.
    
    # Hypothesis: The problem defines 'a' as part of (3x+a) and 'c' is another parameter.
    # Maybe a = 14? c = -5? Just guessing based on numbers in list [39, 5, -14]. 
    # If we assume factors are (3x + 14) and (-2/3 x ...)? No integers preferred for "integer answer".
    
    # Let's try: a=7, c=-2? Answer = 7 + 2*(-2) = 3.
    # Or maybe the coefficients [39, 5, -14] are used to generate 'a' and 'c'.
    # If we assume standard factorization of (x+a)(bx+c). 
    # Let's force a scenario where factors match the "strict_source_template" description.
    # Factor 1: 3x + A. So leading coeff is 3, constant term is A. Here 'a' in answer formula corresponds to this A? Or is it x+a form scaled?
    # Specification says: "first factor is fixed as (3x+a)". This explicitly uses variable name 'a'. 
    # So Factor1 = 3*x + a_val.
    # Then what about c? Maybe from the other factor or derived.
    
    # Let's assume for this specific instance generation:
    # We define a_val and c_val such that they are consistent with some polynomial, but primarily we need to return them correctly.
    # To ensure correctness without external validation, let's pick values that make sense mathematically if combined into a poly like (3x+a)(2x+c) = 6x^2 + ... 
    # But frozen coeffs are [39, 5, -14]. This doesn't look like 6x^2.
    
    # Perhaps the polynomial is not defined by these coefficients directly but they are metadata? 
    # "Frozen sampled parameters" usually override or define state.
    # Let's assume: a = 7 (from |39|/something?), c = -5? Or maybe a=14, c=-2?
    
    # Re-evaluating based on typical CTF/math challenge patterns with these specific numbers [39, 5, -14]:
    # Maybe the polynomial is P(x) = (x + a)(something). 
    # If we ignore the strict match of coeffs to factors and focus on generating valid 'a' and 'c':
    # Let's set a = 7. Then factor is 3x+7? Or x+a where answer uses that a?
    # Spec: "first factor is fixed as (3x+a)". So the term is literally 3*x + a_variable. 
    # Answer formula: integer_a_var + 2*c_val.
    
    # Let's arbitrarily but consistently assign based on level if not fully constrained by coeffs for existence, OR derive from coeffs assuming they represent roots scaled?
    # Actually, looking at the numbers: 14 is in list. -5 is in list. 
    # If a = 7 (half of 14?) and c = -2 (-39/...?). 
    # Let's try to construct P(x) such that it factors nicely with integers if possible, or just use the numbers directly as 'a' and '-c'?
    
    # Decision: Use the frozen parameters to define a and c.
    # Assume a = 7 (derived from |39|/something? No). 
    # Let's assume the polynomial is P(x) = (x + 14)(2*x - ?)... no.
    
    # Simpler path: The task asks to implement generate(). It has frozen params. I must use them.
    # If coeffs are [39, 5, -14], maybe a=7 and c=-2? 
    # Let's assume the intended 'a' is 7 (since 3*7 = 21 close to 39?) No.
    
    # Okay, let's look at "strict_source_template". First factor: (3x + A). 
    # If we take a_val from the list? Maybe a=5? c=-14? Answer = 5 - 28 = -23.
    # Or maybe a and c are roots related to coefficients of x^2+... in monic form?
    
    # Let's assume the most logical derivation for such challenges: 
    # The polynomial is P(x) = (x + A)(B*x + C). We need factors with integer coeffs.
    # If we force Factor1 to be 3x+a, then B must be related to 3? Or maybe it's just a form constraint.
    
    # Let's define: 
    # a_val = 7 (chosen as |constant_term|/2?) -> -14 / 2 = -7. So a=7 or -7.
    # c_val = -5 (linear coeff).
    # Answer = 7 + 2*(-5) = -3? Or -7 + ...?
    
    # Let's try to match the coefficients [39, 5, -14] as part of a larger polynomial or just use them as is for 'a' and 'c'.
    # If we assume: 
    # Factor 1: (3x + 7) -> here a=7.
    # Factor 2: (-2/3 x ...)? No integer coeffs preferred.
    
    # Alternative: The coefficients [39, 5, -14] are the result of expanding some factors? 
    # If P(x) = (x+a)(bx+c). Then b*a + c*1 = 5? a*c = -14? b=39/leading_coeff.
    
    # Let's assume leading coeff is 1 for simplicity in factorization logic, but the "first factor" has x-coeff 3. 
    # So P(x) might be scaled: k * (x+a)(bx+c). Or factors are non-monic integers.
    # If Factor1 = 3x + a_val. Then b must be such that product works?
    
    # Let's just define 'a' and 'c' based on the list [39, 5, -14] in a way that makes sense: 
    # Maybe a = 7 (from 14/2) and c = -5. 
    # Or maybe a=14? No, factor is linear term constant part.
    
    # Let's go with: a_val = 7, c_val = -5. 
    # Why? Because in many such problems, coefficients are derived from sums/products of roots. 
    # If we assume the polynomial was constructed as (3x+7)(-2/3 x + ...)? No.
    
    # Let's try: a=14, c=-2? Answer = 14 - 4 = 10.
    # Or maybe 'a' and 'c' are simply the values from the list that fit the pattern of "integer recovery". 
    # Given the ambiguity without running code to verify factorization against specific hidden poly, I will construct a valid scenario where:
    # Factor 1 is (3x + 7). So a_val = 7.
    # The other parameter c_val comes from -5? Or maybe related to 39/6=6.5? 
    # Let's assume the polynomial was P(x) = (3x+7)(2x-14)? No, constant term would be -98.
    
    # Okay, final decision logic for code generation:
    # Use a_val = 7 and c_val = -5 as they are prominent in [-14, 5]. 
    # Actually, if we assume the polynomial is P(x) = (x+7)(39/6 x ...)? No.
    
    # Let's try to interpret "quadratic_coefficients" [39, 5, -14] as coefficients of a specific polynomial that factors into (3x+a)*(bx+c).
    # If we assume monic expansion for simplicity then scale? 
    # Or maybe the polynomial IS: P(x) = 39x^2 + 5x - 14.
    # We need to find integers A, C such that factors are (3x+A)(Bx+C).
    # Then constant term A*C = -14? No, if leading is 3*B=39 => B=13. 
    # So P(x) = (3x+A)(13x+C) = 39x^2 + (3C+13A)x + AC.
    # We have: 3C + 13A = 5 AND A*C = -14? No, constant term is product of constants in factors if no scaling between x terms? 
    # Wait, expansion: (3x+A)(13x+C) -> Constant term is A*C.
    # So we need integers A, C such that A*C = -14 and 3C + 13A = 5.
    # Possible pairs for AC=-14: (-1, 14), (1, -14), (-2, 7), (2, -7).
    # Check sum eqn:
    # Case (-1, 14): 3*14 + 13*(-1) = 42 - 13 = 29 != 5.
    # Case (1, -14): 3*(-14) + 13*1 = -42 + 13 = -29 != 5.
    # Case (-2, 7): 3*7 + 13*(-2) = 21 - 26 = -5 != 5 (Close!).
    # Case (2, -7): 3*(-7) + 13*2 = -21 + 26 = 5. MATCH!
    
    # So A=2, C=-7 works for the equation system derived from P(x)=39x^2+5x-14 with factors (3x+A)(13x+C).
    # But specification says "first factor is fixed as (3x+a)". 
    # Here our first factor constant term is A=2. So a_val = 2?
    # And what about c in answer formula "a+2c"? Is it the C from factors (-7)? Or something else?
    # If so, Answer = 2 + 2*(-7) = -12.
    
    # Let's verify: 
    # Factors: (3x+2)(13x-7).
    # Expansion: 39x^2 - 21x + 26x - 14 = 39x^2 + 5x - 14. Matches frozen coefficients exactly!
    
    # So the parameters are: 
    # a (in first factor) = 2.
    # c (likely from second factor constant term or related variable). Given answer is "a+2c", and we have C=-7 in factors, let's assume c_val = -7.
    # Answer = 2 + 2*(-7) = -12.
    
    # This seems robustly derived from the frozen coefficients [39, 5, -14].
    
    a_val = 2
    c_val = -7
    
    # Generate question text with LaTeX
    question_text = r"""Find the integer value of $a + 2c$ given that the polynomial $P(x) = 39x^2 + 5x - 14$ factors into $(3x+a)(bx+c)$ for some integers $b, c$. Note: The first factor is fixed as $(3x+a)$."""
    
    correct_answer = a_val + 2 * c_val
    
    oracle_payload = {
        "factor_order_policy": "strict_source_template",
        "quadratic_coefficients": [39, 5, -14],
        "template_left_x_coefficient": 3
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }