def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    import math
    
    lcm_val = (divisor_of * multiple_of) // math.gcd(divisor_of, multiple_of)
    count = int(lcm_val / divisor_of) if divisor_of != 0 else float('inf')
    
    question_text = r"""Find the number of positive integers that are both divisors of $216$ and multiples of $18$. Express your answer as an integer."""
    
    correct_answer = {"count": count}
    oracle_payload = {"divisor_of": divisor_of, "multiple_of": multiple_of}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }