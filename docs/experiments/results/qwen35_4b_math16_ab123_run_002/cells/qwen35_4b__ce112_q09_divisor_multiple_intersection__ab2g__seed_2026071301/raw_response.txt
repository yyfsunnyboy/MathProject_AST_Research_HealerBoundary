def generate(level=1, **kwargs):
    divisor_of = kwargs.get('divisor_of', 216)
    multiple_of = kwargs.get('multiple_of', 18)
    
    # Calculate LCM of divisor and multiple to find the intersection step size
    import math
    lcm_value = (divisor_of * multiple_of) // math.gcd(divisor_of, multiple_of)
    
    count = int(lcm_value / divisor_of) if divisor_of != 0 else 1
    
    question_text = r"""Find the number of positive integers that are both multiples of $x$ and divisors of $y$, where $x = \text{multiple\_of}$ and $y = \text{divisor\_of}$. Express your answer as an integer."""
    
    correct_answer = {"count": count}
    oracle_payload = {
        "divisor_of": divisor_of, 
        "multiple_of": multiple_of
    }
    
    return {
        "question_text": question_text, 
        "correct_answer": correct_answer, 
        "oracle_payload": oracle_payload
    }