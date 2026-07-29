def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    # Find numbers up to a reasonable limit (e.g., LCM of the two or slightly more) that are both divisors and multiples.
    # A number x is a divisor of D if D % x == 0.
    # A number y is a multiple of M if y % M == 0.
    # We need numbers z such that (z divides divisor_of) AND (multiple_of divides z).
    
    limit = max(divisor_of, multiple_of) * 2
    
    valid_numbers = []
    for i in range(1, limit + 1):
        if (divisor_of % i == 0) and (i % multiple_of == 0):
            valid_numbers.append(i)
    
    count = len(valid_numbers)
    
    question_text = f"Find the number of integers that are both a divisor of {divisor_of} and a multiple of {multiple_of}."
    correct_answer = {"count": count}
    oracle_payload = kwargs
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }