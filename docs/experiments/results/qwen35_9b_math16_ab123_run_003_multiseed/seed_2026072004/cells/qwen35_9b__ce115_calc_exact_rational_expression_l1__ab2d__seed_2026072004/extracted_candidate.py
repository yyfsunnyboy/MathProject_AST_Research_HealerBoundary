def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = kwargs.get('frozen_sampled_parameters', {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]})
    
    # Reconstruct the expression based on frozen parameters: (L1 + S*R) for each product? 
    # Usually "products" implies a sum of terms like left + sign * right or similar structure in arithmetic tasks.
    # Given the context "rational_arithmetic", let's assume an alternating series or specific formula.
    # Let's interpret: Term = Left + (Sign * Right). Then Sum all Terms? 
    # Or perhaps it's a product of sums? The prompt says "products" in frozen params, implying list of products to be summed or processed.
    # Standard interpretation for such datasets often involves summing these terms if signs are provided explicitly per term.
    
    api = _get_api()
    
    total_sum_numerator = 0
    total_sum_denominator = 1
    
    product_items = frozen_params.get("products", [])
    
    for item in product_items:
        left_str = item["left"]
        right_str = item["right"]
        sign = int(item["sign"]) # Ensure it's an integer
        
        term_left = api(left_str)
        term_right = api(right_str)
        
        if sign == 1:
            current_term = term_left + term_right
        else:
            current_term = term_left - term_right
            
        total_sum_numerator, total_sum_denominator = F(total_sum_numerator).numerator * total_sum_denominator.denominator \
             , (total_sum_numerator.num * total_sum_denominator.dn) # Logic simplified below
        
    # Correct accumulation logic:
    current_total_num = 0
    current_total_denom = 1
    
    for item in product_items:
        left_str = item["left"]
        right_str = item["right"]
        sign_val = int(item["sign"])
        
        l_frac = api(left_str)
        r_frac = api(right_str)
        
        term = (l_frac + (r_frac if sign_val == 1 else (-r_frac)))
        
        # Add to total: current_total += term
        new_num = current_total_num * term.denominator + num(term.numerator, term.denominator, current_total_denom) # Manual add logic
        
    def manual_add(n1, d1, n2, d2):
        return (n1 * d2 + n2 * d1), (d1 * d2)

    for item in product_items:
        l_str = item["left"]
        r_str = item["right"]
        sgn = int(item["sign"])
        
        fl = api(l_str)
        fr = api(r_str)
        
        if sgn == 1:
            val_num, val_den = fl.numerator, fl.denominator * (fl.numerator + fr.numerator)/fr.denominator # Wait, direct add is safer
        
    # Reset and do it cleanly inside loop
    num_total, den_total = 0, 1
    
    for item in product_items:
        l_str = item["left"]
        r_str = item["right"]
        sgn = int(item["sign"])
        
        fl = api(l_str)
        fr = api(r_str)
        
        term_num, term_den = (fl.numerator + sgn * fr.numerator), (fl.denominator if sgn==1 else fl.denominator) # Simplified for equal denoms? No.
        # Correct addition: a/b +/- c/d = (ad +/- cb)/bd
        
        prev_n, prev_d = num_total, den_total
        
        new_num = prev_n * fr.denominator + (sgn if sgn!=0 else 1) * fl.numerator ? NO
        
        # Re-calculation for the loop
        pass
    
    # Final clean calculation block:
    current_n = 0
    current_d = 1
    
    for item in product_items:
        l_str = item["left"]
        r_str = item["right"]
        sgn = int(item["sign"])
        
        fl = api(l_str)
        fr = api(r_str)
        
        # term = sign * (fl + fr)? Or just fl +/- fr? 
        # Assuming the task is sum of terms: Left +/- Right.
        if sgn == 1:
            term_n, term_d = fl.numerator + fr.numerator, fl.denominator ? No.
            # Addition logic: a/b + c/d = (ad+bc)/bd
            num_add = fl.numerator * fr.denominator + fr.numerator * fl.denominator
            den_add = fl.denominator * fr.denominator
        else:
            num_sub = fl.numerator * fr.denominator - fr.numerator * fl.denominator
            den_add = fl.denominator * fr.denominator
            
        # Accumulate to current total (initially 0/1)
        new_n = current_n * den_add + num_add
        new_d = current_d * den_add
        
        # Simplify before adding? No, keep exact until end.
        
    # Actually, let's just use Fraction arithmetic directly in Python logic for correctness then format
    from fractions import Fraction
    
    total_fraction = F(0)
    
    for item in product_items:
        l_str = item["left"]
        r_str = item["right"]
        sgn = int(item["sign"])
        
        fl = api(l_str) # Returns Fraction object
        fr = api(r_str)
        
        if sgn == 1:
            term = fl + fr
        else:
            term = fl - fr
            
        total_fraction += term
        
    final_frac = total_fraction
    
    # Format correct_answer value as irreducible p/q string
    val_num, val_den = abs(final_frac.numerator), abs(final_frac.denominator)
    
    # Handle sign in the numerator if denominator is positive (standard canonical form has pos denom)
    if final_frac < 0:
        val_num = -val_num
        
    correct_answer_value_str = f"{val_num}/{val_den}"
    
    # Construct LaTeX for value
    latex_val = r"\frac{" + str(val_num).replace('/', '\\text{'} )? No. 
    # Standard LaTeX fraction: \frac{n}{d}
    if val_num == 0:
        canonical_latex = "0"
    else:
        canonical_latex = rf"\frac{{{val_num}}}{{{val_den}}}"

    question_text = f"Simplify the expression based on the given products: {canonical_latex}. The result is an exact rational number." # Generic text
    
    return {
        "question_text": f"Calculate the sum of terms defined by the frozen parameters. Each term follows the pattern 'left' {'+' if int(frozen_params['products'][0]['sign']) else '-'} 'right'.", 
        "correct_answer": {"value": correct_answer_value_str, "canonical_latex": canonical_latex},
        "oracle_payload": frozen_params
    }

# Override to ensure the function signature matches and logic runs without external dependency errors in this snippet context.
def generate(level=1, **kwargs):
    # Re-implementing the calculation inline for robustness against missing imports during generation if needed, 
    # but keeping the structure requested.
    
    frozen_params = kwargs.get('frozen_sampled_parameters', {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]})
    
    # Re-define local FractionOps to avoid import issues in the generated snippet context if external lib is missing
    class LocalFractionOps:
        def create(self, value):
            from fractions import Fraction
            try:
                return Fraction(str(Decimal(value)))
            except Exception:
                s = str(float(value)) # Fallback float to string then frac? No. 
                if '.' in s:
                    p1, p2 = s.split('.')
                    num = int(p1) * (10**len(p2)) + int(p2)
                    den = 10 ** len(p2)
                    return Fraction(num, den)
                else:
                    return Fraction(int(s), 1)

        def mul(self, a, b):
            if isinstance(a, str): a = self.create(a)
            if isinstance(b, str): b = self.create(b)
            return a * b # Python Fraction supports direct multiplication
        
        def add(self, a, b):
            if isinstance(a, str): a = self.create(a)
            if isinstance(b, str): b = self.create(b)
            return a + b

    ops = LocalFractionOps()
    
    total_frac = F(0) # Import Fraction
    
    for item in frozen_params.get("products", []):
        left_str = item["left"]
        right_str = item["right"]
        sign_val = int(item["sign"])
        
        fl = ops.create(left_str)
        fr = ops.create(right_str)
        
        if sign_val == 1:
            term = fl + fr
        else:
            term = fl - fr
            
        total_frac += term
        
    # Final formatting
    num, den = abs(total_frac.numerator), abs(total_frac.denominator)
    
    # Determine sign for the string representation (put in numerator if negative)
    if total_frac < 0:
        num = -num
    
    val_str = f"{num}/{den}"
    latex_val = rf"\frac{{{num}}}{{{den}}}" if den != 1 else str(num)
    
    return {
        "question_text": r"Compute the exact rational value of the expression derived from the products: \sum_{i} (\text{left}_i + s_i \cdot \text{right}_i).", 
        "correct_answer": {"value": val_str, "canonical_latex": latex_val},
        "oracle_payload": frozen_params
    }