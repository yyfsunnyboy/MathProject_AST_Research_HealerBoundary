from typing import Dict, Any
import sys
sys.path.insert(0, '.')
try:
    from core.prompts.domain_function_library import IntegerOps
except ImportError:
    class IntegerOps:
        @staticmethod
        def safe_eval(expr):
            try:
                result = eval(expr)
                if isinstance(result, bool) or (isinstance(result, float) and not (result.is_integer() or False)): # simplistic check for non-int floats that shouldn't happen in simple math usually but let's be strict on int return
                    raise ValueError("Result is not an integer")
                return result
            except Exception:
                raise ValueError(f"Failed to evaluate expression safely: {expr}")

        @staticmethod
        def fmt_num(n):
            if isinstance(n, float) and n.is_integer():
                return str(int(n))
            return str(n)

def generate(level=1, **kwargs) -> Dict[str, Any]:
    frozen_params = kwargs.get("frozen_sampled_parameters", {"base": -3, "exponent": 3})
    
    # Ensure we use the frozen parameters exactly as provided in the contract context if passed, 
    # otherwise default to the task specification's frozen sample.
    base_val = frozen_params.get("base")
    exponent_val = frozen_params.get("exponent")
    
    # Calculate answer using safe_eval and fmt_num for domain compliance
    expr_str = f"{IntegerOps.fmt_num(base_val)}**{IntegerOps.fmt_num(exponent_val)}"
    correct_answer_int = IntegerOps.safe_eval(expr_str)
    
    question_text = (f"What is the value of $\\text{{base}}$ raised to the power of $\\text{{exponent}}$, "
                     f"where base equals {IntegerOps.fmt_num(base_val)} and exponent equals {IntegerOps.fmt_num(exponent_val)}?").replace("base", str(base_val)).replace("exponent", str(exponent_val)) \
    # Re-constructing the latex properly for negative bases to ensure clarity in LaTeX math mode if needed, 
    # but standard text representation with $ signs is requested. Let's make it explicit:
    
    question_text = f"Calculate ${base_val}^{exponent_val}$."

    return {
        "question_text": question_text.replace("$", "\\$").replace("{\\text{", "{\\\\text{").replace("}", "}"), # Simple fix for latex delimiters if needed, but standard is $x$. Let's stick to simple mathjax compatible format: ${base}^{exponent}$ -> \${...}\$
        "correct_answer": correct_answer_int,
        "oracle_payload": frozen_params
    }

# Refining the question_text generation for strict LaTeX delimiters as per instruction "formal LaTeX delimiters"
def generate(level=1, **kwargs) -> Dict[str, Any]:
    try:
        from core.prompts.domain_function_library import IntegerOps
    except ImportError:
        class IntegerOps:
            @staticmethod
            def safe_eval(expr):
                return eval(expr.replace(" ", ""))
            @staticmethod
            def fmt_num(n):
                if isinstance(n, float) and n.is_integer():
                    return str(int(n))
                return str(n)

    frozen_params = kwargs.get("frozen_sampled_parameters", {"base": -3, "exponent": 3})
    
    base_val = frozen_params["base"]
    exponent_val = frozen_params["exponent"]
    
    # Use domain API for formatting numbers and evaluating the expression to get correct_answer
    formatted_base = IntegerOps.fmt_num(base_val)
    formatted_exponent = IntegerOps.fmt_num(exponent_val)
    
    # Construct LaTeX string manually with formal delimiters $...$ or \[...\] usually, 
    # instruction says "formal LaTeX delimiters where math appears". Standard is $.
    question_text = f"Calculate the value of ${formatted_base}^{{{formatted_exponent}}}$."
    
    correct_answer_int = IntegerOps.safe_eval(f"{formatted_base}**{formatted_exponent}")
    
    return {
        "question_text": question_text,
        "correct_answer": correct_answer_int,
        "oracle_payload": frozen_params
    }