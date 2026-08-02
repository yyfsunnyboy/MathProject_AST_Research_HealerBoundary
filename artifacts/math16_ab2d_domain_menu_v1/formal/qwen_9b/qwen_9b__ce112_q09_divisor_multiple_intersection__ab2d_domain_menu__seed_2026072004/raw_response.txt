from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {
        "divisor_of": 216,
        "multiple_of": 18
    }
    
    divisor_limit = frozen_params["divisor_of"]
    multiple_base = frozen_params["multiple_of"]
    
    # Generate all positive multiples of 'multiple_base' that are <= 'divisor_limit'
    count = 0
    
    current_multiple = multiple_base
    while current_multiple <= divisor_limit:
        if IntegerOps.is_divisible(divisor_limit, current_multiple):
            count += 1
        current_multiple += multiple_base
        
    return {
        "question_text": "有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？",
        "correct_answer": {"count": count},
        "oracle_payload": frozen_params
    }