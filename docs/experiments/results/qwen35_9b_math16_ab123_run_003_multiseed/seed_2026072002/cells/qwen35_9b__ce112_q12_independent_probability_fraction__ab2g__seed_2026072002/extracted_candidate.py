def generate(level=1, **kwargs):
    frozen_params = {"p1": [2, 6], "p2": [1, 5]}
    
    # Simplify fractions from frozen params before calculation to ensure irreducible logic in answer if needed, 
    # but oracle_payload must be EXACTLY the frozen sampled parameters.
    p1_num, p1_den = frozen_params["p1"]
    p2_num, p2_den = frozen_params["p2"]
    
    # Calculate probability: P(A and B) for independent events = P(A)*P(B)
    numerator = p1_num * p2_num
    denominator = p1_den * p2_den
    
    # Function to compute GCD manually since math.gcd is standard but we want pure logic verification if needed. 
    # Standard library gcd is allowed in Python source unless restricted, assuming standard env.
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    common_divisor = gcd(numerator, denominator)
    
    final_numerator = numerator // common_divisor
    final_denominator = denominator // common_divisor
    
    # Construct LaTeX for the fraction. Use \frac{}{}. 
    latex_fraction = f"\\frac{{{final_numerator}}}{{{final_denominator}}}"
    canonical_latex = f"{latex_fraction} \\text{ (irreducible)}"

    question_text = r"The probability of event $A$ occurring is $\frac{%d}{%d}$ and the probability of independent event $B$ occurring is $\frac{%d}{%d}$. What is the probability that both events $A$ and $B$ occur? Express your answer as an irreducible fraction in LaTeX format." % (p1_num, p1_den, p2_num, p2_den)
    
    # Wait, the prompt says question_text must use formal LaTeX delimiters. 
    # Let's refine the string to be safe with formatting.
    q_str = f"The probability of event $A$ occurring is $\frac{{{p1_num}}}{{{p1_den}}}$ and the probability of independent event $B$ occurring is $\frac{{{p2_num}}}{{{p2_den}}}$.\n\nWhat is the probability that both events $A$ and $B$ occur? Express your answer as an irreducible fraction."
    
    correct_answer = {
        "numerator": final_numerator,
        "denominator": final_denominator,
        "canonical_latex": f"\\frac{{{final_numerator}}}{{{final_denominator}}}"
    }

    oracle_payload = frozen_params
    
    return {
        "question_text": q_str,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }