def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    # Helper to convert string float to Fraction for exact arithmetic
    def str_to_fraction(s):
        try:
            return _FractionBase(int(float(str(s).replace('.', '')), 1) if '.' in s else int(s)) / (len([c for c in s if c == '.']) + len([int(c) for c in s])) # This is a hack, let's do it properly.
        except:
            return _FractionBase(0)

    def safe_fraction_from_str(s):
        try:
            val = float(str(s))
            num = int(val * 10**9) if abs(int(val*1e9)) == int(val*1e9) else round(val * 1e9) # Better approach for exactness in string context usually implies decimal precision.
            # Actually, standard way to convert float string to Fraction exactly:
            from fractions import Fraction as F
            return F(str(s).replace('.', '')) / (len([c for c in str(s) if c == '.']) + 10**int(len(str(s).split('.')[1]) if '.' in str(s) else 0)) # Still messy.
            
        except:
            from fractions import Fraction as F
            return F(0)

    # Correct approach using standard library's Fraction constructor which accepts string directly for exactness
    def to_fraction_str(s):
        try:
            val = float(str(s).replace('.', '')) if '.' in str(s) else int(str(s))
            denom = 10**int(len([c for c in s.split('.')[1]]) + (len([c for c in s]) - len([c for c in s.split('.')])) * 2) # No.
            
            # The most robust way given the input format "2.79" is to treat it as a decimal fraction directly via Fraction constructor if available, 
            # but since we must use domain APIs which are simulated here:
            pass
        
        except Exception:
            from fractions import Fraction as F
            return F(0)

    # Simulating the required Domain API usage strictly.
    # Since `core.prompts.domain_function_library` is not available, I will implement the logic 
    # that mimics what those functions would do to satisfy "exact arithmetic only".
    
    from fractions import Fraction as F
    
    def create_fraction(value_str):
        try:
            return F(str(value_str)) if '.' in str(value_str) else F(int(value_str))
        except Exception:
            # Handle cases where direct string conversion might fail due to non-numeric chars (unlikely here but safe fallback)
            val = float(str(value_str).replace('.', '')) 
            denom = 10**int(len([c for c in str(value_str) if c == '.']) + len([int(c) for c in str(value_str)])) # No.
            
        return F(0)

    def mul_fraction(a, b):
        num_a, den_a = a.numerator, a.denominator
        num_b, den_b = b.numerator, b.denominator
        res_num = num_a * num_b
        res_den = den_a * den_b
        # Reduce fraction manually to ensure canonical form (gcd reduction)
        from math import gcd as gcd_func
        common = gcd_func(res_num, res_den) if res_den != 0 else 1
        return F(int(res_num // common), int(res_den // common))

    def add_fraction(a, b):
        num_a, den_a = a.numerator, a.denominator
        num_b, den_b = b.numerator, b.denominator
        res_num = (num_a * den_b) + (num_b * den_a)
        res_den = den_a * den_b
        from math import gcd as gcd_func
        common = gcd_func(res_num, res_den) if res_den != 0 else 1
        return F(int(res_num // common), int(res_den // common))

    # Process products list to build the expression tree or sequence of operations.
    # The task is "exact_rational_expression". 
    # We have two product items: (2.79 * 89.3) and (-0.21 * 89.3).
    # Likely the question asks for the sum of these products? Or just one specific calculation based on level=1 defaulting to first item?
    # Given "products" list, usually implies a sequence: Product1 + Product2 or similar structure. 
    # Let's assume the expression is (Product 1) + (Product 2).

    p1_left = F(str(frozen_params["products"][0]["left"]))
    p1_right = F(str(frozen_params["products"][0]["right"]))
    
    if frozen_params["products"][0]["sign"] == -1:
        # If sign is negative, it might mean subtraction or negation. 
        # Given the structure "left", "right", "sign": 1 usually means left * right.
        # Let's assume standard multiplication with optional sign flip on result? Or operation type?
        # Re-reading: "products" list contains objects with 'sign'. 
        # If sign is -1, perhaps it implies subtraction from a base or negation of the product term in an expression like A + B where B has negative coefficient.
        # Let's assume the final answer is sum(product_i * sign_i).
        
    p2_left = F(str(frozen_params["products"][1]["left"]))
    p2_right = F(str(frozen_params["products"][1]["right"]))

    term1 = mul_fraction(p1_left, p1_right)
    
    # Apply sign logic: if sign is -1, negate the result? Or subtract? 
    # Let's assume "sign" indicates whether to add or subtract from a zero base.
    # If sign=1 -> +term; if sign=-1 -> -term.
    term2 = mul_fraction(p2_left, p2_right)
    
    total_sum = F(0)
    for item in frozen_params["products"]:
        val = mul_fraction(F(str(item["left"])), F(str(item["right"])))
        if item["sign"] == 1:
            total_sum = add_fraction(total_sum, val)
        else:
            total_sum = add_fraction(total_sum, -val)

    # Canonical exact rational string format: integer or irreducible p/q with positive denominator.
    num_val = int(total_sum.numerator)
    den_val = int(total_sum.denominator)
    
    if den_val == 1:
        ans_str = str(num_val)
    else:
        # Ensure positive denominator (Fraction does this automatically, but double check)
        if den_val < 0:
            num_val *= -1
            den_val *= -1
        
        ans_str = f"{num_val}/{den_val}"

    question_text = "Calculate the exact rational value of the expression formed by summing the signed products."
    
    correct_answer_dict = {
        "value": ans_str,
        # Additional fields if required? Spec says: exactly value. 
        # Wait, spec says: "correct_answer must be a JSON-compatible dict with exactly value".
        # So only key 'value'.
    }

    oracle_payload = frozen_params["products"]

    return {
        "question_text": question_text,
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }