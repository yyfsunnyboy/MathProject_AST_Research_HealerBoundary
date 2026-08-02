from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    # Step 1: Get all positive divisors of the divisor_of number (216)
    candidates = IntegerOps.positive_divisors(frozen_params["divisor_of"])
    
    # Step 2: Filter to keep only those divisible by multiple_of (18)
    valid_numbers = [n for n in candidates if IntegerOps.is_divisible(n, frozen_params["multiple_of"])]
    
    # Calculate the count
    count = len(valid_numbers)
    
    return {
        "question_text": "有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？",
        "correct_answer": {"count": count},
        "oracle_payload": frozen_params
    }