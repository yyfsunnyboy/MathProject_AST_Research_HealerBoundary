def generate(level=1, **kwargs):
    import fractions
    
    products = kwargs.get("products", [])
    
    # Process each product to build a rational expression
    # Each item has left (string), right (string or number), sign (+/-)
    numerator_parts = []
    denominator_parts = []
    
    for prod in products:
        left_str = str(prod["left"])
        right_val = float(prod["right"]) if isinstance(prod["right"], str) else prod["right"]
        
        # Convert string to Fraction (exact arithmetic)
        try:
            left_frac = fractions.Fraction(float(left_str))
        except ValueError:
            continue
            
        denom_val = int(right_val)  # Treat right as integer denominator for this level
        
        if prod["sign"] == -1 or "right" in str(prod):
            # Multiply by negative fraction (left / right becomes -(left/right))
            term_frac = fractions.Fraction(-left_frac, denom_val)
        else:
            term_frac = fractions.Fraction(left_frac, denom_val)
            
        numerator_parts.append(term_frac.numerator)
        denominator_parts.append(term_frac.denominator)

    # Combine numerators and denominators
    if not numerator_parts or not denominator_parts:
        raise ValueError("No valid products to generate expression")
    
    total_num = sum(numerator_parts)
    total_denom = sum(denominator_parts)
    
    result_frac = fractions.Fraction(total_num, total_denom)
    
    # Simplify if needed (Fraction does this automatically but we ensure irreducibility)
    p = str(result_frac.numerator).strip()
    q = str(result_frac.denominator).strip()

    question_text = r"\text{Compute the exact rational value of: } $ \sum_{i=1}^{2} (\frac{\text{{left}}_i}{\text{{right}}_i})^{\text{{sign}}_i} $"
    
    canonical_latex = f"${\\frac{{{p}}}{{{q}}}$}"

    return {
        "question_text": question_text,
        "correct_answer": {"value": f"{p}/{q}", "canonical_latex": canonical_latex},
        "oracle_payload": products
    }