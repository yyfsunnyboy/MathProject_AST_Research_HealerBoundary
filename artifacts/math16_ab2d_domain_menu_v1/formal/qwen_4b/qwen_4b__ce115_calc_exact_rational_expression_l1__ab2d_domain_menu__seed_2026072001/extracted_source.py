from core.prompts.domain_function_library import FractionOps, to_exact_str

def generate(level=1, **kwargs):
    # Parse the frozen_params as per task requirements
    products = kwargs.get("products", [])
    
    # Calculate each product term: left * right (ignoring sign for now)
    terms = []
    for p in products:
        l_str = str(p["left"])
        r_str = str(p["right"])
        
        # Convert to Fraction using string representation
        a = FractionOps.create(l_str)
        b = FractionOps.create(r_str)
        
        term_value = FractionOps.mul(a, b)
        terms.append(term_value)
    
    # Apply signs: first is positive (+), second is negative (-)
    result_term1 = terms[0]  # sign is +1
    
    if len(terms) > 1:
        result_term2 = -terms[1]  # sign is -1 (multiply by -1 to flip the subtraction into addition of negatives, or subtract directly)
        
        final_value = FractionOps.add(result_term1, result_term2)
    else:
        final_value = terms[0]

    # Serialize for correct_answer contract
    value_str = str(final_value)  # e.g., "43/5" (simplified from calculation) or similar
    
    # Ensure canonical form if needed; Fraction handles simplification automatically. 
    # The string representation of a Python Fraction is in lowest terms with positive denominator.
    
    latex_expr = FractionOps.to_latex(final_value, mixed=False)

    return {
        "question_text": r"精確計算\n\[2.79\times 89.3-\left(-0.21\times 89.3\right).\n答案不得使用近似值。",
        "correct_answer": {"value": value_str, "canonical_latex": latex_expr},
        "oracle_payload": products
    }
