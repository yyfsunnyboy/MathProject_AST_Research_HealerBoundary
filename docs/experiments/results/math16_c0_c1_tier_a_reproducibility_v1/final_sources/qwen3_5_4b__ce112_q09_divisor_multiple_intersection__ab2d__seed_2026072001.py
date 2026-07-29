import json
from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    # Calculate LCM using the formula: lcm(a,b) = (a*b)/gcd(a,b)
    # Since we need numbers that are multiples of 'multiple_val' and divisors of 'divisor_val',
    # the intersection set is {x | x % multiple_val == 0 AND divisor_of(x, divisor_val)}.
    # The problem asks for integers satisfying both conditions.
    # Let's find the count of such positive integers within a reasonable range or all if finite?
    # Usually "intersection" in these contexts implies finding numbers that are multiples of A and divisors of B.
    # If we consider positive integers: x must be a multiple of 18 AND a divisor of 216.
    # The maximum such number is min(ceil(multiple_val), floor(divisor_val)) if they overlap, 
    # but specifically here the set is finite because divisors are bounded by 216 and multiples grow indefinitely?
    # Wait: "divisor_of" means x divides divisor_val. So x <= divisor_val (for positive integers).
    # "multiple_of" means multiple_val divides x. So x >= multiple_val (for positive integers) if we assume standard counting from 1.
    # Actually, the set of divisors of 216 is finite. The subset that are also multiples of 18 is what we count.
    
    import math
    
    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    # Calculate LCM to find the largest multiple of 'multiple_val' that could possibly divide 216? 
    # Actually simpler logic: Find all divisors of 216. Check which ones are multiples of 18. Count them.
    
    count = 0
    
    for i in range(1, divisor_val + 1):
        if IntegerOps.is_divisible(divisor_val, i):
            # If it is a divisor of 216, check if it is a multiple of 18
            try:
                remainder = safe_eval(f"{i} % {multiple_val}")
                if remainder == 0:
                    count += 1
            except ValueError:
                continue
    
    correct_answer_dict = {"count": int(count)}

    return {
        "question_text": r"Find the number of positive integers that are both multiples of $18$ and divisors of $216$. Express your answer as an integer.",
        "correct_answer": correct_answer_dict,
        "oracle_payload": frozen_params
    }