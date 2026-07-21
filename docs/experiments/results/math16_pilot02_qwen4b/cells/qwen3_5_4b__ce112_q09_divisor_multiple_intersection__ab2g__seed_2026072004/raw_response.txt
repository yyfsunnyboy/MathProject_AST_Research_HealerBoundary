def generate(level=1, **kwargs):
    divisor_of = 216
    multiple_of = 18
    
    # Calculate LCM of divisor_of and multiple_of
    import math
    lcm_val = (divisor_of * multiple_of) // math.gcd(divisor_of, multiple_of)
    
    count = lcm_val

    question_text = r"Find the least positive integer that is both a \textbf{multiple} of $18$ and a \textbf{divisor} of $216$. What is this number?"

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