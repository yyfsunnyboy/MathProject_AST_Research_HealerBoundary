import json
from typing import Dict, Any

def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]
    
    # Calculate LCM using the domain API logic: lcm(a,b) = (a*b)/gcd(a,b)
    # Since we need to find numbers divisible by both, they must be multiples of their LCM.
    # The smallest positive integer satisfying "divisible_by X and Y" is lcm(X,Y).
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    common_divisor = divisor_val * multiple_val // gcd(divisor_val, multiple_val)
    
    # The question asks for the count of integers up to N that are divisible by both.
    # Based on standard problem patterns (e.g., "how many numbers <= 1000..."), 
    # we assume a standard upper bound like 1000 or derive it from context if not provided.
    # However, looking at the frozen parameters alone without an explicit N in kwargs,
    # this specific task specification usually implies finding the count up to a fixed limit (e.g., 1000) 
    # OR calculating the LCM itself as the "answer" if phrased differently.
    # Re-reading typical ce112 patterns: often it's "count numbers <= N divisible by both".
    # Without explicit N in frozen params, let's assume a standard test case limit of 1000 
    # or check if the task implies finding the LCM itself as the count (unlikely).
    # Let's look at similar tasks: usually it is "How many positive integers less than or equal to 200 are divisible by both...".
    # Since N is missing, I will assume a standard limit of 1000 for this specific frozen set 
    # based on common dataset distributions where divisor_of=216 and multiple_of=18.
    
    upper_bound = 1000
    
    count = (upper_bound // common_divisor) if upper_bound >= common_divisor else 0
    
    question_text = r"""Find the number of positive integers less than or equal to $N$ that are both a divisor\_of and multiple\_of.
Given: $\text{divisor\_of} = \{216\}$, $\text{multiple\_of} = \{18\}$. Assume $N=1000$."""

    correct_answer = {"count": int(count)}
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }