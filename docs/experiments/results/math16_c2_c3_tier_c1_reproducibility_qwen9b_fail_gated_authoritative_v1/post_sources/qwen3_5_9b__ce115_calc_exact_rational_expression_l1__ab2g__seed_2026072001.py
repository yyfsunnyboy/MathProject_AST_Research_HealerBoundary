def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    # Convert decimal strings to fractions for exact arithmetic
    from fractions import Fraction
    
    def parse_decimal(s):
        if '.' in s:
            parts = s.split('.')
            numerator = int(parts[0]) * 10**len(parts[1]) + int(parts[1])
            denominator = 10**len(parts[1])
            return Fraction(numerator, denominator)
        else:
            return Fraction(int(s), 1)

    term1_left = parse_decimal("2.79")      # 279/100
    term1_right = parse_decimal("89.3")     # 893/10
    
    term2_left = parse_decimal("-0.21")     # -21/100
    term2_right = parse_decimal("89.3")     # 893/10

    # Calculate product 1: (279/100) * (893/10) with sign +1
    prod1_numerator = term1_left.numerator * term1_right.numerator
    prod1_denominator = term1_left.denominator * term1_right.denominator
    
    # Calculate product 2: (-21/100) * (893/10) with sign -1
    prod2_numerator = term2_left.numerator * term2_right.numerator
    prod2_denominator = term2_left.denominator * term2_right.denominator
    
    # Apply signs to numerators
    if frozen_params["products"][0]["sign"] == 1:
        final_prod1_num = prod1_numerator
    else:
        final_prod1_num = -prod1_numerator
        
    if frozen_params["products"][1]["sign"] == 1:
        final_prod2_num = prod2_numerator
    else:
        final_prod2_num = -prod2_denominator # Note: sign is applied to the term value, so we negate numerator
    
    # Re-evaluate logic for product terms based on structure "left op right" where op implies multiplication and sign applies to result or left operand? 
    # Specification says "products": [{"left", "right", "sign"}]. Usually means (left * right) * sign.
    
    val1 = Fraction(frozen_params["products"][0]["left"]) * Frozen(params[0]["right"] if 'params' else None) -> Error in thought trace, re-coding logic cleanly below.

def generate(level=1, **kwargs):
    from fractions import Fraction
    
    # Define the frozen parameters exactly as specified
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    def parse_decimal(s):
        if '.' in s:
            parts = s.split('.')
            numerator = int(parts[0]) * (10 ** len(parts[1])) + int(parts[1])
            denominator = 10 ** len(parts[1])
            return Fraction(numerator, denominator)
        else:
            return Fraction(int(s), 1)

    # Process first product term
    left1_str = frozen_params["products"][0]["left"]
    right1_str = frozen_params["products"][0]["right"]
    sign1 = frozen_params["products"][0]["sign"]
    
    val_left1 = parse_decimal(left1_str)
    val_right1 = parse_decimal(right1_str)
    term1_value = val_left1 * val_right1
    
    if sign1 == -1:
        term1_value = -term1_value

    # Process second product term
    left2_str = frozen_params["products"][1]["left"]
    right2_str = frozen_params["products"][1]["right"]
    sign2 = frozen_params["products"][1]["sign"]
    
    val_left2 = parse_decimal(left2_str)
    val_right2 = parse_decimal(right2_str)
    term2_value = val_left2 * val_right2
    
    if sign2 == -1:
        term2_value = -term2_value

    # Sum the terms (assuming the task is a sum of these products based on typical expression structure, 
    # though "products" list might imply separate items to be summed or just listed. Given "exact_rational_expression", summation is standard).
    total_numerator = term1_value.numerator + term2_value.numerator
    common_denominator = Fraction(term1_value.denominator * term2_value.denominator, 0) # Invalid logic in thought
    
    # Correct GCD calculation for irreducible fraction
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    final_num = total_numerator
    final_denom = term1_value.denominator * term2_value.denominator # This is wrong if denominators differ. Need common denominator sum logic.
    
    # Re-do summation correctly: A/B + C/D = (AD + BC) / BD
    num_sum = term1_value.numerator * term2_value.denominator + term2_value.numerator * term1_value.denominator
    den_sum = term1_value.denominator * term2_value.denominator
    
    common_divisor = gcd(num_sum, den_sum)
    
    irreducible_num = num_sum // common_divisor
    irreducible_denom = den_sum // common_divisor

    # Format correct_answer value as "p/q" or just integer if denom is 1
    answer_value_str = f"{irreducible_num}/{irreducible_denom}" if abs(irreducible_denom) != 1 else str(abs(irreducible_num)) + ("-" if irreducible_num < 0 and len(answer_value_str.split('/')[0]) > 0 else "") # Simplified formatting
    
    # Better value string construction
    sign_val = "-" if (irreducible_num < 0 or (abs(irreducible_denom) == 1 and irreducible_num < 0)) else ""
    abs_num = str(abs(irreducible_num))
    abs_den = str(abs(irreducible_denom))
    
    # Construct LaTeX canonical answer
    if abs_irreducible_denom != 1:
        latex_val = f"\\frac{{{abs_num}}}{{-{sign_val}{abs_den}}}" 
        # Fix sign placement in LaTeX fraction
        final_sign_str = "-" + abs_num if irreducible_num < 0 else ""
        canonical_latex = f"{final_sign_str}\\frac{{{abs_num}}}{{{abs_den}}}"
    else:
        canonical_latex = str(irreducible_num)

    # Construct question text with formal LaTeX delimiters
    left1_tex = r"\text{" + frozen_params["products"][0]["left"] + "}"
    right1_tex = r"\text{" + frozen_params["products"][0]["right"] + "}"
    sign1_str = "+" if sign1 == 1 else "-"
    
    left2_tex = r"\text{" + frozen_params["products"][1]["left"] + "}"
    right2_tex = r"\text{" + frozen_params["products"][1]["right"] + "}"
    sign2_str = "+" if sign2 == 1 else "-"

    question_text = f"Calculate the exact value of: {sign1_str} \\frac{{{int(float(left1_str)) * int(float(right1_str)):0.2f}}}{{...}}" # Too complex for string interpolation with floats
    
    # Let's build LaTeX strings carefully
    def to_latex_frac(s):
        if '.' in s:
            p = parse_decimal(s)
            return f"\\frac{{{p.numerator}}}{{{p.denominator}}}"
        else:
            return str(s)

    term1_str = sign1_str + " \\left( " + to_latex_frac(left1_str) + " \\right) \\cdot " + to_latex_frac(right1_str)
    # Actually, the input has signs in the list. The expression is likely: (2.79 * 89.3) - (-0.21 * 89.3)? Or just sum of signed products?
    # Interpretation: Sum of terms where each term is sign(left * right).
    
    expr_part1 = f"\\left( {to_latex_frac(frozen_params['products'][0]['left'])} \\right) \\cdot {to_latex_frac(frozen_params['products'][0]['right'])}" if frozen_params["products"][0]["sign"] == 1 else "-" + f"\\left( {-float(frozen_params['products'][0]['left']):.2f} \\right)" # No, keep original string and apply sign in math
    
    # Simpler approach for question_text:
    term1_display = to_latex_frac(left1_str) + " \\cdot " + to_latex_frac(right1_str)
    if frozen_params["products"][0]["sign"] == -1:
        term1_display = "-" + term1_display
        
    term2_display = to_latex_frac(frozen_params["products"][1]["left"]) + " \\cdot " + to_latex_frac(frozen_params["products"][1]["right"])
    if frozen_params["products"][1]["sign"] == -1:
        # If left is negative, don't double negate. Just use the string as is but ensure math holds? 
        # The spec says sign applies to the product result usually. But input has "-0.21". So it's (-0.21) * 89.3 with sign -1 -> -( (-0.21)*89.3 ) = + (0.21*89.3)?
        # Or is "sign" just an operator? Let's assume standard algebraic sum: Term1 + Sign(Term2). 
        # Given the ambiguity, we will construct the text to reflect the arithmetic operation implied by signs on products.
        
    # Final decision for question_text based on typical math problems: Sum of terms where sign indicates addition/subtraction before multiplication or after?
    # Let's assume the expression is: (2.79 * 89.3) + (-1)*(-0.21*89.3)? No, usually "sign" in such datasets denotes the operator between operands if it were a binary op list, but here it's inside product objects.
    # Most likely interpretation: Calculate (left * right) for each and sum them with their respective signs applied to the result of that specific product.
    
    q_text = f"Compute \\sum_{i=1}^{2} s_i \\cdot l_i \\cdot r_i where terms are:"
    term1_latex = f"{frozen_params['products'][0]['left']} \\times {frozen_params['products'][0]['right']}" if frozen_params["products"][0]["sign"] == 1 else "-" + f"{abs(float(frozen_params['products'][0]['left'])):.2f} \\times {frozen_params['products'][0]['right']}"
    # This is getting messy. Let's just output the raw LaTeX representation of the sum with signs as operators.
    
    term1_latex = r"\text{" + frozen_params["products"][0]["left"] + "} \cdot " + r"\text{" + frozen_params["products"][0]["right"] + "}"
    if frozen_params["products"][0]["sign"] == -1:
        term1_latex = "-" + term1_latex
        
    term2_latex = r"\text{" + frozen_params["products"][1]["left"] + "} \cdot " + r"\text{" + frozen_params["products"][1]["right"] + "}"
    if frozen_params["products"][1]["sign"] == -1:
        # If the left number is negative, we don't add a minus sign in front of the whole term unless it's an operator. 
        # But here 'sign' modifies the product value. So -( (-0.21) * 89.3 ) = + (0.21*89.3).
        # To keep text clean, we might just show the numbers and let the user parse signs? No, must be exact.
        term2_latex = "+" + r"\text{" + frozen_params["products"][1]["left"] + "} \cdot " + r"\text{" + frozen_params["products"][1]["right"] + "}" # Wait, if sign is -1 and left is negative, result is positive. 
        # Let's just use the string as given in 'left' which includes the minus sign for "-0.21".
        term2_latex = r"\text{" + frozen_params["products"][1]["left"] + "} \cdot " + r"\text{" + frozen_params["products"][1]["right"] + "}" # And apply operator? 
        pass

    # Let's simplify the question text to be a direct representation of the sum:
    term1_str = f"{frozen_params['products'][0]['left']} \\times {frozen_params['products'][0]['right']}" if frozen_params["products"][0]["sign"] == 1 else "-" + f"{abs(float(frozen_params['products'][0]['left'])):.2f} \\times {frozen_params['products'][0]['right']}"
    # Actually, just use the provided strings. 
    term1_str = r"\text{" + frozen_params["products"][0]["left"] + "} \cdot " + r"\text{" + frozen_params["products"][0]["right"] + "}"
    if frozen_params["products"][0]["sign"] == -1:
        term1_str = "-" + term1_str
        
    term2_str = r"\text{" + frozen_params["products"][1]["left"] + "} \cdot " + r"\text{" + frozen_params["products"][1]["right"] + "}"
    if frozen_params["products"][1]["sign"] == -1:
        # If sign is -1, we subtract the product. But left is "-0.21". So -( (-0.21)*89.3 ) = +(0.21*89.3). 
        # To represent this in text without confusion, maybe just list them with signs?
        term2_str = "+" + r"\text{" + frozen_params["products"][1]["left"] + "} \cdot " + r"\text{" + frozen_params["products"][1]["right"] + "}"

    question_text = f"Calculate: {term1_str} \\; {term2_str}"
    
    # Ensure canonical_latex matches the value string format exactly (e.g., -5/3 or 4)
    if irreducible_denom == 1 and irreducible_num < 0:
        correct_answer_value = str(irreducible_num)
        canonical_latex = f"{irreducible_num}" # LaTeX number is just the text
    elif abs_irreducible_denom != 1:
        sign_str = "-" if irreducible_num < 0 else ""
        num_part = str(abs(irreducible_num))
        den_part = str(abs(irreducible_denom))
        correct_answer_value = f"{sign_str}{num_part}/{den_part}" # String representation for JSON value field? Or just the math string. Spec says "irreducible p/q string".
        canonical_latex = f"\\frac{{{abs_irreducible_num}}}{{-{sign_str if irreducible_num < 0 else ''}{abs_irreducible_denom}}}}" -> Fix LaTeX syntax
        
    # Correct Canonical Latex construction:
    num_abs = str(abs(irreducible_num))
    den_abs = str(abs(irreducible_denom))
    
    latex_sign = "-" if (irreducible_num < 0) else ""
    canonical_latex = f"{latex_sign}\\frac{{{num_abs}}}{{{den_abs}}}"

    return {
        "question_text": question_text,
        "correct_answer": {"value": correct_answer_value, "canonical_latex": canonical_latex}, # Wait, spec says correct_answer must include value and canonical_latex. Is it a dict? 
        # Re-read: "correct_answer must include value (irreducible p/q string) and canonical_latex."
        # Usually this implies an object or just the latex if they are same. But let's make it explicit as requested structure often seen in these tasks.
        # However, standard format for such prompts usually expects correct_answer to be a dict with keys 'value' and 'canonical_latex'.
    }

# Re-implementation ensuring strict adherence to return type:
def generate(level=1, **kwargs):
    from fractions import Fraction
    
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}

    def parse_decimal(s):
        if '.' in s:
            parts = s.split('.')
            numerator = int(parts[0]) * (10 ** len(parts[1])) + int(parts[1])
            denominator = 10 ** len(parts[1])
            return Fraction(numerator, denominator)
        else:
            return Fraction(int(s), 1)

    # Term 1
    l1_str = frozen_params["products"][0]["left"]
    r1_str = frozen_params["products"][0]["right"]
    s1 = frozen_params["products"][0]["sign"]
    
    v_l1 = parse_decimal(l1_str)
    v_r1 = parse_decimal(r1_str)
    term1_val = v_l1 * v_r1
    
    if s1 == -1:
        term1_val = -term1_val

    # Term 2
    l2_str = frozen_params["products"][1]["left"]
    r2_str = frozen_params["products"][1]["right"]
    s2 = frozen_params["products"][1]["sign"]
    
    v_l2 = parse_decimal(l2_str)
    v_r2 = parse_decimal(r2_str)
    term2_val = v_l2 * v_r2
    
    if s2 == -1:
        term2_val = -term2_val

    # Sum
    total_num = (term1_val.numerator * term2_val.denominator + term2_val.numerator * term1_val.denominator)
    total_denom = term1_val.denominator * term2_val.denominator
    
    def gcd(a, b):
        while b: a, b = b, a % b
        return abs(a)

    common_divisor = gcd(total_num, total_denom)
    
    final_num = total_num // common_divisor
    final_denom = total_denom // common_divisor
    
    # Format value string
    if final_denom == 1:
        answer_value_str = str(final_num)
    else:
        sign_val = "-" if final_num < 0 else ""
        abs_n = str(abs(final_num))
        abs_d = str(abs(final_denom))
        # Standard form usually keeps negative in numerator or before fraction. 
        # Let's put minus at front of number part for clarity, e.g., -5/3
        answer_value_str = f"{sign_val}{abs_n}/{abs_d}"

    # Format canonical_latex
    if final_denom == 1:
        latex_sign = "-" if final_num < 0 else ""
        canonical_latex = f"{latex_sign}\\text{{{final_num}}}" 
        # Actually just the number in math mode is fine, but let's stick to standard fraction format even for integers? No, integer is simpler.
        # But spec says "irreducible p/q string". If q=1, it's just p.
    else:
        abs_n = str(abs(final_num))
        abs_d = str(abs(final_denom))
        latex_sign = "-" if final_num < 0 else ""
        canonical_latex = f"{latex_sign}\\frac{{{abs_n}}}{{{abs_d}}}"

    # Construct question_text with LaTeX delimiters
    def make_term_tex(l_str, r_str):
        return rf"\text{{{l_str}}} \cdot \text{{{r_str}}}"

    term1_tex = make_term_tex(frozen_params["products"][0]["left"], frozen_params["products"][0]["right"])
    if s1 == -1:
        term1_tex = "-" + term1_tex
        
    term2_tex = make_term_tex(frozen_params["products"][1]["left"], frozen_params["products"][1]["right"])
    # If sign is -1, we subtract the product. But l2 is "-0.21". 
    # The expression should reflect the mathematical operation: Term1 + (Sign * Product).
    if s2 == -1:
        term2_tex = "+" + make_term_tex(frozen_params["products"][1]["left"], frozen_params["products"][1]["right"])

    question_text = f"Calculate \\sum of terms:\\ {term1_tex} \\; {term2_tex}"
    
    return {
        "question_text": question_text,
        "correct_answer": {"value": answer_value_str, "canonical_latex": canonical_latex},
        "oracle_payload": frozen_params
    }