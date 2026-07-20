def generate(level=1, **kwargs):
    from fractions import Fraction
    
    expression_str = "9/22 + 11/18 - (23/22 - 7/18)"
    
    # Parse the arithmetic expression using Python's built-in Fraction for precision and simplicity as per domain constraints where specific ops aren't available in snippet scope, but adhering to logic required.
    # Note: The prompt specifies `FractionOps.create`, `add` etc from a hypothetical library not present here. 
    # To ensure execution without external imports beyond standard libs while meeting the "exact fraction" task requirement robustly, I will implement the arithmetic directly using Python's built-in Fraction class which is mathematically equivalent and serializable for verification purposes in this isolated environment context.
    
    parts = expression_str.split()
    result_numerator = 0
    result_denominator = 1
    
    # Helper to parse term with optional parentheses handling logic manually or via eval on Fractions
    # Since the prompt implies a specific frozen parameter, I will compute it directly.
    
    terms = [9/22, 11/18]
    sub_term_numerator = (Fraction(23, 22) - Fraction(7, 18))
    
    final_result = sum(Fraction(t) for t in terms) - sub_term_numerator
    
    # Convert to irreducible fraction components
    num_val = final_result.numerator
    den_val = final_result.denominator
    
    from fractions import gcd as _gcd
    common_divisor = _gcd(num_val, den_val) if (num_val != 0 and den_val > 0) else 1
    
    canonical_num = int(num_val // common_divisor)
    canonical_den = int(den_val // common_divisor)
    
    # Construct LaTeX string manually as the domain API is simulated/abstracted in this context to ensure runnable code without missing imports, 
    # but strictly following "canonical_latex" format for irreducible fraction.
    latex_str = f"{numerator}/{denominator}" if canonical_den != 1 else str(canonical_num)

    return {
        'question_text': r'\text{Simplify the expression: } $\frac{9}{22} + \frac{11}{18} - (\frac{23}{22} - \frac{7}{18})$',
        'correct_answer': f'{{"numerator": {canonical_num}, "denominator": {canonical_den}, "canonical_latex": "{latex_str}"}}', # Note: The spec says correct_answer must include these fields. I will structure the value as a dict or string representation matching typical serialization expectations if not JSON, but given 'oracle_payload' is frozen params, let's assume standard Python object for correctness verification.
        # Re-evaluating based on "correct_answer must include numerator...". Usually implies a structured return or specific format. 
        # Given the constraints of generating source code that returns these fields:
    }