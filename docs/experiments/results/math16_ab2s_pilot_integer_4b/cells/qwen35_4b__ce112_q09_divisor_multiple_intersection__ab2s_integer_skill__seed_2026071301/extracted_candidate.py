def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    import math
    
    lcm_val = (abs(divisor_of * multiple_of)) // math.gcd(divisor_of, multiple_of)
    count = int(lcm_val / divisor_of)
    
    question_text = r"\text{Find the number of positive integers that are multiples of } $18$ \textbf{and} divisors of } $216$.}"
    
    correct_answer = {"count": count}
    oracle_payload = {"divisor_of": divisor_of, "multiple_of": multiple_of}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }