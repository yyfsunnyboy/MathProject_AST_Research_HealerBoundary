def generate(level=1, **kwargs):
    expression = "3/7 - (-1/4)"
    
    # Perform rational arithmetic: 3/7 + 1/4
    # Common denominator is 28
    num1, den1 = 3, 7
    num2, den2 = 1, 4
    
    common_denominator = den1 * den2
    adjusted_num1 = num1 * den2
    adjusted_num2 = num2 * den1
    
    total_numerator = adjusted_num1 + adjusted_num2
    
    # Reduce fraction by GCD
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)
    
    common_divisor = gcd(total_numerator, common_denominator)
    reduced_numerator = total_numerator // common_divisor
    reduced_denominator = common_denominator // common_divisor
    
    # Format for canonical_latex (irreducible fraction with positive denominator)
    if reduced_denominator < 0:
        reduced_numerator *= -1
        reduced_denominator *= -1
        
    numerator_str = str(reduced_numerator)
    denominator_str = str(reduced_denominator)
    
    # Construct LaTeX strings using formal delimiters $...$ for fraction and \frac{num}{den} structure if needed, but standard mathjax uses $\frac{a}{b}$ or just a/b in text. The requirement asks for canonical_latex for an irreducible fraction. We will use the standard representation inside dollar signs.
    # Using $\dfrac{n}{d}$ for display style is common, but $n/d$ is also valid LaTeX. Let's stick to simple fraction notation within delimiters as requested: \(\frac{numerator}{denominator}\) or similar formal latex. 
    # The prompt asks for "canonical_latex". A standard irreducible fraction in mathjax/latex is often written with a slash or the frac command. Given the context of subtraction problems, $\dfrac{n}{d}$ is clear.
    
    canonical_latex = f"${\\dfrac{{numerator_str}}{{denominator_str}}}$"

    return {
        "question_text": r"$3/7 - (-1/4)$",
        "correct_answer": {
            "numerator": reduced_numerator,
            "denominator": reduced_denominator,
            "canonical_latex": canonical_latex
        },
        "oracle_payload": expression
    }