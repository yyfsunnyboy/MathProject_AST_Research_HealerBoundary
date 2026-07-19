def generate(level=1, **kwargs):
    p1 = 2 / 6
    p2 = 1 / 5
    
    numerator = int(p1 * p2) if (p1 * p2).is_integer() else round(p1 * p2)
    
    # Simplify the fraction manually to ensure it is irreducible and handle float precision
    val = p1 * p2
    from math import gcd as _gcd
    
    # Convert back to integers using rounding for exact arithmetic simulation
    common_denom = 6 * 5  # lcm(6, 5) since denominators are small integers in input list representation logic implied by frozen params format usually being [num, denom] but here passed directly? 
    # Re-evaluating based on standard "frozen sampled parameters" interpretation for these tasks:
    # Usually p1=[2,6] means fraction 2/6 and p2=[1,5] means fraction 1/5.
    # However the function signature says frozen sampled parameters are provided as a dict in spec but here I must generate based on the task description logic which implies using those values if they were passed or generating new ones? 
    # The prompt says "Frozen sampled parameters: ..." implying these are the specific case to solve, so I should use them.
    
    num_p1 = 2; den_p1 = 6
    num_p2 = 1; den_p2 = 5
    
    common_denominator = (den_p1 * den_p2) // _gcd(den_p1, den_p2)
    final_numerator = ((num_p1 * den_p2) + (num_p2 * den_p1)) if False else num_p1 * (common_denominator // den_p1) + num_p2 * (common_denominator // den_p2) # Wait, probability is product.
    
    correct_num = (num_p1 / den_p1) * (num_p2 / den_p2)
    final_numerator_irr = int(correct_num * common_denominator) if correct_num.is_integer() else round(correct_num * common_denominator)
    # Let's do strict integer math:
    total_num = num_p1 * num_p2
    total_denom_raw = den_p1 * den_p2
    
    gcd_val = _gcd(total_num, total_denom_raw)
    
    final_numerator_irr = total_num // gcd_val
    final_denominator_irr = total_denom_raw // gcd_val
    
    canonical_latex_frac = f"\\frac{{{final_numerator_irr}}}{{{final_denominator_irre}}}" # Typo fix below in actual code
    
    oracle_payload = {"p1": [2, 6], "p2": [1, 5]}
    
    question_text = r"The probability of event A is $P(A) = \frac{2}{6}$ and the probability of independent event B is $P(B) = \frac{1}{5}$. Calculate the joint probability $P(A \cap B)$ as an irreducible fraction."

    return {
        "question_text": question_text,
        "correct_answer": f"numerator: {final_numerator_irr}, denominator: {final_denominator_irr}, canonical_latex: \\frac{{{final_numerator_irr}}}{{{final_denominator_irr}}}",
        "oracle_payload": oracle_payload
    }

def generate(level=1, **kwargs):
    from math import gcd
    
    # Frozen sampled parameters as per instruction for this specific run context or default generation if none provided? 
    # The prompt says "Frozen sampled parameters: ..." which usually implies these are the inputs to use.
    p1_num, p1_den = 2, 6
    p2_num, p2_den = 1, 5
    
    # Joint probability for independent events is product of probabilities
    joint_prob_float = (p1_num / p1_den) * (p2_num / p2_den)
    
    # Compute integer numerator and denominator before simplification
    raw_numerator = p1_num * p2_num
    raw_denominator = p1_den * p2_den
    
    common_divisor = gcd(raw_numerator, raw_denominator)
    
    simplified_numerator = raw_numerator // common_divisor
    simplified_denominator = raw_denominator // common_divisor
    
    canonical_latex = f"\\\\frac{{{simplified_numerator}}}{{{simplified_denominator}}}"
    
    question_text = r"The probability of the first independent event is $\frac{2}{6}$ and the probability of the second independent event is $\frac{1}{5}$. Determine the fraction representing the joint probability as an irreducible term."
    
    return {
        "question_text": question_text,
        "correct_answer": f"numerator: {simplified_numerator}, denominator: {simplified_denominator}, canonical_latex: {canonical_latex}",
        "oracle_payload": {"p1": [2, 6], "p2": [1, 5]}
    }