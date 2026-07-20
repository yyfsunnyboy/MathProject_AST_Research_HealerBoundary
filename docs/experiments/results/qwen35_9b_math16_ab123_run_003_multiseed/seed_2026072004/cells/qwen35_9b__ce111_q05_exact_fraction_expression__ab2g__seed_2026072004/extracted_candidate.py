def generate(level=1, **kwargs):
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Manual calculation of the exact fraction:
    # Term 1: 9/22
    # Term 2: 11/18
    # Inner Parenthesis: (23/22 - 7/18) = (414/396 - 154/396) = 260/396 = 65/99
    
    # Expression = 9/22 + 11/18 - 65/99
    # Common denominator for 22, 18, 99: LCM(22, 18) = 198. 
    # Note: 99 is a factor of 198 (198 / 99 = 2). So LCD is 342?
    # Let's re-evaluate denominators: 22 = 2*11, 18=2*3^2. LCM(22, 18) = 2 * 11 * 9 = 198.
    # Since we have terms with denom 22 and 18, LCD is 198. 
    # Wait, the inner term result was 65/99. We need LCM(198, 99). 
    # 99 = 9*11. 198 = 2 * 99. So LCM(198, 99) is 198.
    
    from math import gcd
    
    def lcm(a, b):
        return abs(a*b) // gcd(a,b)

    # Recalculate carefully step-by-step to ensure correctness for the output string.
    # Term A: 9/22
    # Term B: 11/18 -> simplify? No need yet.
    # Inner C: (23/22 - 7/18)
    #   LCD(22, 18) = 198
    #   23*9 / 198 - 7*11 / 198 = 207/198 - 77/198 = 130/198
    #   Simplify 130/198: divide by 2 -> 65/99. Correct.
    
    # Total Expression A + B - C_simplified
    # 9/22 + 11/18 - 65/99
    # LCD(22, 18, 99) = LCM(LCM(22,18), 99) = LCM(198, 99) = 198.
    
    # Convert to denominator 198:
    # A (9/22): 9 * (198//22) / 198 = 9*9 / 198 = 81/198
    # B (11/18): 11 * (198//18) / 198 = 11*11 / 198 = 121/198
    # C_simp (65/99): 65 * (198//99) / 198 = 65*2 / 198 = 130/198
    
    # Numerator sum: 81 + 121 - 130
    num_val = 81 + 121 - 130
    den_val = 198
    
    final_num = num_val
    final_den = den_val
    
    g_final = gcd(final_num, final_den) if (final_num != 0 or final_den != 0) else 1
    canonical_num = final_num // g_final
    canonical_den = final_den // g_final
    
    # Handle sign logic for LaTeX formatting properly
    latex_parts = []
    
    def format_frac(n, d):
        if n == 0: return "0"
        common_gcd = gcd(abs(n), abs(d))
        nn, dd = abs(n)//common_gcd, abs(d)//common_gcd
        
        sign_str = "-" if (n < 0) ^ (d < 0) else ""
        
        # Determine layout: simple inline or display style? Usually inline for single expression.
        # But we need canonical_latex specifically. 
        return f"{sign_str}\\frac{{{nn}}}{{ {dd} }}"

    # Re-calculate components with proper LaTeX formatting logic inside the function to be safe,
    # though here values are fixed. Let's construct the string directly based on calculated integers.
    
    term1_num = 9 * (lcm(22, 18) // 22) # Wait, LCD is 342? 
    # Re-re-check LCM logic.
    # Denominators involved: 22, 18, 99.
    # Primes: 22=2*11; 18=2*3^2; 99=3^2*11.
    # Max powers: 2^1 * 3^2 * 11^1 = 2 * 9 * 11 = 198. 
    # Yes, LCD is 198. My previous manual calc was correct.
    
    term1_scaled_numerator = 9 * (198 // 22) # 9*9=81
    term2_scaled_numerator = 11 * (198 // 18) # 11*11=121
    inner_term_num = 65 * (198 // 99)         # 65*2=130
    
    total_numer = term1_scaled_numerator + term2_scaled_numerator - inner_term_num
    # 81 + 121 - 130 = 72. Wait: 202 - 130 = 72? 
    # Let's re-add: 9+11=20 -> 81+121=202.
    # 202 - 130 = 72.
    
    total_denom = 198
    
    simpl_gcd_val = gcd(abs(total_numer), abs(total_denom))
    final_numerator = total_numer // simpl_gcd_val
    final_denominator = total_denom // simpl_gcd_val
    
    # Construct LaTeX parts for the question text using standard formatting logic derived from inputs
    def make_latex_frac(n, d):
        if n == 0: return "0"
        sgn = "-" if (n < 0) != (d < 0) else ""
        num_abs = abs(n)
        den_abs = abs(d)
        
        # Simple fraction format for text
        return f"{sgn}\\frac{{{num_abs}}}{{ {den_abs} }}"

    latex_term1 = make_latex_frac(9, 22)
    latex_term2 = make_latex_frac(11, 18)
    
    # Inner part: (23/22 - 7/18)
    inner_part_num_raw = 23 * (lcm(22, 18)//22) - 7 * (lcm(22, 18)//18)
    # 207 - 77 = 130. Denom 198. Simplifies to 65/99.
    
    latex_inner_part_left = make_latex_frac(23, 22)
    latex_inner_part_right = make_latex_frac(7, 18)
    inner_result_numerator_raw = 130
    inner_result_denominator_raw = 198
    
    # For the question text, we show original expression as given in frozen params.
    question_text = f"Simplify: {expression}"
    
    canonical_latex_str = make_latex_frac(final_numerator, final_denominator)

    return {
        "question_text": question_text,
        "correct_answer": {
            "numerator": final_numerator,
            "denominator": abs(final_denominator), # Denom should be positive in standard form usually, but math16 might expect sign handling. Standard canonical: denom > 0.
            "canonical_latex": canonical_latex_str
        },
        "oracle_payload": {"expression": expression}
    }