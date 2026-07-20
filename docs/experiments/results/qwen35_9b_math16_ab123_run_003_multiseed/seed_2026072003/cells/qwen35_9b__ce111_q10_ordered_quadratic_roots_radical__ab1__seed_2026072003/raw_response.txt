def generate(level=1, **kwargs):
    equation = "(x-2)^2=3"
    order = "a>b"
    target = "2a+b"
    
    # Parse the expanded quadratic: x^2 - 4x + 4 = 3 => x^2 - 4x + 1 = 0
    a_coeff = 1
    b_coeff = -4
    c_coeff = 1
    
    discriminant = b_coeff**2 - 4*a_coeff*c_coeff
    sqrt_discriminant = (discriminant) ** 0.5
    
    # Roots: x = (-b ± sqrt(d)) / (2a)
    root_a_num = -b_coeff + sqrt_discriminant
    root_b_num = -b_coeff - sqrt_discriminant
    denominator = 2 * a_coeff
    
    # Determine canonical order based on "a>b" logic for the final expression values or coefficients? 
    # Task spec implies 'order' refers to how roots are labeled in the context of the target linear combination.
    # Usually, root_a is the larger one if we follow standard ordering unless specified otherwise by value.
    # However, the task says "math16_ordered_quadratic_roots_radical" with order "a>b". 
    # Let's assume 'a' corresponds to the root derived from '+' and 'b' from '-' in the formula (-b + sqrt)/2a vs (-b - sqrt)/2a.
    # But wait, if discriminant is positive, one is larger than the other.
    # Standard convention: x1 = (-b+sqrt(D))/2a, x2 = (-b-sqrt(D))/2a. 
    # If a>0 (which it is), then x1 > x2. So let root_a be x1 and root_b be x2? 
    # Or does 'order' mean the coefficients of the radical part in the final answer string must match "a>b"?
    # Re-reading: "math16_ordered_quadratic_roots_radical". Likely refers to ordering the roots such that we compute 2*root_a + root_b.
    # Let's define root_a as (-b_coeff - sqrt_discriminant) / denominator and root_b as (-b_coeff + sqrt_discriminant) if order was a<b? 
    # No, standard is usually x1 = (+), x2 = (-). If the task requires specific ordering for coefficients in LaTeX.
    # Let's stick to: root_a corresponds to the term with '+' radical sign numerator (larger value since a=1>0) and root_b to '-'. 
    # Wait, if the order constraint is "a>b", it might imply we must label the larger root as 'a' and smaller as 'b'?
    # If x_large = (-b + sqrt)/2a and x_small = (-b - sqrt)/2a. Then a=x_large, b=x_small satisfies a>b naturally with standard formula.
    
    val_a = (root_a_num) / denominator  # This is the larger root if a>0
    val_b = (root_b_num) / denominator  # This is the smaller root
    
    # Calculate target: 2a + b
    result_value = 2 * val_a + val_b
    
    # Construct LaTeX components
    radical_coefficient_sign = "+" if sqrt_discriminant > 0 else "" 
    # Since discriminant is non-zero here, we have a radical.
    # The coefficient of the radical in standard form x = (-b ± √D)/2a is usually implicit or explicit.
    # Here denominator is 2. Numerator has -(-4) = +4 and sqrt(16-4)=sqrt(12).
    # So roots are (4 ± sqrt(12))/2 = (4 ± 2*sqrt(3))/2 = 2 ± sqrt(3).
    # Root a (larger): 2 + sqrt(3) -> coeff of radical is 1. Radicand is 3.
    # Root b (smaller): 2 - sqrt(3) -> coeff of radical is -1? Or just part of expression.
    
    simplified_radical_term = "sqrt" if level == 0 else "\\sqrt{" + str(abs(int(discriminant))) // int(sqrt_discriminant)**2 
    # Wait, let's simplify sqrt(12). sqrt(12) = 2*sqrt(3).
    # We need to extract square factors.
    
    def simplify_sqrt(n):
        if n <= 0: return (n, 1)
        i = 2
        while i * i <= n:
            count = 0
            temp_n = n
            while temp_n % i == 0:
                temp_n //= i
                count += 1
            if count > 0 and count % 2 != 0:
                # Odd power of factor 'i' remains. One 'i' comes out, rest stay inside? 
                # Actually we want to pull out pairs. 
                pass
        
        # Better approach for perfect square extraction:
        sqrt_val = int(n ** 0.5)
        if sqrt_val * sqrt_val == n:
            return (1, n), "sqrt" + str(sqrt_val*sqrt_val) # This logic is flawed for simplification
    
    def get_simplified_radical_part(discriminant):
        val_sq = discriminant
        i = 2
        while i * i <= val_sq:
            count = 0
            while val_sq % i == 0:
                val_sq //= i
                count += 1
            if count > 0 and count % 2 != 0:
                # There is an odd number of factors 'i'. 
                # One pair (i*i) can be pulled out? No, we pull out pairs.
                # If count=3 -> i^3 = i * i^2. Pull out one i inside? No, sqrt(i^k) = i^(k/2).
                # Integer part: floor(k/2). Remainder k%2 goes under root.
                pass
        
        # Correct simplification logic:
        temp_d = discriminant
        factor_out = 1
        temp_inside = 1
        d_val = int(discriminant ** 0.5)
        
        if d_val * d_val == discriminant:
            return {"coeff": 1, "radicand": discriminant, "latex_part": str(int(sqrt_discriminant))} # Perfect square
        
        # Factor out squares
        for i in range(2, int(discriminant**0.5) + 1):
            count = 0
            while temp_d % i == 0:
                temp_d //= i
                count += 1
            
            if count >= 2:
                pairs = count // 2
                factor_out *= (i ** pairs)
        
        remaining_inside = int(discriminant / (factor_out**2)) # Or recalculate on reduced number? 
        # Actually, simpler: start with original discriminant.
        d_orig = discriminant
        
        simplified_coeff = 1
        simplified_radicand = d_orig
        
        for i in range(2, int(simplified_radicand**0.5) + 1):
            count = 0
            while simplified_radicand % i == 0:
                simplified_radicand //= i
                count += 1
            
            if count >= 2:
                pairs = count // 2
                simplified_coeff *= (i ** pairs)
        
        final_radicand = int(discriminant / (simplified_coeff**2)) # Wait, this logic is slightly off because I modified the loop variable.
        
    # Re-do simplification cleanly inside generate
    d_val = discriminant
    
    def simplify_sqrt_int(n):
        if n <= 0: return (1, abs(int(n)))
        coeff_out = 1
        temp_n = n
        for i in range(2, int(temp_n**0.5) + 1):
            count = 0
            while temp_n % i == 0:
                temp_n //= i
                count += 1
            if count >= 2:
                coeff_out *= (i ** (count // 2))
        return coeff_out, int(temp_n)

    rad_coeff, radicand = simplify_sqrt_int(discriminant)
    
    # Calculate exact float values for verification but output LaTeX structure
    root_a_expr_num1 = -b_coeff + discriminant**0.5
    root_b_expr_num2 = -b_coeff - discriminant**0.5
    
    # Roots: (4 ± 2*sqrt(3)) / 2 -> 2 ± sqrt(3)
    # Root a (larger): 2 + sqrt(3). Coeff of radical is rad_coeff? 
    # Wait, if simplified_sqrt returns coeff_out=2 and radicand=3. Then term is 2*sqrt(3). Divided by 2 -> sqrt(3).
    # So final coefficient in the root expression becomes (coeff_out / denominator) * sign?
    
    numerator_radical_coeff = rad_coeff
    radical_term_in_root_a_sign = "+" 
    radical_term_in_root_b_sign = "-" 
    
    # But wait, we divide by 2a. Here a=1, so div is 2.
    # Numerator term was -b + sqrt(D). -(-4) = 4. So (4 ± 2sqrt(3))/2 = 2 ± sqrt(3).
    # The radical part coefficient in the final root expression is rad_coeff / denominator? 
    # No, we must check if numerator has common factor with denominator before simplifying fraction fully? 
    # Standard form usually keeps integer coefficients outside.
    
    # Let's construct the LaTeX for correct_answer components based on standard math16 format expectations:
    # root_a = 2 + sqrt(3) -> a_val corresponds to this.
    # root_b = 2 - sqrt(3). 
    # Target: 2a + b = 2*(2+sqrt(3)) + (2-sqrt(3)) = 4 + 2sqrt(3) + 2 - sqrt(3) = 6 + sqrt(3).
    
    final_radical_coeff_in_target = rad_coeff * 1 # From a term: coeff=rad/den. Wait. 
    # Let's re-evaluate the coefficient mathematically without code simulation errors.
    # Root A (larger): (-b + sqrt(D))/2a. Numerator radical part is sqrt(D). Denom 2a.
    # Simplified Radical Part of Num: rad_coeff * sqrt(radicand). 
    # Term in root = (rad_coeff / denom) * sqrt(radicand).
    # Here rad_coeff=2, radicand=3, denom=2. Coeff becomes 1.
    
    term_a_radical_coef = numerator_radical_coeff // denominator if denominator != 0 else numerator_radical_coeff
    # Actually integer division might lose sign info or precision if not careful, but here it's exact.
    # Is rad_coeff always divisible? In this case yes (2/2=1). 
    # What if D was something where simplification didn't yield divisibility by 2a? 
    # The task implies a canonical form exists. We assume the fraction reduces nicely or we keep it as is?
    # "canonical_latex" usually expects simplified fractions and radicals with no common factors in radical term unless rationalizing needed.
    
    # Let's compute the target value numerically first to ensure correctness, then build LaTeX string matching that structure.
    val_a = ( -b_coeff + rad_coeff * radicand**0.5 ) / denominator if denominator != 0 else float('inf') 
    # Wait, math: (-b + sqrt(D))/2a. The 'radical' in the numerator is just sqrt(D). 
    # My simplify_sqrt_int returns coeff and radicand such that sqrt(D) = coeff * sqrt(radicand).
    # So term is (coeff / denom) * sqrt(radicand).
    
    coef_a_rad = rad_coeff // denominator if denominator != 0 else float(rad_coeff)/denominator 
    # But wait, the sign of b? -b is +4. The radical part is separate from rational part.
    # Rational part: -b / denom = 4/2 = 2. Radical part: (coeff/denom)*sqrt(radicand).
    
    coef_b_rad = rad_coeff // denominator if denominator != 0 else float(rad_coeff)/denominator 
    # Note: Root b has minus sign before radical term in standard formula (-b - sqrt(D)).
    # So root a rational + coeff_a * sqrt. Root b rational - coeff_b * sqrt? 
    # Yes, usually written as p +/- q*sqrt(r). 
    
    # Calculate target 2a+b exactly:
    # 2*(rational_a + coef_a_rad) + (rational_b - coef_b_rad) assuming standard form where 'b' root has minus.
    # Rational part of both roots is same (-b/2a = 4/2=2). 
    # Target = 2*(2 + c*sqrt(3)) + (2 - c*sqrt(3)) where c = rad_coeff/denom = 1.
    # = 4 + 2c sqrt(3) + 2 - c sqrt(3) = 6 + c sqrt(3). 
    # So final radical coefficient is c*(2-1) = 1. Radicand remains 3.
    
    target_rational_part = ( (-b_coeff * denominator + (-b_coeff)) / denominator )? No.
    Target rational part: 2*(-b/2a) + (-b/2a) = -3*b/(2a). 
    Here b=-4, a=1 -> -3*(-4)/2 = 6. Correct.
    
    target_radical_coef_calc = rad_coeff * (2 // denominator) # Wait. 
    # Root A: R + C*Sqrt(Rad). Root B: R - C*Sqrt(Rad).
    # Target = 2*(R+C*sqrt) + (R-C*sqrt) = 3*R + C*sqrt.
    # Coefficient of sqrt in target is C * (2-1)? No, 2*C - C = C? 
    # Wait: 2*(C*Sqrt) + (-C*Sqrt) = 2C Sqrt - C Sqrt = C Sqrt.
    # So coefficient remains rad_coeff/denom. Here 1/1 = 1.
    
    final_radical_coef_val = numerator_radical_coeff // denominator if denominator != 0 else float(numerator_radical_coeff)/denominator
    
    # Construct canonical LaTeX for the result: "6 + \\sqrt{3}" or "6 - ..."? 
    # Since coeff is positive, use "+".
    
    latex_sign_target = "+" if final_radical_coef_val > 0 and numerator_radical_coeff != 0 else ""
    # If coefficient was negative? Then sign would be "-". Here it's +1.
    
    canonical_latex_str = f"{target_rational_part} {latex_sign_target}\\sqrt{{{radicand}}}" if latex_sign_target else str(target_rational_part)
    
    question_text = (f"Given the equation \\({equation}\\), find the value of $2a+b$ where "
                     f"$a$ and $b$ are the roots satisfying the order constraint ${order}$.\n\n"
                     f"The quadratic expands to x^{{-4}}x + 1 = 0. The roots are derived from the formula.")
    # Refine question text for formal LaTeX delimiters as per instruction "use formal LaTeX delimiters".
    
    q_text_final = (f"Solve the equation {equation} by expanding and applying the quadratic formula. \n" 
                    f"If $a$ and $b$ are the roots such that ${order}$, compute the value of {target}.")

    correct_answer_dict = {
        "rational": target_rational_part, # This is an integer 6 in this case. Should it be float or int? Usually rational implies fraction if needed, but here integer.
        "radical_coefficient": final_radical_coef_val, 
        "radicand": radicand, 
        "canonical_latex": canonical_latex_str
    }

    # Ensure correct_answer structure matches spec: result with rational, radical_coefficient...
    # Maybe combine into a single string or dict? Spec says "correct_answer must include result with ...". 
    # Usually these tasks expect the final answer object to be structured.
    
    return {
        "question_text": q_text_final.replace("$", "\\\\$").replace("{", "{").replace("}", "}"), # Ensure raw latex braces handled if needed, but f-string handles it? No, need escape backslashes in python string for \\sqrt.
        # Wait, question_text must use formal LaTeX delimiters. 
        # Python strings: "\\( ... \\\)". Inside math blocks $...$ or $$...$?. 
        # Let's format strictly with single dollar signs inside the text if it's inline, or double for display. 
        # "question_text must use formal LaTeX delimiters."
        
        q_final = (f"Solve the equation \\({equation}\\). If roots $a,b$ satisfy ${order}$, compute {target}.")
        
    },

# Re-writing to be a single valid function block without comments outside.
def generate(level=1, **kwargs):
    frozen_params = {"equation": "(x-2)^2=3", "order": "a>b", "target": "2a+b"}
    
    # Parse equation logic manually for robustness against string variations if needed, 
    # but here parameters are fixed in the call context description. We use them directly or derived?
    # The prompt says "Frozen sampled parameters". We should probably use these to construct the question.
    # However, we need to compute the math answer which depends on expanding "(x-2)^2=3".
    
    eq_str = frozen_params["equation"]
    order_str = frozen_params["order"]
    target_expr = frozen_params["target"]
    
    # Expand (x-h)^2=k -> x^2 - 2hx + h^2 = k -> x^2 - 2h*x + (h^2-k) = 0
    import re
    
    match_expanded = re.match(r'\(\s*([+-]?\d*)\s*\-\s*(x\s*[+-]\s*\d+)?\)\s*=?\.?(.*)', eq_str, flags=re.IGNORECASE) # Rough regex not needed if we know the form
    # Simpler: The string is "(x-2)^2=3". 
    # We can programmatically expand or hardcode logic for this specific frozen param since it's fixed.
    # But to be generic "def generate", let's parse (x-h)^2=k pattern.
    
    match = re.match(r'\(x\s*([-+]\s*\d+)\)\^2\s*=\s*(-?\d+(?:\.\d+)?)', eq_str)
    if not match:
        # Fallback or error? Assume valid input per spec.
        pass
        
    h_val = int(match.group(1).replace("-", "").lstrip("-")) 
    # group 1 is "-2" -> parse as -2. 
    sign_h, val_h_str = re.match(r'([+-])(\d+)', match.group(1)).groups() if '-' in eq_str else ('+', '0')
    
    # Easier: Just use the known expansion for this specific frozen param to ensure accuracy, or implement generic parser.
    # Generic parser for (x-h)^2 = k:
    # Extract h and k from "(x-{h})^2={k}"
    pattern = r'\(x\s*([+-]\d+)\)\^\s*2\s*=\s*(-?\d+(?:\.\d+)?)'
    m = re.search(pattern, eq_str)
    
    if m:
        h_sign_h_val = int(m.group(1)) # e.g. -2 from "-2" string? No, group 1 is the whole thing like "-2". 
        # Actually regex capture "[-+]\d+". So match.group(1) is "-2". Convert to int -> -2.
        h_sign_h_val = m.group(1) # Keep as string for sign extraction if needed, but int() handles signs? No, int("-2") works.
        
    h_signed_int = int(m.group(1)) 
    k_float = float(m.group(2))
    
    a_coeff_quad = 1
    b_coeff_quad = -2 * h_signed_int
    c_const = h_signed_int**2 - k_float
    
    discriminant_val = b_coeff_quad**2 - 4*a_coeff_quad*c_const
    
    # Simplify sqrt(discriminant)
    def simplify_sqrt(n):
        if n <= 0: return (1, abs(int(n)))
        coeff_out = 1
        temp_n = int(abs(n))
        for i in range(2, int(temp_n**0.5)+1):
            count = 0
            while temp_n % i == 0:
                temp_n //= i
                count += 1
            if count >= 2:
                coeff_out *= (i ** (count // 2))
        return coeff_out, int(temp_n)

    rad_coeff_int, radicand_val = simplify_sqrt(discriminant_val)
    
    # Roots calculation
    denom_quad = 2 * a_coeff_quad
    
    # Root A (associated with + in numerator of formula -b+sqrt(D))
    # Rational part: -b / denom
    rational_part_num = abs(b_signed_int) if b_signed_int < 0 else b_signed_int 
    # Actually -(-4) = 4. So rational part is (-b_coeff)/denom.
    
    num_rational = -(b_coeff_quad // a_coeff_quad * (a_coeff_quad)) / denom_quad # Just -b/denom
    
    # Wait, integer division for exactness? Yes if divisible. 
    # Here b=-4 -> -(-4)=4. 4/2=2.
    
    rational_val = -(b_coeff_quad) // denom_quad if (-(b_coeff_quad)) % denom_quad == 0 else float(-(b_coeff_rad))/denom_quad
    
    # Radical coefficient in root: rad_coeff_int / denom_quad
    radical_coef_root = rad_coeff_int // denom_quad if denom_quad != 0 and rad_coeff_int % denom_quad == 0 else (rad_coeff_int/denom_quad)
    
    # Determine roots a and b based on order "a>b"
    # Root_plus_val = rational_part + radical_term_sign * abs(radical_coef_root)*sqrt(radicand)? 
    # Formula: x = (-b ± sqrt(D))/2a. 
    # Let root1 (plus) be larger if 2a>0? Here a=1, so yes.
    # Root_a_val = rational_part + radical_coef_root * math.sqrt(radicand_val) ? No, the coefficient applies to sqrt(radicand).
    # The term is simply: (-b/denom) +/- (rad_coeff_int/denom)*sqrt(radicand_val)? 
    # Wait, if we simplified D -> coeff_out^2 * radicand. Then sqrt(D) = coeff_out*sqrt(radicand).
    # So numerator radical part is coeff_out*sqrt(radicand). Divided by denom.
    
    term_radical_coef_a = rad_coeff_int / denom_quad 
    # Check divisibility: 2/2=1. Exact.
    
    root_plus_val = rational_part + (rad_coeff_int/denom_quad) * float(math.sqrt(radicand_val)) if radicand_val > 0 else None
    
    # For LaTeX, we need the symbolic representation.
    # Root a (larger): p + c*sqrt(r). Root b: p - c*sqrt(r).
    
    root_a_latex = f"{rational_part} {'' if term_radical_coef_a==1 and radicand_val>0 else ''}" 
    # Wait, construct canonical string for the answer components.
    
    import math
    
    final_rational_answer = 3 * rational_part # From previous derivation: target = 6 + sqrt(3). Rational part is 6.
    # Recalculate exactly: Target = 2a+b. a=p+cS, b=p-cS (assuming order a>b implies p+cS > p-cS which holds for c>0).
    # If c<0? Here c=1/2*sqrt(4)=1. Positive. 
    # So root_a is the one with + radical term relative to rational part. Root_b has -.
    
    target_rational = 3 * (-(b_coeff_quad) // denom_quad if b_coeff_quad != 0 else 0) ? No, -b/2a for both.
    # Target Rational: 2*(-b/denom) + (-b/denom) = -3*b/denom.
    
    target_rational_val = -(3 * b_coeff_quad) // denom_quad if (-(3 * b_coeff_quad)) % denom_quad == 0 else float(-(3 * b_coeff_quad))/denom_quad
    
    # Target Radical Coefficient: 
    # Term from a: +2*(radical_coef_root). Term from b: -1*(radical_coef_root).
    # Sum: (2-1)*radical_coef_root = radical_coef_root.
    
    target_radical_coef_val = term_radical_coef_a
    
    final_radicand_val = radicand_val if radicand_val > 0 else 0 # If perfect square, we handle separately? 
    # Here D=12 -> sqrt(12)=2sqrt(3). rad_coeff_int=2, radicand_val=3.
    
    target_latex_sign = "+" if target_radical_coef_val != 0 and (target_radical_coef_val > 0 or target_expr in ["a+b", "b+a"]) else "" 
    # If coefficient is negative? Then sign "-".
    
    canonical_str_target = f"{int(target_rational_val)}" + ("+" if target_latex_sign == "+" else "") + f"\\sqrt{{{target_radical_coef_val**2 * radicand_val}}" ? No.
    The radical in the answer should be simplified: coefficient is 1, radicand 3. 
    If coeff was -1? Then "-\\sqrt{...}".
    
    # Construct canonical_latex for correct_answer dict entry 'canonical_latex' which represents the full result string like "6+\\\\sqrt{3}" or similar format expected by oracle.
    # Usually: "{rational}{sign}\\sqrt{{radicand}}" if coeff is 1/-1? 
    # But what if coefficient != +/-1? The problem says radical_coefficient may be +1 or -1. So we assume simplified form has unit coeffs in target?
    
    latex_parts = []
    rational_str = str(int(target_rational_val))
    rad_part_sign = ""
    rad_latex_content = f"\\sqrt{{{radicand_val}}" if radicand_val > 0 else "1" # If perfect square, usually just number. Here not perfect square in final D? 
    # Wait, target radical coefficient is derived from original simplification. It might be non-integer if denom doesn't divide rad_coeff_int evenly?
    # But spec says radial_coefficient may be +1 or -1. So we assume it reduces to integer 1/-1.
    
    if abs(target_radical_coef_val) == 1:
        sign_char = "+" if target_radical_coef_val > 0 else "-"
        rad_latex_content = f"\\sqrt{{{radicand_val}}"
        latex_parts.append(f"{rational_str} {sign_char}\\sqrt{{{radicand_val}}}" ) # Wait, need to escape backslash in python string? Yes.
    elif target_radical_coef_val == 0:
         latex_parts.append(rational_str)
    
    correct_answer = {
        "result": float(target_rational_val + (target_latex_sign * math.sqrt(radicand_val))), # Just for internal check, output dict needs specific keys? 
        # Spec says: correct_answer must include result with rational, radical_coefficient... 
        # So structure: {"rational": ..., "radical_coefficient": ..., "radicand": ..., "canonical_latex": ...}
    }
    
    return {
        "question_text": f"Solve the equation \\({eq_str}\\). If roots $a,b$ satisfy ${order}$, compute {target_expr}.",
        "correct_answer": correct_answer = {"rational": int(target_rational_val), "radical_coefficient": target_radical_coef_val if abs(target_radical_coef_val) == 1 else None, "radicand": radicand_val, "canonical_latex": latex_parts[0] or str(int(target_rational_val))},
        # Wait, correct_answer is a dict? Or just the string? 
        # Spec: "correct_answer must include result with rational...". Implies an object/dict.
    }

# Final clean code block without comments/explanations outside function