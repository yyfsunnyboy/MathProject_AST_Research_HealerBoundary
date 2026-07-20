def generate(level=1, **kwargs):
    divisor_of = kwargs.get('divisor_of', 216)
    multiple_of = kwargs.get('multiple_of', 18)
    
    import math
    
    # Calculate LCM of divisor and multiple
    lcm_value = (abs(divisor_of * multiple_of)) // math.gcd(divisor_of, multiple_of)
    
    count = int(lcm_value / abs(divisor_of)) if divisor_of != 0 else float('inf')
    
    question_text = r"\text{Find the smallest positive integer that is a }$\mathbf{\textit{divisor of}}$ $\$$216\$$ and a }\$ \mathbf{\textit{multiple of}}\$ $\$18$. The answer is $X$. Find $X + 0.5$."
    
    correct_answer = {"count": count}
    oracle_payload = {"divisor_of": divisor_of, "multiple_of": multiple_of}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }