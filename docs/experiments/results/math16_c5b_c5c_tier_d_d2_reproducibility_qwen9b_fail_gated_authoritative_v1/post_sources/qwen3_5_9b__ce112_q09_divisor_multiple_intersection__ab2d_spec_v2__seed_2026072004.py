# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Define all frozen parameters directly as per task specification
    divisor_of = 216
    multiple_of = 18
    
    # Compute the exact result using native Python.
    # We need to count positive integers x such that:
    # 1. x is a multiple of 'multiple_of' (x % multiple_of == 0)
    # 2. x divides 'divisor_of' (divisor_of % x == 0)
    
    # Condition 2 implies x must be a divisor of divisor_of.
    # Therefore, we only need to check the divisors of divisor_of.
    # Among those divisors, count how many are also multiples of multiple_of.
    
    count = 0
    
    # Iterate through all positive integers up to divisor_of to find its divisors
    for x in range(1, divisor_of + 1):
        if (divisor_of % x == 0) and (x % multiple_of == 0):
            count += 1
            
    correct_answer = {"count": count}
    
    question_text = r"Count the number of positive integers $x$ satisfying both: $x \equiv 0 \pmod{multiple\_of}$ and $divisor\_of \equiv 0 \pmod{x}$."
    
    oracle_payload = {
        "divisor_of": divisor_of, 
        "multiple_of": multiple_of
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }