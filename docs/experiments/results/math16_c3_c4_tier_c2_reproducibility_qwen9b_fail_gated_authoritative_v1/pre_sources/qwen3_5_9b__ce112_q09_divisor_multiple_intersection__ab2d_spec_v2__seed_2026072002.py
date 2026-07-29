# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Define all frozen parameters directly as per task specification
    divisor_of = 216
    multiple_of = 18
    
    # Compute the exact result using native Python.
    # We need to count positive integers x such that:
    # 1. x is a multiple of 'multiple_of' (x % multiple_of == 0) => x >= multiple_of, step = multiple_of
    # 2. divisor_of is divisible by x (divisor_of % x == 0) => x must be a divisor of 'divisor_of'
    
    count = 0
    
    # Iterate through all divisors of divisor_of to check condition 1
    for candidate in range(1, divisor_of + 1):
        if divisor_of % candidate == 0:
            # Check if this divisor is also a multiple of 'multiple_of'
            if candidate % multiple_of == 0:
                count += 1
                
    correct_answer = {"count": count}
    
    question_text = r"Count the number of positive integers $x$ satisfying both conditions:\n\n- $x \equiv 0 \pmod{\\text{{multiple\_of}}}$\n- $\\text{{divisor\_of}} \\equiv 0 \\pmod{x}$\n\nwhere $\text{{divisor\_of}} = {}$ and $\text{{multiple\_of}} = {}$."
    
    oracle_payload = {"divisor_of": divisor_of, "multiple_of": multiple_of}

    return {
        "question_text": question_text.format(divisor_of=divisor_of, multiple_of=multiple_of),
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }