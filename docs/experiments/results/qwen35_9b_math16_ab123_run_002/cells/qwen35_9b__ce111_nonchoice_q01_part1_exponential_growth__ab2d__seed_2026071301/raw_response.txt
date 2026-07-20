from typing import Dict, Any
import json
# Simulating the required imports from a hypothetical module structure as per instructions
try:
    from core.prompts.domain_function_library import IntegerOps
except ImportError:
    # Fallback implementation if the specific library is not available in this environment
    class IntegerOps:
        @staticmethod
        def safe_eval(expr):
            allowed_names = {"__builtins__": {}}
            try:
                result = eval(expr, allowed_names)
                return int(result) if isinstance(result, (int, float)) and not isinstance(result, bool) else result
            except Exception as e:
                raise ValueError(f"Safe evaluation failed for '{expr}': {e}")

        @staticmethod
        def fmt_num(n):
            # Ensure integer formatting without decimal points unless necessary
            if n == int(n):
                return str(int(n))
            else:
                return str(float(n))

def generate(level=1, **kwargs) -> Dict[str, Any]:
    """
    Generates a question about exponential growth based on frozen parameters.
    
    Returns a dict with exactly 'question_text', 'correct_answer', and 'oracle_payload'.
    """
    # Extract frozen sampled parameters from kwargs or defaults if not provided in call args directly
    # The prompt specifies "Frozen sampled parameters" which act as the ground truth for this specific run.
    # We must ensure we use these exact values: {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    frozen_params = {
        "days": 15, 
        "hours_per_generation": 20, 
        "initial": 1, 
        "split_factor": 4
    }
    
    # Override with kwargs if the caller explicitly provides different values for a dynamic test case?
    # The prompt says "Preserve frozen parameters exactly", implying we should use these specific ones.
    # However, standard function behavior allows overriding via **kwargs unless strictly forbidden.
    # Given "Frozen sampled parameters" context usually implies fixed inputs for the task instance:
    
    days = frozen_params.get("days")
    hours_per_generation = frozen_params.get("hours_per_generation")
    initial = frozen_params.get("initial")
    split_factor = frozen_params.get("split_factor")

    # Calculate total generations based on hours per day and hours per generation logic.
    # Usually: Total Hours in days * (1 / hours_per_generation) -> Generations? 
    # Or does it imply continuous growth where each 'hour' passes, a split happens every X hours?
    # Standard exponential model for discrete steps over time:
    # If we assume the organism splits every `hours_per_generation` within the day cycle.
    
    total_hours = days * 24  # Assuming standard 24h day unless specified otherwise (not in frozen params)
    generations_count = int(total_hours / hours_per_generation) + 1 if initial > 0 else 0
    
    # However, looking at typical "exponential growth" tasks with these specific param names:
    # It often implies N(t) = Initial * SplitFactor^(t/generation_time).
    # Let's calculate the number of splits that occur.
    
    total_hours_available = days * 24
    num_splits = int(total_hours_available / hours_per_generation)
    
    if initial > 0:
        final_count = IntegerOps.safe_eval(f"{initial} * {split_factor} ** {num_splits}")
    else:
        final_count = 0
        
    # Format the number for correctness_answer['k'] as int per spec "correct_answer must be a JSON-compatible dict with exactly k (int)"
    correct_k = IntegerOps.safe_eval(f"{initial} * {split_factor} ** {num_splits}") if initial > 0 else 0
    
    question_text = f"An organism starts with an initial population of {IntegerOps.fmt_num(initial)} individuals. It splits every {hours_per_generation} hours for a duration of {days} days (assuming 24-hour days). If the split factor is {split_factor}, what is the final population count? Express your answer as k."
    
    correct_answer = {"k": int(correct_k) if not isinstance(correct_k, bool) else None} # Ensure it's treated correctly
    
    oracle_payload = frozen_params

    return {
        "question_text": question_text,
        "correct_answer": correct_answer,
        "oracle_payload": oracle_payload
    }