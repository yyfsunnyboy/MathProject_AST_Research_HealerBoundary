def generate(level=1, **kwargs):
    base = 7
    expression_str = "7**10 * 7**2 / 7**4"
    
    # Calculate exponents: a + b - c
    exp_a = 10
    exp_b = 2
    exp_c = 4
    
    total_exponent = exp_a + exp_b - exp_c
    
    if total_exponent >= 0:
        exponent_value = int(total_exponent)
        base_str = str(base)
        exponent_str = f"{base_str}^{exponent_value}"
    else:
        # Handle negative exponents as p/q string format "p/q" where q=1/|exp|, but standard math notation for integer division usually implies keeping it simple or using fractions. 
        # Given the context of junior high and exact arithmetic without floats, a negative exponent is represented as 7^-2 which is often written in fraction form p/q if required by "irreducible p/q string".
        # However, standard power laws result in integers here (10+2-4=8). 
        # Let's double check: 7^10 * 7^2 = 7^(12), divided by 7^4 is 7^(12-4) = 7^8.
        
        exponent_value = int(total_exponent)
    
    correct_answer_dict = {
        "base": base,
        "exponent": total_exponent if isinstance(total_exponent, (int, float)) and not isinstance(total_exponent, bool) else f"{total_exponent}" # Fallback for string representation if needed, but here it's int.
    }

    oracle_payload = {
        "base": base,
        "expression": expression_str,
        "required_form": "power_of_same_base"
    }

    return {
        "question_text": f"Simplify the power of same base: {expression_str}",
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }