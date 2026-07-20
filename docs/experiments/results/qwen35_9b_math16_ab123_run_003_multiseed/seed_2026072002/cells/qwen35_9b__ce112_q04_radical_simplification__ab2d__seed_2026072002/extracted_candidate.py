def generate(level=1, **kwargs):
    frozen_params = {"radicand": 135} # Must exactly equal the frozen sampled parameters
    
    radicand_input = frozen_params.get("radicand", kwargs.get("radicand", 0))
    
    coeff_in, _ = RadicalOps.simplify_term(1, radicand_input)
    new_radicand, remainder = RadicalOps.simplify_term(radicand_input // (coeff_in**2), None) # This logic is flawed in thought trace
    
    # Correct Logic for Task: simplify sqrt(n). 
    c, r = RadicalOps.simplify_term(1, radicand_input)
    
    # Re-implement simplification correctly inside generate to ensure correctness based on domain API usage constraints if they existed differently.
    # But I must use the imported functions defined above or similar logic adhering to contract.
    # The Domain section defines RadicalOps.simplify_term taking (coeff, radicand). 
    # Let's re-run strictly:
    
    c_initial = 1
    r_input = radicand_input
    
    simplified_coeff, square_free_rad = RadicalOps.simplify_term(c_initial, r_input)
    
    final_c_str = str(simplified_coeff)
    if abs(float(final_c_str)) == 1 and int(simplified_coeff) > 0:
        latex_part = f"+\\sqrt{{{square_free_rad}}}" # No coeff displayed for +1
        latex_part = latex_part.replace("+", "") 
    elif float(final_c_str) < 0 or (int(float(final_c_str)) == -1):
         if int(simplified_coeff) == -1:
             latex_part = f"-\\sqrt{{{square_free_rad}}}"
         else:
            # Should not happen with this API logic for positive radicand start, but safe check
            c_abs = abs(int(float(final_c_str)))
            sign = "-" if simplified_coeff < 0 else "+" 
            latex_part = f"{sign}{c_abs}\\sqrt{{{square_free_rad}}}"
    else:
        # Integer > 1 or Fraction (unlikely for this specific task but handled)
         c_val = int(simplified_coeff)
         if c_val == 0: return "0"
         
         sign = "+" if simplified_coeff > 0 else "-" 
         latex_part = f"{sign}{c_val}\\sqrt{{{square_free_rad}}}"

    # Construct correct_answer dict structure implied by contract? No, correct_answer must include coefficient, radicand, canonical_latex.
    # Wait: "correct_answer must include coefficient, radicand, and canonical_latex." -> This implies a dictionary inside the return or specific fields? 
    # Re-read: "return a dict with exactly question_text, correct_answer, and oracle_payload".
    # And for 'correct_answer': "must include coefficient, radicand, and canonical_latex". 
    # Does this mean correct_answer IS a dict {coeff, radicand, latex}? Or just the string? Usually in these tasks, correct_answer is the ground truth string.
    # However, if it says "include...", maybe it's an object. Let's assume standard format where correct_answer is the canonical_latex string for grading systems, BUT strict reading suggests a dict structure might be needed IF the system expects structured data. 
    # Given typical patterns: question_text (str), correct_answer (str - the latex solution).
    # But if it says "must include...", let's look at oracle_payload which is params. 
    # Let's assume correct_answer is just the canonical_latex string, as that is standard for 'answer'. The description might mean the answer object contains these properties conceptually or I should return a dict for correct_answer?
    # Let's stick to returning the LaTeX string as correct_answer unless explicitly told it must be an object. 
    # Actually, re-reading: "correct_answer must include coefficient, radicand, and canonical_latex". This strongly implies `correct_answer` is a dictionary containing these keys.
    
    answer_obj = {
        "coefficient": simplified_coeff if abs(float(final_c_str)) != 1 else (1 if float(final_c_str) > 0 else -1), # Adjust for sign display logic? 
                   # Actually, let's just store the integer value used in latex generation.
                   # If displayed as "+\sqrt...", coeff is 1. "-\\sqrt", coeff is -1. "\\sqrt", coeff is 1 (implicit).
        "radicand": square_free_rad,
        "canonical_latex": latex_part.replace("+ ", "").replace(" + ", "") if False else latex_part # Clean up spaces? 
    }

    # Refine answer_obj to be clean:
    final_coeff_val = simplified_coeff
    if abs(final_c_str) == 1 and int(simplified_coeff) > 0:
        # Displayed as just sqrt, so coefficient is effectively 1 but not shown. 
        # If the requirement says "include", maybe we store it regardless of display? Or set to None/1? Let's use simplified_coeff logic.
        pass
    
    clean_latex = latex_part.replace(" + ", "").replace("+\\sqrt", "\\sqrt") if "+" in latex_part and not latex_part.startswith("-") else latex_part.replace("\\frac{+}{...}", "") # Basic cleanup for leading plus
    # Simpler: The RadicalOps.format_term handles this? I wrote my own logic above. Let's use a helper or clean string directly.
    
    # Recalculate cleanly using the API call pattern strictly if possible, but since format_term is defined with specific args, let's try to use it properly for the final latex generation step in thought process (though implementation uses manual cleanup).
    # To be safe and compliant: 
    c_str = str(simplified_coeff)
    
    def get_latex(c, r):
        if c == 0: return "0"
        num, den = Fraction(c).numerator, Fraction(c).denominator
        
        s_num = str(abs(num))
        
        term_base = f"{s_num}\\sqrt{{{r}}}"
        
        sign_prefix = ""
        val_float = float(c)
        if val_float < 0:
            return "-" + get_latex(-c, r) # Recursion for negative
        
        # If coefficient is fraction? 
        if den != 1 and abs(val_float) > 0.95: # Float check fallback or exact frac check
             pass
            
        # Check if coeff should be omitted (magnitude 1 integer)
        if num == den: # i.e., value is integer magnitude 1 -> wait, Fraction(2)/Fraction(2)=1? No. 
            # c = simplified_coeff from API which returns int usually for level 1? 
            pass
            
        return term_base

    # Let's rebuild the string properly based on standard math latex rules:
    coeff_val = simplified_coeff
    
    if abs(float(coeff_val)) == 1 and int(coeff_val) > 0:
       final_latex = f"+\\sqrt{{{square_free_rad}}}" 
       # Standard convention often omits leading +. But prompt says "complete single-term LaTeX including coefficient/sign". 
       # If coeff is implicit, usually omitted. Let's assume standard simplification output (no leading +).
       
    if int(coeff_val) == 1:
        final_latex = f"\\sqrt{{{square_free_rad}}}"
    elif int(coeff_val) < -1 or float(coeff_val) != 0 and abs(float(coeff_val)) > 1: # Integer case from API
         sign = "+" if coeff_val > 0 else "-"
         val_str = str(abs(int(coeff_val)))
         final_latex = f"{sign}{val_str}\\sqrt{{{square_free_rad}}}"
    elif int(coeff_val) == -1 or (isinstance(coeff_val, float) and abs(float(coeff_val)-int(float(coeff_val))) < 1e-9): # Negative unit integer
        sign = "-" if coeff_val < 0 else "+" 
        final_latex = f"{sign}\\sqrt{{{square_free_rad}}}"

    return {
        "question_text": r"Simplify the radical: $\\sqrt{" + str(square_free_rad) + "}$",
        "correct_answer": {
            "coefficient": coeff_val if abs(float(coeff_val)) != 1 else (coeff_val), # Store actual value used for math check, even if display omits it. Or maybe just the displayed coefficient? 
                            # Let's store what is visually present or implicit. If omitted, usually represented as 1 in data structures but hidden in latex.
                            # I will return coeff_val itself (int).
            "radicand": square_free_rad,
            "canonical_latex": final_latex.replace(" + ", "").replace("+\\sqrt", "\\sqrt") if "+" == final_latex[0] else final_latex
        },
        "oracle_payload": frozen_params
    }