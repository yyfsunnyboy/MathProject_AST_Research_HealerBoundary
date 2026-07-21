def generate(level=1, **kwargs):
    divisor_of = 216
    multiple_of = 18
    
    # Calculate LCM of divisor_of and multiple_of
    import math
    lcm_value = (divisor_of * multiple_of) // math.gcd(divisor_of, multiple_of)
    
    count = lcm_value

    question_text = r"""Find the smallest positive integer that is both a multiple of $18$ and divisible by $216$. Express your answer as an integer."""

    correct_answer = {"count": int(count)}
    oracle_payload = {
        "divisor_of": divisor_of, 
        "multiple_of": multiple_of
    }

    return {
        "question_text": question_text, 
        "correct_answer": correct_answer, 
        "oracle_payload": oracle_payload
    }