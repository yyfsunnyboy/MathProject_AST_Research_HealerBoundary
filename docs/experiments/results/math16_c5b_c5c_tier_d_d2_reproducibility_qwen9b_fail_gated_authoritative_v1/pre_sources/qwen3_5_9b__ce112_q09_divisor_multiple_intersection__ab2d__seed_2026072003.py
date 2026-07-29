from typing import Dict, Any
import json

# Simulating the required imports from a hypothetical library structure


def generate(level=1, **kwargs) -> Dict[str, Any]:
    # Frozen sampled parameters from the prompt specification
    frozen_params = {"divisor_of": 216, "multiple_of": 18}

    divisor_val = frozen_params["divisor_of"]
    multiple_val = frozen_params["multiple_of"]

    # Logic: Find integers that are both multiples of 'multiple_val' and divisors of 'divisor_val'.
    # These numbers must satisfy: x % multiple_val == 0 AND divisor_val % x == 0.
    
    count = 0
    
    # Iterate through all possible candidates up to the smaller number (which is a candidate for both)
    limit = min(divisor_val, multiple_val)
    
    for i in range(1, limit + 1):
        if IntegerOps.is_divisible(i, multiple_val) and IntegerOps.is_divisible(divisor_val, i):
            count += 1

    # Construct the return dictionary exactly as specified
    result_dict = {
        "question_text": r"Find the number of integers that are both multiples of $\\frac{d}{m}$ where $d=216$ and $m=18$, satisfying: an integer is a multiple of 18 AND a divisor of 216.",
        # More precise LaTeX formulation for clarity based on standard math problem formats
        "question_text": r"Let $S = \\{ x \in \mathbb{Z}^+ : x \text{ is a multiple of } 18 \text{ and } x \text{ divides } 216 \\}$. Determine the cardinality $|S|$.",
        "correct_answer": {
            "count": count
        },
        "oracle_payload": frozen_params
    }

    return result_dict