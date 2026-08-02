from core.prompts.domain_function_library import IntegerOps


def generate(level=1, **kwargs):
    divisor_of = kwargs.get("divisor_of", 216)
    multiple_of = kwargs.get("multiple_of", 18)
    
    # Step 1: Get all positive divisors of the number that is a "divisor_of" (i.e., n such that d|n)
    # The API returns divisors of n. Here, we need numbers x where divisor_of % x == 0? 
    # Wait, re-reading the task description and frozen_params:
    # Task: How many positive integers are multiples of A AND factors (divisors) of B?
    # Frozen params: "multiple_of": 18, "divisor_of": 216.
    # So we need x such that: 
    #   1) x is a multiple of 18 => x % 18 == 0
    #   2) x is a divisor (factor) of 216 => 216 % x == 0
    
    # The API IntegerOps.positive_divisors(n) returns divisors OF n.
    # So we get all positive integers that divide 216. Let's call this set D.
    
    candidates = IntegerOps.positive_divisors(divisor_of)
    
    # Step 2: Filter to keep only those divisible by multiple_of (i.e., x % multiple_of == 0)
    filtered_candidates = [x for x in candidates if x % multiple_of == 0]
    
    # The count is the length of this list. 
    correct_answer_count = len(filtered_candidates)
    
    return {
        "question_text": f"有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？",
        "correct_answer": {"count": correct_answer_count},
        "oracle_payload": kwargs,
    }
