def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_sampled_parameters", {"radicand": 27})
    
    radicand = frozen_params["radicand"]
    
    # Factorize radicand into perfect squares and remaining part for level 1 simplification
    simplified_radical = None
    
    if radicand == 0:
        return {
            "question_text": r"Simplify $\sqrt{0}$.",
            "correct_answer": f"coefficient=0, radicand={radicand}, canonical\_latex=\text{{\backslash sqrt {{}} }}",
            "oracle_payload": frozen_params
        }

    # Find largest perfect square factor for level 1 (usually small numbers or simple squares)
    simplified_radical = None
    
    if radicand > 0:
        temp_radicand = radicand
        
        # Check divisibility by squares from 4 up to sqrt(radicand)^2 roughly, but strictly for exact factors
        found_factor = False
        factor_num = -1
        
        i = 2
        while i * i <= temp_radicand:
            if (temp_radicand % (i * i)) == 0:
                # Found a square factor. For difficulty level 1, we might stop at the first or largest? 
                # Usually simplify fully. Let's find all and multiply coefficients.
                count = 0
                while temp_radicand % (i * i) == 0:
                    temp_radicand //= (i * i)
                    factor_num *= i
                
                if not found_factor or (factor_num < temp_radicand): 
                     # Actually, standard simplification pulls out ALL square factors.
                     pass
        
        # Re-do logic cleanly to get coefficient and remaining radicand
        coeff = 1
        current_rad = radicand
        simplified_radical = None
        
        if current_rad > 0:
            d = 2
            while d * d <= current_rad:
                count = 0
                temp_d_sq = d * d
                while (current_rad % temp_d_sq) == 0:
                    current_rad //= temp_d_sq
                    coeff *= d
                
                # If we found a factor, update simplified radical if not set or if this is the only one? 
                # Actually, multiple factors combine. e.g., sqrt(72) = sqrt(36*2) = 6sqrt(2).
                # My loop above modifies coeff and current_rad correctly for d=2. But what about subsequent primes?
                pass
            
            # Reset to do it properly in one go or accumulate
            temp_radicand = radicand
            final_coeff = 1
            remaining = 0
            
            if temp_radicand > 0:
                i = 2
                while i * i <= temp_radicand:
                    count = 0
                    sq = i * i
                    while (temp_radicand % sq) == 0:
                        temp_radicand //= sq
                        final_coeff *= i
                    
                    # If we extracted a factor, the remaining part is what's left in temp_radicand.
                    # However, if there are multiple square factors like 4 and 9 (36), they get processed sequentially.
                    pass
                
                # The logic above accumulates into final_coeff but leaves temp_radicand as the non-square part.
                # But wait: sqrt(72) = sqrt(8*9). 
                # Let's restart the factorization loop to be absolutely sure.
                
            coeff_val = 1
            rem_rad = radicand
            
            if rem_rad > 0:
                d = 2
                while d * d <= rem_rad:
                    count = 0
                    sq = d * d
                    while (rem_rad % sq) == 0:
                        rem_rad //= sq
                        coeff_val *= d
                    
                    # If we found a factor, it contributes to coefficient. 
                    # But if the remaining part is still divisible by something else? The loop continues.
                    pass
                
                simplified_radical = {"coefficient": coeff_val, "radicand": rem_rad}

    # Construct canonical latex based on result or 0 case
    if radicand == 0:
        canon_latex = r"\sqrt{}"
        coef_str = "0"
        rad_str = f"{radicand}"
    else:
        if simplified_radical is None:
            # Should not happen for positive integers unless logic fails, but fallback to unsimplified? 
            # The loop ensures simplification. If no square factor >1 found (prime), coeff=1, radicand unchanged.
            coef_str = "1"
            rad_str = f"{radicand}"
        else:
            coef_str = str(simplified_radical["coefficient"]) if simplified_radical["coefficient"] != 1 else "" # Omit coefficient if 1? Usually keep it or omit depending on style. Standard math omits coeff of 1.
            
            if simplified_radical["coefficient"] == 1:
                coef_str = "" 
            else:
                 coef_str = str(simplified_radical["coefficient"]) + " " # Add space
            
        rad_val = simplified_radical["radicand"]
        
        # Handle case where coefficient is omitted vs included. Standard form: c sqrt(r). If c=1, just sqrt(r).
        if coeff_val == 1 and radicand > 0:
            canon_latex = rf"\sqrt{{{radicand}}}"
        else:
             rad_str_formatted = f"{radicand}" # Using original for latex inside? No, use simplified radicand.
             
    # Re-evaluating the simplification logic specifically for "level 1" which implies basic perfect square extraction.
    
    temp_n = radicand
    coeff_out = 1
    
    if temp_n > 0:
        d = 2
        while d * d <= temp_n:
            count = 0
            sq = d * d
            while (temp_n % sq) == 0:
                temp_n //= sq
                coeff_out *= d
            
            # If we extracted a factor, the remaining part is updated. 
            # However, if there were multiple distinct square factors? e.g. sqrt(72). 
            # 72 / 4 = 18 (coeff=2). Next check 3: 18/9 = 2 (coeff *= 3 -> 6). Correct.
            
        final_rad = temp_n
    
    if radicand == 0:
        canon_latex = r"\sqrt{}"
        coef_out = "0"
        rad_out = f"{radicand}"
    elif coeff_out == 1 and final_rad > 0:
         # Format without coefficient
         canon_latex = rf"\sqrt{{{final_rad}}}"
         coef_out_str = "" 
     else:
          if coeff_out == 1:
             coef_out_str = ""
          else:
             coef_out_str = str(coeff_out) + " "
          
          canon_latex = rf"{coef_out_str}\sqrt{{{final_rad}}}"

    # Ensure exact integers and correct formatting for the answer string
    if radicand == 0:
        ans_text = f"coefficient=0, radicand={radicand}, canonical\_latex=\text{{\backslash sqrt {{}} }}"
    else:
        coef_display = ""
        if coeff_out != 1:
            coef_display = str(coeff_out) + " "
        
        rad_str_latex = f"{final_rad}" # Using the simplified radicand
        
        canon_latex_final = rf"\sqrt{{{rad_str_latex}}}"
        if coeff_out != 1:
             canon_latex_final = rf"{coef_display}\sqrt{{{rad_str_latex}}}"
        
        ans_text = f"coefficient={coeff_out}, radicand={final_rad}, canonical\_latex=\text{{\backslash sqrt {{{final_rad}}}}" + (rf"\text{{ {coef_out} }}" if coeff_out != 1 else "")

    # Re-constructing the exact string format required: "coefficient=..., radicand=..., canonical_latex=..."
    
    final_coeff = str(coeff_out) if coeff_out == 0 or coeff_out > 1 else "" 
    # Wait, spec says "correct_answer must include coefficient...". If coeff is 1, do we write '1'? Usually no. But let's stick to standard math representation in the string field?
    # Let's assume standard simplified form: if c=1, don't show it.
    
    final_coeff_str = str(coeff_out) if coeff_out != 1 else "" 
    final_rad_str_latex = f"{final_rad}"
    canonical_latex_final = rf"\sqrt{{{final_rad_str_latex}}}"
    if coeff_out != 1:
        # Insert coefficient before sqrt in latex
        canonical_latex_final = rf"{coeff_out} \sqrt{{{final_rad_str_latex}}}"

    question_text = f"Simplify $\sqrt{{{radicand}}}.$"
    
    answer_part = ""
    if radicand == 0:
        answer_part = "coefficient=0, radicand=" + str(radicand) + ", canonical\_latex=\text{\backslash sqrt\{\}}"
    else:
        # Construct the specific string requested: coefficient=X, radicand=Y...
        c_str = str(coeff_out).strip() if coeff_out != 1 else "" 
        r_str = f"{final_rad}"
        
        latex_part = rf"\sqrt{{{r_str}}}"
        if c_str != "":
            latex_part = rf"{c_str} {latex_part}" # Standard spacing
        
        answer_part = f"coefficient={coeff_out}, radicand={r_str}, canonical\_latex=\text{{\backslash sqrt {{{final_rad}}}}" + (rf"\text{{ {c_str} }}" if c_str else "")
        
    # Correction on the exact string format for 'canonical_latex' field in answer dict. 
    # It should be a single latex string representing the simplified radical.
    
    final_canon_latex = rf"{coeff_out} \sqrt{{{final_rad}}}" if coeff_out != 1 else rf"\sqrt{{{final_rad}}"

    return {
        "question_text": question_text,
        "correct_answer": f"coefficient={coeff_out}, radicand={r_str}, canonical\_latex=\text{{\backslash sqrt {{{final_rad}}}}" + (rf"\text{{ {c_str} }}" if c_str else "")", 
        # Wait, the correct_answer string must be valid python string.
    }

# Refactoring to ensure correctness and simplicity for generation:
def generate(level=1, **kwargs):
    frozen_params = kwargs.get("frozen_sampled_parameters", {"radicand": 27})
    
    radicand_int = frozen_params["radicand"]
    
    # Simplification Logic
    if radicand_int == 0:
        coeff_val = 0
        rem_rad = 0
        canon_latex_str = r"\sqrt{}"
        coef_out_str = "0"
    else:
        temp_n = radicand_int
        coeff_val = 1
        
        d = 2
        while d * d <= temp_n:
            count_sq = 0
            sq_factor = d * d
            while (temp_n % sq_factor) == 0:
                temp_n //= sq_factor
                coeff_val *= d
            
            # If we extracted a factor, it's done. Continue to next divisor.
        
        rem_rad_int = temp_n
        
        if coeff_val == 1 and radicand_int > 0:
             canon_latex_str = rf"\sqrt{{{rem_rad_int}}}"
             coef_out_str = "" 
        else:
            # If coefficient is not 1, include it. Note: for sqrt(4)=2, technically no radical left? 
            # But task says "radicals", implying result keeps the root unless perfect square fully extracted? 
            # Level 1 usually implies simple extraction leaving a radical if possible. 
            # However, if radicand is a perfect square (e.g., 36), sqrt(36)=6. Is that represented as coeff=0 or something else?
            # The prompt asks for "radical_simplification". Usually returns c*sqrt(r). If r becomes 1 after extraction, it's just integer.
            # But the spec says: correct_answer must include coefficient, radicand... 
            # Let's assume if perfect square, we might return coeff=0? Or maybe radicand=1? 
            # Standard simplification of sqrt(36) is 6. Does that fit "coefficient, radicand"?
            # Maybe the task expects c*sqrt(r) where r > 1 or handles integer case separately.
            # Given frozen_params={"radicand": 27}, let's trace: 
            # 27 = 9 * 3 -> coeff=3, rem_rad=3. Result: 3\sqrt{3}. Fits well.
            
            if rem_rad_int == 1:
                # Perfect square case? e.g., radicand=4 -> coeff=2, rem_rad=1. 
                # Should we output "coefficient=2, radicand=1..." or just integer?
                # Spec says include coefficient and radicand. Let's keep it consistent with c*sqrt(r) format even if r=1?
                # Or maybe treat 1 as no radical? 
                # Safest bet for generic generator: return the mathematical expression components.
                
            coef_str_val = str(coeff_val).strip()
            
            # Build latex string carefully
            inner_latex = f"{rem_rad_int}"
            final_canon_latex = rf"\sqrt{{{inner_latex}}}"
            
            if coeff_val != 1:
                final_canon_latex = rf"{coeff_val} {final_canon_latex}"

    # Format the correct_answer string exactly as requested with backslashes escaped for python dict? 
    # No, inside a python dict value is a string. The content of that string should contain LaTeX delimiters like \sqrt{...}.
    
    if radicand_int == 0:
        ans_str = "coefficient=0, radicand=0, canonical\_latex=\text{\backslash sqrt\{\}}"
    else:
        # Handle the perfect square edge case where rem_rad might be 1. 
        # If rem_rad is 1, usually we say it's an integer. But spec requires 'radicand' field.
        if coeff_val == 0 or (coeff_val != 1 and rem_rad_int == 1): 
             # This branch handles cases where the root disappears? No, sqrt(x^2) = x. Coefficient becomes part of number?
             # Let's stick to c*sqrt(r). If r=1, it is still technically a radical form with radicand 1? Uncommon but fits spec fields.
             
        coef_disp = str(coeff_val) if coeff_val != 1 else "" 
        rad_disp = f"{rem_rad_int}"
        
        # Construct the latex string for canonical_latex field in correct_answer
        lat_str_base = rf"\sqrt{{{rad_disp}}}"
        if coeff_val != 1:
            lat_str_final = rf"{coef_disp} {lat_str_base}" 
        else:
             lat_str_final = lat_str_base
        
        # Escape backslashes for the string literal in Python? No, just write it as normal text inside quotes.
        ans_str = f"coefficient={coeff_val}, radicand={rad_disp}, canonical\_latex=\text{{\backslash sqrt {{{rem_rad_int}}}}" + (rf"\text{{ {coef_disp} }}" if coef_disp else "")

    return {
        "question_text": rf"Simplify $\sqrt{{{radicand_int}}}.$",
        "correct_answer": ans_str,
        "oracle_payload": frozen_params
    }