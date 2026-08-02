from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"divisor_of": 216, "multiple_of": 18}
    
    # Calculate the number of multiples of 'm' that are also divisors of 'n'.
    # These numbers must be in the range [0, n]. Since we want positive integers, range is (0, n].
    # The k-th multiple of m is k*m. We need k*m <= n => k <= floor(n/m).
    
    divisor_of = frozen_params["divisor_of"]  # 216
    multiple_of = frozen_params["multiple_of"]  # 18
    
    if multiple_of == 0:
        count = 0
    else:
        max_k = IntegerOps.sub(divisor_of, 0) // IntegerOps.add(multiple_of, 0)
        
        # We need to ensure the division is integer floor. 
        # Python's / returns float for non-integers in some contexts but here inputs are ints.
        # However, safe_eval or direct arithmetic works best with integers.
        # Let's use IntegerOps.safe_eval for clarity on logic if needed, but simple // is fine.
        # To strictly follow allowed ops and avoid potential type issues:
        
        quotient = divisor_of // multiple_of
        
        count = quotient
    
    return {
        "question_text": "有多少個正整數同時是 \(18\) 的倍數，也是 \(216\) 的因數？",
        "correct_answer": {"count": count},
        "oracle_payload": frozen_params,
    }