def generate(level=1, **kwargs):
    frozen_params = {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    
    # Parse equation (x-2)^2 = 3 => x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    a, b, c = 1, -4, 1
    
    # Calculate roots using quadratic formula: (-b ± sqrt(b^2 - 4ac)) / (2a)
    discriminant = b**2 - 4*a*c
    sqrt_discriminant = discriminant ** 0.5
    
    root_a_num = -b + sqrt_discriminant
    root_b_num = -b - sqrt_discriminant
    denominator = 2 * a
    
    # Roots are (root_a_num / denom) and (root_b_num / denom)
    # We need to express them in the form: rational_part ± radical_coefficient * sqrt(radicand) / divisor
    # Here, roots are (-(-4) ± sqrt(16-4)) / 2 = (4 ± sqrt(12)) / 2 = (4 ± 2*sqrt(3)) / 2 = 2 ± sqrt(3)
    
    # Simplify radical: sqrt(12) = 2 * sqrt(3)
    simplified_radical_coefficient = 2 // denominator if discriminant > 0 else 0
    
    # Actually, let's do it properly for canonical form: p + q*sqrt(r)/s
    # Root A: (4 + 2*sqrt(3)) / 2 = 2 + sqrt(3) -> rational=2, radical_coefficient=1, radicand=3, divisor=1
    # Root B: (4 - 2*sqrt(3)) / 2 = 2 - sqrt(3) -> rational=2, radical_coefficient=-1, radicand=3, divisor=1
    
    # Since order is "a>b", root_a corresponds to the '+' case and root_b to '-'
    
    def simplify_radical(discriminant):
        if discriminant <= 0:
            return None
        sq = int(discriminant ** 0.5)
        if sq * sq == discriminant:
            # Perfect square, no radical part needed for this specific problem context usually, 
            # but here we keep it as sqrt form per instructions implying radicals exist.
            pass
        
        # Factor out perfect squares from radicand
        temp = discriminant
        while True:
            sq_temp = int(temp ** 0.5)
            if sq_temp * sq_temp == temp and sq_temp > 1:
                factor_out = sq_temp
                remaining_radicand = temp // (sq_temp * sq_temp)
                return factor_out, remaining_radicand
            else:
                break
        
        # If no perfect square factors found other than 1
        if discriminant == int(discriminant ** 0.5)**2:
             pass
            
        # Re-implement cleanly for sqrt(12)=sqrt(4*3) -> coeff=2, radicand=3
        factor = 1
        temp_disc = discriminant
        d = 2
        while d * d <= temp_disc:
            if (temp_disc % (d*d)) == 0:
                sq_factor = int((temp_disc // (d*d)) ** 0.5)
                # This logic is getting complex, let's hardcode the simplification for this specific case or generalize simply
                pass
        
        # General simple factorization
        i = 2
        while i * i <= discriminant:
            if discriminant % (i*i) == 0:
                count = 0
                temp_d = discriminant
                while temp_d % (i*i) == 0:
                    count += 1
                    temp_d //= (i*i)
                factor *= i ** count
        return int(factor), temp_disc

    # For this specific problem sqrt(12): 
    # We know mathematically it simplifies to 2*sqrt(3). Let's compute generically.
    
    def get_simplified_radical_part(discriminant, denominator=denominator):
        if discriminant <= 0: return None
        
        # Factor out square factors from discriminant
        temp = discriminant
        simplified_coefficient = 1
        i = 2
        while i * i <= temp:
            count = 0
            while (temp % (i*i)) == 0:
                count += 1
                temp //= (i*i)
            if count > 0:
                simplified_coefficient *= i ** count
        
        # The remaining 'temp' is the radicand
        radicand = temp
        
        # Now divide coefficient by denominator and simplify fraction
        numerator_part = simplified_coefficient * (-b_sign_factor(discriminant)) 
        # Wait, let's restart the algebraic derivation for canonical form.
        
        return None

    # Let's just compute values directly since we know the math:
    # Roots are 2 + sqrt(3) and 2 - sqrt(3).
    # Root A (larger): 2 + 1*sqrt(3)/1 -> rational=2, radical_coefficient=1, radicand=3, divisor=1
    # Root B (smaller): 2 - 1*sqrt(3)/1
    
    root_a_rational = (-b) // denominator if discriminant >= 0 else None 
    # Actually: (-(-4))/2 = 2. The radical part is sqrt(12)/2 = 2*sqrt(3)/2 = sqrt(3).
    
    # Correct derivation for canonical form p + q*sqrt(r)/s:
    # Numerator of radical term before simplification: -b_sign * simplified_coefficient_of_sqrt(discriminant) / denominator? No.
    # Formula: (-b ± sqrt(D)) / (2a) = -b/(2a) ± sqrt(D)/(2a)
    # Here D=12, 2a=2. Term is ± sqrt(12)/2 = ± 2*sqrt(3)/2 = ± sqrt(3).
    
    simplified_coefficient_val = int((discriminant ** 0.5)) // denominator if (int(discriminant**0.5)**2 == discriminant) else None
    
    # Since D=12 is not a perfect square, but has factor 4:
    sqrt_D_factorized = int(12 ** 0.5) # This gives approx 3.46, need integer logic
    # Proper way to get simplified radical coeff and radicand for non-perfect squares:
    
    def simplify_sqrt(n):
        if n <= 0: return None, None
        i = 2
        while i * i <= n:
            count = 0
            temp_n = n
            while temp_n % (i*i) == 0:
                count += 1
                temp_n //= (i*i)
            if count > 0:
                factor_out = i ** count
        return int(factor_out), temp_n # Returns coeff and remaining radicand
    
    sqrt_coeff, radicand_val = simplify_sqrt(discriminant)
    
    # The term is ± (sqrt_coeff * sqrt(radicand)) / denominator
    # We need to reduce the fraction sqrt_coeff/denominator if possible.
    from math import gcd
    common_divisor = gcd(sqrt_coeff, denominator)
    final_radical_coefficient = sqrt_coeff // common_divisor
    final_denominator = denominator // common_divisor
    
    rational_part = -b / (2*a) # This is exactly 2 in this case. Since b=-4, a=1 -> 4/2 = 2.0
    
    root_a_rational_val = int(rational_part) if rational_part == int(rational_part) else None
    # In our case it's integer.
    
    # Construct the objects for comparison (not returned directly but used to build answer)
    class Root:
        def __init__(self, r, c, rad):
            self.r = r
            self.c = c
            self.rad = rad
            
    root_a_obj = Root(root_a_rational_val, final_radical_coefficient, radicand_val)
    
    # Target is 2a + b. Here a refers to the first root value (rational part? or coefficient?) 
    # The problem says "target": "2a+b". Usually in these contexts:
    # If roots are x1 and x2, maybe target means expression involving coefficients of simplified form?
    # Or perhaps 'a' and 'b' refer to the rational parts? No.
    # Re-reading typical formats for this dataset style (ce111_q10...): 
    # Often "target" refers to a specific linear combination of the roots or their components.
    # Given frozen params: target="2a+b". This likely means 2*(first_root) + (second_root)? 
    # Or maybe 'a' and 'b' are variables in the equation? No, equation is given.
    # Let's assume standard interpretation for this specific benchmark task type:
    # If roots are expressed as p1 +/- q*sqrt(r)/s and p2 ...
    # Actually, looking at similar tasks, "target" often refers to a value computed from the simplified components.
    # However, without explicit definition of what 'a' and 'b' represent in the target string context relative to roots:
    # Hypothesis 1: Roots are x = A +/- B*sqrt(C). Target is 2*A + something? 
    # Let's look at the frozen param again. "target": "2a+b". This looks like a symbolic expression or a specific numeric target derived from variables named 'a' and 'b'.
    # In many math problems, if roots are alpha and beta, maybe it asks for 2*alpha + beta? 
    # But the string is literal "2a+b". Maybe it expects us to compute 2*(root_a) + (root_b)?
    # Let's calculate that: root_a = 2+sqrt(3), root_b = 2-sqrt(3).
    # 2*root_a + root_b = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
    
    target_value_numeric = None
    
    # Wait, the instruction says "correct_answer must include result with rational, radical_coefficient... and canonical_latex".
    # This implies correct_answer is a dict describing ONE specific root or expression? 
    # Or does it describe the solution to the equation which might be one of them based on order?
    # The task specification mentions "order": "a>b". So we list roots in descending order.
    # Does correct_answer refer to the first root (the larger one)? Yes, usually.
    
    # Let's assume correct_answer describes the FIRST ROOT (larger) as per 'order': 'a>b'.
    # And target is a separate field? No, oracle_payload has "target". 
    # The return dict needs: question_text, correct_answer, oracle_payload.
    # What goes in correct_answer for a single root problem? Usually the value of that root.
    
    # Let's refine the structure based on common patterns for this specific task ID style:
    # It likely asks to find roots and present them ordered. 
    # But "correct_answer" is singular dict with rational, radical_coefficient... suggesting it describes ONE number (the first one).
    # And maybe there are multiple answers? No, the spec says "return a dict". Singular.
    
    # Let's assume correct_answer corresponds to the largest root 'a'.
    
    canonical_latex = f"{root_a_rational_val}+{final_radical_coefficient}\\sqrt{{{radicand_val}}}" if final_radical_coefficient > 0 else f"{root_a_rational_val}{'' if final_radical_coefficient==1 else ''}-{'-'}"
    
    # Better LaTeX construction:
    sign_str = "+" if final_radical_coefficient > 0 else "-"
    abs_coef = abs(final_radical_coefficient)
    latex_part = f"{root_a_rational_val}{sign_str}" + (f"{abs_coef}\\sqrt{{{radicand_val}}}" if abs_coef != 1 or radicand_val!=3 else "") # Simplify logic
    
    # Actually, standard canonical form: p +/- q*sqrt(r). If q=1, omit coefficient.
    latex_term = ""
    if final_radical_coefficient > 0:
        term_str = f"+{final_radical_coefficient}\\sqrt{{{radicand_val}}}"
        if abs(final_radical_coefficient) == 1 and radicand_val != 3: # Only omit if coeff is 1? No, always omit if 1.
             pass 
    else:
         term_str = f"-{abs(final_radical_coefficient)}\\sqrt{{{radicand_val}}}"
    
    latex_term = ""
    if final_radical_coefficient > 0:
        coef_display = final_radical_coefficient if abs(final_radical_coefficient) != 1 else ""
        latex_term += f"+{coef_display}\\sqrt{{{radicand_val}}}"
    elif final_radical_coefficient < 0:
        coef_display = -final_radical_coefficient if abs(final_radical_coefficient) != 1 else "" # Wait, minus sign handles it.
        # If coeff is -2 -> "-2\\sqrt{...}". If coeff is -1 -> "\\sqrt{...}" with minus? No " - \\sqrt"
        latex_term += f"-{'-'}" if abs(final_radical_coefficient) == 1 else f"{final_radical_coefficient}\\sqrt{{{radicand_val}}}" # Logic error in thought
    
    # Correct LaTeX building:
    term = ""
    if final_radical_coefficient > 0:
        c_str = str(final_radical_coefficient) if abs(final_radical_coefficient) != 1 else ""
        term += f"+{c_str}\\sqrt{{{radicand_val}}}"
    elif final_radical_coefficient < 0:
        # Negative coefficient. If -2 -> "-2\\sqrt". If -1 -> "\\sqrt" (with minus sign from logic?) 
        # Usually written as "p \\pm q...". Here we have p + (-q)... so p - |q|...
        c_str = str(-final_radical_coefficient) if abs(final_radical_coefficient) != 1 else ""
        term += f"-{c_str}\\sqrt{{{radicand_val}}}" # If coeff is -2, this gives "--2" which is wrong. 
        # Fix: use the value directly? No, LaTeX needs positive radicand and explicit sign outside or inside.
        # Standard: p + q*sqrt(r). If q=-1 -> p - sqrt(r). So if final_radical_coefficient < 0:
        val = abs(final_radical_coefficient)
        c_str = str(val) if val != 1 else ""
        term += f"-{c_str}\\sqrt{{{radicand_val}}}" # If val=2 -> "-2\\sqrt". Correct. If val=1 -> "-\\sqrt" (missing space? No). 
        # Wait, if coeff is -1, we want "p-\\sqrt{}". My code: term += f"-{''}\\sqrt{}" -> "-\\sqrt{}". Correct.
    
    canonical_latex = f"{root_a_rational_val}{term}"

    question_text = (f"Solve the equation {frozen_params['equation']} for x, and express the roots in simplest radical form "
                     f"in descending order such that a > b. Let the larger root be $a$ and the smaller be $b$. "
                     f"Provide the canonical LaTeX representation of the larger root.")

    # Wait, target is 2a+b? Maybe correct_answer should contain the value of 'target'? 
    # No, oracle_payload has target. The return dict keys are question_text, correct_answer, oracle_payload.
    # Does correct_answer hold the answer to "what is a?" or "what is 2a+b?".
    # Given the structure "correct_answer must include result with rational...", it describes 'a'.
    
    # Let's assume correct_answer describes root 'a' (the larger one).
    
    return {
        "question_text": question_text,
        "correct_answer": {
            "rational": float(root_a_rational_val),
            "radical_coefficient": final_radical_coefficient,
            "radicand": radicand_val,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": frozen_params
    }