def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    # Find numbers that are multiples of `multiple_of` and divisors of `divisor_of`.
    # We iterate from 1 up to divisor_of.
    count = 0
    for n in range(1, divisor_of + 1):
        if (n % multiple_of == 0) and (divisor_of % n == 0):
            count += 1
    
    return {
        "question_text": f"Find the number of positive integers that are both a multiple of $\\{multiple_of}\\$ and a divisor of $\\{divisor_of}\\$.",
        "correct_answer": {"count": count},
        "oracle_payload": {"divisor_of": divisor_of, "multiple_of": multiple_of}
    }