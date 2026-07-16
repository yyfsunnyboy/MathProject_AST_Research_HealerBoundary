def generate(level=1, **kwargs):
    from core.prompts.domain_function_library import FractionOps
    
    # Frozen input data
    products = [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]
    
    # Build the expression string for question_text
    terms_strs = []
    for term in products:
        left_frac = FractionOps.create(term["left"])
        right_frac = FractionOps.create(term["right"])
        product_val = FractionOps.mul(left_frac, right_frac)
        
        sign_mult = 1 if term["sign"] == 1 else -1
        
        # Format the individual part for display (e.g., "2.79 * 89.3")
        left_str = str(term["left"])
        right_str = str(term["right"])
        op_sign = "+" if term["sign"] == 1 else "-"
        
        terms_strs.append(f"{op_sign} {left_str} × {right_str}")
    
    question_text = "Evaluate the following expression:\n" + "\n".join(terms_strs)

    # Calculate exact rational result using domain API
    total_sum = FractionOps.create("0")
    for term in products:
        left_frac = FractionOps.create(term["left"])
        right_frac = FractionOps.create(term["right"])
        product_val = FractionOps.mul(left_frac, right_frac)
        
        sign_mult = 1 if term["sign"] == 1 else -1
        
        total_sum = FractionOps.add(total_sum, FractionOps.mul(sign_mult, product_val))

    # Format the final answer as a canonical string (integer or p/q with positive denominator)
    result_str = str(total_sum.numerator) + "/" + str(total_sum.denominator) if total_sum.denominator != 1 else str(total_sum.numerator)
    
    # Ensure positive denominator for consistency, though FractionOps usually handles this. 
    # If the fraction is negative and we want p/q with q > 0:
    num = int(result_str.split("/")[0])
    den = int(result_str.split("/")[1])
    if den < 0:
        result_str = f"{num * -1}/{den * -1}"

    correct_answer = {"value": result_str}
    
    # Oracle payload must exactly equal the frozen parameters
    oracle_payload = products
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
