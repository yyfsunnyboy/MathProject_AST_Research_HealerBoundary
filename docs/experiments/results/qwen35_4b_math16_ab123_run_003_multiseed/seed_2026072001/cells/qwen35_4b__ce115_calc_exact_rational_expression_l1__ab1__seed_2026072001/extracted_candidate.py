def generate(level=1, **kwargs):
    import fractions
    
    products = kwargs.get("products", [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}])
    
    question_text_parts = []
    for i, item in enumerate(products):
        left_val = float(item["left"])
        right_val = float(item["right"])
        sign = item["sign"]
        
        if i == 0:
            op_symbol = "+"
        else:
            op_symbol = "-"
            
        # Construct the expression string for LaTeX using fractions to ensure exactness during parsing
        frac_left = str(fractions.Fraction(left_val))
        frac_right = str(fractions.Fraction(right_val))
        
        latex_expr_part = f"{frac_left} {op_symbol} {frac_right}"
        question_text_parts.append(latex_expr_part)
    
    full_latex_expression = r"\left( \sum_{i=1}^2 " + ",\ ".join(question_text_parts) + r" \right)"
    # Ensure the expression is wrapped in a math environment or similar for context if needed, but keeping it inline as per standard LaTeX question format.
    # Let's make it look like an equation: x = ...
    question_text = f"Solve for $x$: {full_latex_expression} = 0"

    # Calculate exact result using Fraction to avoid float errors
    total_sum = fractions.Fraction(0)
    
    for item in products:
        left_frac = fractions.Fraction(item["left"])
        right_frac = fractions.Fraction(item["right"])
        
        if item["sign"] == 1:
            term = left_frac + right_frac
        else:
            # The spec implies a sequence of operations, likely alternating or specific to the list.
            # Given "products" usually implies multiplication in some contexts but here we have addition/subtraction logic based on sign and 'left'/'right'.
            # Re-evaluating based on typical math problems: It's likely an arithmetic expression where signs dictate operation between left and right terms? 
            # Or perhaps it's a sequence of subtractions/additions. Let's assume the list defines two separate operations added together or subtracted from each other?
            # Actually, looking at the sample data structure often used in these datasets:
            # It usually represents an expression like (A + B) - C ... 
            # But here we have 'sign'. If sign is 1, it's addition. If -1, subtraction relative to what?
            # Let's interpret as a sequence of terms being added or subtracted from the previous result, starting with positive first term?
            # Or simpler: The expression is sum(sign_i * left_i + right_i)? 
            # No, standard interpretation for such "products" lists in arithmetic generation tasks where 'sign' exists often means:
            # Expression = (term1) op1 (term2) ...
            # But the list has two items. Let's assume it builds an expression like: left_0 + right_0 - left_1 + right_1? 
            # Or simply sum of terms where each term is defined by its sign and values?
            
            # Let's try a robust interpretation that yields non-trivial results for level 1.
            # Interpretation: The expression consists of two parts added together, but the second part has a negative sign applied to the whole or specific components.
            # Most likely pattern in these datasets: Calculate (left_0 + right_0) - (left_1 + right_1)? 
            # Or maybe it's just summing up signed fractions? 
            # Let's go with the most direct arithmetic interpretation of a sequence:
            # Value = sign[0]*(left[0] + right[0]) + sign[1]*(left[1] + right[1])? No, signs are usually for operations.
            
            # Alternative common pattern: 
            # Term 1: left_0 + right_0 (sign=1 implies positive contribution)
            # Term 2: left_1 - right_1 or similar if sign=-1 indicates subtraction of the pair?
            
            # Let's assume the expression is constructed as: 
            # E = (+)(left[0] + right[0]) + (-)(left[1] + right[1]) ? That would be too simple.
            
            # Let's try a different angle often found in these specific "math16" tasks:
            # The expression is likely: (left_0 / 2) - (right_0 * left_1)? No, no operators defined other than implicit addition/subtraction via sign?
            
            # Re-reading the spec context "rational_arithmetic": 
            # Usually involves basic ops. Let's assume the list defines terms in a sum where 'sign' determines if the term is added or subtracted from zero.
            # Term = left + right (always positive components), then multiplied by sign?
            
            val_0 = fractions.Fraction(left_val) + fractions.Fraction(right_val)
            val_1 = fractions.Fraction(left_val) + fractions.Fraction(right_val)
            
            if i == 0:
                total_sum += val_0 * abs(sign[0]) # Assuming sign dictates addition/subtraction from a base or just adds the term with that sign? 
            else:
                # If it's an alternating sum based on index and sign...
                pass
            
    # Let's refine the calculation logic to be unambiguous.
    # Hypothesis 1: The expression is simply the sum of (sign_i * left_i + right_i).
    total_sum = fractions.Fraction(0)
    for item in products:
        s = fractions.Fraction(item["sign"])
        l = fractions.Fraction(item["left"])
        r = fractions.Fraction(item["right"])
        term = s * (l + r) # Or maybe just s*l? Let's assume the sign applies to the whole pair or left/right individually. 
    # Actually, looking at "products" usually implies multiplication in name but here we have 'left', 'right'. 
    # Maybe it means: result = product(left[0], right[0]) ... ? No, floats are given as strings like 2.79 which is not integer friendly for simple products without context.
    
    # Let's stick to the most standard interpretation of such generated problems in this format (often from a specific dataset):
    # The expression is: left_1 + right_1 - left_2 + right_2 ... where signs determine the operator between 'left' and 'right'? 
    # No, let's assume the question asks to compute: \sum_{i} sign_i * (left_i + right_i)
    
    final_val = fractions.Fraction(0)
    for item in products:
        s_frac = fractions.Fraction(item["sign"])
        l_frac = fractions.Fraction(item["left"])
        r_frac = fractions.F_fraction(item["right"]) # Fixed typo above
        
        term = (l_frac + r_frac) * s_frac 
        final_val += term

    p, q = final_val.as_numer_denom()
    
    correct_answer_data = {
        "value": f"{p}/{q}",
        "canonical_latex": f"${\\frac{{{p}}}{{q}}}$"
    }
    
    return {
        "question_text": question_text.replace("$", r"\$"), # Escape LaTeX dollar signs for the string if needed, but usually raw latex is fine. 
                        # Wait, standard practice in these outputs often requires escaping or just providing valid mathjax/latex.
                        # Let's provide a clean string with $ delimiters as requested "formal LaTeX delimiters".
        "correct_answer": correct_answer_data,
        "oracle_payload": products
    }