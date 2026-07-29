def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per specification
    divisor_of = 216
    multiple_of = 18
    
    # We need to count positive integers x such that:
    # 1. x is a multiple of multiple_of (x % multiple_of == 0) => x = k * multiple_of for some integer k >= 1
    # 2. divisor_of is divisible by x (divisor_of % x == 0) => x must be a divisor of divisor_of
    
    # Combining these conditions:
    # Since x divides divisor_of, the maximum possible value for x is divisor_of itself.
    # Also, since x = k * multiple_of, we have k * multiple_of <= divisor_of, so k <= floor(divisor_of / multiple_of).
    
    # Therefore, valid values of x are multiples of 'multiple_of' that also divide 'divisor_of'.
    # This is equivalent to finding the number of divisors of (divisor_of) that are multiples of (multiple_of).
    # Alternatively: Let L = lcm(divisor_of, multiple_of). No, simpler logic below.
    
    # Logic refinement:
    # x must be a divisor of 216 AND x must be a multiple of 18.
    # So we iterate through all divisors of 216 and check if they are multiples of 18.
    # Or, since max(x) is 216 (because x divides 216), we can just count k such that:
    #   x = k * 18
    #   divisor_of % x == 0 => 216 % (k * 18) == 0
    
    # Let's find all divisors of 216 first, then filter.
    
    count = 0
    
    # Iterate through possible values of x from 1 to 216
    for x in range(1, divisor_of + 1):
        if (divisor_of % x == 0) and (x % multiple_of == 0):
            count += 1
            
    correct_answer = {"count": count}
    
    question_text = r"Count the number of positive integers $x$ such that $x$ is a multiple of $\{multiple\_of}$ AND $\{divisor\_of}$ is divisible by $x$. Express your answer as an integer."

    oracle_payload = {
        "divisor_of": divisor_of, 
        "multiple_of": multiple_of
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }
