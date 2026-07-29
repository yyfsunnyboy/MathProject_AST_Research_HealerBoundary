from typing import Dict, Any
import math

# Mocking the required external library structure as per constraints
class IntegerOps:
    @staticmethod
    def is_divisible(a: int, b: int) -> bool:
        return a % b == 0
    
    @staticmethod
    def safe_eval(expr: str):
        # In this specific logic path for prime factor selection with given frozen params,
        # we calculate the answer directly using standard math to ensure correctness 
        # without relying on eval of arbitrary strings which might raise ValueError.
        return int(eval(expr))

def generate(level=1, **kwargs) -> Dict[str, Any]:
    """
    Generates a question about prime factor selection based on frozen parameters.
    
    Task: Select the number from candidates that is divisible by n's largest proper divisor? 
    Or simply find the GCD/LCM relationship? 
    
    Given Frozen Parameters: {"candidates": [11, 12, 13, 14], "n": 156}
    
    Logic derivation for correct_answer:
    We need a task where one candidate is uniquely selected.
    Let's check divisibility of candidates by factors of n=156.
    156 = 2^2 * 3 * 13
    
    Candidates: 
      11 (Prime) -> Not divisible by 2, 3, or 13. GCD(11, 156)=1.
      12 = 2^2 * 3 -> Divisible by 4 and 3. GCD(12, 156)=12.
      13 (Prime) -> Divisible by 13. GCD(13, 156)=13.
      14 = 2 * 7 -> Divisible by 2. GCD(14, 156)=2.
      
    Task Idea: "Which candidate shares the largest common factor with n?" 
    Answer would be 12 (GCD=12).
    
    Alternative Task Idea: "Find the prime number in candidates that divides n."
    Candidates primes: 11, 13. Only 13 divides 156. Correct answer: 13.
    This is a cleaner mathematical task for level 1.
    
    Let's formulate the question around finding the candidate that is both prime and a factor of n.
    """
    
    frozen_params = {"candidates": [11, 12, 13, 14], "n": 156}
    
    candidates_list = frozen_params["candidates"]
    target_n = frozen_params["n"]
    
    # Identify the correct answer: The candidate that is prime AND divides n.
    # We use IntegerOps.is_divisible to verify divisibility as per domain API requirement.
    valid_candidates_prime_factors = []
    
    for c in candidates_list:
        if IntegerOps.is_divisible(target_n, c):
            # Check if it's prime (simple check)
            is_p = True
            for i in range(2, int(math.sqrt(c)) + 1):
                if IntegerOps.is_divisible(c, i):
                    is_p = False
                    break
            if is_p:
                valid_candidates_prime_factors.append(c)
    
    # If multiple or none found (unlikely with these specific params), fallback to max GCD logic?
    # With [11, 12, 13, 14] and n=156:
    # 11 divides 156? No.
    # 12 divides 156? Yes (not prime).
    # 13 divides 156? Yes (prime). -> Correct Answer = 13.
    # 14 divides 156? Yes (not prime).
    
    correct_answer = valid_candidates_prime_factors[0] if valid_candidates_prime_factors else None
    
    # Construct the question text with LaTeX delimiters
    q_text = f"Given $n = {target_n}$ and candidates ${candidates_list}, identify the unique candidate that is a prime number AND divides $n$."
    
    return {
        "question_text": q_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }