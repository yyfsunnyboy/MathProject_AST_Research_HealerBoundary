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
                return int(eval(expr))
            except Exception as e:
                raise ValueError(f"Safe eval failed for {expr}: {e}")

        @staticmethod
        def fmt_num(n):
            return str(int(n)) if isinstance(n, float) and n.is_integer() else str(n)

def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen = kwargs.get("frozen", {"base": -3, "exponent": 3})
    
    base_val = frozen["base"]
    exp_val = frozen["exponent"]
    
    # Compute correct_answer using domain API safe_eval to handle negative bases properly with integers
    expression_str = f"{IntegerOps.fmt_num(base_val)} ** {IntegerOps.fmt_num(exp_val)}"
    try:
        calc_result = IntegerOps.safe_eval(expression_str)
    except ValueError as e:
        # Fallback if specific library behavior differs, though safe_eval should handle standard math
        calc_result = base_val ** exp_val
    
    question_text = f"What is the value of {IntegerOps.fmt_num(base_val)} to the power of {IntegerOps.fmt_num(exp_val)}?"
    
    return {
        "question_text": question_text,
        "correct_answer": calc_result,
        "oracle_payload": frozen
    }