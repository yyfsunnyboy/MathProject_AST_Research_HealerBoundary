def generate(level=1, **kwargs):
    frozen_params = {"products": [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]}
    
    # Parse and compute exact rational arithmetic manually to avoid float errors
    
    def parse_decimal(s):
        if '.' in s:
            int_part, frac_part = s.split('.')
            num = int(int_part) * (10 ** len(frac_part)) + int(frac_part.ljust(len(frac_part), '0')) # Ensure correct length handling
            den = 10 ** len(s.split('.')[1])
        else:
            num = int(s)
            den = 1
        
        if s.startswith('-'):
            num *= -1
            
        return (num, den)

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    def simplify(num, den):
        common = gcd(num, den)
        return (num // common, den // common)

    # Product 1: left=2.79, right=89.3, sign=1 -> + (2.79 * 89.3)
    l1_num, l1_den = parse_decimal("2.79")   # 279/100
    r1_num, r1_den = parse_decimal("89.3")  # 893/10
    
    p1_num = l1_num * r1_num
    p1_den = l1_den * r1_den

    # Product 2: left=-0.21, right=89.3, sign=-1 -> - (-0.21 * 89.3) => + (0.21 * 89.3)
    # Wait, specification says "sign": -1 for the second product entry in frozen params list? 
    # Let's re-read: [{"left": "-0.21", ...}, {"left": "-0.21" is not there... wait input was: 
    # [{"left": "2.79", "right": "89.3", "sign": 1}, {"left": "-0.21", "right": "89.3", "sign": -1}]
    
    l2_num, l2_den = parse_decimal("-0.21") # -21/100
    r2_num, r2_den = parse_decimal("89.3")  # 893/10
    
    p2_raw_num = l2_num * r2_num
    p2_raw_den = l2_den * r2_den
    
    sign_2 = frozen_params["products"][1]["sign"] # -1
    
    # The task is "ce115_calc_exact_rational_expression_l1". Usually implies summing products or evaluating expression.
    # Given the structure, it likely asks for: (Product 1) + (Sign of Product 2 * Value of Product 2)? 
    # Or simply evaluate the list as a sequence? The prompt says "rational_arithmetic".
    # Let's assume standard interpretation: Calculate P1 and then calculate Term2 = sign_2 * (L2 * R2). Then sum them.
    
    term2_num = p2_raw_num * sign_2
    term2_den = p2_raw_den
    
    total_num = p1_num + term2_num
    total_den = p1_den # Denominators are same? No, P1 den is 100*10=1000. Term2 den is 100*10=1000. Yes!
    
    common_gcd = gcd(total_num, total_den)
    final_num = total_num // common_gcd
    final_den = total_den // common_gcd
    
    # Format answer string "p/q" or "-q/p"? Usually p/q where q>0. If num<0, keep sign in num.
    
    if final_den < 0:
        final_num *= -1
        final_den *= -1
        
    ans_str = f"{final_num}/{final_den}"
    
    # Construct LaTeX for question text based on frozen params structure
    p1_left_latex = r"\frac{2.79}{1} \times 89.3" if "2.79" else r"2.79" 
    # Actually, inputs are decimals in string form but treated as rationals. 
    # Question text should reflect the exact input strings provided in frozen_params for clarity or standard math notation?
    # Let's use the raw values from frozen params to construct a clean LaTeX expression representing the sum of products.
    
    p1_val = "2.79"
    r1_val = "89.3"
    sgn1_str = "+" if frozen_params["products"][0]["sign"] == 1 else "-"
    
    l2_val = "-0.21"
    r2_val = "89.3"
    sgn2_str = "+" if frozen_params["products"][1]["sign"] == 1 else "-"
    
    # Constructing the expression: (sgn1 * p1_left * p1_right) + (sgn2 * l2_left * r2_right)? 
    # Or just summing the signed products? The "sign" field likely indicates the operator before that term or the sign of the result.
    # Let's assume the expression is: (+ 2.79 \times 89.3) + (- -0.21 \times 89.3)? 
    # Or maybe it's a list of terms to sum? "products" implies multiple multiplications summed up.
    
    term1_latex = f"{p1_val} \\cdot {r1_val}" if frozen_params["products"][0]["sign"] == 1 else f"-{p1_val} \\cdot {r1_val}"
    # Wait, sign=1 usually means positive contribution. 
    # Term 2: left is "-0.21". If sign=-1, does it mean subtract the product? Or multiply by -1 again?
    # Let's assume standard algebraic sum of terms where 'sign' dictates the coefficient relative to (left * right).
    
    term1_raw = f"{p1_val} \\cdot {r1_val}" if frozen_params["products"][0]["sign"] == 1 else f"-{p1_val} \\cdot {r1_val}"
    # Actually, simpler: Just write the terms as they appear in math context. 
    # Term 1: + (2.79)(89.3)
    # Term 2: - (-0.21)(89.3) ? Or just add them? 
    # Let's construct a generic "Calculate:" prompt with the specific numbers from frozen_params.
    
    q_text = f"Compute the exact value of $\\left( {frozen_params['products'][0]['sign']} \\cdot {p1_val} \\times {r1_val} \\right) + \\left( {frozen_params['products'][1]['sign']} \\cdot {l2_val} \\times {r2_val} \\right)$."
    # Wait, sign is integer 1 or -1. LaTeX needs +/- signs usually for readability in text unless using explicit multiplication by variable x? 
    # Better: "Compute $\\text{sgn}_1 (A) + \\text{sgn}_2 (B)$"? No, keep it simple math problem style.
    
    if frozen_params["products"][0]["sign"] == 1:
        t1 = f"{p1_val} \\times {r1_val}"
    else:
        t1 = f"-{p1_val} \\times {r1_val}"
        
    if frozen_params["products"][1]["sign"] == 1:
        t2 = f"+ {l2_val} \\times {r2_val}" # Note l2 is negative string "-0.21"
    else:
        t2 = f"- ({l2_val}) \\times {r2_val}" if frozen_params["products"][1]["sign"] == -1 and str(l2_val).startswith("-") else f"+ {l2_val} \\times {r2_val}" # Complex logic. 
        # Let's simplify: Just sum the signed products directly as written in params?
        
    # Re-evaluating "sign" meaning based on typical dataset generation for math tasks (like GSM8K or similar rational arithmetic):
    # Often it defines a list of operations to perform sequentially or independently summed.
    # Given "products", likely: Sum( sign_i * left_i * right_i ).
    
    t1_val = frozen_params["products"][0]["left"] if frozen_params["products"][0]["sign"] == 1 else f"-{frozen_params['products'][0]['left']}"
    # Wait, if left is "-0.21" and sign=-1, then term is -(-0.21 * ...). 
    # Let's stick to the raw calculation logic: Term = sign * (float(left) * float(right)).
    
    t1_str_latex = f"{frozen_params['products'][0]['left']} \\times {r1_val}" if frozen_params["products"][0]["sign"] == 1 else f"-{abs(float(frozen_params['products'][0]['left'])):.2f} \\times {r1_val}".replace(".","") # No, keep decimals.
    
    # Let's just use the raw strings and apply sign visually in LaTeX if needed for clarity, or assume standard summation notation.
    # To be safe and formal: 
    term1_latex = f"{frozen_params['products'][0]['left']} \\times {r1_val}" if frozen_params["products"][0]["sign"] == 1 else f"-{frozen_params['products'][0]['left'].replace('-', '')} \\times {r1_val}" # This is risky with negative numbers.
    
    # Robust LaTeX construction:
    def make_term(left, right, sign):
        if left.startswith('-'):
            val = left[1:] + " (" 
            return f"-{val}{right})" if sign == -1 else f"+ {left} \\times {right}" # Ambiguous.
        
        # Simplest robust way: Just write the expression as sum of terms with explicit signs from 'sign' field applied to (L*R).
        l_str = left.replace("-", "-") 
        r_str = right
        
        if sign == 1:
            return f"+ {l_str} \\times {r_str}"
        else:
            # If L is negative, e.g., -0.21, and sign=-1 -> term is + (positive value)? Or subtract the product?
            # Let's assume 'sign' modifies the whole product result.
            return f"- ({l_str}) \\times {r_str}" if left.startswith("-") else f"- {l_str} \\times {r_str}"

    t1_latex = make_term(frozen_params["products"][0]["left"], r1_val, frozen_params["products"][0]["sign"])
    # Remove leading + for cleaner text or keep? Usually "Compute A + B". 
    if t1_latex.startswith("+"):
        t1_latex = t1_latex[2:] # remove "+ "
        
    t2_latex = make_term(frozen_params["products"][1]["left"], r2_val, frozen_params["products"][1]["sign"])
    
    q_text = f"Compute the exact value of $\\text{term}_1 + \\text{term}_2$ where term$_1={t1_latex}$ and term$_2={t2_latex}$. Simplify to an irreducible fraction."
    # Or simpler: "Calculate:" followed by the expression.
    
    final_q_text = f"Compute $\\left( {frozen_params['products'][0]['sign']} \\cdot {p1_val} \\times {r1_val} \\right) + \\left( {frozen_params['products'][1]['sign']} \\cdot {l2_val} \\times {r2_val} \\right)$."
    # Wait, if sign is -1 and left is negative string "-0.21", then mathematically it's (-1)*(-0.21*89.3) = + (0.21*89.3). 
    # The LaTeX should reflect the intended operation clearly.
    
    # Let's try to make the question text match the exact arithmetic logic:
    term1_expr = f"{p1_val} \\times {r1_val}" if frozen_params["products"][0]["sign"] == 1 else f"-{abs(float(p1_val)):.2f} \\times {r1_val}".replace(".","") # No, keep decimals. 
    # Let's just use the raw string and prepend sign char?
    
    sgn_char = "+" if frozen_params["products"][0]["sign"] == 1 else "-"
    term1_expr = f"{sgn_char} {p1_val} \\times {r1_val}"
    
    sgn_char2 = "+" if frozen_params["products"][1]["sign"] == 1 else "-"
    # If left is negative, e.g. "-0.21", and we want to subtract the product (-0.21 * ...), it becomes + (positive). 
    # But usually these datasets just list terms: (+ A*B) + (- C*D).
    
    term2_expr = f"{sgn_char2} {l2_val} \\times {r2_val}"
    
    q_text = f"Compute $\\left( {term1_expr} \\right) + \\left( {term2_expr} \\right)$."

    # Correct answer format: "value (irreducible p/q string)" and canonical_latex.
    ans_str = f"{final_num}/{final_den}" if final_den != 0 else str(final_num).rstrip('0').rstrip('.') # Handle integer case? 
    # If denominator is 1, usually just the number or n/1? "irreducible p/q string". Usually implies fraction format even for integers (n/1) unless specified otherwise.
    # Let's assume standard math notation: if den=1, return str(num). Else f"{num}/{den}".
    
    canonical_latex = ans_str
    
    result_dict = {
        "question_text": q_text,
        "correct_answer": f"value={ans_str}; canonical_latex=${canonical_latex}$", # Wait spec: "must include value (irreducible p/q string) and canonical_latex". 
        # Maybe format is just the latex of the answer? Or a dict inside correct_answer? 
        # Spec says: "correct_answer must include value ... and canonical_latex."
        # Likely structure: {"value": "...", "canonical_latex": "..."} or concatenated string.
        # Given previous examples in similar tasks, often it's a single string like "$\\frac{p}{q}$". 
        # But instruction says "include value... AND ...". Let's make correct_answer a dict for clarity if allowed, but usually these are strings.
        # Re-reading: "correct_answer must include value (irreducible p/q string) and canonical_latex."
        # I will format it as "$\\frac{p}{q}$" which serves both? Or explicit keys? 
        # Let's assume the field `correct_answer` is a dict with 'value' and 'canonical_latex'.
        
    }

    if final_den == 1:
        ans_str = str(final_num)
        canonical_latex = f"${final_num}$"
    else:
        canonical_latex = rf"\frac{{{final_num}}}{{{final_den}}}"
    
    result_dict["correct_answer"] = {
        "value": ans_str,
        "canonical_latex": canonical_latex
    }

    return {
        "question_text": q_text.replace("term_1", "\\text{Term}_1").replace("term_2", "\\text{Term}_2"), # Clean up text slightly if needed. 
        "correct_answer": result_dict["correct_answer"],
        "oracle_payload": frozen_params
    }