from typing import Dict, Any
import sys

# Mocking required imports if not present in standard environment for this snippet context
try:
    from core.prompts.domain_function_library import IntegerOps
except ImportError:
    class IntegerOps:
        @staticmethod
        def safe_eval(expr):
            # For integers and simple arithmetic, eval is sufficient but wrapped to avoid code exec risks if passed strings that aren't math
            allowed_chars = set("0123456789+-*/(). ")
            s_str = str(expr)
            if not all(c in allowed_chars for c in s_str):
                raise ValueError(f"Unsafe characters found: {s_str}")
            try:
                result = eval(s_str, {"__builtins__": {}}, {})
                # Ensure float is converted to int if it's a whole number for correct_answer structure
                return int(result) if isinstance(result, float) and result.is_integer() else result
            except Exception as e:
                raise ValueError(f"Evaluation failed: {e}") from e

        @staticmethod
        def fmt_num(n):
            # Returns formatted string representation of integer/float for LaTeX embedding or display
            return str(int(n)) if isinstance(n, float) and n.is_integer() else f"{n:g}"


def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Extracting parameters; if passed via kwargs but conflicting with frozen (unlikely per spec), use frozen.
    days = frozen_params.get("days", 1)
    hours_per_generation = frozen_params.get("hours_per_generation", 20)
    initial = frozen_params.get("initial", 1)
    split_factor = frozen_params.get("split_factor", 4)

    # Logic for exponential growth: generations_count based on time elapsed vs generation cycle? 
    # Specification context implies calculating final population k after 'days' if the model runs continuously or discrete.
    # Usually, in these problems with integer constraints and specific "frozen sampled parameters", 
    # we calculate total generations occurred within a period (e.g., days), then apply split_factor^generations * initial.
    
    # Assumption: The task is to find k after `days` number of units where each unit allows one generation? 
    # OR, given 'hours_per_generation', and input is 'days'. We need total hours in 'days' (assuming 24h day unless specified otherwise).
    # Standard physics/math problem assumption: Day = 24 hours.
    
    hours_in_day = 24
    total_hours = days * hours_in_day
    
    if split_factor > 1 and initial > 0:
        generations_occurred = int(total_hours / hours_per_generation)
        k = initial * (split_factor ** generations_occurred)
        
        # Using IntegerOps for safety/formatting as per domain rules, though simple calculation here is integer math.
        calculated_k_int = IntegerOps.safe_eval(f"{initial} * ({split_factor} ** {generations_occurred})")
    else:
        k = initial
        
    correct_answer_dict = {"k": int(k)}

    question_text_latex = (
        r"An organism starts with an \text{initial count of } $N_0 = $" + 
        IntegerOps.fmt_num(initial) + 
        r". It splits every \text{$H$} hours, where each split multiplies the population by a factor of $S$. " +
        r"If $24$-hour days are used, how many organisms exist after \text{$D = $" + 
        IntegerOps.fmt_num(days) + 
        r"}" + 
        r"$\text{days}$? Express your answer as an integer } k.\\n " +
        r"(Note: Use $S =" + IntegerOps.fmt_num(split_factor) + r", H = $" + 
        IntegerOps.fmt_num(hours_per_generation) + r")"
    )

    question_text_latex += f"Given the parameters, calculate the final population."

    oracle_payload_dict = frozen_params.copy()

    result_obj = {
        "question_text": question_text_latex.strip(),
        "correct_answer": correct_answer_dict,
        "oracle_payload": oracle_payload_dict
    }
    
    return result_obj