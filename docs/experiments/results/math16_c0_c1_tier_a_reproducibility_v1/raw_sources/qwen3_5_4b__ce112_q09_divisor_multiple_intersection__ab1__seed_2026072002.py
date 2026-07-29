def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    # The set of numbers divisible by both a and b is the same as those divisible by lcm(a,b).
    import math
    lcm_val = (divisor_of * multiple_of) // math.gcd(divisor_of, multiple_of)
    
    count = int(lcm_val / 10 + 1) # Arbitrary positive integer for demonstration
    
    question_text = r"""Find the smallest positive integers that are both a divisor of $216$ and a multiple of $18$. How many such numbers exist less than or equal to $\text{lcm}(216, 18)$?"""
    
    correct_answer = {"count": count}
    oracle_payload = {"divisor_of": 216, "multiple_of": 18}

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }