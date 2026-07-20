def generate(level=1, **kwargs):
    import math
    
    # Frozen sampled parameters from task specification
    expression = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Compute the exact rational value of the expression using Fraction logic manually to ensure irreducibility and correctness
    # Expression: A/B + C/D - ((E/F) - (G/H))
    # = A/B + C/D - E/F + G/H
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    def lcm(a, b):
        if a == 0 or b == 0:
            return 0
        return abs((a * b)) // gcd(a, b)

    # Parse terms from the frozen expression string manually to ensure exactness without external eval risks on general input
    # Terms identified in "9/22 + 11/18 - (23/22 - 7/18)":
    # Term 1: +9/22
    # Term 2: +11/18
    # Inner group: -(23/22) -> becomes -23/22
    # Inner group: -(-7/18) -> becomes +7/18
    
    terms = [
        {"num": 9, "den": 22},      # Term 1 (positive)
        {"num": 11, "den": 18},     # Term 2 (positive)
        {"num": -23, "den": 22},    # Term 3 (negative of first inner term)
        {"num": 7, "den": 18}       # Term 4 (positive second inner term because double negative)
    ]

    common_den = terms[0]["den"]
    for t in terms:
        current_lcm = lcm(common_den, abs(t["den"]))
        if common_den != current_lcm or any(den != common_den and den == 18 or den == 22 for d in [common_den]): 
             # Re-calculate LCM iteratively safely
            pass
        
    def reduce_fraction(numerator, denominator):
        g = gcd(numerator, denominator)
        return numerator // g, denominator // g

    total_numerator = 0
    
    # Compute common denominator for all terms: lcm(22, 18) -> 198
    current_denom = abs(lcm(abs(terms[0]["den"]), abs(terms[1]["den"]))) 
    if len(terms) > 2:
        current_denom = abs(lcm(current_denom, abs(terms[2]["den"])))
    if len(terms) > 3:
        current_denom = abs(lcm(current_denom, abs(terms[3]["den"])))

    for t in terms:
        scaled_numerator = (t["num"] * (current_denom // abs(t["den"])))
        total_numerator += scaled_numerator
    
    final_num, final_den = reduce_fraction(total_numerator, current_denom)
    
    # Ensure denominator is positive; adjust numerator if needed
    if final_den < 0:
        final_num *= -1
        final_den *= -1
        
    correct_answer_str = f"{final_num}/{final_den}"

    return {
        "question_text": r"Compute the exact value of $9/22 + 11/18 - (23/22 - 7/18)$ and express your answer as an irreducible fraction.",
        "correct_answer": correct_answer_str,
        "oracle_payload": {
            "expression": expression
        }
    }