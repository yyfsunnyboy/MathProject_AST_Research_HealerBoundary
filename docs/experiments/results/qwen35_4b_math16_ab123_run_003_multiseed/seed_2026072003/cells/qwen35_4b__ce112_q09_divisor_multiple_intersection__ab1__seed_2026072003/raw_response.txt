def generate(level=1, **kwargs):
    import json
    
    divisor_of = 216
    multiple_of = 18
    
    # Calculate the least common multiple (LCM) to find a valid number that is both a multiple of 'multiple_of' and divisible by 'divisor_of'.
    # A number X satisfies:
    # 1. X % divisor_of == 0
    # 2. X % multiple_of == 0
    
    # The smallest positive integer satisfying these conditions is the LCM(divisor_of, multiple_of).
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    lcm_val = (divisor_of * multiple_of) // gcd(divisor_of, multiple_of)
    
    # To ensure we have enough numbers for the question context without making it trivially infinite, 
    # let's count how many such positive integers exist below 1000. If there are none or too few, adjust slightly to ensure a valid range exists.
    limit = 2500
    count = sum(1 for x in range(lcm_val, limit + 1) if (x % divisor_of == 0 and x % multiple_of == 0))
    
    # Construct the question text using LaTeX delimiters
    question_text = r"""Find the number of positive integers less than $2500$ that are both a multiple of $\text{multiple\_of}$ ($18$) and divisible by $\text{divisor\_of}$ ($216$). Express your answer as an integer."""

    # Construct the correct answer
    correct_answer = {"count": count}
    
    return {
        "question_text": question_text,
        "correct_answer": json.dumps(correct_answer),
        "oracle_payload": dict(divisor_of=divisor_of, multiple_of=multiple_of)
    }