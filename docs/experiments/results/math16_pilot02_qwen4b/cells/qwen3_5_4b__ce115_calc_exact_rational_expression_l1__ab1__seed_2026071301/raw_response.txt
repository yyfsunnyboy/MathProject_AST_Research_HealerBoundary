def generate(level=1, **kwargs):
    import fractions
    
    products = kwargs.get("products", [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}])
    
    question_text = r"\text{Calculate the exact value of: } \frac{(2.79)(89.3) + (-0.21)(89.3)}{?}" # Placeholder for structure, focusing on calculation
    
    # Parse floats to fractions
    f1 = float(products[0]["left"])
    f2 = float(products[0]["right"])
    s1 = products[0]["sign"]
    
    f3 = float(products[1]["left"])
    f4 = float(products[1]["right"])
    s2 = products[1]["sign"]
    
    # Calculate numerator: (f1 * f2) + (s2 * f3 * f4) -- Wait, sign is usually for the term itself or operation? 
    # Based on typical patterns: Term 1 = left*right with sign. Term 2 = left*right with sign.
    # Let's assume expression: s1*(f1*f2) + s2*(f3*f4) ? Or just sum of signed products?
    # Re-reading spec "products": list of {left, right, sign}. 
    # Likely structure: (sign_1 * left_1 * right_1) + (sign_2 * left_2 * right_2)? 
    # But the example has 89.3 twice. Let's assume it is a sum/difference of products.
    
    term1 = s1 * f1 * f2
    term2 = s2 * f3 * f4
    
    numerator_val = term1 + term2
    
    # Convert to irreducible fraction p/q
    frac_obj = fractions.Fraction(numerator_val).limit_denominator(1) # Exact arithmetic requires no limit, just Fraction constructor handles exact if input is float? 
    # No, float conversion loses precision. We must convert string inputs directly or use Decimal/Fractions from strings to avoid float error.
    
    # Correct approach: Parse as Fractions immediately from the decimal representations provided in strings.
    frac1 = fractions.Fraction(products[0]["left"])
    frac2 = fractions.Fraction(products[0]["right"])
    term1_frac = s1 * (frac1 * frac2)
    
    frac3 = fractions.Fraction(products[1]["left"])
    frac4 = fractions.Fraction(products[1]["right"])
    term2_frac = s2 * (frac3 * frac4)
    
    numerator_obj = term1_frac + term2_frac
    
    # Denominator? The task is "rational_arithmetic". Usually implies a single value or expression. 
    # Given the frozen params, it seems to be calculating a specific rational number resulting from these operations.
    # If no denominator is specified in input, assume result is just numerator_obj (as an integer/fraction).
    
    p = numerator_obj.numerator
    q = numerator_obj.denominator
    
    correct_answer_value = f"{p}/{q}"
    canonical_latex = r"\frac{" + str(p) + "}{"} + str(q) + r"}"
    
    oracle_payload = products

    return {
        "question_text": r"$\text{Compute the exact rational value: } \left(\pm 2.79 \times 89.3\right) + \left(\mp 0.21 \times 89.3\right)$",
        "correct_answer": {
            "value": correct_answer_value,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": oracle_payload
    }