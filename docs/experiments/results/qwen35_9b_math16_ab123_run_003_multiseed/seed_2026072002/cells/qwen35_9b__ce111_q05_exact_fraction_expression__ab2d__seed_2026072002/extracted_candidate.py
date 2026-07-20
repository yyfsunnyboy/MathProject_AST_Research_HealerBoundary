def generate(level=1, **kwargs):
    frozen_params = {"expression": "9/22 + 11/18 - (23/22 - 7/18)"}
    
    # Parse the expression manually using FractionOps for correctness and canonical form
    
    expr_str = frozen_params["expression"]
    
    # Split into tokens to handle operations safely without eval on raw strings if possible, 
    # but given constraints, we will parse components.
    from fractions import Fraction
    
    def clean(s): return s.replace(" ", "")
    
    parts1 = [clean(x) for x in expr_str.split("+")]
    parts2 = [clean(y) for y in parts1] # This is naive splitting; let's do a robust parse
    
    # Robust parsing of "9/22 + 11/18 - (23/22 - 7/18)"
    import re
    expr_cleaned = clean(expr_str)
    
    # Replace subtractions with addition of negatives for uniform processing if needed, 
    # but standard Python Fraction handles string parsing well.
    # Let's evaluate step-by-step to ensure canonical form logic is applied via domain APIs conceptually
    
    try:
        f1 = frac_create(expr_cleaned.split("+")[0])
        
        term2_str = expr_cleaned.split(" + ")[-1]
        if "-" in term2_str and "(" not in term2_str: # Simple subtraction case at end or middle
             pass
        
        # Actually, let's just use Python's Fraction directly for the calculation 
        # as per "use domain API" instruction implies using them where possible. 
        # Since `create` handles strings with '/', we can build up terms.
        
        # Term 1: 9/22
        t1 = frac_create("9/22")
        
        # Term 2: + 11/18
        t2 = frac_add(t1, frac_create("11/18"))
        
        # Term 3 part A: -(23/22) -> - (23/22)
        inner_a = frac_create("23/22")
        
        # Term 3 part B: - (-7/18) inside parens? No, expression is ... - (A - B) => -A + B
        inner_b = frac_create("7/18")
        paren_val = frac_add(inner_a, frac_sub := lambda a,b: frac_add(a, frac_create("-" + str(b.numerator)+"/"+str(b.denominator))) if False else None ) # Placeholder logic
        
        # Correct Logic for -(23/22 - 7/18):
        inner_diff = frac_add(frac_create("23/22"), frac_create("-1") * frac_create("7/18")) 
        # Actually: (23/22) + (-7/18). Let's use add(a, b) where b is negative.
        
        from fractions import Fraction as F
        
        t_sub = F(0) - inner_diff # -(A-B) = B-A ? No. -(A-B) = -A+B.
        # So we need: (-1)*inner_a + (1)*inner_b
        neg_inner_a = frac_add(F(-23), F(22)) # -23/22? No, create takes string "num/den" usually positive or negative numerator
        
        let's restart the calculation strictly using `create` and `add`.
        
        term1 = frac_create("9/22")
        term2 = frac_add(term1, frac_create("11/18")) # 9/22 + 11/18
        
        sub_term_a = frac_create("-23/22")
        sub_term_b = frac_create("7/18")
        
        total_diff = frac_add(sub_term_a, sub_term_b) # -23/22 + 7/18 which is -(23/22 - 7/18)
        
        final_result = frac_add(term2, total_diff)
        
    except Exception as e:
        from fractions import Fraction
        # Fallback direct calculation if domain API fails on specific string formats
        f_expr = Fraction(expr_str.replace(" ", ""))
        try:
            final_result = float(f_expr.limit_denominator())
        except:
             pass

    # Format correct_answer
    num = int(final_result.numerator)
    den = int(final_result.denominator)
    
    latex_val = frac_to_latex(final_result, mixed=False)
    
    return {
        "question_text": f"Simplify the expression \\(\\left[9/22 + 11/18 - (23/22 - 7/18)\\right]\\).",
        "correct_answer": {
            "numerator": num,
            "denominator": den,
            "canonical_latex": latex_val
        },
        "oracle_payload": frozen_params
    }