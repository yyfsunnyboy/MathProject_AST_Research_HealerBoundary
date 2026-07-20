import json
from typing import Dict, Any
from core.prompts.domain_function_library import IntegerOps


def generate(level: int = 1, **kwargs) -> Dict[str, Any]:
    frozen_params = kwargs.get("frozen_sampled_parameters", {"divisor_of": 216, "multiple_of": 18})
    
    divisor_of_value = frozen_params["divisor_of"]
    multiple_of_value = frozen_params["multiple_of"]
    
    count: int
    
    # Calculate the least common multiple (LCM) of divisor and multiple.
    # LCM(a, b) = abs(a * b) // GCD(a, b). However, we can use integer operations directly if available or compute via division logic compatible with domain APIs.
    # Since IntegerOps does not explicitly provide a gcd function in the prompt list but provides safe_eval and is_divisible:
    # We need to find LCM(divisor_of_value, multiple_of_value).
    # The number of integers that are both multiples of A and B up to infinity? No, typically "intersection" implies finding numbers satisfying conditions within a range or simply the count in a specific context. 
    # Re-reading task: "divisor_multiple_intersection". Usually this means find x such that x is divisible by divisor_of AND x is multiple of multiple_of (which are tautological if they mean same thing) OR it implies finding numbers <= N?
    # Let's look at the specific frozen params: 216 and 18. 
    # "divisor_of": 216 means we are looking for divisors of 216? No, usually phrasing is "find x such that x % a == 0".
    # If it asks for intersection of {x | x divides 216} and {y | y is multiple of 18}? 
    # Or perhaps: Find count of integers n <= some_limit where n is divisible by divisor_of AND n is multiple of multiple_of? Without a limit, the set is infinite.
    # Standard interpretation for such coding tasks without explicit bounds often implies finding the LCM itself as a representative or counting divisors that are multiples? 
    # Let's reconsider "divisor_multiple_intersection". It likely asks: How many numbers divide 216 AND are multiples of 18? Or vice versa?
    # Actually, looking at similar problems (e.g., Project Euler style or math puzzles): 
    # Often it is "Count how many integers n exist such that gcd(n, A) = B" etc. 
    # But the simplest interpretation given just two numbers and a count output: 
    # Maybe it asks for the number of divisors of 216 that are also multiples of 18?
    # Let's check logic: Divisors of 216 that are divisible by 18.
    # Multiples of 18 <= 216 (since they must divide 216): 18, 36, 54, ... 
    # Check which ones divide 216:
    # 216 / 18 = 12. So any k * 18 where k*18 divides 216 implies k must be a divisor of (216/18) = 12.
    # The divisors of 12 are: 1, 2, 3, 4, 6, 12. Count is 6.
    
    # Alternative interpretation: Intersection of set of multiples of A and set of multiples of B? That's just multiples of LCM(A,B), infinite count unless bounded by max(A,B) or similar? 
    # Given the constraint "count (int)", an infinite answer makes no sense without a bound. The most logical finite bound in such problems where one is 'divisor_of' N and other is 'multiple_of' M is often divisors of N that are multiples of M, OR numbers <= max(N,M). 
    # Let's assume the question implies: "How many integers n divide 216 AND n are divisible by 18?"
    
    a = divisor_of_value
    b = multiple_of_value
    
    if not IntegerOps.is_divisible(a * b, a):
        raise ValueError("Invalid input for logic") # Sanity check
        
    # Calculate LCM to find the step size? 
    # We need x such that: (216 % x == 0) AND (x % 18 == 0).
    # From x = k * 18. Then 216 % (k*18) == 0 => 216 / (k*18) is integer => 12/k is integer => k divides 12.
    # Number of divisors of 12: 
    # Factors of 12: 1, 2, 3, 4, 6, 12 -> count = 6.
    
    target_divisor_count = a // b if a % b == 0 else -1
    
    temp_val = IntegerOps.safe_eval(str(target_divisor_count))
    num_factors: int = len([i for i in range(1, int(temp_val) + 1) if temp_val % i == 0])
    
    correct_answer_data: Dict[str, Any] = {"count": num_factors}
    
    question_text_template = """Determine the number of integers that are divisors of $216$ and also multiples of $18$."""
    
    return {
        "question_text": question_text_template.format(), # Ensure no markdown fences in text content if required, but template is plain. The prompt says use formal LaTeX delimiters where math appears. So just "$".
        "correct_answer": correct_answer_data, 
        "oracle_payload": frozen_params
    }