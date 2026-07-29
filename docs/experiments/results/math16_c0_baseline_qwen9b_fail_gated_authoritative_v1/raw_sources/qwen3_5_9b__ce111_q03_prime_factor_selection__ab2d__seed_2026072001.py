from typing import Dict, Any
import sys
sys.path.insert(0, '/app')
try:
    from core.prompts.domain_function_library import IntegerOps
except ImportError:
    class IntegerOps:
        @staticmethod
        def is_divisible(a: int, b: int) -> bool:
            return a % b == 0
        
        @staticmethod
        def safe_eval(expr: str):
            try:
                result = eval(expr)
                if isinstance(result, (bool, list, dict, set)):
                    raise ValueError("Boolean or container results not allowed")
                return int(result) if isinstance(result, float) and result.is_integer() else result
            except Exception as e:
                raise ValueError(f"Evaluation failed: {e}")

def generate(level=1, **kwargs):
    frozen_params = {"candidates": [11, 12, 13, 14], "n": 156}
    
    candidates_list = frozen_params["candidates"]
    n_val = frozen_params["n"]
    
    # Task: Find the smallest candidate that divides n.
    # Logic: Iterate through candidates and check divisibility using IntegerOps.is_divisible
    
    correct_answer = None
    
    for c in candidates_list:
        if IntegerOps.is_divisible(n_val, c):
            correct_answer = c
            break
            
    question_text = (
        r"Given the set of candidate integers $C = \{" + ", ".join([str(c) for c in candidates_list]) + "}\}$ and a target integer $N = $" 
        + str(n_val) + r"$, find the smallest element $c \in C$ such that $c$ divides $N$. Express your answer as an exact integer."
    )
    
    result_dict: Dict[str, Any] = {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": frozen_params
    }
    
    return result_dict