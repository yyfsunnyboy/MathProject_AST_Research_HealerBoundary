# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Define all frozen parameters directly as per task specification
    divisor_of = 216
    multiple_of = 18
    
    # Compute the count of positive integers x satisfying both conditions:
    # 1. x is a multiple of 'multiple_of' (x % multiple_of == 0)
    # 2. x divides 'divisor_of' (divisor_of % x == 0)
    
    # Condition 1 implies x must be in the set {k * multiple_of for k >= 1}
    # Condition 2 implies x must be a divisor of 'divisor_of'
    # Therefore, x must be a common element of these two sets.
    # Since x divides divisor_of, we only need to check divisors of divisor_of.
    
    count = 0
    
    # Iterate through all positive integers up to divisor_of (inclusive)
    for x in range(1, divisor_of + 1):
        if (x % multiple_of == 0) and (divisor_of % x == 0):
            count += 1
            
    correct_answer = {"count": count}
    
    question_text = r"Count the number of positive integers $x$ such that $x$ is a multiple of $\text{multiple\_of}$ AND $x$ divides $\text{divisor\_of}$."
    
    oracle_payload = {
        "divisor_of": divisor_of,
        "multiple_of": multiple_of
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }