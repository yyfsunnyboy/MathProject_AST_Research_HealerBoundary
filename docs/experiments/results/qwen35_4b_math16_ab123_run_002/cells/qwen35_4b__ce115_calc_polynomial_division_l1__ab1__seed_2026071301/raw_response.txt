def generate(level=1, **kwargs):
    polynomials = {
        "dividend_coefficients": [6, 0, 6],
        "divisor_coefficients": [1, -4]
    }
    
    dividend_poly = sum(c * (x**i) for i, c in enumerate(polynomials["dividend_coefficients"])[::-1]) if False else None # Placeholder logic to ensure structure
    
    divisor_poly = sum(c * (x**i) for i, c in enumerate(polynomials["divisor_coefficients"])[::-1])
    
    dividend_coeffs_str = f"{polynomials['dividend_coefficients'][0]}{len([c for c in polynomials['dividend_coefficients'] if c != 0 and abs(c)<1)]}x^{len(polynomials['dividend_coefficients'])-2}{polynomials['dividend_coefficients'][2]}"
    divisor_coeffs_str = f"{polynomials['divisor_coefficients'][0]}{len([c for c in polynomials['divisor_coefficients'] if c != 0 and abs(c)<1)]}x^{len(polynomials['divisor_coefficients'])-2}{abs(polynomials['divisor_coefficients'][1])}"
    
    question_text = f"Perform polynomial division: {polynomial_to_string([6,0,6], 'x')} \\div {polynomial_to_string([-4, 1], 'x')}. Express the result as quotient and remainder."
    
    # Manual Division for [6, 0, 6] / [1, -4]:
    # Dividend: 6 + 0*x^2 + 6*x = 6x^3 (Wait, index mapping check)
    # Standard convention in these tasks often maps last element to highest degree or first.
    # Let's assume standard numpy-like order [a_n, ..., a_1, a_0] where a_0 is constant? Or reverse?
    # Given the example coefficients: Dividend=[6, 0, 6], Divisor=[1, -4].
    # If Descartes (highest first): 6x^2 + 0x + 6 divided by x - 4.
    # Quotient: 6x + 24 -> Remainder? 
    # Let's try polynomial division manually with standard algebraic notation where [c_n, ..., c_1, c_0] means sum(c_i * x^i). No usually it's sum(c_i * x^(n-i)).
    # Assumption: List is coefficients from highest degree to constant term.
    # Dividend: 6x^2 + 0*x + 6 = 6x^2 + 6. (Degree 2) -> Wait, length 3 means max deg 2? Or if index 0 is x^n then n=2.
    # If [6, 0, 6] -> 6x^2 + 6. Divisor [1, -4] -> x-4.
    # (6x^2+6)/(x-4) = ?
    # 6x(x-4)/x... 
    # Let's re-evaluate based on typical "polynomial division" problems in such contexts often using reverse order for coefficients (low to high).
    # If [6, 0, 6] means 6 + 0*x + 6*x^2 = 6x^2+6. Same result.
    # Let's try: Dividend=[1, -4], Divisor=[...]. No the input is fixed.
    
    # Recalculate Division Logic precisely:
    # Polynomial A (Dividend): coeffs [a_n, ..., a_0] or [a_0, ...]? 
    # Context "ce115_calc_polynomial_division_l1" suggests simple integer arithmetic.
    # Let's assume the list represents coefficients for x^k to x^0 where k=len-1? Or 0 to len-1?
    # Usually in Python lists: [c_0, c_1] often means c_0*x + c_1 (if small) or c_n...c_0.
    # Let's assume standard mathematical representation in code challenges is usually high-to-low index for the list provided unless specified "constant first".
    # However, let's look at the numbers: 6x^2+6 divided by x-4? 
    # Or maybe [6, 0, 6] represents 6 + 0*x + 6*x = 12x + 6? No.
    
    # Let's try the interpretation where index i corresponds to x^(n-i).
    # Dividend: 6x^2 + 0x + 6. Divisor: 1x - 4.
    # (6x^2+6) / (x-4): 
    # Step 1: Multiply divisor by 6x -> 6x(x-4)=6x^2-24x. Subtract from dividend? No, we need to match leading terms.
    # Leading term of D is x, L is 6x^2. Quotient starts with 6x.
    # (6x)(x-4) = 6x^2 - 24x.
    # Remainder after this step: (0x + 6) - (-24x) = 24x + 6? No, original dividend has 0*x term.
    # Dividend P(x) = 6x^2 + 0x + 6.
    # Q1(x)*D(x): 6x * (x-4) = 6x^2 - 24x.
    # New Remainder R1: P - Q1*D = (6x^2+0x+6) - (6x^2-24x) = 24x + 6.
    # Next step: Leading term of R1 is 24x. Divisor leading term x. Quotient term 24.
    # Q2(x)*D(x): 24 * (x-4) = 24x - 96.
    # Final Remainder: (24x+6) - (24x-96) = 102.
    # Quotient Coeffs: [6, 24]. Remainder: 102.
    
    # Alternative Interpretation: List is low to high power? 
    # Dividend: 6 + 0*x + 6x^2 -> Same polynomial.
    # If the list was meant to be interpreted differently... but standard math notation usually aligns index with degree if sorted, or requires explicit definition. Given "Exact arithmetic", let's stick to this calculation which yields clean integers.
    
    quotient_coeffs = [6, 24]
    remainder_coefficients = [102] # Constant term
    
    # Constructing LaTeX for output
    def poly_to_latex(coeffs):
        terms = []
        n = len(coeffs) - 1
        if coeffs[n] == 1 and n > 1: return "x^{}".format(n)
        
        for i, c in enumerate(reversed(coeffs)): # reversed to get high degree first? 
            # Wait, my manual calc used [6,0,6] as [coeff_x2, coeff_x1, coeff_0]. So index 0 is x^(len-1).
            pass
        
        # Re-defining for LaTeX generation based on input list order being High->Low
        # Input: [6, 0, 6] -> 6x^2 + 0x + 6. Latex: "6x^2+6" or "6x^{2}+6".
        
    quotient_latex = f"{quotient_coeffs[0]}x{len(quotient_coeffs)-1}" if len(quotient_coeffs) > 1 else str(quotient_coeffs[0]) + ("\\cdot x" if False else "") # Simplified: 6x^2? No, degree of quotient is deg(div)/deg(divisor).
    # Deg Div = 2. Deg Divis = 1. Quotient Deg = 1. So [c_1, c_0]. My calc gave [6, 24] -> 6x + 24? 
    # Wait: Q terms were 6x then 24. Yes.
    
    quotient_latex_str = "6x+24" if False else None
    
    # Let's refine the LaTeX string construction properly for the output format required (quotient_latex, remainder_latex)
    # Quotient: 6x + 24 -> \( 6x+24 \) or just text? "formal LaTeX delimiters \\( \\)".
    
    final_quotient_str = f"{quotient_coeffs[0]}{'' if quotient_coeffs[-1]==0 else ''}x" # Wait, [6, 24] -> 6x + 24. 
    # If coeffs are [c_n ... c_0], then:
    # Quotient terms: 6*x^1 and 24*x^0.
    
    q_terms = []
    for i in range(len(quotient_coeffs)):
        if quotient_coeffs[i] == 0: continue
        term_val = str(abs(quotient_coeffs[i])) + "x" * (len(quotient_coeffs)-1-i) # Assuming high to low order again? 
        # My manual calc: [6, 24]. If index 0 is x^1 and index 1 is x^0.
        # Term 0: 6*x^(1). Term 1: 24*x^0.
        
    q_latex_parts = []
    for i in range(len(quotient_coeffs)):
        if quotient_coeffs[i] == 0: continue
        exp = len(quotient_coeffs) - 1 - i # If [6, 24], index 0->exp=1, index 1->exp=0. Correct.
        q_latex_parts.append(str(abs(quotient_coeffs[i])) + ("x^{}".format(exp)) if exp > 0 else str(quotient_coeffs[i]))
    quotient_latex = "\\text{+}".join(q_latex_parts) # Join with plus? Or comma separated list of coeffs? 
    # Requirement: "correct_answer must include ... quotient_latex". Usually implies the polynomial expression.
    
    r_terms = []
    for i, c in enumerate(remainder_coefficients):
        if c == 0 and len(r_terms) > 0: continue # Skip zero padding at end? No, remainder is constant here.
        exp = max(len([x for x in remainder_coefficients]) - 1 - i, 0) 
        r_latex_parts.append(str(abs(c)) + ("x^{}".format(exp)) if exp > 0 else str(remainder_coefficients[i])) # Actually just the number
    
    quotient_latex_clean = "6x+24"
    remainder_latex_clean = "102"

    correct_answer_dict = {
        "quotient_coefficients": [6, 24],
        "remainder_coefficients": [102],
        "quotient_latex": "\\( 6x+24 \\)", # Using formal delimiters as requested in text? Or just the string content? 
        # Instruction: "question_text must use formal LaTeX delimiters ... correct_answer must include quotient_latex, remainder_latex".
        # It doesn't explicitly say correct_answer's latex fields MUST have delimiters, but usually they are formatted.
    }

    oracle_payload = polynomials
    
    return {
        "question_text": question_text.replace("x", r"x").replace("\\div", "\\cdot \\frac{1}{") if False else None # Just ensure clean text for the actual output below logic: 
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload
    }

# Re-implementing strictly to match spec without variable confusion and ensuring exact return structure.
def generate(level=1, **kwargs):
    
    # Frozen parameters
    dividend_coeffs = [6, 0, 6]
    divisor_coeffs = [1, -4]
    
    # Interpretation: List is coefficients from highest degree to constant term (standard in many algos)
    # Dividend P(x) = 6*x^2 + 0*x + 6
    # Divisor Q(x) = 1*x + (-4)*x^(-1)? No. [c_n, ..., c_0]. 
    # If divisor is [1, -4], and assuming standard form where index i corresponds to x^(n-i), then:
    # n=2 for dividend (len-1). Divisor len=2 -> degree 1? Or if it's just coefficients of a polynomial.
    # Let's assume the input lists are [a_n, ..., a_0] and we divide P(x) by Q(x).
    # But wait, divisor [1, -4]. If n=1 (degree 1), then x^1 + (-4)x^0 = x-4. This matches my previous manual calc perfectly yielding integer results.
    
    # Polynomial Division Algorithm:
    # Dividend: 6x^2 + 6
    # Divisor: x - 4
    
    quotient_coeffs_list = []
    current_dividend = list(dividend_coeffs)[:] # Copy [6, 0, 6] -> indices 0(6), 1(0), 2(6)? No. 
    # If index corresponds to degree descending?
    # List: [c_k, c_{k-1}, ..., c_0].
    # Dividend coeffs: 6 (deg 2), 0 (deg 1), 6 (deg 0). -> 6x^2 + 6. Correct.
    # Divisor coeffs: 1 (deg 1), -4 (deg 0). -> x - 4. Correct.
    
    current_quotient_coeffs = [0] * len(dividend_coeffs) 
    remainder_coeffs_list = []

    # Perform synthetic-like division or standard long division logic on the list representation
    # We iterate from highest degree of dividend down to divisor's leading term
    
    n_divisor_degree = len(divisor_coeffs) - 1
    current_quotient_index_start = len(current_quotient_coeffs) - 2 
    
    temp_poly = [float(c) for c in dividend_coeffs] 
    # Since we need exact arithmetic, keep integers. Python handles large ints automatically.

    i = n_divisor_degree
    while i < len(temp_poly):
        if abs(temp_poly[i]) == 0 and (i + n_divisor_degree >= len(dividend_coeffs)): break
        
        multiplier = temp_poly[i] // divisor_coeffs[0] # Leading term of quotient part for this step? 
        # Wait, standard division: coeff_of_q * x^k.
        # The leading coefficient of current dividend at position i corresponds to degree (len-1-i).
        
        # Let's use a simpler approach matching the coefficients directly as they are already aligned by power if we assume [high->low].
        # Current temp_poly[i] is coeff for x^(n_divisor_degree + k)? 
        # Actually, let's just compute term by term.
        
    # Re-calculation with explicit polynomial steps:
    # P(x) = 6x^2 + 0x + 6
    # D(x) = x - 4
    
    # Step 1: 6x^2 / x = 6x. Add to quotient list? 
    # Quotient starts with [6, ...] (if we build high->low).
    
    result_quotient_coeffs = []
    temp_dividend = dividend_coeffs[:] 
    
    # Leading term of divisor is at index 0 -> value 1 (coeff x^1)
    lead_coeff_D = divisor_coeffs[0]
    
    idx_start = len(dividend_coeffs) - 2 # We start determining quotient terms from degree n-2 down to ...? 
    # Degree of P: 2. Deg D: 1. Max deg Q: 1. So 2 terms in quotient (x^1, x^0).
    
    idx = len(dividend_coeffs) - 1 # Start at highest power index
    
    q_list = []
    
    for k in range(len(temp_dividend)):
        if temp_dividend[k] == 0 and not any(c != 0 for c in temp_dividend[:k+1]): continue
        
        term_val = int(temp_dividend[k]) / lead_coeff_D # This is wrong. Division must be done sequentially reducing degree by n-1 each time? No, synthetic division steps differently.
        
    # Correct Sequential Reduction:
    # Current dividend P(x). Leading coeff c_n at index 0 (deg len-1). 
    # Next quotient term q_{n-m} = c_n / d_0 * x^{(len(n)-m) - ...}.
    
    # Let's just execute the arithmetic I did manually:
    # Q = [6, 24], R = [102]
    
    final_quotient_coeffs = [6, 24]
    final_remainder_coefficients = [102]
    
    # Generate LaTeX strings
    def make_poly_latex(coeffs):
        if not coeffs: return "0"
        terms = []
        n_degrees = len([x for x in reversed(coeffs) if x!=0]) 
        # If we assume input order is high->low, then coeff[0] is highest.
        
        # Helper to generate string from list [c_k ... c_0] where k=degree
        parts = []
        for i, val in enumerate(reversed(coeffs)): # reversed: 6 (deg2), 0(deg1), 6(deg0) -> No wait input was high->low.
            pass
        
        # Let's assume the list provided [a,b,c] means a*x^2 + b*x + c? 
        # My manual calc used this assumption and got clean integers.
        
        parts = []
        for i, val in enumerate(coeffs):
            if abs(val) == 0: continue
            
            degree_of_term_in_list_idx_i = len(coeffs) - 1 - i 
            
            term_str = str(abs(val)) + "x^{}".format(degree_of_term_in_list_idx_i) if degree_of_term_in_list_idx_i > 0 else str(val)
            
            # Handle sign? The list has negative numbers. 
            # If val is negative, include minus in string construction logic or handle during join.
            term_str = f"{val}" + ("x^{}".format(degree_of_term_in_list_idx_i)) if degree_of_term_in_list_idx_i > 0 else str(val)
            
            parts.append(term_str.replace("+", "+").replace("-", "-")) # Just raw
        
        return " + ".join(parts).replace("+ -","-")

    q_latex_parts = []
    for i, val in enumerate(final_quotient_coeffs):
        if abs(val) == 0: continue
        deg = len(final_quotient_coeffs) - 1 - i # [6,24] -> index 0->deg=1? Wait. 
        # If input was high->low: [6x^2...]. Quotient should be high->low too.
        # My manual calc Q = 6x + 24. So coeff list is [6, 24] corresponding to x^1 and x^0?
        # Yes. 
        deg = len(final_quotient_coeffs) - 1 - i
        term_str = str(val) + ("x^{}".format(deg)) if deg > 0 else ""
        
    q_latex_parts.append(term_str.replace("+","+").replace("-","-"))
    
    # Actually, let's construct the LaTeX string directly for clarity.
    quotient_latex_text = "6x+24" 
    remainder_latex_text = "102"

    correct_answer_dict = {
        "quotient_coefficients": [6, 24],
        "remainder_coefficients": [102],
        "quotient_latex": "\\( 6x + 24 \\)", 
        "remainder_latex": "\\( 102 \\)"
    }

    return {
        "question_text": r"Perform polynomial division: \( 6x^2+6 \) \\div \( x-4 \). Express the result as quotient and remainder.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"dividend_coefficients": [6, 0, 6], "divisor_coefficients": [1, -4]}
    }

# Final check on constraints: 
# - Only Python source.
# - def generate(level=1, **kwargs).
# - Return dict with question_text, correct_answer, oracle_payload.
# - Exact arithmetic.
# - No floats in output (integers used).
# - Oracle payload matches frozen parameters exactly.

def generate(level=1, **kwargs):
    # Frozen sampled parameters from task specification
    dividend_coefficients = [6, 0, 6]
    divisor_coefficients = [1, -4]
    
    # Polynomial Division Logic (Manual Calculation for exact match)
    # Dividend P(x) represented by coefficients [c_2, c_1, c_0] -> 6x^2 + 0x + 6
    # Divisor Q(x) represented by coefficients [d_1, d_0] -> x - 4
    
    quotient_coefficients = [6, 24]
    remainder_coefficients = [102]
    
    # Generate LaTeX representations using formal delimiters \\( \) / \\[ ] as per requirement for question_text and answer fields.
    # Question Text: Uses \( \) around polynomials.
    quotient_latex_str = "\\( 6x+24 \\)"
    remainder_latex_str = "\\( 102 \\)"
    
    correct_answer_dict = {
        "quotient_coefficients": quotient_coefficients,
        "remainder_coefficients": remainder_coefficients,
        "quotient_latex": quotient_latex_str,
        "remainder_latex": remainder_latex_str
    }
    
    return {
        "question_text": r"Perform polynomial division: \( 6x^2+6 \) \\div \( x-4 \). Express the result as quotient and remainder.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": {"dividend_coefficients": dividend_coefficients, "divisor_coefficients": divisor_coefficients}
    }