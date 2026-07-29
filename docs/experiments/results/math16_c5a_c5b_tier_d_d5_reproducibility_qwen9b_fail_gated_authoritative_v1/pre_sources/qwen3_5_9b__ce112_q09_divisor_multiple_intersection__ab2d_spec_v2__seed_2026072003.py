# -*- coding: utf-8 -*-

def generate(level=1, **kwargs):
    # Frozen sampled parameters defined directly as per contract
    divisor_of = 216
    multiple_of = 18
    
    # Compute the exact result using native Python.
    count = 0
    for x in range(1, divisor_of + 1):
        if (x % multiple_of == 0) and (divisor_of % x == 0):
            count += 1
            
    correct_answer = {"count": count}
    
    question_text = r"Count positive integers $x$ satisfying both: $x \equiv 0 \pmod{\text{multiple\_of}}$ and $\text{divisor\_of} \equiv 0 \pmod{x}$."
    
    oracle_payload = {
        "divisor_of": divisor_of, 
        "multiple_of": multiple_of
    }

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload,
    }