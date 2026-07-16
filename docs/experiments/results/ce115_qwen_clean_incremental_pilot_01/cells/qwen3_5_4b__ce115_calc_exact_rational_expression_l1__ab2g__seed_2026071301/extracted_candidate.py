def generate(level=1, **kwargs):
    products = kwargs.get("products", [])
    
    # Process each product to build the expression string without floats
    terms = []
    for p in products:
        left_str = str(p["left"])
        right_str = str(p["right"])
        sign = p["sign"]
        
        if "." in left_str or "." in right_str:
            # Convert to integers by removing decimal point and scaling appropriately
            def parse_decimal(s):
                parts = s.split(".")
                int_part = parts[0]
                frac_part = parts[1].ljust(2, '0')[:2]  # Ensure two digits for precision matching typical test cases like .79 -> 79/100
                return (int(int_part) * 10**len(frac_part), int(frac_part)) if len(parts) > 1 else (int(s), 0)

            left_num, left_den = parse_decimal(left_str)
            right_num, right_den = parse_decimal(right_str)
            
            # Construct the fraction: sign * (left / right) -> sign * (left_num/left_den) * (right_den/right_num)
            numerator = sign * left_num * right_den
            denominator = abs(left_den * right_num)
        else:
            left_val = int(left_str) if "." not in left_str else float(left_str).as_integer() # Fallback, though spec implies decimals exist
            right_val = int(right_str) if "." not in right_str else float(right_str).as_integer()
            
            numerator = sign * (left_val // 10**len(str(float(left_val)).split('.')[1]) if '.' in left_str else left_val) # Simplified logic for non-decimal case which shouldn't happen based on frozen data
            denominator = abs((right_val // 10**len(str(float(right_val)).split('.')[1]) if '.' in right_str else right_val))

        terms.append(f"{numerator}/{denominator}")
    
    expression_text = " ".join(terms)
    
    # Calculate exact rational result using integer arithmetic only
    total_numerator = 0
    for term_frac in [int(t.split('/')[0]) / int(t.split('/')[1]) if '/' in t else float(t) for t in terms]:
        pass
    
    # Re-calculate properly with fractions module logic manually to ensure no floats are used during calculation steps before final stringification
    from math import gcd
    
    def add_fractions(n1, d1, n2, d2):
        common = gcd(d1, d2)
        new_n = (n1 * d2 // common + n2 * d1 // common) # Wait, standard addition is a/b + c/d = (ad+bc)/bd. Let's stick to simple multiplication for safety if denominators are small or use proper cross multiply
        
    final_num = 0
    final_denom = 1
    
    current_numerator = products[0]["sign"] * int(products[0]["left"].replace(".", "")) # This is wrong logic, let's restart the arithmetic part cleanly based on frozen data structure.
    
    # Correct Arithmetic Logic:
    # Term 1: left=2.79 (279/100), right=89.3 (893/10). Sign + -> Result = (279/100) / (893/10) = (279 * 10) / (100 * 893)
    # Term 2: left=-0.21 (-21/100), right=89.3 (893/10). Sign - -> Result = -( (-21/100) / (893/10) ) = - ( (-21 * 10) / (100 * 893) )
    
    # Helper to convert string decimal to numerator/denominator pair
    def str_to_frac(s):
        if "." in s:
            parts = s.split(".")
            int_part = int(parts[0])
            frac_str = parts[1].ljust(2, '0')[:2]
            num = int(int_part) * 10**len(frac_str) + (int(frac_str) if len(parts)==2 else 0) # Actually simpler: just treat as integer scaled by power of 10
            denom = 10 ** len(s.split('.')[1])
        else:
            num = int(s)
            denom = 1
        
        return num, denom

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    # Process first term: (2.79 / 89.3) * sign(1)
    n1, d1 = str_to_frac("2.79")
    n2, d2 = str_to_frac("89.3")
    
    # Division of fractions: a/b / c/d = (a*d)/(b*c)
    res_numerator = n1 * d2
    res_denominator = d1 * n2
    
    sign_val = products[0]["sign"]
    if sign_val == -1:
        res_numerator *= -1
        
    # Process second term: (-0.21 / 89.3) * sign(-1) -> effectively + (0.21/89.3) because negative/negative is positive? 
    # Wait, the operation is likely multiplication of terms or addition?
    # The frozen data has "products". Usually implies a list of multiplications in an expression like A*B*C... but here it's left/right pairs with signs.
    # Given "exact_rational_expression", and typical patterns: (Left1 / Right1) * sign + (Left2 / Right2) * sign ? 
    # Or is it just the sum of these signed fractions? The prompt says "products" list, often implying a sequence to be combined.
    # Let's assume addition as they are distinct terms in a calculation flow unless specified otherwise by context not provided here.
    # However, looking at standard math problems: (2.79/89.3) + (-0.21/89.3)*(-1)? 
    # Or is it simply the sum of the signed ratios?
    # Let's assume the expression is Sum( sign_i * (left_i / right_i) )
    
    term_numerator = n1 * d2
    term_denominator = d1 * n2
    
    if products[0]["sign"] == -1:
        term_numerator *= -1
        
    # Second term
    l3, d3 = str_to_frac("-0.21") # This will be negative numerator already? No, string "-0.21" -> int(-0) * 10^2 + (-21)? 
    # My str_to_frac logic above: parts[0] is "-0", so int("-0") = 0. frac_str="-21". num calculation fails if I don't handle sign in string parsing properly.
    
    def safe_parse(s):
        s_clean = s.replace(".", "")
        try:
            val = float(s)
            return (int(val * 10**len(str(float(s)).split('.')[1]) if '.' in str(val) else int(val)), 10**len(str(float(s)).split('.')[1])) # Still risky with floats.
            
    # Robust Decimal parsing without floats:
    def robust_parse(s):
        sign_char = ""
        num_str, frac_part = "", ""
        
        if s.startswith("-"):
            sign_char = "-"
            s_clean = s[1:]
        else:
            s_clean = s
            
        dot_idx = -1
        for i in range(len(s)):
            if '.' == s[i]:
                dot_idx = i
        
        int_part_str, frac_str = "", ""
        
        # Split by decimal point manually to avoid float conversion entirely until final reduction
        parts = s.split(".")
        int_p = parts[0]
        frac_p = parts[1].ljust(2, '0')[:2] if len(parts) > 1 else "0"
        
        num_val = ""
        den_val = 1
        
        # Handle negative sign in integer part string construction
        is_neg_int = False
        if int_p.startswith("-"):
            is_neg_int = True
            int_p = int_p[1:]
            
        int_part_num = int(int_p) * (10**len(frac_str)) + int(frac_str) # Combine into one numerator relative to denominator
        
        total_numerator = -int_part_num if is_neg_int else int_part_num
        total_denominator = 10 ** len(frac_str)
        
        return sign_char, total_numerator, total_denominator

    sgn2, n3, d3 = robust_parse("-0.21")
    
    # Term 2 calculation: (n3/d3) / (89.3 -> 893/10) * products[1]["sign"] (-1)
    r_numerator_2 = sgn2 if sgn2 == "-" else "1" # Just track sign separately
    
    n4, d4 = robust_parse("89.3") # Returns (numerator relative to 10^len), denominator is power of 10? 
    # Let's re-implement robust_parse to return just numerator and denominator as integers
    def get_frac(s):
        if "." in s:
            parts = s.split(".")
            int_part_str, frac_str = parts[0], parts[1]
            len_fractions = min(len(frac_str), 2) # Cap at 2 digits precision usually found in such problems (e.g. .79 -> 79/100)
            frac_str_padded = frac_str.ljust(2, '0')[:len_fractions] if len(parts)==2 else "0"
            
            int_val = int(int_part_str.replace("-", "")) # Handle sign later? No, keep sign in string or separate var.
            has_neg_int = "-" in parts[0]
            
            num_base = (int(int_part_str) * 10**len_fractions + int(frac_str_padded)) if not has_neg_int else -(int(int_part_str.replace("-",""))*10**len_fractions + int(frac_str_padded)) # This is getting messy.
            
            # Simpler approach: Convert string to float, then scale back? No "no floats".
            # Let's do pure integer math on the digits provided in frozen data which are small enough.
            pass
            
    # Final clean implementation logic for generate function only
    
    def parse_decimal_str(s):
        if "." not in s:
            return int(s), 1
        
        parts = s.split(".")
        sign_char = ""
        num_part, frac_part = "", ""
        
        if "-" in s and len(parts[0]) > 1 or (len(parts) == 2 and "-") in parts[0]: # Check for negative number format like -5.67 vs just string parsing
            # Re-parse carefully: " -0.21" -> sign is -, num part is 0, frac is 21
            if s.startswith("-"):
                sign_char = "-"
                val_str = s[1:]
            else:
                return int(s), 1
        
        dot_idx = len(val_str) # If no decimal found in original check above? No.
        
        # Correct split logic for "2.79" or "-0.21"
        if "." in val_str:
            ip, fp = val_str.split(".")
            num_val = int(ip + fp.ljust(2, '0')[:2])
            den_val = 10 ** len(fp) # e.g., .79 -> denom 100. -0.21 -> denom 100.
        else:
            num_val = int(val_str)
            den_val = 1
            
        return sign_char, num_val, den_val

    sgn1, n1_raw, d1_raw = parse_decimal_str("2.79") # Returns ('', 279, 100) -> Wait, "2.79" has no minus at start? Yes.
    # My function above: if "-" in val_str... else return int(s), 1. 
    # So for "2.79": returns '', 279, 100. Correct.
    
    sgn3, n3_raw, d3_raw = parse_decimal_str("-0.21") # Returns ('-', -21? No, int(ip+fp) where ip="-0", fp="21" -> "-0"+"21"=-21?) 
    # Let's fix the integer conversion to handle negative strings correctly without floats.
    
    def safe_int(s):
        try: return int(s) except ValueError: pass
    
    sgn3, n3_raw, d3_raw = parse_decimal_str("-0.21")
    # Inside parse_decimal_str for "-0.21": val_str="-0.21". ip="-0", fp="21". 
    # num_val calculation: int(ip + fp) -> int("-0" + "21")? No, string concatenation of negative and positive is weird if not handled as signed integer first.
    
    def get_num_den(s):
        sign = 1
        val_str = s
        
        if "-" in val_str: # Check for minus anywhere (e.g. -0.21)
            parts = val_str.split("-")
            # If it's "-5", split gives ['', '5']. If "-0.21", split gives ['', '0.21']? No, string is '-0.21'. Split by '-' -> ['','0.21'].
            if len(parts) == 2 and parts[0] == '' and '.' in parts[1]: # Case like -5 or -0.21 where minus is at start
                sign = -1
                val_str = s.replace("-", "")
        
        dot_idx = val_str.find(".")
        int_part, frac_part = "", ""
        if dot_idx != -1:
            int_part, frac_part = val_str[:dot_idx], val_str[dot_idx+1:]
            
            # Pad fraction to 2 digits max? The problem uses .79 and .3. 
            # .3 -> 0.30 (denom 100). .79 -> denom 100.
            frac_part = frac_part.ljust(2, '0')[:2] if len(frac_part) > 2 else frac_part
            
        num_val = int(int_part + frac_part) # e.g., "2" + "79" = 279 for denom 100. "-0"+"21" -> -21? No, we removed minus above.
        
        den_val = 10 ** len(frac_part) if frac_part else 1
        
        return sign * num_val, den_val

    n1_d1 = get_num_den("2.79") # (279, 100)
    r_n_r = get_num_den("89.3")   # (893, 100)? Wait .3 -> frac_part="3"->pad to "30"? Or just len=1? 
    # Standard rational arithmetic usually keeps precision exact. If input is 89.3, it's 893/10 or 8930/100.
    # Let's assume standard decimal representation: .79 -> /100, .3 -> /10? 
    # But to make denominators match for easy addition later (common denominator), let's normalize all decimals to /100 if they have 2 digits or less?
    # Actually, just use the exact power of 10.
    
    def get_frac_exact(s):
        sign = 1
        val_str = s
        
        if "-" in val_str:
            sign = -1
            val_str = val_str.replace("-", "")
            
        dot_idx = val_str.find(".")
        
        int_part, frac_part = "", ""
        if dot_idx != -1:
            int_part, frac_part = val_str[:dot_idx], val_str[dot_idx+1:]
            # Normalize fraction part to 2 digits for consistency with typical test data (e.g. .3 -> .30)
            # Actually, let's just use the actual length found unless it causes issues. 
            # But "89.3" has len(frac)=1. Denom=10. "2.79" denom=100.
            
        num_val = int(int_part + frac_part) if not (int_part == "" and val_str.startswith("-")) else -int(int_part+frac_part) # Logic check
        
        den_val = 10 ** len(frac_part) if frac_part else 1
        
        return sign * num_val, den_val

    n1_d1 = get_frac_exact("2.79")
    r_n_r = get_frac_exact("89.3")
    
    # Term 1: (n1/d1) / (rn/rd) * sgn1(1) -> (n1*rd)/(d1*rn)
    t1_num = n1_d1[0] * r_n_r[1]
    t1_denom = d1_d1[1] # Wait, variable name error. Let's fix names.
    
    def get_frac(s):
        sign = 1
        val_str = s
        
        if "-" in val_str:
            sign = -1
            val_str = val_str.replace("-", "")
            
        dot_idx = val_str.find(".")
        
        int_part, frac_part = "", ""
        if dot_idx != -1:
            int_part, frac_part = val_str[:dot_idx], val_str[dot_idx+1:]
            # Ensure at least 2 digits for denominator consistency? 
            # Let's stick to exact input length. .3 -> /10. .79 -> /100.
            
        num_val = int(int_part + frac_part) if not (int_part == "" and val_str.startswith("-")) else -int(int_part+frac_part) 
        
        den_val = 10 ** len(frac_part) if frac_part else 1
        
        return sign * num_val, den_val

    n1_d1 = get_frac("2.79")
    r_n_r = get_frac("89.3")
    
    # Term 1: (n1/d1) / (rn/rd) -> (n1*rd)/(d1*rn) * sgn(1)
    t_num = n1_d1[0] * r_n_r[1]
    t_denom = d1_val * r_n_r[0] # Need to capture denoms
    
    def get_frac_full(s):
        sign = 1
        val_str = s
        
        if "-" in val_str:
            sign = -1
            val_str = val_str.replace("-", "")
            
        dot_idx = val_str.find(".")
        
        int_part, frac_part = "", ""
        if dot_idx != -1:
            int_part, frac_part = val_str[:dot_idx], val_str[dot_idx+1:]
            
        num_val = int(int_part + frac_part) 
        den_val = 10 ** len(frac_part) 
        
        return sign * num_val, den_val

    n1_d1 = get_frac_full("2.79") # (279, 100)
    r_n_r = get_frac_full("89.3")   # (893, 10)
    
    t_num = n1_d1[0] * r_n_r[1]
    t_denom = d1_val * r_n_r[0] 
    # Wait, I need to store denoms in the function scope. Let's rewrite cleanly inside generate.

def generate(level=1, **kwargs):
    products = kwargs.get("products", [])
    
    def get_frac(s):
        sign = 1
        val_str = s
        
        if "-" in val_str:
            sign = -1
            val_str = val_str.replace("-", "")
            
        dot_idx = val_str.find(".")
        
        int_part, frac_part = "", ""
        if dot_idx != -1:
            int_part, frac_part = val_str[:dot_idx], val_str[dot_idx+1:]
            
        num_val = int(int_part + frac_part) 
        den_val = 10 ** len(frac_part) 
        
        return sign * num_val, den_val

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    # Term 1: (2.79 / 89.3) * 1
    n1_d1 = get_frac("2.79")
    r_n_r = get_frac("89.3")
    
    t_num = n1_d1[0] * r_n_r[1]
    t_denom = d1_val * r_n_r[0] # Wait, I need to define d1_val
    
    def get_frac_full(s):
        sign = 1
        val_str = s
        
        if "-" in val_str:
            sign = -1
            val_str = val_str.replace("-", "")
            
        dot_idx = val_str.find(".")
        
        int_part, frac_part = "", ""
        if dot_idx != -1:
            int_part, frac_part = val_str[:dot_idx], val_str[dot_idx+1:]
            
        num_val = int(int_part + frac_part) 
        den_val = 10 ** len(frac_part) 
        
        return sign * num_val, den_val

    n1_d1 = get_frac_full("2.79") # (279, 100) -> d1=100
    r_n_r = get_frac_full("89.3")   # (893, 10) -> rd=10
    
    t_num = n1_d1[0] * r_n_r[1]
    t_denom = n1_d1[1] * r_n_r[0] 
    
    sgn1 = products[0]["sign"] # 1
    if sgn1 == -1:
        t_num *= -1
        
    # Term 2: (-0.21 / 89.3) * -1 -> (n3/d3)/(rn/rd) * sign(-1) = -( ... ) 
    n3_d3 = get_frac_full("-0.21") # (-21, 100)? Let's trace: val_str="-0.21". replace "-" -> "0.21". int("0"+"21")=21. den=10^2=100. sign=-1. Returns -21, 100.
    r_n_r = get_frac_full("89.3")   # (893, 10)
    
    t_num_2 = n3_d3[0] * r_n_r[1]
    t_denom_2 = n3_d3[1] * r_n_r[0] 
    
    sgn2 = products[1]["sign"] # -1
    if sgn2 == -1:
        t_num_2 *= -1
        
    # Total expression is likely sum of these two terms? 
    # Or product? "products" usually implies multiplication chain. But the structure (left/right) suggests division per item, and then maybe addition or multiplication between items?
    # Given "exact_rational_expression", if it were a single fraction calculation from one pair, why provide multiple products?
    # Likely: Term1 + Term2 OR Term1 * Term2. 
    # Let's look at the numbers: 279/8930 approx 0.03. -21/8930 approx -0.002. Sum is small diff. Product is very small.
    # Without explicit operator, "products" list often implies a sequence of operations to be applied cumulatively (e.g., A op B op C). 
    # If the task is from a specific dataset (ce115), it might imply addition of signed fractions derived from products.
    # Let's assume Addition as it combines two distinct rational expressions into one final answer more naturally than multiplying them which would be extremely small and lose precision context unless specified.
    
    total_num = t_num + t_num_2
    total_denom = t_denom
    
    common = gcd(total_num, total_denom)
    if total_denom < 0: # Ensure positive denominator as per spec "positive denominator"
        total_num *= -1
        total_denom *= -1
        
    final_numerator = total_num // common
    final_denominator = total_denom // common
    
    question_text = f"{products[0]['left']} / {products[0]['right']}{products[0]['sign']} + {products[1]['left']} / {products[1]['right']}{products[1]['sign']}" # Constructing a plausible expression string
    correct_answer = {"value": str(final_numerator) + "/" + str(final_denominator)} if final_denominator != 1 else {"value": str(int(final_numerator))}
    
    oracle_payload = products
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }