import json
from typing import Dict

def generate(level=1, **kwargs):
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    divisor_of_val = frozen_params["divisor_of"]
    multiple_of_val = frozen_params["multiple_of"]
    
    # Find the least common multiple (LCM) of the two numbers.
    # LCM(a, b) = abs(a * b) / GCD(a, b).
    # Since we are looking for intersection of multiples and divisors in a generalized sense 
    # based on typical number theory problems where "divisor_of X" implies finding factors or related structures,
    # but given the phrasing "multiple_of A AND divisor_of B", it usually asks for numbers N such that:
    # 1. N is divisible by multiple_of_val (N % m == 0) -> Wait, standard interpretation of "multiple of X" means N = k*X.
    # 2. The problem likely implies finding the smallest positive integer that satisfies both conditions simultaneously 
    # or a specific count based on context usually found in such datasets.
    # Re-reading task: "divisor_of": 216, "multiple_of": 18.
    # Interpretation A: Find N where N is a multiple of 18 AND N divides 216? 
    #   - Multiples of 18 that divide 216.
    #   - 18 * k must be <= 216 and (216 % (18*k)) == 0.
    # Interpretation B: Find N where N is a multiple of divisor_of AND N divides multiple_of? Unlikely order.
    # Standard interpretation for "intersection" in such math problems usually refers to the set of numbers satisfying both properties.
    # Let's assume the question asks for the count of positive integers that are multiples of 18 and divisors of 216.
    
    m = multiple_of_val # 18
    d_max = divisor_of_val # 216
    
    count = 0
    n = 1
    while True:
        candidate = m * n
        
        if candidate > d_max:
            break
            
        # Check if candidate is a divisor of d_max (i.e., d_max % candidate == 0)
        if d_max % candidate == 0:
            count += 1
        
        n += 1
    
    correct_answer = {"count": count}
    
    question_text = r"""Find the number of positive integers that are multiples of $18$ and divisors of $216$. Use formal LaTeX delimiters for mathematical expressions."""

    oracle_payload = frozen_params
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }