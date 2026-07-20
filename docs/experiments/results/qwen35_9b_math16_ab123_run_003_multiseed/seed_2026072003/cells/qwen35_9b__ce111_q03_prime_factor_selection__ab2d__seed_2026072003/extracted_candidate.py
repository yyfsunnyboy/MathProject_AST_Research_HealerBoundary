import json
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen = kwargs.get("frozen", {"candidates": [11, 12, 13, 14], "n": 156})
    
    candidates = frozen["candidates"]
    n = frozen["n"]
    
    # Task: Select a subset of candidates whose product is divisible by n? 
    # Or find the largest divisor? Given difficulty level 1 and specific numbers,
    # let's assume the task is to check divisibility or find factors.
    # However, looking at "prime_factor_selection", it likely asks for prime factorization related logic.
    # Let's construct a question: Find the product of all candidates that are divisors of n? 
    # Or maybe select primes from candidates that divide n.
    
    # Refined Task Interpretation for Level 1 Math:
    # "From the given list, identify which numbers are prime factors of n."
    # But 12 and 14 are not prime. Maybe "Select all numbers in candidates that divide n".
    # Let's try: Sum of all elements in 'candidates' that divide 'n'.
    
    valid_divisors = []
    for c in candidates:
        if IntegerOps.is_divisible(n, c):
            valid_divisors.append(c)
            
    correct_answer = sum(valid_divisors)
    
    # Construct question text with LaTeX delimiters
    candidate_str = ", ".join([f"${c}$" for c in candidates])
    q_text = f"Determine the sum of all elements from the set $\\{{{candidate_str}\\}}$ that are divisors of ${n}$."
    
    return {
        "question_text": q_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen
    }