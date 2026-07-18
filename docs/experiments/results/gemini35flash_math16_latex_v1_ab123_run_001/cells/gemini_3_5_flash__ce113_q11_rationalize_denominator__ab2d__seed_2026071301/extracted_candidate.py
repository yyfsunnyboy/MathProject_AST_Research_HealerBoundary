from core.prompts.domain_function_library import FractionOps

def generate(level=1, **kwargs):
    # Frozen parameters
    numerator = 9
    radicand = 7
    denominator = "4-sqrt(7)"
    
    # Parse denominator
    if '-' in denominator:
        d_val = int(denominator.split('-')[0])
        sign = -1
    elif '+' in denominator:
        d_val = int(denominator.split('+')[0])
        sign = 1
    else:
        raise ValueError("Invalid denominator format")
        
    # Calculate rationalized denominator: d_val^2 - radicand
    denom_rationalized = d_val * d_val - radicand
    
    # a = (numerator * d_val) / denom_rationalized
    # b = (-sign * numerator) / denom_rationalized
    a_val = FractionOps.create((numerator * d_val) / denom_rationalized)
    b_val = FractionOps.create((-sign * numerator) / denom_rationalized)
    
    ans = FractionOps.add(a_val, b_val)
    correct_answer = int(ans)
    
    # Format denominator for LaTeX
    denominator_latex = denominator.replace(f"sqrt({radicand})", f"\\sqrt{{{radicand}}}")
    
    question_text = (
        f"Rationalize the denominator of $\\frac{{{numerator}}}{{{denominator_latex}}}$. "
        f"If the result is expressed in the form $a + b\\sqrt{{{radicand}}}$, "
        f"find the value of $a + b$."
    )
    
    oracle_payload = {
        "denominator": denominator,
        "numerator": numerator,
        "radicand": radicand
    }
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }