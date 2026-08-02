from core.prompts.domain_function_library import FractionOps, to_exact_adapter

def generate(level=1, **kwargs):
    # Parse the frozen_params as per task requirements.
    products = kwargs.get("products", [])
    
    # Extract components from the first product: 2.79 * 89.3 with sign +1
    p_left_1 = float(products[0]["left"])
    p_right_1 = float(products[0]["right"])
    sgn_1 = products[0]["sign"]

    # Extract components from the second product: -0.21 * 89.3 with sign -1 (applied to result)
    p_left_2 = float(products[1]["left"])
    p_right_2 = float(products[1]["right"])
    sgn_2 = products[1]["sign"]

    # Create fractions for the terms inside parentheses
    term_a = FractionOps.from_parts(int(p_left_1 * 10**3), int(89.3 * 10)) / (int(1) if p_right_1 == float(products[0]["right"]) else None) 
    # Correction: Directly create fractions from the decimal values provided in frozen_params
    term_a = FractionOps.from_parts(int(p_left_1), int(round(p_right_1 * 10))) / (int(89.3)) if False else ...

    # Correct approach using to_exact_adapter for decimals first, then convert to fraction logic manually or via API
    
    # Re-evaluating based on available APIs:
    # We need exact rational arithmetic. The input is decimal strings like "2.79".
    # FractionOps.create accepts legal numeric str. Let's try creating fractions directly from the string representation if possible, 
    # but standard float conversion might lose precision before fraction creation unless we handle it carefully.
    
    # Strategy: Convert decimals to exact integers by scaling (e.g., 2.79 = 279/100), then compute using FractionOps.from_parts
    
    def decimal_to_fraction(s):
        """Convert a string like '2.79' or '-0.21' to an integer numerator and denominator."""
        if '.' in s:
            parts = s.split('.')
            int_part = int(parts[0])
            frac_str = parts[1]
            denom = 10 ** len(frac_str)
            num = int(int_part * (denom // 10**len(s.split('.')[1].split('')[::-1])) + ... ) # Simplified logic below
            
        return FractionOps.from_parts(...)

    # Simpler approach: Use the fact that we can create fractions from strings if they are valid.
    # However, "2.79" is a float string. The API says inputs for create include legal numeric str or int/fraction.
    # Let's manually construct numerators and denominators to ensure exactness.

    def parse_decimal(s):
        """Returns (numerator, denominator) tuple representing the fraction."""
        if '.' in s:
            integer_part = float(int(s.split('.')[0])) * 10 ** len(s.split('.')[1])
            fractional_part_str = s.split('.')[1]
            # Reconstruct numerator as int(integer_part + fractional part scaled correctly)
            total_num = int(float(s.replace('.', ''))) 
            denom = 10 ** len(frac_parts := s.split('.'))[-1] if '.' in s else 1
            
        return FractionOps.from_parts(int(total_num), int(denom))

    # Correct parsing logic:
    def get_fraction_from_str(val):
        """Converts string like '2.79' to exact fraction."""
        val = str(val)
        if '.' not in val:
            return FractionOps.create(int(float(val)))
        
        integer_part, fractional_part = val.split('.')
        # Construct numerator and denominator manually for precision
        denom = 10 ** len(fractional_part)
        num_str = int(integer_part + '0' * (len(denom)) if not fractional_part else '') 
        # Actually simpler: multiply everything by power of 10 to make integer
        
        full_num = float(val.replace('.', ''))
        denom_power = 10 ** len(fractional_part)
        
        return FractionOps.from_parts(int(full_num * (denom // int(denom))), int(denom))

    # Let's use a robust method: convert string to fraction manually using from_parts
    
    def str_to_fraction(s):
        if '.' in s:
            parts = s.split('.')
            integer_part_str = parts[0]
            fractional_part_str = parts[1]
            
            denom = 10 ** len(fractional_part_str)
            # Combine integer and fractional part into a single numerator scaled by denominator
            num_int = int(integer_part_str) * (denom // 1 if not fractional_part_str else ... ) 
            # Correct way:
            val_float = float(s)
            # To get exact fraction from float string without precision loss, we can use the decimal module logic or manual scaling.
            # Since FractionOps.create accepts legal numeric str, and "2.79" is a valid representation of 279/100? 
            # The API says inputs: int, finite float, legal numeric str... returns Fraction.
            # But creating from '2.79' might result in an approximation if not handled as exact string parsing.
            
            # Safest manual construction:
            num = int(float(s.replace('.', ''))) 
            denom = 10 ** len(fractional_part_str)
        else:
            return FractionOps.create(int(float(s)))

    term_a_num, term_a_denom = str_to_fraction("2.79") # Should be 279/100
    term_b_1_num, term_b_1_denom = str_to_fraction("89.3")   # Should be 893/10
    
    term_c_num, term_c_denom = str_to_fraction("-0.21")      # Should be -21/100
    term_d_num, term_d_denom = str_to_fraction("89.3")       # Same as above

    a_frac = FractionOps.from_parts(term_a_num, term_a_denom)
    b_1_frac = FractionOps.from_parts(term_b_1_num, term_b_1_denom)
    
    c_frac = FractionOps.from_parts(term_c_num, term_c_denom) # -21/100
    d_frac = FractionOps.from_parts(term_d_num, term_d_denom)

    # Calculate 2.79 * 89.3
    prod_1 = FractionOps.mul(a_frac, b_1_frac)
    
    # Calculate (-0.21 * 89.3). Note: the input is "-0.21", so c_frac handles the negative sign correctly in numerator? 
    # Yes, from_parts takes int numerator and denominator. -21/100 works if we pass -21 as num.
    
    prod_2 = FractionOps.mul(c_frac, d_frac)

    # The expression is: (prod_1) - (- prod_2)? No, the term in parenthesis is already negative? 
    # Expression: 2.79 * 89.3 - (-0.21 * 89.3)
    # This equals prod_1 + abs(prod_2) if c_frac was positive? 
    # Wait, the expression has a minus sign before the parenthesis containing "-0.21".
    # So it is: (A * B) - [ (-C) * D ] = A*B + C*D
    
    term_inside_parenthesis = FractionOps.mul(c_frac, d_frac) # This results in negative fraction
    total_subtraction_term = prod_2

    final_result = FractionOps.sub(prod_1, total_subtraction_term)

    # Convert result to exact string and latex
    value_str = str(final_result.numerator / final_result.denominator) if False else ... 
    # Use the provided adapter logic: to_exact returns int or 'p/q'
    
    correct_answer_value = FractionOps.to_exact(final_result)
    canonical_latex = FractionOps.to_latex(FractionOps.create(str(correct_answer_value)))

    return {
        "question_text": r"精確計算 \[ 2.79\times 89.3-\left(-0.21\times 89.3\right). \] 答案不得使用近似值。",
        "correct_answer": {"value": str(correct_answer_value), "canonical_latex": canonical_latex},
        "oracle_payload": {
            "products": [
                {
                    "left": "2.79",
                    "right": "89.3",
                    "sign": 1
                },
                {
                    "left": "-0.21",
                    "right": "89.3",
                    "sign": -1
                }
            ]
        }
    }

# Helper to ensure exact fraction creation from decimal strings without float precision issues during intermediate steps if needed, 
# though FractionOps.create might handle it well enough for simple decimals like 2.79.
