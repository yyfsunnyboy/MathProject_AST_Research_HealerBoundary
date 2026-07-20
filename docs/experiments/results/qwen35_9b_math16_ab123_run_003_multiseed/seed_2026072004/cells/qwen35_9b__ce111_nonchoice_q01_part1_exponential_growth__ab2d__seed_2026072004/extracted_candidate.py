from typing import Dict, Any
import math
from core.prompts.domain_function_library import IntegerOps

def generate(level=1, **kwargs):
    frozen_params = {"days": 15, "hours_per_generation": 20, "initial": 1, "split_factor": 4}
    
    # Calculate the number of generations based on days and hours per generation
    total_hours = frozen_params["days"] * 24
    num_generations = int(total_hours / frozen_params["hours_per_generation"])
    
    # Initial population count from kwargs or default if not present in logic context, 
    # but task says 'initial' is a frozen param. We use the formula: N(t) = initial * (split_factor ^ generations)
    # However, usually exponential growth tasks ask for final amount after specific time steps defined by params.
    
    base_count = IntegerOps.fmt_num(frozen_params["initial"])
    split_val = IntegerOps.safe_eval(str(frozen_params["split_factor"]))
    gen_steps = num_generations
    
    # Calculate total generations count integer result
    if gen_steps < 0:
        final_amount = frozen_params["initial"]
    else:
        final_amount = int(IntegerOps.safe_eval(str(base_count) + " * (" + str(split_val) + "**" + str(gen_steps) + ")"))

    # Construct the JSON-compatible answer dict with 'k' being the integer result of growth calculation
    correct_answer = {"k": final_amount}
    
    question_text = (f"Determine $k$, where a population starts at {IntegerOps.fmt_num(frozen_params['initial'])}, "
                     f"grows exponentially by splitting every {IntegerOps.fmt_num(frozen_params['hours_per_generation'])} hours, "
                     f"for a duration of {IntegerOps.fmt_num(frozen_params['days'])} days. The split factor is 4.")

    return {"question_text": question_text, "correct_answer": correct_answer, "oracle_payload": frozen_params}