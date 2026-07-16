def generate(level=1, **kwargs):
    products = kwargs.get("products", [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}])

    def parse_float_to_int(s):
        return int(round(float(s) * 100))

    questions = []
    
    for i, item in enumerate(products):
        left_val_str = str(item["left"])
        right_val_str = str(item["right"])
        
        # Convert to integers by scaling (assuming inputs are decimals with up to 2 decimal places)
        try:
            l_int = parse_float_to_int(left_val_str)
            r_int = parse_float_to_int(right_val_str)
            
            if item["sign"] == 1:
                numerator = l_int * r_int
                denominator = 10000 # Since both were scaled by 100, product is scaled by 100*100=10000
                
                # Simplify fraction
                def gcd(a, b):
                    while b:
                        a, b = b, a % b
                    return abs(a)
                
                common_divisor = gcd(numerator, denominator)
                num_simplified = numerator // common_divisor
                den_simplified = denominator // common_divisor
                
                if den_simplified < 0:
                    num_simplified *= -1
                    den_simplified *= -1
                    
                canonical_str = f"{num_simplified}/{den_simplified}"
            else: # sign == -1, meaning subtraction or negative result based on context of "exact rational expression" usually implying a/b form. 
                # Given the structure {"left": ..., "right": ...}, and typical arithmetic tasks, this likely represents (a * b) / c where c is derived from right side scaling if it's division, OR simply multiplication with sign flip.
                # However, looking at standard rational expression problems: often they are fractions like a/b - c/d or similar. 
                # But the input format here suggests two operands and an operation implied by 'sign'.
                # Let's interpret as: (left * right) if sign=1 else -(left * right).
                # Wait, re-reading "exact_rational_expression". Usually involves fractions like 2.79/89.3 or similar? 
                # No, the input keys are 'left' and 'right'. Let's assume operation is multiplication based on typical simple arithmetic generation unless specified otherwise as division.
                # Actually, looking at common datasets for this task type (ce115), it often involves fractions like a/b + c/d or similar. 
                # But with just left/right/ sign, let's stick to the most direct interpretation: Multiplication of two numbers represented as decimals converted to rationals.
                
                numerator = l_int * r_int
                
                if item["sign"] == -1:
                    numerator *= -1
                    
                denominator = 10000 # Same scaling factor for both inputs multiplied
                
                common_divisor = gcd(numerator, denominator)
                num_simplified = numerator // common_divisor
                den_simplified = denominator // common_divisor

                if den_simplified < 0:
                    num_simplified *= -1
                    den_simplified *= -1
                    
                canonical_str = f"{num_simplified}/{den_simplified}"
                
        except ValueError:
            # Fallback for non-decimal inputs or parsing errors, though spec implies decimals.
            continue
            
        question_text = f"Calculate the exact rational expression resulting from {left_val_str} * {right_val_str}. The result should be expressed as an irreducible fraction p/q with a positive denominator."
        
        correct_answer = {"value": canonical_str}

    if not questions:
        # Fallback generation in case of parsing issues, though unlikely given spec
        return generate(level=level)

    final_question = questions[0]
    
    oracle_payload = products
    
    result_dict = {
        "question_text": final_question["question_text"],
        "correct_answer": final_question["correct_answer"],
        "oracle_payload": oracle_payload
    }
    
    return result_dict