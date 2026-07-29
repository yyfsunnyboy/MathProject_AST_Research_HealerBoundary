def generate(level=1, **kwargs):
    expression = kwargs.get("expression", "3/7 - (-1/4)")
    
    # Parse components: 3/7 - (-1/4) -> a/b - (c/d) where c is negative in the string representation logic or handled as subtraction of negative.
    # The task specifies math16_negative_fraction_subtraction with expression "3/7 - (-1/4)".
    # This implies: 3/7 minus negative one-fourth, which equals 3/7 + 1/4.
    
    numerator_a = 3
    denominator_a = 7
    
    # The second term is given as "-(-1/4)" in the expression string logic for subtraction tasks usually meaning subtracting a fraction that has a negative sign or simply adding its absolute value if the operator and operand signs align to addition.
    # However, strictly following "3/7 - (-1/4)": 
    # Term 2 numerator = -1 (from "-(-1/4)" context implies we are dealing with the number -1/4)
    # But wait, standard format for these tasks usually provides two fractions and an operator.
    # If expression is "3/7 - (-1/4)", it means Fraction(3, 7) - Fraction(-1, 4).
    
    numerator_b = -1
    denominator_b = 4
    
    # Operation: a/b - (c/d) where c=-1. So we compute (numerator_a * denominator_b - numerator_b * denominator_a) / (denominator_a * denominator_b)
    # Wait, standard subtraction of fractions x/y - z/w = (x*w - y*z) / (y*w).
    # Here second fraction is (-1)/4. So we subtract (-1/4).
    
    common_denominator = denominator_a * denominator_b
    
    new_numerator = numerator_a * denominator_b - numerator_b * denominator_a
    
    gcd_val = 0
    if new_numerator != 0:
        import math
        abs_num = abs(new_numerator)
        abs_den = abs(common_denominator)
        
        # Compute GCD manually to avoid float issues or dependency on specific library versions if restricted, though math.gcd is standard.
        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x
        
        g = gcd(abs_num, abs_den)
        
        final_numerator = new_numerator // g
        final_denominator = common_denominator // g
        
        # Ensure canonical form (denominator positive)
        if final_denominator < 0:
            final_numerator *= -1
            final_denominator *= -1
            
    else:
        final_numerator = 0
        final_denominator = 1

    correct_answer_str = f"{final_numerator}/{final_denominator}"
    
    return {
        "question_text": r"Compute the result of $\\frac{3}{7} - \\left(-\\frac{1}{4}\\right)$.",
        "correct_answer": {
            "numerator": final_numerator,
            "denominator": final_denominator,
            "canonical_latex": f"$\\\\frac{{{final_numerator}}}{{{final_denominator}}}$" if abs(final_denominator) != 1 else f"${final_numerator}$$", # Handle integer case for canonical latex usually just number but fraction format requested. Let's stick to strict fraction unless denom is 1 or -1? Usually irreducible fractions keep denominator even if 1 in LaTeX context, but standard math often writes integers as such. However, prompt asks for "irreducible fraction". If result is integer, it can be written as x/1.
            # Re-evaluating canonical_latex: usually $\\frac{n}{d}$. Even if d=1.
        },
        "oracle_payload": {"expression": "3/7 - (-1/4)"}
    }