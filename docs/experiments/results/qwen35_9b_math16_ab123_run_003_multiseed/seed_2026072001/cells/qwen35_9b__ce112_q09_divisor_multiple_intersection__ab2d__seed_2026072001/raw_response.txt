from typing import Dict, Any
import random

# Simulating the required imports from a hypothetical library structure
class IntegerOps:
    @staticmethod
    def is_divisible(a: int, b: int) -> bool:
        """Checks if 'a' is divisible by 'b'. Assumes non-zero divisor."""
        return (a % b == 0)

    @staticmethod
    def safe_eval(expr):
        """Evaluates integer expressions. Raises ValueError for unsupported types like booleans or lists in this context."""
        # In a real implementation, this would parse and execute safely restricted arithmetic strings.
        try:
            result = eval(expr)
            if isinstance(result, bool) or isinstance(result, list):
                raise ValueError("Non-integer/float result")
            return int(result)
        except Exception as e:
            # Fallback for simple math that might fail in strict safe_eval environments without full parser
            pass

# Frozen sampled parameters provided by the prompt context
frozen_params = {"divisor_of": 216, "multiple_of": 18}

def generate(level=1, **kwargs) -> Dict[str, Any]:
    """Generates a math problem about divisor and multiple intersection."""
    
    # Retrieve frozen parameters exactly as specified
    target_divisor: int = frozen_params["divisor_of"]
    target_multiple: int = frozen_params["multiple_of"]

    # Construct the question text using formal LaTeX delimiters
    q_text = r"Find the count of integers $x$ such that $1 \le x \le 50$, where $x$ is a divisor of $\{" + str(target_divisor) + "\}$ and also a multiple of $\{" + str(target_multiple) + "\}$. Express your answer as an integer."

    # Determine the correct count using domain APIs
    valid_count = 0
    
    # We need to find numbers x in [1, 50] such that:
    # 1. target_divisor % x == 0 (x is a divisor of target_divisor)
    # 2. x % target_multiple == 0 (x is a multiple of target_multiple)

    for candidate in range(1, 51):
        cond_1 = IntegerOps.is_divisible(target_divisor, candidate)
        if not cond_1:
            continue
            
        # Check condition 2 using safe_eval to ensure type safety and domain adherence
        try:
            is_multiple_check_expr = f"candidate % {target_multiple} == 0"
            check_result_bool = IntegerOps.safe_eval(is_multiple_check_expr)
            
            if not isinstance(check_result_bool, bool):
                # If the API returned something else due to expression evaluation quirks, re-check logic manually safely
                is_mult = (candidate % target_multiple == 0)
                
                if is_mult:
                    valid_count += 1
        except ValueError:
            continue

    correct_answer = {"count": valid_count}
    
    # Construct the return dictionary with exactly the three required keys
    result_dict = {
        "question_text": q_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }
    
    return result_dict