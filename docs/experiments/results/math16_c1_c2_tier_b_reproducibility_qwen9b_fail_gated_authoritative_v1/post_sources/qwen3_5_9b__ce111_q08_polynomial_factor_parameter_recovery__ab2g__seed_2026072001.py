def generate(level=1, **kwargs):
    frozen_params = {"factor_order_policy": "strict_source_template", "quadratic_coefficients": [39, 5, -14], "template_left_x_coefficient": 3}
    
    # Extract parameters from frozen dict or kwargs if provided (though spec says preserve exactly)
    factor_order_policy = frozen_params["factor_order_policy"]
    quadratic_coefficients = frozen_params["quadratic_coefficients"]
    template_left_x_coefficient = frozen_params["template_left_x_coefficient"]
    
    a, b, c = quadratic_coefficients
    
    # Construct the polynomial: (3x + a)(x + 2c) -> 3x^2 + (6c+a)x + 2ac
    # Given coefficients [A, B, C] where A=39, B=5, C=-14
    # We have: 
    #   3 = coefficient of x^2 in expanded form? Wait.
    # Let's re-evaluate the structure based on standard polynomial factorization tasks.
    # Usually: P(x) = (mx + a)(nx + b). Expanded: mn*x^2 + (mb+na)x + ab.
    # Here, template_left_x_coefficient is 3. So first factor is (3x + a).
    # Let second factor be (1x + d). Then P(x) = (3x+a)(x+d) = 3x^2 + (3d+a)x + ad.
    # Coefficients given: [39, 5, -14]. This implies the polynomial is likely scaled or specific format.
    # However, looking at "correct_answer must be the integer a+2c", it suggests a specific mapping.
    # Let's assume the standard form where coefficients are for Ax^2 + Bx + C.
    # If P(x) = k*(3x+a)(x+d), then:
    #   A = 3k, B = (3d+a)k, C = ad*k.
    # Given [39, 5, -14]. 
    # Maybe the polynomial is just defined by these coefficients directly without scaling k=1?
    # If k=1: 3x^2 + ... but A=39. So maybe factors are (something)(something) resulting in 39x^2...
    # Let's reconsider "factor_order_policy": "strict_source_template". 
    # First factor fixed as (3x+a). Second factor must be derived to match coefficients [39, 5, -14].
    # If P(x) = (3x + a)(bx + c), then:
    #   x^2 coeff: 3b = 39 => b = 13.
    #   x coeff: 3c + ab = 5 => 3c + 13a = 5.
    #   const term: ac = -14.
    # From ac = -14, possible integer pairs (a,c): (-1,14), (1,-14), (-2,7), (2,-7), etc.
    # Check 3c + 13a = 5 for these:
    #   a=-1, c=14 -> -42 != 5.
    #   a=1, c=-14 -> -42+13 = -29 != 5.
    #   a=-2, c=7 -> 21-26 = -5 != 5.
    #   a=2, c=-7 -> -21+26 = 5. MATCH!
    # So factors are (3x + 2) and (13x - 7). 
    # Here 'a' in the problem context likely refers to the constant term of the first factor? Or is it a variable name from the prompt's specific logic?
    # The prompt says "correct_answer must be the integer a+2c". In our derivation, we found factors (3x+a) and (bx+c). 
    # Wait, if second factor is (13x - 7), then its constant term is c=-7. First factor constant is a=2.
    # Then answer = a + 2c? Or does the prompt imply specific variable names from a template where 'a' and 'c' are defined differently?
    # Re-reading: "first factor is fixed as (3x+a)". So first factor constants term is 'a'. 
    # Second factor, let's call it (dx + e). Then P = (3x+a)(dx+e) = 3d x^2 + (3e+ad)x + ae.
    # Given coeffs [A,B,C] = [39,5,-14].
    # A=3d => d=13.
    # C=ae => a*e = -14.
    # B=3e+ad = 5 => 3e + 13a = 5.
    # We solved this: a=2, e=-7 works (since 2*-7=-14 and 3*(-7)+13*2 = -21+26=5).
    # So first factor is (3x+2), second is (13x-7). 
    # The prompt asks for "a+2c". In the context of typical generated tasks, 'c' often refers to the constant term of the *second* factor? Or maybe there's a specific template variable mapping.
    # However, looking at the instruction: "correct_answer must be the integer a+2c". 
    # If we assume standard polynomial notation (ax^2 + bx + c), then 'a' and 'c' are coefficients 39 and -14? No, that doesn't fit the formula.
    # It is highly likely that in this specific task template:
    #   Factor 1: (3x + a) -> constant term is named 'a'. Here a=2.
    #   Factor 2: (c x + d)? Or maybe the second factor's constant term is named 'c'? 
    # If we assume the formula "a+2c" refers to our found values where first const=a and second const=c?
    # Then answer = 2 + 2*(-7) = -12.
    # BUT, let's look at the frozen params again: "quadratic_coefficients": [39, 5, -14]. 
    # Is it possible the task defines 'a' and 'c' differently? 
    # Let's assume the question text asks to recover parameters where factors are (3x+a) and (cx+d).
    # Then P = (3x+a)(cx+d) = 3c x^2 + (3d+ac)x + ad.
    # Match with [39,5,-14]:
    #   3c = 39 => c=13.
    #   ad = -14.
    #   3d + ac = 5 => 3d + 13a = 5.
    # From ad=-14, pairs (a,d): (-2,7), (2,-7)... 
    # Check 3(7) + 13(-2) = 21 - 26 = -5 != 5.
    # Check 3(-7) + 13(2) = -21 + 26 = 5. MATCH.
    # So a=2, d=-7, c=13 (coefficient of x in second factor). 
    # If the answer formula is "a+2c", and 'c' here refers to the coefficient of x in the second factor? Then 2 + 2*13 = 28.
    # Or if 'c' refers to the constant term of the second factor (which was -7)? Then 2 + 2*(-7) = -12.
    # Given "quadratic_coefficients" usually implies [A, B, C] for Ax^2+Bx+C. 
    # The variable names 'a' and 'c' in the answer formula likely refer to specific parameters defined in the template logic not fully explicit here but implied by standard patterns.
    # However, without external context, I must rely on the most logical interpretation of "strict_source_template".
    # Often in such tasks: 
    #   Factor 1: (3x + a)
    #   Factor 2: (c x + d) -> wait, usually second factor is monic or similar? No.
    # Let's assume the question asks for 'a' and 'c' where factors are (3x+a) and (cx+d). 
    # Then answer = a + 2*c_coefficient_of_x_in_second_factor? Or constant term of second?
    # Actually, looking at similar tasks: often "c" in "a+2c" refers to the coefficient 'c' from the factor definition like (x+c) or (cx+d). 
    # If Factor 2 is defined as (1*x + c), then our previous solution had second factor (13x -7). That doesn't fit monic.
    # Let's try: Factor 1 = (3x+a), Factor 2 = (c x + d)? No, usually one variable per letter.
    # Maybe the factors are (3x+a) and (b x + c)? Then answer a+2c uses 'a' from first const and 'c' from second const? 
    # If so: a=2, c=-7 -> ans = -12.
    # OR maybe the polynomial is defined as 39(x^2) ... no.
    # Let's assume the standard interpretation for this specific generated task type (ce111_q08...): 
    # The factors are typically constructed such that one has a coefficient and the other might be monic or vice versa.
    # Given "template_left_x_coefficient": 3, left factor is (3x + ...).
    # Right factor? If we assume right factor is (c x + d), then 'c' in answer formula likely refers to that 'c'. 
    # But wait, if the task says "correct_answer must be the integer a+2c", and we found factors with constants 2 and -7.
    # Is there any chance the coefficients [39,5,-14] imply something else?
    # What if the polynomial is P(x) = (x+a)(bx+c)? No, left coeff is fixed at 3.
    # Let's assume the question text will define 'a' and 'c' clearly in LaTeX. 
    # I need to generate a valid Python function that returns the dict with correct_answer calculated based on the frozen params logic derived above (finding integer roots).
    # Based on calculation: Factors are (3x+2) and (13x-7). 
    # If 'a' is constant of first factor -> 2.
    # If 'c' is coefficient of x in second factor? Or constant? 
    # Let's guess the formula "a+2c" uses: a=constant_of_first, c=coefficient_of_x_in_second? (13) -> 2+26=28.
    # OR c=constant_of_second (-7) -> -12.
    # Given typical math problems, 'c' often denotes the constant term in quadratic ax^2+bx+c. But here it's a parameter name. 
    # Let's assume the question asks for parameters of factors (3x+a) and (cx+d). Then c=13. Answer = 2 + 2*13 = 28.
    # OR if factors are (3x+a) and (b x + c), then c=-7. 
    # Without explicit definition, I will assume the most robust interpretation: The parameters 'a' and 'c' correspond to the constants in a standard factorization form often used where one variable is per term? No.
    # Let's look at "quadratic_coefficients": [39, 5, -14]. 
    # If we assume the factors are (3x+a) and (cx+d), then:
    #   x^2 coeff = 3c = 39 -> c=13.
    #   const term = ad = -14.
    #   x coeff = 3d + ac = 5.
    # We found a=2, d=-7 satisfies this with c=13.
    # So parameters are: first factor (3x+2), second factor (13x-7). 
    # The answer formula "a+2c" likely uses 'a' from first const and 'c' from the x-coeff of second? Or is it a typo for something else?
    # Actually, in many such tasks, the factors are defined as (mx+a) and (nx+c). 
    # If so, answer = a + 2*c. Here c would be -7? No, usually 'c' is reserved for constant term of quadratic Ax^2+Bx+C.
    # But here it's parameter recovery. Let's assume the question text defines factors as (3x+a) and (cx+d). 
    # Then answer = a + 2*c_coefficient_of_x_in_second_factor? That seems arbitrary.
    # Alternative: Maybe the second factor is monic? i.e., (1*x + c)? But we found coefficient must be 13 to get x^2=39. So not monic unless scaled. 
    # If P(x) = k(3x+a)(x+c), then k*3 = 39 -> k=13.
    # Then P(x) = 13*(3x+a)*(x+c) = (42)x^2 + ... No, 13*3=39 ok.
    # Expansion: 13 * [3x^2 + (a+3c)x + ac] = 39x^2 + 13(a+3c)x + 13ac.
    # Match with 5 and -14:
    #   13(a+3c) = 5 -> a+3c = 5/13 (not integer). Impossible for integers.
    # So scaling factor k is not an integer multiplier outside, but part of coefficients? 
    # Wait, if factors are (3x+a) and (bx+c), then x^2 coeff is 3b=39 -> b=13. This works with integers.
    # So factors are definitely (3x+2) and (13x-7).
    # Now, what does "a+2c" mean? 
    # If the question defines factor 2 as (cx+d), then c=13. Answer = 2 + 2*13 = 28.
    # If the question defines factor 2 as (x+c) [monic], it's impossible with these numbers unless non-integers allowed, but task implies integers ("integer a+2c").
    # So 'c' in "a+2c" must refer to something else or my assumption about variable naming is wrong. 
    # Could 'c' be the constant term of the second factor? i.e., c=-7. Then 2 + 2*(-7) = -12.
    # Which one is more standard? In "ax^2+bx+c", c is constant. But here we are recovering parameters a and c from factors (3x+a) and ... 
    # If the second factor was intended to be (cx+d), then 'c' is 13. 
    # Let's assume the question text will say "factors are (3x+a) and (cx+d)". Then answer = 28.
    # Or if it says "(3x+a) and (bx+c)", then c=-7, answer -12.
    # Given "quadratic_coefficients" usually maps to A,B,C of Ax^2+Bx+C. 
    # Let's assume the safest bet for generated tasks: The parameters 'a' and 'c' are the constants in the factors if possible? No, first factor has 3x+a. Second must have a variable name.
    # If I write code to generate text that says "factors (3x+a) and (cx+d)", then c=13 is correct for x-coeff. 
    # But usually 'c' in polynomial context is constant term. 
    # Let's check the constraint: "correct_answer must be the integer a+2c".
    # If I assume the second factor is defined as (x+c) [monic], it fails. 
    # So second factor MUST have an x-coefficient variable, say 'b' or 'c'. 
    # If the template uses 'c' for the x-coefficient of the second factor: c=13 -> ans 28.
    # If the template uses 'c' for constant term of second factor: c=-7 -> ans -12.
    # Let's look at "factor_order_policy": "strict_source_template". This implies a specific string format exists in source code I don't see, but must infer logic. 
    # Common pattern: Factors (mx+a) and (nx+c). Answer often involves these parameters. 
    # If answer is a+2c, and c is likely the constant term of second factor? Why 2*c? Maybe to distinguish from 'b'?
    # Let's try to find an example where integers make sense. Both -12 and 28 are integers.
    # However, in many math problems involving (3x+a)(cx+d), c is the coefficient. 
    # But if I assume standard variable naming for quadratic factors: (ax+b) and (cx+d). Here first factor has fixed x-coeff 3. So maybe second factor uses 'c' as its constant? No, usually a,b,c,d are constants in ax^2+bx+c = (px+r)(qx+s).
    # Let's assume the question text defines factors as: f1(x) = 3x + a, f2(x) = c*x + d. 
    # Then answer is a + 2*c? Or a + 2*d? The prompt says "a+2c". So 'c' must be defined in the factor definition text.
    # If f2 is (cx+d), then c=13. Answer = 28.
    # This seems plausible as 'c' often denotes an x-coefficient in generic linear factors (like ax+b, cx+d). 
    # I will proceed with this assumption: Factors are (3x+a) and (cx+d). Thus c=13. Answer = 2 + 2*13 = 28.
    
    a_val = 2
    b_coeff_second_factor = 13
    d_val = -7
    
    # Assuming the question text defines second factor as (c*x + d), so parameter 'c' is 13.
    correct_answer = a_val + 2 * b_coeff_second_factor 
    
    # Construct LaTeX strings for factors and polynomial
    poly_str = f"39x^2 + 5x - 14"
    factor1_str = "3x+a"
    factor2_str = f"{b_coeff_second_factor}x+d" # Wait, if I use 'c' in text, it should be c*x. But d is constant. 
    # The question_text needs to define the factors clearly so 'a' and 'c' are identified.
    # "Factor 1: (3x+a), Factor 2: (cx+d)" -> then a=2, c=13. Answer = 28.
    
    factor2_str_with_c = f"{b_coeff_second_factor}x+{d_val}" 
    # But to use 'c' in the text for the variable name, I should write "cx + d" where c is substituted? Or just show numbers and ask to find a,c?
    # Usually: "Given factors (3x+a) and (cx+d), recover parameters."
    
    question_text = f"The polynomial $P(x)$ has integer coefficients given by {poly_str}. It can be factored into two linear terms with the form $(3x + a)(c x + d)$, where $a$ and $d$ are integers. Find the value of $a+2c$."
    
    # Wait, if I say "cx+d", then c is 13. 
    # Is it possible 'c' refers to constant term? If text says "(x+c)", impossible. So must be (cx+d).
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }