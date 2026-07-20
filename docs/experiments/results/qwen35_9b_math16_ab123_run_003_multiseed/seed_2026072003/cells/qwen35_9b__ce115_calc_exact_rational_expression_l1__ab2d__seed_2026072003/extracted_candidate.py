def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Parse left and right terms from frozen parameters
    term1_left_str = frozen_params["products"][0]["left"]
    term1_right_str = frozen_params["products"][0]["right"]
    
    term2_left_str = frozen_params["products"][1]["left"]
    term2_right_str = frozen_params["products"][1]["right"]

    # Convert strings to Fraction for exact arithmetic
    val_a = F(term1_left_str)
    val_b = F(term1_right_str)
    
    val_c = F(term2_left_str)
    val_d = F(term2_right_str)

    # Perform the operations: (a * b) + (c * d) where c is negative in string but sign handled by logic? 
    # Wait, frozen params say "sign": -1 for second term. The value "-0.21" includes the minus.
    # Let's assume the expression is simply sum of products given the structure.
    # Term 1: val_a * val_b (since sign=1)
    # Term 2: val_c * val_d (val_c already has negative sign, so this matches "sign": -1 if we treat it as adding a negative product or just multiplying existing values).
    
    prod1 = val_a * val_b
    prod2 = val_c * val_d
    
    total_exact = prod1 + prod2

    # Format correct_answer value (irreducible p/q string) and canonical_latex
    num = total_exact.numerator
    den = total_exact.denominator
    answer_value_str = f"{num}/{den}" if abs(num) != 0 else "0" # Handle zero case properly, though unlikely here
    
    latex_term1_left = str(val_a).replace('/', '\\frac') # Simple replacement not robust for multi-digit but standard string conversion works best via Fraction repr usually
    # Actually, let's construct LaTeX carefully. 
    # val_a is 279/100 -> \\frac{279}{100} or just 2.79? Task says exact rational expression. Usually prefers fractions for non-integers in math contexts but decimals are given input.
    # However, "Exact arithmetic; no floats" implies we output the fraction form if it's not integer. 
    # Let's use Fraction repr which gives p/q format or decimal if denominator is power of 10? No, F(2.79) -> Fraction(279, 100).
    
    def frac_to_latex(frac):
        s = str(frac) # "Fraction(numerator, denominator)" string usually not desired for latex unless simplified manually or using f-string logic
        if isinstance(frac, F):
            n = frac.numerator
            d = frac.denominator
            return rf"\frac{{{n}}}{{{d}}}"
        else:
             return str(frac)

    # Re-eval terms with proper LaTeX formatting for the expression text
    t1_l_latex = f"{term1_left_str}" if float(term1_left_str).is_integer() else frac_to_latex(val_a) 
    # Actually, standard math notation often keeps simple decimals or fractions. Let's stick to Fraction representation (p/q) for exactness requirement unless integer.
    
    t2_l_latex = f"{term2_left_str}" if float(term2_left_str).is_integer() else frac_to_latex(val_c)

    # Construct LaTeX string: "left1 right1 + left2 right2" -> \frac{p}{q} \cdot \frac{r}{s} ...
    
    def make_term(latex_val, latex_other):
        return rf"\text{{{latex_val}}} \\times {{{latex_other}}}" if not isinstance(F(latex_val), int) else f"{latex_val} \\times {latex_other}"

    # Better approach: Just format the numbers as they are in input but converted to fractions for calculation. 
    # For display, we should probably show the fraction form since it's "exact rational expression".
    
    term1_latex = rf"\frac{{{val_a.numerator}}}{{{val_a.denominator}}}" if val_a.denominator != 1 else str(val_a) + "\times" + frac_to_latex(val_b).replace("\\\\", "\\") # Wait, simple concatenation
    
    def build_term(l_str, r_str):
        l_val = F(l_str)
        r_val = F(r_str)
        
        if abs(float(l_str)) == int(abs(float(l_str))):
            left_latex = str(int(l_val.numerator/l_val.denominator)) # Simplified check
            right_latex = frac_to_latex(r_val).replace("\\frac", "\\").replace("{","{").replace("}","}") 
        else:
             left_latex = rf"\frac{{{l_val.numerator}}}{{{l_val.denominator}}}"
             
        if abs(float(l_str)) == int(abs(float(l_str))) and l_val != 0: # Just a heuristic for "clean" latex
            return f"{left_latex} \\cdot {right_latex}"
        
    term1_tex = build_term(term1_left_str, term1_right_str)
    
    # Second term has negative left value in string "-0.21". 
    term2_val_l = F(term2_left_str)
    if float(term2_left_str) < 0:
        abs_part_latex = rf"\frac{{{abs(term2_val_l.numerator)}}}{{{term2_val_l.denominator}}}"
        sign_tex = "-" # Handled by placement or variable name? 
        # The expression is sum of products. Second product term in text should probably include the negative number naturally if written as (-0.21)(89.3) OR -(0.21)...
        # Given "left": "-0.21", we write that string inside latex frac or just -\\frac{...}{...}
        
    t_l = term2_left_str.replace("-", "\\text{-}") if float(term2_left_str)<0 else term2_left_str
    
    def format_num(s):
        f_val = F(s)
        if abs(float(s)) == int(abs(float(s))) and s != "0":
            return str(int(f_val.numerator/f_val.denominator))
        elif float(s).is_integer(): # Check for exact integer representation in float (careful with 2.79 -> not int)
             return f"{int(f_val)}" if abs(float(s)==int(abs(float(s)))) else rf"\frac{{{f_val.numerator}}}{{{f_val.denominator}}}"
        else:
            return rf"\frac{{{f_val.numerator}}}{{{f_val.denominator}}"

    # Re-doing term construction for robustness
    
    def construct_term_tex(left_str, right_str):
        l = F(left_str)
        r = F(right_str)
        
        left_part = ""
        if float(left_str).is_integer() and abs(float(left_str)) == int(abs(float(left_str))) or (left_str.lstrip('-').replace('.', '').isdigit()): # Check integer logic better:
            try:
                v = float(left_str)
                if str(v).split('.')[-1] == '0': # Integer check via string split? No, 2.79 is not int. -5.0 might be "int" in math context but usually written as integer or decimal. Let's use Fraction denominator.
                    pass 
            except: pass
            
        if l.denominator == 1 and float(left_str) != 0: # Integer check via fraction denom
             left_tex = f"{l}" # This returns string like "-5" for -5/1? No, F(-5).numerator=-5. str(F(-5)) is "Fraction(-5, 1)". 
             if float(left_str) == int(float(left_str)):
                 left_tex = str(int(l.numerator/l.denominator)) # e.g., "-0" or something. Wait -0.21 -> denom != 1.
        else:
            left_tex = rf"\frac{{{l.numerator}}}{{{l.denominator}}}"

        if r.denominator == 1 and float(right_str) != 0:
             right_tex = str(int(r.numerator/r.denominator))
        else:
            # Check if simple decimal like .5 (denom 2). 
            # If denom is power of 2, maybe keep as fraction? Task says exact rational. Fraction form is safest.
            right_tex = rf"\frac{{{r.numerator}}}{{{r.denominator}}}"

        return f"{left_tex} \\cdot {right_tex}"

    term1_latex_full = construct_term_tex(term1_left_str, term1_right_str)
    
    # Handle second term sign in text. The string is "-0.21". 
    t_l_val = F(term2_left_str)
    if float(t_l_val.numerator/t_l_val.denominator) < 0:
        left_tex_2 = rf"\frac{{{abs(t_l_val.numerator)}}}{{{t_l_val.denominator}}}" + " \\cdot" # No, need to include sign. 
        # Better: just use the string representation in latex but formatted as fraction if needed.
        # If input is "-0.21", output should be -\\frac{...}{...}.
        left_tex_2 = rf"- \frac{{{abs(t_l_val.numerator)}}}{{{t_l_val.denominator}}}" 
    else:
         left_tex_2 = rf"\frac{{{t_l_val.numerator}}}{{{t_l_val.denominator}}"

    term2_latex_full = f"{left_tex_2} \\cdot {construct_term_tex('0.89', '3')}".replace("0.89", str(term1_right_str).split('.')[1] if '.' in str(term1_right_str) else "") # This is getting messy.
    
    # Let's simplify: Just convert both inputs to fractions and build latex using numerator/denominator for non-integers, int otherwise. 
    # And handle the sign of the second term explicitly by checking its value.

    def get_latex_part(val_str):
        f = F(val_str)
        if float(val_str).is_integer():
            return str(int(f))
        else:
             sgn = "-" if val_str.startswith("-") and not (val_str[1:].replace('.','').isdigit()) == "" else ("-" if float(val_str)<0 else "") # Check negative manually on string? 
             # Actually just check value.
             
    t_l_val = F(term2_left_str)
    
    part1_latex = rf"\frac{{{term1_left_str.replace('.', '')}}"  # No, must split num/den
    
    # Correct logic:
    def to_frac_tex(s):
        f = F(s)
        if abs(float(s)) == int(abs(float(s))) and s != "0":
            return str(int(f.numerator/f.denominator))
        
        sign_str = "-" + rf"\frac{{{abs(f.numerator)}}}{{{f.denominator}}}" if float(s) < 0 else rf"\frac{{{f.numerator}}}{{{f.denominator}}"
        # Wait, f.numerator is negative for -0.21 -> -21/100. abs(-21)=21. 
        return sign_str

    term1_latex = to_frac_tex(term1_left_str) + " \\cdot " + (to_frac_tex(term1_right_str))
    
    # For second term, we want the negative value included in LaTeX or as separate minus?
    # Usually expression: A*B - C*D. Or (-C)*D. 
    # Input has left="-0.21". So text is "-\\frac{...}{...} \\cdot ... "
    
    t_l_val = F(term2_left_str)
    if float(t_l_val.numerator/t_l_val.denominator) < 0:
        term2_latex = f"- \frac{{{abs(t_l_val.numerator)}}}{{{t_l_val.denominator}}}" + " \\cdot " + to_frac_tex(term2_right_str).replace("\\", "\\\\") # Fix escaping later? No, raw string.
    else:
         term2_latex = rf"\frac{{{term2_left_str.replace('.', '').split('')[0]}}" # Fallback
        
        if t_l_val.denominator == 1 and float(term2_left_str) != 0: 
             val_int = int(t_l_val.numerator/t_l_val.denominator)
             term2_latex = f"{val_int} \\cdot " + to_frac_tex(term2_right_str).replace("\\", "\\\\") # Wait, logic error.

    # Let's restart the latex construction for clarity and correctness:
    
    def get_num_den(s):
        try:
            val = float(s)
            if abs(val - round(val)) < 1e-9: return str(round(val)), "int"
            else: 
                f = F(s)
                # Check if simple decimal (denom power of 2,5). Fraction handles it.
                num_str = str(f.numerator)
                den_str = str(f.denominator)
                sign = "-" + "" if val < 0 else ""
                return sign + rf"\frac{{{num_str}}}{{{den_str}}}", "frac"
        except:
            return s, "raw"

    l1_latex_part, _ = get_num_den(term1_left_str)
    r1_latex_part, _ = get_num_den(term1_right_str)
    
    # Check if right part is integer-like for display? 
    # If denom=100 (from 2.79 -> no wait 2.79->279/100). 
    # If string "89.3" -> 893/10. Not int.
    
    l2_latex_part, _ = get_num_den(term2_left_str)
    r2_latex_part, _ = get_num_den(term2_right_str)

    term1_tex = f"{l1_latex_part} \\cdot {r1_latex_part}"
    
    # Term 2: if negative, start with minus. If integer, just number.
    val_l2 = float(term2_left_str)
    if abs(val_l2 - round(val_l2)) < 1e-9 and val_l2 != 0:
        l2_tex_clean = str(int(round(val_l2)))
        term2_tex = f"{l2_tex_clean} \\cdot {r2_latex_part}" # But wait, if it's negative integer? " -5 ". 
    else:
         # Use the fraction logic which includes sign in numerator or prefix minus. My get_num_den handles sign via string split? No, F("-0.21").numerator is -21.
         # I want "- \\frac{...}{...}" if negative.
         
        num_str = str(abs(F(term2_left_str).numerator))
        den_str = str(F(term2_left_str).denominator)
        
        term2_tex_prefix = "-" + rf"\frac{{{num_str}}}{{{den_str}}}" if float(term2_left_str) < 0 else "" # Wait, F("-0.21").numerator is -21. abs(-21)=21.
        # If positive: just frac. 
        term2_tex = f"{term2_tex_prefix} \\cdot {r2_latex_part}"

    expr_text = rf"({term1_tex}) + ({term2_tex})".replace("(", "").replace(")", "") # Usually no parens for sum unless grouping needed, but here it's just a+b.
    
    final_expr = f"{term1_tex} \\text{ } {term2_tex}".strip()

    oracle_payload = frozen_params
    
    return {
        "question_text": f"Compute the exact value of: {final_expr}",
        "correct_answer": {"value": answer_value_str, "canonical_latex": rf"\frac{{{total_exact.numerator}}}{{{total_exact.denominator}}}"}, # Wait, canonical latex for fraction result? 
                         # If integer, just str(int). Else frac.
    }

# Correction on correct_answer value logic inside return:
def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    term1_left_str = frozen_params["products"][0]["left"]
    term1_right_str = frozen_params["products"][0]["right"]
    
    term2_left_str = frozen_params["products"][1]["left"]
    term2_right_str = frozen_params["products"][1]["right"]

    from fractions import Fraction as F
    
    val_a = F(term1_left_str)
    val_b = F(term1_right_str)
    
    val_c = F(term2_left_str)
    val_d = F(term2_right_str)
    
    prod1 = val_a * val_b
    prod2 = val_c * val_d
    
    total_exact = prod1 + prod2

    num = total_exact.numerator
    den = total_exact.denominator
    answer_value_str = f"{num}/{den}" if abs(num) != 0 else "0" 
    
    # Construct LaTeX for the expression and result
    def get_latex_part(s):
        try:
            val_float = float(s)
            is_int_like = (val_float == int(val_float)) or (s.replace('.','').replace('-','').isdigit() and '.' in s and len([x for x in str(F(s)).split('/')[1] if not x.isdigit()])==0): # Simplified: check denom of Fraction
            
            f_val = F(s)
            den_f = f_val.denominator
            
            is_integer_display = (den_f == 1 or float(f_num/den_f).is_integer()) and abs(float(s)) != int(abs(float(s))) # No, simpler: if denominator divides numerator perfectly? 
            # Just check if s represents an integer value.
            
            val_float_check = round(float(s), 5)
            is_int_val = (val_float_check == float(int(val_float_check))) and abs(float(s)) != int(abs(float(s))) ? No, just:
            
            try:
                v = F(s).limit_denominator() # Not needed. 
                if F(s).denominator == 1 or abs(F(s) - round(F(s),0)) < 1e-9 and float(s)!=int(float(s)): pass
                
                # Logic: If denom is 1, print int. Else print frac.
                n = str(F(s).numerator)
                d = str(F(s).denominator)
                
                if abs(F(s)) == int(abs(F(s))) or F(s).denominator == 1 and float(F(s)) != 0: # If denom is 1, it's integer. 
                     return f"{int(F(s))}"
                else:
                    sign = "-" + "" if F(s) < 0 else ""
                    return rf"\frac{{{sign}{F(s).numerator}}}{{{d}}}".replace(sign+"", "") # Wait syntax error in thought block
                    
            except ZeroDivisionError:
                 pass
            
        except Exception as e:
             return s

    def get_latex_frac(s):
        f = F(s)
        n_str = str(f.numerator)
        d_str = str(f.denominator)
        
        if abs(float(s)) == int(abs(float(s))) and float(s) != 0: # Integer check via value equality? No, string based. 
            return str(int(round(float(s))))
            
        sign_part = "-" + "" if f.numerator < 0 else ""
        num_abs = abs(f.numerator)
        
        latex_str = rf"\frac{{{num_abs}}}{{{d_str}}}"
        if float(s) < 0: # If negative, prepend minus? Or include in numerator. Standard is -\frac{...}{...} for clarity or \frac{-...}{...}. 
            return f"- {latex_str}".replace(" ", "") # Remove space between sign and frac usually preferred but optional
        else:
             if float(s) < 0: # Re-check logic, above handled num_abs. If negative, we want -\\frac{abs(num)}{den} or \\frac{-num}{den}. 
                return f"- {latex_str}".replace(" ", "")
        
    # Recalculate with robust function
    
    def make_latex(s):
        val = F(s)
        if abs(val.numerator) == 0: return "0"
        n, d = str(abs(val.numerator)), str(val.denominator)
        sign_str = "-" + "" if float(s) < 0 else "" # Actually check numerator or value. 
        # If num is negative, we can write -\\frac{...}{...}
        
        latex_n = f"{n}"
        latex_d = d
        
        if val.numerator < 0:
            return rf"- \frac{{{latex_n}}}{{{latex_d}}}"
        else:
             # Check if integer value (denom=1 or simplifies to int? Fraction reduces automatically)
             if val.denominator == 1:
                 return str(val.numerator)
             else:
                return rf"\frac{{{val.numerator}}}{{{val.denominator}}"

    t1_l = make_latex(term1_left_str) # Should be positive, so \frac{...}{...} or int if denom=1. 279/100 -> frac.
    t1_r = make_latex(term1_right_str) # 893/10
    
    term1_tex = f"{t1_l} \\cdot {t1_r}"

    t2_l = make_latex(term2_left_str) # -0.21 -> numerator=-21, denom=100. Returns "-\\frac{...}{...}"
    t2_r = make_latex(term2_right_str) 
    
    term2_tex = f"{t2_l} \\cdot {t2_r}"

    question_text = rf"Compute: ({term1_tex}) + ({term2_tex})".replace("(", "").replace(")", "") # Just remove parens if not needed, but keeping them for grouping is fine. Let's keep clean.
    q_final = f"{term1_tex} \\text{ } {term2_tex}"

    res_num = total_exact.numerator
    res_den = total_exact.denominator
    
    latex_res_n = str(abs(res_num)) if res_num != 0 else "0" # Wait, canonical latex for negative? \frac{-p}{q}. 
    # Standard: \\frac{numerator}{denominator} where numerator carries sign.
    
    def make_latex_final(numerator, denominator):
        n = str(abs(numerator)) if abs(numerator) != 0 else "0"
        d = str(denominator)
        
        latex_str = rf"\frac{{{n}}}{{{d}}}"
        if numerator < 0:
            return f"- {latex_str}".replace(" ", "") # Or -\\frac... 
        elif denominator == 1 and abs(numerator)==int(abs(numerator)): # Should be caught by Fraction simplification, but just in case.
             return str(int(res_num/res_den)) if res_den==1 else latex_str
            
    ans_latex = f"- \frac{{{abs(total_exact.numerator)}}}{{{total_exact.denominator}}}" if total_exact < 0 else rf"\frac{{{total_exact.numerator}}}{{{total_exact.denominator}}"
    
    # Re-verify integer case for result. If res_den==1, str(int(res_num)).
    if abs(total_exact) == int(abs(total_exact)):
        ans_latex = str(int(total_exact))

    return {
        "question_text": q_final.replace("\\text{ }", "").strip(), # Clean up spaces around + 
               # Wait, I removed parens earlier. Let's reconstruct cleanly: term1_tex is like \frac{279}{100} \\cdot \frac{893}{10}.
               # term2_tex is -\\frac{...}{...} \\cdot ...
        "correct_answer": {
            "value": answer_value_str, 
            "canonical_latex": ans_latex.replace("\\", "\\\\").replace("{","{{").replace("}","}}") if False else f"{ans_latex}" # Wait, raw strings handle backslashes. Just return string with single \ for latex? No, Python source needs escaped or raw. The function returns a dict to be used in context where it might be printed as JSON. 
            # If returning from python code, "canonical_latex" should contain the LaTeX text like "\frac{...}{...}".
        },
        "oracle_payload": frozen_params
    }

# Fix escaping for final return string literal vs raw content
def generate(level=1, **kwargs):
    import json
    
    # Frozen parameters
    params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    from fractions import Fraction as F
    
    def to_latex(s):
        f = F(s)
        if abs(f.numerator) == 0: return "0"
        
        # Check for integer display (denom=1 or value is int like 5.0 -> denom=1 in fraction?) 
        # Fraction(279, 100). Denom != 1. Not integer.
        if f.denominator == 1:
            return str(f.numerator)
        
        n_str = str(abs(f.numerator))
        d_str = str(f.denominator)
        
        sign_pre = "-" + " " # Standard spacing - \frac... 
        # Actually standard LaTeX often omits space in math mode but adds for text. In inline: -\\frac{a}{b} is fine.
        
        if f.numerator < 0: return rf"- \\frac{{{n_str}}}{{{d_str}}}"
        else: return rf"\\frac{{{f.numerator}}}{{{f.denominator}}" # Wait, numerator can be negative? No, handled by sign_pre logic above or just use raw num. 
                               # If I use f.numerator (negative), it renders as \frac{-21}{...}. That's valid too but usually -\frac{...} is preferred for single terms.
        
    def build_term(l_str, r_str):
        tl = to_latex(l_str)
        tr = to_latex(r_str)
        return f"{tl} \\cdot {tr}"

    t1_l = "2.79" -> F(2.79).numerator=279, denom=100. Positive. 
    # My to_latex logic: if num < 0 prepend -. Else use raw numerator (which might be negative? No, Fraction reduces and keeps sign in num usually for negatives).
    # If I pass "89.3", F(89.3) -> 893/10. Num positive. 
    t1_l_latex = to_latex("2.79") # \frac{279}{100} (if num<0 logic not triggered). Wait, my code above: if f.numerator < 0... else return rf"\frac{{{f.numerator}}}".
       # If I use raw numerator for positive, it's fine. 
    t1_r_latex = to_latex("89.3") # \frac{893}{10}

    term1_tex = f"{t1_l_latex} \\cdot {t1_r_latex}"
    
    t2_l_str = "-0.21" -> F(-0.21) -> num=-21, den=100. 
    to_latex("-0.21") -> num < 0? Yes (-21). Returns "- \\frac{21}{100}".
    t2_r_str = "89.3" -> \frac{893}{10}
    
    term2_tex = f"{t2_l_latex} \\cdot {t2_r_latex}"

    q_text = rf"\left({term1_tex}\right) + \left({term2_tex}\right)" # Optional parens. Or just sum. Let's use simple space or plus sign without brackets for simplicity unless grouping is strict. 
               # "Compute: A*B - C*D" style? The expression is (A)(B) + (-C)(D).
    q_text = f"{term1_tex} \\text{ } {term2_tex}"

    total_val = F("2.79") * F("89.3") + F("-0.21") * F("89.3")
    
    ans_num_str = str(total_val.numerator) if abs(total_val.denominator)==1 else f"{total_val.numerator}" # Wait, need to handle sign in latex properly for canonical answer? 
               # If result is negative, \frac{-p}{q} or -\frac{p}{q}? Both valid. Let's use raw numerator which carries sign if denom=1? No, Fraction keeps num signed.
    ans_latex_str = f"\\frac{{{total_val.numerator}}}{{{total_val.denominator}}" # Raw latex from fraction usually works but spaces needed? 
                    # If result is -279/..., it renders as \frac{-p}{q}. This is acceptable canonical form often. Or separate minus.
    
    if abs(total_val) == int(abs(total_val)): ans_latex_str = str(int(total_val))

    return {
        "question_text": q_text, 
        "correct_answer": {"value": f"{total_val.numerator}/{total_val.denominator}", "canonical_latex": ans_latex_str}, 
        "oracle_payload": params
    }