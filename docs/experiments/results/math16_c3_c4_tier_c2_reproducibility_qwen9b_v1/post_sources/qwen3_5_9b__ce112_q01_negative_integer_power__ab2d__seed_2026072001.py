from typing import Dict, Any
import sys
sys.path.insert(0, '/app')
try:
    from core.prompts.domain_function_library import IntegerOps
except ImportError:
    class IntegerOps:
        @staticmethod
        def safe_eval(expr):
            try:
                result = eval(expr)
                if isinstance(result, bool) or (isinstance(result, float) and not result.is_integer()):
                    raise ValueError("Non-integer/bool result")
                return int(result)
            except Exception as e:
                raise ValueError(f"Evaluation failed: {e}")

        @staticmethod
        def fmt_num(n):
            if isinstance(n, bool):
                raise TypeError("Boolean not allowed in formatting for this task context")
            return str(int(n))

def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = kwargs.get('frozen_sampled_parameters', {"base": -3, "exponent": 3})
    
    base_val = frozen_params["base"]
    exponent_val = frozen_params["exponent"]
    
    # Compute the result using IntegerOps.safe_eval to adhere to domain API constraints
    expr_str = f"{IntegerOps.fmt_num(base_val)} ** {IntegerOps.fmt_num(exponent_val)}"
    correct_answer_int = IntegerOps.safe_eval(expr_str)
    
    question_text = (
        r"What is the value of $(-3)^{3}$?"
    )
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_int,
        "oracle_payload": frozen_params
    }